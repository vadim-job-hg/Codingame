// https://github.com/nico91470/CodeOfKutulu/blob/master/Program.cs

using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;
using System.Windows;

public enum State
{
    SPAWNING = 0,
    WANDERING = 1,
    STALKING = 2,
    RUSHING = 3,
    STUNNED = 4
}

#region Entité
public class Player
{
    public int ID { get; set; }
    public Point Position { get; set; }
    public int health { get; set; }
    public int state { get; set; }
    public int param3 { get; set; }
}

public class Explorateur : Player
{
    internal bool IsVisibleBy(Player slasher, char[,] map)
    {
        if (this.Position.y == slasher.Position.y)
        {
            for (int i = (int)(this.Position.x < slasher.Position.x ? this.Position.x : slasher.Position.x); i < (int)(this.Position.x > slasher.Position.x ? this.Position.x : slasher.Position.x); i++)
            {
                if (map[i, (int)this.Position.y] != '.')
                    return false;
            }
            return true;
        }
        else if (this.Position.x == slasher.Position.x)
        {
            for (int i = (int)(this.Position.y < slasher.Position.y ? this.Position.y : slasher.Position.y); i < (int)(this.Position.y > slasher.Position.y ? this.Position.y : slasher.Position.y); i++)
            {
                if (map[(int)this.Position.x, i] != '.')
                    return false;
            }
            return true;
        }
        return false;
    }
}
public class Wanderer : Player { }
public class Slasher : Player { }
public class Shelter : Player { }

#endregion

public class Point
{
    public float x { get; set; }
    public float y { get; set; }

    public float DistanceTo(Point p)
    {
        return (float)(Math.Sqrt((this.x - p.x) * (this.x - p.x) + (this.y - p.y) * (this.y - p.y)));
    }
}

public class Game
{
    public int width { get; set; }
    public int height { get; set; }
    public char[,] Map { get; set; }
    public int sanityLossLonely { get; set; }
    public int sanityLossGroup { get; set; }
    public int wandererSpawnTime { get; set; }
    public int wandererLifeTime { get; set; }
    public List<Explorateur> Explorateurs { get; set; }
    public List<Wanderer> Wanderers { get; set; }
    public List<Slasher> Slashers { get; set; }
    public List<Shelter> Shelters { get; set; }
}

public class Kutulu
{

    static Game game;
    static void Main(string[] args)
    {
        game = new Game();
        game.Explorateurs = new List<Explorateur>();
        game.Wanderers = new List<Wanderer>();
        game.Slashers = new List<Slasher>();
        game.Shelters = new List<Shelter>();
        GameInit();
        while (true)
        {
            TurnInit();
            GameLoop();
            TurnClear();
        }
    }

    #region Init
    public static void GameInit()
    {
        string[] inputs;
        game.width = int.Parse(Console.ReadLine());
        game.height = int.Parse(Console.ReadLine());
        game.Map = new char[game.width, game.height];
        for (int i = 0; i < game.height; i++)
        {
            string line = Console.ReadLine();
            for (int j = 0; j < game.width; j++)
            {
                game.Map[j, i] = line.ElementAt(j);
            }
        }

        for (int i = 0; i < game.height; i++)
        {
            string line = string.Empty;
            for (int j = 0; j < game.width; j++)
            {
                line = line + game.Map[j, i];
            }
            Console.Error.WriteLine(line);
        }

        Console.Error.WriteLine(game.Map);

        inputs = Console.ReadLine().Split(' ');
        game.sanityLossLonely = int.Parse(inputs[0]); // how much sanity you lose every turn when alone, always 3 until wood 1
        game.sanityLossGroup = int.Parse(inputs[1]); // how much sanity you lose every turn when near another player, always 1 until wood 1
        game.wandererSpawnTime = int.Parse(inputs[2]); // how many turns the wanderer take to spawn, always 3 until wood 1
        game.wandererLifeTime = int.Parse(inputs[3]); // how many turns the wanderer is on map after spawning, always 40 until wood 1
    }

