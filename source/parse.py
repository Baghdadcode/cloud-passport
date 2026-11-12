"""Turn the MIT-licensed SAA-C03 study repo into data.js for the quiz app."""
import json, re, sys, pathlib, markdown

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])

CHAPTERS = [
    ("01-AWS-Fundamentals", "fund", "AWS Fundamentals", "#2449A6"),
    ("02-IAM", "iam", "IAM", "#BF2F2A"),
    ("03-Compute", "compute", "Compute", "#17734F"),
    ("04-Storage", "storage", "Storage", "#66399B"),
    ("05-Database", "db", "Databases", "#0F6F7A"),
    ("06-Networking", "net", "Networking", "#2449A6"),
    ("07-Security", "sec", "Security", "#5A1424"),
    ("08-Application-Integration", "integ", "App Integration", "#17734F"),
    ("09-Monitoring", "mon", "Monitoring", "#BF2F2A"),
    ("10-Migration", "mig", "Migration & Transfer", "#66399B"),
    ("11-Analytics", "ana", "Analytics & ML", "#0F6F7A"),
    ("12-Architecture-Patterns", "arch", "Architecture Patterns", "#5A1424"),
    ("13-Cost-Optimization", "cost", "Cost Optimization", "#2449A6"),
    ("14-Practice", "mixed", "Mixed Practice", "#8A5300"),
]

md = lambda s: markdown.markdown(s, extensions=["tables", "sane_lists"])
NO_SHUFFLE = re.compile(r"\b(all|none|both) of the above\b|\b(both )?[A-F] and [A-F]\b|^(all|none|both) of", re.I)

questions, chapters, skipped = [], [], []
for folder, cid, title, color in CHAPTERS:
    text = (SRC / folder / "PRACTICE-QUESTIONS.md").read_text(encoding="utf-8")
    blocks = re.split(r"^###\s+Question\s+(\d+)[^\n]*\n", text, flags=re.M)
    n = 0
    for i in range(1, len(blocks), 2):
        num, body = blocks[i], blocks[i + 1]
        body = body.split("\n---")[0] if "</details>" in body.split("\n---")[0] else body
        m = re.search(r"^(.*?)\n\s*A[.)]\s", body, re.S)
        ans = re.search(r"\*\*Answer:\s*([A-F](?:\s*,\s*[A-F])*)\s*\*\*", body)
        tick = re.findall(r"^\s*([A-F])[.)]\s+.*✓", body, re.M)
        if not m or not (ans or tick):
            skipped.append(f"{folder} Q{num}: no stem/answer")
            continue
        stem = re.sub(r"\*\*Options:?\*\*:?", "", m.group(1)).strip()
        if ans:
            correct_letters = ans.group(1).split(",")
            expl = body.split(ans.group(0), 1)[1].split("</details>")[0]
            optsrc = body.split("<details>")[0]
        else:
            correct_letters = tick
            parts = re.split(r"\*\*Explanation:?\*\*:?", body, maxsplit=1)
            optsrc, expl = re.sub(r"\s*✓", "", parts[0]), (parts[1] if len(parts) > 1 else "")
        opts = re.findall(r"^\s*([A-F])[.)]\s+(.+?)\s*$", optsrc, re.M)
        letters = [l for l, _ in opts]
        if letters != list("ABCDEF"[: len(letters)]) or len(letters) < 2:
            skipped.append(f"{folder} Q{num}: options {letters}")
            continue
        correct = ["ABCDEF".index(x.strip()) for x in correct_letters]
        expl = re.sub(r"^\s*\*\*Explanation:?\*\*:?\s*", "", expl.strip())
        texts = [t for _, t in opts]
        n += 1
        questions.append({
            "id": f"{cid}-{num}",
            "c": cid,
            "q": md(stem),
            "o": [md(t).removeprefix("<p>").removesuffix("</p>") for t in texts],
            "a": correct,
            "x": re.sub(r"(\s*<hr />)+\s*$", "", md(expl)),
            "fixed": any(NO_SHUFFLE.search(t) for t in texts),
        })
    lesson_path = SRC / folder / "ULTRA-FAST-LEARN.md"
    lesson = md(re.sub(r"^# .*\n", "", lesson_path.read_text(encoding="utf-8"), count=1)) if lesson_path.exists() else ""
    chapters.append({"id": cid, "title": title, "color": color, "count": n, "lesson": lesson})

OUT.write_text("window.BANK=" + json.dumps({"chapters": chapters, "questions": questions}, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8")
print(len(questions), "questions;", sum(len(q["a"]) > 1 for q in questions), "multi;", sum(q["fixed"] for q in questions), "fixed")
print("\n".join(skipped))
for c in chapters: print(c["id"], c["count"])
