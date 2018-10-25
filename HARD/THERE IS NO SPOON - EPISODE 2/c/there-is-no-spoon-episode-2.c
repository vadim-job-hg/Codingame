#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/**
 * The machines are gaining ground. Time to show them what we're really made of...
 **/

typedef struct link
{
 int X, Y, X1, Y1, How, IsGuess;
} LINK;

typedef enum direction
{
 UP, DOWN, RIGHT, LEFT
} DIRECTION;

int width; // the number of cells on the X axis
int height; // the number of cells on the Y axis
char** cell;
int** horLink;
int** verLink;
LINK* doneLink;
int dCnt = 0;
int curNodeX = 0;
int curNodeY = 0;
int justRollback = 0;
int** groupNbr;

int nextNode(int * fromX, int * fromY)
{
 int x = *fromX;
 for (int y = *fromY; y < height; y++)
 {
  for ( ;x < width; x++) if ((cell[y][x] > '0') && (cell[y][x] <= '8')) { *fromX = x; *fromY = y; return 1;}
  x = 0;
 }
 return 0;
}

int findNeighbor(int x, int y, DIRECTION dir, int * x1, int * y1)
{
 int incX, incY;
 if      (dir == UP)    {incX =  0; incY = -1;}
 else if (dir == DOWN)  {incX =  0; incY =  1;}
 else if (dir == RIGHT) {incX =  1; incY =  0;}
 else if (dir == LEFT)  {incX = -1; incY =  0;}
 int result = 0;
 int xi = x + incX;
 int yi = y + incY;
 while (!result && (xi >= 0) && (xi < width) && (yi >= 0) && (yi < height))
 {
  if ((cell[yi][xi] >= '0') && (cell[yi][xi] <= '8'))
  {
   result = 1;
   *x1 = xi;
   *y1 = yi;
  }
  xi += incX;
  yi += incY;
 }
 return result;
}

int canLink(int x, int y, int x1, int y1)
{
 int result = 1;
 if ((cell[y][x] == '0') || (cell[y1][x1] == '0'))
  result = 0;
 else if (y == y1)
 {
  int xmin = x > x1 ? x1 : x;
  int xmax = x > x1 ? x : x1;
  int x2, y2;
  if (horLink[y][xmin] < 2)
  {
   int count = 0;
   for (xmin++; xmin < xmax; xmin++)
    if (findNeighbor(xmin, y, UP, &x2, &y2)) count += verLink[y2][x2];
   result = (count == 0);
  }
 }
 else if (x == x1)
 {
  int ymin = y > y1 ? y1 : y;
  int ymax = y > y1 ? y : y1;
  int x2, y2;
  if (verLink[ymin][x] < 2)
  {
   int count = 0;
   for (ymin++; ymin < ymax; ymin++)
    if (findNeighbor(x, ymin, LEFT, &x2, &y2)) count += horLink[y2][x2];
   result = (count == 0);
  }
 }
 return result;
}

int maxGroup()
{
 int result = 0;
 for (int i = 0; i < height; i++)
  for (int j = 0; j < width; j++)
   if (result < groupNbr[i][j]) result = groupNbr[i][j];
 return result;
}

int isAllNodesConnected()
{
 for (int i = 0; i < height; i++)
  for (int j = 0; j < width; j++)
   groupNbr[i][j] = 0;
 for (int i = 0; i < dCnt; i++)
 {
  int x = doneLink[i].X;
  int y = doneLink[i].Y;
  int x1 = doneLink[i].X1;
  int y1 = doneLink[i].Y1;
  if (groupNbr[y][x] == 0)
  {
   if (groupNbr[y1][x1] == 0)
   {
    groupNbr[y][x] = maxGroup() + 1;
    groupNbr[y1][x1] = groupNbr[y][x];
   }
   else
    groupNbr[y][x] = groupNbr[y1][x1];
  }
  else if (groupNbr[y1][x1] == 0)
   groupNbr[y1][x1] = groupNbr[y][x];
  else
  {
   int maxGr = groupNbr[y][x];
   int minGr = groupNbr[y1][x1];
   if (groupNbr[y1][x1] > groupNbr[y][x])
   {
    maxGr = groupNbr[y1][x1];
    minGr = groupNbr[y][x];
   }
   for (int i = 0; i < height; i++)
    for (int j = 0; j < width; j++)
     if (groupNbr[i][j] == maxGr) groupNbr[i][j] = minGr;
  }
 }
 return (maxGroup() == 1);
}

