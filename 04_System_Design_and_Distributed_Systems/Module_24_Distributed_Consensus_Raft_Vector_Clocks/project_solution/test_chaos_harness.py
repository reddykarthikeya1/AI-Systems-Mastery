"""Tests for the chaos harness.

Every test here asserts **safety**, not liveness. Raft is permitted to stop
making progress while the cluster is partitioned; it is never permitted to
commit two different values at the same log index.

The final assertion of most tests is `cluster.divergence() == []`.
"""

from __future__ import annotations

import pytest
from chaos_harness import ChaosCluster, ChaosNetwork
from raft_cluster_engine import RaftRole

FIVE = ["n1", "n2", "n3", "n4", "n5"]


def fresh(seed: int = 0) -> ChaosCluster:
    return ChaosCluster(node_ids=list(FIVE), seed=seed)


# ---------------------------------------------------------------------------
# the network itself
# ---------------------------------------------------------------------------


def test_partition_must_account_for_every_node():
    network = ChaosNetwork(FIVE)
    with pytest.raises(ValueError):
        network.partition(["n1", "n2"], ["n3"])          # n4, n5 unaccounted for


def test_a_node_cannot_be_in_two_partitions():
    network = ChaosNetwork(FIVE)
    with pytest.raises(ValueError):
        network.partition(["n1", "n2", "n3"], ["n3", "n4", "n5"])


def test_partition_blocks_both_directions():
    network = ChaosNetwork(FIVE)
    network.partition(["n1", "n2", "n3"], ["n4", "n5"])
    assert network.same_side("n1", "n2")
    assert not network.same_side("n1", "n4")
    assert not network.same_side("n4", "n1")
    network.heal()
    assert network.same_side("n1", "n4")


def test_one_way_block_is_asymmetric():
    network = ChaosNetwork(FIVE)
    network.block_one_way("n1", "n2")
    assert not network.deliver("n1", "n2")
    assert network.deliver("n2", "n1"), "the reverse direction still works"


def test_loss_rate_is_deterministic_for_a_seed():
    def run(seed: int) -> list[bool]:
        network = ChaosNetwork(FIVE, seed=seed)
        network.set_loss(0.5)
        return [network.deliver("n1", "n2") for _ in range(50)]

    assert run(7) == run(7), "same seed, same faults - a failure must reproduce"
    assert run(7) != run(8)


def test_loss_rate_is_rejected_outside_zero_to_one():
    network = ChaosNetwork(FIVE)
    with pytest.raises(ValueError):
        network.set_loss(1.5)


def test_stats_account_for_every_attempt():
    network = ChaosNetwork(FIVE, seed=1)
    network.set_loss(0.3)
    network.partition(["n1", "n2", "n3"], ["n4", "n5"])
    for _ in range(100):
        network.deliver("n1", "n2")
        network.deliver("n1", "n4")
    stats = network.stats
    assert stats.attempted == 200
    assert stats.dropped_by_partition == 100, "every cross-partition send blocked"
    assert 0 < stats.dropped_by_loss < 100
    assert stats.delivered + stats.dropped_by_loss == 100


# ---------------------------------------------------------------------------
# elections under partition
# ---------------------------------------------------------------------------


def test_healthy_cluster_elects_a_leader():
    cluster = fresh()
    assert cluster.run_election("n1")
    assert cluster.leaders() == ["n1"]


def test_majority_side_elects_and_minority_side_cannot():
    """The 3/2 split. This is the whole reason the algorithm exists."""
    cluster = fresh()
    cluster.network.partition(["n1", "n2", "n3"], ["n4", "n5"])

    assert cluster.run_election("n1"), "3 of 5 is a majority"
    assert not cluster.elect_with_retries("n4", attempts=30), (
        "2 of 5 can never be a majority, however many times it tries")

    assert cluster.nodes["n4"].role != RaftRole.LEADER
    assert cluster.leaders() == ["n1"]


def test_an_even_split_elects_nobody():
    """Four nodes, split 2/2. Neither side has three."""
    cluster = ChaosCluster(node_ids=["n1", "n2", "n3", "n4"], seed=0)
    cluster.network.partition(["n1", "n2"], ["n3", "n4"])
    assert not cluster.elect_with_retries("n1", attempts=20)
    assert not cluster.elect_with_retries("n3", attempts=20)
    assert cluster.leaders() == [], "unavailable is correct here; two leaders is not"


