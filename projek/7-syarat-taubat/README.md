# 7 Syarat Taubat Jalan Makrifat — video motion bercerita

Video 16:9 (1920×1080, 30 fps, ~3 min 50 s) dengan suara latar Bahasa Melayu dan kapsyen karaoke.

## Aliran kerja

```bash
W=folder-kerja                      # salin fail projek ini ke sini
python3 tts.py $W                   # narration.json -> vo/*.mp3 + vo/words.json (edge-tts, ms-MY-OsmanNeural)
python3 timeline.py $W              # -> timeline.json (masa setiap babak & perkataan)
python3 mix.py $W                   # -> audio.wav (suara + whoosh + bunyi latar lembut, tiada muzik)
(cd $W && python3 -m http.server 8765 --bind 127.0.0.1 &)
node preview.mjs pv 3 30 63 105     # tangkap bingkai pratonton
node render.mjs 0 1724 seg/s0.mp4   # render julat bingkai (jalankan 4 serentak)
```

Ubah teks suara dalam `narration.json`; jalankan semula `tts.py` dan `timeline.py` — animasi
mengikut masa perkataan secara automatik (fungsi `cue()` dalam `comp.html`).

Nota: di persekitaran awan, `tts.py` menggunakan CA proksi `/root/.ccr/ca-bundle.crt`.

## Versi 9:16 (TikTok/Reels/Shorts, ~1 min 57 s)

Skrip suara dipendekkan dalam `narration-9x16.json`; babak Mahsyar dan Ilmu digugurkan.
`comp-9x16.html` dijana daripada `comp-9x16.src.html` + blok ikon dalam `comp.html`.

```bash
python3 tts.py $W -9x16 && python3 timeline.py $W -9x16 && python3 mix.py $W -9x16
PAGE=comp-9x16.html VW=1080 VH=1920 node render.mjs 0 876 segv/s0.mp4   # 4 julat serentak
```

Zon selamat teks: y 250–1480 (atas = bar aplikasi, bawah = kapsyen/butang platform).
