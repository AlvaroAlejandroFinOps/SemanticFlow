# Security Policy

## Supported Versions

We provide security updates and patches for the following versions of **SemanticFlow**:

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | :white_check_mark: |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

The SemanticFlow team takes security vulnerabilities seriously. If you discover a security vulnerability, please report it responsibly:

1. **Do NOT open a public GitHub issue.**
2. Send an email describing the vulnerability to **security@semanticflow.dev** with:
   - Description of the vulnerability and attack vector
   - Steps to reproduce or proof-of-concept (PoC) code
   - Potential impact on semantic models or emitted artifacts
   - Any proposed remediation
3. You will receive an initial response acknowledging your report within **48 hours**.
4. We will keep you updated on the progress towards remediation and coordinate public disclosure timelines with you.

---

## Security Guarantees & Built-in Defenses

SemanticFlow enforces strict defense-in-depth principles:

1. **Safe YAML & JSON Parsing**: All user-supplied configuration and schemas are parsed using `yaml.safe_load()` and strict Pydantic schemas to prevent arbitrary code execution or deserialization attacks.
2. **Output Path Isolation**: The `PbipWriter` and documentation emitters validate destination paths to prevent path traversal (`../`) and reject writing directly to root directories (`/`, `C:\`, `D:\`).
3. **Atomic Writes & Rollbacks**: Artifacts are emitted into isolated temporary staging directories and moved atomically upon successful generation, preventing partial corruption or polluted target environments.
4. **PII Automatic Redaction**: Attributes tagged with sensitive privacy classifications (`is_pii: true`) are systematically masked or redacted from consumer-facing persona lenses unless elevated governance credentials are provided.
5. **Input Sanitization & Path Traversal Eradication**: All identifiers (companies, cultures, entities, tables) are validated using strict whitelists (`^[a-zA-Z0-9_-]+$`) and boundary verification (`resolve_within`) to prevent arbitrary directory escape.
6. **Secret Leak Prevention**: Schemas, markdown and YAML profiles are pre-scanned for hardcoded credentials, Azure Client Secrets, and Bearer tokens before parsing, halting compilation immediately and suppressing secret values from logs and AI context.
7. **Zero-Diff Deterministic Invariant**: TMDL, PBIP, and dbt emitters enforce canonical lexicographical sorting across tables, attributes, measures, and relationships to guarantee identical SHA-256 hashes across runs.
8. **DAX Lexical Sandboxing & Anti-Injection**: DAX expressions in semantic models are validated for strict delimiter balancing and protected against administrative command execution (`EVALUATE`, `DEFINE`, `DROP`, `EXEC`).
9. **Fabric Direct Lake & VertiPaq Quality Rules**: Algorithmic rules (D-011 and D-012) in the cQS Quality Gate prevent Direct Lake fallbacks to DirectQuery and flag performance bottlenecks on large tables.
