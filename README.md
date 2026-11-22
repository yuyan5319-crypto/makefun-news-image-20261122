# The World in One Day — Sunday, 22 November 2026

A make.fun entry for **news-image-20261122**: one image that sums up the
world's news of Sunday 22 November 2026.

## The image

A newspaper front page, drawn with Pillow by `render_image.py`:

- **Lead:** Iran claims new missile and drone strikes on U.S. Patriot
  radars at bases in Bahrain (IRGC claim, 22 Nov).
- **COP31** in overtime over fossil fuels; **Trump** vows a 10% cap on
  credit-card rates.
- Pentagon moves to curb U.S.–Canada defence ties; Kim's factory tour
  after a "Trump snub"; protests hit Meta offices in India.
- Talks open a path to a "killer robot" pact; WFP to aid 91 million in
  2027; youth take to the streets across Europe.
- Also today: Houthi missiles fired at Riyadh (all three intercepted),
  Florida's flood clean-up, 11 dead in tainted liquor in Manipur,
  "El Chapo Isidro" arrested, Estonia to shut its Russia border,
  Rohingya hail the world court's genocide verdict, Cummins keeps the
  Test captaincy, Modi opens the Nitish Setu bridge, and Seoul on the
  AI race.

Every headline was checked against news reported on 22 November 2026
(AP, AFP, BBC and others). Nothing is invented: claims are worded as
claims, and the verdict the Rohingya are hailing was delivered on
19 November — the celebrations it prompted are the 22 November story.

## The program

`main.py` (Python 3.13, standard library only) copies the `entry.png`
in this repository to `/output/entry.png` (`MAKEFUN_OUTPUT_DIR` stands
in for `/output` outside the grader). No network, no randomness: every
run writes the same bytes.

Rebuild the image locally (needs Pillow):

```sh
python3 render_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
