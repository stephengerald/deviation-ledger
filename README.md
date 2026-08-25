# Deviation Ledger

Freezes a study plan, records later deviations append-only, and classifies their justification and likely impact.

## Why GenLayer

Validators interpret a deviation against the frozen plan and independently agree on a classification and LOW, MEDIUM, or HIGH impact.

## Reusable workflow

The principal records and freezes plan sections, the researcher appends a deviation and rationale, consensus classifies it, and the principal may acknowledge and close the ledger. Constructor parameters create a new independent instance, so the code is reusable; state is not shared between deployments.

The contract is deliberately non-custodial. It records a decision, entitlement, score, or approval signal and never transfers GEN.

## Evidence boundary

Validators use only frozen plan sections and the stored deviation packet. The contract collects no publication, dataset, or external research source.

## Verify locally

```powershell
genvm-lint check contracts/deviation_ledger.py
genvm-lint typecheck contracts/deviation_ledger.py
pytest tests/direct -q
python tests/run_glsim.py --validators 5
```

With GLSim running in another terminal:

```powershell
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The live smoke test requires fresh test-only keys in `GENLAYER_PRIVATE_KEY`, `GENLAYER_SECONDARY_PRIVATE_KEY`. Never commit a `.env` file or use a production wallet.

```powershell
gltest tests/integration/test_studionet_smoke.py --network studionet -s -q --default-wait-interval=6000 --default-wait-retries=240
```

Use the documented 6-second StudioNet polling interval to stay comfortably below public endpoint limits.

See `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md`, and `deployments/studionet.json` for the review boundary and exact public evidence.