    public static void TurnInit()
    {
        string[] inputs;
        int entityCount = int.Parse(Console.ReadLine()); // the first given entity corresponds to your explorer
        for (int i = 0; i < entityCount; i++)
        {
            inputs = Console.ReadLine().Split(' ');
            /*foreach (var input in inputs)
            {
                Console.Error.WriteLine( input);
            }*/
            switch (inputs[0])
            {
                case "EXPLORER":
                    game.Explorateurs.Add(new Explorateur
                    {
                        ID = int.Parse(inputs[1]),
                        Position = new Point { x = int.Parse(inputs[2]), y = int.Parse(inputs[3]) },
                        health = int.Parse(inputs[4]),
                        state = int.Parse(inputs[5]),
                        param3 = int.Parse(inputs[6]),
                    });
                    break;

                case "WANDERER":
                    game.Wanderers.Add(new Wanderer
                    {
                        ID = int.Parse(inputs[1]),
                        Position = new Point { x = int.Parse(inputs[2]), y = int.Parse(inputs[3]) },
                        health = int.Parse(inputs[4]),
                        state = int.Parse(inputs[5]),
                        param3 = int.Parse(inputs[6]),
                    });
                    break;

                case "SLASHER":
                    game.Slashers.Add(new Slasher
                    {
                        ID = int.Parse(inputs[1]),
                        Position = new Point { x = int.Parse(inputs[2]), y = int.Parse(inputs[3]) },
                        health = int.Parse(inputs[4]),
                        state = int.Parse(inputs[5]),
                        param3 = int.Parse(inputs[6]),
                    });
                    break;

                case "EFFECT_SHELTER":
                    game.Shelters.Add(new Shelter
                    {
                        ID = int.Parse(inputs[1]),
                        Position = new Point { x = int.Parse(inputs[2]), y = int.Parse(inputs[3]) },
                        health = int.Parse(inputs[4]),
                        state = int.Parse(inputs[5]),
                        param3 = int.Parse(inputs[6]),
                    });
                    break;

                default:
                    break;
            }
        }
    }

    public static void TurnClear()
    {
        game.Explorateurs.Clear();
        game.Wanderers.Clear();
        game.Slashers.Clear();
        game.Shelters.Clear();
    }
    #endregion

    public static void GameLoop()
    {
        var ret = string.Empty;
        List<Point> newPositions = new List<Point> {
                new Point {x = game.Explorateurs[0].Position.x + 1, y = game.Explorateurs[0].Position.y},
                new Point {x = game.Explorateurs[0].Position.x - 1, y = game.Explorateurs[0].Position.y},
                new Point {x = game.Explorateurs[0].Position.x, y = game.Explorateurs[0].Position.y + 1},
                new Point {x = game.Explorateurs[0].Position.x, y = game.Explorateurs[0].Position.y - 1},
                };


        Point bestPosition = null;
        //Eviter les slashers
        foreach (var slasher in game.Slashers)
        {
            if ((game.Explorateurs[0].IsVisibleBy(slasher, game.Map)))
            {
                Console.Error.WriteLine("EN DANGER by SLASHER " + slasher.ID);
                foreach (var newPosition in newPositions)
                {
                    if (bestPosition == null)
                        bestPosition = newPosition;

                    if (game.Map[(int)newPosition.x, (int)newPosition.y] != '#' &&
                        newPosition.x != slasher.Position.x && newPosition.y != slasher.Position.y)
                    {
                        if (slasher.Position.DistanceTo(newPosition) > slasher.Position.DistanceTo(bestPosition))
                            bestPosition = newPosition;
                    }
                }
                ret = "MOVE " + bestPosition.x + " " + bestPosition.y;
            }
        }

        //Eviter les petits mobs
        foreach (var wanderer in game.Wanderers)
        {
            if ((game.Explorateurs[0].IsVisibleBy(wanderer, game.Map)))
            {
                Console.Error.WriteLine("EN DANGER by SLASHER " + wanderer.ID);
                foreach (var newPosition in newPositions)
                {
                    if (bestPosition == null)
                        bestPosition = newPosition;

                    if (wanderer.Position.DistanceTo(newPosition) > wanderer.Position.DistanceTo(bestPosition))
                        bestPosition = newPosition;
                }
                ret = "MOVE " + bestPosition.x + " " + bestPosition.y + " Tentative d'esquive du slasher";
            }
        }

        //Si en danger, on prend un soin
        if (string.IsNullOrEmpty(ret) && game.Explorateurs[0].health < 100 && game.Explorateurs[0].state > 0)
        {
            ret = "PLAN";
        }

        if (string.IsNullOrEmpty(ret) && game.Shelters.Count(s => s.health > 0) > 0)
        {
            //On prend l'abri le plus proche
            var nearest = game.Shelters.OrderBy(s => s.Position.DistanceTo(game.Explorateurs[0].Position)).Where(s => s.health > 0).FirstOrDefault();
            if (nearest != null)
            {
                var chemin = new ASTAR();
                var nextCase = chemin.GetChemin(game.Explorateurs[0].Position, nearest.Position, game.Map);
                ret = "MOVE " + nextCase.x + " " + nextCase.y;
            }
        }

        if (string.IsNullOrEmpty(ret))
        {
            //On essaye de se déplacer
            foreach (var newPosition in newPositions)
            {
                List<Player> enemyList = new List<Player>();
                enemyList.AddRange(game.Wanderers.Where(w => w.state != (int)State.SPAWNING));
                enemyList.AddRange(game.Slashers.Where(w => (w.state != (int)State.SPAWNING) && w.state != (int)State.STUNNED));

                if (game.Map[(int)newPosition.x, (int)newPosition.y] == '.' && enemyList.Count > 0)
                {
                    Console.Error.WriteLine("Test de " + newPosition.x + " " + newPosition.y);
                    if (bestPosition == null)
                        bestPosition = newPosition;

                    var nearest = enemyList.OrderBy(w => w.Position.DistanceTo(game.Explorateurs[0].Position)).FirstOrDefault();
                    Console.Error.WriteLine("best Distance " + bestPosition.DistanceTo(nearest.Position));
                    Console.Error.WriteLine("new Distance " + newPosition.DistanceTo(nearest.Position));
                    //On teste si on s'éloigne du minion, on doitaussi tester que la nouvelle position ne va pas nous mettre sur la case d'un Slasher
                    if (bestPosition.DistanceTo(nearest.Position) < newPosition.DistanceTo(nearest.Position))
                    {
                        foreach (var slasher in game.Slashers)
                        {
                            if (newPosition.x != slasher.Position.x && newPosition.y != slasher.Position.y)
                            {
                                bestPosition = newPosition;
                                continue;
                            }
                        }
                    }
                    ret = "MOVE " + bestPosition.x + " " + bestPosition.y;
                }
            }
        }
        if (!string.IsNullOrEmpty(ret))
            Console.WriteLine(ret); // MOVE <x> <y> | WAIT
        else
            Console.WriteLine("WAIT");
    }
}

