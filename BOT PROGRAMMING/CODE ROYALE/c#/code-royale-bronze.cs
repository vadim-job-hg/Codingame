using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;

/**
 * This code was developped in 1.5 days, it won't be the cleanest you ever seen.
 **/

enum Action {BUILD_TOWER,
             BUILD_MINE,
             BUILD_CASERNE,
             BUILD_ARCHERY,
             REPAIR_TOWER,
             REPAIR_MINE,
             SELF_PROTECT,
             SELF_PROTECT_TOWER,
             DESTROY
            };

class Player
{

    //Game Variables
    static List<Barrack> listBarrack = new List<Barrack>{};
    static List<Unit> listUnit = new List<Unit>{};
    static Joueur moi = new Joueur(0, 100);
    static Joueur adv = new Joueur(1, 100);
    static int currentScale = 1;

    static Joueur getJoueurFromId(int id){
        if(id == 0)
            return moi;
        if(id == 1)
            return adv;
        return null;
    }

    static Barrack getBarrackFromId(int id){
        foreach(Barrack barrack in listBarrack) {
            if(barrack.id == id)
                return barrack;
        }
        return null;
    }

    static string barrackTypeToString(BarrackType type){
        if(type == BarrackType.BUILD_SITE)
            return "BARRACKS-BUILD"; //unusable
        if(type == BarrackType.CASERNE)
            return "BARRACKS-KNIGHT";
        if(type == BarrackType.ARCHERY)
            return "BARRACKS-ARCHER";
        if(type == BarrackType.TOWER)
            return "TOWER";
        if(type == BarrackType.MINE)
            return "MINE";
        return "";
    }

