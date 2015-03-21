# narratr
## Style guide

This style guide is a subset of the PEP 8 style guide for Python (https://www.python.org/dev/peps/pep-0008/). There may be some differences from PEP 8 to better suit the project, so please check the style guide even if your are already familiar with PEP 8.

### Comments
Comments that contradict the code are worse than no comments. Always make a priority of keeping the comments up-to-date when the code changes!

Comments should be complete sentences. If a comment is a phrase or sentence, its first word should be capitalized, unless it is an identifier that begins with a lower case letter (never alter the case of identifiers!).

If a comment is short, the period at the end can be omitted. Block comments generally consist of one or more paragraphs built out of complete sentences, and each sentence should end in a period.

You should use two spaces after a sentence-ending period.

#### Block Comments

Block comments generally apply to some (or all) code that follows them, and are indented to the same level as that code. Each line of a block comment starts with a # and a single space (unless it is indented text inside the comment).

Paragraphs inside a block comment are separated by a line containing a single # .

#### Inline Comments

Use inline comments sparingly.

An inline comment is a comment on the same line as a statement. Inline comments should be separated by at least two spaces from the statement. They should start with a # and a single space.

Inline comments are unnecessary and in fact distracting if they state the obvious. Don't do this:
```
x = x + 1                 # Increment x
```
But sometimes, this is useful:
```
x = x + 1                 # Compensate for border
```

###Indentation

A Tab of size 4 spaces should be used per indentation level.

Continuation lines should align wrapped elements either vertically using Python's implicit line joining inside parentheses, brackets and braces, or using a hanging indent [5] . When using a hanging indent the following considerations should be applied; there should be no arguments on the first line and further indentation should be used to clearly distinguish itself as a continuation line.

Yes:
```
# Aligned with opening delimiter.
foo = long_function_name(var_one, var_two,
						 var_three, var_four)

# More indentation included to distinguish this from the rest.
def long_function_name(
		var_one, var_two, var_three,
		var_four):
	print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
	var_one, var_two,
	var_three, var_four)
```
No:
```
# Arguments on first line forbidden when not using vertical alignment.
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# Further indentation required as indentation is not distinguishable.
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```
The 4-space tab rule is optional for continuation lines.

Optional:
```
# Hanging indents *may* be indented to other than 4 spaces.
foo = long_function_name(
  var_one, var_two,
  var_three, var_four)
```
When the conditional part of an if -statement is long enough to require that it be written across multiple lines, it's worth noting that the combination of a two character keyword (i.e. if ), plus a single space, plus an opening parenthesis creates a natural 4-space tab indent for the subsequent lines of the multiline conditional. This can produce a visual conflict with the indented suite of code nested inside the if -statement, which would also naturally be indented to 4 spaces.

```
# No extra indentation.
if (this_is_one_thing and
    that_is_another_thing):
    do_something()

# Add a comment, which will provide some distinction in editors
# supporting syntax highlighting.
if (this_is_one_thing and
    that_is_another_thing):
    # Since both conditions are true, we can frobnicate.
    do_something()

# Add some extra indentation on the conditional continuation line.
if (this_is_one_thing
        and that_is_another_thing):
    do_something()
```
The closing brace/bracket/parenthesis on multi-line constructs may either line up under the first non-whitespace character of the last line of list, as in:
```
my_list = [
    1, 2, 3,
    4, 5, 6,
    ]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )
```
or it may be lined up under the first character of the line that starts the multi-line construct, as in:
```
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)
```

####Tabs or Spaces?

Tabs are the preferred indentation method. On no account should spaces be mixed with tabs during indentation.
