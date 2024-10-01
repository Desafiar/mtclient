import app
import chr
import chrmgr
import skill
import net
import item
import player
import effect
import constinfo
import localeinfo
import emotion

JOB_WARRIOR = 0
JOB_ASSASSIN = 1
JOB_SURA = 2
JOB_SHAMAN = 3

RACE_WARRIOR_M = 0
RACE_ASSASSIN_W = 1
RACE_SURA_M = 2
RACE_SHAMAN_W = 3
RACE_WARRIOR_W = 4
RACE_ASSASSIN_M = 5
RACE_SURA_W = 6
RACE_SHAMAN_M = 7

FACE_IMAGE_DICT = {
	RACE_WARRIOR_M : "d:/ymir work/ui/game/windows/face_warrior.sub",
	RACE_ASSASSIN_W : "d:/ymir work/ui/game/windows/face_assassin.sub",
	RACE_SURA_M : "d:/ymir work/ui/game/windows/face_sura.sub",
	RACE_SHAMAN_W : "d:/ymir work/ui/game/windows/face_shaman.sub",
}

PASSIVE_GUILD_SKILL_INDEX_LIST = ( 151, )
ACTIVE_GUILD_SKILL_INDEX_LIST = ( 152, 153, 154, 155, 156, 157, )

# instead of the relative app.NEW_678TH_SKILL_ENABLE
NEW_678TH_SKILL_ENABLE = constinfo.NEW_678TH_SKILL_ENABLE
SKILL_INDEX_DICT = []

def DefineSkillIndexDict():
	global NEW_678TH_SKILL_ENABLE
	global SKILL_INDEX_DICT
	
	if app.ENABLE_NEW_PASSIVE_SKILLS:
		passiveBoost = (236, 240, 237, 241, 238, 242, 239, 243)
	else:
		passiveBoost = (0, 0, 0, 0, 0, 0, 0, 0)
	
	SKILL_INDEX_DICT = {
		JOB_WARRIOR : {
			1 : (1, 2, 3, 4, 5, 6, passiveBoost[0], 0, 137, 0, 138, 0, 139, 0,),
			2 : (16, 17, 18, 19, 20, 21, passiveBoost[1], 0, 137, 0, 138, 0, 139, 0,),
			"SUPPORT" : (122, 123, 121, 124, 125, 0, 0, 0, 130, 131, 0, 0,),
		},
		JOB_ASSASSIN : {
			1 : (31, 32, 33, 34, 35, 36, passiveBoost[2], 0, 137, 0, 138, 0, 139, 0, 140,),
			2 : (46, 47, 48, 49, 50, 51, passiveBoost[3], 0, 137, 0, 138, 0, 139, 0, 140,),
			"SUPPORT" : (122, 123, 121, 124, 125, 0, 0, 0, 130, 131, 0, 0,),
		},
		JOB_SURA : {
			1 : (61, 62, 63, 64, 65, 66, passiveBoost[4], 0, 137, 0, 138, 0, 139, 0,),
			2 : (76, 77, 78, 79, 80, 81, passiveBoost[5], 0, 137, 0, 138, 0, 139, 0,),
			"SUPPORT" : (122, 123, 121, 124, 125, 0, 0, 0, 130, 131, 0, 0,),
		},
		JOB_SHAMAN : {
			1 : (91, 92, 93, 94, 95, 96, passiveBoost[6], 0, 137, 0, 138, 0, 139, 0,),
			2 : (106, 107, 108, 109, 110, 111, passiveBoost[7], 0, 137, 0, 138, 0, 139, 0,),
			"SUPPORT" : (122, 123, 121, 124, 125, 0, 0, 0, 130, 131, 0, 0,),
		},
	}

def RegisterSkill(race, group, empire=0):

	DefineSkillIndexDict()

	job = chr.RaceToJob(race)

	## Character Skill
	if app.ENABLE_NEW_PASSIVE_SKILLS:
		passiveDefense = (221, 222, 223, 224, 225, 226, 227, 228)
		for i in xrange(len(passiveDefense)):
			player.SetSkill(i+221, passiveDefense[i])
	
	if SKILL_INDEX_DICT.has_key(job):
		if SKILL_INDEX_DICT[job].has_key(group):

			activeSkillList = SKILL_INDEX_DICT[job][group]

			for i in xrange(len(activeSkillList)):
				skillIndex = activeSkillList[i]

				## 7번 8번 스킬은 여기서 설정하면 안됨
				if i != 6 and i != 7 and not app.ENABLE_NEW_PASSIVE_SKILLS:
					player.SetSkill(i+1, skillIndex)
				else:
					player.SetSkill(i+1, skillIndex)

			if app.ENABLE_NEW_SECONDARY_SKILLS:
				supportSkillList = (122, 123, 121, 130, 131, 143, 144, 145, 146, 0, 0, 0,)
			else:
				supportSkillList = SKILL_INDEX_DICT[job]["SUPPORT"]

			for i in xrange(len(supportSkillList)):
				player.SetSkill(i+100+1, supportSkillList[i])

	## Language Skill
	if 0 != empire and not app.ENABLE_NEW_SECONDARY_SKILLS:
		languageSkillList = []
		for i in xrange(3):
			if (i+1) != empire:
				languageSkillList.append(player.SKILL_INDEX_LANGUAGE1+i)
		for i in xrange(len(languageSkillList)):
			player.SetSkill(107+i, languageSkillList[i])

	## Guild Skill
	for i in xrange(len(PASSIVE_GUILD_SKILL_INDEX_LIST)):
		player.SetSkill(200+i, PASSIVE_GUILD_SKILL_INDEX_LIST[i])

	for i in xrange(len(ACTIVE_GUILD_SKILL_INDEX_LIST)):
		player.SetSkill(210+i, ACTIVE_GUILD_SKILL_INDEX_LIST[i])

