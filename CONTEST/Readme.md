<div class="statement-expert-rules-content">
                <br>

                <p><strong>Collisions</strong><br>
                    <br>

                    There are no collisions between entities.</p><br>

                <p><strong>Round types</strong><br>
                    <br>

                    There are two different types of turns in this game.
<br><br>
                    The first one is for hero picks and occurs at the beginning of the game.  When the input variable <var>roundType</var> is negative, you must output the name of the hero you want to play. If you output <action> WAIT </action> instead of a hero name, a hero will be selected for you.
<br>
                    <br>The second type of turn is a normal game turn where you have to fight your way towards the win conditions. <var>roundType</var> will be positive and its value will represent the amount of heroes that you have to order.</p><br>

                <p><strong>Game Entities: Units / Heroes / Towers / Neutral Creatures</strong><br>
                    <br>

                    Every entity has the following attributes:<br>
                </p><ul><li><var>unitId</var></li><li><var>team</var> - the team they belong to</li><li><var>type</var> - it can be an Unit / Hero / Tower / Groot(Neutral Unit)</li><li><var>attackRange</var> - the distance from which entities can attack</li><li><var>health</var> - the current amount of damage they can take before they die</li><li><var>mana</var> - the current amount of mana they have available to perform their skills</li><li><var>attack_damage</var> - the amount of damage they can deal with an <action>ATTACK</action> command</li><li><var>movement_speed</var> - the distance they can travel in a single turn. An entity will stop where it arrives and won't travel any further until the following round.</li><li><br>
Entities also have <var>maxHealth</var> and <var>maxMana</var>. These represent the maximum values of <var>health</var> and <var>mana</var> they can have.
<br><br>
Towers are stationary. They do not move. Ever.
                </li></ul><p></p><br>

                <p><strong>Spawn Locations</strong><br>
                    <br>


                    Hero for player 0 spawns at:<br>
                    x: <const>200</const>, y: <const>590</const><br>
                    Hero for player 1 spawns at:<br>
                    x: <const>1720</const>, y: <const>590</const><br>
                </p><br>


                <p><strong>Hero stats</strong><br>
                    <br>


                </p><table style="width:100%;border:1px solid white"><tbody><tr><th>Name</th><th>Stats</th></tr><tr><td>Deadpool</td><td><ul><li>health 1380</li><li>mana 100</li><li>damage 80</li><li>move speed 200</li><li>mana regen 1</li><li>attackRange 110</li></ul></td></tr><tr><td>Doctor Strange</td><td><ul><li>health 955</li><li>mana 300</li><li>damage 50</li><li>move speed 200</li><li>mana regen 2</li><li>attackRange 245</li></ul></td></tr><tr><td>Hulk</td><td><ul><li>health 1450</li><li>mana 90</li><li>damage 80</li><li>move speed 200</li><li>mana regen 1</li><li>attackRange 95</li></ul></td></tr><tr><td>Ironman</td><td><ul><li>health 820</li><li>mana 200</li><li>damage 60</li><li>move speed 200</li><li>mana regen 2</li><li>attackRange 270</li></ul></td></tr><tr><td>Valkyrie</td><td><ul><li>health 1400</li><li>mana 155</li><li>damage 65</li><li>move speed 200</li><li>mana regen 2</li><li>attackRange 130</li></ul></td></tr></tbody></table>

               <br>

                <p><strong>Attacking</strong><br>

                    <br>

Heroes have an attack time of 0.1 and units have an attack time of 0.2<br><br>

Ranged units require an additional attack time * distance / <var>attackRange</var> for their projectiles to hit the target. <br><br>

A unit or hero is ranged if their attack <var>attackRange</var> is greater than 150.<br><br>

If a unit is out of range, your hero will first move closer towards the target and then try to attack it. This helps a lot if you're only slightly out of range.<br><br>

The time used to move is distance / <var>moveSpeed</var> <br><br>

So if your hero has <const>75</const> range and travels a distance of <const>100</const> on the map, at <const>200</const> <var>moveSpeed</var>, it uses up <const>100</const> / <const>200</const> = <const>0.5</const> turn time and still has half the turn left to attack. The attack will take place at <const>0.5</const> + <const>0.1</const> since the hero is melee in this case.<br><br>
The distance to the unit still needs to be equal or smaller to the hero's range for the attack to take place.<br><br>
Attacks with an attack time higher than 1 don't carry over to the next round.<br><br>

<action>ATTACK_NEAREST</action> <var>unitType</var> : works like a regular attack command, except it attacks nearest entity of given type.<br>
<action>MOVE_ATTACK x y </action>  <var>unitId</var> : your hero first moves to target location and then executes the attack, only if enough time is left during the current round to hit the target and if the target is within <var>attackRange</var>.

                </p><br>



                <p><strong>Lane units aggro and attack pattern</strong><br>
                    <br>

                    If your hero attacks an enemy hero while his allied units are around him, these units will follow and attack your hero. This is called aggro. The attacking hero needs to be within 300 distance to the enemy units for this to take effect and it's canceled if the hero moves out of this range. Unit aggro lasts for 3 rounds, including the initial round.<br><br>

Lane units will always first try to hit the hero that aggroed them.<br><br>

If not aggroed, units move straight towards the enemy tower from their current location. <br>
On their way they always stop to hit the closest unit from the enemy <var>team</var>, if the enemy is within <var>attackRange</var>.<br>
- If multiple targets are at the same distance, the lowest <var>health</var> enemy is selected.<br>
- Then the enemy with highest <var>y</var> coordinate in their location is selected.<br>
- And last the enemy with lowest <var>unitId</var> is selected.</p><br>


                <p><strong>Tower aggro and attack pattern</strong><br>
                    <br>
The tower will attack in the following order:
<br><br>
First targets any enemy hero that attacks an allied hero.<br>
Targets closest enemy unit within range.<br>
Targets closest enemy hero.<br>
<br><br>
Using spells or hitting the tower, doesn't force tower aggro.
                    </p><br>


                    <p><strong>Gold rewards</strong><br>
                    <br>

</p><table style="width:100%;border:1px solid white"><tbody><tr><th>
Entity Type
</th><th>
Gold Reward
</th></tr><tr><td>
Melee Unit
</td><td>
30
</td></tr><tr><td>
Ranged Unit
</td><td>
50
</td></tr><tr><td>
Hero
</td><td>
300
</td></tr></tbody></table>

                    <br>

                <p><strong>General information</strong><br>
                    <br>

                    Overall it looks complex, but it's very simple and fun.</p><br>


            </div>