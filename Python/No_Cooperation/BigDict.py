BigDict = {"Enemies":{}, "Pickups":{}, "WorldObjects":{}, "Players":{}, "Items":{}}
BigDict["Enemies"] = {"Hard":{}, "Medium":{}, "Easy":{}}
BigDict["Players"] = {"Unarmed":{}, "Knight":{}, "Ranger":{}, "Mage":{}}
BigDict["Pickups"] = {"Weapons":{"Ranged":{}, "Melee":{}, "Magic":{}}}
BigDict["WorldObjects"]={"Spawnpoints":[]}
#dictionary of enemies
BigDict["Enemies"]["Hard"] = {"CastleSlime":["slime00cas", 100, 10, 100, "random"],"LBomb":["bomb", 100, 10, 100, "random"], "SkeletonArcher": ["Skeleton Archer", 100, 15, 100, "range"], "ghost": ["ghost", 100, 20, 150, "chase"]}
BigDict["Enemies"]["Medium"] = {"DesertSlime":["slime00des", 100, 7, 75, "random"]}
BigDict["Enemies"]["Easy"] = {"Slime":["slime", 100, 5, 50, "random"]}
#Order of Attributes: Spritename, health, attack, speed, if follow(AI type)

#Dictionary of playable characters.
BigDict["Players"]["Unarmed"] = ["Unarmed", .75, .75]
BigDict["Players"]["Knight"] = ["Knight", 1, .75]
BigDict["Players"]["Ranger"] = ["Ranger", .75, 1]
BigDict["Players"]["Mage"] = ["Mage", 1, 1]
#Order of Attributes: Spritename, health, speed.
#health and speed will be multiplied by base class.
#Dictionary of pickups.
#--Weapons--#
#Order of Attributes: Spritename, attackType, Cooldown(Seconds), Power cooldown(Seconds), Damage, Power Damage, Range(pixels), Speed.
BigDict["Pickups"]["Weapons"]["Ranged"] = [["Bow", "proj", 0.5, 2.5, 0.75, 1.25, 1024, 1.0],
										   ["Crossbow", "proj", 0.75, 2.0, 1.25, 1.0, 512, 175],
										   ["Rifle", "proj", 0.75, 4.3, 1.4, 2.0, 1536, 2.2],
                                           ["Bomb", "Special", 1.0, 7.0, 2.5, 2.5, 256, 0.5]]

# The outer list is the direction in which the player is facing (W, E, N, S)
# The tuples inside that are the points for each frame
swordPtList = [ [[(-68, -23), (-48, -23)], [(-79, -23), (-58, -23)], [(-88, -23), (-68, -23)], [(-68, -23), (-48, -23)]],   #swordPtList[0]
				[[(69,-23), (49, -23)], [(90,-23), (70, -23)], [(80,-23), (60, -23)], [(74,-23), (54, -23)]],               #swordPtList[1]
                [[(28, -80), (28, -60)], [(28, -99), (28, -79)], [(28, -94), (28, -74)], [(28, -85), (28, -65)]],           #swordPtList[2]
				[[(-28, 38), (-28, 18)], [(-28, 56), (-28, 36)], [(-28, 51), (-28, 31)], [(-28, 39), (-28, 19)]] ]          #swordPtList[3]

scythePtList = [ [[(-30,-59), (-60, -29)], [(-30,-59), (-60, -29)], [(-30,-59), (-60, -29)], [(-30,-59), (-60, -29)]],      #scythePtList[0]
				 [[(34,-59), (64, -29)], [(34,-59), (64, -29)], [(34,-59), (64, -29)], [(34,-59), (64, -29)]],              #scythePtList[1]
                 [[(23,-70), (-13, -100)], [(23,-70), (-13, -100)], [(23,-70), (-13, -100)], [(23,-70), (-13, -100)]],      #scythePtList[2]
				 [[(-23, 16), (7, 36)], [(-23, 16), (7, 36)], [(-23, 16), (7, 36)], [(-23, 16), (7, 36)]] ]                 #scythePtList[3]

BigDict["Pickups"]["Weapons"]["Melee"] =  [["Sword", "stab", 0.6, 3, 1.0, 1.5, 0.0, 0.0, swordPtList],
                                           ["StrongSword", "stab", 0.6, 3, 2.0, 3.0, 0.0, 0.0, swordPtList],
										   ["Scythe", "arc", 0.75, 5.1, 1.8, 2.5, 0.0, 0.0, scythePtList],
										   ["Axe", "stab", 0.75, 4.5, 1.5, 1.75, 0.0, 0.0],
										   ["Spear", "stab", 0.65, 4.4, 1.6, 2.0, 0.0, 0.0]]

BigDict["Pickups"]["Weapons"]["Magic"] =  [["MagicStaff", "proj", 0.75, 2.0, 1.0, 2.0, 1024, 0.6],
                                           ["FireStaff", "proj", 0.75, 2.0, 1.0, 1.5, 1024, 0.6],
                                           ["LightningStaff", "proj", 0.75, 2.0, 1.0, 1.5, 1024, 0.6],
                                           ["EarthStaff", "proj", 0.75, 2.0, 1.0, 1.0, 1024, 0.6],
                                           ["DoomStaff", "Special", 0.75, 2.5, 1.4, 2.5, 1024, 0.6]]

#--Pickups--#
BigDict["Pickups"]["Compass"] = ["Compass", True]
#Order of Attributes: Spritename, Boolean set to true.



BigDict["Items"]["HealthPot"] = ["Potion_RedPU", "heal", 30]
#BigDict["Items"]["Sword"] = ["Claymore", "changeClass", ("Melee", BigDict["Pickups"]["Weapons"]["Melee"][0])]
BigDict["Items"]["Staff"] = ["staffPU", "changeClass", ("Magic", BigDict["Pickups"]["Weapons"]["Magic"][0])]
BigDict["Items"]["Scythe"] = ["ScythePU", "changeClass", ("Melee", BigDict["Pickups"]["Weapons"]["Melee"][2])]
BigDict["Items"]["Bow"] = ["BowPU", "changeClass", ("Ranged", BigDict["Pickups"]["Weapons"]["Ranged"][0])]
BigDict["Items"]["StrongSword"] = ["ClaymorePU", "changeClass", ("Melee", BigDict["Pickups"]["Weapons"]["Melee"][1])]


