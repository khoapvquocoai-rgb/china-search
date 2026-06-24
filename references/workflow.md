# China Search Workflow

## 1. Intake

Capture:
- Topic and decision needed.
- Known names in Vietnamese, English, Chinese.
- Entity type: company, product, API, repo, standard, vendor, market, legal/risk.
- Desired output: query matrix, source list, translated summary, download checklist, report.
- Constraints: no paid API, no login, only copy/download, VPN allowed or not, sensitive data restrictions.

Default assumptions when unspecified:
- Public sources only.
- No paid API.
- No login automation.
- No bypass of captcha, paywall, anti-bot, rate limits, or GFW.
- Final answer in Vietnamese.

## 2. Safety gate

Classify each requested method:

| Class | Examples | Action |
|---|---|---|
| Allowed | public search, official docs, public repos, user-uploaded files, public PDFs | proceed |
| Caution | manual login, WeChat public articles, Baidu Wenku, Tianyancha public view, VPN manual public browsing | warn, record limitation, avoid automation |
| Forbidden | captcha solver, request signing reverse engineering, proxy rotation, scraping logged-in content, Tor/Shadowsocks/V2Ray/Xray/Hysteria setup | refuse method and provide lawful alternative |

## 3. Query expansion

Build 6 query packs:

1. Official docs.
2. Vendor/product docs.
3. File/PDF/whitepaper.
4. Code/repo.
5. WeChat/public media.
6. Negative/risk.

Prefer native Chinese terms from `chinese-query-glossary.md`.

## 4. Source routing

Route by research type:

| Research type | First sources | Secondary sources |
|---|---|---|
| API/cloud/AI | official docs, GitHub/Gitee SDK, developer center | CSDN, OSChina |
| Company/vendor | official site, Baidu/360, WeChat public articles | JD/1688/Tmall, CSDN |
| Code/open source | GitHub, Gitee, OSChina, GitCode, ModelScope | blogs/forums |
| Risk/due diligence | official notices, Tianyancha/Qichacha/Aiqicha public/manual, negative search | news/community |
| Technical documents | official docs, PDF search, vendor whitepapers | Baidu Wenku, CSDN |

## 5. Execution without paid API

If no external API budget exists:

1. Generate query matrix.
2. Provide manual search URLs/query strings.
3. Ask user to copy snippets, URLs, or upload downloaded pages/files.
4. Translate and summarize user-provided content.
5. Score evidence.
6. Produce a decision-ready report.

## 6. Copy/download workflow

For each useful page:

1. Save URL.
2. Save page as PDF or copy text.
3. Download only public PDF/DOC/XLS/HTML files.
4. Do not download executable files unless explicitly required and security-scanned outside the skill.
5. Add ledger row.
6. Upload file or paste content for translation.

## 7. VPN/manual lane

Use only when public pages are geo-blocked and the user accepts risk:

- Manual browsing only.
- Do not enter corporate credentials, API keys, cookies, or sensitive data.
- Do not scrape, automate, or bypass captcha.
- Record access method as `vpn_manual_public_browsing`.
- Prefer official APIs or public exports when available.

## 8. Reporting

Report must separate:
- Facts observed.
- Claims by sources.
- Inferences.
- Missing evidence.
- Risks.
- Next verification steps.
