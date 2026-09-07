## Give a parameter a default
A parameter can have a default value when the caller leaves it out.

```python
def repeat_word(word, times=2):
    return word * times


print(repeat_word("ha"))
print(repeat_word("ha", times=3))
```

The first call returns `"haha"`; the second returns `"hahaha"`.
`times=3` is a keyword argument: it names the parameter receiving that value.
Required parameters go before parameters with defaults.
A variable assigned inside a function is normally local to that call.
Start accumulators inside the function so repeated calls do not share old results.

## Build
Define `subtotal(prices, discount=0)`.
`prices` is a list of nonnegative integer prices and `discount` is a nonnegative integer amount to subtract from the total, not a percentage.
Return the total after subtracting the discount, with a minimum of zero.
`subtotal([6, 4])` returns `10`; `subtotal([6, 4], discount=3)` returns `7`.
An empty list returns `0`, including when a positive discount is given.
Use the loop and accumulator pattern you already know.
Do not mutate the input list.

## Repair
The broken function subtracts the discount once per item.
The contract asks for one discount on the whole order.
