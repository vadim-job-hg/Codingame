/**
  * https://www.codingame.com/multiplayer/bot-programming/ghost-in-the-cell
  * Created by kotobotov.ru on 26.02.2017.
  */

object Player extends App {
  val factorycount = readInt
  val linkcount = readInt
  var allNodes = List[List[Int]]()
  for (i <- 0 until linkcount) {
    val node = for (i <- readLine split " ") yield i.toInt
    allNodes = allNodes ++ List(node.toList) ++ List(List(node(1), node(0), node(2)))
  }

  object Config {
    val ME = 1
    val OPPONENT = -1
    val NOBODY = 0
    var bombCounter = 2
    var clasterCenter: Int = 1
    var firstRun = true
  }


  val cells = for (j <- 0 until factorycount) yield new Cell(j, allNodes.filter(_.head == j).map(item => (item(1), item(2))).sortBy(_._2))

  case class Cell(id: Int, listOfNodes: List[(Int, Int)]) {
    var alreadyChecked = false
    var owner = 0.0
    var defenders = 0.0
    var production = 0.0
    var totalIncome3Steep = 0.0
    var totalIncome1Steep = 0.0
    var totalIncome6Steep = 0.0
    var recomendToreduceOutcome = 0.0
    var ownerCounter = 0
    var owners = Array(0.0, 0.0, 0.0, 0.0, 0.0)
    var alreadeAttacked = false
    var attackKoeficient = 1.2
    var deffendCoeficient = 0.0
    var roiPerDistance = 100.0
    var roi = 10000.0
    var targetList: List[(Int, Double)] = List.empty[(Int, Double)]

    def mayDropBomb = {
      Config.bombCounter match {
        case 0 => false
        case _ => production match {
          case 0.0 => false
          case 1.0 => false
          case _ => owners.sum match {
            case -5.0 => {
              alreadeAttacked match {
                case true => false
                case false =>
                  if (defenders >= 2.0) {
                    alreadeAttacked = true
                    true
                  }
                  else false
              }
            }
            case _ => false
          }
        }
      }
    }

    def sendBomb(target: Int) = {
      Config.bombCounter -= 1
      Answer.add(s"BOMB $id $target")
    }

    def incomingRobots = {

      val correctedIncome1 = if (totalIncome1Steep < 0) totalIncome1Steep + production else totalIncome1Steep
      val correctedIncome3 = if (totalIncome3Steep < 0) totalIncome3Steep + (production) else 0
      val correctedIncome6 = if (totalIncome6Steep < 0) totalIncome6Steep + (production) else 0
      math.floor(correctedIncome1 - correctedIncome3 - correctedIncome6)
    }

    def needToAttack(distance: Int) = {
      val currentProduction = if (owner == Config.NOBODY) 0 else production * (-1)
      math.floor(defenders - totalIncome1Steep - totalIncome3Steep - totalIncome6Steep + 1 - (currentProduction * distance))

    }

    def setIncome1Steep(delta: Double) = {
      totalIncome1Steep += delta
    }

    def setIncome3Steep(delta: Double) = {
      totalIncome3Steep += (delta)
    }

    def setIncome6Steep(delta: Double) = {
      totalIncome6Steep += (delta)
    }

    def directSend(to: Int, amount: Int): Unit = {
      if (amount > 0) {
        defenders -= amount.toDouble
        cells(to).setIncome1Steep(amount)
//                Answer.add(s"MOVE $id ${shorterPath(to)} $amount")
        Answer.add(s"MOVE $id $to $amount")
      }
    }

    def directSendLogged(to: Int, amount: Int): Unit = {
      if (amount > 0) {
        defenders -= amount.toDouble
        cells(to).setIncome1Steep(amount)
        Console.err.println(s"sended: from $id to $to : $amount ")
//                Answer.add(s"MOVE $id ${shorterPath(to)} $amount")
        Answer.add(s"MOVE $id $to $amount")
      }
    }

    def send(to: Int, amount: Int): Unit = {
      if (amount > 0) {
        directSend(shorterPath(to), amount)
      }
    }

    def distance(to:Int):Int= {
      listOfNodes.find(item => item._1 == to)
        .map(_._2).getOrElse(10000)
    }


    def shorterPath(to: Int): Int = {
      val oldDistance = listOfNodes.find(item => (item._1 == to)).map(_._2).getOrElse(10000)
      val betterWayNodes = listOfNodes.map(cellId => cells(cellId._1))
        .find(_.listOfNodes.exists(item => (item._2 + cells(item._1).distance(to)) <= oldDistance))
      betterWayNodes match {
        case Some(x) => x.id
        case None => to
      }

    }

    def sendAttackBots(target: Int) = {
      if (defenders >= 1.0 && this.id != target) {
        val distance = listOfNodes.filter(_._1 == target).head._2
        if (atakAvailible > 0.0) {
//                    val needToAtak = cells(target).needToAttack(distance) -2
          send(target, (atakAvailible).toInt)

        }
      }
    }

    def atakAvailible = defenders + (if (incomingRobots > 0) 0 else incomingRobots)

    def requestDefend(ammount: Int) = {
      Console.err.println(s"request: to $id $ammount ${listOfNodes.size } ")
      var intermediatAmmount = ammount * (-1)
      listOfNodes
        .map(id => cells(id._1))
        .filter(_.owner == Config.ME)
        .filter(_.atakAvailible > 0)
        .foreach(cell => cell.directSendLogged(id, prepareToSend(cell)))

      def prepareToSend(cell: Cell) = {
        val result = if ((cell.atakAvailible - intermediatAmmount) > 0) intermediatAmmount else cell.atakAvailible.toInt
        intermediatAmmount -= result
        result
      }
    }

    def defend: Unit = {
      if (atakAvailible < 0.0) requestDefend(atakAvailible.toInt)


//            val defendAmount = this.incomingRobots * deffendCoeficient / 3.0
//            defendAmount match {
//                case x: Double if x >= 1.0 => listOfNodes.filter(item => item._1 == Config.ME).take(3).foreach(item => send(item._1, x.toInt))
//                case x: Double if x > 0.6 => listOfNodes.take(2).filter(item => item._1 == Config.ME).foreach(item => send(item._1, (((x * 3) + 0.1) / 2).toInt))
//                case x: Double if x > 0.3 => listOfNodes.filter(item => item._1 == Config.ME).take(1).foreach(item => send(item._1, 1))
//                case _ => Nil
//            }
    }

    def attack(target: Int) = {
      cells(target).mayDropBomb match {
        case true => sendBomb(target)
          sendAttackBots(target)
        case false => sendAttackBots(target)
      }
    }

    def setOwner(input: Double) = {
      owner = input
      owners(ownerCounter) = input
      ownerCounter += 1
      if (ownerCounter > 4) ownerCounter = 0
    }

    //        предварительно сократив общий выход на редьюс аутком
//        выход в таргет (50%), и 50% рандомно на остальные

    def increaseProduction = {
      defenders -= 10.0
      s"INC $id"
    }

    def reduceOutcome(input: Int) = {

    }

    def getAllNode() = {
      listOfNodes
    }

    def getROI = {
      ((defenders + 1.0) / production)
    }

    def getROI(distance: Double): Double = {
      owner match {
        case 0.0 => distance + getROI
        case -1.0 => distance + (((defenders + 1) + (production * distance)) / production)
        case 1.0 => 100000.0
      }
    }

    override def toString: String = s"id: $id owner: $owner defenders: $defenders ROI: $getROI ROIPERDIST: $roiPerDistance ${if (targetList.size > 3) "enemy:" + targetList.head._1 + " roi: " + targetList.head._2 }"
  }

