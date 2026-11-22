import json, sys
W = sys.argv[1]; SUF = sys.argv[2] if len(sys.argv) > 2 else ""
vo = json.load(open(f"{W}/vo{SUF}/words.json"))
PRE = {"intro":(0.8 if SUF else 1.2),"title":0.6,"mahsyar":0.5,"tiga":0.5,"gelincir":0.6,"ilmu":0.5,"doa":0.6}
POST = {"intro":0.4,"title":(1.1 if SUF else 1.6),"doa":(4.8 if SUF else 7.5),"s4":1.0,"s5":1.0}
XF = 0.45
t = 0.0; out = []
for v in vo:
    pre = PRE.get(v["id"], 0.8 if SUF else 1.1); post = POST.get(v["id"], 0.6 if SUF else 0.9)
    st = t; vs = st + pre; en = vs + v["dur"] + post
    out.append({"id": v["id"], "start": round(st,3), "vo": round(vs,3), "end": round(en,3),
                "words": [{"w": w["w"], "s": round(vs + w["s"],3), "e": round(vs + w["s"] + w["d"],3)} for w in v["words"]]})
    t = en - XF
total = out[-1]["end"]
json.dump({"total": round(total,3), "scenes": out}, open(f"{W}/timeline{SUF}.json","w"), ensure_ascii=False)
for s in out: print(s["id"], s["start"], s["vo"], s["end"])
print("total", total)
