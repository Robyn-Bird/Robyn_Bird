# robynbird.com

Robyn Bird's personal site: who she is, her committeeperson and community work, Local 22, and a page on her 2026 campaign. Plain static site on GitHub Pages; domain at GoDaddy.

Paid for by Friends of Robyn Bird. Designed and built by Shirah M. Brown.

## Pages
| Path | What it is |
|---|---|
| `index.html` | Home |
| `about/` | Robyn's story |
| `campaign/` | The 2026 campaign |
| `404.html`, `robots.txt`, `sitemap.xml`, `CNAME` | Housekeeping |

## Editing
Pages are stamped from `_build/build.py` (shared header, footer and form). Edit the copy there, then run `python3 _build/build.py .` from this folder and commit. Styles are in `assets/site.css`. GitHub Pages republishes in about a minute.

- The get-in-touch form posts to Robyn's "Get in Touch" Google Form (same responses sheet as voterobynbird.com). Checkboxes add "Invite to speak/event: yes" and "Women in local government: yes" to the Comments answer.
- Analytics: same GA4 property as the campaign site; filter by hostname robynbird.com.
- voterobynbird.com is a separate site (Robyn-Bird/voterobynbird.com) and is unchanged.

## Going live
1. Settings → Pages: deploy from `main`, root. Custom domain `www.robynbird.com`.
2. GoDaddy, robynbird.com: turn off forwarding. A records for `@` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; CNAME `www` → `robyn-bird.github.io`. Leave MX/TXT (email) records alone.
3. When the DNS check passes, tick Enforce HTTPS. Add robynbird.com to Search Console and submit the sitemap.
