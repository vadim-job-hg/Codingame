import java.util.*;
import java.io.*;
import java.math.*;

/**
 *
 * @author wael
 */

/**
 * Block class
 * Rotation 0:   A B
 *
 *               B
 * Rotation 1:   A
 *
 * Rotation 2: B A
 *
 * Rotation 3:   A
 *               B
 */
class Block {

    public int colorA;
    public int colorB;
    private int rotation;

    public Block(int a, int b) {
        colorA = a;
        colorB = b;
        rotation = 0;
    }

    public boolean sameColor(){
        return colorA == colorB;
    }

    public int getRotation() {
        return rotation;
    }

    public void setRotation(int rot){
        rotation = rot;
    }

    public Block[] getVariations(){
        Block[] variations;
        if(colorA == colorB)
            variations = new Block[2];
        else
            variations = new Block[4];
        for(int i=0; i<variations.length; i++){
            variations[i] = new Block(colorA, colorB);
            variations[i].setRotation(i);
        }
        return variations;
    }
}

class GameState{
    public static int ID_TRACKER;

    private int id;
    private GameState[] childStates;
    private GameState parent;
    private GameState bestChild;
    private int evaluation;
    private boolean expanded;

    private Block[] nextBlocks;
    private int nextBlocksInd;
    private int[][] myGrid;
    private int myScore;
    private int myNuisancePoints;
    private int[][] enemyGrid;
    private int enemyScore;
    private int enemyNuisancePoints;
    private boolean myTurn;

    // GETTERS SETTERS CONSTRUCTORS

    public GameState(){
        nextBlocks = new Block[8];
        myGrid = new int[6][12];
        myScore = 0;
        enemyGrid = new int[6][12];
        enemyScore = 0;
        myTurn = true;
        id = ID_TRACKER;
        ID_TRACKER++;
        evaluation = 0;
        expanded = false;
    }

    public int getId() {
        return id;
    }

    // METHODS RELATED TO MIN MAX SEARCH

    public void expand(){
        if(nextBlocks[nextBlocksInd] != null && getEvaluation()!= Integer.MAX_VALUE && getEvaluation()!= Integer.MIN_VALUE){

        }
        Block[] variations = nextBlocks[nextBlocksInd].getVariations();
        childStates = new GameState[(variations.length/2)*11];
        for(Block b : variations){

        }
    }

    public int getEvaluation(){
        if(!expanded){
            if(myScore == Integer.MIN_VALUE)
                evaluation = myScore;
            else if(enemyScore == Integer.MIN_VALUE)
                evaluation = Integer.MAX_VALUE;
            else
                evaluation = myScore-enemyScore;
        }
        return evaluation;
    }

    private void cascadeScoreUp(){
        if(parent.bestChild == null){
            //Cascade Score up
            if( (parent.myTurn && parent.getEvaluation() < getEvaluation()) || (!parent.myTurn && parent.getEvaluation() > getEvaluation())){
                parent.bestChild = this;
                parent.evaluation = getEvaluation();
            }
            //Cull
            else{
                parent.childStates[ parent.childStates[0].id - id ] = null;
            }
        }
    }

    // METHODS RELATED TO ACTUAL GAME SIMULATION

    public void dropBlockAt(Block block, int x) {
        int[][] grid = myTurn ? myGrid : enemyGrid;
        //There's space to drop this block here
        if (block.getRotation() % 2 == 1 && grid[x][0] == -1 && grid[x][1] == -1) {
            grid[x][0] = (block.getRotation() == 1) ? block.colorB : block.colorA;
            grid[x][1] = (block.getRotation() == 1) ? block.colorA : block.colorB;
        }
        if (block.getRotation() % 2 == 0 && x < 5 && grid[0][x] == -1 && grid[0][x + 1] == -1) {
            grid[x][0] = (block.getRotation() == 0) ? block.colorA : block.colorB;
            grid[x+1][0] = (block.getRotation() == 0) ? block.colorB : block.colorA;
        }else{
            if(myTurn)
                myScore = Integer.MIN_VALUE;
            else
                enemyScore = Integer.MIN_VALUE;
        }
        clearGroups();
    }

