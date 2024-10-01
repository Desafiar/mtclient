import app
import net
import chrmgr
import player
import item
import os
import chat
import localeInfo

# EXTRA BEGIN
# loads 5 (B,M,G,P,F) skills .mse
ENABLE_NEW_LEVELSKILL_SYSTEM = 0
# don't set a random channel when you open the client
ENABLE_RANDOM_CHANNEL_SEL = 0
# don't remove id&pass if the login attempt fails
ENABLE_CLEAN_DATA_IF_FAIL_LOGIN = 0
# ctrl+v will now work
ENABLE_PASTE_FEATURE = 0
# display all the bonuses added by a stone instead of the first one
ENABLE_FULLSTONE_DETAILS = 1
# enable successfulness % in the refine dialog
ENABLE_REFINE_PCT = 0
# extra ui features
EXTRA_UI_FEATURE = 1
ADDPERCENT = 0
WND_EVENT = None

## AUTO LOGIN"
LOGIN_UI_MODIFY = False # Login countdown


if app.ENABLE_ZODIAC_MISSION:
	ZodiacLua=0

if app.ENABLE_DISCORD_STUFF:
	msgname = ""

if app.ENABLE_FEATURES_OXEVENT:
	if not os.path.exists("lib\item_proto_list.py"):
		fileName = file("lib\item_proto_list.py", "w")

_game_instance = None

def GetGameInstance():
	global _game_instance
	return _game_instance

def SetGameInstance(instance):
	global _game_instance
	if _game_instance:
		del _game_instance
	_game_instance = instance

# def GetInterfaceInstance():
# 	global _game_instance
# 	if _game_instance:
# 		return _game_instance.interface
# 	return None

if app.ENABLE_PVP_TOURNAMENT:
	_interface_instance = None
	def GetInterfaceInstance():
		global _interface_instance
		return _interface_instance

	def SetInterfaceInstance(instance):
		global _interface_instance
		if _interface_instance:
			del _interface_instance
		_interface_instance = instance

if app.ENABLE_WIKI:
	_main_wiki_instance = None
	_listbox_wiki_instance = None
	def SetMainParent(instance):
		global _main_wiki_instance
		if _main_wiki_instance:
			del _main_wiki_instance
		_main_wiki_instance = instance
	def GetMainParent():
		global _main_wiki_instance
		return _main_wiki_instance
	def SetListBox(instance):
		global _listbox_wiki_instance
		if _listbox_wiki_instance:
			del _listbox_wiki_instance
		_listbox_wiki_instance = instance
	def GetListBox():
		global _listbox_wiki_instance
		return _listbox_wiki_instance
	def IS_SET(value, flag):
		return (value & flag) == flag


if app.ENABLE_DUNGEON_INFO:
	DungeonWarp = ""
	dungeon_qf_index = 0
	py_Flag = {}
	def GetFlag(flagname):
		global py_Flag
		return py_Flag.get(flagname, 0)
	def SetFlag(flagname,value):
		global py_Flag
		py_Flag[flagname] = value
	def take_first(elem):
		return elem[1]
	def CalculateDungeonList(data):
		newList = sorted(data, key=take_first)
		return newList
def minutetoday(time):
	return int(int((time / 60) / 60) / 24)
def minutetohour(time):
	return int((time / 60) / 60) % 24
def minutetominute(time):
	return int((time / 60) % 60)
def minutetosecond(time):
	return int(time % 60)
	
if app.ENABLE_OFFLINESHOP_SYSTEM:
	#SHOPNAMES_RANGE = 2500
	MAX_SHOP_TYPE = 13
	MAX_SHOP_TITLE = 6
	def NumberToString(n) :
		if n <= 0 :
			return "0"
		return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))
	def IS_SET(value, flag):
		return (value & flag) == flag
	def SET_BIT(value, bit):
		return value | (bit)
	def REMOVE_BIT(value, bit):
		return value & ~(bit)
	def getFlagValue(value):
		return 1 << value
	
	def getInjectCheck(text):
		words = ["SELECT", "TRUNCATE", "INSERT", "REPLACE", "DELETE", "ALTER", "DROP",";", ":", "*", "'", '"', "="]
		characters = []
		for word in words:
			if text.find(word) != -1:
				return True
		return False
			
