#!/usr/bin/env bash
# PostToolUse hook: run `ovweb lint` on a just-edited content file (~0.4 s).
# Errors go back to Claude via exit 2 so it self-corrects in the same turn; warnings and info
# stay silent here (the /check-web command surfaces them). Degrades to a no-op when the file is
# out of scope or ovweb is not installed — a hook that nags on every edit gets disabled.

file=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null) || exit 0
[ -n "$file" ] || exit 0

case "$file" in
  */docs/*.md | */shared/*.md | */docs/overrides/*.html) ;;
  *) exit 0 ;;
esac

command -v ovweb >/dev/null 2>&1 || exit 0
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

rel=${file#"$PWD"/}
[ -f "$rel" ] || exit 0

if ! output=$(ovweb lint "$rel" 2>&1); then
  printf '%s\n' "$output" | grep -F "error:" >&2
  exit 2
fi
exit 0
