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
└── dclp/
    ├── index.html        workshop overview
    ├── cfp.html          call for papers
    ├── shared-task.html  document-level meaning representation parsing
    └── organizers.html   organizers + programme committee
```

No build step, no JavaScript, no dependencies. Every page is plain HTML plus one stylesheet.
Google Fonts (Source Serif 4 + Inter) load from a CDN and fall back to system fonts including
CJK faces.

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
