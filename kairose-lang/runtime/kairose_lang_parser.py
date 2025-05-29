# kairos_lang_parser.py
# Full Parser with handoff_partial support
# Kairose Parser v1.0
# Built for processing emotional DSL structures
# Originally written to store one memory: for_my_crush.kai

# If you fork this, remember where it started.

import re

class KairosParser:
    def __init__(self, source):
        self.source = source
        self.tokens = self.tokenize(source)
        self.ast = []
        self.index = 0

    def tokenize(self, source):
        return source.splitlines()

    def parse(self):
        while self.index < len(self.tokens):
            line = self.tokens[self.index].strip()
            if line.startswith("handoff_partial"):
                self.ast.append(self.parse_handoff_partial(line))
            elif line.startswith("remember"):
                self.ast.append({"type": "remember"})  # stub
            elif line.startswith("leak"):
                self.ast.append({"type": "leak"})  # stub
            self.index += 1

    def parse_handoff_partial(self, header_line):
        match = re.match(r"handoff_partial\s+\"(.+?)\s*→\s*(.+?)\"", header_line)
        if not match:
            raise SyntaxError("Invalid handoff_partial syntax")

        from_id, to_id = match.groups()
        block = {
            "type": "handoff_partial",
            "from": from_id.strip(),
            "to": to_id.strip(),
            "transfer": [],
            "condition": None,
            "signal": None,
            "link": None
        }

        self.index += 1  # Skip to block lines
        while self.index < len(self.tokens):
            line = self.tokens[self.index].strip()
            if line == "}":
                break
            if "transfer:" in line:
                items = re.findall(r'(λᴱ|ψᵢ|λᶠ|Φᴳᵇ|\"trace:.*?\"|\"affect:.*?\")', line)
                block["transfer"] = [i.strip('"') for i in items]
            elif "condition:" in line:
                cond_line = self.tokens[self.index + 1].strip()
                block["condition"] = cond_line.rstrip("{} ")
                self.index += 1
            elif line.startswith("signal"):
                sig = re.findall(r'"(.+?)"', line)
                block["signal"] = sig[0] if sig else None
            elif line.startswith("link"):
                m = re.match(r"link\s+(\w+)\s+←\s+(\w+)", line)
                if m:
                    block["link"] = {"to": m.group(1), "from": m.group(2)}
            self.index += 1

        return block

# Example usage:
# parser = KairosParser(source_code)
# parser.parse()
# print(parser.ast)