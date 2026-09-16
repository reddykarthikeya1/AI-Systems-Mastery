import React, { useState, useEffect } from 'react';
import { executeSql } from '../services/api';
import { SqlResult } from '../types';
import { soundService } from '../services/sound';

interface SqlPlaygroundViewProps {
  initialQuery?: string;
  onClose?: () => void;
}

const PRESET_QUERIES: Record<string, { name: string; query: string }[]> = {
  storage_engine: [
    {
      name: '1. Inspect B-Tree Pages & Allocation',
      query: 'SELECT page_id, page_type, item_count, free_bytes, lsn\nFROM btree_pages\nORDER BY page_id ASC;',
    },
    {
      name: '2. Check WAL Frame Commits & Checkpoints',
      query: 'SELECT frame_no, page_id, commit_flag, salt1, salt2\nFROM wal_frames\nWHERE commit_flag = 1;',
    },
    {
      name: '3. Scan Distributed KV Store State',
      query: 'SELECT key, value, version, created_at\nFROM key_value_store\nORDER BY version DESC;',
    },
    {
      name: '4. Explain Query Plan for Leaf Nodes',
      query: 'SELECT * FROM btree_pages WHERE page_type = \'leaf\';',
    },
  ],
  ecommerce: [
    {
      name: '1. High-Value Customers (> $10k)',
      query: 'SELECT id, name, tier, spend\nFROM customers\nWHERE spend > 10000\nORDER BY spend DESC;',
    },
    {
      name: '2. Customer Order Aggregations',
      query: 'SELECT c.name, COUNT(o.order_id) AS total_orders, COALESCE(SUM(o.amount), 0) AS total_amount\nFROM customers c\nLEFT JOIN orders o ON c.id = o.customer_id\nGROUP BY c.id, c.name;',
    },
  ],
};

