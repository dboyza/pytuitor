# Learning and release decisions

## Learning and feedback

Complete specifications and trustworthy checks take priority over adding more completion signals.
Keep teaching separate from the active exercise, with a persistent Build, Extend, or Repair heading and independently scrollable Markdown requirements.
Short requirements should give space back to the editor.
Check results must show the next action outside the scrolling case details, using words rather than color alone.

Reference comparison is explicitly revealed and read-only.
Compare the learner's saved snapshot with one correct approach, including supporting files, and ask for an explanation of a behavioral difference.
A textual difference is not proof that the learner's solution is wrong.
Optional prediction checkpoints provide a short conceptual pause in every chapter and never gate coding progress.
See [chapter challenge criteria](teaching-criteria.md) for the content review standard.

## Reviews and evidence boundaries

[Optional mixed reviews](learning-experience.md#optional-mixed-review) provide local scheduling, independent drafts, and controls to defer or pause suggestions.
Reviews never block Continue or award course credit, and the app does not infer mastery scores.
Legacy practice and study-note profile fields remain loadable but inert; current review records and personal notes are separate.
Use the [learner study protocol](learner-study.md) to evaluate learning outcomes; executable checks alone do not establish teaching effectiveness.

Textual status words, keyboard access, and monochrome readability are supported design requirements.
A fully linear screen-reader interface still needs dedicated assistive-technology evaluation; terminal screenshots and synthetic keyboard checks do not establish that support.
Keep this distinct from the tested color-independent status messages.

## Execution trust

The supported execution model is a local, single-user tutor running trusted code under the user's own permissions.
Resource limits, sanitized child environments, isolated imports, temporary workspaces, and child-process cleanup reduce accidental interference; they do not prevent arbitrary filesystem or network access by learner code.
Expose this boundary through the Execution and privacy command and the workspace documentation.

No accounts or learning telemetry are required.
Lessons and checks stay offline; the explicit release lookup is the tutor's only network action.
The optional online chapter teaches requests and pytest, which ship as tutor dependencies; its checks use practice servers on 127.0.0.1, and only its try-it steps in the learner's own terminal need internet.
A shared service that accepts untrusted code would require a separate OS isolation design and is outside this product's deployment contract.

## Profile and release integrity

Save a complete temporary profile, flush and sync it, atomically replace the destination, then sync the containing directory on Unix or request write-through replacement on Windows.
If directory synchronization fails after replacement, report a durability warning without pretending the committed write was rolled back.
Preserve migration backups, historical completion, and both stage drafts; a changed exercise revision invalidates only its old checked-pass evidence.

Release requires recorded Windows/macOS/Linux verification, installed-wheel checks, an upgrade journey, and explicit publication authorization.
Verification runs locally; GitHub CI requires an explicit user request.
Validation on one platform is not evidence that another platform passed.
Keep branch-push authorization separate from package publication authorization.
