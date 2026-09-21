# Learning and release decisions

## Immediate priorities

Complete specifications and trustworthy checks take priority over adding more completion signals.
Keep teaching separate from the active exercise, with a persistent Build or Repair heading and independently scrollable Markdown requirements.
Short requirements should give space back to the editor.
Check results must show the next action outside the scrolling case details, using words rather than color alone.

Reference comparison is explicitly revealed and read-only.
Compare the learner's saved snapshot with one correct approach, including supporting files, and ask for an explanation of a behavioral difference.
A textual difference is not proof that the learner's solution is wrong.
Optional prediction checkpoints provide a short conceptual pause in every chapter and never gate coding progress.
See [chapter challenge criteria](teaching-criteria.md) for the content review standard.

## Deliberate deferrals

Retrieval scheduling and mastery scoring remain deferred.
Existing practice and study-note profile fields remain loadable but inert, and no new completion gates or inferred mastery scores are introduced.
A future proposal needs an explicit learning model, opt-in controls, migration behavior, and evidence that the feature improves learning without misleading learners about mastery.
Learner studies are skipped at the user's request, so no teaching-effectiveness claim is made.

Textual status words, keyboard access, and monochrome readability are supported design requirements.
A fully linear screen-reader interface still needs dedicated assistive-technology evaluation; terminal screenshots and synthetic keyboard checks do not establish that support.
Keep this distinct from the tested color-independent status messages.

## Execution trust

The supported execution model is a local, single-user tutor running trusted code under the user's own permissions.
Resource limits, sanitized child environments, isolated imports, temporary workspaces, and child-process cleanup reduce accidental interference; they do not prevent arbitrary filesystem or network access by learner code.
Virtual environments separate packages, not operating-system permissions.
Expose this boundary through the Execution and privacy command and the workspace documentation.

No accounts or learning telemetry are required.
Ordinary lessons and checks stay offline; package installation and release lookup remain explicit network actions.
A shared service that accepts untrusted code would require a separate OS isolation design and is outside this product's deployment contract.

## Profile and release integrity

Save a complete temporary profile, flush and sync it, atomically replace the destination, then sync the containing directory.
If directory synchronization fails after replacement, report a durability warning without pretending the committed write was rolled back.
Preserve migration backups, historical completion, and both stage drafts; a changed exercise revision invalidates only its old checked-pass evidence.

Release requires evidence from the configured macOS/Linux Python matrix, installed-wheel checks, an upgrade journey, and explicit publication authorization.
Local validation is not a substitute for a missing Linux job, and a configured workflow is not evidence that it passed.
Keep branch-push authorization separate from package publication authorization.
