"""AeroTrade Core - Real-Time Double-Entry Ledger

Demonstrates concepts from Chapters 01, 04, 05, 09, and 12:
- Double-entry accounting principles: Every credit has an equal and opposite debit.
- Strict mathematical conservation invariant: System total cash and total shares never drift.
- Audit trail integrity.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
from domain import Trade


@dataclass(slots=True)
class Account:
    trader_id: str
    cash_balance: float = 0.0
    shares: Dict[str, int] = field(default_factory=dict)

    def deposit_cash(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.cash_balance += amount

    def deposit_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Share quantity must be positive")
        self.shares[symbol] = self.shares.get(symbol, 0) + quantity


class DoubleEntryLedger:
    """Manages trader balances and validates conservation invariants."""

    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.trade_history: List[Trade] = []

    def get_or_create_account(self, trader_id: str) -> Account:
        if trader_id not in self.accounts:
            self.accounts[trader_id] = Account(trader_id=trader_id)
        return self.accounts[trader_id]

    def record_trade_settlement(self, trade: Trade) -> None:
        """Atomically transfers cash and securities between buyer and seller."""
        buyer = self.get_or_create_account(trade.buyer_id)
        seller = self.get_or_create_account(trade.seller_id)

        notional_value = trade.price * trade.quantity

        # Debit buyer cash, credit buyer shares
        buyer.cash_balance -= notional_value
        buyer.shares[trade.symbol] = buyer.shares.get(trade.symbol, 0) + trade.quantity

        # Credit seller cash, debit seller shares
        seller.cash_balance += notional_value
        seller.shares[trade.symbol] = seller.shares.get(trade.symbol, 0) - trade.quantity

        self.trade_history.append(trade)

    def verify_conservation_invariant(self, initial_total_cash: float, initial_total_shares: int, symbol: str) -> bool:
        """Verifies that no cash or shares were created or destroyed."""
        current_total_cash = sum(acc.cash_balance for acc in self.accounts.values())
        current_total_shares = sum(acc.shares.get(symbol, 0) for acc in self.accounts.values())

        cash_conserved = abs(current_total_cash - initial_total_cash) < 1e-6
        shares_conserved = current_total_shares == initial_total_shares

        if not (cash_conserved and shares_conserved):
            raise AssertionError(
                f"Ledger invariant violation! "
                f"Cash: {current_total_cash} vs {initial_total_cash}, "
                f"Shares: {current_total_shares} vs {initial_total_shares}"
            )
        return True
