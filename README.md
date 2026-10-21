# SIGHAN websites

Two static sites in one tree, sharing one stylesheet:

| Path | Site |
|---|---|
| `/` | **SIGHAN** — the ACL Special Interest Group on Chinese Language Processing |
| `/dclp/` | **SIGHAN-DCLP 2027** — the *Diversifying Chinese Language Processing* workshop |

```
.
├── index.html            SIGHAN home
├── about.html            purpose, membership, officers, constitution
├── workshops.html        every edition 2000–present, with links back to each original site
├── shared-tasks.html     bakeoffs and shared-task evaluations
├── assets/css/style.css  the only stylesheet; both sites use it
├── assets/js/lang.js     the EN / 简 / 繁 language switch
├── tools/hant.py         regenerates the Traditional Chinese text from the Simplified
└── dclp/
    ├── index.html        workshop overview
    ├── cfp.html          call for papers
    ├── shared-task.html  document-level meaning representation parsing
    └── organizers.html   organizers + programme committee
```

No build step and no dependencies. Every page is plain HTML plus one stylesheet and one small
script. Google Fonts (Source Serif 4 + Inter) load from a CDN and fall back to system fonts
including CJK faces.

## English, Simplified and Traditional Chinese

Every page carries three languages, and the EN / 简 / 繁 switch in the header chooses between
them. Each string is a set of sibling spans inside one shared element, so the layout rules keep
working:

```html
<h2><span lang="en">Key dates</span><span lang="zh-Hans">重要日期</span><span lang="zh-Hant">重要日期</span></h2>
```

**Edit only the English and the Simplified (`zh-Hans`) spans.** The Traditional (`zh-Hant`) spans,
and each page's `data-title-zh-hant`, are generated from the Simplified text with Taiwan-standard
characters and vocabulary (資訊, 資料, 大型語言模型 …). After any Chinese edit, regenerate them:

```bash
pip install opencc-python-reimplemented
python3 tools/hant.py
```

`python3 tools/hant.py --check` exits non-zero if any page is out of date. Don't hand-edit a
`zh-Hant` span — the next run overwrites it. If a Traditional term comes out wrong, add the
correction to the `PHRASES` table at the top of `tools/hant.py` and rerun.

Only the language that `<html lang>` names is shown. `assets/js/lang.js` sets it before the page
paints, from (in order) `?lang=` in the URL, the visitor's last choice, then the browser's
preferred language — zh-TW / zh-HK / zh-MO browsers get Traditional, other Chinese browsers get
Simplified, everyone else English. Without JavaScript the site is English. To share a link in
Chinese, add `?lang=zh-Hans` or `?lang=zh-Hant`, e.g.
`https://sighan-dclp.github.io/dclp/cfp.html?lang=zh-Hant` (`?lang=zh` also means Simplified).

Names, affiliations, emails and URLs are shared and need no spans. Don't use `lang` attributes for
anything else — a `lang="zh"` tag on a Chinese word inside English text would be hidden in
English mode. Each page's Chinese tab titles are in `data-title-zh-hans` / `data-title-zh-hant`
on `<html>`.

If you change `style.css` or `lang.js`, bump the `?v=` on its link in every page. GitHub Pages lets
browsers cache them for ten minutes, and new HTML with an old stylesheet shows every language at
once.

## Local preview

From the repository root:

```bash
python3 -m http.server 8765
```

Then open <http://localhost:8765>.

## Deployment

Served by GitHub Pages from the repository root. All internal links are relative, so the tree also
works from a subdirectory or from a `file://` path.

`.nojekyll` disables Jekyll processing — the site is plain HTML and needs no build.

## Theming

`assets/css/style.css` holds all design tokens at the top. `data-site="dclp"` on `<html>` swaps
the accent from cinnabar to jade — that is the only difference between the two sites. Dark mode
is handled by `prefers-color-scheme`; no toggle is needed.

## Contact

<sighandclp@gmail.com>
