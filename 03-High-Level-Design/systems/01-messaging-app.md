# HLD Case Study 1: Real-Time Messaging Platform (WhatsApp / Discord)

> **Key Focus Areas:** Real-time WebSockets, message delivery guarantees (sent, delivered, read), distributed connection servers, and offline message synchronization.

---

## 1. Problem Statement & Requirements

Design a global real-time chat platform supporting 1-on-1 and group messaging with delivery receipts.

### Functional Requirements:
1. Low-latency 1-on-1 and group messaging ($< 100\text{ms}$ delivery).
2. Message status tracking: `Sent` $\rightarrow$ `Delivered` $\rightarrow$ `Read`.
3. Support offline users (queue messages until user reconnects).
4. Media sharing (images/videos up to 100MB).

### Non-Functional Requirements:
1. High availability ($99.99\%$).
2. Low latency worldwide.
3. End-to-End Encryption (E2EE) support.

---

## 2. Back-of-the-Envelope Estimations

* **DAU:** $500 \text{ Million}$ active users.
* **Message Volume:** 40 messages per user/day $\rightarrow 20 \text{ Billion messages/day}$.
* **Write QPS:** $\frac{20 \times 10^9}{10^5} \approx \mathbf{200,000 \text{ QPS}}$ (Peak = $400,000\text{ QPS}$).
* **Storage per day:** Average message size $100 \text{ bytes} \rightarrow 20 \text{ Billion} \times 100 \text{ bytes} = \mathbf{2 \text{ TB/day}}$ text storage.
* **Concurrent Connections:** $\sim 50 \text{ Million}$ simultaneous WebSocket connections.

---

## 3. High-Level Architecture Diagram

```mermaid
flowchart TD
    ClientA["Sender Client A"] -->|1. WebSocket Connection| WS_Gateway["WebSocket Gateway Cluster<br/>(Maintains open TCP sockets)"]
    WS_Gateway --> SessionSvc["Session Registry (Redis Cluster)<br/>User -> Connected WS Gateway IP"]
    WS_Gateway --> MsgSvc["Message Ingestion Service"]
    MsgSvc --> Kafka["Kafka Topic: chat_events"]
    
    Kafka --> MsgStoreWorker["Message Store Worker"]
    MsgStoreWorker --> Cassandra["Cassandra Cluster (Messages DB)<br/>(Partition: chat_id, Cluster: message_id DESC)"]

    Kafka --> PushRouter["Push / Route Worker"]
    PushRouter --> SessionSvc
    PushRouter -->|If Receiver Online| WS_Gateway_B["Receiver's WS Gateway"]
    WS_Gateway_B --> ClientB["Receiver Client B"]
    
    PushRouter -->|If Receiver Offline| APNS["APNs / FCM (Push Notification Gateway)"]
```

---

## 4. Database Schema Design (Apache Cassandra)

Cassandra is selected because it excels at ultra-high write throughput (LSM-Tree) and sequential range queries by time:

```sql
CREATE TABLE messages (
    chat_id uuid,
    message_id timeuuid, -- Guarantees time-ordered monotonic sorting
    sender_id uuid,
    content text,
    media_url text,
    status text, -- SENT, DELIVERED, READ
    created_at timestamp,
    PRIMARY KEY ((chat_id), message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

---

## 5. Deep-Dive: Delivery Guarantees & Sync

```mermaid
sequenceDiagram
    autonumber
    actor A as User A
    participant Svr as Message Server
    participant DB as Cassandra
    actor B as User B

    A->>Svr: send_message(payload, client_msg_id)
    Svr->>DB: persist_message(status = SENT)
    Svr-->>A: ACK: status = SENT (Single checkmark)
    
    alt User B Online
        Svr->>B: deliver_message(payload)
        B-->>Svr: ACK: delivered
        Svr->>DB: update status = DELIVERED
        Svr-->>A: notification: status = DELIVERED (Double checkmarks)
    else User B Offline
        Note over Svr: Store in pending queue and trigger Push Notification
    end
```
