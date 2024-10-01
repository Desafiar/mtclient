#! /usr/bin/env python
__author__		= 'VegaS'
__date__		= '2020-02-04'
__name__		= 'IntroLoading Renewal'
__version__		= '4.3'

import ui
import uiScriptLocale
import net
import app
import player
import background
import wndMgr
import constInfo
import playerSettingModule
import colorInfo
import chrmgr
import localeInfo
import emotion
import playerLoad
from _weakref import proxy

##################################
## loadingFunctions
##################################
NAME_COLOR_DICT = {
	chrmgr.NAMECOLOR_PC : colorInfo.CHR_NAME_RGB_PC,
	chrmgr.NAMECOLOR_NPC : colorInfo.CHR_NAME_RGB_NPC,
	chrmgr.NAMECOLOR_MOB : colorInfo.CHR_NAME_RGB_MOB,
	chrmgr.NAMECOLOR_PVP : colorInfo.CHR_NAME_RGB_PVP,
	chrmgr.NAMECOLOR_PK : colorInfo.CHR_NAME_RGB_PK,
	chrmgr.NAMECOLOR_PARTY : colorInfo.CHR_NAME_RGB_PARTY,
	chrmgr.NAMECOLOR_WARP : colorInfo.CHR_NAME_RGB_WARP,
	chrmgr.NAMECOLOR_WAYPOINT : colorInfo.CHR_NAME_RGB_WAYPOINT,
	chrmgr.NAMECOLOR_BOSS : colorInfo.CHR_NAME_RGB_BOSS,
	chrmgr.NAMECOLOR_EMPIRE_MOB : colorInfo.CHR_NAME_RGB_EMPIRE_MOB,
	chrmgr.NAMECOLOR_EMPIRE_NPC : colorInfo.CHR_NAME_RGB_EMPIRE_NPC,
	chrmgr.NAMECOLOR_EMPIRE_PC+1 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_A,
	chrmgr.NAMECOLOR_EMPIRE_PC+2 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_B,
	chrmgr.NAMECOLOR_EMPIRE_PC+3 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_C,
}

if app.ENABLE_OFFLINESHOP_SYSTEM:
	NAME_COLOR_DICT[chrmgr.NAMECOLOR_SHOP] = colorInfo.CHR_NAME_RGB_SHOP

TITLE_COLOR_DICT = (
	colorInfo.TITLE_RGB_GOOD_4,
	colorInfo.TITLE_RGB_GOOD_3,
	colorInfo.TITLE_RGB_GOOD_2,
	colorInfo.TITLE_RGB_GOOD_1,
	colorInfo.TITLE_RGB_NORMAL,
	colorInfo.TITLE_RGB_EVIL_1,
	colorInfo.TITLE_RGB_EVIL_2,
	colorInfo.TITLE_RGB_EVIL_3,
	colorInfo.TITLE_RGB_EVIL_4,
)

if app.ENABLE_STONEMINIMAP:
	NAME_COLOR_DICT.update({
			chrmgr.NAMECOLOR_METIN : colorInfo.CHR_NAME_RGB_METIN,
		})

def __main__():
	## RegisterColor

	for nameIndex, nameColor in NAME_COLOR_DICT.items():
		chrmgr.RegisterNameColor(nameIndex, *nameColor)


	for titleIndex, titleColor in enumerate(TITLE_COLOR_DICT):
		chrmgr.RegisterTitleColor(titleIndex, *titleColor)
		
	## RegisterTitleName	
	for titleIndex, titleName in enumerate(localeInfo.TITLE_NAME_LIST):
		chrmgr.RegisterTitleName(titleIndex, titleName)
		
	## RegisterEmotionIcon	
	emotion.RegisterEmotionIcons()
		
	## RegisterDungeonMapName	
	dungeonMapNameList = ("metin2_map_spiderdungeon", "metin2_map_monkeydungeon", "metin2_map_monkeydungeon_02", "metin2_map_monkeydungeon_03", "metin2_map_deviltower1")
	for dungeonMapName in dungeonMapNameList:
		background.RegisterDungeonMapName(dungeonMapName)
		
	## LoadGuildBuilding	
	playerSettingModule.LoadGuildBuildingList(localeInfo.GUILD_BUILDING_LIST_TXT)
	if app.RACE_HEIGHT:
		playerSettingModule.LoadRaceHeight()

##################################
## LoadingWindow
##################################

class LoadingWindow(ui.ScriptWindow):
	def __init__(self, stream):
		print "NEW LOADING WINDOW -------------------------------------------------------------------------------"
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, self)
		self.stream=stream
		self.errMsg=0
		self.update=0
		self.playerX=0
		self.playerY=0
		self.loadStepList=[]

	def __del__(self):
		print "---------------------------------------------------------------------------- DELETE LOADING WINDOW"
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, 0)
		ui.Window.__del__(self)

	def Open(self):
		print "OPEN LOADING WINDOW -------------------------------------------------------------------------------"
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/LoadingWindow1.py")
		except:
			import exception
			exception.Abort("LodingWindow.Open - LoadScriptFile Error")

		try:
			self.errMsg=self.GetChild("ErrorMessage")
		except:
			import exception
			exception.Abort("LodingWindow.Open - LoadScriptFile Error")

		self.errMsg.Hide()

		self.Show()
		chrSlot=self.stream.GetCharacterSlot()
		net.SendSelectCharacterPacket(chrSlot)
		app.SetFrameSkip(0)

	def Close(self):
		print "---------------------------------------------------------------------------- CLOSE LOADING WINDOW"
		app.SetFrameSkip(1)
		self.loadStepList=[]
		self.errMsg=0
		self.ClearDictionary()
		self.Hide()

	def OnPressEscapeKey(self):
		app.SetFrameSkip(1)
		self.stream.SetLoginPhase()
		return True

	def __SetNext(self, next):
		if next:
			self.update=ui.__mem_func__(next)
		else:
			self.update=0

	def LoadData(self, playerX, playerY):
		self.playerX=playerX
		self.playerY=playerY

		self.loadStepList=[
			(100, ui.__mem_func__(self.__StartGame)),
		]

	def OnUpdate(self):
		if len(self.loadStepList)>0:
			(progress, runFunc)=self.loadStepList[0]

			try:
				runFunc()

			except:
				self.errMsg.Show()
				self.loadStepList=[]

				dbg.TraceError(" !!! Failed to load game data : STEP [%d]" % (progress))
				app.Exit()

				return

			self.loadStepList.pop(0)

	def __StartGame(self):
		background.SetViewDistanceSet(background.DISTANCE0, 9999999)
		background.SelectViewDistanceNum(background.DISTANCE0)
		app.SetGlobalCenterPosition(self.playerX, self.playerY)
		net.StartGame()