void addLink(int x, int y, int x1, int y1, int how, int isGuess)
{
 justRollback = 0;
 doneLink[dCnt].X = x;
 doneLink[dCnt].Y = y;
 doneLink[dCnt].X1 = x1;
 doneLink[dCnt].Y1 = y1;
 doneLink[dCnt].How = how;
 doneLink[dCnt].IsGuess = isGuess;
 dCnt++;
}

void countLink(int x, int y, int x1, int y1, int how)
{
 cell[y][x] -= how;
 cell[y1][x1] -= how;
 if (y == y1) horLink[y][x] += how;
 if (x == x1) verLink[y][x] += how;
}

void makeLink(int x, int y, int x1, int y1, int how, int isGuess)
{
 if ((x <= x1) && (y <= y1))
 {
  countLink(x, y, x1, y1, how);
  addLink(x, y, x1, y1, how, isGuess);
 }
 else
 {
  countLink(x1, y1, x, y, how);
  addLink(x1, y1, x, y, how, isGuess);
 }
}

void rollback()
{
 do
 {
  dCnt--;
  countLink(doneLink[dCnt].X, doneLink[dCnt].Y, doneLink[dCnt].X1, doneLink[dCnt].Y1, -doneLink[dCnt].How);
 } while (!doneLink[dCnt].IsGuess);
 curNodeX = doneLink[dCnt].X;
 curNodeY = doneLink[dCnt].Y;
 justRollback = 1;
}

int GuessOneLink()
{
 int x1;
 int y1;
 if (justRollback && (doneLink[dCnt].Y1 > doneLink[dCnt].Y))
  //Mы только что откатили связь "вниз", то есть перебрали все варианты и ничего не нашли.
  //Значит, неверно угадана более ранняя связь.
  return 0;
 else if (!justRollback && findNeighbor(curNodeX, curNodeY, RIGHT, &x1, &y1) && canLink(curNodeX, curNodeY, x1, y1))
  //Если только что откатили связь, то вправо гадать уже нельзя.
 {
  makeLink(curNodeX, curNodeY, x1, y1, 1, 1);
  return 1;
 }
 else if (findNeighbor(curNodeX, curNodeY, DOWN, &x1, &y1) && canLink(curNodeX, curNodeY, x1, y1))
 {
  makeLink(curNodeX, curNodeY, x1, y1, 1, 1);
  return 1;
 }
 else
  return 0;
}

void _intialPhaseAdd(int x, int y, int x1, int y1)
{
 int already = 0;
 for (int i = 0; !already && (i < dCnt); i++)
  already = ((x == doneLink[i].X) && (x1 == doneLink[i].X1) && (y == doneLink[i].Y) && (y1 == doneLink[i].Y1));
 if (!already) addLink(x, y, x1, y1, 1, 0);
}

void intialPhaseAdd(int x, int y, int x1, int y1)
{
 if ((x <= x1) && (y <= y1))
  _intialPhaseAdd(x, y, x1, y1);
 else
  _intialPhaseAdd(x1, y1, x, y);
}

void intialPhase()
{
//Пара простых правил, вытекающих из требования связности.
 int nodes, nodes1or2, nodes2orMore;
 int x1;
 int y1;
 int onlyX;
 int onlyY;
 for (int y = 0; y < height; y++)
  for (int x = 0; x < width; x++)
   if ((cell[y][x] > '0') && (cell[y][x] <= '8'))
   {
    nodes2orMore = 0;
    nodes = 0;
    nodes1or2 = 0;
    for (DIRECTION dir = UP; dir <= LEFT; dir=(DIRECTION)((int)dir + 1))
    {
     if (findNeighbor(x, y, dir, &x1, &y1))
     {
      if (cell[y1][x1] > '1')
      {
       nodes2orMore++;
       onlyX = x1;
       onlyY = y1;
      }
      nodes++;
      nodes1or2 += (cell[y1][x1] <= '2');
     }
    }

    if (nodes2orMore == 1)
    // Если только один сосед больше чем "1", то с ним есть связь.
    {
     if ((onlyX >= x) && (onlyY >= y))
      intialPhaseAdd(x, y, onlyX, onlyY);
     else
      intialPhaseAdd(onlyX, onlyY, x, y);
    }
    if ((cell[y][x] == '2') && (nodes == 2) && (nodes1or2 == 2))
    // Если у "2" ровно два соседа и оба "1" или "2", то связи есть с обоими.
     for (DIRECTION dir = UP; dir <= LEFT; dir=(DIRECTION)((int)dir + 1))
      if (findNeighbor(x, y, dir, &x1, &y1)) intialPhaseAdd(x, y, x1, y1);
   }
 for (int i = 0; i < dCnt; i++)
  countLink(doneLink[i].X, doneLink[i].Y, doneLink[i].X1, doneLink[i].Y1, doneLink[i].How);
}

