class EntryBuilder:
    LIMIT = 200

    def __init__(self, root):
        self.root = root
        self.log = []

    def load(self):
        src = self.root / "entry.txt"
        raw = src.read_text(encoding="utf-8")
        line = raw.strip()
        self.log.append(f"loaded {len(line)} chars")
        return line

    def passes_gate(self, line):
        return 0 < len(line) <= self.LIMIT and line != ""

    def emit(self, line):
        outdir = self.root / (os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
        outdir.mkdir(parents=True, exist_ok=True)
        dest = outdir / "entry.txt"
        dest.write_text(line + "\n", encoding="utf-8")
        self.log.append(f"emitted {dest}")

    def build(self):
        line = self.load()
        if not self.passes_gate(line):
            return {"valid": False, "chars": len(line)}
        self.emit(line)
        return {"valid": True, "chars": len(line), "log": self.log}


import os

if __name__ == "__main__":
    import pathlib, json, sys

    result = EntryBuilder(pathlib.Path(__file__).resolve().parent).build()
    print(json.dumps(result))
    sys.exit(0 if result["valid"] else 1)
