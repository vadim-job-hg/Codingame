
A contribution by Fokz
Approved by [CG]Nick , MadKnight and Stilgart
 Goal
On a Cartesian plane, given a point of coordinates (A, B) and N circles. Each circle is specified by its center coordinates (x, y) and its radius r.
Calculate how many circles contains the point (A, B).
Note: the point is counted if it is either inside or on the circle.
Input
Line 1 : A pair of integers A and B which is the coordinates of the point in question.
Line 2 : An integer N which is the number of circles.
N next lines : Three integers x, y, r where (x, y) are the coordinates of a circle center and r is the circle radius.
Output
Line 1 : A single integer which is the number of circles that contains point (A, B).
Constraints
0 ≤ N ≤ 1000
-10000 ≤ A, B, x, y ≤ 10000
0 < r ≤ 10000
Example
Input

0 0
2
0 0 1
0 0 2

Output

2

