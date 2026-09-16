# Module Troubleshooting & Production Edge Cases: Module_00_System_Design_Fundamentals_Interview_Playbook

Here are the most critical production failure modes, concurrency traps, and architectural edge cases encountered in this domain, along with root cause analyses and hardened fixes.

---

## 1. Omission of Storage Replication Factor

### 🚨 The Bug & Symptoms
Capacity estimations calculate raw data volume and forget that Kafka, Cassandra, and HDFS require 3x replication plus 20% filesystem headroom.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Always multiply baseline disk storage by (Replication Factor / (1 - HeadroomMargin)).

---

## 2. Peak-to-Average QPS Ratio Blindspots

### 🚨 The Bug & Symptoms
Sizing servers for average daily QPS (e.g. 10M DAU / 86400 = 115 QPS) causes complete brownouts during lunch or marketing spikes.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Size for Peak QPS = Average QPS * Peak Multiplier (typically 3x to 5x for consumer apps).

---

## 3. Network Egress vs. Ingress Asymmetry

### 🚨 The Bug & Symptoms
Estimating symmetric network interfaces when read-heavy workloads (100:1) require 100x more outbound egress bandwidth than inbound ingress.

### 🔍 Why It Happens Under Production Load
In distributed and high-concurrency environments, naive assumptions about deterministic scheduling, network reliability, or hardware uniformity break down.

### 🛠️ The Production Fix & Invariant
Separate network links: `Egress = QPS_read * read_payload` vs `Ingress = QPS_write * write_payload`.

---

