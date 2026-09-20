## Track state in a small adventure

A program can model a changing situation with a few variables.
Set each variable before a loop so its value survives from one move to the next.
A location string can describe where the player is, a number can count collected items, and a boolean can remember whether a one-time event happened.

## Returning two values

`return place, coins` returns two values together as a tuple.
A tuple is an ordered group of values, often written with parentheses: `("forest", 0)`.
The caller can unpack the result into two names or inspect the tuple as a whole.

## Conditions depend on state

A branch can check both the current location and the command before changing state.
`and` joins conditions that must both be true.
`not collected` is true when `collected` is false.
A one-time action needs a boolean guard so visiting the same place again does not repeat the reward.

For example, `place == "cave" and move == "west"` checks the location and the move together.
The order of branches matters when a command is meaningful only in one location.