if app.ENABLE_NEW_PET_SYSTEM:
	def getInjectCheck(text):
		words = ["SELECT", "TRUNCATE", "INSERT", "REPLACE", "DELETE", "ALTER", "DROP",";", ":", "*", "'", '"', "="]
		characters = []
		for word in words:
			if text.find(word) != -1:
				return True
		return False
	PET_BONUS_MAX_LEVEL = 20.0
	PET_SKILL_MAX_LEVEL = 20.0

	petEvolutionLimits = [40, 75, 100, 120]
	pet_bonus_types=[item.APPLY_MAX_HP,item.APPLY_ATTBONUS_MONSTER,item.APPLY_CRITICAL_PCT]
	pet_bonus_value=[3000,10,10]

	evoleItems = [\
		[ [55004,10],[30058,10],[30073,10], [30041,10], [30017,10], [30074,5], [30088,5]],\
		[ [55005,10],[27994,2],[30035,10], [30089,10], [30031,10], [30011,10], [30080,5]],\
		[ [55006,10],[27992,2],[27993,2], [30083,10], [30086,10], [30077,10], [30550,5]]]

	pet_skill_data = [\
		["", 0, 0],\
		[localeInfo.PET_SKIL_1, item.APPLY_ATTBONUS_STONE, 10],\
		[localeInfo.PET_SKIL_2, item.APPLY_ATTBONUS_MONSTER, 10],\
		[localeInfo.PET_SKIL_3, item.APPLY_ATTBONUS_BOSS, 10],\
		[localeInfo.PET_SKIL_4, item.APPLY_STR, 10],\
		[localeInfo.PET_SKIL_5, item.APPLY_INT, 10],\
		[localeInfo.PET_SKIL_6, item.APPLY_DEX, 10],\
		[localeInfo.PET_SKIL_7, item.APPLY_CON, 10],\
		[localeInfo.PET_SKIL_8, item.APPLY_ATTBONUS_ANIMAL, 15],\
		[localeInfo.PET_SKIL_9, item.APPLY_ATTBONUS_ORC, 15],\
		[localeInfo.PET_SKIL_10, item.APPLY_ATTBONUS_MILGYO, 15],\
		[localeInfo.PET_SKIL_11, item.APPLY_ATTBONUS_UNDEAD, 15],\
		[localeInfo.PET_SKIL_12, item.APPLY_ATTBONUS_DEVIL, 15],\
		[localeInfo.PET_SKIL_13, item.APPLY_EXP_DOUBLE_BONUS, 10],\
		[localeInfo.PET_SKIL_14, item.APPLY_ITEM_DROP_BONUS, 10],\
		[localeInfo.PET_SKIL_15, item.APPLY_GOLD_DOUBLE_BONUS, 20],\
		[localeInfo.PET_SKIL_16, item.APPLY_ATTBONUS_HUMAN, 5],\
		[localeInfo.PET_SKIL_17, item.APPLY_RESIST_HUMAN, 5],\
		[localeInfo.PET_SKIL_18, item.APPLY_SKILL_DAMAGE_BONUS, 5],\
		[localeInfo.PET_SKIL_19, item.APPLY_SKILL_DEFEND_BONUS, 5],\
		[localeInfo.PET_SKIL_20, item.APPLY_NORMAL_HIT_DAMAGE_BONUS, 10],\
		[localeInfo.PET_SKIL_21, item.APPLY_NORMAL_HIT_DEFEND_BONUS, 10],\
		[localeInfo.PET_SKIL_22, item.APPLY_ANTI_CRITICAL_PCT, 10],\
		[localeInfo.PET_SKIL_23, item.APPLY_ANTI_PENETRATE_PCT, 10],\
		[localeInfo.PET_SKIL_24, item.APPLY_CAST_SPEED, 15],\
		[localeInfo.PET_SKIL_25, item.APPLY_BLOCK, 10],\
		[localeInfo.PET_SKIL_26, item.APPLY_POISON_REDUCE, 10],\
		[localeInfo.PET_SKIL_27, item.APPLY_RESIST_ICE, 10],\
		[localeInfo.PET_SKIL_28, item.APPLY_RESIST_EARTH, 10],\
		[localeInfo.PET_SKIL_29, item.APPLY_RESIST_DARK, 10],\
	]
	exp_table = [
		0,
		300,
		800,
		1500,
		2500,
		4300,
		7200,
		11000,
		17000,
		24000,
		33000,
		43000,
		58000,
		76000,
		100000,
		130000,
		169000,
		219000,
		283000,
		365000,
		472000,
		610000,
		705000,
		813000,
		937000,
		1077000,
		1237000,
		1418000,
		1624000,
		1857000,
		2122000,
		2421000,
		2761000,
		3145000,
		3580000,
		4073000,
		4632000,
		5194000,
		5717000,
		6264000,
		6837000,
		7600000,
		8274000,
		8990000,
		9753000,
		10560000,
		11410000,
		12320000,
		13270000,
		14280000,
		15340000,
		16870000,
		18960000,
		19980000,
		21420000,
		22930000,
		24530000,
		26200000,
		27960000,
		29800000,
		32780000,
		36060000,
		39670000,
		43640000,
		48000000,
		52800000,
		58080000,
		63890000,
		70280000,
		77310000,
		85040000,
		93540000,
		102900000,
		113200000,
		124500000,
		137000000,
		150700000,
		165700000,
		236990000,
		260650000,
		286780000,
		315380000,
		346970000,
		381680000,
		419770000,
		461760000,
		508040000,
		558740000,
		614640000,
		676130000,
		743730000,
		1041222000,
		1145344200,
		1259878620,
		1385866482,
		1524453130,
		1676898443,
		1844588288,
		2029047116,
		2050000000,
		2150000000,
		2210000000,
		2250000000,
		2280000000,
		2310000000,
		2330000000,
		2930000000,
		3370000000,
		3790000000,
		4000000000,
		4190000000,
		2420000000,
		2430000000,
		2440000000,
		2450000000,
		2460000000,
		2470000000,
		2480000000,
		2490000000,
		2490000000,
		2500000000
	]