def __LoadGameSkill():
	try:
		skill.LoadSkillData()
	except:
		import exception
		exception.Abort("__LoadGameSkill")

def __LoadGameEnemy():
	pass

def __LoadGameNPC():
	try:
		lines = open("data/monsters/npclist.txt", "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("LoadLocaleError(%(srcFileName)s)" % locals())
		app.Abort()

	for line in lines:
		tokens = line[:-1].split("\t")
		if len(tokens) == 0 or not tokens[0]:
			continue

		try:
			vnum = int(tokens[0])
		except ValueError:
			import dbg
			dbg.LogBox("LoadGameNPC() - %s - line #%d: %s" % (tokens, lines.index(line), line))
			app.Abort()

		try:
			if vnum:
				chrmgr.RegisterRaceName(vnum, tokens[1].strip())
			else:
				chrmgr.RegisterRaceSrcName(tokens[1].strip(), tokens[2].strip())
		except IndexError:
			import dbg
			dbg.LogBox("LoadGameNPC() - %d, %s - line #%d: %s " % (vnum, tokens, lines.index(line), line))
			app.Abort()


# GUILD_BUILDING
def LoadGuildBuildingList(filename):
	import uiguild
	uiguild.BUILDING_DATA_LIST = []

	handle = app.OpenTextFile(filename)
	count = app.GetTextFileLineCount(handle)
	for i in xrange(count):
		line = app.GetTextFileLine(handle, i)
		tokens = line.split("\t")

		TOKEN_VNUM = 0
		TOKEN_TYPE = 1
		TOKEN_NAME = 2
		TOKEN_LOCAL_NAME = 3
		NO_USE_TOKEN_SIZE_1 = 4
		NO_USE_TOKEN_SIZE_2 = 5
		NO_USE_TOKEN_SIZE_3 = 6
		NO_USE_TOKEN_SIZE_4 = 7
		TOKEN_X_ROT_LIMIT = 8
		TOKEN_Y_ROT_LIMIT = 9
		TOKEN_Z_ROT_LIMIT = 10
		TOKEN_PRICE = 11
		TOKEN_MATERIAL = 12
		TOKEN_NPC = 13
		TOKEN_GROUP = 14
		TOKEN_DEPEND_GROUP = 15
		TOKEN_ENABLE_FLAG = 16
		LIMIT_TOKEN_COUNT = 17

		if not tokens[TOKEN_VNUM].isdigit():
			continue

		if len(tokens) < LIMIT_TOKEN_COUNT:
			import dbg
			dbg.TraceError("Strange token count [%d/%d] [%s]" % (len(tokens), LIMIT_TOKEN_COUNT, line))
			continue

		ENABLE_FLAG_TYPE_NOT_USE = False
		ENABLE_FLAG_TYPE_USE = True
		ENABLE_FLAG_TYPE_USE_BUT_HIDE = 2

		if ENABLE_FLAG_TYPE_NOT_USE == int(tokens[TOKEN_ENABLE_FLAG]):
			continue

		vnum = int(tokens[TOKEN_VNUM])
		type = tokens[TOKEN_TYPE]
		name = tokens[TOKEN_NAME]
		localName = tokens[TOKEN_LOCAL_NAME]
		xRotLimit = int(tokens[TOKEN_X_ROT_LIMIT])
		yRotLimit = int(tokens[TOKEN_Y_ROT_LIMIT])
		zRotLimit = int(tokens[TOKEN_Z_ROT_LIMIT])
		price = tokens[TOKEN_PRICE]
		material = tokens[TOKEN_MATERIAL]

		folderName = ""
		if "HEADQUARTER" == type:
			folderName = "headquarter"
		elif "FACILITY" == type:
			folderName = "facility"
		elif "OBJECT" == type:
			folderName = "object"
		elif "WALL" == type:
			folderName = "fence"

		materialList = ["0", "0", "0"]
		if material:
			if material[0] == "\"":
				material = material[1:]
			if material[-1] == "\"":
				material = material[:-1]
			for one in material.split("/"):
				data = one.split(",")
				if 2 != len(data):
					continue
				itemID = int(data[0])
				count = data[1]

				if itemID == uiguild.MATERIAL_STONE_ID:
					materialList[uiguild.MATERIAL_STONE_INDEX] = count
				elif itemID == uiguild.MATERIAL_LOG_ID:
					materialList[uiguild.MATERIAL_LOG_INDEX] = count
				elif itemID == uiguild.MATERIAL_PLYWOOD_ID:
					materialList[uiguild.MATERIAL_PLYWOOD_INDEX] = count

		## GuildSymbol 은 일반 NPC 들과 함께 등록한다.
		import chrmgr
		chrmgr.RegisterRaceSrcName(name, folderName)
		chrmgr.RegisterRaceName(vnum, name)

		appendingData = { "VNUM":vnum,
						  "TYPE":type,
						  "NAME":name,
						  "LOCAL_NAME":localName,
						  "X_ROT_LIMIT":xRotLimit,
						  "Y_ROT_LIMIT":yRotLimit,
						  "Z_ROT_LIMIT":zRotLimit,
						  "PRICE":price,
						  "MATERIAL":materialList,
						  "SHOW" : True }

		if ENABLE_FLAG_TYPE_USE_BUT_HIDE == int(tokens[TOKEN_ENABLE_FLAG]):
			appendingData["SHOW"] = False

		uiguild.BUILDING_DATA_LIST.append(appendingData)

	app.CloseTextFile(handle)

# END_OF_GUILD_BUILDING

loadGameDataDict={
	"SKILL" : __LoadGameSkill,
	"ENEMY" : __LoadGameEnemy,
	"NPC" : __LoadGameNPC,
}

if app.ENABLE_RACE_HEIGHT:
	def __LoadRaceHeight():
		try:
			lines = open("data/monsters/race_height.txt", "r").readlines()
		except IOError:
			return
		
		for line in lines:
			tokens = line[:-1].split("\t")
			if len(tokens) == 0 or not tokens[0]:
				continue
			
			vnum = int(tokens[0])
			height = float(tokens[1])
			riding = float(tokens[2])
			
			chrmgr.SetRaceHeight(vnum, height, riding)
	
	loadGameDataDict.update({"RACE_HEIGHT" :  __LoadRaceHeight,})

def LoadGameData(name):
	global loadGameDataDict

	load=loadGameDataDict.get(name, 0)
	if load:
		loadGameDataDict[name]=0
		try:
			load()
		except:
			print name
			import exception
			exception.Abort("LoadGameData")
			raise


## NPC

def SetMovingNPC(race, name):
	chrmgr.CreateRace(race)
	chrmgr.SelectRace(race)

	## RESERVED
	chrmgr.SetPathName("d:/ymir work/npc/" + name + "/")
	chrmgr.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, "wait.msa")
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WALK, "walk.msa")
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_RUN, "run.msa")
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DEAD, "die.msa")
	chrmgr.LoadRaceData(name + ".msm")

