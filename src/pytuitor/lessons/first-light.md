## Text and numbers

A Python program is a set of instructions that the computer runs in order, from top to bottom.
We will start with two kinds of values: text and whole numbers.

**A string** is a value containing text, such as a word or a sentence.
A **type** describes what kind of value something is and which operations it supports.
Python calls the string type `str`.
Write a string inside matching quotes: `"Hello"` or `'Hello'`.
The quotes tell Python where the text begins and ends; they are not part of the text itself.

**An integer** is a whole number, such as `7`, `0`, or `-3`.
Python calls this type `int`.
Write integers without quotes so Python can use them in calculations.

## Display a value with print

`print()` is a built-in function: an operation Python already knows how to perform.
Put the value you want to display between its parentheses.
Using a function this way is called **calling** it; a value you pass to it is an **argument**.
By default, `print()` moves to a new line after displaying its value.

```python
print("Hello")
print(7)
print(2 + 3)
```

This program displays:

```text
Hello
7
5
```

An **expression** is code that produces a value, such as `2 + 3`.
Python calculates this expression before printing the result.
These calculation symbols are called **operators**.
Use `+` for addition, `-` for subtraction, and `*` for multiplication.

## Why the quotes matter

`2 + 3` adds two integers and gives `5`.
`"2" + "3"` joins two strings and gives `"23"`.
Even if a string contains digits, Python still treats it as text.

## Read, fix, and run again

Finding and fixing mistakes is called **debugging**.
For example, this instruction has an opening quote but no closing quote:

```text
print("Hello)
```

Python reports a `SyntaxError`, meaning it cannot read the instruction as written.
The message may say `unterminated string literal`: Python reached the end of the line before finding the quote that ends the string.
Look for the file and line number in the error output, then read the error type and message.
An arrow or caret (`^`) can help point to the problem, but check the surrounding instruction too.

Add the missing quote before the closing parenthesis:

```python
print("Hello")
```

Run the corrected program again: it should display `Hello`.
Make one correction at a time, then check whether the output matches what you expected.
Errors are clues you can use, not a sign that you cannot program.

## Exercise

Write a complete program that displays `Hello, explorer!` on the first line and the result of `6 * 7` on the second line.
Keep the greeting in quotes and write the calculation without quotes.

The **editor** is the area where you write code; the **console** shows output and accepts answers when a program asks for input.
Press **Ctrl+T** to move from the lesson to the editor, then type your changes.
Press **Ctrl+R** to run the program and see its output in the console.
Press **F5** to check the exercise requirements.
After Build passes, open Repair and fix a separate program that should produce the same output.
The short question below is optional practice.
