from decimal import Decimal
import uuid

class LedgerError(Exception):
    pass

class DoubleEntryEngine:
    """In-memory reference implementation mirroring Django transaction.atomic + select_for_update."""
    def __init__(self):
        self.accounts = {}
        self.entries = []
        self.processed_keys = set()

    def create_account(self, account_id: str, initial_balance: str = "0.00"):
        self.accounts[account_id] = Decimal(initial_balance)

    def transfer(self, idempotency_key: str, from_acct: str, to_acct: str, amount: str) -> dict:
        if idempotency_key in self.processed_keys:
            return {"status": "duplicate_ignored", "idempotency_key": idempotency_key}
        amt = Decimal(amount)
        if amt <= 0:
            raise LedgerError("Transfer amount must be positive")
        if self.accounts.get(from_acct, Decimal("0")) < amt:
            raise LedgerError("Insufficient funds")

        tx_id = str(uuid.uuid4())
        self.accounts[from_acct] -= amt
        self.accounts[to_acct] += amt
        self.entries.append({"tx_id": tx_id, "account": from_acct, "type": "DEBIT", "amount": str(amt)})
        self.entries.append({"tx_id": tx_id, "account": to_acct, "type": "CREDIT", "amount": str(amt)})
        self.processed_keys.add(idempotency_key)
        return {"status": "settled", "tx_id": tx_id}

if __name__ == "__main__":
    eng = DoubleEntryEngine()
    eng.create_account("merchant_1", "1000.00")
    eng.create_account("vendor_9", "250.00")
    print(eng.transfer("idem-001", "merchant_1", "vendor_9", "125.50"))
    print("Balances:", eng.accounts)
