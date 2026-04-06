# DESIGN.md

# Best UI/UX Rules for Web Apps

This document captures practical UI/UX rules for web applications based on widely respected usability, accessibility, and product design guidance. These are strong defaults, not absolute laws. Break them only when there is a clear reason and evidence that a different choice is better for users.

## Core priorities

- Prioritize clarity over cleverness.
- Prioritize usability over visual novelty.
- Prioritize accessibility from the start, not as cleanup.
- Prioritize consistency unless inconsistency solves a real problem.
- Prioritize reducing user effort across every flow.

---

## 1. Visual hierarchy and layout

### Rule: Make the most important thing obvious first
**Why it matters**  
Users scan before they read. A clear hierarchy helps them understand what matters immediately.

**Example**  
A dashboard shows one primary KPI row, one primary action, and secondary filters below.

**What to avoid**  
Several equally prominent cards, buttons, or banners competing for attention.

### Rule: Reduce visible complexity
**Why it matters**  
Showing only what is needed makes interfaces easier to understand and less intimidating.

**Example**  
Display basic filters by default and hide advanced filters behind “More filters”.

**What to avoid**  
Dumping every setting, option, and edge case into the default view.

### Rule: Group related content clearly
**Why it matters**  
Spacing, headings, and alignment help users understand what belongs together.

**Example**  
Billing details, payment methods, and invoices are separated into clearly labeled sections.

**What to avoid**  
Weak sectioning, inconsistent spacing, and layouts where unrelated items appear visually connected.

---

## 2. Navigation and information architecture

### Rule: Use clear, descriptive navigation labels
**Why it matters**  
Users should know what they will get before they click.

**Example**  
Use “Billing”, “Invoices”, and “Team members” instead of vague labels like “Admin” or “Manage”.

**What to avoid**  
Cute wording, internal jargon, or category names that require interpretation.

### Rule: Keep navigation predictable and consistent
**Why it matters**  
Consistency lowers cognitive load and helps users build confidence.

**Example**  
Primary navigation stays in the same place and same order across the product.

**What to avoid**  
Moving major nav items between pages or renaming the same concept in different areas.

### Rule: Expose structure, not just pages
**Why it matters**  
Good information architecture helps users understand where they are and what else exists.

**Example**  
Use breadcrumbs, page titles, and section overviews for deeper product areas.

**What to avoid**  
Interfaces where users land on pages without context or orientation.

---

## 3. Interaction design

### Rule: Follow common UI conventions unless there is a strong reason not to
**Why it matters**  
Familiar patterns reduce learning time and mistakes.

**Example**  
Clickable items look clickable. Modals behave like modals. Links look like links.

**What to avoid**  
Inventing unusual interaction patterns for common actions.

### Rule: Keep users informed about system status
**Why it matters**  
Users should always know whether something is loading, saving, successful, or failed.

**Example**  
After pressing “Save”, show progress and then a clear confirmation.

**What to avoid**  
Silent state changes, mystery delays, or no feedback after an action.

### Rule: Keep users in control
**Why it matters**  
Undo, cancel, and escape paths reduce anxiety and make interfaces feel safer.

**Example**  
A destructive action includes confirmation and, when possible, undo.

**What to avoid**  
Flows that trap users, surprise them, or make recovery difficult.

### Rule: Prevent errors before explaining them
**Why it matters**  
Prevention is better than correction.

**Example**  
Disable impossible dates in date pickers and constrain numeric inputs where appropriate.

**What to avoid**  
Allowing obviously invalid input and only complaining after submission.

---

## 4. Forms and validation

### Rule: Use persistent labels
**Why it matters**  
Users need field context while typing, reviewing, and fixing errors.

**Example**  
Label: “Phone number”  
Placeholder: “e.g. 8123 4567”

**What to avoid**  
Using placeholders as the only label.

### Rule: Prefer simple single-column forms
**Why it matters**  
Single-column layouts are easier to scan and complete accurately.

**Example**  
A sign-up form stacks name, email, password, and confirm password vertically.

**What to avoid**  
Dense two-column forms unless the grouped fields are tightly related.

### Rule: Ask only for what is needed
**Why it matters**  
Every extra field adds friction.

**Example**  
Only request company information if the user selects a business account.

**What to avoid**  
Collecting optional or future-use data too early.

### Rule: Validate helpfully and at the right time
**Why it matters**  
Users need specific, actionable guidance without being interrupted too early.

**Example**  
“Enter a valid email address, like name@example.com.”

**What to avoid**  
Generic messages like “Invalid input” or aggressive inline errors while the user is still typing.

---

## 5. Accessibility

### Rule: Accessibility is a baseline requirement
**Why it matters**  
Accessible products are more usable for everyone and are essential for many users.

**Example**  
Support keyboard navigation, visible focus states, readable contrast, and proper labels.

**What to avoid**  
Removing focus outlines, using low-contrast text, or relying on color alone to convey meaning.

### Rule: Make interactions work for touch and keyboard
**Why it matters**  
Users interact in different ways depending on device, ability, and context.

**Example**  
Buttons and tappable targets are large enough and spaced far enough apart to avoid mis-taps.

**What to avoid**  
Tiny icons, dense control clusters, or drag-only critical interactions.

### Rule: Make errors and instructions understandable
**Why it matters**  
Accessibility is not just technical compliance. It is also clarity.

**Example**  
Error text explains both the issue and how to fix it.

