import React, { useState, useEffect, useRef } from 'react';
import mermaid from 'mermaid';
import { soundService } from '../services/sound';

interface ArchitectureCanvasViewProps {
  onClose?: () => void;
}

interface Blueprint {
  id: string;
  name: string;
  description: string;
  code: string;
}

const BLUEPRINTS: Blueprint[] = [
  {
    id: 'raft',
    name: '1. Raft Consensus Algorithm',
    description: 'Leader election, heartbeat timeouts, log replication, and RPC commit quorums.',
    code: `graph TD
    subgraph Cluster["Distributed Raft Cluster"]
        L["Leader (Node A)<br/>[Term 4]"]
        F1["Follower (Node B)<br/>[Term 4]"]
        F2["Follower (Node C)<br/>[Term 4]"]
    end
    
    Client["Client Request"] -->|"PUT /key 'val'"| L
    L -->|"AppendEntries RPC"| F1
    L -->|"AppendEntries RPC"| F2
    F1 -.->|"Success Quorum (2/3)"| L
    F2 -.->|"Success Quorum (2/3)"| L
    L -->|"Commit & Respond 200 OK"| Client
    
    style L fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    style F1 fill:#3b82f6,stroke:#2563eb,stroke-width:1px,color:#fff
    style F2 fill:#3b82f6,stroke:#2563eb,stroke-width:1px,color:#fff`,
  },
  {
    id: 'cqrs',
    name: '2. CQRS & Event Sourcing',
    description: 'Decoupled command mutating path, Kafka commit log, and read-optimized query projections.',
    code: `flowchart LR
    API["API Gateway / Client"]
    
    subgraph CommandPath["Write Path (Command Side)"]
        CmdService["Order Command Service"]
        EventStore[("Kafka Event Log<br/>Partitioned Topic")]
    end
    
    subgraph ReadPath["Read Path (Query Side)"]
        Consumer["Projection Worker"]
        ReadDB[("Elasticsearch / Redis<br/>Materialized Views")]
        QueryService["Order Query API"]
    end
    
    API -->|"POST /orders (PlaceOrder)"| CmdService
    CmdService -->|"Append OrderPlaced Event"| EventStore
    EventStore -->|"Stream Events"| Consumer
    Consumer -->|"Update Read Models"| ReadDB
    API -->|"GET /orders/123"| QueryService
    QueryService -->|"Low-Latency Fetch"| ReadDB
    
    style EventStore fill:#f59e0b,stroke:#d97706,color:#000
    style ReadDB fill:#8b5cf6,stroke:#7c3aed,color:#fff`,
  },
  {
    id: 'twopc',
    name: '3. Two-Phase Commit (2PC)',
    description: 'Atomic cross-database transaction coordination with Prepare and Commit phases.',
    code: `sequenceDiagram
    autonumber
    participant Coord as Transaction Coordinator
    participant P1 as Payment Service DB
    participant P2 as Inventory Service DB
    
    Note over Coord, P2: Phase 1: Prepare Phase
    Coord->>P1: PREPARE (TID: 9912)
    Coord->>P2: PREPARE (TID: 9912)
    P1-->>Coord: VOTE_COMMIT (WAL Locked)
    P2-->>Coord: VOTE_COMMIT (Stock Reserved)
    
    Note over Coord, P2: Phase 2: Commit Phase (Quorum Unanimous)
    Coord->>P1: GLOBAL_COMMIT (Release Locks)
    Coord->>P2: GLOBAL_COMMIT (Confirm Stock)
    P1-->>Coord: ACK_COMMITTED
    P2-->>Coord: ACK_COMMITTED`,
  },
  {
    id: 'active_active',
    name: '4. Multi-Region Active-Active Sharding',
    description: 'Anycast DNS routing, partitioned shard clusters, and asynchronous bi-directional cross-region replication.',
    code: `graph TB
    UserUS["US Users"] --> Route53["Latency-Based Anycast Route"]
    UserEU["EU Users"] --> Route53
    
    subgraph USRegion["AWS us-east-1 (Primary Shard A)"]
        LB_US["ALB US"]
        Svc_US["Services US"]
        DB_US[("Postgres Master US<br/>Range A-M")]
    end
    
    subgraph EURegion["AWS eu-central-1 (Primary Shard B)"]
        LB_EU["ALB EU"]
        Svc_EU["Services EU"]
        DB_EU[("Postgres Master EU<br/>Range N-Z")]
    end
    
    Route53 -->|"Closest Region"| LB_US
    Route53 -->|"Closest Region"| LB_EU
    LB_US --> Svc_US --> DB_US
    LB_EU --> Svc_EU --> DB_EU
    
    DB_US <===>|"Bi-Directional Async WAL Replication"| DB_EU`,
  },
];

