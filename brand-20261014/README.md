# ห้าหมี · FIVE BEARS — brand kit (14 Oct 2026)

Everything reads from `brand.py`. Rebuild in this order:

    python3 logo/build.py                         # logo/svg (outlined, no fonts needed)
    python3 posters/build.py                      # posters/html + posters/jobs.json
    node tools/render.mjs <jobs.json>             # PNGs (logo jobs: see logo/png, posters: posters/jobs.json)
    python3 site/build.py                         # site/brandbook.html, launch.html, index.html

Fonts in `fonts/` are Mitr and IBM Plex Sans Thai (SIL Open Font License, Google Fonts).
The birthday deck source is in `deck/project/` (Slides artifact files).

Pages: summary https://claude.ai/artifact/1bBApc1D6ewCk8bpq3AydB ·
brand book https://claude.ai/artifact/3asVqkM4vs6fGM3rihHSYp ·
launch kit https://claude.ai/artifact/AyvcJTzj5BY6spbPkZYQXS ·
deck https://claude.ai/artifact/D61pf56uCqYrktNuuFG2c6
