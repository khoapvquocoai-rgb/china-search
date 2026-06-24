# Compliance Boundaries

## Default boundary

This skill supports public-source research and user-authorized analysis. It does not support access bypass, evasion, credential misuse, or scraping private/restricted data.

## Stop conditions

Stop automation and switch to manual/legal review when any of these appear:

- Captcha / 验证码 / 安全验证.
- Login / QR login / phone verification / real-name verification.
- Paywall / membership / VIP area.
- Rate limit / access too frequent / suspicious activity warning.
- Request requires cookie, token, app secret, private API, or signed request not provided by official docs.
- User asks to scrape group chats, private WeChat content, private profiles, personal data, or paid databases.

## Lawful alternatives

| Blocked method | Alternative |
|---|---|
| Captcha bypass | Manual review or official API. |
| Proxy rotation | Lower-rate public search, official API, licensed data provider. |
| Private content scraping | User-authorized export or manual copy by account owner. |
| Paid platform scraping | Buy official access/API or ask vendor for documents. |
| Request signing reverse engineering | Official SDK/API or public web page review. |
| GFW evasion tooling | Licensed business access, public sources, or manual browsing with risk logging. |

## VPN/manual public browsing lane

Only discuss as a manual, last-resort option for public pages. Do not provide setup instructions for circumvention tools. Remind user:

- Use a separate browser profile.
- Do not enter corporate credentials or API keys.
- Do not automate.
- Do not bypass captcha/login/paywall.
- Record `access_method` and limitations in evidence ledger.
