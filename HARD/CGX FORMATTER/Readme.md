# CGX Formatter

At CodinGame we like to reinvent things. XML, JSON etc. that’s great, but for a better web, we’ve invented our own text data format (called CGX) to represent structured information.

Here is an example of data structured with CGX:​

#### Example of CGX formatted content.

![data example](img/cgx5.png 'data example')

#### Graphical representation of the example.

![formatted example](img/cgx6.png 'formatted example')
​
CGX content is composed of [element](#element)s.

### Element

An [element](#element) can be of any of the following types:
[Block](#block) 
[PRIMITIVE_TYPE](#PRIMITIVE_TYPE) or 
[KEY_VALUE](#KEY_VALUE).

### Block

* A sequence of [element](#element)s sseparated by the character ``;``
* A [Block](#block) starts with the marker ``(`` and ends with the marker ``)``.

### PRIMITIVE_TYPE

A number, a Boolean, null, or a string of characters (surrounded by the marker ``'``)

### KEY_VALUE

A string of characters separated from a [Block](#block) or a [PRIMITIVE_TYPE](#PRIMITIVE_TYPE) by the character ``=``

![data](img/cgx7.png 'data')

Your mission: write a program that formats CGX content to make it readable!

Beyond the rules below, the displayed result should not contain any space, tab, or carriage return. No other rule should be added.​

* The content of strings of characters must not be modified.
* A [Block](#block) starts on its own line.
* The markers at the start and end of a [Block](#block) are in the same column.
* Each [element](#element) contained within a [Block](#block) is indented 4 spaces from the marker of that [Block](#block).
* A [KEY_VALUE](#KEY_VALUE) starts on its own line.
* A [PRIMITIVE_TYPE](#PRIMITIVE_TYPE) starts on its own line unless it is the value of a [KEY_VALUE](#KEY_VALUE).

## Input

* **Line 1**: The number N of CGX lines to be formatted
* **The N following lines**: The CGX content. Each line contains maximum 1000 characters. All the characters are ASCII.

## Output

The formatted CGX content

## Constraints

* The CGX content supplied will always be valid.
* The strings of characters do not include the character ``'``
* 0 < N < 10000

## Examples

#### Example #1

    Input

        4
        true

    Output

        true

#### Example #2

    Input

        1
        'spaces and    tabs'

    Output

        'spaces and    tabs'

#### Example #3

    Input

        1
        (0)

    Output

        (
            0
        )

#### Example #4

    Input

        1
        ()

    Output

        (
​        )

#### Example #5

    Input

        1
        (0;1;2)

    Output

        (
            0;
            1;
            2
​        )

#### Example #6

    Input

        1
        (('k1'=1);('k2'=2))

    Output

        (
            (
                'k1'=1
            );
            (
                'k2'=2
            )
        )

#### Example #7

    Input

        10
        'users'=(('id'=10;
        'name'='Serge';
        'roles'=('visitor';
        'moderator'
        ));
        ('id'=11;
        'name'='Biales'
        );
        true
        )

    Output

        'users'=
        (
            (
                'id'=10;
                'name'='Serge';
                'roles'=
                (
                    'visitor';
                    'moderator'
                )
            );
            (
                'id'=11;
                'name'='Biales'
            );
            true
        )

#### Example #8

    Input

        9
        ( 'user'= (
            'key'='1= t(c)(';
            'valid'=false
          );
          'user'= (
            'key'=' = ; ';
            'valid'= true
          ); ()
        ​)

    Output

        (
            'user'=
            (
                'key'='1= t(c)(';
                'valid'=false
            );
            'user'=
            (
                'key'=' = ; ';
                'valid'=true
            );
            (
            ​)
        ​)

## Conditions

* Available RAM : 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment