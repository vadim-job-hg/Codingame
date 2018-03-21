open System

while true do
    let enemy1 = Console.In.ReadLine() (* name of enemy 1 *)
    let dist1 = int(Console.In.ReadLine()) (* distance to enemy 1 *)
    let enemy2 = Console.In.ReadLine() (* name of enemy 2 *)
    let dist2 = int(Console.In.ReadLine()) (* distance to enemy 2 *)

    if dist1 < dist2 then printfn "%s" enemy1
    else printfn "%s" enemy2

()