    static void Main(string[] args)
    {
        //Standard input
        string[] inputs;
        int numSites = int.Parse(Console.ReadLine());
        for (int i = 0; i < numSites; i++)
        {
            inputs = Console.ReadLine().Split(' ');
            int siteId = int.Parse(inputs[0]);
            int x = int.Parse(inputs[1]);
            int y = int.Parse(inputs[2]);
            int radius = int.Parse(inputs[3]);
            listBarrack.Add(new Barrack(siteId,x,y,radius, -1));
        }

        // game loop
        while (true)
        {

            //Joueur
            inputs = Console.ReadLine().Split(' ');
            int gold = int.Parse(inputs[0]);
            int touchedSite = int.Parse(inputs[1]); // -1 if none
            moi.gold = gold;
            moi.touchedSite = touchedSite;

            for (int i = 0; i < numSites; i++)
            {
                inputs = Console.ReadLine().Split(' ');
                int siteId = int.Parse(inputs[0]);
                int remainingGold = int.Parse(inputs[1]); // used in future leagues
                int maxProductionRate = int.Parse(inputs[2]); // used in future leagues
                int structureType = int.Parse(inputs[3]); // -1 = No structure, 2 = Barracks
                int owner = int.Parse(inputs[4]); // -1 = No structure, 0 = Friendly, 1 = Enemy
                int param1 = int.Parse(inputs[5]);
                int param2 = int.Parse(inputs[6]);
                Barrack barrack = getBarrackFromId(siteId);
                if(barrack == null)
                    Console.Error.WriteLine("WARN: Barrack not found " + siteId);
                else {
                    BarrackType type = BarrackType.BUILD_SITE;
                    if(structureType == 2 && param2 == 0)
                        type = BarrackType.CASERNE;
                    else if(structureType == 2 && param2 == 1)
                        type = BarrackType.ARCHERY;
                    else if(structureType == 1){
                        type = BarrackType.TOWER;
                        barrack.pv = param1;
                        barrack.actionRadius = param2;
                    }
                    else if(structureType == 0){
                        type = BarrackType.MINE;
                        barrack.productionRate = param1;
                        barrack.maxProductionRate = maxProductionRate;
                        barrack.remainingGold = remainingGold;
                    }
                    barrack.setType(type);
                    barrack.ownerId = owner;
                    barrack.cyclesRemaining = param1;
                }
            }

            //Units
            int numUnits = int.Parse(Console.ReadLine());
            listUnit.Clear();
            listUnit.Capacity = numUnits - 2; // - 2 queens
            for (int i = 0; i < numUnits; i++)
            {
                inputs = Console.ReadLine().Split(' ');
                int x = int.Parse(inputs[0]);
                int y = int.Parse(inputs[1]);
                int owner = int.Parse(inputs[2]);
                int unitType = int.Parse(inputs[3]); // -1 = QUEEN, 0 = KNIGHT, 1 = ARCHER
                int health = int.Parse(inputs[4]);
                if(unitType == -1) { //Qween
                    Joueur joueur = getJoueurFromId(owner);
                    if(joueur.queen == null){
                        joueur.queen = new Unit(x,y,health,UnitType.QUEEN, owner);
                        listUnit.Add(joueur.queen);
                    }
                    else{
                        joueur.queen.x = x;
                        joueur.queen.y = y;
                        joueur.queen.pv = health;
                    }
                }
                else{
                    UnitType type = UnitType.UNKNOWN;
                    if(unitType == 0)
                        type = UnitType.KNIGHT;
                    else if(unitType == 1)
                        type = UnitType.ARCHER;
                    listUnit.Add(new Unit(x,y,health,type, owner));
                }
            }
            //Output variables
            Barrack selectedBarrack = null;
            BarrackType selectedType = BarrackType.CASERNE;
            bool shouldBuild = false;
            List<int> listTrainingId = new List<int>{};
            listBarrack = listBarrack.OrderBy(x => moi.queen.distanceTo(x)).ToList();

            int towerTargetCount = 0;
            int mineTargetCount = 0;
            int caserneTargetCount = 0;
            int armyTargetSize = 1;
            int giantTargetCount = 0;
            int protectionPointX = 0;
            int protectionPointY = 0;
            List<Action> priorityList = new List<Action>{};

            bool underAttack = false;
            int attackDistance = 2000;
            int meanAdvFirstUnitsX = 0;
            int meanAdvFirstUnitsY = 0;
            int meanAdvFirstUnitsCount = 0;
            listUnit = listUnit.OrderBy(x => moi.queen.distanceTo(x)).ToList();
            int c=0;
            foreach(Unit unit in listUnit) {
                if(unit.ownerId != moi.id
                && unit.pv>6
                ){
                    if(c<3){
                        meanAdvFirstUnitsX += unit.x;
                        meanAdvFirstUnitsY += unit.y;
                        meanAdvFirstUnitsCount++;
                        c++;
                    }
                    else
                        break;
                }
            }
            if(meanAdvFirstUnitsCount > 1){
                meanAdvFirstUnitsX /= meanAdvFirstUnitsCount;
                meanAdvFirstUnitsY /= meanAdvFirstUnitsCount;
                attackDistance = (int) moi.queen.distanceTo(meanAdvFirstUnitsX,meanAdvFirstUnitsY);
                if(attackDistance < 150){
                    underAttack = true;
                    Console.Error.WriteLine("Under attack");
                }
            }
            Console.Error.WriteLine("Touching "+moi.touchedSite);
            int currentTowerCount = listBarrack.FindAll(o=>o.ownerId == moi.id && o.type == BarrackType.TOWER).Count();
            int currentMineCount = listBarrack.FindAll(o=>o.ownerId == moi.id && o.type == BarrackType.MINE).Count();
            int currentCaserneCount = listBarrack.FindAll(o=>o.ownerId == moi.id && o.type == BarrackType.CASERNE).Count();
            for(int i=0;i<=5;i++){
                if(i == 0){
                   towerTargetCount = 0;
                   mineTargetCount = 3;
                   caserneTargetCount = 0;
                   armyTargetSize = 1;
                   priorityList = new List<Action>{
                       Action.REPAIR_MINE,
                       Action.BUILD_MINE,
                       Action.BUILD_CASERNE,
                       Action.REPAIR_TOWER,
                       Action.BUILD_TOWER,
                       Action.SELF_PROTECT,
                       Action.SELF_PROTECT_TOWER
                   };
                   if(moi.queen.pv <= 40){
                       priorityList = new List<Action>{
                       Action.BUILD_CASERNE,
                       Action.REPAIR_MINE,
                       Action.BUILD_MINE,
                       Action.REPAIR_TOWER,
                       Action.BUILD_TOWER,
                       Action.SELF_PROTECT,
                       Action.SELF_PROTECT_TOWER
                       };
                   }
                }
                else if(i == 1){ //add 1 tower fast
                   towerTargetCount = 1;
                   mineTargetCount = 3;
                   caserneTargetCount = 1;
                   armyTargetSize = 1;
                   priorityList = new List<Action>{
                       Action.BUILD_CASERNE,
                       Action.REPAIR_MINE,
                       Action.BUILD_MINE,
                       Action.REPAIR_TOWER,
                       Action.BUILD_TOWER,
                       Action.SELF_PROTECT,
                       Action.SELF_PROTECT_TOWER
                   };
                }
                else if(i == 2){
                   towerTargetCount = 3;
                   mineTargetCount = 3;
                   caserneTargetCount = 2;
                   armyTargetSize = 2;
                   priorityList = new List<Action>{
                       Action.BUILD_TOWER,
                       Action.REPAIR_TOWER,
                       Action.REPAIR_MINE,
                       Action.BUILD_MINE,
                       Action.SELF_PROTECT,
                       Action.BUILD_CASERNE,
                       Action.SELF_PROTECT_TOWER
                   };
                }
                /*else if(i == 3){
                   towerTargetCount = 3;
                   mineTargetCount = 3;
                   caserneTargetCount = 2;
                   armyTargetSize = 2;
                   priorityList = new List<Action>{
                       Action.REPAIR_TOWER,
                       Action.BUILD_TOWER,
                       Action.SELF_PROTECT,
                       Action.REPAIR_MINE,
                       Action.BUILD_CASERNE,
                       Action.BUILD_MINE,
                       Action.SELF_PROTECT_TOWER
                   };
                }*/
                else if(i == 4){
                   towerTargetCount = 4;
                   mineTargetCount = 3;
                   caserneTargetCount = 3;
                   armyTargetSize = 2;
                   priorityList = new List<Action>{
                       Action.REPAIR_TOWER,
                       Action.BUILD_TOWER,
                       Action.SELF_PROTECT,
                       Action.REPAIR_MINE,
                       Action.BUILD_CASERNE,
                       Action.BUILD_MINE,
                       Action.SELF_PROTECT_TOWER
                   };
                }
                else if(i == 5){
                   towerTargetCount = 5;
                   mineTargetCount = 3;
                   caserneTargetCount = 2;
                   armyTargetSize = 2;
                   priorityList = new List<Action>{
                       Action.REPAIR_TOWER,
                       Action.SELF_PROTECT,
                       Action.REPAIR_MINE,
                       Action.BUILD_TOWER,
                       Action.BUILD_CASERNE,
                       Action.BUILD_MINE,
                       Action.SELF_PROTECT_TOWER
                   };
                }
                if(towerTargetCount>currentTowerCount
                || mineTargetCount>currentMineCount
                || caserneTargetCount>currentCaserneCount){
                    currentScale = i;
                    break;
                }
                currentScale = i;
            }
            if(underAttack /*|| moi.queen.pv < 15*/){
                if(towerTargetCount<4)
                    towerTargetCount = 4;
                priorityList = new List<Action>{
                   Action.REPAIR_TOWER,
                   Action.BUILD_TOWER,
                   Action.SELF_PROTECT,
                   Action.BUILD_CASERNE,
                   Action.REPAIR_MINE,
                   Action.BUILD_MINE,
                   Action.SELF_PROTECT_TOWER
               };
               if(moi.touchedSite !=-1 && getBarrackFromId(moi.touchedSite).type != BarrackType.TOWER){
                   priorityList = new List<Action>{
                   Action.BUILD_TOWER,
                   Action.REPAIR_TOWER,
                   Action.SELF_PROTECT,
                   Action.BUILD_CASERNE,
                   Action.REPAIR_MINE,
                   Action.BUILD_MINE,
                   Action.SELF_PROTECT_TOWER
               };
               }
            }


            Console.Error.WriteLine("Scale "+currentScale);
            Console.Error.WriteLine("Tower "+currentTowerCount+"/"+towerTargetCount);
            Console.Error.WriteLine("Mine "+currentMineCount+"/"+mineTargetCount);
            Console.Error.WriteLine("Caserne "+currentCaserneCount+"/"+caserneTargetCount);
            Console.Error.WriteLine("Adv at "+attackDistance);

            foreach(Action action in priorityList) {
                switch(action){
                    case Action.SELF_PROTECT:
                        if(shouldBuild == false && selectedBarrack == null && moi.queen.pv < 45
                        && protectionPointX == 0 && protectionPointY == 0){
                            bool ennemyClose = false;
                            foreach(Unit unit in listUnit) {
                                if(unit.ownerId != moi.id
                                && unit.distanceTo(moi.queen) < 300
                                ){
                                    ennemyClose = true;
                                    break;
                                }
                            }
                            if(ennemyClose){
                                List<Barrack> moiTowerList = listBarrack.Where(x=>x.ownerId == moi.id && x.type == BarrackType.TOWER).ToList();
                                if(moiTowerList.Count>1){
                                    //Get moi tower center
                                    int towerCenterX = 0;
                                    int towerCenterY = 0;
                                    foreach(Barrack tower in moiTowerList){
                                        towerCenterX += tower.x;
                                        towerCenterY += tower.y;
                                    }
                                    towerCenterX /= moiTowerList.Count;
                                    towerCenterY /= moiTowerList.Count;
                                    protectionPointX = towerCenterX;
                                    protectionPointY = towerCenterY;

                                    //Get adv unit center
                                    int advUnitCenterX = 0;
                                    int advUnitCenterY = 0;
                                    int advUnitCount = 0;
                                    foreach(Unit unit in listUnit){
                                        if(unit.ownerId == adv.id && unit.type != UnitType.QUEEN){
                                            advUnitCenterX += unit.x;
                                            advUnitCenterY += unit.y;
                                            advUnitCount++;
                                        }
                                    }
                                    advUnitCenterX /= advUnitCount;
                                    advUnitCenterY /= advUnitCount;

                                    //move back keeping in the towers range
                                    bool postitionValid = true;
                                    for(double i=0;i<=1 && postitionValid;i+=0.02){
                                        int x1 = towerCenterX + (int)(i*(double)(towerCenterX-advUnitCenterX));
                                        int y1 = towerCenterY + (int)(i*(double)(towerCenterY-advUnitCenterY));
                                        int inRadiusCount = 0;
                                        foreach(Barrack tower in moiTowerList){
                                            if(tower.distanceTo(x1,y1) < tower.actionRadius){
                                                inRadiusCount++;
                                            }
                                        }
                                        postitionValid = inRadiusCount>=3;
                                        if(postitionValid){
                                            protectionPointX = x1;
                                            protectionPointY = y1;
                                        }
                                    }
                                    Console.Error.WriteLine("Protect "+(protectionPointX-moi.queen.x)+" "+(protectionPointY-moi.queen.y));
                                }
                            }
                        }
                        break;
                    case Action.SELF_PROTECT_TOWER:
                        if(shouldBuild == false && selectedBarrack == null && moi.queen.pv < 60
                        && protectionPointX == 0 && protectionPointY == 0){
                            bool towerClose = false;
                            foreach(Barrack barrack in listBarrack) {
                                if(barrack.ownerId != moi.id
                                && barrack.type == BarrackType.TOWER
                                && barrack.distanceTo(moi.queen) <= barrack.actionRadius + 60
                                ){
                                    bool protectedByUnit = false;
                                    foreach(Unit unit in listUnit){
                                        if(unit.ownerId == moi.id
                                        && barrack.distanceTo(unit) <= barrack.actionRadius){
                                            protectedByUnit = true;
                                            break;
                                        }
                                    }
                                    if(!protectedByUnit){
                                        Console.Error.WriteLine("TC:"+barrack.id+"  "+barrack.distanceTo(moi.queen)+" < "+barrack.actionRadius);
                                        towerClose = true;
                                        break;
                                    }
                                }
                            }
                            if(towerClose){
                                List<Barrack> moiTowerList = listBarrack.Where(x=>x.ownerId == moi.id && x.type == BarrackType.TOWER).ToList();
                                foreach(Barrack tower in moiTowerList){
                                    protectionPointX += tower.x;
                                    protectionPointY += tower.y;
                                }
                                if(moiTowerList.Count>0){
                                    protectionPointX /= moiTowerList.Count;
                                    protectionPointY /= moiTowerList.Count;
                                    Console.Error.WriteLine("Protect Tower ");
                                }
                            }
                        }
                        break;
                    case Action.DESTROY:
                        //Destroy adv towers
                        Console.Error.WriteLine("Destroy adv ");
                        listBarrack = listBarrack.OrderBy(x => moi.queen.distanceTo(x)).ToList();
                        if(shouldBuild == false){
                            foreach(Barrack barrack in listBarrack) {
                                if(selectedBarrack == null && barrack.isBuildable(moi, listBarrack, false)){
                                    selectedBarrack = barrack;
                                    selectedType = BarrackType.TOWER;
                                    shouldBuild = true;
                                    Console.Error.WriteLine("DT "+barrack.id);
                                    break;
                                }
                            }
                        }
                        break;
                    case Action.BUILD_TOWER:
                        //Keep n towers built, prefer building on moi side
                        listBarrack = listBarrack.OrderBy(x => moi.queen.distanceTo(x) - 0.5*x.distanceTo(1920/2,moi.queen.y)).ToList();
                        int moiTowerBuilt = listBarrack.FindAll(o=>o.ownerId == moi.id && o.type == BarrackType.TOWER).Count();
                        if(shouldBuild == false && moiTowerBuilt<towerTargetCount){
                            foreach(Barrack barrack in listBarrack) {
                                bool allowOwn = false;
                                if(selectedBarrack!=null){
                                    allowOwn = moi.queen.pv < 20 && selectedBarrack.ownerId == moi.id && selectedBarrack.type != BarrackType.TOWER;
                                }
                                if(selectedBarrack == null && barrack.isBuildable(moi, listBarrack, allowOwn)){
                                    selectedBarrack = barrack;
                                    selectedType = BarrackType.TOWER;
                                    shouldBuild = true;
                                    break;
                                }
                            }
                        }
                        break;
                    case Action.BUILD_MINE:
                        //Keep n mine built
                        listBarrack = listBarrack.OrderBy(x => moi.queen.distanceTo(x) - 100*(x.maxProductionRate>0?x.maxProductionRate:1) ).ToList();
                        int moiMineBuilt = listBarrack.FindAll(o=>o.ownerId == moi.id && o.type == BarrackType.MINE).Count();
                        if(shouldBuild == false && moiMineBuilt<mineTargetCount){
                            foreach(Barrack barrack in listBarrack) {

                                bool allowOwn = towerTargetCount<currentTowerCount && currentTowerCount>2 && barrack.type == BarrackType.TOWER;

                                if(selectedBarrack == null
                                && barrack.isBuildable(moi, listBarrack, allowOwn ) //allow to destroy own towers
                                && (barrack.remainingGold>50 || barrack.remainingGold==-1)
                                ){
                                    bool advClose = false;
                                    foreach(Unit unit in listUnit) {
                                        if(unit.ownerId != moi.id
                                        && unit.distanceTo(barrack) < barrack.radius + 30
                                        ){
                                            advClose = true;
                                            break;
                                        }
                                    }
                                    bool reachable = true;
                                    if(attackDistance<barrack.distanceTo(moi.queen))
                                        reachable = false;
                                    if(!advClose && reachable){
                                        selectedBarrack = barrack;
                                        selectedType = BarrackType.MINE;
                                        shouldBuild = true;
                                        Console.Error.WriteLine("BM ID "+barrack.id+" G"+barrack.remainingGold+" R"+barrack.maxProductionRate+" "+barrackTypeToString(barrack.type));
                                        Console.Error.WriteLine("Own:"+allowOwn+" Build:"+barrack.isBuildable(moi, listBarrack, allowOwn ));
                                        break;
                                    }
                                }
                            }
                        }
                        break;
                    case Action.REPAIR_MINE:
                        //Repair mines
                        List<Barrack> moiMineList = listBarrack.Where(x=>x.ownerId == moi.id && x.type == BarrackType.MINE).ToList();
                        moiMineList = moiMineList.OrderBy(x => x.productionRate).ToList();
                        if(shouldBuild == false){
                            foreach(Barrack barrack in moiMineList) {
                                if(barrack.productionRate < barrack.maxProductionRate){
                                    Console.Error.WriteLine("RM "+barrack.productionRate+" "+barrack.maxProductionRate);
                                    selectedBarrack = barrack;
                                    selectedType = BarrackType.MINE;
                                    shouldBuild = true;
                                    break;
                                }
                            }
                        }
                        break;
                    case Action.BUILD_CASERNE:
                        //Keep n caserne built, prefer building in the middle
                        listBarrack = listBarrack.OrderBy(x => moi.queen.distanceTo(x) + 0.5*x.distanceTo(1920/2,moi.queen.y)).ToList();
                        int moiCaserneBuilt = listBarrack.FindAll(o=>o.ownerId == moi.id && o.type == BarrackType.CASERNE).Count();
                        if(shouldBuild == false && moiCaserneBuilt<caserneTargetCount){
                            foreach(Barrack barrack in listBarrack) {
                                if(selectedBarrack == null && barrack.isBuildable(moi, listBarrack)){
                                    selectedBarrack = barrack;
                                    selectedType = BarrackType.CASERNE;
                                    shouldBuild = true;
                                    break;
                                }
                            }
                        }
                        break;
                    case Action.REPAIR_TOWER:
                        //Repair towers
                        listBarrack = listBarrack.OrderBy(x => moi.queen.distanceTo(x)).ToList();
                        List<Barrack> towerList = listBarrack.Where(x=>x.ownerId == moi.id && x.type == BarrackType.TOWER).ToList();
                        towerList = towerList.OrderBy(x => moi.queen.distanceTo(x)).ToList();
                        if(shouldBuild == false && currentTowerCount<=towerTargetCount){
                            foreach(Barrack barrack in towerList) {
                                int minPoints = 200;
                                if(moi.touchedSite == barrack.id)
                                    minPoints = 700;
                                if(barrack.pv < minPoints){
                                    Console.Error.WriteLine("RT "+barrack.pv);
                                    selectedBarrack = barrack;
                                    selectedType = BarrackType.TOWER;
                                    shouldBuild = true;
                                    break;
                                }
                            }
                        }
                        break;
                    default:
                        break;
                }
            }

            //Wait gold for n knight army
            int moiCaserneCount = listBarrack.FindAll(o=>o.ownerId == moi.id && o.type == BarrackType.CASERNE).Count();
            if(moiCaserneCount<armyTargetSize)
                armyTargetSize = moiCaserneCount;
            if(moi.gold >= armyTargetSize*Unit.getUnitCost(UnitType.KNIGHT)){
                listBarrack = listBarrack.OrderBy(x => adv.queen.distanceTo(x)).ToList();
                foreach(Barrack barrack in listBarrack) {
                    if(barrack.ownerId == moi.id
                    && barrack.cyclesRemaining == 0
                    && barrack.type == BarrackType.CASERNE){
                        if(moi.gold >= barrack.unitCost){
                            listTrainingId.Add(barrack.id);
                            moi.gold -= barrack.unitCost;
                            Console.Error.WriteLine("train army");
                        }
                    }
                }
            }

            //Send knight if queen is close
            if(moi.gold >= Unit.getUnitCost(UnitType.KNIGHT)){
                listBarrack = listBarrack.OrderBy(x => adv.queen.distanceTo(x)).ToList();
                foreach(Barrack barrack in listBarrack) {
                    if(barrack.ownerId == moi.id
                    && barrack.cyclesRemaining == 0
                    && barrack.type == BarrackType.CASERNE){
                        if(moi.gold >= barrack.unitCost
                        && barrack.distanceTo(adv.queen) < 550){
                            listTrainingId.Add(barrack.id);
                            moi.gold -= barrack.unitCost;
                            Console.Error.WriteLine("adv queen close");
                        }
                    }
                }
            }


            //Write the output
            // First line: A valid queen action
            // Second line: A set of training instructions
            //Build
            if(protectionPointX != 0 && protectionPointY != 0){
                Console.Error.WriteLine(">Protect");
                if(moi.touchedSite != -1
                && (getBarrackFromId(moi.touchedSite).type == BarrackType.BUILD_SITE
                    || (getBarrackFromId(moi.touchedSite).ownerId == adv.id && getBarrackFromId(moi.touchedSite).type != BarrackType.TOWER)
                    )
                )
                    Console.WriteLine("BUILD " + moi.touchedSite + " " + barrackTypeToString(BarrackType.TOWER));
                else
                    Console.WriteLine("MOVE " + protectionPointX + " " + protectionPointY);
            }
            else if(shouldBuild && moi.touchedSite != -1 && selectedBarrack.id == moi.touchedSite){
                Console.Error.WriteLine(">Build");
                Console.WriteLine("BUILD " + selectedBarrack.id + " " + barrackTypeToString(selectedType));
            }
            else if(selectedBarrack != null){
                Console.Error.WriteLine(">Move "+selectedBarrack.id);
                if(moi.touchedSite != -1
                && (getBarrackFromId(moi.touchedSite).type == BarrackType.BUILD_SITE
                    || (getBarrackFromId(moi.touchedSite).ownerId == adv.id && getBarrackFromId(moi.touchedSite).type != BarrackType.TOWER)
                    )
                )
                    Console.WriteLine("BUILD " + moi.touchedSite + " " + barrackTypeToString(BarrackType.TOWER));
                else
                    Console.WriteLine("MOVE " + selectedBarrack.x + " " + selectedBarrack.y);
            }
            else{
                Console.Error.WriteLine(">Wait");
                int advUnitCount = listUnit.FindAll(o=>o.ownerId != moi.id && o.type != UnitType.QUEEN).Count();;
                if(moi.touchedSite != -1 && getBarrackFromId(moi.touchedSite).type == BarrackType.BUILD_SITE)
                    Console.WriteLine("BUILD " + moi.touchedSite + " " + barrackTypeToString(BarrackType.TOWER));
                else if(advUnitCount>4){
                    //hide beetween towers
                    List<Barrack> moiTowerList = listBarrack.Where(x=>x.ownerId == moi.id && x.type == BarrackType.TOWER).ToList();
                    protectionPointX = 0;
                    protectionPointY = 0;
                    foreach(Barrack tower in moiTowerList){
                        protectionPointX += tower.x;
                        protectionPointY += tower.y;
                    }
                    if(moiTowerList.Count>0){
                        protectionPointX /= moiTowerList.Count;
                        protectionPointY /= moiTowerList.Count;
                        Console.Error.WriteLine("Protect waiting");
                        Console.WriteLine("MOVE " + protectionPointX + " " + protectionPointY);
                    }
                }
                else
                    Console.WriteLine("WAIT");
            }

            //Training
            string trainingList = "";
            foreach(int id in listTrainingId) {
                trainingList += " " + id;
            }
            Console.WriteLine("TRAIN" + trainingList);
        }
    }
}