def SetOneNPC(race, name):
	chrmgr.CreateRace(race)
	chrmgr.SelectRace(race)

	## RESERVED
	chrmgr.SetPathName("d:/ymir work/npc/" + name + "/")
	chrmgr.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, "wait.msa")
	chrmgr.LoadRaceData(name + ".msm")

def SetGuard(race, name):
	chrmgr.CreateRace(race)
	chrmgr.SelectRace(race)

	## Script Data
	chrmgr.SetPathName("d:/ymir work/npc/" + name + "/")
	chrmgr.LoadRaceData(name + ".msm")

	## GENERAL
	chrmgr.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SPAWN,		"00.msa")
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT,			"00.msa")
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_RUN,			"03.msa")

	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE,		"30.msa", 50)
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE,		"30_1.msa", 50)

	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE_BACK,	"34.msa", 50)
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE_BACK,	"34_1.msa", 50)

	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE_FLYING,"32.msa")
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_STAND_UP,		"33.msa")

	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE_FLYING_BACK,	"35.msa")
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_STAND_UP_BACK,		"36.msa")

	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DEAD,					"31.msa")
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DEAD_BACK,			"37.msa")

	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_NORMAL_ATTACK,		"20.msa")

	## Attacking Data
	chrmgr.RegisterNormalAttack(chr.MOTION_MODE_GENERAL, chr.MOTION_NORMAL_ATTACK)

def SetWarp(race):
	chrmgr.CreateRace(race)
	chrmgr.SelectRace(race)

	chrmgr.SetPathName("d:/ymir work/npc/warp/")
	chrmgr.LoadRaceData("warp.msm")

	## GENERAL
	chrmgr.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, "wait.msa")

