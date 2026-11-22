# Immanuel of Rome, *Maḥberot*: an English translation in progress

Site: <https://openseforim.org/immanuel/>

Immanuel ben Solomon of Rome (about 1261 to about 1335) wrote 28 *maḥberot* in Hebrew rhymed prose with poems set into it. No complete translation exists in any language. This repository holds a line-aligned Hebrew and English text and the scripts that build the side-by-side pages.

## Status

| Maḥberet | Status |
|---|---|
| 1 (the poet's ruin, the Prince, Time, his books, his wife) | Draft, 13-Nov-2026. 1,212 lines. Allusions not verified. 9 uncertain renderings. |
| 2 (Tamar and Beriah) | Pilot, 13-Nov-2026. 350 lines. Allusions not verified. 8 uncertain renderings. |
| 3–28 | Not started |

## Sources

- **Hebrew text:** [Project Ben-Yehuda, work 36886](https://benyehuda.org/read/36886), from the edition of Dov Yarden (Mosad Bialik, 1957). Fully vocalized, marked public domain, without Yarden's notes. The plain text is from the [public-domain dump](https://github.com/projectbenyehuda/public_domain_dump), file `txt/p156/m36886.txt`.
- **Early editions (scans):** [Brescia 1491](https://archive.org/details/ita-bnc-in1-00000512-001), [Constantinople 1535](https://archive.org/details/ldpd_in00034094629_000).

## Translations that exist

- Complete work: none.
- Maḥberet 28 (*Tofet and Eden*): Hermann Gollancz, [*Tophet and Eden*](https://archive.org/details/tophetedenhellpa01imma) (1921); Dana W. Fishkin, appendix to *Bridging Worlds* (Wayne State University Press); M. E. Stern, [*Tofet und Eden*](https://archive.org/details/tofetundedenode01stergoog) (German, 1865).
- The 38 sonnets: Yehudah Cohn, [*Mine Is the Golden Tongue*](https://primolevicenter.org/product/mineisthegoldentongue) (CPL Editions, 2023).
- Maḥberet 9: [Lev Taylor](https://simlev.blog/2025/10/10/immanuel-of-romes-9th-machberet/) (2025).

More links are on the site.

## Layout

| Path | Contents |
|---|---|
| `data/mahberet-NN.he.json` | Hebrew, split into blocks and lines |
| `data/mahberet-NN.en.txt` | English, one line for each Hebrew line |
| `data/mahberet-NN.notes.json` | Notes for the uncertain renderings (⚠) |
| `scripts/extract_hebrew.py` | Cuts one maḥberet from the dump and splits it into lines |
| `scripts/build_page.py` | Checks the alignment and writes `docs/mahberet-NN.html` |
| `docs/` | The GitHub Pages site |
| `notes/` | Working notes, including a verse attempt at the first sonnet |

## Build

The dump file is not in the repository. Download `txt/p156/m36886.txt` to `source/m36886.txt`, then:

```
py -3.13 scripts/extract_hebrew.py source/m36886.txt 2 data/mahberet-02.he.json
py -3.13 scripts/build_page.py 2 "The Second Maḥberet" "Tamar and Beriah: a contest of praise and dispraise"
```

`build_page.py` stops if the Hebrew and English line counts do not agree.

## English file format

- One line of English for each Hebrew line. A blank line ends a block.
- `@prose`, `@saying`, `@verse` set the kind of the blocks that follow. `@gap` puts a stanza space before the next block.
- `[Gen 20:13]` is an allusion reference. `⚠3` points to note 3.

## Credits

The English draft is by Claude (Anthropic), directed and reviewed by Ezra Brand.

## Licence

The English translation, the notes, the aligned text files and the build scripts: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (see `LICENSE`). The Hebrew text is Dov Yarden's edition as published by Project Ben-Yehuda, marked public domain there.