void DoAllExplicit()
{
 int count;
 do
 {
  count = 0;
  for (int y = 0; y < height; y++)
  {
   for (int x = 0; x < width; x++)
   {
    int needs = cell[y][x] - '0';
    if ((needs > 0) && (needs <= 8))
    {
     int x1;
     int y1;
     int nodes = 0;
     int maxLinks[4] = {0, 0, 0, 0};
     int totalLinks = 0;
     for (DIRECTION dir = UP; dir <= LEFT; dir=(DIRECTION)((int)dir + 1))
     {
      if (findNeighbor(x, y, dir, &x1, &y1)) if (canLink(x, y, x1, y1))
      {
       nodes++;
       int max1 = 2;
       if (y == y1)
        max1 -= (x < x1) ? horLink[y][x] : horLink[y][x1];
       else
        max1 -= (y < y1) ? verLink[y][x] : verLink[y1][x];
       int max2 = (cell[y1][x1] > '1') ? 2 : 1;
       maxLinks[dir] = (max1 < max2) ? max1 : max2;
       totalLinks += maxLinks[dir];
      }
     }

     if (needs > totalLinks)
     {
      rollback();
      x = width;
      y = height;
     }
     else if (needs == totalLinks)
     //Все возможные связи нужны
     {
      for (DIRECTION dir = UP; dir <= LEFT; dir=(DIRECTION)((int)dir + 1))
       if (maxLinks[dir] && findNeighbor(x, y, dir, &x1, &y1)) makeLink(x, y, x1, y1, maxLinks[dir], 0);
      count++;
      curNodeX = 0;
      curNodeY = 0;
     }
     else if (needs == totalLinks - 1)
     {
      //Из возможных связей только одна лишняя. Значит, там где возможны две, точно есть хоть одна.
      for (DIRECTION dir = UP; dir <= LEFT; dir=(DIRECTION)((int)dir + 1))
      if ((maxLinks[dir] == 2) && findNeighbor(x, y, dir, &x1, &y1))
      {
       makeLink(x, y, x1, y1, 1, 0);
       count++;
       curNodeX = 0;
       curNodeY = 0;
      }
     }
    }
   }
  }
 } while (count > 0);
}

int main()
{
 scanf("%d", &width);
 scanf("%d", &height);
 fgetc(stdin);

 horLink = (int**) malloc(height * sizeof(int*));
 verLink = (int**) malloc(height * sizeof(int*));
 groupNbr = (int**) malloc(height * sizeof(int*));
 cell = (char**) malloc(height * sizeof(char*));
 for (int i = 0; i < height; i++)
 {
  horLink[i] = (int*)  malloc(width * sizeof(int));
  verLink[i] = (int*)  malloc(width * sizeof(int));
  groupNbr[i] = (int*) malloc(width * sizeof(int));
  cell[i] = (char*) malloc((width+1) * sizeof(char));
  for (int j = 0; j < width; j++)
  {
   cell[i][j] = fgetc(stdin);
   verLink[i][j] = 0;
   horLink[i][j] = 0;
  }
  fgetc(stdin);
  cell[i][width] = 0;
 }
 doneLink = (LINK*) malloc((width*height*4) * sizeof(LINK));

 dCnt = 0;
 curNodeX = 0;
 curNodeY = 0;
 justRollback = 0;

 intialPhase();

 do
 {
  DoAllExplicit();

  if (nextNode(&curNodeX, &curNodeY))
  {
   if (!GuessOneLink()) rollback();
  }
  else if (isAllNodesConnected())
   //Все раздали, граф связен. Ура.
   break;
  else
   rollback(); //Все раздали, граф несвязен.
 } while (1);

 for (int i = 0; i < dCnt; i++)
  printf("%d %d %d %d %d\n", doneLink[i].X, doneLink[i].Y, doneLink[i].X1, doneLink[i].Y1, doneLink[i].How);
 return 0;
}