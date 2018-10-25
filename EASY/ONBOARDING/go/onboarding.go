package main

import "fmt"

func main() {
    for
    {
        // enemy1: name of enemy 1
        var enemy1 string
        fmt.Scan(&enemy1)

        // dist1: distance to enemy 1
        var dist1 int
        fmt.Scan(&dist1)

        // enemy2: name of enemy 2
        var enemy2 string
        fmt.Scan(&enemy2)

        // dist2: distance to enemy 2
        var dist2 int
        fmt.Scan(&dist2)

        if dist1 < dist2 {
            fmt.Println(enemy1)
        } else {
            fmt.Println(enemy2)
        }
    }
}