class Joueur
{
    public int id;
    public int gold;
    public Unit queen = null;
    public int touchedSite = -1;

    public Joueur(int id, int gold)
    {
        this.id = id;
        this.gold = gold;
    }

}

enum UnitType {UNKNOWN,QUEEN,KNIGHT,ARCHER};

class Unit
{
    public int x,y;
    public int pv;
    public UnitType type;
    public int ownerId;

    public Unit(int x, int y, int pv, UnitType type, int ownerId)
    {
        this.x = x;
        this.y = y;
        this.pv = pv;
        this.type = type;
        this.ownerId = ownerId;
    }

    public double distanceTo(Barrack barrack){
        return Math.Sqrt((Math.Pow(barrack.x-x,2)+Math.Pow(barrack.y-y,2)));
    }

    public double distanceTo(Unit unit){
        return Math.Sqrt((Math.Pow(unit.x-x,2)+Math.Pow(unit.y-y,2)));
    }

    public double distanceTo(int x1, int y1){
        return Math.Sqrt((Math.Pow(x1-x,2)+Math.Pow(y1-y,2)));
    }

    public static int getUnitCost(UnitType type){
        if(type == UnitType.KNIGHT)
            return 80;
        else if(type == UnitType.ARCHER)
            return 100;
        return 0;
    }
}

