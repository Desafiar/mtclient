#! /usr/bin/env python
__author__		= 'VegaS'
__date__		= '2020.01.19'
__name__		= 'PlayerSettingsModule - Renewal'
__version__		= '4.3'

import app, chrmgr

JOB_WARRIOR, JOB_ASSASSIN, JOB_SURA, JOB_SHAMAN, JOB_WOLFMAN = range(5)
RACE_WARRIOR_M, RACE_ASSASSIN_W, RACE_SURA_M, RACE_SHAMAN_W, RACE_WARRIOR_W, RACE_ASSASSIN_M, RACE_SURA_W, RACE_SHAMAN_M, RACE_WOLFMAN_M = range(9)

PASSIVE_GUILD_SKILL_INDEX_LIST = ( 151, )
ACTIVE_GUILD_SKILL_INDEX_LIST = ( 152, 153, 154, 155, 156, 157, )

FACE_IMAGE_DICT = {
	RACE_WARRIOR_M	: "d:/ymir work/ui/game/windows/face_warrior.sub",
	RACE_ASSASSIN_W	: "d:/ymir work/ui/game/windows/face_assassin.sub",
	RACE_SURA_M	: "d:/ymir work/ui/game/windows/face_sura.sub",
	RACE_SHAMAN_W	: "d:/ymir work/ui/game/windows/face_shaman.sub",
}

FACE_DICT = {
	RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	RACE_SURA_M		: "icon/face/sura_m.tga",
	RACE_SURA_W		: "icon/face/sura_w.tga",
	RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}

def LoadRaceHeight():
	try:
		lines = open("race_height.txt", "r").readlines()
	except IOError:
		return

	for line in lines:
		tokens = line[:-1].split("\t")
		if len(tokens) == 0 or not tokens[0]:
			continue

		chrmgr.SetRaceHeight(int(tokens[0]), float(tokens[1]))

isInitData=0


def __InitData():
	global isInitData

	if isInitData:
		return			

	isInitData = 1
		## paste your code here

# GUILD_BUILDING
def LoadGuildBuildingList(filename):
	import uiGuild
	uiGuild.BUILDING_DATA_LIST = []

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

				if itemID == uiGuild.MATERIAL_STONE_ID:
					materialList[uiGuild.MATERIAL_STONE_INDEX] = count
				elif itemID == uiGuild.MATERIAL_LOG_ID:
					materialList[uiGuild.MATERIAL_LOG_INDEX] = count
				elif itemID == uiGuild.MATERIAL_PLYWOOD_ID:
					materialList[uiGuild.MATERIAL_PLYWOOD_INDEX] = count

		## GuildSymbol
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

		uiGuild.BUILDING_DATA_LIST.append(appendingData)

	app.CloseTextFile(handle)

loadGameDataDict={
	"INIT" : __InitData,
}



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