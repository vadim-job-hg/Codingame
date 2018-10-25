# Ascii

In stations and airports you often see this type of screen. Have you ever asked yourself how it might be possible to simulate this display on a good old terminal? We have: with ASCII art!

ASCII art allows you to represent forms by using characters. To be precise, in our case, these forms are words. For example, the word "MANHATTAN" could be displayed as follows in ASCII art:

    # #  #  ### # #  #  ### ###  #  ###
    ### # # # # # # # #  #   #  # # # #
    ### ### # # ### ###  #   #  ### # #
    # # # # # # # # # #  #   #  # # # #
    # # # # # # # # # #  #   #  # # # #

​Your mission is to write a program that can display a line of text in ASCII art.

## Input

* **Line 1**: the width L of a letter represented in ASCII art. All letters are the same width.
* **Line 2**: the height H of a letter represented in ASCII art. All letters are the same height.
* **Line 3**: The line of text T, composed of N ASCII characters.
* **Following Lines**: the string of characters ABCDEFGHIJKLMNOPQRSTUVWXYZ? Represented in ASCII art.

## Output

* The text T in ASCII art.
* The characters a to z are shown in ASCII art by their equivalent in upper case.
* The characters which are not in the intervals [a-z] or [A-Z] will be shown as a question mark in ASCII art.

## Constraints

* 0 < L < 30
* 0 < H < 30
* 0 < N < 200

## Examples

### Example 1

    Input

        4
        5
        E
         #  ##   ## ##  ### ###  ## # # ###  ## # # #   # # ###  #  ##   #  ##   ## ### # # # # # # # # # # ### ###  
        # # # # #   # # #   #   #   # #  #    # # # #   ### # # # # # # # # # # #    #  # # # # # # # # # #   #   #  
        ### ##  #   # # ##  ##  # # ###  #    # ##  #   ### # # # # ##  # # ##   #   #  # # # # ###  #   #   #   ##  
        # # # # #   # # #   #   # # # #  #  # # # # #   # # # # # # #    ## # #   #  #  # # # # ### # #  #  #        
        # # ##   ## ##  ### #    ## # # ###  #  # # ### # # # #  #  #     # # # ##   #  ###  #  # # # #  #  ###  # 

    Output

        ### 
        #   
        ##  
        #   
        ### 

### Example 2

    Input

        4
        5
        MANHATTAN
         #  ##   ## ##  ### ###  ## # # ###  ## # # #   # # ###  #  ##   #  ##   ## ### # # # # # # # # # # ### ###  
        # # # # #   # # #   #   #   # #  #    # # # #   ### # # # # # # # # # # #    #  # # # # # # # # # #   #   #  
        ### ##  #   # # ##  ##  # # ###  #    # ##  #   ### # # # # ##  # # ##   #   #  # # # # ###  #   #   #   ##  
        # # # # #   # # #   #   # # # #  #  # # # # #   # # # # # # #    ## # #   #  #  # # # # ### # #  #  #        
        # # ##   ## ##  ### #    ## # # ###  #  # # ### # # # #  #  #     # # # ##   #  ###  #  # # # #  #  ###  # 

    Output

        # #  #  ### # #  #  ### ###  #  ###  
        ### # # # # # # # #  #   #  # # # #  
        ### ### # # ### ###  #   #  ### # #  
        # # # # # # # # # #  #   #  # # # #  
        # # # # # # # # # #  #   #  # # # # 

## Conditions

* Available RAM: 512MB
* Timeout: 1 seconds
* The program has to read inputs from standard input
* The program has to write the solution to standard output
* The program must run in the test environment