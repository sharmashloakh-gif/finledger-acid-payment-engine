# FinLedger — Double-Entry ACID Wallet & Settlement Engine

An enterprise-grade double-entry ledger system built with **Django** and **MySQL** featuring idempotency keys, row-level pessimistic locking (`SELECT ... FOR UPDATE`), and immutable audit logs.

## Why Recruiters Love This
Financial systems fail when race conditions allow double-spending. FinLedger guarantees zero-sum ledger invariants across concurrent transfers.
