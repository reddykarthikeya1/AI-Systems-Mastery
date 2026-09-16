# Module_21_Metaprogramming_Descriptors_Memory: Project Implementation Guide

**Deliverable:** a declarative database modeling framework utilizing descriptors, __init_subclass__, and automatic SQL DDL generation.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_mini_orm.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — Base Column Descriptor
Implement `Field` descriptor capturing column name via `__set_name__` and storing values on private instance attributes.

### Step 2 — Typed Descriptors
Implement `StringField`, `IntegerField`, and `FloatField` with runtime type and constraint validation in `__set__`.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_mini_orm.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Declarative Model Metaprogramming
Implement `Model.__init_subclass__` automatically discovering and registering all `Field` instances on the model class.

### Step 4 — SQL Schema & Query Generation
Implement `get_create_table_sql()` and `as_insert_sql()` generating standard SQL DDL and INSERT statements.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/mini_orm.py`, modify `Field.__set__` to store value on `self.val` instead of `setattr(instance, self.storage, value)`.
Run:
```bash
pytest ../project_solution/test_mini_orm.py -k test_instance_creation_and_insert_sql -v
```
Watch all instances overwrite each other's data due to descriptor sharing, then restore instance storage.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_mini_orm.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **ForeignKey Relationship Descriptor:** Implement a `ForeignKey(OtherModel)` descriptor resolving related records.
2. **Query Builder DSL:** Implement a chainable query builder: `User.filter(score__gt=90).limit(5)`.
3. **Dirty Field Tracking:** Track which fields were modified to emit minimal `UPDATE ... SET` statements.
4. **Metaclass Inheritance Alternative:** Compare `__init_subclass__` implementation against a type metaclass (`MetaModel`).

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_schema_generation` | Proves get_create_table_sql generates valid DDL with constraints |
| `test_instance_creation_and_insert_sql` | Proves model instantiation and SQL INSERT generation |
| `test_validation_constraints` | Proves type and max_length constraints reject invalid assignments |
| `test_missing_required_field_raises_value_error` | Proves non-nullable fields raise ValueError when omitted |
| `test_perf_model_instantiation_throughput` | Proves model instantiation and descriptor validation execute with high throughput |

---

## 🎓 You have mastered this module when you can…

- [ ] Implement data and non-data descriptors using __get__, __set__, and __delete__
- [ ] Use __set_name__ to automatically bind attribute names without explicit string duplication
- [ ] Store descriptor state on the instance rather than the descriptor to prevent cross-instance leaks
- [ ] Use __init_subclass__ as a cleaner, modern alternative to metaclasses for class registration
- [ ] Construct declarative domain-specific languages (DSLs) in pure Python
- [ ] Generate SQL statements programmatically from introspected class metadata
- [ ] Benchmark descriptor attribute access overhead against standard __dict__ lookups
