---
name: git-commit-message-only
description: Generates a git commit message (subject + optional body) following the team's git commit conventions. Use when the user asks for a commit message or invokes `/commit-message`; returns only the message text and never creates a commit.
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
     - One blank line between subject and body.
     - Wrap body lines at 72 characters.
     - Use blank lines between paragraphs.
     - Use bullets when it improves clarity.
   - Content:
     - Explain WHAT and WHY (avoid HOW).
     - Use the recommended structure/templates from the conventions when it fits.
7. Output rules (strict):
   - Return only the commit message text.
   - Do not include explanations, labels like `Subject:`, or any extra commentary.
   - If a body exists, output exactly one blank line after the subject.

## Examples

Subject only:

```text
Add README.md
```

Subject + body:

```text
bug fix: Handle empty search query

Search crashes when the query is empty because the filter assumes a
non-empty keyword.

Return all results on an empty query to match user expectations.
```