export const ArchitectureCanvasView: React.FC<ArchitectureCanvasViewProps> = ({ onClose }) => {
  const [selectedBlueprint, setSelectedBlueprint] = useState<string>('raft');
  const [code, setCode] = useState<string>(BLUEPRINTS[0].code);
  const [svgContent, setSvgContent] = useState<string>('');
  const [renderError, setRenderError] = useState<string | null>(null);
  const [copied, setCopied] = useState<boolean>(false);
  const canvasRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'dark',
      securityLevel: 'loose',
      fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
    });
  }, []);

  const renderDiagram = async (src: string) => {
    try {
      setRenderError(null);
      const id = `mermaid-arch-${Date.now()}`;
      const { svg } = await mermaid.render(id, src);
      setSvgContent(svg);
    } catch (err: any) {
      setRenderError(err.message || 'Syntax error in Mermaid diagram');
    }
  };

  useEffect(() => {
    renderDiagram(code);
  }, [code]);

  const handleSelectBlueprint = (bp: Blueprint) => {
    soundService.playClick();
    setSelectedBlueprint(bp.id);
    setCode(bp.code);
  };

  const handleCopyCode = () => {
    soundService.playSuccess();
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden shadow-xl">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-zinc-50 dark:bg-zinc-900/80 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 flex items-center justify-center font-bold text-sm">
            ☊
          </div>
          <div>
            <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
              Distributed Architecture Canvas
              <span className="px-2 py-0.5 text-xs rounded-full bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 font-mono">
                Live Mermaid Engine
              </span>
            </h2>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">
              Model consensus, event streaming, and multi-region fault tolerance topologies in code.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopyCode}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-50 dark:hover:bg-zinc-700 transition-colors"
          >
            {copied ? '✓ Copied' : 'Copy Mermaid Code'}
          </button>
          {onClose && (
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Blueprint Presets */}
      <div className="flex items-center gap-2 px-4 py-2 bg-zinc-100/50 dark:bg-zinc-900/40 border-b border-zinc-200 dark:border-zinc-800 overflow-x-auto text-xs">
        <span className="text-zinc-400 font-medium whitespace-nowrap">Architectures:</span>
        {BLUEPRINTS.map((bp) => (
          <button
            key={bp.id}
            onClick={() => handleSelectBlueprint(bp)}
            className={`px-2.5 py-1 rounded-md border whitespace-nowrap transition-colors shadow-sm ${
              selectedBlueprint === bp.id
                ? 'bg-indigo-600 text-white border-indigo-600 font-medium'
                : 'bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 border-zinc-200 dark:border-zinc-700 hover:bg-zinc-50 dark:hover:bg-zinc-700'
            }`}
          >
            {bp.name}
          </button>
        ))}
      </div>

      {/* Split View: Left Monospace Editor, Right Live Render Canvas */}
      <div className="flex-1 grid grid-cols-1 md:grid-cols-2 min-h-0">
        {/* Editor */}
        <div className="flex flex-col border-r border-zinc-200 dark:border-zinc-800 min-h-0">
          <div className="px-4 py-2 bg-zinc-50 dark:bg-zinc-900 text-xs font-semibold text-zinc-500 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between">
            <span>Mermaid DSL Source Code</span>
            <span className="text-[11px] font-normal text-zinc-400">Updates live as you type</span>
          </div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            spellCheck={false}
            className="flex-1 p-4 font-mono text-xs bg-zinc-950 text-indigo-300 resize-none focus:outline-none leading-relaxed selection:bg-indigo-600 selection:text-white overflow-auto"
            placeholder="graph TD..."
          />
        </div>

        {/* Live Preview Canvas */}
        <div className="flex flex-col min-h-0 bg-zinc-900/30 overflow-hidden">
          <div className="px-4 py-2 bg-zinc-50 dark:bg-zinc-900 text-xs font-semibold text-zinc-500 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between">
            <span>Rendered Architecture View</span>
            {renderError ? (
              <span className="text-rose-500 font-mono text-[11px]">Compile Error</span>
            ) : (
              <span className="text-emerald-500 font-mono text-[11px]">✓ Valid Diagram</span>
            )}
          </div>

          <div
            ref={canvasRef}
            className="flex-1 p-6 overflow-auto flex items-center justify-center min-h-0 bg-white dark:bg-zinc-950"
          >
            {renderError ? (
              <div className="p-4 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900 rounded-lg text-rose-700 dark:text-rose-300 text-xs font-mono max-w-md">
                <strong>Mermaid Syntax Error:</strong>
                <p className="mt-1 text-rose-500 break-words">{renderError}</p>
              </div>
            ) : svgContent ? (
              <div
                className="w-full h-full flex items-center justify-center [&_svg]:max-w-full [&_svg]:max-h-full [&_svg]:h-auto"
                dangerouslySetInnerHTML={{ __html: svgContent }}
              />
            ) : (
              <div className="text-zinc-400 text-xs">Rendering diagram...</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
