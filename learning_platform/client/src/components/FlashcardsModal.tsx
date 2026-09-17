import React, { useState, useMemo, useEffect } from 'react';
import { useProgress } from '../hooks/useProgress';
import { soundService } from '../services/sound';
import { useFocusTrap } from '../hooks/useFocusTrap';

export interface FlashcardItem {
  id: string;
  category: 'Storage & DB' | 'Distributed Systems' | 'DSA' | 'Concurrency' | 'Networking';
  question: string;
  answer: string;
  keyTakeaway: string;
}

const FLASHCARD_DECK: FlashcardItem[] = [
  // Storage & Database Internals
  {
    id: 'srs-01',
    category: 'Storage & DB',
    question: 'Why do B+ Trees place all actual row data / payload pointers exclusively in leaf nodes?',
    answer: 'By keeping interior nodes lean (storing only indexing keys and page pointers), the branching factor (fanout) is maximized. A single 4KB page can hold hundreds of keys, keeping tree height shallow (3-4 levels for billions of rows) and minimizing disk random I/O. Furthermore, leaf nodes are linked into a doubly-linked list for ultra-fast sequential range scans.',
    keyTakeaway: 'High fanout + shallow tree height + linear sequential range scans.',
  },
  {
    id: 'srs-02',
    category: 'Storage & DB',
    question: 'What is the Write-Ahead Log (WAL) and why is it sequentially written before dirty pages are flushed?',
    answer: 'The WAL logs all mutations sequentially to disk before modifying in-memory buffer pool pages. Sequential writes are orders of magnitude faster than random page writes. In the event of a sudden power outage or crash, the database recovers complete state by replaying uncheckpointed WAL frames (ARIES recovery protocol).',
    keyTakeaway: 'Durability guarantee (D in ACID) without paying random disk I/O latency on transactions.',
  },
  {
    id: 'srs-03',
    category: 'Storage & DB',
    question: 'Compare B-Trees and Log-Structured Merge (LSM) Trees regarding Read vs Write amplification.',
    answer: 'B-Trees suffer from write amplification because modifying a single row requires rewriting an entire 4KB-16KB page to disk, but offer predictable 1-3 I/O point reads. LSM-trees (RocksDB, Cassandra) buffer writes entirely in-memory (MemTable) and append sequentially to disk (SSTables), providing immense write throughput at the cost of higher read amplification (must check MemTable + Bloom filters + multiple SSTable compaction levels).',
    keyTakeaway: 'B-Tree = Read-optimized (OLTP). LSM-Tree = High-write throughput & append-heavy workloads.',
  },
  {
    id: 'srs-04',
    category: 'Storage & DB',
    question: 'How does Multi-Version Concurrency Control (MVCC) eliminate read-write contention?',
    answer: 'Instead of acquiring locks on rows during reads, readers inspect a snapshot of data corresponding to their transaction read timestamp (xmin/xmax). Writers create a new tuple version with their transaction ID rather than overwriting in place. Readers never block writers, and writers never block readers.',
    keyTakeaway: 'Readers never lock out writers; historical tuple versions are periodically garbage-collected (VACUUM).',
  },
  {
    id: 'srs-05',
    category: 'Storage & DB',
    question: 'What is the difference between Clustered and Non-Clustered Indexes?',
    answer: 'A clustered index dictates the physical on-disk sort order of table rows (only 1 per table, typically the Primary Key). Non-clustered (secondary) indexes are auxiliary B-Trees whose leaf nodes store secondary keys mapped to the clustered index key (or row RID), requiring a secondary index lookup followed by a bookmark lookup.',
    keyTakeaway: 'Clustered index holds the actual row data at leaves; secondary indexes point to the primary key.',
  },

  // Distributed Systems & Consensus
  {
    id: 'srs-06',
    category: 'Distributed Systems',
    question: 'State the PACELC theorem and explain how it extends CAP.',
    answer: 'PACELC states: In the presence of a Partition (P), choose Availability (A) or Consistency (C); Else (E), choose Latency (L) or Consistency (C). CAP only describes degraded network partition behavior, whereas PACELC also explains trade-offs during normal operating conditions (e.g. Cassandra chooses PA/EL; DynamoDB/MongoDB can be configured).',
    keyTakeaway: 'During partitions: Trade A vs C. During normal times: Trade Latency vs Consistency.',
  },
  {
    id: 'srs-07',
    category: 'Distributed Systems',
    question: 'How does Raft prevent split-brain leader elections during network partitions?',
    answer: 'Raft requires a candidate node to secure votes from a strict majority (quorum = ⌊N/2⌋ + 1) of all nodes in the cluster. If an isolated partition contains fewer than a majority of nodes, it can never elect a leader or commit log entries. Furthermore, randomized election timers prevent split-vote deadlocks.',
    keyTakeaway: 'Majority quorum (N/2 + 1) ensures at most one partition can elect a leader in any given term.',
  },
  {
    id: 'srs-08',
    category: 'Distributed Systems',
    question: 'Why is Two-Phase Commit (2PC) considered a blocking protocol?',
    answer: 'If the transaction coordinator crashes after participants vote "YES" during the Prepare phase but before broadcasting "GLOBAL_COMMIT", participants are left in doubt and must hold locks indefinitely, blocking other concurrent transactions until the coordinator recovers.',
    keyTakeaway: 'Coordinator crash during the in-doubt window locks resources indefinitely; modern systems prefer Sagas.',
  },
  {
    id: 'srs-09',
    category: 'Distributed Systems',
    question: 'What is the Saga Pattern and how does it manage distributed transactions across microservices?',
    answer: 'A Saga decomposes a distributed transaction into a series of local transactions executed by individual services. Each service updates its local database and publishes an event/message. If a step fails, the Saga coordinates compensating transactions in reverse order to undo earlier changes, achieving eventual consistency without distributed 2PC locks.',
    keyTakeaway: 'Replaces distributed locks with sequential local transactions + explicit compensating undo steps.',
  },
  {
    id: 'srs-10',
    category: 'Distributed Systems',
    question: 'What information do Vector Clocks capture that Lamport Timestamps cannot?',
    answer: 'Lamport timestamps establish a total order of events but cannot determine whether two events are causally dependent or concurrent (happened concurrently without knowledge of each other). Vector clocks maintain an array of clocks per node: if V1[i] <= V2[i] for all i and strictly less for at least one, V1 causally precedes V2; otherwise, they conflict (concurrent).',
    keyTakeaway: 'Vector Clocks distinguish causality from true concurrent conflicts across independent nodes.',
  },
  {
    id: 'srs-11',
    category: 'Distributed Systems',
    question: 'How does Consistent Hashing minimize data movement during node additions/removals?',
    answer: 'Both keys and nodes are mapped onto a 360-degree hash ring using a cryptographic hash function. Keys are assigned to the first clockwise node. When a node is added or removed, only keys residing on the immediate adjacent segment (approx 1/N of total keys) need migration, unlike naive modulo hashing `hash(key) % N` which invalidates almost 100% of keys.',
    keyTakeaway: 'Only 1/N of keys are relocated upon node membership changes; virtual nodes ensure balanced distribution.',
  },

  // Data Structures & Algorithms
  {
    id: 'srs-12',
    category: 'DSA',
    question: 'Explain Floyd\'s Cycle Detection (Tortoise and Hare) and how to find the cycle start node.',
    answer: 'Slow pointer moves 1 step; Fast pointer moves 2 steps. If a cycle exists, they must collide inside the cycle in O(N) time and O(1) space. Upon collision, reset one pointer to head and advance both 1 step at a time; their new collision point is mathematically guaranteed to be the exact cycle entrance.',
    keyTakeaway: 'O(N) time, O(1) space cycle detection and entrance identification.',
  },
  {
    id: 'srs-13',
    category: 'DSA',
    question: 'When should you apply a Monotonic Stack vs a Two-Pointer approach?',
    answer: 'Use a Monotonic Stack when you need to identify the Next Greater Element, Next Smaller Element, or optimal subarray boundaries (e.g. Largest Rectangle in Histogram, Trapping Rain Water, Daily Temperatures) in linear O(N) time. Use Two-Pointers for sorted arrays, palindrome validation, or sliding interval windows with monotonic boundaries.',
    keyTakeaway: 'Monotonic Stack maintains sorted element invariants to resolve next/previous boundary problems in O(N).',
  },
  {
    id: 'srs-14',
    category: 'DSA',
    question: 'What is the difference between Dijkstra\'s and the A* Search algorithm?',
    answer: 'Dijkstra explores paths based solely on known exact distance from source `g(n)`, radiating equally in all directions. A* adds an admissible and consistent heuristic `h(n)` representing estimated cost to goal: `f(n) = g(n) + h(n)`. This directs the search frontier directly towards the target, drastically pruning the state space.',
    keyTakeaway: 'A* is Dijkstra informed by a heuristic function h(n) to prioritize target-directed exploration.',
  },
  {
    id: 'srs-15',
    category: 'DSA',
    question: 'What is the time complexity of Disjoint Set Union (DSU) with Path Compression and Union by Rank?',
    answer: 'Practically O(1) per operation: formally O(α(N)) where α is the inverse Ackermann function. For any imaginable physical universe input size (N < 10^80), α(N) < 5.',
    keyTakeaway: 'Near constant time O(α(N)) per find/union query.',
  },
  {
    id: 'srs-16',
    category: 'DSA',
    question: 'Explain how Boyer-Moore Majority Vote finds the majority element in O(1) auxiliary space.',
    answer: 'Initialize candidate and count = 0. Iterate through array: if count == 0, candidate = num. If num == candidate, increment count, else decrement count. Because the majority element appears > N/2 times, its count will never be entirely cancelled out by other non-majority elements.',
    keyTakeaway: 'O(N) time and O(1) space cancellation pairing algorithm.',
  },

  // Concurrency & Low-Level Architecture
  {
    id: 'srs-17',
    category: 'Concurrency',
    question: 'What are Coffman\'s Four Necessary and Sufficient Conditions for Deadlock?',
    answer: '1. Mutual Exclusion (non-shareable resources)\n2. Hold and Wait (process holds resource while requesting another)\n3. No Preemption (resources cannot be forcibly taken)\n4. Circular Wait (closed chain of processes waiting for each other).\nBreaking any single condition prevents deadlock entirely.',
    keyTakeaway: 'Prevent deadlock by breaking at least 1 of 4 conditions (e.g. strict resource ordering eliminates circular wait).',
  },
  {
    id: 'srs-18',
    category: 'Concurrency',
    question: 'How do Compare-And-Swap (CAS) hardware instructions achieve lock-free synchronization?',
    answer: 'CAS is an atomic CPU primitive: `CAS(address, expected_val, new_val)`. If the value at address equals expected_val, it atomically updates it to new_val and returns true; otherwise it returns false without modifying memory. Threads retry in a lock-free loop (`while (!CAS(...))`), eliminating OS kernel context switches and priority inversions.',
    keyTakeaway: 'Lock-free optimistic concurrency at hardware CPU instruction speed; watches out for ABA problem.',
  },
  {
    id: 'srs-19',
    category: 'Concurrency',
    question: 'What is false sharing in multi-core CPU architectures and how do you prevent it?',
    answer: 'When two threads on separate CPU cores concurrently modify independent variables that happen to reside on the same 64-byte L1/L2 cache line, the CPU cache coherence protocol (MESI) constantly invalidates the cache line across cores, causing severe performance degradation. Prevent it via cache-line padding (e.g. `@Contended` or 64-byte alignment padding).',
    keyTakeaway: 'Independent variables on the same CPU cache line cause invalidation storms; resolve with 64-byte padding.',
  },
  {
    id: 'srs-20',
    category: 'Concurrency',
    question: 'Explain the difference between Preemptive vs Cooperative Multitasking (e.g. OS threads vs Async Coroutines).',
    answer: 'Preemptive multitasking relies on OS kernel timer interrupts to forcibly pause and context-switch threads. Cooperative multitasking (Python asyncio, Node.js event loop, Go goroutines) relies on tasks explicitly yielding execution (`await` or I/O boundary). Cooperative switches are lightweight (nanoseconds vs microseconds) without kernel transition overhead.',
    keyTakeaway: 'Preemptive = OS kernel forced switches. Cooperative = Lightweight voluntary yielding at await points.',
  },

  // Networking & Web Architecture
  {
    id: 'srs-21',
    category: 'Networking',
    question: 'How does HTTP/2 multiplexing solve application-level head-of-line blocking, and what remains at the TCP layer?',
    answer: 'HTTP/2 breaks requests and responses into binary frames multiplexed over a single TCP connection, eliminating HTTP/1.1 pipeline head-of-line blocking. However, if a single TCP packet is dropped at the network layer, TCP stops all stream delivery until the missing packet is retransmitted, blocking all streams. HTTP/3 (QUIC over UDP) solves this by isolating packet loss per stream.',
    keyTakeaway: 'HTTP/2 multiplexes over 1 TCP socket; HTTP/3 (QUIC/UDP) removes TCP-layer packet drop blocking.',
  },
  {
    id: 'srs-22',
    category: 'Networking',
    question: 'Explain the purpose of the TCP TIME_WAIT state and why it lasts 2 * MSL (Maximum Segment Lifetime).',
    answer: 'The endpoint that actively initiates connection termination enters TIME_WAIT (typically 60-120 seconds). Purposes: 1. Ensure the final ACK was received by the peer (retransmitting if FIN is received again). 2. Prevent delayed lingering duplicate packets from a previous connection from corrupting a new socket with identical (IP, Port) tuple.',
    keyTakeaway: 'Guarantees clean graceful close and flushes duplicate stale packets out of the internet routing fabric.',
  },
];