public class Location
{
    public int x { get; set; }
    public int y { get; set; }
    public int F { get; set; }
    public int G { get; set; }
    public int H { get; set; }
    public Location Parent { get; set; }
}

public class ASTAR
{
    public Point GetChemin(Point depart, Point finish, char[,] map)
    {
        Location current = null;
        var start = new Location { x = (int)depart.x, y = (int)depart.y };
        var target = new Location { x = (int)finish.x, y = (int)finish.y };
        List<Location> openList = new List<Location>();
        List<Location> closedList = new List<Location>();
        int g = 0;

        openList.Add(start);

        while (openList.Count > 0)
        {
            var lowest = openList.Min(l => l.F);
            current = openList.First(l => l.F == lowest);

            closedList.Add(current);
            openList.Remove(current);

            if (closedList.FirstOrDefault(l => l.x == target.x && l.y == target.y) != null)
                break;

            var adjacents = GetWalkableAdjacent(current.x, current.y, map);
            g++;

            foreach (var adjacent in adjacents)
            {
                if (closedList.FirstOrDefault(l => l.x == adjacent.x
                && l.y == adjacent.y) == null)
                    continue;

                if (openList.FirstOrDefault(l => l.x == adjacent.x && l.y == adjacent.y) == null)
                {
                    adjacent.G = g;
                    adjacent.H = ComputeHScore(adjacent.x, adjacent.y, target.x, target.y);
                    adjacent.F = adjacent.G + adjacent.H;
                    adjacent.Parent = current;

                    openList.Insert(0, adjacent);
                }
                else
                {
                    if (g + adjacent.H < adjacent.F)
                    {
                        adjacent.G = g;
                        adjacent.F = adjacent.G + adjacent.H;
                        adjacent.Parent = current;
                    }
                }
            }
        }
        return new Point { x = current.x, y = current.y };
    }

    private List<Location> GetWalkableAdjacent(int x, int y, char[,] map)
    {
        var proposedLocations = new List<Location>()
        {
            new Location {x = x, y = y-1},
            new Location {x = x, y = y+1},
            new Location {x = x+1, y = y},
            new Location {x = x-1, y = y}
        };

        return proposedLocations.Where(l => map[l.x, l.y] == '.' || map[l.x, l.y] == 'w' || map[l.x, l.y] == 'U').ToList();
    }

    private int ComputeHScore(int x, int y, int targetX, int targetY)
    {
        return Math.Abs(targetX - x) + Math.Abs(targetY - y);
    }
}