# narratr
## Style guide

This style guide is a subset of the PEP 8 style guide for Python (https://www.python.org/dev/peps/pep-0008/). There may be some differences from PEP 8 to better suit the project, so please check the style guide even if your are already familiar with PEP 8.

### Quick start to the Style Guide
Packages like pep8 (https://pypi.python.org/pypi/pep8) and autopep8 (https://pypi.python.org/pypi/autopep8) can be installed to make life easier.
Irrespective of everything else, before committing any code, it must be ensured that the code does not have any PEP8 style errors. An easy way to ensure that is to copy paste the code into an online PEP8 style checker like http://pep8online.com/

Some of the major style issues are Indentation, Comments and line length.

### Indentation

Use **4 spaces** per indentation level.

Indentation is the biggest style issue in Python. Spaces should be used, and not tabs. This does not mean that spaces have to be manually typed in. With most editors, typing a Tab can be automatically set to insert 4 spaces, instead of a Tab character. In Sublime Text for instance, click on the Tabs size/Spaces option on the bottom right corner, select "Indent Using Spaces" and "Tab Size: 4". Sublime would now insert four space characters when the tab button is pressed.

Continuation lines should align wrapped elements either vertically using Python's implicit line joining inside parentheses, brackets and braces, or using a hanging indent. When using a hanging indent the following considerations should be applied; there should be no arguments on the first line and further indentation should be used to clearly distinguish itself as a continuation line.

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
The 4-space rule is optional for continuation lines.

Optional:
```
# Hanging indents *may* be indented to other than 4 spaces.
foo = long_function_name(
  var_one, var_two,
  var_three, var_four)
```
When the conditional part of an if-statement is long enough to require that it be written across multiple lines, it's worth noting that the combination of a two character keyword (i.e. if ), plus a single space, plus an opening parenthesis creates a natural 4-space indent for the subsequent lines of the multiline conditional. This can produce a visual conflict with the indented suite of code nested inside the if -statement, which would also naturally be indented to 4 spaces. This PEP takes no explicit position on how (or whether) to further visually distinguish such conditional lines from the nested suite inside the if-statement. Acceptable options in this situation include, but are not limited to:
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

Spaces are the preferred indentation method. Any Python code indented with a mixture of tabs and spaces should be converted to using spaces exclusively.

When invoking the Python 2 command line interpreter with the -t option, it issues warnings about code that illegally mixes tabs and spaces. When using -tt these warnings become errors. These options are highly recommended!

###Maximum Line Length

Limit all lines to a maximum of 79 characters.

For flowing long blocks of text with fewer structural restrictions (docstrings or comments), the line length should be limited to 72 characters.

Limiting the required editor window width makes it possible to have several files open side-by-side, and works well when using code review tools that present the two versions in adjacent columns.

The default wrapping in most tools disrupts the visual structure of the code, making it more difficult to understand. The limits are chosen to avoid wrapping in editors with the window width set to 80, even if the tool places a marker glyph in the final column when wrapping lines. Some web based tools may not offer dynamic line wrapping at all.

Some teams strongly prefer a longer line length. For code maintained exclusively or primarily by a team that can reach agreement on this issue, it is okay to increase the nominal line length from 80 to 100 characters (effectively increasing the maximum length to 99 characters), provided that comments and docstrings are still wrapped at 72 characters.

The Python standard library is conservative and requires limiting lines to 79 characters (and docstrings/comments to 72).

The preferred way of wrapping long lines is by using Python's implied line continuation inside parentheses, brackets and braces. Long lines can be broken over multiple lines by wrapping expressions in parentheses. These should be used in preference to using a backslash for line continuation.

Backslashes may still be appropriate at times. For example, long, multiple with -statements cannot use implicit continuation, so backslashes are acceptable:
```
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())
```

Another such case is with assert statements.

Make sure to indent the continued line appropriately. The preferred place to break around a binary operator is after the operator, not before it. Some examples:
```
class Rectangle(Blob):

    def __init__(self, width, height,
                 color='black', emphasis=None, highlight=0):
        if (width == 0 and height == 0 and
                color == 'red' and emphasis == 'strong' or
                highlight > 100):
            raise ValueError("sorry, you lose")
        if width == 0 and height == 0 and (color == 'red' or
                                           emphasis is None):
            raise ValueError("I don't think so -- values are %s, %s" %
                             (width, height))
        Blob.__init__(self, width, height,
                      color, emphasis, highlight)
```

###Blank Lines

Separate top-level function and class definitions with two blank lines.

Method definitions inside a class are separated by a single blank line.

Extra blank lines may be used (sparingly) to separate groups of related functions. Blank lines may be omitted between a bunch of related one-liners (e.g. a set of dummy implementations).

Use blank lines in functions, sparingly, to indicate logical sections.

Each python file should have exactly one black line at the end.

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



#Updated Sections
##Introduction
This document gives coding conventions for narratr
##Code lay-out
###Indentation
Use 4 spaces per indentation level. For a scene, the setup, action, and cleanup must all begin on the same indentation level

**Yes:**
scene $1 { 
    setup:
    action:
        say "THE MATRIX HAS YOU"				
    cleanup: 
} 

**No:**
scene $1 { 
setup:
action:
say "THE MATRIX HAS YOU"				
cleanup: 
} 


The closing brace/bracket/parenthesis on multi-line constructs may either line up under the first non-whitespace character of the last line of list, as in:
my_list = [
    1, 2, 3,
    4, 5, 6,
    ]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )


or it may be lined up under the first character of the line that starts the multi-line construct, as in:
my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)