interface FlashcardsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const FlashcardsModal: React.FC<FlashcardsModalProps> = ({ isOpen, onClose }) => {
  const { progress, updateSrsReview } = useProgress();
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [flipped, setFlipped] = useState<boolean>(false);

  const allCards = useMemo(() => {
    const custom = (progress.srs_custom_cards || []).map((c) => ({
      ...c,
      category: (c.category || 'Quiz Mistakes') as any,
    }));
    return [...custom, ...FLASHCARD_DECK];
  }, [progress.srs_custom_cards]);

  const categories = useMemo(() => {
    const base = ['All', 'Due Today', 'Storage & DB', 'Distributed Systems', 'DSA', 'Concurrency', 'Networking'];
    if ((progress.srs_custom_cards || []).length > 0) {
      base.splice(2, 0, 'Quiz Mistakes');
    }
    return base;
  }, [progress.srs_custom_cards]);

  const filteredCards = useMemo(() => {
    if (selectedCategory === 'All') return allCards;
    if (selectedCategory === 'Due Today') {
      return allCards.filter((c) => {
        const rev = progress.srs_card_reviews?.[c.id];
        return !rev || rev.next_review_epoch <= Date.now();
      });
    }
    if (selectedCategory === 'Quiz Mistakes') {
      return allCards.filter((c) => c.id.startsWith('mistake-') || (progress.srs_custom_cards || []).some((sc) => sc.id === c.id));
    }
    return allCards.filter((c) => c.category === selectedCategory);
  }, [selectedCategory, allCards, progress.srs_card_reviews]);

