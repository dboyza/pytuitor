## Define your own function

You have already called built-in functions such as `print()` and `input()`.
A **function** groups instructions under a name so you can reuse them.
Use `def` to define one:

```python
def double(number):
    return number * 2


answer = double(4)
print(answer)
```

`double` is the function's name.
`number` is a **parameter**, a variable that receives a value when the function is called.
The value `4` in `double(4)` is called an **argument**.
The indented line is the function's body.

Defining the function does not run its body.
Calling `double(4)` runs the body with `number` set to `4`.
`return` ends the function and sends `8` back to the caller, which stores it in `answer`.

## Return and print do different jobs

`return` gives the caller a value to use.
`print()` displays something in the console.
A function that finishes without `return` gives back `None`, Python's value for "no result".

```python
def double(number):
    print(number * 2)


answer = double(4)
print(answer)
```

This displays `8`, then `None`.
Printing `8` inside the function did not return it to `answer`.

## Exercise

Write `def heal(health, potion):` and implement its body to return `health + potion`, with a maximum result of `100`.
For example, `heal(20, 10)` should return `30`, and `heal(90, 25)` should return `100`.

Use a variable to calculate the new health, an `if` to handle values above 100, and `return` to send back the answer.
You may add `print(heal(90, 25))` outside the function so you can see the result when you run it.
Checks call the function directly, so this extra print is optional.

## Read an error message

If a run fails, look at the error type and the line number in your code.
`NameError` often means a variable name is misspelled or has not been assigned yet.
`TypeError` often means you used an operation on the wrong kind of value, such as adding a string to an integer.
Fix one problem, run again, and compare what changed.