if app.__CHAT_SETTINGS__:
	def CheckDirectory(directory):
		try:
			os.makedirs(directory)
		except:
			pass
	def CheckFile(directory):
		if os.path.exists(directory):
			return True
		return False
	def RemoveFile(directory):
		if os.path.exists(directory):
		  os.remove(directory)

	OPTION_CHECKBOX_TALKING = 1
	OPTION_CHECKBOX_PARTY = 2
	OPTION_CHECKBOX_GUILD = 3
	OPTION_CHECKBOX_SHOUT = 4
	OPTION_CHECKBOX_INFO = 5
	OPTION_CHECKBOX_NOTICE = 6
	OPTION_CHECKBOX_DICE = 7
	OPTION_CHECKBOX_EXP_INFO = 8
	OPTION_CHECKBOX_ITEM_INFO = 9
	OPTION_CHECKBOX_MONEY_INFO = 10
	OPTION_CHECKBOX_FILTER = 11

	OPTION_CHECKBOX_FLAG_EN = 12
	OPTION_CHECKBOX_FLAG_DE = 13
	OPTION_CHECKBOX_FLAG_TR = 14
	OPTION_CHECKBOX_FLAG_PT = 15
	OPTION_CHECKBOX_FLAG_ES = 16
	OPTION_CHECKBOX_FLAG_FR = 17
	OPTION_CHECKBOX_FLAG_RO = 18
	OPTION_CHECKBOX_FLAG_PL = 19
	OPTION_CHECKBOX_FLAG_IT = 20
	OPTION_CHECKBOX_FLAG_CZ = 21
	OPTION_CHECKBOX_FLAG_HU = 22
	OPTION_MAX = 23

	OPTION_CHECKBOX_MODE = {
		OPTION_CHECKBOX_TALKING : [[chat.CHAT_TYPE_TALKING], localeInfo.CHATTING_SETTING_TALKING],
		OPTION_CHECKBOX_INFO : [[chat.CHAT_TYPE_INFO], localeInfo.CHATTING_SETTING_SYSTEM],
		OPTION_CHECKBOX_NOTICE : [[chat.CHAT_TYPE_NOTICE,chat.CHAT_TYPE_BIG_NOTICE], localeInfo.CHATTING_SETTING_NOTICE],
		OPTION_CHECKBOX_PARTY : [[chat.CHAT_TYPE_PARTY], localeInfo.CHATTING_SETTING_PARTY],
		OPTION_CHECKBOX_GUILD : [[chat.CHAT_TYPE_GUILD], localeInfo.CHATTING_SETTING_GUILD],
		OPTION_CHECKBOX_SHOUT : [[chat.CHAT_TYPE_SHOUT], localeInfo.CHATTING_SETTING_SHOUT],
		OPTION_CHECKBOX_DICE : [[chat.CHAT_TYPE_DICE_INFO], localeInfo.CHATTING_SETTING_DICE],
		OPTION_CHECKBOX_EXP_INFO : [[chat.CHAT_TYPE_EXP_INFO], localeInfo.CHATTING_SETTING_EXP],
		OPTION_CHECKBOX_ITEM_INFO : [[chat.CHAT_TYPE_ITEM_INFO], localeInfo.CHATTING_SETTING_ITEM],
		OPTION_CHECKBOX_MONEY_INFO : [[chat.CHAT_TYPE_MONEY_INFO], localeInfo.CHATTING_SETTING_GOLD],
	}

	cacheChat = {}
	def CreateEmptyList(index):
		list = [1] * OPTION_MAX
		list[0] = str(index)
		list[OPTION_CHECKBOX_FILTER] = 0
		for langIndex in range(OPTION_CHECKBOX_FLAG_EN, OPTION_MAX):
			list[langIndex] = 0
		return list
	
	def SaveChatData():
		global cacheChat
		if len(cacheChat) == 0:
			return
		
		#import dbg
		#dbg.TraceError("--------------------------------------------")
		#dbg.TraceError(" ")
		#dbg.TraceError(str(cacheChat))
		#dbg.TraceError(" ")
		#dbg.TraceError("--------------------------------------------")
		
		MAIN_FILE = "lib/chatConfig"
		PLAYER_FILE = MAIN_FILE+"/"+player.GetName()+".chat"

		try:
			file = open(PLAYER_FILE, "w+")
			for key, data in cacheChat.items():
				data = cacheChat[key]
				text = ""
				for x in xrange(OPTION_MAX):
					text+=str(data[x])+"#"
				file.write(text+"\n")
			file.close()
		except:
			pass

	def LoadChatNewEmpty(index):
		global cacheChat
		cacheChat[index] = CreateEmptyList(index)
		SaveChatData()

	def LoadChatEmpty():
		global cacheChat
		cacheChat = {
			0: ['0', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			1: ['Empire', 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			2: ['Yang', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			3: ['Exp', 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			4: ['Server', 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		}
		#cacheChat[0] = CreateEmptyList(0)
		SaveChatData()

	def RemoveChat(index):
		global cacheChat
		if cacheChat.has_key(index):
			del cacheChat[index]
			SaveChatData()

	def LoadChatData():
		global cacheChat
		cacheChat = {}
		MAIN_FILE = "lib/chatConfig"
		PLAYER_FILE = MAIN_FILE+"/"+player.GetName()+".chat"
		CheckDirectory(MAIN_FILE)
		if CheckFile(PLAYER_FILE):
			lines = open(PLAYER_FILE, "r").readlines()
			if len(lines) > 0:

				index = 0
				for line in lines:
					lineSplit = line.split("#")

					if len(lineSplit)==0 or OPTION_MAX != len(lineSplit)-1:
						LoadChatEmpty()
					else:
						list = [1] * OPTION_MAX
						for j in xrange(len(lineSplit)-1):
							if j == 0:
								list[j] = str(lineSplit[j])
							else:
								list[j] = int(lineSplit[j])
						cacheChat[index] = list
					index+=1
			else:
				LoadChatEmpty()
		else:
			LoadChatEmpty()
			
SUPPORTGUI = 0
SUPPORT_SHOW = 0
SUPPORT_INFO_ITEMS = {"item_1":0,"item_2":0,"item_3":0,"item_4":0,"item_5":0,"item_6":0}

if app.ENABLE_OPTION_COLLECT_EQUIPMENT:
	PickupSpeed = 0

if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
	PICKUPMODE = 0
	RARITYMODE = 0
	PREMIUMMODE = [False, 0]

NEW_678TH_SKILL_ENABLE = 1
# EXTRA END
PETGUI = 0
PETMINILEVEL = 0
PETMINIEVO = 0
FEEDWIND = 0
SKILL_PET3 = 0
SKILL_PET2 = 0
SKILL_PET1 = 0
LASTAFFECT_POINT = 0
LASTAFFECT_VALUE = 0
EVOLUTION = 0
COMBAT_ZONE = 0
BOSS_EVENT = 0
BOSS_EVENT_STATUS = 0
SHOP_IN_CLIENT = 0


METIN_EVENT = 0
METIN_EVENT_STATUS = 0

FontValue = 0

TEST_FUNCTION = 0
NEW_LOGIN_INTERFACE = 0

Dominios = {
'dominios' : {},
'subdominios' : {},
}

TitleSystem = {
'title_pvm' : [],
'title_pvp' : [],
'load' : 0,
}

Achievements = {
'QID' : 0,
'QCMD' : '',
'achievements' : {},
'last_achievements' : [],
'achievementshop' : {'items': {}},
'POINTS' : 0
}

arayuz_mod = 0
nesnemarket_mod = 0
arayuz_cur = 0
arayuz_max = 0
arayuz_hp_cur = 0
arayuz_hp_max = 0
arayuz_mp_cur = 0
arayuz_mp_max = 0
GUI_ARAYUZ_ICERIK = [ [], [], [], [], [], [], [], [], [], [] ]
GUI_ARAYUZ = []

TEST_FUNCTION = 0
NEW_LOGIN_INTERFACE = 0
mob_perro = 0
SEQUENCE_PACKET_ENABLE = 0

ACCOUNT_NAME = "Nethis"
WOLF_MAN = "DISABLED"	# ENABLED/DISABLED
WOLF_WOMEN = "DISABLED"	# ENABLED/DISABLED
#LANG
Mount_Affect = {"status":0,"vnum":0}

NewGoldWindow = 0

if app.ENABLE_REFINE_RENEWAL:
	IS_AUTO_REFINE = False
	AUTO_REFINE_TYPE = 0
	AUTO_REFINE_DATA = {
		"ITEM" : [-1, -1],
		"NPC" : [0, -1, -1, 0]
	}

Tickets = {
	'QID' : 0,
	'QCMD' : '',
	'MY_TICKETS' : [],
	'GLOBAL_TICKETS' : [],
	'ANSWERS' : {},
	'PERMISIONS' : []
}

Inventory_Locked = {
	"Active" : True,
}

for x in xrange(0,6):
	Inventory_Locked.update({"Keys_Can_Unlock_%d"%x : 0})

LoginAndFace = ""

if app.ENABLE_SEND_TARGET_INFO:
	MONSTER_INFO_DATA = {}

COINS_DRS = [0,0]
ITEMSHOP = {
	'items' : {
			'startpage' : {
					'mostBought' : [],
					'hotOffers' : [],
					},
			'itemshop' : {},
			'voteshop' : {},
			'achievementshop' : {},
		},
	'category': [], ##(id, name, image)
	'subCategories': {}, ## categoryId: [...name]
	'tableUpdate' : '0000-00-00 00:00:00',
	'qid'	: 0,
	'questCMD' : '',
}
# OFFLINE_SHOPS
shop_cost=[]
shop_money=0
gift_items={}
MyShops=[]
SHOPNAMES_RANGE = 5000

INPUT_IGNORE = 0
SELECT_CHARACTER_ROTATION = 0 #1
# option
IN_GAME_SHOP_ENABLE = 1
CONSOLE_ENABLE = 0

if app.ENABLE_MULTI_REFINE_WORLDARD:
	multi_refine_dates = []
	
PVPMODE_ENABLE = 1
PVPMODE_TEST_ENABLE = 0
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 30

FOG_LEVEL0 = 4800.0
FOG_LEVEL1 = 9600.0
FOG_LEVEL2 = 12800.0
FOG_LEVEL = FOG_LEVEL0
FOG_LEVEL_LIST=[FOG_LEVEL0, FOG_LEVEL1, FOG_LEVEL2]

CAMERA_MAX_DISTANCE_SHORT = 2500.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_SHORT

CHRNAME_COLOR_INDEX = 0

ENVIRONMENT_NIGHT="d:/ymir work/environment/moonlight04.msenv"

# constant
HIGH_PRICE = 500000
MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960
SUB2_LOADING_ENABLE = 1
EXPANDED_COMBO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 1
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 1
LOGIN_COUNT_LIMIT_ENABLE = 0

USE_SKILL_EFFECT_UPGRADE_ENABLE = 1

VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100
GUILD_WAR_TYPE_SELECT_ENABLE = 1
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 0

HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
SEQUENCE_PACKET_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 0
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 0
LOGIN_COUNT_LIMIT_ENABLE = 0
PVPMODE_PROTECTED_LEVEL = 15
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

isItemQuestionDialog = 0
isOffShopOpened = 0

def GetFont():
	valor = localeInfo.UI_DEF_FONT
	if os.path.exists("font.cfg"):
		file = old_open("font.cfg", 'r')
		result = file.read()[0]
		if len(result) >= 1:
			if result == "1":
				valor = localeInfo.UI_DEF_FONT_LARGE
			elif result == "2":
				valor = localeInfo.UI_DEF_FONT

		file.close()

	return valor

def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag

def SET_OFFSHOP_OPEN(flag):
	global isOffShopOpened
	isOffShopOpened = flag
	
def GET_OFFSHOP_OPENED():
	global isOffShopOpened
	return isOffShopOpened

########################

def SET_DEFAULT_FOG_LEVEL():
	global FOG_LEVEL
	app.SetMinFog(FOG_LEVEL)

def SET_FOG_LEVEL_INDEX(index):
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	try:
		FOG_LEVEL=FOG_LEVEL_LIST[index]
	except IndexError:
		FOG_LEVEL=FOG_LEVEL_LIST[0]
	app.SetMinFog(FOG_LEVEL)

def GET_FOG_LEVEL_INDEX():
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	return FOG_LEVEL_LIST.index(FOG_LEVEL)

########################

def SET_DEFAULT_CAMERA_MAX_DISTANCE():
	global CAMERA_MAX_DISTANCE
	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def SET_CAMERA_MAX_DISTANCE_INDEX(index):
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	try:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[index]
	except:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[0]

	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def GET_CAMERA_MAX_DISTANCE_INDEX():
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	return CAMERA_MAX_DISTANCE_LIST.index(CAMERA_MAX_DISTANCE)

########################

def SET_DEFAULT_CHRNAME_COLOR():
	global CHRNAME_COLOR_INDEX
	chrmgr.SetEmpireNameMode(CHRNAME_COLOR_INDEX)

def SET_CHRNAME_COLOR_INDEX(index):
	global CHRNAME_COLOR_INDEX
	CHRNAME_COLOR_INDEX=index
	chrmgr.SetEmpireNameMode(index)

def GET_CHRNAME_COLOR_INDEX():
	global CHRNAME_COLOR_INDEX
	return CHRNAME_COLOR_INDEX

def SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index):
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = index

def GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	return VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD

def SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE():
	global CONVERT_EMPIRE_LANGUAGE_ENABLE
	net.SetEmpireLanguageMode(CONVERT_EMPIRE_LANGUAGE_ENABLE)

def SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS():
	global USE_ITEM_WEAPON_TABLE_ATTACK_BONUS
	player.SetWeaponAttackBonusFlag(USE_ITEM_WEAPON_TABLE_ATTACK_BONUS)

def SET_DEFAULT_USE_SKILL_EFFECT_ENABLE():
	global USE_SKILL_EFFECT_UPGRADE_ENABLE
	app.SetSkillEffectUpgradeEnable(USE_SKILL_EFFECT_UPGRADE_ENABLE)

def SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE():
	global TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE
	app.SetTwoHandedWeaponAttSpeedDecreaseValue(TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE)

########################

ACCESSORY_MATERIAL_LIST = [50623, 50624, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 50634, 50635, 50636, 50637, 50638, 50639]
JewelAccessoryInfos = [
		# jewel		wrist	neck	ear
		[ 50634,	14420,	16220,	17220 ,	19220],
		[ 50635,	14500,	16500,	17500 ,	19500],
		[ 50636,	14520,	16520,	17520 ,	19520],
		[ 50637,	14540,	16540,	17540 ,	19540],
		[ 50638,	14560,	16560,	17560 ,	19560],
		[ 50639,	14570,	16570,	17570 ,	19570],
	]
def GET_ACCESSORY_MATERIAL_VNUM(vnum, subType):
	ret = vnum
	item_base = (vnum / 10) * 10
	for info in JewelAccessoryInfos:
		if item.ARMOR_WRIST == subType:
			if info[1] == item_base:
				return info[0]
		elif item.ARMOR_NECK == subType:
			if info[2] == item_base:
				return info[0]
		elif item.ARMOR_EAR == subType:
			if info[3] == item_base:
				return info[0]
		elif item.ITEM_TYPE_RINGS == subType:
			if info[4] == item_base:
				return info[0]


	if vnum >= 16210 and vnum <= 16219:
		return 50625

	if item.ARMOR_WRIST == subType:
		WRIST_ITEM_VNUM_BASE = 14000
		ret -= WRIST_ITEM_VNUM_BASE
	elif item.ARMOR_NECK == subType:
		NECK_ITEM_VNUM_BASE = 16000
		ret -= NECK_ITEM_VNUM_BASE
	elif item.ARMOR_EAR == subType:
		EAR_ITEM_VNUM_BASE = 17000
		ret -= EAR_ITEM_VNUM_BASE
	elif item.ITEM_TYPE_RINGS == subType:
		RINGS_ITEM_VNUM_BASE = 19000
		ret -= RINGS_ITEM_VNUM_BASE

	type = ret/20

	if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
		type = (ret-170) / 20
		if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
			return 0

	return ACCESSORY_MATERIAL_LIST[type]

##################################################################
## ���� �߰��� '��Ʈ' ������ Ÿ�԰�, ��Ʈ�� ���Ͽ� ���� ������ ����..
## ��Ʈ�� ���Ͻý����� �Ǽ������� �����ϱ� ������, �� �Ǽ����� ���� �ϵ��ڵ�ó�� �̷������� �� ���ۿ� ����..

def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	# ����� ��� ��Ʈ���� �ϳ��� ������(#18900)�� ���� ����
	return 18900

##################################################################
## �ڵ����� (HP: #72723 ~ #72726, SP: #72727 ~ #72730)

# �ش� vnum�� �ڵ������ΰ�?
def IS_AUTO_POTION(itemVnum):
	if app.ENABLE_NEW_AUTOPOTION:
		return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum) or IS_NEW_AUTO_POTION(itemVnum)
	else:
		return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum)

# �ش� vnum�� HP �ڵ������ΰ�?
def IS_AUTO_POTION_HP(itemVnum):
	if 72723 <= itemVnum and 72726 >= itemVnum:
		return 1
	elif itemVnum >= 76021 and itemVnum <= 76022:		## ���� �� ������ ȭ���� �ູ
		return 1
	elif itemVnum == 79012:
		return 1

	return 0

# �ش� vnum�� SP �ڵ������ΰ�?
def IS_AUTO_POTION_SP(itemVnum):
	if 72727 <= itemVnum and 72730 >= itemVnum:
		return 1
	elif itemVnum >= 76004 and itemVnum <= 76005:		## ���� �� ������ ������ �ູ
		return 1
	elif itemVnum == 79013:
		return 1
	elif itemVnum >= 51010 and itemVnum <= 51035 and app.__RENEWAL_CRYSTAL__:
		return 1
	#elif itemVnum == 55701 or itemVnum == 55702 or itemVnum == 55703 or itemVnum == 55704:
	#	return 1
	# elif itemVnum == 71124:
		# return 1
	return 0


def WriteLineInFile(fname, linenum, s):
	farr = []
	if os.path.exists(fname):
		f = open(fname, "r")
		for line in f:
			farr.append(line)
		f.close()
	while len(farr) < int(linenum):
		farr.append("")
	farr[int(linenum)-1] = str(s)
	f = open(fname, "w")
	for line in farr:
		f.write(line)
		if (len(line) > 0 and line[-1:] != "\n") or len(line) == 0:
			f.write("\n")
	f.close()

def ReadLineInFile(fname, linenum):
	if not os.path.exists(fname):
		return ""
	f = open(fname, "r")
	farr = []
	for line in f:
		farr.append(line)
	f.close()
	if len(farr) >= int(linenum):
		ret = farr[int(linenum)-1]
		if ret[-1:] == "\n":
			return ret[:-1]
		else:
			return ret
	else:
		return ""

if app.ENABLE_NEW_AUTOPOTION:
	def IS_NEW_AUTO_POTION(itemVnum):
		return IS_AUTO_POTION_ATTACK_SPEED(itemVnum) or IS_AUTO_POTION_MOV_SPEED(itemVnum) or IS_AUTO_POTION_CRITICAL(itemVnum) or IS_AUTO_POTION_PENETRATE(itemVnum) or IS_AUTO_POTION_VIT(itemVnum) or IS_AUTO_POTION_STR(itemVnum) or IS_AUTO_POTION_INT(itemVnum) or IS_AUTO_POTION_DEX(itemVnum) or IS_AUTO_COLOR_POTION(itemVnum)

	def IS_AUTO_POTION_ATTACK_SPEED(itemVnum):
		return itemVnum == 72731

	def IS_AUTO_POTION_MOV_SPEED(itemVnum):
		return itemVnum == 72732

	def IS_AUTO_POTION_CRITICAL(itemVnum):
		return itemVnum == 79051

	def IS_AUTO_POTION_PENETRATE(itemVnum):
		return itemVnum == 79052

	def IS_AUTO_POTION_VIT(itemVnum):
		return itemVnum == 79053

	def IS_AUTO_POTION_STR(itemVnum):
		return itemVnum == 79054

	def IS_AUTO_POTION_INT(itemVnum):
		return itemVnum == 79055

	def IS_AUTO_POTION_DEX(itemVnum):
		return itemVnum == 79056

	def IS_AUTO_COLOR_POTION(itemVnum):
		return itemVnum >= 79057 and itemVnum <= 79062
