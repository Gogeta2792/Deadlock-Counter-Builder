---
name: git-commit-message-only
description: Generates a git commit message (subject + optional body) following the team's git commit conventions. Use when the user asks for a commit message or invokes `/commit-message`; outputs the subject and body in separate fenced code blocks for easy copy-paste, and never creates a commit.
---

# Git Commit Message Only

## Instructions

When invoked, generate a single git commit message using the team's conventions in [reference.md](reference.md).

1. Inspect changes (never commit):
   - Prefer staged changes: run `git diff --cached`.
   - If empty, run `git diff`.
   - Also gather quick stats:
     - staged/unstaged: `git diff --cached --stat` (or `git diff --stat`)
     - staged/unstaged: `git diff --cached --numstat` (or `git diff --numstat`)
2. If there is no diff to analyze, ask the user for:
   - a short summary of what changed, and
   - whether it is a `bug fix`, `chore`, `docs`, or a specific code area (scope).
3. Choose an optional prefix (one only):
   - Scope prefix for code-focused changes: `UI: ...`, `Main.java: ...`, `Parser: ...`
   - Category prefix for non-code chores: `bug fix: ...`, `chore: ...`, `docs: ...`
   - Do not use both scope and category unless truly necessary.
4. Write the subject line:
   - Imperative mood (e.g., `Fix`, `Add`, `Update`, `Normalize`, `Handle`).
   - Capitalize the first letter.
   - Do not end with a period.
   - Aim for ~50 characters; hard limit 72 characters.
5. Decide whether to include a body:
   - Include a body when changes are non-trivial (heuristic: multiple files or roughly more than ~25 total lines added+removed).
   - If trivial, output subject only.
6. Write the body (if included):
   - Formatting:
     - Git expects one blank line between subject and body when they are combined; the subject and body are emitted in separate code blocks, so the user inserts that blank line when pasting into a single field or file.
     - Wrap body lines at 72 characters.
     - Use blank lines between paragraphs.
     - Use bullets when it improves clarity.
   - Content:
     - Explain WHAT and WHY (avoid HOW).
     - Use the recommended structure/templates from the conventions when it fits.
7. Output rules (strict):
   - Return only the commit message text in fenced code blocks—no explanations, labels like `Subject:`, or other commentary outside those blocks.
   - **Subject:** Put the subject line alone in the first fenced code block (opening fence may use an info string such as `text`).
   - **Body:** If there is no body (trivial change), stop after the first code block. If there is a body, put the full body alone in a **second** fenced code block. Do not repeat the subject in the body block; do not put a leading blank line inside the body block.
   - When the user pastes into one commit message, they combine: contents of the first block, one blank line, then contents of the second block.

## Examples

Subject only (one code block):

```text
Add README.md
```

Subject + body (two code blocks):

```text
bug fix: Handle empty search query
```

```text
Search crashes when the query is empty because the filter assumes a
non-empty keyword.

Return all results on an empty query to match user expectations.
```
