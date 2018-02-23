
A contribution by CyberLemonade
Approved by Stilgart , dwarfie and nicola
 Goal
String Transformation:

Transform a string according to the following criteria:
1. The final string has the same length as the original string
2. The character at index i of the encoded string is the character at index j of the original string, such that j is at a distance n from i, where n is the ith term of the series 1,3,6,10,15,21...

--------------------------------------------------- xxx ---------------------------------------------------

Explanation:

Let L be the length of the string.
Let i be the current index.
Let n be the ith term of the given series
So, index of the character at index i of the final string will be:
index j = (i+n) MOD l

--------------------------------------------------- xxx ---------------------------------------------------

Example:

consider the string FINE

It has characters at index:
0 = F
1 = I
2 = N
3 = E

In the final String:
character at index 0 is at distance 1 from F = I (j = 1 MOD 4 = 1)
character at index 1 is at distance 3 from I = F (j = 4 MOD 4 = 0)
character at index 2 is at distance 6 from N = F (j = 8 MOD 4 = 0)
character at index 3 is at distance 10 from E = I (j = 13 MOD 4 = 1)
So the final string is IFFI

--------------------------------------------------- xxx ---------------------------------------------------
Input
Line 1: A String STRING
Output
Line 1: The final String FINAL
Constraints
No constraints
Example
Input

FINE

Output

IFFI