  object BombDetector {
    var bomb1 = List[Int]()
    var bomb2 = List[Int]()
    var bomp1Arrival = 0
    var bomp2Arrival = 0

  }

  object Govorilka {
    var counter = 3
    var lastText = 0
    val data = Array("People come here for pain! For suffering!", "No tears please, it’s a waste of good suffering.", "Time to cause some screaming.", "I promise to kill you quickly when the time comes.", "I'll swallow your soul!", "SOSNOOOLEYY", "Sosimba Nagibimba", "I get so tired of watching. I want to start doing.", "Feel free to scream whenever you want.", "Never open portals to Hell. Deal with the consequences.", "The soup is made from tears, thickened by a nice roux.", "Metal scraping against bone sets my teeth on edge.", "today is good day to die", "Stand UP and fight like man", "DAVAY DAVAY NAAGIBAY", "RABOTAT' SUKI", "ATTACK!", "Attack lazy basters", "NO MERCY", "Let's go let's go LET'S GO-GO!!!")
    var dataIndex = 0

    def getNext: String = {
      counter match {
        case x: Int if x > 3 =>
          dataIndex = (math.random * data.size.toDouble).toInt
          if (math.random > 0.4) {
            lastText = dataIndex
            counter = 0
            "MSG " + data(dataIndex)
          }
          else ""
        case _ => counter = counter + 1
          "MSG " + data(dataIndex)
      }
    }
  }