enum BarrackType {BUILD_SITE,CASERNE,ARCHERY,TOWER,MINE};

class Barrack
{
    public int id;
    public int x,y;
    public BarrackType type = BarrackType.BUILD_SITE;
    public int ownerId;
    public int radius;
    public int cyclesRemaining = 0; //CASERNE,ARCHERY
    public int pv = 0;//towers
    public int unitCost = 0; //CASERNE,ARCHERY
    public int productionRate = 0;
    public int maxProductionRate = 0;
    public int remainingGold = -1;
    public int actionRadius = -1;

    public Barrack(int id, int x, int y, int radius, int ownerId)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.radius = radius;
        this.ownerId = ownerId;
    }

    public double distanceTo(Barrack barrack){
        return Math.Sqrt((Math.Pow(barrack.x-x,2)+Math.Pow(barrack.y-y,2)));
    }

    public double distanceTo(Unit unit){
        return Math.Sqrt((Math.Pow(unit.x-x,2)+Math.Pow(unit.y-y,2)));
    }

    public double distanceTo(int x1, int y1){
        return Math.Sqrt((Math.Pow(x1-x,2)+Math.Pow(y1-y,2)));
    }

    public void setType(BarrackType type){
        this.type = type;
        if(type == BarrackType.CASERNE)
            this.unitCost = Unit.getUnitCost(UnitType.KNIGHT);
        else if(type == BarrackType.ARCHERY)
            this.unitCost = Unit.getUnitCost(UnitType.ARCHER);
    }

    public bool isBuildable(Joueur moi, List<Barrack> barrackList, bool allowOwn=false){
        if(ownerId != moi.id || allowOwn){
            if(ownerId != moi.id && type == BarrackType.TOWER && actionRadius > 100)
                return false;
            if(moi.queen.pv < 30){
                foreach(Barrack barrack in barrackList){
                    if(barrack.ownerId != moi.id && barrack.type == BarrackType.TOWER){
                        if(barrack.actionRadius > distanceTo(barrack)) //if target in adv tower range
                            return false;
                    }
                }
                //if path through adv tower range
                for(double i=0;i<=1;i+=0.1){
                    int x1 = moi.queen.x + (int)(i*(double)(x-moi.queen.x));
                    int y1 = moi.queen.y + (int)(i*(double)(y-moi.queen.y));
                    foreach(Barrack barrack in barrackList){
                    if(barrack.ownerId != moi.id && barrack.type == BarrackType.TOWER){
                        if(barrack.actionRadius < barrack.distanceTo(moi.queen)){
                            if(barrack.actionRadius > barrack.distanceTo(x1,y1)) //if target in adv tower range
                                return false;
                        }
                    }
                }
                }
            }
            return true;
        }
        return false;
    }
}