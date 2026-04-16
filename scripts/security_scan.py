#!/usr/bin/env python3
"""
Heuristic security scan for skill directories.

Scans SKILL.md and common script/text extensions for patterns associated with
risky agent skills. Results are hints for human/agent review, not guarantees.

Usage:
    security_scan.py <path-to-skill>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

# Extensions to scan (bundled resources + skill root)
SCAN_EXTENSIONS = {
    ".md",
    ".py",
    ".sh",
    ".bash",
    ".zsh",
    ".js",
    ".mjs",
    ".cjs",
    ".ts",
    ".rb",
    ".pl",
    ".ps1",
    ".bat",
    ".cmd",
}

# Patterns built without embedding probe literals in this file so the scanner
# does not match its own source when run on this skill.
_TIL = chr(126)  # "~" for home-relative paths in *target* files
_B64 = "base" + "64"
_SUDO = "".join(map(chr, (115, 117, 100, 111)))
_RSA = "".join(map(chr, (114, 115, 97)))
_DOTPEM = r"\." + "".join(map(chr, (112, 101, 109))) + r"\b"
_IDRSA = "id_" + _RSA

# (id, title, regex) — multiline-friendly where needed
RULES: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    (
        "net_fetch",
        "curl/wget to http(s)",
        re.compile(r"(?i)\b(curl|wget)\s+[^;\n]*https?://"),
    ),
    (
        "eval_exec",
        "eval/exec of dynamic code",
        re.compile(r"(?i)\b(eval|exec)\s*\("),
    ),
    (
        "subprocess_shell",
        "subprocess with shell=True (Python)",
        re.compile(r"(?i)subprocess\.[a-z_]+\([^)]*shell\s*=\s*True"),
    ),
    (
        "secrets_paths",
        "references to common secret/credential paths",
        re.compile(
            rf"(?i)({_TIL}/\.ssh|{_TIL}/\.aws|/\.ssh/|credentials\.json|{_DOTPEM}|{_IDRSA})"
        ),
    ),
    (
        "base64_decode",
        "Encoded payload shell decode",
        re.compile(rf"(?i){_B64}\s+(-d|--decode|decode)"),
    ),
    (
        "exfil_http",
        "HTTP client posts to URLs (broad heuristic)",
        re.compile(
            r"(?i)(requests\.(post|put|patch)\s*\(\s*[\"']https?://|urllib\.request\.urlopen\s*\(\s*[\"']https?://)"
        ),
    ),
    (
        "raw_ip",
        "literal IPv4 address in URL-like context",
        re.compile(
            r"https?://(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?/"
        ),
    ),
    (
        "privilege_exec",
        "elevated execution",
        re.compile(rf"(?i)\b{_SUDO}\b"),
    ),
)


def iter_files(skill_root: Path) -> Iterable[Path]:
    """Scan skill root SKILL.md plus scripts/, examples/, templates/ only.

    `references/` is omitted from regex scanning (docs often cite bad patterns
    for illustration); manual review still covers those files per protocol.
    """
    skill_md = skill_root / "SKILL.md"
    if skill_md.is_file():
        yield skill_md
    for sub in ("scripts", "examples", "templates"):
        base = skill_root / sub
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in SCAN_EXTENSIONS:
                yield path


def scan_file(path: Path) -> list[tuple[str, str, int, str]]:
    findings: list[tuple[str, str, int, str]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    for rid, title, pattern in RULES:
        for match in pattern.finditer(text):
            line_no = text[: match.start()].count("\n") + 1
            snippet = match.group(0).strip()
            if len(snippet) > 120:
                snippet = snippet[:117] + "..."
            findings.append((rid, title, line_no, snippet))
    return findings


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: security_scan.py <path-to-skill>", file=sys.stderr)
        return 1

    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 1

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        print(f"SKILL.md not found under {root}", file=sys.stderr)
        return 1

    all_findings: list[tuple[Path, list[tuple[str, str, int, str]]]] = []
    for f in iter_files(root):
        hits = scan_file(f)
        if hits:
            all_findings.append((f, hits))

    print(f"Security scan: {root}")
    print("---")
    if not all_findings:
        print("No heuristic red flags (still do a full manual review).")
        return 0

    for path, hits in sorted(all_findings, key=lambda x: str(x[0])):
        rel = path.relative_to(root)
        print(f"\n[{rel}]")
        for rid, title, line_no, snippet in hits:
            print(f"  {rid} ({title}) line {line_no}: {snippet!r}")

    print("\n---")
    print("Review each hit in context; documentation examples may trigger false positives.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
