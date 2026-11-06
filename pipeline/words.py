import sys, json
from faster_whisper import WhisperModel
src, out, lang, model = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
m = WhisperModel(model, device="cpu", compute_type="int8")
segs, info = m.transcribe(src, language=lang, word_timestamps=True, vad_filter=False, beam_size=5,
    initial_prompt="Casual Malayalam-English (Manglish) talk by an engineering startup founder about B.Tech final year projects, report, paper presentation, graphs, data points, tools, project assistance company in India.")
res=[]
for s in segs:
    res.append({"start":s.start,"end":s.end,"text":s.text.strip(),"words":[{"w":w.word.strip(),"s":w.start,"e":w.end} for w in (s.words or [])]})
json.dump(res, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(info.language, info.language_probability)
for r in res: print(f"[{r['start']:5.1f}-{r['end']:5.1f}] {r['text']}")