    private void dropColumn(int x) {
        int emptySpaces = 0;
        int[][] grid = myTurn ? myGrid : enemyGrid;
        for (int y = 11; y >= 0; y--) {
            if (grid[x][y] == -1) {
                emptySpaces++;
            } else if (emptySpaces != 0) {
                grid[x][y+emptySpaces] = grid[x][y];
                grid[x][y] = -1;
            }
        }
    }

    private void dropBalls(){
        for( int i = 0; i<6; i++)
            dropColumn(i);
    }

    private int getAdjacents(int x, int y) {
        if (y < 0 || y > 11 || x < 0 || x > 5) {
            return 0;
        }
        int[][] grid = myTurn ? myGrid : enemyGrid;
        if (grid[x][y] == -1 || grid[x][y] == 0)
            return 0;
        int originalColor = grid[x][y];
        int res = 1;
        grid[x][y] = -2;
        if (x > 0 && (grid[x-1][y] == originalColor))
            res += getAdjacents(x-1, y);
        if (x < 5 && (grid[x+1][y] == originalColor))
            res += getAdjacents(x+1, y);
        if (y > 0 && (grid[x][y-1] == originalColor))
            res += getAdjacents(x, y-1);
        if (y < 11 && (grid[x][y+1] == originalColor))
            res += getAdjacents(x, y+1);
        grid[x][y] = originalColor;
        return res;
    }

    public void clearAdjacents(int x, int y) {
        if (x < 0 || x > 5 || y < 0 || y > 11) {
            return;
        }
        int[][] grid = myTurn ? myGrid : enemyGrid;
        if (grid[x][y] == -1)
            return;
        int originalColor = grid[x][y];
        grid[x][y] = -1;
        if (originalColor == 0)
            return;
        if (x > 0 && (grid[x - 1][y] == originalColor || grid[x - 1][y] == 0))
            clearAdjacents(x - 1, y);
        if (x < 5 && (grid[x + 1][y] == originalColor || grid[x + 1][y] == 0))
            clearAdjacents(x + 1, y);
        if (y > 0 && (grid[x][y - 1] == originalColor || grid[x][y - 1] == 0))
            clearAdjacents(x, y - 1);
        if (y < 11 && (grid[x][y + 1] == originalColor || grid[x][y + 1] == 0))
            clearAdjacents(x, y + 1);
    }

    private void clearGroups() {
        int[][] grid = myTurn ? myGrid : enemyGrid;
        boolean cleared = true;
        int B = 0;
        int CP = 0;
        int CB = 0;
        int GB = 0;
        boolean[] colorArray = new boolean[5];
        while (cleared) {
            cleared = false;
            for (int y = 0; y < 12; y++) {
                for (int x = 0; x < 6; x++) {
                    int destroyed = getAdjacents(y, x);
                    if (destroyed > 4) {
                        int color = grid[x][y];
                        B += destroyed;
                        CP = CP == 0 ? 8 : CP*2;
                        if(!colorArray[color-1]){
                            colorArray[color-1] = true;
                            CB = CB == 0 ? 2 : CB*2;
                        }
                        GB += (destroyed >= 11) ? 8 : destroyed - 4;
                        clearAdjacents(x, y);
                        cleared = true;
                        break;
                    }
                }
                if (cleared) {
                    dropBalls();
                    break;
                }
            }
        }
        int multiplier = CP + CB + GB;
        multiplier = multiplier < 1 ? 1 : multiplier > 999 ? 999 : multiplier;
        if(myTurn){
            myScore += 10 * B * multiplier;
            myNuisancePoints += (B * multiplier)/7;
            if(myNuisancePoints >= 6)
                dropNuisanceBlocks();
        }else{
            enemyScore += 10 * B * multiplier;
            enemyNuisancePoints += (B * multiplier)/7;
            if(enemyNuisancePoints >= 6)
                dropNuisanceBlocks();
        }
    }

