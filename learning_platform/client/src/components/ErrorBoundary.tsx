import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RotateCcw } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallbackTitle?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[300px] flex items-center justify-center p-8">
          <div className="max-w-md w-full p-8 rounded-2xl bg-surface border border-rose-500/30 shadow-xl text-center space-y-4">
            <div className="w-12 h-12 rounded-xl bg-rose-500/10 text-rose-500 flex items-center justify-center mx-auto border border-rose-500/20">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-fg">
                {this.props.fallbackTitle || 'Unable to display this view'}
              </h2>
              <p className="text-xs text-fg-muted mt-1 leading-relaxed">
                An unexpected error occurred while rendering. Your study progress and notes are safely saved.
              </p>
              {this.state.error && (
                <pre className="mt-3 p-2 text-xs font-mono bg-zinc-100 dark:bg-zinc-900 text-rose-600 dark:text-rose-400 rounded-lg overflow-x-auto text-left">
                  {this.state.error.message}
                </pre>
              )}
            </div>
            <button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-500 px-4 py-2 rounded-xl text-xs font-semibold bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 hover:opacity-90 transition flex items-center gap-2 mx-auto shadow-sm" onClick={this.handleReset} >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reload View</span>
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
