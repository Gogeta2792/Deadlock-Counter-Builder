# Team Git Commit Conventions

This document defines how we write commit messages and name branches, aligned with SE-EDU Git conventions.

## 1. Goals

* Make history readable and searchable
* Help reviewers understand changes quickly
* Reduce "mystery commits" and noisy logs

## 2. Commit message - Subject line (required)

Every commit must have a well-written subject line.

### 2.1 Hard rules

* Keep it short

  * Target: 50 characters
  * Hard limit: 72 characters
* Use the imperative mood

  * Good: `Add README.md`
  * Bad: `Added README.md`
  * Bad: `Adding README.md`
* Capitalize the first letter

  * Good: `Move index.html file to root`
  * Bad: `move index.html file to root`
* Do not end with a period

  * Good: `Update sample data`
  * Bad: `Update sample data.`

### 2.2 Optional prefix: `<scope>:` or `<category>:`

You may add a prefix in front when it improves clarity.

**Scope prefix examples (preferred for code changes):**

* `Person class: Remove static imports`
* `Main.java: Remove blank lines`
* `UI: Improve empty-state message`

**Category prefix examples (preferred for non-code chores):**

* `bug fix: Add space after name`
* `chore: Update release date`
* `docs: Update user guide for export feature`

Guidelines:

* Use either scope or category, not both, unless it is truly necessary.
* Use a consistent scope vocabulary (module/class/file names).
* Keep prefixes short and lower maintenance.

### 2.3 Subject quality checklist

Before committing, check:

* [ ] One clear intent (one logical change)
* [ ] Specific verb + object (avoid vague "Update stuff")
* [ ] No implementation detail that belongs in the body

## 3. Commit message - Body (required for non-trivial commits)

Add a body when the commit is not self-explanatory from the subject line.

### 3.1 Formatting rules

* Separate subject from body with a blank line.
* Wrap body lines at 72 characters.
* Use blank lines to separate paragraphs.
* Use bullet points if it improves clarity.

### 3.2 Content rules

* Explain **WHAT** and **WHY**, not **HOW**.

  * Readers can inspect the diff to see how it was implemented.
* If the body becomes long, that is a signal the commit might need to be split.
* Avoid repeating information already present in code comments in the same commit.

### 3.3 Recommended body structure

Use this structure when it fits:

1. Current situation (present tense)
2. Why it needs to change
3. What is being done (imperative mood)
4. Why it is done that way
5. Other relevant info (links, follow-ups, references)

Tip:

* Avoid words like "currently" or "originally" when describing the current
  situation - the tense already implies it.
* Use "Let's" to clearly mark the start of the change action if helpful.

### 3.4 Body templates

**Template A - short body**

```text
<Subject>

<What changed, at a high level>

<Why we changed it>
```

**Template B - structured body**

```text
<Subject>

<Current situation>

<Why it needs to change>

Let's,
* <do X>
* <do Y>

<Why it is done that way>

<Other relevant info>
```

## 4. Examples

### 4.1 Trivial commit (subject only)

```text
Add README.md
```

### 4.2 Non-trivial commit (subject + body)

```text
Route service: Normalize travel time units

Travel-time values are stored in mixed units across the routing
pipeline, which causes inconsistent UI display and test flakiness.

Let's,
* store travel time internally in seconds
* convert units only at UI boundaries

This keeps calculations consistent and makes formatting a pure
presentation concern.
```

### 4.3 Bug fix commit

```text
bug fix: Handle empty search query

Search crashes when the query is empty because the filter assumes a
non-empty keyword.

Return all results on an empty query to match user expectations.
```

### 4.4 Refactor commit

```text
Parser: Extract shared validation helpers

Multiple parser branches duplicate the same validation logic, making
it easy for behavior to diverge.

Let's extract common validation into a single helper class.

This reduces duplication and centralizes rule updates.
```

## 5. Branch names

Follow these rules to improve consistency:

* Use a meaningful name consisting of relevant keywords, in kebab case.

  * Example: `refactor-ui-tests`
* If the branch is related to an issue, use:

  * `issueNumber-some-keywords-from-issue-title`
  * Example: `1234-ui-freeze-error`

### 5.1 Branch naming checklist

* [ ] Kebab case only (lowercase + hyphens)
* [ ] Keywords describe the outcome, not the implementation
* [ ] Issue number included when there is a tracked issue

## 6. Team rules of thumb

* Prefer many small, reviewable commits over one massive commit.
* Keep each commit buildable whenever practical.
* If doing a multi-commit PR, make each commit tell a coherent story.

## 7. Quick reference

### Subject line

* 50 chars target, 72 chars max
* Imperative mood
* Capitalized first letter
* No trailing period
* Optional `Scope:` or `category:` prefix

### Body

* Blank line after subject
* Wrap at 72 chars
* Explain WHAT and WHY, not HOW
* Use the recommended structure when it helps