  const currentCard = filteredCards[currentIndex] || filteredCards[0];
  const cardReview = currentCard ? progress.srs_card_reviews?.[currentCard.id] : undefined;

  const trapRef = useFocusTrap(isOpen, onClose);

  if (!isOpen) return null;

  const handleNext = () => {
    soundService.playClick();
    setFlipped(false);
    setCurrentIndex((prev) => (prev + 1) % filteredCards.length);
  };

  const handlePrev = () => {
    soundService.playClick();
    setFlipped(false);
    setCurrentIndex((prev) => (prev - 1 + filteredCards.length) % filteredCards.length);
  };

  const handleFlip = () => {
    soundService.playClick();
    setFlipped(!flipped);
  };

  const handleRate = (rating: number) => {
    if (!currentCard) return;
    updateSrsReview(currentCard.id, rating);
    handleNext();
  };

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div 
        ref={trapRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="srs-modal-title"
        className="flex flex-col w-full max-w-3xl max-h-[90vh] bg-surface border border-border rounded-2xl shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-surface/60">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center font-bold text-base">
              🗂️
            </div>
            <div>
              <h2 id="srs-modal-title" className="text-base font-semibold text-fg flex items-center gap-2">
                Systems Engineering Spaced Repetition (SRS)
                <span className="px-2 py-0.5 text-xs rounded-full bg-amber-500/10 text-amber-600 dark:text-amber-400 font-mono">
                  SM-2 Algorithm
                </span>
              </h2>
              <p className="text-xs text-fg-muted">
                Lock in database internals, consensus protocols, algorithmic patterns, and low-level concurrency.
              </p>
            </div>
          </div>
          <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 p-1.5 rounded-lg text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition-colors" onClick={() => {
              soundService.playClick();
              onClose();
            }}
            aria-label="Close spaced repetition modal" >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Category Filter Pills */}
        <div className="flex items-center gap-2 px-6 py-2.5 bg-zinc-100/50 dark:bg-zinc-900/40 border-b border-border overflow-x-auto text-xs">
          {categories.map((cat) => (
            <button className={`focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1 rounded-full text-xs transition-all whitespace-nowrap ${
                selectedCategory === cat
                  ? 'bg-amber-500 text-zinc-950 font-semibold shadow-sm'
                  : 'bg-white dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200 dark:hover:bg-zinc-700 border border-zinc-200 dark:border-zinc-700'
              }`} key={cat}
              onClick={() => {
                soundService.playClick();
                setSelectedCategory(cat);
                setCurrentIndex(0);
                setFlipped(false);
              }} >
              {cat}
            </button>
          ))}
          <div className="ml-auto text-xs text-zinc-400 font-mono">
            {currentIndex + 1} / {filteredCards.length}
          </div>
        </div>

        {/* Card Body */}
        <div className="flex-1 p-6 overflow-y-auto flex flex-col justify-center items-center">
          {currentCard && (
            <div
              onClick={handleFlip}
              className="w-full max-w-2xl min-h-[300px] cursor-pointer p-8 rounded-2xl bg-zinc-50 dark:bg-zinc-950/80 border-2 border-dashed border-zinc-300 dark:border-zinc-800 hover:border-amber-500/50 transition-all flex flex-col justify-between shadow-inner group select-none"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-500/10 text-amber-600 dark:text-amber-400">
                    {currentCard.category}
                  </span>
                  {cardReview && (
                    <span className="text-xs font-mono text-zinc-400">
                      Reviewed: {cardReview.repetition}x • Interval: {cardReview.interval_days}d
                    </span>
                  )}
                </div>

                {!flipped ? (
                  <div className="mt-4">
                    <span className="text-xs font-mono uppercase tracking-wider text-zinc-400">Question</span>
                    <p className="mt-2 text-lg font-semibold text-fg leading-snug">
                      {currentCard.question}
                    </p>
                    <div className="mt-12 text-center text-xs text-zinc-400 group-hover:text-amber-500 transition-colors flex items-center justify-center gap-1">
                      <span>Click card or press space to reveal answer</span>
                      <span>↷</span>
                    </div>
                  </div>
                ) : (
                  <div className="mt-2 animate-in fade-in slide-in-from-bottom-2 duration-200">
                    <span className="text-xs font-mono uppercase tracking-wider text-emerald-500 font-bold">Comprehensive Answer</span>
                    <p className="mt-2 text-sm text-zinc-700 dark:text-zinc-200 leading-relaxed">
                      {currentCard.answer}
                    </p>

                    <div className="mt-6 p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-700 dark:text-amber-300">
                      <strong>Key Architectural Takeaway:</strong> {currentCard.keyTakeaway}
                    </div>
                  </div>
                )}
              </div>

              <div className="pt-4 border-t border-border/80 text-xs text-zinc-400 flex items-center justify-between">
                <span>Card ID: {currentCard.id}</span>
                <span>{flipped ? 'Click to flip back' : 'Flip to inspect'}</span>
              </div>
            </div>
          )}
        </div>

        {/* Rating and Navigation Controls */}
        <div className="px-6 py-4 bg-surface/90 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 text-xs font-medium rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors" onClick={handlePrev} >
              ← Previous
            </button>
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 text-xs font-medium rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors" onClick={handleNext} >
              Next →
            </button>
          </div>

          {flipped ? (
            <div className="flex items-center gap-2">
              <span className="text-xs text-zinc-400 mr-1">SM-2 Rating:</span>
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 text-xs font-semibold rounded-lg bg-rose-500/15 text-rose-600 dark:text-rose-400 hover:bg-rose-500/25 border border-rose-500/30 transition-all" onClick={() => handleRate(1)} >
                Again (1)
              </button>
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 text-xs font-semibold rounded-lg bg-orange-500/15 text-orange-600 dark:text-orange-400 hover:bg-orange-500/25 border border-orange-500/30 transition-all" onClick={() => handleRate(2)} >
                Hard (2)
              </button>
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-500/15 text-blue-600 dark:text-blue-400 hover:bg-blue-500/25 border border-blue-500/30 transition-all" onClick={() => handleRate(3)} >
                Good (3)
              </button>
              <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/25 border border-emerald-500/30 transition-all shadow-sm" onClick={() => handleRate(5)} >
                Easy (5)
              </button>
            </div>
          ) : (
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-5 py-2 text-xs font-semibold rounded-lg bg-amber-500 hover:bg-amber-400 text-zinc-950 shadow transition-all" onClick={handleFlip} >
              Reveal Answer (Space)
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
