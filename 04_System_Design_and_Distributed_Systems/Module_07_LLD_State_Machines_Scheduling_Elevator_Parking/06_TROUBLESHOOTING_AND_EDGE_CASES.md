# Module Troubleshooting & Production Edge Cases: Module_07_LLD_State_Machines_Scheduling_Elevator_Parking

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. Door State Machine Invalid Transition

### 🚨 The Bug & Symptoms
Transitioning directly from `MOVING` to `DOOR_OPEN` while car speed > 0 simulates high-risk hardware failure.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Strictly enforce FSM transitions: `MOVING` -> `STOPPED` -> `DOORS_OPENING` -> `DOORS_OPEN`.

---

## 2. Nearest Car Dispatch Blindspot

### 🚨 The Bug & Symptoms
Assigning an elevator moving DOWN at floor 5 to a passenger at floor 6 because Euclidean distance is only 1 floor, causing huge turnaround delays.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Incorporate directional penalty: a car moving away must be penalized by twice the building height.

---

## 3. Over-Capacity Weight Sensor Bypass

### 🚨 The Bug & Symptoms
Allowing an elevator car to accept new hall calls when weight capacity is >= 100%.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
When capacity threshold is reached, bypass all hall calls until internal drop-offs occur.

---