    private void dropNuisanceBlocks(){
        int[][] grid = myTurn ? enemyGrid : myGrid;
        int nuisanceLines;
        if(myTurn){
            nuisanceLines = myNuisancePoints / 6;
            myNuisancePoints = myNuisancePoints % 6;
        }else{
            nuisanceLines = enemyNuisancePoints / 6;
            myNuisancePoints = enemyNuisancePoints % 6;
        }
        for(int x = 0; x<6; x++){
            for(int y = 0; y<nuisanceLines; y++){
                if(grid[x][y] == -1){
                    grid[x][y] = 0;
                }else{
                    if(myTurn)
                        enemyScore = Integer.MIN_VALUE;
                    else
                        myScore = Integer.MIN_VALUE;
                    return;
                }
            }
        }
        dropBalls();
    }

    // OTHER METHODS

    @Override
    public boolean equals(Object o){
        if(o instanceof GameState){
            return id == ((GameState)o).getId();
        }
        return false;
    }

    @Override
    public int hashCode() {
        int hash = 5;
        hash = 29 * hash + this.id;
        return hash;
    }
}

class Brain {

    public static int culls;
    public static int positionsEvaluated;
    public static int stopDepth;
    public static long startTime;
    public static boolean first;
    private List<Block> nextBlocks;
    private int[][] myGrid;
    private List<int[][]> gridHistory;
    private int myLine;
    private int[][] hisGrid;
    private int hisLine;
    private int myScore;
    private int hisScore;
    private int emptyGrids;
    private int bestScore;
    private List<int[]> moves;

    public Brain() {
        nextBlocks = new ArrayList<Block>();
        myGrid = new int[12][6];
        gridHistory = new ArrayList<int[][]>();
        hisGrid = new int[12][6];
        moves = new ArrayList<int[]>();
    }

    public void addBlock(int a, int b) {
        nextBlocks.add(new Block(a, b));
        if (nextBlocks.size() > 8) {
            nextBlocks.remove(8);
        }
    }

    public void addBlock(Block b) {
        nextBlocks.add(b);
        if (nextBlocks.size() > 8) {
            nextBlocks.remove(8);
        }
    }

    public void setMyScore(int score) {
        myScore = score;
    }

    public void setHisScore(int score) {
        hisScore = score;
    }

    public void resetGrids() {
        myLine = 0;
        hisLine = 0;
    }

    public void insertMyLine(String row) {
        if (myLine == 0) {
            emptyGrids = 0;
        }
        for (int i = 0; i < 6; i++) {
            int newValue = (row.charAt(i) == '.') ? -1 : row.charAt(i) - '0';
            if (newValue != myGrid[myLine][i] && moves.size() > 0) {
                bestScore = 0;
                moves.clear();
            }
            myGrid[myLine][i] = newValue;
        }
        myLine = (myLine + 1) % 12;
    }

    public void insertHisLine(String row) {
        for (int i = 0; i < 6; i++) {
            switch (row.charAt(i)) {
                case '.':
                    hisGrid[hisLine][i] = -1;
                    break;
                default:
                    hisGrid[hisLine][i] = row.charAt(i) - '0';
                    break;
            }
        }
        hisLine = (hisLine + 1) % 12;
    }

