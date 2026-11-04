"""Google Zanzibar: Relationship-Based Access Control (ReBAC) Graph Engine.

Educational Simulator vs. Production Google Zanzibar Architecture:
-------------------------------------------------------------------
1. Educational Simulator (This Module):
   - In-memory relationship tuple store (`(object, relation) -> Set[user/userset]`).
   - Breadth-First Search (BFS) graph traversal with visited sets for cycle detection.
   - Evaluates direct relations, userset rewrites (inheritance: owner -> editor -> viewer),
     and subject-set group memberships in pure Python.
   - Fail-closed security design: if the authorization service is unavailable, all checks fail closed.

2. Production Google Zanzibar Architecture (Global Distributed System):
   - Global Scale & TrueTime: Stores trillions of relation tuples and processes millions of
     QPS globally across Google services (Drive, Cloud IAM, YouTube, Maps). Relies on
     Google Cloud Spanner with TrueTime atomic/GPS synchronized clocks for externally consistent reads.
   - Zookies (Consistency Tokens): Clients supply opaque snapshot tokens ("zookies") containing
     a Spanner timestamp to ensure authorization checks reflect a snapshot at least as fresh
     as the requested content version, completely preventing the "New Enemy" problem (stale ACL reads).
   - Leopard Indexing System: Zanzibar precomputes and flattens transitive group reachability
     into an offline indexing layer called Leopard. Reachability checks evaluate in sub-millisecond
     time via set-intersection operations rather than live graph traversals.
   - Distributed Call Graphs & Caching: Traversal trees are executed across thousands of RPC
     workers with deduplicated sub-problem evaluation and multi-level distributed caches.

Foundational Principles:
------------------------
1. Relation Tuples:
   Expressed as:
       `namespace:object_id#relation@user`
   or with Subject Sets (Usersets):
       `namespace:object_id#relation@subject_namespace:subject_id#subject_relation`
   Examples:
       `doc:101#owner@user:alice`
       `doc:101#viewer@group:engineering#member`
       `group:engineering#member@user:bob`

2. Userset Rewrite Rules (Inheritance):
   Defines how relations are derived from other relations on the same object or computed usersets.
   Example:
       `viewer` := _this OR computed_userset(relation='editor')
       `editor` := _this OR computed_userset(relation='owner')

3. Graph Traversal with Cycle Detection:
   Resolves `check(user, relation, object)` by exploring the directed authorization graph
   using Breadth-First Search (BFS) or Depth-First Search (DFS) while tracking visited
   sub-problems to prevent infinite recursion on cyclical group hierarchies.
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass(frozen=True)
class RelationTuple:
    """Canonical Zanzibar Relation Tuple representation."""
    object_namespace: str
    object_id: str
    relation: str
    # Subject: either an individual user ("user:alice") or a userset ("group:eng#member")
    user: str

    @property
    def object_str(self) -> str:
        return f"{self.object_namespace}:{self.object_id}"

    @property
    def is_subject_set(self) -> bool:
        return "#" in self.user

    def parse_subject_set(self) -> Tuple[str, str, str]:
        """Parses 'namespace:id#relation' into (namespace, id, relation)."""
        obj_part, relation = self.user.split("#", 1)
        ns, obj_id = obj_part.split(":", 1)
        return ns, obj_id, relation


@dataclass
class RelationRule:
    """Rule defining how a relation is satisfied (direct, computed, or union)."""
    inherits_from: List[str] = field(default_factory=list)


@dataclass
class NamespaceConfig:
    """Configuration schema for an object namespace."""
    name: str
    # relation_name -> RelationRule
    rules: Dict[str, RelationRule] = field(default_factory=dict)


class ZanzibarEngine:
    """High-performance ReBAC authorization engine simulating Google Zanzibar."""

    def __init__(self) -> None:
        # (object_str, relation) -> list of users/usersets
        self.tuples: Dict[Tuple[str, str], Set[str]] = {}
        self.namespace_configs: Dict[str, NamespaceConfig] = {}
        self.is_available: bool = True
        self._setup_default_configs()

    def _setup_default_configs(self) -> None:
        """Sets up standard enterprise inheritance rules:

        owner -> editor -> viewer
        """
        doc_cfg = NamespaceConfig(name="doc")
        doc_cfg.rules["owner"] = RelationRule(inherits_from=[])
        doc_cfg.rules["editor"] = RelationRule(inherits_from=["owner"])
        doc_cfg.rules["viewer"] = RelationRule(inherits_from=["editor"])
        self.register_namespace(doc_cfg)

        group_cfg = NamespaceConfig(name="group")
        group_cfg.rules["member"] = RelationRule(inherits_from=[])
        self.register_namespace(group_cfg)

    def register_namespace(self, config: NamespaceConfig) -> None:
        self.namespace_configs[config.name] = config

    def write_tuple(self, tuple_obj: RelationTuple) -> None:
        """Stores a relation tuple in the ACL database."""
        key = (tuple_obj.object_str, tuple_obj.relation)
        if key not in self.tuples:
            self.tuples[key] = set()
        self.tuples[key].add(tuple_obj.user)

    def delete_tuple(self, tuple_obj: RelationTuple) -> None:
        """Deletes a relation tuple."""
        key = (tuple_obj.object_str, tuple_obj.relation)
        if key in self.tuples and tuple_obj.user in self.tuples[key]:
            self.tuples[key].remove(tuple_obj.user)
            if not self.tuples[key]:
                del self.tuples[key]

    def check(self, user: str, relation: str, object_str: str) -> bool:
        """Evaluates whether `user` holds `relation` on `object_str`.

        Utilizes BFS traversal over the relation graph with cycle detection.
        Fails closed with RuntimeError if the ReBAC service is marked unavailable.
        """
        if not self.is_available:
            raise RuntimeError("Zanzibar authorization service unavailable")

        # Ensure user format has prefix, e.g. "user:alice"
        target_user = user if ":" in user else f"user:{user}"

        # State queue: (current_object_str, current_relation)
        queue = deque([(object_str, relation)])
        visited: Set[Tuple[str, str]] = set()

        while queue:
            curr_obj, curr_rel = queue.popleft()
            state_key = (curr_obj, curr_rel)

            if state_key in visited:
                continue
            visited.add(state_key)

            # 1. Direct and Subject Set check in tuple database
            subjects = self.tuples.get((curr_obj, curr_rel), set())

            # Direct match check
            if target_user in subjects:
                return True

            # Subject set expansion (e.g., curr_obj#curr_rel -> group:dev#member)
            for subject in subjects:
                if "#" in subject:
                    sub_obj, sub_rel = subject.split("#", 1)
                    if (sub_obj, sub_rel) not in visited:
                        queue.append((sub_obj, sub_rel))

            # 2. Relation Rewrite / Inheritance check
            # e.g., if checking for 'viewer', also explore 'editor' and 'owner'
            if ":" in curr_obj:
                ns, _ = curr_obj.split(":", 1)
                config = self.namespace_configs.get(ns)
                if config and curr_rel in config.rules:
                    rule = config.rules[curr_rel]
                    for parent_rel in rule.inherits_from:
                        if (curr_obj, parent_rel) not in visited:
                            queue.append((curr_obj, parent_rel))

        return False

    def list_authorized_objects(
        self, user: str, relation: str, namespace: str
    ) -> List[str]:
        """Return all object IDs in `namespace` that `user` can access with `relation`."""
        all_objects = set()
        for (obj_str, _) in self.tuples.keys():
            if obj_str.startswith(f"{namespace}:"):
                all_objects.add(obj_str)

        authorized = []
        for obj in all_objects:
            if self.check(user, relation, obj):
                authorized.append(obj)
        return sorted(authorized)
