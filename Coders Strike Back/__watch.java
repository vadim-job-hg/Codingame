import java.util.*;
import java.io.*;
import java.math.*;
import java.lang.Math;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
class Player {

    private int x;
    private int y;
    private int nextCheckpointX; // x position of the next check point
    private int nextCheckpointY; // y position of the next check point
    private int nextCheckpointDist; // distance to the next checkpoint
    private int nextCheckpointAngle; // angle between your pod orientation and the direction of the next checkpoint
    private int opponentX;
    private int opponentY;

    private int beforeX;
    private int beforeY;

    private boolean isAfterPeak = false;
    private boolean hasBoost = true;

    // 다음 동작을 위한 값
    private int destinationX;
    private int destinationY;
    private int force;
    private String thrust;

    public void move() {
        beforeX = x;
        beforeY = y;

        // Write an action using System.out.println()
        System.out.println(destinationX + " " + destinationY + " " + thrust);
    }

    public void decisionNextMove() {
        // You have to output the target position
        // // followed by the power (0 <= thrust <= 100) or "BOOST" or "SHIELD"
        // // i.e.: "x y thrust"

        // default moving value
        destinationX = nextCheckpointX;
        destinationY = nextCheckpointY;
        force = 100;

        double rad = Math.toRadians(nextCheckpointAngle);

        // normal moving
        if (nextCheckpointAngle < 90) {
            // pod이 다음 checkpoint에 가장 가까이 접근할 수 있는 최적의 thrust, 단, 관성은 고려하지 않았다.
            double perfectForce = nextCheckpointDist * Math.cos(rad) * 0.15;
            if (perfectForce > 100) {
                force = 100;
            } else if (perfectForce < 0) {
                force = 0;
            } else {
                force = (int) perfectForce;
            }
        } else {
            force = 0;
        }
        thrust = String.valueOf(force);

        // a case to boost
        if (hasBoost && nextCheckpointDist > 3000 && nextCheckpointAngle == 0) {
            thrust = "BOOST";
            hasBoost = false;
        }
    }

    public void log() {
        // To debug: System.err.println("Debug messages...");
        double moved = Math.sqrt(Math.pow(x-beforeX, 2) + Math.pow(y-beforeY, 2));
        System.err.println("Debug messages : x = " + x + ", y = " + y);
        System.err.println("Debug messages : moved = " + moved);
        System.err.println("Debug messages : Angle = " + nextCheckpointAngle);
    }

    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);

        Player p = new Player();

        // game loop
        while (true) {
            p.x = in.nextInt();
            p.y = in.nextInt();
            p.nextCheckpointX = in.nextInt(); // x position of the next check point
            p.nextCheckpointY = in.nextInt(); // y position of the next check point
            p.nextCheckpointDist = in.nextInt(); // distance to the next checkpoint
            p.nextCheckpointAngle = in.nextInt(); // angle between your pod orientation and the direction of the next checkpoint
            p.opponentX = in.nextInt();
            p.opponentY = in.nextInt();

            p.log();

            p.decisionNextMove();

            // move
            p.move();
        }
    }
}