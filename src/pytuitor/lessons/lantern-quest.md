## Build a small text adventure

Use the variables, conditions, loops, lists, and functions you have learned to process a player's moves.
You start in a forest and can visit a cave to collect five coins.

Write a function called `play(moves)`.
`moves` is a list of strings, such as `["east", "take", "west"]`.
The function should return both the final location and the coin count.

## Returning two values

`return place, coins` returns the two values together as a **tuple**.
A tuple is an ordered group of values, often written with parentheses: `("forest", 0)`.
Unlike a list, you cannot replace its individual items after creating it.
For this exercise, write `return place, coins` at the end of your function.

## Game rules

- Start in `"forest"` with `0` coins.
- `"east"` moves from the forest to the cave.
- `"take"` in the cave collects `5` coins, once per game.
- `"west"` moves from the cave to the forest.
- Other moves do nothing; returning to the cave does not refill its treasure.

Use a boolean variable such as `collected = False` to remember whether the treasure has been taken.
Set it to `True` after collecting the coins.
`and` joins conditions that must both be true; `not collected` is true when `collected` is false.
For example, `place == "cave" and move == "west"` checks both the location and the move.

## Build it in steps

First, loop over the moves and implement east and west.
Then add treasure collection using your boolean variable.
Keep all three state variables outside the loop so they retain their values between moves.
Return the final pair after the loop has finished.

To try the game interactively, you may add `moves = input("Moves: ").split()` followed by `print(play(moves))` below the function.
Checks call `play` directly, so these interactive lines are optional.
These two lines let you type moves separated by spaces and display the returned result.
Run with `east take west`; the result should be `('forest', 5)`.
Then try `east take take` to check that treasure cannot be collected twice.

Once the checks pass, try adding a new location or an extra command of your own.
