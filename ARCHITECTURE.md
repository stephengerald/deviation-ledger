# Architecture

## State machine

The principal records and freezes plan sections, the researcher appends a deviation and rationale, consensus classifies it, and the principal may acknowledge and close the ledger.

The relevant roles are study principal and researcher. Write methods enforce role, phase, uniqueness, and bounded-storage rules before any state transition.

## Consensus boundary

Validators interpret a deviation against the frozen plan and independently agree on a classification and LOW, MEDIUM, or HIGH impact. The leader returns a small JSON schema; validators independently rerun the same decision function and accept only exact enum or bitmask values. Malformed model output raises a tagged model error and writes no decision.

## Deterministic boundary

Enrollment, authorization, commitments, counters, phase changes, caps, masks, and any score or credit arithmetic are deterministic contract logic. Only semantic interpretation of the stored evidence occurs inside `run_nondet_unsafe`.

## Off-chain boundary

Wallet custody, identity verification, indexing, notifications, private file storage, source authentication, money movement, legal process, and user-interface behavior are outside this repository. This is a transparency aid, not scientific, ethical, or regulatory certification. Inputs may be incomplete and require domain-expert review.
