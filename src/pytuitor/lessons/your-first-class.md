## Objects keep data and related operations together
A class describes how to create a kind of object.
Each object made from the class is an instance with its own data.
The data an object keeps is its state, and the operations it provides are its behavior.

```python
class Counter:
    def __init__(self, start=0):
        self.value = start

    def increment(self):
        self.value = self.value + 1


counter = Counter(4)
counter.increment()
print(counter.value)
```

`__init__` sets up a new instance.
Python calls it when you create an object with `Counter(4)`, passing `4` as `start`.
`self` refers to the instance receiving a method call; Python supplies it automatically when you call `counter.increment()`.
Attributes such as `self.value` keep data on that object between method calls.
A method is a function defined inside a class.

## Build
Define a class `Wallet`.
`Wallet()` starts with a `.balance` of `0`.
Its method `deposit(amount)` adds a nonnegative integer amount to the balance and returns the new balance.
Its method `spend(amount)` returns `True` and subtracts the amount when affordable; otherwise it returns `False` without changing the balance.
Each wallet must have its own balance.
Amounts are always nonnegative integers.
Spending zero succeeds, even for an empty wallet.

## Repair
The broken spend method deducts money before checking affordability.
An unsuccessful spend must leave the wallet's balance unchanged.
