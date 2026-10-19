# security — skills index
Read THIS file only. Open an individual SKILL.md ONLY if the current task needs it.
Each skill lives at `<path>/SKILL.md` (+ `scripts/agent.py`, run via Bash with `--target`).
Paths are relative to `.claude/role-skills/security/`.

| skill | when to apply | path |
|---|---|---|
| SQL injection | task touches DB queries / user input reaches SQL | exploiting-sql-injection-vulnerabilities/SKILL.md |
| IDOR | object access by id / broken access control | exploiting-idor-vulnerabilities/SKILL.md |
| SSRF | backend fetches external URLs on user input | performing-ssrf-vulnerability-exploitation/SKILL.md |
| CSRF | state-changing web forms / cookie-based auth | performing-csrf-attack-simulation/SKILL.md |
| XSS | user input rendered in HTML / a web surface | testing-for-xss-vulnerabilities/SKILL.md |
| JWT | auth uses JSON Web Tokens | testing-for-json-web-token-vulnerabilities/SKILL.md |
| OWASP Top 10 (API) | full API audit gate for a phase | testing-api-security-with-owasp-top-10/SKILL.md |
| CORS | cross-origin API access | testing-cors-misconfiguration/SKILL.md |
| Security headers | any HTTP surface is exposed | performing-security-headers-audit/SKILL.md |
| Rate limiting | auth / expensive / OTP endpoints | performing-api-rate-limiting-bypass/SKILL.md |
| Secret scanning | before release / repo or env audit | implementing-secret-scanning-with-gitleaks/SKILL.md |
| Trivy image scan | dockerized service / image before deploy | scanning-docker-images-with-trivy/SKILL.md |
