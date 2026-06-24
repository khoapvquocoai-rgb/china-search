# Security Policy

## 🛡️ Supported Versions

We provide security updates for the following versions:

| Version | Supported |
|---------|-----------|
| 2.0.x   | ✅ Yes    |
| 1.0.x   | ⚠️ Security fixes only |
| < 1.0   | ❌ No     |

---

## 🚨 Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these guidelines:

### Responsible Disclosure

**DO:**
- Report vulnerabilities privately via email: security@github.com/khoapvquocoai-rgb/china-search
- Provide detailed information about the vulnerability
- Allow reasonable time for us to fix before public disclosure
- Follow responsible disclosure practices

**DON'T:**
- Publicly disclose vulnerabilities before they're fixed
- Exploit vulnerabilities for malicious purposes
- Disrupt or degrade our service
- Violate our Terms of Service

### What to Include

When reporting a vulnerability, please provide:

```markdown
### Vulnerability Report

**Type:** [e.g., Prompt Injection, RAG Poisoning, Auth Bypass]

**Severity:** [Critical/High/Medium/Low]

**Description:**
Clear explanation of the vulnerability

**Steps to Reproduce:**
1. Setup environment
2. Execute attack vector
3. Observe impact

**Impact:**
What can an attacker achieve?

**Proof of Concept (Optional):**
Code or commands demonstrating the issue

**Suggested Fix (Optional):**
If you know how to mitigate it

**Reporter:**
Your name/handle (optional)
```

### Response Time

We aim to:
- Acknowledge receipt within **48 hours**
- Provide initial assessment within **5 business days**
- Release fix within **30 days** (depending on severity)

---

## 🔒 Security Best Practices

### For Users

1. **Never upload sensitive data to cloud demos**
   - Contracts, bids, internal reports should ONLY be processed locally
   - Use self-hosted deployment for sensitive workloads

2. **Review license terms before commercial use**
   - SaaS provision requires written permission
   - Check COMMERCIAL.md if available

3. **Sandbox all code execution**
   - Use containerized environments
   - Limit network access
   - Set resource limits (CPU, memory, timeout)

4. **Validate all inputs**
   - Sanitize user-provided documents
   - Check file types and sizes
   - Scan for malicious content

5. **Monitor for anomalies**
   - Track unusual query patterns
   - Alert on high token usage
   - Log all AI-assisted decisions

### For Developers

1. **Input Validation**
   ```python
   # Always validate and sanitize
   def safe_process_document(file_path: str) -> str:
       if not is_safe_file(file_path):
           raise SecurityError("Unsafe file detected")
       return extract_text(file_path)
   ```

2. **Avoid Hardcoded Secrets**
   ```python
   # ❌ BAD
   API_KEY = "sk-1234567890"
   
   # ✅ GOOD
   API_KEY = os.environ.get("API_KEY")
   ```

3. **Use Parameterized Queries**
   ```python
   # Prevent injection attacks in database queries
   cursor.execute("SELECT * FROM docs WHERE id = %s", (user_id,))
   ```

4. **Implement Rate Limiting**
   ```python
   from ratelimit import limits, sleep_and_retry
   
   @sleep_and_retry
   @limits(calls=10, period=60)  # 10 calls per minute
   def process_request(user_input):
       pass
   ```

5. **Log Security Events**
   ```python
   import logging
   
   logger = logging.getLogger(__name__)
   logger.warning(f"Security event: {event_details}")
   ```

---

## ⚠️ Known Security Considerations

### Prompt Injection

**Risk:** Malicious instructions in uploaded documents could override system prompts.

**Mitigation:**
- Input sanitization before processing
- System prompt hardening with explicit rules
- Output filtering for sensitive information

### RAG Poisoning

**Risk:** Toxic documents could corrupt knowledge base retrieval.

**Mitigation:**
- Source verification before indexing
- Chunk-level scanning for malicious content
- Metadata validation (author, date, domain)

### Tool Execution

**Risk:** Agents executing arbitrary code/files could compromise system.

**Mitigation:**
- Containerized sandbox with read-only filesystem
- No network access for code execution
- Strict timeout limits (max 30 seconds)
- Whitelist allowed operations only

### Data Leakage

**Risk:** Sensitive information exposed via API responses or logs.

**Mitigation:**
- Local storage only for PoC deployments
- No cloud sync without encryption
- PII detection and redaction
- Audit logging with access controls

---

## 📋 Security Checklist for Contributors

Before submitting PRs, ensure:

- [ ] No hardcoded secrets or API keys
- [ ] All user inputs validated and sanitized
- [ ] File paths properly escaped (no path traversal)
- [ ] Error messages don't expose stack traces
- [ ] Dependencies up-to-date (no known CVEs)
- [ ] Security implications documented
- [ ] Tests cover edge cases and attack vectors

---

## 🔍 Security Audit History

| Date | Issue | Severity | Status |
|------|-------|----------|--------|
| 2026-06-24 | Initial security review | N/A | ✅ Passed |

---

## 📞 Contact

For security inquiries:
- **Email:** security@github.com/khoapvquocoai-rgb/china-search
- **GitHub Security Advisories:** [Report a vulnerability](https://github.com/khoapvquocoai-rgb/china-search/security/advisories/new)

**Note:** Please do NOT use GitHub Issues for security vulnerabilities. Keep them private until resolved.

---

## 🙏 Acknowledgments

Thank you to all security researchers who have helped improve our security!

*Last updated: 2026-06-24*