def test_two_leaders_cannot_both_commit():
    """The split-brain test.

    An isolated old leader keeps believing it is the leader - nothing tells it
    otherwise. What it cannot do is commit, because commitment needs a majority
    and it cannot reach one.
    """
    cluster = fresh()
    assert cluster.run_election("n1")
    cluster.client_write("n1", "before-the-split")

    # n1 is cut off with one follower; the other three carry on.
    cluster.network.partition(["n1", "n2"], ["n3", "n4", "n5"])
    assert cluster.elect_with_retries("n3", attempts=30)

    # Both nodes now believe they are leaders.
    assert cluster.nodes["n1"].role == RaftRole.LEADER
    assert cluster.nodes["n3"].role == RaftRole.LEADER

    stale_ok, _ = cluster.client_write("n1", "written-by-the-stale-leader")
    fresh_ok, _ = cluster.client_write("n3", "written-by-the-real-leader")

    assert not stale_ok, "the minority leader must not be able to commit"
    assert fresh_ok, "the majority leader can"
    assert cluster.divergence() == [], "no index holds two different committed values"


# ---------------------------------------------------------------------------
# replication under partition and loss
# ---------------------------------------------------------------------------


def test_minority_leader_cannot_commit_anything():
    cluster = fresh()
    assert cluster.run_election("n1")
    cluster.network.partition(["n1"], ["n2", "n3", "n4", "n5"])
    for i in range(5):
        committed, index = cluster.client_write("n1", f"cmd{i}")
        assert not committed and index == -1
    assert cluster.nodes["n1"].commit_index == 0
    assert cluster.divergence() == []


def test_a_bare_majority_is_enough():
    """Exactly three of five reachable: commit succeeds. Two: it does not."""
    cluster = fresh()
    assert cluster.run_election("n1")
    cluster.network.partition(["n1", "n2", "n3"], ["n4", "n5"])
    assert cluster.client_write("n1", "quorum-of-three")[0]

    cluster.network.heal()
    cluster.network.partition(["n1", "n2"], ["n3", "n4", "n5"])
    assert not cluster.client_write("n1", "quorum-of-two")[0]


def test_commits_survive_the_partition_healing():
    cluster = fresh()
    assert cluster.run_election("n1")
    cluster.network.partition(["n1", "n2", "n3"], ["n4", "n5"])
    assert cluster.client_write("n1", "during-the-split")[0]

    cluster.network.heal()
    assert cluster.client_write("n1", "after-the-heal")[0]
    assert cluster.committed_commands("n1") == ["during-the-split", "after-the-heal"]
    assert cluster.divergence() == []


@pytest.mark.parametrize("loss", [0.1, 0.3, 0.5])
def test_safety_holds_under_message_loss(loss):
    """Liveness degrades with loss. Safety does not degrade at all."""
    cluster = fresh(seed=42)
    cluster.network.set_loss(loss)

    elected = cluster.elect_with_retries("n1", attempts=60)
    if elected:
        for i in range(10):
            cluster.client_write("n1", f"cmd{i}")

    assert cluster.divergence() == [], (
        f"split brain under {loss:.0%} loss - safety must not depend on the network")
    assert len(cluster.leaders()) <= 1


def test_asymmetric_reachability_does_not_produce_two_leaders():
    """n1 cannot reach anyone, but everyone can reach n1.

    A failure detector built on "can I see you" gets this wrong: n1 thinks the
    cluster is down, and the cluster thinks n1 is fine. Raft does not care,
    because n1 still has to collect votes it cannot collect.
    """
    cluster = fresh()
    for peer in FIVE[1:]:
        cluster.network.block_one_way("n1", peer)

    assert not cluster.elect_with_retries("n1", attempts=20)
    assert cluster.elect_with_retries("n2", attempts=20)
    assert cluster.leaders() == ["n2"]
    assert cluster.divergence() == []


# ---------------------------------------------------------------------------
# liveness, measured rather than assumed
# ---------------------------------------------------------------------------


def test_retries_recover_liveness_that_a_single_round_loses():
    """With 40% loss a single election round usually fails and retrying works.

    This is what randomised election timeouts buy you in real Raft, and it is
    the only liveness claim this harness makes.
    """
    single_round_successes = 0
    with_retries_successes = 0
    for seed in range(30):
        one = fresh(seed=seed)
        one.network.set_loss(0.4)
        single_round_successes += one.run_election("n1")

        many = fresh(seed=seed)
        many.network.set_loss(0.4)
        with_retries_successes += many.elect_with_retries("n1", attempts=25)

    assert single_round_successes < 30, "some single rounds must fail, or loss is not biting"
    assert with_retries_successes > single_round_successes, "retrying must help"


def test_latency_is_accounted_without_anyone_waiting():
    cluster = fresh()
    cluster.network.set_latency(base_ms=500, jitter_ms=0)
    cluster.run_election("n1")
    stats = cluster.network.stats
    assert stats.delivered > 0
    assert stats.total_latency_ms == pytest.approx(stats.delivered * 500)
