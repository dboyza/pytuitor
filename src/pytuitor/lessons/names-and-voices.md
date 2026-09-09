## Store a value in a variable

A **variable** lets you give a value a name and use it later.
For example:

```python
student = "Ada"
print(student)
```

Here, `student` is the variable and `"Ada"` is its string value.
The `=` symbol assigns the value on the right to the variable on the left.
The second line displays `Ada` because Python looks up the value of `student`.
Writing `print("student")` instead would display the word `student`.

You can assign a different value later:

```python
student = "Ada"
student = "Lin"
print(student)
```

This displays `Lin`.
Variable names are case-sensitive: `student` and `Student` are different names.

## Ask the user a question

`input()` pauses the program so the user can type an answer and press Enter.
The text inside its parentheses is the question, called a **prompt**.
The function **returns** the typed answer as a string: it gives that value back to the code that called it.
Use `=` to store that answer in a variable:

```python
student = input("What is your name? ")
print(student)
```

Run this program, type `Ada` in the console when the question appears, and press Enter.
The program continues and displays `Ada`.
You do not type quotes around your answer in the console.

An answer from `input()` is always a string, even if you type digits.
To calculate with a whole-number answer, convert it with `int()`:

```python
age = int(input("How old are you? "))
print(age + 1)
```

For this example, type a whole number such as `20`.
Other text, such as `twenty`, produces a `ValueError` because it cannot be converted to an integer.

## Put a variable into a message

An **f-string** is a string that can include the values of variables.
Write `f` just before the opening quote and put the variable inside curly braces, `{` and `}`:

```python
student = "Ada"
greeting = f"Welcome, {student}!"
print(greeting)
```

This displays `Welcome, Ada!`.
Python replaces `{student}` with `Ada` when it creates the string.
The braces are not displayed.

## Exercise

Ask for the user's name and store the answer in `student`.
Create a variable called `greeting` containing `Welcome, `, their name, and `!`.
Print the greeting.

Use Run to try your own name in the console.
Then use Check: it tests several names automatically.
A **hard-coded** greeting uses one fixed name instead of the answer from `input()`, so it will not pass.