  class Troop() {
    var owner = 0
    var from = 0
    var to = 0
    var attack = 0
    var distance = 0
  }

  def recalculateOwners = {
//        cells.filter(_.owner == Config.OPPONENT).foreach(cell => if (cell.needToAttack <= 0.0) cell.owner = Config.NOBODY)
//        cells.filter(_.owner == Config.ME).foreach(cell => if (cell.needToDefend <= 0.0) cell.owner = Config.OPPONENT)

  }

  def readGameData() = {
    cells.foreach(cell => {
      cell.totalIncome1Steep = 0.0
      cell.totalIncome3Steep = 0.0
      cell.totalIncome6Steep = 0.0
    })
    val entitycount = readInt
    for (i <- 0 until entitycount) {
      val Array(_entityid, entitytype, _arg1, _arg2, _arg3, _arg4, _arg5) = readLine split " "
      val entityid = _entityid.toInt
      val arg1 = _arg1.toDouble
      val arg2 = _arg2.toDouble
      val arg3 = _arg3.toDouble
      val arg4 = _arg4.toDouble
      val arg5 = _arg5.toDouble
      entitytype match {
        case "FACTORY" =>
          cells(entityid).setOwner(arg1)
          cells(entityid).defenders = arg2
          cells(entityid).production = arg1 match {
            case 0.0 => if (arg3 == 0.0) {
              cells(entityid).defenders += 10
              1.0
            } else arg3
            case 1.0 => if (arg2 > 10 && cells(entityid).owners.sum == 5.0 && arg3 < 3.0) Answer.add((cells(entityid).increaseProduction))
              arg3
            case _ => 0.01
          }
        case "TROOP" => arg5 match {
//                    case x: Double if (x <= 1.0) => cells(arg3.toInt).setIncome1Steep(arg4 * arg1)
//                    case x: Double if (x <= 3.0) => cells(arg3.toInt).setIncome3Steep(arg4 * arg1)
          case x: Double if (x <= 4.0) => cells(arg3.toInt).setIncome1Steep(arg4 * arg1)
          case _ =>
        }
        case _ =>
      }
    }
    recalculateOwners
    Config.firstRun = false
  }

  object Answer {
    var data: List[String] = List.empty

    def addFirst(input: String) = {
      data = List(input) ++ data

    }

    def add(input: String) = {
      data = data ++ List(input)
    }

    def send = {
      //            Console.err.println(s"data: ${data.mkString(";")}")
      val otvet = data.filter(_.size > 2)
      println(if (otvet.size > 0) otvet.mkString(";") else "WAIT")
      data = List.empty
    }

    override def toString: String = {
      data.mkString(";")
    }
  }

