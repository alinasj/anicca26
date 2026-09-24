# Anicca 26 website

The code for **anicca26.org**: a plain HTML/CSS site with no build step. It replaces the GoDaddy Website Builder site.

```
anicca26/
├── docs/                 ← the website (this folder gets published)
│   ├── index.html        Home
│   ├── atask/            aTask page
│   ├── support/          Buy me a coffee
│   ├── thanks/           shown after the contact form is sent
│   ├── 404.html
│   ├── assets/css/site.css
│   ├── assets/img/       logos, icons, Terra, social image (og.png)
│   └── .nojekyll
└── brand/
    ├── logo/             final logo files (SVG) and logo/png/ (PNG)
    └── source/           scripts that generate the logo and the brand board
```

## Preview on your computer

```bash
cd docs
python3 -m http.server 8726
```

Then open http://localhost:8726. Links won't work if you double-click the HTML files directly; use the server.

## Brand at a glance

| | |
|---|---|
| Racing Green | `#12492F` (main color) |
| Royal Gold | `#D4AF37` (accent). Use on green or dark only. Gold buttons need dark text. |
| Logo line fade | white → `#8B5CF6` → `#118AB2` → `#3A9A6A` |
| Logo dots | `#3A9A6A` `#7DAA55` `#AFAE45` `#D4AF37` |
| Font | Jost Light (300) for headings and the logo. Jost Regular (400) for text. |

Logo files in `brand/logo/`:
- `…-on-dark`: white line, for green or dark backgrounds.
- `…-on-light`: green line, for white backgrounds.
- `…-lockup-on-light-deepgold`: the same as `…-on-light`, but with a deeper gold ’26 that's easier to read on white.
- `anicca26-favicon.svg`: a simpler version with a thicker line and two dots, for tiny sizes.

The Jost font file in `brand/source/` is licensed under the SIL Open Font License (`OFL.txt`).

To regenerate the logo files: `cd brand/source && python3 export.py && ./render_png.sh` (needs Python with fontTools and Google Chrome).

## Contact form

The form uses [FormSubmit](https://formsubmit.co), which is free and works on any host. It sends messages to alina@anicca26.com.

**Activate it once, after the site is live:**
1. Send a test message from the live site.
2. FormSubmit emails alina@anicca26.com an activation link. Click it.
3. Send another test and confirm it arrives. Until then, the form doesn't deliver anything.
4. Optional: the activation email also gives you a random form address. Replace `alina@anicca26.com` in the form's `action` in `docs/index.html` with it, so your email isn't visible in the page code.

## Going live (GitHub Pages + GoDaddy DNS)

### 1. The code on GitHub
The code is on GitHub at https://github.com/alinasj/anicca26. It's published with GitHub Pages from the `main` branch, `/docs` folder.

Before the domain switch, you can preview it at **https://alinasj.github.io/anicca26/**. Any push to `main` updates it within a minute or two.

### 2. Point the domain at GitHub (in GoDaddy)
In GoDaddy, open **My Products → anicca26.org → DNS**.

**Change only these records:**

| Type | Name | Value |
|---|---|---|
| A | @ | `185.199.108.153` |
| A | @ | `185.199.109.153` |
| A | @ | `185.199.110.153` |
| A | @ | `185.199.111.153` |
| AAAA | @ | `2606:50c0:8000::153` |
| AAAA | @ | `2606:50c0:8001::153` |
| AAAA | @ | `2606:50c0:8002::153` |
| AAAA | @ | `2606:50c0:8003::153` |
| CNAME | www | `alinasj.github.io` |

- **Delete** the old `@` A records that point to GoDaddy's website builder (currently `13.248.243.5` and `76.223.105.230`).
- The `www` record currently points to `anicca26.org`. Replace it with the CNAME above.

**Do not touch:**
- `atask` → `ghs.googlehosted.com`. This runs the aTask web app and its invite links.
- The **MX** records (`aspmx.l.google.com` and the others). These handle email for anicca26.org.
- The **TXT** records: `v=spf1 …` and `google-site-verification=…` on `@`, and `v=DMARC1 …` on `_dmarc`. Also leave any record whose name contains `_spfm` or `_domainkey`. Email delivery depends on these.

If GoDaddy won't let you edit the `@` records, disconnect the Website Builder site from the domain first. It's under the Website Builder settings.

Source for the GitHub addresses: [GitHub docs: managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

### 3. Connect the domain on GitHub
1. In the repository, go to **Settings → Pages → Custom domain**. Enter `anicca26.org` and save. GitHub adds a `CNAME` file to `docs/` for you.
2. DNS changes can take from a few minutes to a few hours. When the DNS check passes, tick **Enforce HTTPS**.

### 4. Finish up
1. Activate the contact form (see above).
2. Before cancelling Website Builder, export any messages or email-list signups collected by the old GoDaddy contact form. They're lost when the plan ends.
3. Check that the domain is billed separately from the Website Builder plan, then cancel the Builder plan. Keep the domain itself.
