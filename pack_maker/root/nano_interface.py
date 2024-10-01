## IMPORTS
import playerSettingModule

## GLOBALS
global CREATE_ACCOUNT
global FORGOT_PASSWORD

#PATCHS
PATCH = "nano_interface/"
COMMON = PATCH + "common/"
SCRIPTS = "nano_scripts/"
CHAR_CREATE = "nano_interface/character_create/"
CHAR_SELECT = "nano_interface/select_character/"

## COLORS
COLOR_NORMAL = 0xffa08784
COLOR_HOVER = 0xfff8d090
SING_IN_COLOR = 0xfff0e6d2
COLOR_RED = 0xffbe1e27
COLOR_LOGIN_TEXT = 0xffe8decb
COLOR_WHITE = 0xffe5dfcf
COLOR_HOVER2 = 0xffaca17d

name = "Nethis" #Nombre Del Metin
name_channel1 = "-Ch1" #Nombre del Channel1
name_channel2 = "-Ch2" #Nombre del Channel2
name_channel3 = "-Ch3" #Nombre del Channel3
name_channel4 = "-Ch4" #Nombre del Channel4

## SERVER PORTS
SERVERS_LIST_DICT = {
	#0:{'ip':'198.50.239.68','CH1':13360,'CH2':16340,'CH3':18320,'CH4':20380,'auth':11025,'name':'Angel2',}, ##test
	0:{'ip':'192.168.191.103','CH1':30003,'CH2':30011,'CH3':30019,'CH4':30027,'auth':30001,'name':'Fetin2',}, ##bueno
	#2:{'ip':'11.111.11.113','CH1':25070,'CH2':25070,'CH3':25070,'CH4':25070,'auth':2300,'name':'Server 3',},
	# 3:{'ip':'11.111.11.111','CH1':25070,'CH2':25070,'CH3':25070,'CH4':25070,'auth_port':2300,'name':'Server 4',},

}

CHANNEL_NAME_DICT = {
	1: "Kanal 1",
	2: "Kanal 2",
	3: "Kanal 3",
	4: "Kanal 4"
}

## LINKS
CREATE_ACCOUNT = "https://angel2.es/registro#centrado"
FORGOT_PASSWORD = "https://angel2.es/recuperarpass"


## RACES

RACES = {
	0 : "playerSettingModule.RACE_WARRIOR_M",
	1 : "playerSettingModule.RACE_ASSASSIN_M",
	2 : "playerSettingModule.RACE_SURA_M",
	3 : "playerSettingModule.RACE_SHAMAN_M",
	4 : "playerSettingModule.RACE_WARRIOR_W",
	5 : "playerSettingModule.RACE_ASSASSIN_W",
	6 : "playerSettingModule.RACE_SURA_W",
	7 : "playerSettingModule.RACE_SHAMAN_W",
	8 : "playerSettingModule.RACE_SOLARI_W",
}

FACE_IMAGE_SELECT = {
	playerSettingModule.RACE_WARRIOR_M	: PATCH + "faces/select_faces/icon_mwarrior.png",
	playerSettingModule.RACE_WARRIOR_W	: PATCH + "faces/select_faces/icon_wwarrior.png",
	playerSettingModule.RACE_ASSASSIN_M	: PATCH + "faces/select_faces/icon_mninja.png",
	playerSettingModule.RACE_ASSASSIN_W	: PATCH + "faces/select_faces/icon_wninja.png",
	playerSettingModule.RACE_SURA_M		: PATCH + "faces/select_faces/icon_msura.png",
	playerSettingModule.RACE_SURA_W		: PATCH + "faces/select_faces/icon_wsura.png",
	playerSettingModule.RACE_SHAMAN_M	: PATCH + "faces/select_faces/icon_mshaman.png",
	playerSettingModule.RACE_SHAMAN_W	: PATCH + "faces/select_faces/icon_wshaman.png",
}
FACE_IMAGE_SELECT_BIG = {
	playerSettingModule.RACE_WARRIOR_M	: PATCH + "faces/select_faces/icon_mwarrior.png",
	playerSettingModule.RACE_WARRIOR_W	: PATCH + "faces/select_faces/icon_wwarrior.png",
	playerSettingModule.RACE_ASSASSIN_M	: PATCH + "faces/select_faces/icon_mninja.png",
	playerSettingModule.RACE_ASSASSIN_W	: PATCH + "faces/select_faces/icon_wninja.png",
	playerSettingModule.RACE_SURA_M		: PATCH + "faces/select_faces/icon_msura.png",
	playerSettingModule.RACE_SURA_W		: PATCH + "faces/select_faces/icon_wsura.png",
	playerSettingModule.RACE_SHAMAN_M	: PATCH + "faces/select_faces/icon_mshaman.png",
	playerSettingModule.RACE_SHAMAN_W	: PATCH + "faces/select_faces/icon_wshaman.png",
}
FACE_IMAGE_SELECT_SMALLER = {
	playerSettingModule.RACE_WARRIOR_M	: PATCH + "faces/icon_mwarrior.png",
	playerSettingModule.RACE_WARRIOR_W	: PATCH + "faces/icon_wwarrior.png",
	playerSettingModule.RACE_ASSASSIN_M	: PATCH + "faces/icon_mninja.png",
	playerSettingModule.RACE_ASSASSIN_W	: PATCH + "faces/icon_wninja.png",
	playerSettingModule.RACE_SURA_M		: PATCH + "faces/icon_msura.png",
	playerSettingModule.RACE_SURA_W		: PATCH + "faces/icon_wsura.png",
	playerSettingModule.RACE_SHAMAN_M	: PATCH + "faces/icon_mshaman.png",
	playerSettingModule.RACE_SHAMAN_W	: PATCH + "faces/icon_wshaman.png",
}