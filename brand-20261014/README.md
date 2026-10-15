# OCT. 26 — brand kit (14 Oct 2026)

Master brand OCT. 26 (our crafted things; 26 October). First collection SOI. 02 (from our root).
Palette #2 Soi Candy and the golden-ratio system (phi = 1.618) chosen 15 Oct 2026: see `GOLDEN` in brand.py.
Sub-brand ห้าหมี FIVE BEARS by OCT. 26, first collection Love (pattern 01 products).

Everything reads from `brand.py`. Rebuild in this order:

    python3 logo/build.py                         # logo/svg (outlined, no fonts needed) + logo/jobs.json for logo/png
    python3 posters/build.py                      # posters/html + posters/jobs.json
    node tools/render.mjs <jobs.json>             # PNGs (logo jobs: see logo/png, posters: posters/jobs.json)
    python3 bible/build.py                        # bible/svg (golden sizes: tag 55x89, card 89x55, bag 130x210x80, edition 89x89 mm)
    python3 colorlab/build.py                     # colorlab/svg: seven palette boards (#2 Soi Candy chosen)
    python3 research/build.py                     # research/svg: three crossbody bag concepts (data in research/research.py)
    python3 logolab/build.py                      # site/logolab.html: logo directions; chosen B tag + A letters + C seal (geometry in logolab/geometry.py)
    python3 site/build.py                         # site/brandbook, launch, bible, colorlab, productlab, index
    python3 techpack/build.py && node tools/pdf.mjs site/techpack.html techpack/oct26-techpack-a4.pdf   # tech pack, web + A4
    python3 deck/assets/build.py && node tools/render.mjs deck/assets/jobs.json
    python3 deck/build.py                         # deck/project slides (images are /_blob assets uploaded to the deck)

Brand names are drawn, not typed (logolab/geometry.py). Fonts in `fonts/`: Jost (Latin text, fonts/alt), Anuphan (OCT. 26 Thai headings), Mitr (FIVE BEARS), IBM Plex Sans Thai (body). All SIL Open Font License, Google Fonts.
The birthday deck source is in `deck/project/` (Slides artifact files).

Pages: summary https://claude.ai/artifact/1bBApc1D6ewCk8bpq3AydB ·
brand bible https://claude.ai/artifact/4FtQN6WRW3cUF1rATo3jvi (content in bible.py) ·
logo lab https://claude.ai/artifact/HoVpShtP9q9LKAZDFjxb8x · color lab https://claude.ai/artifact/8yxyk7koPUSrBeYHtAWZYT · unbranded palette generator https://claude.ai/artifact/DEiZWoJh5GpwyhAwDM2Umg (site/palettes.html, hand-written) · product lab https://claude.ai/artifact/MiABkv9sRLFUurcTqscmHt ·
brand book https://claude.ai/artifact/3asVqkM4vs6fGM3rihHSYp ·
launch kit https://claude.ai/artifact/AyvcJTzj5BY6spbPkZYQXS ·
deck https://claude.ai/artifact/D61pf56uCqYrktNuuFG2c6 ·
tech pack https://claude.ai/artifact/XR5yqf6HFfA4JoJ9eQvapd
