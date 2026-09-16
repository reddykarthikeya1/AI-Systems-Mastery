# Module Troubleshooting & Production Edge Cases: Module_05_SOLID_Principles_Clean_Architecture

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. Direct Database Coupling Inside Domain Entities

### 🚨 The Bug & Symptoms
Importing ORM models directly inside domain aggregate roots breaks testability and violates Clean Architecture.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Domain entities must be plain Python dataclasses; database operations must be isolated behind Repository interfaces.

---

## 2. Floating-Point Money Value Object Corruption

### 🚨 The Bug & Symptoms
Using `float` for prices causes `$19.99 + $0.01` to evaluate to `$20.000000000000004`, causing ledger reconciliation failures.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Use integer cents (`1999` cents) or `decimal.Decimal` with strict rounding rules.

---

## 3. Anemic Domain Model Anti-Pattern

### 🚨 The Bug & Symptoms
Placing all business rules in service classes while domain classes are passive property bags leads to duplicated logic and fragmented invariants.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Encapsulate business invariants directly inside Aggregate Root methods (`order.add_item()`).

---