export const SqlPlaygroundView: React.FC<SqlPlaygroundViewProps> = ({
  initialQuery = 'SELECT page_id, page_type, item_count, free_bytes, lsn\nFROM btree_pages\nORDER BY page_id ASC;',
  onClose,
}) => {
  const [preset, setPreset] = useState<'storage_engine' | 'ecommerce'>('storage_engine');
  const [query, setQuery] = useState(initialQuery);
  const [executing, setExecuting] = useState(false);
  const [result, setResult] = useState<SqlResult | null>(null);

  const handleExecute = async () => {
    if (!query.trim() || executing) return;
    soundService.playClick();
    setExecuting(true);
    try {
      const res = await executeSql(query, preset);
      setResult(res);
      if (res.status === 'success') {
        soundService.playSuccess();
      } else {
        soundService.playError();
      }
    } catch (err: any) {
      soundService.playError();
      setResult({
        status: 'error',
        error: err.message || 'Execution failed',
        columns: [],
        rows: [],
        row_count: 0,
        duration_ms: 0,
        query_plan: [],
      });
    } finally {
      setExecuting(false);
    }
  };

  useEffect(() => {
    // Run initial query on mount
    handleExecute();
  }, [preset]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleExecute();
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-zinc-950 border border-zinc-200 dark:border-zinc-800 rounded-xl overflow-hidden shadow-xl">
      {/* Header bar */}
      <div className="flex items-center justify-between px-4 py-3 bg-zinc-50 dark:bg-zinc-900/80 border-b border-zinc-200 dark:border-zinc-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-bold text-sm">
            SQL
          </div>
          <div>
            <h2 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
              Storage Engine & SQL Sandbox
              <span className="px-2 py-0.5 text-xs rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-mono">
                SQLite In-Memory
              </span>
            </h2>
            <p className="text-xs text-zinc-500 dark:text-zinc-400">
              Query B-Tree page slots, WAL write logs, and analyze internal execution plans.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Preset selector */}
          <select
            value={preset}
            onChange={(e) => {
              const nextPreset = e.target.value as any;
              setPreset(nextPreset);
              setQuery(PRESET_QUERIES[nextPreset][0].query);
            }}
            className="text-xs px-2.5 py-1.5 rounded-lg border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-800 dark:text-zinc-200 focus:outline-none focus:ring-1 focus:ring-emerald-500"
          >
            <option value="storage_engine">Database Internals (B-Tree & WAL)</option>
            <option value="ecommerce">Relational E-Commerce Schema</option>
          </select>

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

      {/* Preset Query Chips */}
      <div className="flex items-center gap-2 px-4 py-2 bg-zinc-100/50 dark:bg-zinc-900/40 border-b border-zinc-200 dark:border-zinc-800 overflow-x-auto text-xs">
        <span className="text-zinc-400 font-medium whitespace-nowrap">Examples:</span>
        {PRESET_QUERIES[preset].map((p, idx) => (
          <button
            key={idx}
            onClick={() => {
              soundService.playClick();
              setQuery(p.query);
            }}
            className="px-2.5 py-1 rounded-md bg-white dark:bg-zinc-800 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 hover:text-emerald-600 dark:hover:text-emerald-400 border border-zinc-200 dark:border-zinc-700 whitespace-nowrap text-zinc-700 dark:text-zinc-300 transition-colors shadow-sm"
          >
            {p.name}
          </button>
        ))}
      </div>

      {/* Split View: Editor on Top, Results on Bottom */}
      <div className="flex-1 flex flex-col min-h-0">
        {/* Editor Area */}
        <div className="flex flex-col border-b border-zinc-200 dark:border-zinc-800">
          <div className="flex items-center justify-between px-4 py-1.5 bg-zinc-50/50 dark:bg-zinc-900/30 text-xs text-zinc-500 border-b border-zinc-200 dark:border-zinc-800">
            <span>SQL Query Editor (Press <kbd className="px-1 py-0.5 bg-zinc-200 dark:bg-zinc-800 rounded font-mono text-xs">Ctrl+Enter</kbd> to run)</span>
            <button
              onClick={handleExecute}
              disabled={executing}
              className="flex items-center gap-1.5 px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded-md font-medium text-xs shadow-sm transition-all disabled:opacity-50"
            >
              {executing ? (
                <svg className="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                </svg>
              ) : (
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                </svg>
              )}
              Run Query
            </button>
          </div>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={5}
            spellCheck={false}
            className="w-full p-4 font-mono text-xs bg-zinc-900 text-emerald-400 resize-none focus:outline-none leading-relaxed selection:bg-emerald-600 selection:text-white"
            placeholder="Write your SQL statement here..."
          />
        </div>

        {/* Results Area */}
        <div className="flex-1 flex flex-col min-h-0 bg-white dark:bg-zinc-950 overflow-auto">
          {/* Query status header */}
          <div className="flex items-center justify-between px-4 py-2 bg-zinc-50 dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800 text-xs">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-zinc-700 dark:text-zinc-300">Execution Output</span>
              {result && (
                <span className={`px-2 py-0.5 rounded text-xs font-mono ${
                  result.status === 'success'
                    ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400'
                    : 'bg-rose-500/10 text-rose-600 dark:text-rose-400'
                }`}>
                  {result.status === 'success' ? `${result.row_count} row(s) in ${result.duration_ms} ms` : 'Query Error'}
                </span>
              )}
            </div>
            {result?.query_plan && result.query_plan.length > 0 && (
              <span className="text-zinc-400 text-xs font-mono">
                {result.query_plan.length} Plan Step(s)
              </span>
            )}
          </div>

          {/* Results table or Error box */}
          <div className="flex-1 overflow-auto p-4">
            {result?.error ? (
              <div className="p-3 bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900 rounded-lg text-rose-700 dark:text-rose-400 font-mono text-xs">
                <strong>Error:</strong> {result.error}
              </div>
            ) : result?.columns && result.columns.length > 0 ? (
              <div className="overflow-x-auto border border-zinc-200 dark:border-zinc-800 rounded-lg">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-zinc-100 dark:bg-zinc-900 text-zinc-700 dark:text-zinc-300 border-b border-zinc-200 dark:border-zinc-800">
                    <tr>
                      {result.columns.map((col, cIdx) => (
                        <th key={cIdx} className="px-3 py-2 font-semibold">
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
                    {result.rows.map((row, rIdx) => (
                      <tr key={rIdx} className="hover:bg-zinc-50 dark:hover:bg-zinc-900/50">
                        {row.map((val, vIdx) => (
                          <td key={vIdx} className="px-3 py-2 text-zinc-600 dark:text-zinc-300">
                            {val === null ? <span className="text-zinc-400 italic">NULL</span> : String(val)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-8 text-zinc-400 text-xs">
                No rows returned or empty query.
              </div>
            )}

            {/* Query plan section if present */}
            {result?.query_plan && result.query_plan.length > 0 && (
              <div className="mt-4 p-3 bg-zinc-50 dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-lg">
                <div className="text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-2">
                  SQLite Query Execution Plan
                </div>
                <div className="space-y-1 font-mono text-xs text-zinc-600 dark:text-zinc-400">
                  {result.query_plan.map((step, sIdx) => (
                    <div key={sIdx} className="flex items-center gap-2">
                      <span className="text-emerald-500">→</span>
                      <span>{step}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
