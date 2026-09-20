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
