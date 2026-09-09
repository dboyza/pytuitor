## Give a parameter a default
A parameter can have a default value when the caller leaves it out.

```python
def repeat_word(word, times=2):
    return word * times


print(repeat_word("ha"))
print(repeat_word("ha", times=3))
```

Multiplying a string by an integer repeats the string that many times.
The first call returns `"haha"`; the second returns `"hahaha"`.
`times=3` is a keyword argument: it names the parameter receiving that value.
Required parameters go before parameters with defaults.
A variable assigned inside a function is normally **local**: it belongs to that function call.
An **accumulator** is a variable that keeps a running result, such as a total.
Start the total at zero inside the function so each call calculates its own result.

## Build
Define `subtotal(prices, discount=0)`.
`prices` is a list of nonnegative integer prices and `discount` is a nonnegative integer amount to subtract from the total, not a percentage.
Return the total after subtracting the discount, with a minimum of zero.
`subtotal([6, 4])` returns `10`; `subtotal([6, 4], discount=3)` returns `7`.
An empty list returns `0`, including when a positive discount is given.
Use the loop and accumulator pattern you already know.
Do not change the input list.

## Repair
The broken function subtracts the discount once per item.
The requirements ask for one discount on the whole order.