**What to avoid**  
Relying only on red borders or icons without text.

---

## 6. Responsive design

### Rule: Reflow layouts instead of shrinking them
**Why it matters**  
Good responsive design preserves usability, not just visual fit.

**Example**  
A wide desktop table becomes stacked cards or a simplified mobile layout.

**What to avoid**  
Forcing horizontal scrolling for normal content.

### Rule: Design for mobile intentionally
**Why it matters**  
Mobile users face smaller screens, touch input, and often more interruptions.

**Example**  
Primary actions stay reachable, forms are easy to tap through, and key content appears earlier.

**What to avoid**  
Desktop-first layouts that become cluttered, hidden, or frustrating on phones.

### Rule: Choose navigation patterns based on screen size and task needs
**Why it matters**  
Navigation that works on desktop may not work well on mobile.

**Example**  
A mobile app may use bottom navigation for a few top-level destinations, while desktop uses a sidebar.

**What to avoid**  
Copying the same navigation pattern everywhere without considering context.

---

## 7. Feedback, states, and error handling

### Rule: Design all meaningful states
**Why it matters**  
Real products spend a lot of time in non-ideal states.

**Example**  
Design loading, empty, success, error, offline, and partial-success states.

**What to avoid**  
Only designing the happy path and leaving edge states blank or vague.

### Rule: Errors should help users recover
**Why it matters**  
A good error state reduces friction and restores progress.

**Example**  
“Upload failed. File exceeds 10MB. Try a smaller file or compress this one.”

**What to avoid**  
“Something went wrong.” with no explanation or next step.

### Rule: Make success visible too
**Why it matters**  
Users need confirmation that their action worked.

**Example**  
A toast confirms “Changes saved” after editing a profile.

**What to avoid**  
Actions that appear to do nothing.

---

## 8. Content clarity and readability

### Rule: Write for scanning
**Why it matters**  
Users skim interfaces quickly.

**Example**  
Use clear headings, short paragraphs, meaningful labels, and front-loaded keywords.

**What to avoid**  
Dense text blocks, vague headings, or long button labels that bury the main action.

### Rule: Use plain language
**Why it matters**  
Clear wording improves comprehension and confidence.

**Example**  
Use “Delete account” instead of “Initiate irreversible account deprovisioning”.

**What to avoid**  
Internal language, technical jargon, or overly clever microcopy.

### Rule: Make critical information easy to notice
**Why it matters**  
Warnings, costs, deadlines, and consequences should never feel hidden.

**Example**  
A subscription screen clearly shows billing amount, renewal timing, and cancellation policy.

**What to avoid**  
Hiding important conditions in tiny secondary text.

---

## 9. Trust, clarity, and reducing user friction

### Rule: Explain why sensitive information is needed
**Why it matters**  
Users are more likely to continue when requests feel justified and transparent.

**Example**  
“Phone number (used only for delivery updates)”.

**What to avoid**  
Requesting personal data with no explanation.

### Rule: Remove unnecessary steps wherever possible
**Why it matters**  
Every extra click, screen, or repeated entry creates drop-off risk.

**Example**  
Autocomplete addresses, remember previous choices, and avoid re-entering known data.

**What to avoid**  
Making users repeat information already provided.

### Rule: Build credibility visually and structurally
**Why it matters**  
Trust is influenced by clarity, polish, and predictability.

**Example**  
Clear page titles, polished spacing, transparent pricing, and straightforward error handling.

**What to avoid**  
Messy layouts, suspicious copy, inconsistent styling, or hidden terms.

---

## Tradeoffs and judgment

These rules are not equally rigid in every context.

- **Consistency vs optimization:** consistency is usually better, but sometimes one workflow needs a different pattern because the task is different.
- **Minimalism vs clarity:** fewer elements can look cleaner, but removing labels, instructions, or visible structure often harms usability.
- **Speed vs safety:** reduce friction for frequent actions, but add safeguards for destructive or high-risk actions.
- **Expert density vs beginner simplicity:** expert tools may tolerate denser UIs, but only if hierarchy and predictability remain strong.
- **Brand expression vs comprehension:** distinctive visual style is valuable, but never at the cost of clarity.

---

## Short checklist for reviewing a web app UI

- Is the primary action obvious on each screen?
- Can users understand what matters first at a glance?
- Are navigation labels clear and descriptive?
- Is the interface consistent across pages and flows?
- Does every action produce visible feedback?
- Are users protected from common mistakes?
- Are forms short, clear, and easy to recover from?
- Are labels persistent and validation specific?
- Is the app accessible by keyboard and touch?
- Does the mobile layout feel intentionally designed rather than squeezed?
- Is the content easy to scan and understand?
- Are sensitive requests explained clearly?
- Is unnecessary friction removed?

---

## The 10 most important rules if time is limited

1. Make the main action obvious.
2. Use plain language.
3. Keep navigation clear and consistent.
4. Give immediate system feedback.
5. Let users undo, cancel, or recover.
6. Prevent errors before they happen.
7. Use persistent form labels.
8. Make validation specific and helpful.
9. Treat accessibility as mandatory.
10. Remove unnecessary friction.

---

## Practical standard for teams

When designing or reviewing a web app, default to these questions:

- Is this clear?
- Is this consistent?
- Is this accessible?
- Is this efficient?
- Is this necessary?
- Is this easy to recover from if something goes wrong?

If the answer to any of those is no, the design probably needs another pass.