    public int[] getBest(int depth, int score) {
        if (depth == 8 || System.currentTimeMillis() > startTime + 90) {
            stopDepth = depth;
            return new int[]{0, 0, 0};
        }
        boolean found = false;
        int firstCol = 0;
        int firstRot = 0;
        if (moves.size() > depth) {
            firstCol = moves.get(0)[0];
            firstRot = moves.get(0)[1];
        }
        for (int col = firstCol; col < 6; col++) {
            if (col != firstCol) {
                firstRot = 0;
            }
            int rotationsToTest = (nextBlocks.get(depth).sameColor()) ? 2 : 4;
            for (int rot = firstRot; rot < rotationsToTest; rot++) {
                nextBlocks.get(depth).setRotation(rot);
                if (dropBlockAt(col, depth)) {
                    positionsEvaluated++;
                    score += clearGroups();
                    if (score > bestScore) {
                        found = true;
                    } else {
                        score = getBest(depth + 1, score)[2];
                    }
                    if (score > bestScore) {
                        bestScore = score;
                    }
                    myGrid = gridHistory.remove(gridHistory.size() - 1);
                    if (found) {
                        if (depth == 0) {
                            System.err.println("Found score :" + score + " col: " + col + " rot: " + rot);
                        }
                        moves.add(new int[]{((rot == 2) ? col + 1 : col), rot});
                        bestScore = score;
                        break;
                    }
                }
            }
            nextBlocks.get(depth).setRotation(0);
            if (found) {
                break;
            }
        }
        if (moves.size() > 0) {
            return new int[]{moves.get(0)[0], moves.get(0)[1], bestScore};
        }

        return new int[]{-1, -1, 0};
    }

    public boolean dropBlockAt(int col, int depth) {
        Block block = nextBlocks.get(depth);
        //Block is upright
        if (block.getRotation() % 2 == 1) {
            if (myGrid[0][col] == -1 && myGrid[1][col] == -1) {
                int[][] oldGrid = new int[12][6];
                for (int i = 0; i < 12; i++) {
                    System.arraycopy(myGrid[i], 0, oldGrid[i], 0, myGrid[i].length);
                }
                gridHistory.add(oldGrid);
                myGrid[0][col] = (block.getRotation() == 1) ? block.colorB : block.colorA;
                myGrid[0 + 1][col] = (block.getRotation() == 1) ? block.colorA : block.colorB;
                dropColumn(col);
                return true;
            }
        } else if (col < 5 && myGrid[0][col] == -1 && myGrid[0][col + 1] == -1) {
            int[][] oldGrid = new int[12][6];
            for (int i = 0; i < 12; i++) {
                System.arraycopy(myGrid[i], 0, oldGrid[i], 0, myGrid[i].length);
            }
            gridHistory.add(oldGrid);
            myGrid[0][col] = (block.getRotation() == 0) ? block.colorA : block.colorB;
            myGrid[0][col + 1] = (block.getRotation() == 0) ? block.colorB : block.colorA;
            dropColumn(col);
            dropColumn(col + 1);
            return true;
        }
        return false;
    }

    private void dropColumn(int col) {
        int emptySpaces = 0;
        for (int y = 11; y >= 0; y--) {
            if (myGrid[y][col] == -1) {
                emptySpaces++;
            } else if (emptySpaces != 0) {
                myGrid[y + emptySpaces][col] = myGrid[y][col];
                myGrid[y][col] = -1;
            }
        }
    }

    public int clearGroups() {
        boolean cleared = true;
        int balls = 0;
        int CP = 0;
        int GB = 0;
        int CB = 0;
        int[] colorArray = new int[5];
        while (cleared) {
            cleared = false;
            for (int y = 0; y < 12; y++) {
                for (int x = 0; x < 6; x++) {
                    int destroyed = getAdjacents(y, x);
                    if (destroyed > 4) {
                        int color = myGrid[y][x];
                        if (color >= 1 && color <= 5 && colorArray[color - 1] == 0) {
                            CB++;
                        }
                        colorArray[color - 1]++;
                        GB += (destroyed >= 11) ? 8 : destroyed - 4;
                        CP++;
                        balls += destroyed;
                        clearAdjacents(y, x);
                        cleared = true;
                        break;
                    }
                }
                if (cleared) {
                    dropBalls();
                    break;
                }
            }
        }
        int multiplier = ((CP > 1) ? 8 * (int) Math.pow(2, CP - 1) : 0) + GB + ((CB > 1) ? (int) Math.pow(2, CB - 1) : 0);
        multiplier = (multiplier < 1) ? 1 : multiplier;
        multiplier = (multiplier > 999) ? 999 : multiplier;
        return 10 * balls * multiplier;
    }

