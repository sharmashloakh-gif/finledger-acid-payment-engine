# finledger-acid-payment-engine
Double-entry ACID digital wallet and settlement engine built with Python, Django, and MySQL. Prevents race conditions and duplicate payouts using idempotency keys, row-level pessimistic locking (SELECT FOR UPDATE), fixed-point Decimal math, and immutable audit logs.