  def init(): String = {
    readGameData()
    var dostupnoRobotov = 0.0
    val otvet = cells.filter(cell => cell.owner == Config.ME)
      .flatMap(current => current.defenders match {
        case 0 => List.empty[String]
        case _ =>
          dostupnoRobotov = current.defenders
          val allNodes = current.getAllNode().sortBy(item => {
            cells(item._1).getROI(item._2.toDouble)
          })
            .map(item => if (current.defenders > cells(item._1).defenders) {
//                        Console.err.println(s"roi: ot ${current.id} dlia ${item._1} ${cells(item._1).getROI(item._2.toDouble)}")
              current.defenders = current.defenders - (cells(item._1).defenders + 1)
              s"MOVE ${current.id } ${current.shorterPath(item._1) } ${cells(item._1).defenders.toInt + 1 }"
            }
            else {
              if (current.defenders == 0) ""
              else {
                //                            Console.err.println(s"roi: ot ${current.id} dlia ${item._1} ${cells(item._1).getROI(item._2.toDouble)}")
                val otvet = s"MOVE ${current.id } ${current.shorterPath(item._1) } ${cells(item._1).defenders.toInt }"
                current.defenders = 0
                otvet
              }
            })
          allNodes
      }).filter(_.size > 2)

    if (otvet.size < 1) "WAIT" else otvet.mkString(";")
  }

  def calculateROI = {
    cells.filter(_.owner == Config.ME)
      .foreach(current => {
        val newTarget = current.getAllNode()
          .map(item => (item._1, cells(item._1).getROI(item._2.toDouble)))
          .sortBy(_._2)
        current.targetList = newTarget
//                    newTarget.foreach(item => Console.err.println(s"roi: ot ${current.id} dlia ${item._1} ${item._2} "))
      })


//                    getROI(item.get._2.toDouble))
  }

  def setupClasterCenter = {
    Config.clasterCenter = cells.find(_.owner == Config.ME).get.id
  }

  def recalculateWeights = {
    cells.filter(_.owner != -1.0)
      .foreach(current => current.targetList.isEmpty match {
        case true => Nil
        case false =>
          val enemy = current.targetList.head
          Console.err.println(s"RECALKULATE ot ${current.id } enemy: ${enemy._1 } ROI PROTIVNIKA ${enemy._2 } distance ${current.listOfNodes.filter(_._1 == enemy._1).head._2 } ")
          current.roi = enemy._2
          current.roiPerDistance = enemy._2 / current.listOfNodes.filter(_._1 == enemy._1).head._2
      })
  }

  def mainStrategy = {
    val otvet = cells.filter(cell => cell.owner == Config.ME)
      .foreach(current => {
        current.defend
        current.listOfNodes.map(item => cells(item._1))
          .filter(_.owner !=  Config.ME)
          .foreach(target => current.attack(target.id))

//                    current.defenders match {
//                    case 0 => List.empty[String]
//                    case _ =>
//                        current.attack(current.targetList(0)._1)
//                        current.defend
      }
      )
  }


  // ne atakovat' tuda kuda protivnik mojet takje bqstro dostignut

  Answer.add(init())
  Answer.add(Govorilka.getNext)
  Answer.send
  calculateROI
  Answer.add(init())
  Answer.add(Govorilka.getNext)
  Answer.send
  calculateROI
  Answer.add(init())
  Answer.add(Govorilka.getNext)
  Answer.send
  calculateROI
  Answer.add(init())
  Answer.add(Govorilka.getNext)
  Answer.send
//    recalculateWeights
  setupClasterCenter

  // game loop
  while (true) {


    readGameData
    calculateROI
//        recalculateWeights
//        cells.foreach(current => Console.err.println(s"cell №${current.id}: $current"))
    mainStrategy
//        makeDefence()
//        choose3Target()
    //    Answer.add(Govorilka.getNext)
    Answer.send
//        readGameData()
//        cells.foreach(item => Console.err.println((item.toString)))
//        val otvet = cells.filter(cell => cell.owner == Owner.ME)
//                .flatMap(current => current.getAllNode()
//                .sortBy(item => (item._2))
//                .map(node => s"MOVE ${current.id} ${node._1} 1"))
//        println(if (otvet.size < 2) "WAIT" else otvet.mkString(";") + Govorilka.getNext)
//        println(s"MOVE ${from.id} ${to.id} 100")
  }

}