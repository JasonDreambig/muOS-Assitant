#!/usr/bin/env sh
# Extracts all ```sh and ```bash fenced code blocks from Markdown files and
# runs `sh -n` (POSIX syntax check) on each one.
# Exits 1 if any snippet fails to parse.

set -e

ASSETS_DIR="$(cd "$(dirname "$0")/../assets" && pwd)"
TMPFILE="$(mktemp /tmp/muos_snippet_XXXXXX.sh)"
trap 'rm -f "$TMPFILE"' EXIT

errors=0
total=0

extract_and_check() {
    file="$1"
    in_block=0
    lang=""
    lineno=0
    block_start=0

    while IFS= read -r line; do
        lineno=$((lineno + 1))

        if [ "$in_block" -eq 0 ]; then
            case "$line" in
                '```sh'|'```bash'|'```shell')
                    in_block=1
                    lang="$line"
                    block_start=$lineno
                    : > "$TMPFILE"
                    ;;
            esac
        else
            case "$line" in
                '```')
                    in_block=0
                    total=$((total + 1))
                    if ! sh -n "$TMPFILE" 2>/tmp/sh_err; then
                        printf "FAIL  %s (block starting line %d):\n" "$file" "$block_start"
                        cat /tmp/sh_err
                        errors=$((errors + 1))
                    fi
                    ;;
                *)
                    printf '%s\n' "$line" >> "$TMPFILE"
                    ;;
            esac
        fi
    done < "$file"
}

find "$ASSETS_DIR" -name "*.md" | sort | while IFS= read -r mdfile; do
    extract_and_check "$mdfile"
done

# The while+subshell means we need a different mechanism to propagate the count.
# Re-run with awk to get a clean exit code based on actual failures.
ERRORS=0
TOTAL=0

for mdfile in $(find "$ASSETS_DIR" -name "*.md" | sort); do
    in_block=0
    block_start=0
    lineno=0
    : > "$TMPFILE"

    while IFS= read -r line; do
        lineno=$((lineno + 1))
        if [ "$in_block" -eq 0 ]; then
            case "$line" in
                '```sh'|'```bash'|'```shell')
                    in_block=1
                    block_start=$lineno
                    : > "$TMPFILE"
                    ;;
            esac
        else
            case "$line" in
                '```')
                    in_block=0
                    TOTAL=$((TOTAL + 1))
                    if ! sh -n "$TMPFILE" 2>/tmp/sh_err; then
                        printf "FAIL  %s (block at line %d):\n" "$mdfile" "$block_start"
                        cat /tmp/sh_err
                        ERRORS=$((ERRORS + 1))
                    fi
                    ;;
                *)
                    printf '%s\n' "$line" >> "$TMPFILE"
                    ;;
            esac
        fi
    done < "$mdfile"
done

if [ "$ERRORS" -gt 0 ]; then
    printf "\nFAIL — %d of %d shell snippet(s) have syntax errors\n" "$ERRORS" "$TOTAL"
    exit 1
fi

printf "OK — %d shell snippet(s) passed syntax check\n" "$TOTAL"