def SetDoor(race, name):
	chrmgr.CreateRace(race)
	chrmgr.SelectRace(race)
	chrmgr.SetPathName("d:/ymir work/npc/"+name+"/")
	chrmgr.LoadRaceData(name + ".msm")
	chrmgr.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, "close_wait.msa")
	chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DEAD, "open.msa")

def SetGuildBuilding(race, name, grade):
	chrmgr.CreateRace(race)
	chrmgr.SelectRace(race)
	chrmgr.SetPathName("d:/ymir work/guild/building/%s/" % name)
	chrmgr.LoadRaceData("%s%02d.msm" % (name, grade))
	chrmgr.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	#chrmgr.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DEAD, name + "_destruction.msa")

def OLD_SetNPC():
	SetOneNPC(9001, "arms")
	SetOneNPC(9002, "defence")
	SetOneNPC(9003, "goods")
	SetOneNPC(9004, "bank")
	SetOneNPC(9005, "hotel_grandfa")
	SetOneNPC(9006, "hotel_grandma")
	SetOneNPC(9007, "arms")
	SetOneNPC(9008, "defence")
	SetOneNPC(9009, "sailor")

	SetMovingNPC(20001, "alchemist")
	SetMovingNPC(20002, "auntie")
	SetMovingNPC(20003, "baby_and_mom")
	SetMovingNPC(20004, "beggar")
	SetMovingNPC(20005, "ceramist")
	SetMovingNPC(20006, "girl_lost_elder_brother")
	SetMovingNPC(20007, "hotel_grandfa")
	SetMovingNPC(20008, "mr_restaurant")
	SetMovingNPC(20009, "oldster")
	SetMovingNPC(20010, "peddler")
	SetMovingNPC(20011, "plant_researcher")
	SetMovingNPC(20012, "rice_cake_seller")
	SetMovingNPC(20013, "sailor")
	SetMovingNPC(20014, "timid_boy")
	SetMovingNPC(20015, "woodcutter")
	SetMovingNPC(20016, "blacksmith")
	SetMovingNPC(20017, "musician")
	SetMovingNPC(20018, "doctor")
	SetMovingNPC(20019, "hunter")
	SetMovingNPC(20020, "old_pirate")
	SetMovingNPC(20021, "widow")
	SetMovingNPC(20022, "young_merchant")
	SetMovingNPC(20023, "bookworm")
	SetMovingNPC(20024, "yu_hwa_rang")
	SetMovingNPC(20041, "beggar")
	SetMovingNPC(20042, "peddler")

	SetGuard(20300, "sinsu_patrol_spear")
	SetGuard(20301, "sinsu_patrol_spear")
	SetGuard(20302, "sinsu_patrol_spear")
	SetGuard(20303, "sinsu_patrol_spear")
	SetGuard(20304, "sinsu_patrol_spear")
	SetGuard(20305, "sinsu_patrol_spear")
	SetGuard(20306, "sinsu_patrol_spear")
	SetGuard(20307, "sinsu_patrol_spear")

	SetGuard(20320, "gangyo_patrol_spear")
	SetGuard(20321, "gangyo_patrol_spear")
	SetGuard(20322, "gangyo_patrol_spear")
	SetGuard(20323, "gangyo_patrol_spear")
	SetGuard(20324, "gangyo_patrol_spear")
	SetGuard(20325, "gangyo_patrol_spear")
	SetGuard(20326, "gangyo_patrol_spear")
	SetGuard(20327, "gangyo_patrol_spear")

	SetGuard(20340, "jinno_patrol_spear")
	SetGuard(20341, "jinno_patrol_spear")
	SetGuard(20342, "jinno_patrol_spear")
	SetGuard(20343, "jinno_patrol_spear")
	SetGuard(20344, "jinno_patrol_spear")
	SetGuard(20345, "jinno_patrol_spear")
	SetGuard(20346, "jinno_patrol_spear")
	SetGuard(20347, "jinno_patrol_spear")

	## Warp
	for i in xrange(18):
		SetWarp(10001 + i)

	SetGuard(11000, "gangyo_patrol_spear")
	SetGuard(11001, "gangyo_patrol_bow")
	SetGuard(11002, "jinno_patrol_spear")
	SetGuard(11003, "jinno_patrol_bow")
	SetGuard(11004, "sinsu_patrol_spear")
	SetGuard(11005, "sinsu_patrol_bow")

	## Campfire (Bonfire)
	chrmgr.CreateRace(12000)
	chrmgr.SelectRace(12000)
	chrmgr.SetPathName("d:/ymir Work/npc/campfire/")
	chrmgr.LoadRaceData("campfire.msm")

	## Door
	SetDoor(13000, "wooden_door")
	SetDoor(13001, "stone_door")
