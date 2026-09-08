# Learner study

Use a scratch profile so this study does not alter normal learning progress:

```sh
pytuitor --data-dir /tmp/pytuitor-study
```

Run separate beginner and experienced sessions with separate scratch directories.
A self-run study can reveal usability problems, but familiarity with the product can hide confusing assumptions.
Automated checks and a developer's walkthrough do not establish that first-time learners understand the teaching.

## Session notes

Record the operating system, terminal application, terminal dimensions, selected path, lesson identifier, and the step where difficulty occurred.
Record what you expected, what happened, and whether help was needed.
Avoid recording personal input, complete source code, account details, filesystem paths, or terminal history.
Keep notes locally unless you deliberately choose to share them.

## Beginner session

Allow about 45 minutes and begin without knowing the intended interface flow.

1. Open the app and explain the difference between the available paths in your own words.
2. Choose Beginner, locate the next lesson, and open it using only the keyboard.
3. Explain a string and an integer using the first lesson's examples.
4. Complete Build without starter code, run it, and check the result.
5. Deliberately enter an incorrect answer and explain the expected and actual values shown by Check.
6. Complete Repair and explain why the original program failed.
7. Continue to the input lesson, type an answer in the console, stop execution, and run again.
8. Leave an unfinished draft, quit, reopen, and confirm the draft and stage were retained.
9. Open F10, discover how to move between lesson, editor, and console, and return to the dashboard.
10. Open a later lesson and determine what prerequisite knowledge it expects.

After foundational chapters, repeat the study with a multi-file project.
Create or switch files, run the entry point, export the project, and explain the difference between a project directory and a virtual environment.
Confirm the project can be understood without revealing the reference solution.

## Experienced session

Allow about 45 minutes and use an experienced programmer's existing knowledge without assuming familiarity with Python syntax.

1. Choose Experienced, mark familiar concepts, and explain which items Continue will skip.
2. Reopen a skipped lesson and confirm its content remains available.
3. Complete one Python semantics lesson using an alternative correct implementation.
4. Inspect every check's inputs, output, expected result, and pass/fail status.
5. Complete a Repair stage and explain the Python-specific behavior that caused the defect.
6. Use progressive hints, then deliberately reveal a reference solution and return to the untouched draft.
7. Open a project with more than one file, edit a supporting module, and verify Run and Check use the current files.
8. Create an environment and inspect the package-installation explanation without installing anything.
9. Open an advanced lesson about descriptors, metaclasses, or internals and identify its prerequisite knowledge.
10. Browse the syllabus and explain the next chapter's learning outcomes.

## Acceptance notes

For each task, record completed independently, completed with help, or could not complete.
Capture confusing wording verbatim along with the lesson identifier.
Treat missing prerequisites, unclear exercise contracts, lost drafts, blocked keyboard navigation, and misleading checks as release blockers.
Retest every corrected blocker through the same learner journey.
Also inspect the app at 80 × 24 and 140 × 44, including error messages, dialogs, file controls, and focus outlines.
