import json, subprocess, numpy as np, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
W = sys.argv[1]; SUF = sys.argv[2] if len(sys.argv) > 2 else ""; SR = 48000
tl = json.load(open(f"{W}/timeline{SUF}.json")); N = int((tl["total"] + .5) * SR)
vo = np.zeros(N); fx = np.zeros(N)
def dec(p):
    raw = subprocess.check_output(["ffmpeg","-loglevel","error","-i",p,"-f","f32le","-ac","1","-ar",str(SR),"-"])
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)
for s in tl["scenes"]:
    a = dec(f"{W}/vo{SUF}/{s['id']}.mp3"); i = int(s["vo"] * SR); vo[i:i+len(a)] += a[:N-i]
rng = np.random.default_rng(1)
def whoosh(t0, dur=1.1, amp=.10):
    n = int(dur*SR); x = rng.standard_normal(n); out = np.zeros(n)
    for k in range(0, n, 2400):
        f = 300 + 2600 * np.sin(np.pi * k / n); sos = butter(2, [max(80,f*.6), min(20000,f*1.4)], 'bandpass', fs=SR, output='sos')
        out[k:k+2400] = sosfilt(sos, x[k:k+2400])
    env = np.sin(np.linspace(0, np.pi, n)) ** 2; i = int(t0*SR); seg = out*env*amp/(np.abs(out).max()+1e-9)
    fx[i:i+n] += seg[:N-i]
def thump(t0, amp=.22):
    n = int(.6*SR); t = np.arange(n)/SR; x = np.sin(2*np.pi*(55 + 40*np.exp(-t*18))*t) * np.exp(-t*7)
    i = int(t0*SR); fx[i:i+n] += (x*amp)[:N-i]
for s in tl["scenes"]:
    if s["start"] > 0: whoosh(max(0, s["start"] - .55))
    if s["id"] in ("s1","s2","s3","s4","s5","s6","s7"): thump(s["start"] + .15)
thump(tl["scenes"][1]["start"] + .45, .3)
bed = sosfilt(butter(2, 380, 'lowpass', fs=SR, output='sos'), rng.standard_normal(N))
bed = bed / np.abs(bed).max() * .05 * (1 + .3*np.sin(np.arange(N)/SR*2*np.pi/23))
fade = np.minimum(1, np.minimum(np.arange(N)/(2*SR), (N-np.arange(N))/(3*SR)))
mix = vo + fx + bed * fade
mix = mix / np.abs(mix).max() * .9
wavfile.write(f"{W}/audio{SUF}.wav", SR, (mix*32767).astype(np.int16))
print("ok", N/SR)
