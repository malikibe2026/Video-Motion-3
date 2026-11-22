import asyncio, ssl, os, json, sys, subprocess
import edge_tts, edge_tts.communicate as c
c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
W = sys.argv[1]; SUF = sys.argv[2] if len(sys.argv) > 2 else ""; VOICE = "ms-MY-OsmanNeural"; os.makedirs(f"{W}/vo{SUF}", exist_ok=True)
items = json.load(open(f"{W}/narration{SUF}.json"))
async def one(it):
    comm = edge_tts.Communicate(it["text"], VOICE, rate="-6%", boundary="WordBoundary", proxy=os.environ.get("HTTPS_PROXY"))
    words = []
    with open(f"{W}/vo{SUF}/{it['id']}.mp3", "wb") as f:
        async for ch in comm.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                words.append({"w": ch["text"], "s": ch["offset"]/1e7, "d": ch["duration"]/1e7})
    dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{W}/vo{SUF}/{it['id']}.mp3"]))
    return {"id": it["id"], "dur": dur, "words": words}
async def main():
    out = [await one(it) for it in items]
    json.dump(out, open(f"{W}/vo{SUF}/words.json","w"), ensure_ascii=False, indent=1)
    for o in out: print(o["id"], round(o["dur"],2), len(o["words"]))
asyncio.run(main())
