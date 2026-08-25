# Submission: Deviation Ledger

Project name: Deviation Ledger

Repository: https://github.com/stephengerald/deviation-ledger

StudioNet contract: https://explorer-studio.genlayer.com/address/0x1249d3E391daC5c6E34C79d342ab4fb47468145E

Deployment transaction: https://explorer-studio.genlayer.com/tx/0x976b87afb67faea3aee339ea9ac83b997b6b073121e90b5f6fd5ff89317e1104

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0xb3cd8b733a1e30df56cbd677b2ce9fa4bd6e019a59f9014d22d422fe20182d8a

Summary: Freezes a study plan, records later deviations append-only, and classifies their justification and likely impact.

Why it is GenLayer-native: Validators interpret a deviation against the frozen plan and independently agree on a classification and LOW, MEDIUM, or HIGH impact.

Evidence/source model: Validators use only frozen plan sections and the stored deviation packet. The contract collects no publication, dataset, or external research source.

Declared scope: Reusable, non-custodial prototype. This is a transparency aid, not scientific, ethical, or regulatory certification. Inputs may be incomplete and require domain-expert review.

Review evidence: `AUDIT.md`, `SECURITY.md`, `SOURCE_POLICY.md`, and `deployments/studionet.json` bind the reviewed source hash to the public live result.
