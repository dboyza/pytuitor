## Your first complete tool
A project combines things you already practiced.
Here you will read two answers, convert one to a number, make a decision, and print a useful result.
You already know everything needed to solve it.

## Build
Read an integer age from the first input line and a ticket type from the second.
Save them in `age` and `kind`.
Valid ages are nonnegative integers.
An age under 12 costs 5 credits; an age of 65 or older costs 7 credits; everyone else pays 10 credits.
If the ticket type is exactly `"return"`, double that price.
Any other ticket type uses the single price.
Store the final integer in `price` and print `Price: N`, replacing `N` with that price.
For age `12` and kind `return`, print `Price: 20`.
For age `4` and kind `single`, print `Price: 5`.
Choose your own input prompts.

There are two separate decisions: first select a price by age, then decide whether to double it.
Use a fresh `if` for the second decision because it applies after every age branch.

## Repair and explore

Repair uses a parcel-pricing scenario with a zone, weight, and express choice.
Choose a base price by zone, add a weight surcharge only above 5, and add an express surcharge when the answer is `yes`.
After it passes, try the weight boundary and both kinds of zone and express choices.
