## Lists can contain lists
A nested list is a list containing other lists, such as `["tea", ["bread", "rice"]]`.
The inner list can contain more lists in turn.
`isinstance(value, list)` returns `True` when a value is a list.
This lets a recursive function decide whether to visit children or handle one ordinary item.

```python
def count_words(items):
    count = 0
    for item in items:
        if isinstance(item, list):
            count += count_words(item)
        else:
            count += 1
    return count


print(count_words(["tea", ["bread", ["rice"]]]))  # 3
```

`count += 1` means `count = count + 1`.
An empty list contributes zero, so it is a base case without a special `if` statement.
Each recursive call receives an inner list, moving deeper into a finite structure until there are no children left.
The nesting structure is sometimes called a tree: each list branches into its items.

## Build
Define `sum_nested(items)`.
`items` is a finite list whose elements are integers or more lists following the same rule.
Return the sum of all integers at every depth.
`sum_nested([1, [2, [3]], 4])` returns `10`.
Empty lists contribute zero, negative integers are allowed, and nesting is at most 20 levels deep.
The input never contains cycles or other types.
Do not change any input list and do not print.
Try recursion, but any implementation with the required behavior is accepted.

## Repair
The broken function counts an inner list's immediate items instead of adding the integers inside it.
A list length says nothing about its values or deeper nesting.
