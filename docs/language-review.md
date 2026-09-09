# Lesson language review

Reviewed all 75 teaching lessons and 12 projects in the unified syllabus order.
The review covered explanations, worked examples, exercise instructions, Repair descriptions, hints, check labels, and optional questions.
It used the current chapter prerequisites rather than the retired Beginner and Experienced paths.

## Review standard

Use plain English for instructions and standard Python or programming names for concepts.
Explain an unfamiliar term when introducing it, then use that term consistently.
Explain new syntax within the lesson before requiring learners to write or repair it.
Do not replace useful technical terms with invented metaphors or assume that programmers from another language already know Python syntax.
Projects may rely on their named preparation, while optional chapters must explain the Python features they introduce.

## Coverage and corrections

| Section | Units reviewed | Main corrections |
| --- | ---: | --- |
| Foundations | 21 | Define expressions, arguments, operators, methods, iterations, keyword arguments, accumulators, and exceptions; explain numeric and collection terminology; correct two Repair descriptions. |
| Everyday Python | 16 | Explain file encodings, paths, data formats, regex syntax, modules, entry points, library errors, random state, dates, and iterable inputs. |
| Building programs | 7 | Explain instances, state, enum inheritance, test suites, copies, validation, and file operations in concrete terms. |
| Python depth | 28 | Explain lazy evaluation, iterators, callbacks, folds, wrappers, metadata, protocols, annotations, type variables, properties, and testing dependencies; remove premature packaging instructions. |
| Specialized topics | 15 | Explain coroutines, event loops, concurrency, cancellation, semaphores, package metadata, command-line conventions, descriptors, metaclasses, method lookup, introspection, and registration. |

The decimal measurement Repair previously blamed conversion even though the program converted with `float()` correctly and used floor division afterward.
The collection-editing Repair previously claimed to remove every matching item, although its code could remove two.
Both now describe the supplied defect accurately.
Generic check feedback now asks learners to compare actual and expected results for the supplied input instead of referring to an unexplained contract or edge cases.
The Types and tests lesson no longer marks packaging as a taught concept; packaging remains in its dedicated chapter.

The review preserves lesson IDs, executable exercise requirements, checks, reference solutions, Repair programs, file layouts, and revisions.
Existing drafts and completed work remain compatible.
Python example blocks were syntax-checked, and representative lessons were inspected through the tutor at narrow and wide terminal sizes.

## Practical limits

This is an editorial and prerequisite review, not evidence that every learner will understand every sentence.
Learners who jump ahead need the listed preparation or equivalent knowledge.
Use the [learner study](learner-study.md) to identify words learners cannot explain and instructions they cannot act on without help.
Recheck this standard whenever lessons move or new syntax appears in examples, hints, or Repair code.
