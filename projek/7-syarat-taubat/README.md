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
