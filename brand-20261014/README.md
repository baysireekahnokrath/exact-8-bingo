# OCT. 26 — brand kit (14 Oct 2026)

Master brand OCT. 26 (our crafted things; 26 October). First collection Soi 2.
Sub-brand ห้าหมี FIVE BEARS by OCT. 26, first collection Love (pattern 01 products).

Everything reads from `brand.py`. Rebuild in this order:

    python3 logo/build.py                         # logo/svg (outlined, no fonts needed); logo/jobs.json renders logo/png
    python3 posters/build.py                      # posters/html + posters/jobs.json
    node tools/render.mjs <jobs.json>             # PNGs (logo jobs: see logo/png, posters: posters/jobs.json)
    python3 bible/build.py                        # bible/svg (hang tags, story card, bag, pattern, map, booth)
    python3 colorlab/build.py                     # colorlab/svg: seven palette boards (brand colour not decided yet)
    python3 research/build.py                     # research/svg: three crossbody bag concepts (data in research/research.py)
    python3 site/build.py                         # site/brandbook, launch, bible, colorlab, productlab, index

Fonts in `fonts/`: Syne (OCT. 26 logo), Anuphan (OCT. 26 Thai headings), Mitr (FIVE BEARS), IBM Plex Sans Thai (body). All SIL Open Font License, Google Fonts.
The birthday deck source is in `deck/project/` (Slides artifact files).

Pages: summary https://claude.ai/artifact/1bBApc1D6ewCk8bpq3AydB ·
brand bible https://claude.ai/artifact/4FtQN6WRW3cUF1rATo3jvi (content in bible.py) ·
color lab https://claude.ai/artifact/8yxyk7koPUSrBeYHtAWZYT · product lab https://claude.ai/artifact/MiABkv9sRLFUurcTqscmHt ·
brand book https://claude.ai/artifact/3asVqkM4vs6fGM3rihHSYp ·
launch kit https://claude.ai/artifact/AyvcJTzj5BY6spbPkZYQXS ·
deck https://claude.ai/artifact/D61pf56uCqYrktNuuFG2c6