###Tabs or Spaces?
Spaces are the preferred indentation method.
Tabs should be used solely to remain consistent with code that is already indented with tabs.
###Maximum Line Length
Limit all lines to a maximum of __ characters.
##String Quotes
In narratr, single-quoted strings and double-quoted strings are the same. 

##Comments
Comments that contradict the code are worse than no comments. 
If a comment is short, the period at the end can be omitted. Block comments generally consist of one or more paragraphs built out of complete sentences, and each sentence should end in a period.

###Block Comments
Block comments generally apply to some (or all) code that follows them, and are indented to the same level as that code. Each line of a block comment starts with a # and a single space (unless it is indented text inside the comment).
Paragraphs inside a block comment are separated by a line containing a single # .

##Naming Conventions
###Descriptive: Naming Styles
There are a lot of different naming styles. It helps to be able to recognize what naming style is being used, independently from what they are used for.
The following naming styles are commonly distinguished:

* b (single lowercase letter)
* B (single uppercase letter)
* lowercase
* lower_case_with_underscores
* UPPERCASE
* UPPER_CASE_WITH_UNDERSCORES
* CapitalizedWords
* mixedCase 
* Capitalized_Words_With_Underscores 

###Prescriptive: Naming Conventions
###Names to Avoid
Never use the characters 'l' (lowercase letter el), 'O' (uppercase letter oh), or 'I' (uppercase letter eye) as single character variable names.
In some fonts, these characters are indistinguishable from the numerals one and zero. When tempted to use 'l', use 'L' instead.
###Global Variable Names
(Let's hope that these variables are meant for use inside one module only.) The conventions are about the same as those for functions.
Modules that are designed for use via from M import * should use the __all__ mechanism to prevent exporting globals, or use the older convention of prefixing such globals with an underscore (which you might want to do to indicate these globals are "module non-public").
###Function Names
Function names should be lowercase, with words separated by underscores as necessary to improve readability.
mixedCase is allowed only in contexts where that's already the prevailing style (e.g. threading.py), to retain backwards compatibility.
###Function and method arguments
Always use self for the first argument to instance methods.
Always use cls for the first argument to class methods.
If a function argument's name clashes with a reserved keyword, it is generally better to append a single trailing underscore rather than use an abbreviation or spelling corruption. Thus class_ is better than clss . (Perhaps better is to avoid such clashes by using a synonym.)
###Method Names and Instance Variables
Use the function naming rules: lowercase with words separated by underscores as necessary to improve readability.
Use one leading underscore only for non-public methods and instance variables.
To avoid name clashes with subclasses, use two leading underscores to invoke Python's name mangling rules.
Python mangles these names with the class name: if class Foo has an attribute named __a , it cannot be accessed by Foo.__a . (An insistent user could still gain access by calling Foo._Foo__a .) Generally, double leading underscores should be used only to avoid name conflicts with attributes in classes designed to be subclassed.
Note: there is some controversy about the use of __names (see below).
###Constants
Constants are usually defined on a module level and written in all capital letters with underscores separating words. Examples include MAX_OVERFLOW and TOTAL .
##Programming Recommendations
* Comparisons to singletons like None should always be done with is or is not , never the equality operators.
* Use is not operator rather than not ... is . While both expressions are functionally identical, the former is more readable and preferred.

* **Yes:**
	* if foo is not None:


* **No:**
	* if not foo is None:


* Don't write string literals that rely on significant trailing whitespace. 
