# AI Song Generator

A Flask web app that turns **Arabic lyrics into a full song** — synthesizing a
vocal performance and a style-matched backing track, then mixing and exporting
the result as an MP3.

Powered by Suno's [Bark](https://github.com/suno-ai/bark) text-to-audio model.

## Features

- **Lyrics → song** — paste lyrics, choose a style, download an MP3.
- **Four musical styles**, each with dedicated voice and instrumentation prompts:
  - `إلكتروني` — bright electronic pop
  - `حماسي` — energetic stadium anthem
  - `هادئ` — calm ambient
  - `درامي` — dramatic cinematic score
- **Optional tempo** control (40–240 BPM), validated and clamped to a safe range.
- **Two-track production** — vocals and backing music are generated separately,
  level-balanced, overlaid, and normalized.
- **RTL Arabic web UI** with a one-click download link.

## How it works

1. `generate_song.py` preloads the Bark checkpoints once and reuses them for
   every request.
2. The **vocal track** is synthesized from the lyrics plus a style-specific
   voice prompt, using Bark's `v2/singing` history prompt.
3. The **backing track** is synthesized from an instrumental style description
   and padded to at least the length of the vocals.
4. The tracks are mixed (vocals +6 dB, backing −8 dB), normalized, and exported
   at 192 kbps.

## Getting started

```bash
pip install -r requirements.txt
python app.py
```

The app runs at <http://localhost:5000>.

- The **first** generation downloads and preloads the Bark checkpoints, so
  expect a longer wait on first use.
- MP3 export relies on `pydub`, which requires an **FFmpeg** install on the
  system `PATH`.
- Bark is compute-heavy and performs best on a CUDA GPU.

## Project layout

```
app.py                # Flask routes: / , /generate , /download
generate_song.py      # Bark loading, vocal + backing synthesis, mixing
templates/index.html  # RTL Arabic web UI
requirements.txt      # Flask, pydub, numpy, torch/torchaudio, Bark
```

## Notes

- Bark is multilingual and handles Arabic, but output quality varies with lyric
  length, structure, and diacritics.
- Generated audio and per-run logs are written locally (`song.mp3`, `logs/`)
  and are gitignored.