    public void dropBalls() {
        for (int x = 0; x < 6; x++) {
            dropColumn(x);
        }
    }

    public void clearAdjacents(int y, int x) {
        if (y < 0 || y > 11 || x < 0 || x > 5) {
            return;
        }
        if (myGrid[y][x] == -1) {
            return;
        }
        int originalColor = myGrid[y][x];
        myGrid[y][x] = -1;
        if (originalColor == 0) {
            return;
        }
        if (y > 0 && (myGrid[y - 1][x] == originalColor || myGrid[y - 1][x] == 0)) {
            clearAdjacents(y - 1, x);
        }
        if (y < 11 && (myGrid[y + 1][x] == originalColor || myGrid[y + 1][x] == 0)) {
            clearAdjacents(y + 1, x);
        }
        if (x > 0 && (myGrid[y][x - 1] == originalColor || myGrid[y][x - 1] == 0)) {
            clearAdjacents(y, x - 1);
        }
        if (x < 5 && (myGrid[y][x + 1] == originalColor || myGrid[y][x + 1] == 0)) {
            clearAdjacents(y, x + 1);
        }
    }

    public int getAdjacents(int y, int x) {
        if (y < 0 || y > 11 || x < 0 || x > 5) {
            return 0;
        }
        if (myGrid[y][x] == -1 || myGrid[y][x] == 0) {
            return 0;
        }
        int originalColor = myGrid[y][x];
        int res = 1;
        myGrid[y][x] = -2;
        if (y > 0 && (myGrid[y - 1][x] == originalColor)) {
            res += getAdjacents(y - 1, x);
        }
        if (y < 11 && (myGrid[y + 1][x] == originalColor)) {
            res += getAdjacents(y + 1, x);
        }
        if (x > 0 && (myGrid[y][x - 1] == originalColor)) {
            res += getAdjacents(y, x - 1);
        }
        if (x < 5 && (myGrid[y][x + 1] == originalColor)) {
            res += getAdjacents(y, x + 1);
        }
        myGrid[y][x] = originalColor;
        return res;
    }

    public String getGrid() {
        String ret = "";
        for (int y = 0; y < 12; y++) {
            for (int x = 0; x < 6; x++) {
                if (myGrid[y][x] == -1) {
                    ret += " ";
                } else if (myGrid[y][x] == 0) {
                    ret += "X";
                } else {
                    ret += myGrid[y][x];
                }
            }
            ret += "\n";
        }
        return ret;
    }

    public void setGrid(int[][] grid) {
        myGrid = grid;
    }
}

class Player {

    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);
        int column = 0;
        Brain brain = new Brain();
        // game loop
        while (true) {
            Brain.startTime = System.currentTimeMillis();
            for (int i = 0; i < 8; i++) {
                int colorA = in.nextInt(); // color of the first block
                int colorB = in.nextInt(); // color of the attached block
                brain.addBlock(colorA, colorB);
            }
            int score1 = in.nextInt();
            brain.setMyScore(score1);
            for (int i = 0; i < 12; i++) {
                String row = in.next();
                brain.insertMyLine(row);
            }
            int score2 = in.nextInt();
            brain.setHisScore(score2);
            for (int i = 0; i < 12; i++) {
                String row = in.next(); // One line of the map ('.' = empty, '0' = skull block, '1' to '5' = colored block)
                brain.insertHisLine(row);
            }

            // Write an action using System.out.println()
            // To debug: System.err.println("Debug messages...");
            Brain.positionsEvaluated = 0;
            int[] res = brain.getBest(0, 0);
            System.out.println(res[0] + " " + res[1] + " Evaluated: " + Brain.positionsEvaluated); // "x": the column in which to drop your blocks
        }
    }
}