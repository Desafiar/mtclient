import os
import app
import dbg
import grp
import item
import background
import chr
import chrmgr
import player
import snd
import chat
import textTail
import snd
import net
import effect
import wndMgr
import fly
import systemSetting
import uiScriptLocale
import quest
import guild
import skill
import messenger
import localeInfo
import constInfo
import uiarayuz
import exchange
import ime
import uiToolTip
import uiCantDestroyItem
if app.ENABLE_DEFENSAWESHIP:
	import uiShipMastHP

from uiToolTip import ItemToolTip

if app.ENABLE_OFFLINESHOP_SYSTEM:
	import uiOfflineShopBuilder
	import shop

if app.ENABLE_ITEMSHOP:
	import uiItemShopNew

if app.ENABLE_SKILL_BOOK_READING:
	import uibkoku
if app.ENABLE_SPIRIT_STONE_READING:
	import uiruhtasi

import ui
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget
import uiEventCalendar

if app.ENABLE_MULTILANGUAGE_SYSTEM:
	import nonplayer
	import event

# PRIVATE_SHOP_PRICE_LIST
#import uiPrivateShopBuilder
# END_OF_PRIVATE_SHOP_PRICE_LIST

import mouseModule
import consoleModule
import localeInfo

import playerSettingModule
import interfaceModule

import musicInfo
import debugInfo
import stringCommander
if app.NEW_PET_SYSTEM:
	import uipetsystem
import uiitemshop_v2
import uisupportsystem
import extern_wa_shopitem

if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
	import uiAuto

if app.ENABLE_FEATURES_OXEVENT:
	import uioxevent

if app.ENABLE_ADMIN_BAN_MANAGER:
	import uiadmintool

from _weakref import proxy

#import logininfo

from uiUtils import Edit2 as Edit2
# TEXTTAIL_LIVINGTIME_CONTROL
#if localeInfo.IsJAPAN():
#	app.SetTextTailLivingTime(8.0)
# END_OF_TEXTTAIL_LIVINGTIME_CONTROL

# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = False
SCREENSHOT_DIR = None

if localeInfo.IsEUROPE():
	SCREENSHOT_CWDSAVE = True

if localeInfo.IsCIBN10():
	SCREENSHOT_CWDSAVE = False
	SCREENSHOT_DIR = "YT2W"

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0
if app.ENABLE_BIOLOG_SYSTEM:
	import uiprofessionalbiolog
class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
		player.SetGameWindow(self)
		#self.uiNewShopCreate = None
		#self.uiNewShop = None

		if app.ENABLE_DEFENSAWESHIP:
			self.wndShipMastHP = uiShipMastHP.ShipMastHP()
			self.wndShipMastHP.Close()

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None
		if (app.WJ_COMBAT_ZONE):
			import uicombatzone
			self.wndCombatZone = uicombatzone.CombatZoneWindow()
		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.console = None
		self.mapNameShower = None
		self.affectShower = None
		self.arayuz = None
		self.playerGauge = None
		self.loopList = []

		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			constInfo.PREMIUMMODE =[False,0]

		constInfo.SetGameInstance(self)
		self.affectShower = uiAffectShower.AffectShower()

		self.stream=stream
		self.interface = interfaceModule.Interface()

		if app.ENABLE_PVP_TOURNAMENT or app.ENABLE_RENEWAL_PVP:
			constInfo.SetInterfaceInstance(self.interface)

		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.Hide()
		
		if app.NEW_PET_SYSTEM:
			self.petmain = uipetsystem.PetSystemMain()
			self.petmini = uipetsystem.PetSystemMini(self.petmain)
		
		self.console = consoleModule.ConsoleWindow()
		self.console.BindGameClass(self)
		self.console.SetConsoleSize(wndMgr.GetScreenWidth(), 200)
		self.console.Hide()

		##
		self.eventList = []
		self.tempEventList = []
		self.lastUpdate = 0
		##

		##
		self.notificationItem = None
		##

		self.supportpg = uisupportsystem.SupportMainGui()

		self.mapNameShower = uiMapNameShower.MapNameShower()

		if app.ENABLE_SPIRIT_STONE_READING:
			self.ruhtasi = uiruhtasi.RuhTasi()
			self.ruhtasi.Hide()

		if app.ENABLE_SKILL_BOOK_READING:
			self.bkoku = uibkoku.BKOku()
			self.bkoku.Hide()

		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()

		self.arayuz = uiarayuz.arayuzdialog()
		self.arayuz.Show()

		#wj 2014.1.2. ESCŰ�� ���� �� �켱������ DropQuestionDialog�� ������ �������? ������ ó���� itemDropQuestionDialog�� ����Ǿ�?���� �ʾ� ERROR�� �߻��Ͽ� init���� �����?���ÿ� �ʱ�ȭ ��Ŵ.
		self.itemDropQuestionDialog = None

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()

		if app.ENABLE_FEATURES_OXEVENT:
			self.eventWindowLogin = uioxevent.OxEventManagerLogin()
			self.eventWindowManager = uioxevent.OxEventManager()
			self.eventWindow = uioxevent.OxEventWinners()

		if app.ENABLE_ADMIN_BAN_MANAGER:
			self.wndAdminTool = uiadmintool.AdminTool()

	def __del__(self):
		player.SetGameWindow(0)
		net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.SetFrameSkip(1)

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		
		self.LoadingBar = uiitemshop_v2.LoadingBar()
		self.LoadingBar.Open()
		self.LoadingBar.SetPercent(100)
		
		self.quickSlotPageIndex = 0
		self.getplayersonline = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.consoleEnable = False
		self.isShowDebugInfo = False
		self.ShowNameFlag = False

		self.enableXMasBoom = False
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0
		


		##
		self.eventList = []
		self.tempEventList = []
		self.lastUpdate = 0
		
		#if not self.notificationItem:
		#	self.notificationItem = uiEventCalendar.EventNotificationItem(self)

		if not constInfo.WND_EVENT:
			constInfo.WND_EVENT = uiEventCalendar.EventNotificationItem(self)

		self.notificationItem = constInfo.WND_EVENT
		self.notificationItem.SetParentW(self)
		#self.notificationItem.AddFlag("not_pick")
		self.notificationItem.SetCurrentEvent("luz_luna.tga", 0, 0, 0)
		self.notificationItem.SetEvent(self.__ClickCalendarioButton)
		#self.notificationItem.SetPosition(100, 10)
		self.notificationItem.Open()
		##

		self.cantDestroyItemDialog = uiCantDestroyItem.CantDestroyItemDialog()
		self.cantDestroyItemDialog.Hide()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()

		# TWO_HANDED_WEAPON_ATTACK_SPEED_UP
		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
		# END_OF_TWO_HANDED_WEAPON_ATTACK_SPEED_UP

		import PrivateShopSearch
		self.wndOffShopSearch = PrivateShopSearch.PrivateShopSearch()
		
		
		import event
		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)

		if constInfo.PVPMODE_TEST_ENABLE:
			self.testPKMode = ui.TextLine()
			self.testPKMode.SetFontName(localeInfo.UI_DEF_FONT)
			self.testPKMode.SetPosition(0, 15)
			self.testPKMode.SetWindowHorizontalAlignCenter()
			self.testPKMode.SetHorizontalAlignCenter()
			self.testPKMode.SetFeather()
			self.testPKMode.SetOutline()
			self.testPKMode.Show()

			self.testAlignment = ui.TextLine()
			self.testAlignment.SetFontName(localeInfo.UI_DEF_FONT)
			self.testAlignment.SetPosition(0, 35)
			self.testAlignment.SetWindowHorizontalAlignCenter()
			self.testAlignment.SetHorizontalAlignCenter()
			self.testAlignment.SetFeather()
			self.testAlignment.SetOutline()
			self.testAlignment.Show()

		self.__BuildKeyDict()
		self.__BuildDebugInfo()
		self.ToggleDebugInfo()

		# PRIVATE_SHOP_PRICE_LIST
		#uiPrivateShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST

		# UNKNOWN_UPDATE
		exchange.InitTrading()
		# END_OF_UNKNOWN_UPDATE
		if app.ENABLE_ULTIMATE_REGEN:
			player.LoadNewRegen()


		## Sound
		snd.SetMusicVolume(systemSetting.GetMusicVolume()*net.GetFieldMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		netFieldMusicFileName = net.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("BGM/" + netFieldMusicFileName)
		elif musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		net.SendEnterGamePacket()
		if app.ENABLE_DEFENSAWESHIP:
			if background.GetCurrentMapName() == "defensawe_hydra":
				self.__ShipMastHPShow()

		# START_GAME_ERROR_EXIT
		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		# END_OF_START_GAME_ERROR_EXIT
		
		

		if app.ENABLE_SNOW_MODE:
			for i in xrange(10):
				if systemSetting.IsSnowTexturesMode():
					if background.GetCurrentMapName():
						snow_maps = [
							"metin2_map_a1",
							"metin2_map_b1",
							"metin2_map_c1"
						]
						snow_maps_textures = {
							# "metin2_map_a1" : "textureset\metin2_a1_snow.txt",
							# "metin2_map_b1" : "textureset\metin2_b1_snow.txt",
							# "metin2_map_c1" : "textureset\metin2_c1_snow.txt", }
							"metin2_map_a1" : "textureset\snow\snow_metin2_a1.txt",
							"metin2_map_b1" : "textureset\snow\snow_metin2_b1.txt",
							"metin2_map_c1" : "textureset\snow\snow_metin2_c1.txt", }
						if str(background.GetCurrentMapName()) in snow_maps:
							background.TextureChange(snow_maps_textures[str(background.GetCurrentMapName())])
							
		# NPC�� ť��ý�������?���� �� �ִ� �����۵��� �����?ĳ��
		# ex) cubeInformation[20383] = [ {"rewordVNUM": 72723, "rewordCount": 1, "materialInfo": "101,1&102,2", "price": 999 }, ... ]
		self.cubeInformation = {}
		self.currentCubeNPC = 0

	def __ClickCalendarioButton(self):
		self.interface.CalendarDialog()
	
	def Close(self):
		self.Hide()
		if app.ENABLE_MULTI_FARM_BLOCK:
			app.SetMultiFarmExeIcon(1)

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None
		self.loopList = []

		#uiPrivateShopBuilder.Clear()
		chat.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		skill.ClearSkillData()
		wndMgr.Unlock()
		if app.ENABLE_OFFLINESHOP_SYSTEM:
			uiOfflineShopBuilder.Clear()
			shop.Clear()
		mouseModule.mouseController.DeattachObject()

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()
		
		if app.ENABLE_DEFENSAWESHIP:
			if self.wndShipMastHP:
				self.wndShipMastHP.Close()
				self.wndShipMastHP=0

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None
		self.cantDestroyItemDialog.Hide()

		# UNKNOWN_UPDATE
		self.itemDropQuestionDialog = None
		# END_OF_UNKNOWN_UPDATE

		# QUEST_CONFIRM
		self.confirmDialog = None
		# END_OF_QUEST_CONFIRM

		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None
		if app.NEW_PET_SYSTEM:
			self.petmain.Close()
			self.petmini.Close()
		self.supportpg.Close()
		self.ClearDictionary()

		self.playerGauge = None
		self.mapNameShower = None
		self.affectShower = None
		self.arayuz = None

		if self.console:
			self.console.BindGameClass(0)
			self.console.Close()
			self.console=None

		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None

		if app.ENABLE_ADMIN_BAN_MANAGER:
			if self.wndAdminTool:
				self.wndAdminTool.Hide()

		if app.ENABLE_SPIRIT_STONE_READING:
			if self.ruhtasi:
				self.ruhtasi.Destroy()
				self.ruhtasi = None

		if app.ENABLE_SKILL_BOOK_READING:
			if self.bkoku:
				self.bkoku.Destroy()
				self.bkoku = None

		if (app.WJ_COMBAT_ZONE):
			if self.wndCombatZone:
				self.wndCombatZone.Close()
		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			self.interface=None

		if app.ENABLE_FEATURES_OXEVENT:
			if self.eventWindowLogin:
				self.eventWindowLogin.Hide()

			if self.eventWindowManager:
				self.eventWindowManager.Hide()

			if self.eventWindow:
				self.eventWindow.Hide()

		if self.cantDestroyItemDialog:
			self.cantDestroyItemDialog = None

		#if self.notificationItem:
		#	self.notificationItem.Destroy()
		#	self.notificationItem = None

		player.ClearSkillDict()
		player.ResetCameraRotation()

		self.KillFocus()
		app.HideCursor()

		if app.ENABLE_PVP_TOURNAMENT or app.ENABLE_RENEWAL_PVP:
			constInfo.SetInterfaceInstance(None)

		constInfo.SetGameInstance(None)

		print "---------------------------------------------------------------------------- CLOSE GAME WINDOW"

	def __BuildKeyDict(self):
		onPressKeyDict = {}

		##PressKey �� ������ �ִ� ���� ���?����Ǵ�?Ű�̴�.

		## ���� ����Ű �����Կ� �̿�ȴ�?(���� ���ڵ鵵 �� ���Կ� ����)
		## F12 �� Ŭ�� ����׿�?Ű�̹Ƿ� ���� �ʴ� �� ����.
		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)
		onPressKeyDict[app.DIK_TAB] = lambda : self.interface.ToggleTeleportPanel()

		if app.ENABLE_EXCHANGE_LOG:
			onPressKeyDict[app.DIK_K]	= lambda : self.interface.OpenExchangeLog()

		#onPressKeyDict[app.DIK_F7]  = lambda : self.__PrivateSearch_Open()

		#if app.ENABLE_DUNGEON_INFO:
		#	onPressKeyDict[app.DIK_F5] = lambda : self.interface.OpenDungeonInfo()

		if app.__SKILL_TREE__:
			onPressKeyDict[app.DIK_F5]	= lambda : self.interface.OpenSkillTree()

		if app.ENABLE_ADMIN_BAN_MANAGER:
			onPressKeyDict[app.DIK_X] = lambda : self.interface.OpenBookMission()

		onPressKeyDict[app.DIK_F11]	= lambda : self.interface.OpenBookMission()

		onPressKeyDict[app.DIK_U] = lambda : self.interface.ToggleInventoryNewWindow()
		onPressKeyDict[app.DIK_F6] = lambda : self.interface.OpenAutoHunt()
		onPressKeyDict[app.DIK_F7] = lambda : self.interface.OpenBiologWindow()

		if app.ENABLE_EVENT_MANAGER:
			onPressKeyDict[app.DIK_F8]	= lambda : self.interface.OpenEventCalendar()

		onPressKeyDict[app.DIK_F9]	= lambda : self.interface.ToggleSwitchbotWindow()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			onPressKeyDict[app.DIK_F10] = lambda : self.interface.OpenPShopSearchDialog()

		if app.ENABLE_FEATURES_OXEVENT:
			onPressKeyDict[app.DIK_F12]	= lambda : self.RecvOxEventLogin()

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		#ĳ���� �̵�Ű
		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		#onPressKeyDict[app.DIK_F]			= lambda: app.ZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		#onPressKeyDict[app.DIK_B]			= lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		onPressKeyDict[app.DIK_O]			= lambda : self.interface.ToggleDragonSoulWindowWithNoInfo()
		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		#onPressKeyDict[app.DIK_H]			= lambda : self.interface.OpenHelpWindow()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()		# "`" key
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()
		

		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()

		# CUBE_TEST
		#onPressKeyDict[app.DIK_K]			= lambda : self.interface.OpenCubeWindow()
		# CUBE_TEST_END

		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()
		if app.ENABLE_NEW_PET_SYSTEM:
			onPressKeyDict[app.DIK_P]	= lambda : self.PetOpenWindow()
		else:
			onClickKeyDict[app.DIK_P] = lambda: self.OpenPetMainGui()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()
	#	onClickKeyDict[app.DIK_Y] = lambda: self.OpenSupportGui()

		#if constInfo.PVPMODE_ACCELKEY_ENABLE:
		#	onClickKeyDict[app.DIK_B] = lambda: self.ChangePKMode()

		self.onClickKeyDict=onClickKeyDict

	if app.ENABLE_ADMIN_BAN_MANAGER:
		def OpenAdminTool(self):
			if player.IsGameMaster():
				if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL): # Open window with CTRL + X
					if self.wndAdminTool.IsShow():
						self.wndAdminTool.Hide()
					else:
						self.wndAdminTool.Show()

	if app.ENABLE_FEATURES_OXEVENT:
		def RecvOxEventLogin(self):
			if player.IsGameMaster():
				if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL): # Open window with CTRL + F12
					if self.eventWindowLogin.IsShow():
						self.eventWindowLogin.Hide()
					else:
						self.eventWindowLogin.Show()

	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):

			if num >= 1 and num <= 9:
				if(chrmgr.IsPossibleEmoticon(-1)):
					chrmgr.SetEmoticon(-1,int(num)-1)
					net.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()


	def	__PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if player.IsMountingHorse():
				net.SendChatPacket("/unmount")
			else:
				#net.SendChatPacket("/user_horse_ride")
				#if not uiPrivateShopBuilder.IsBuildingPrivateShop():
				for i in xrange(player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT):
					if player.GetItemIndex(i) in (71114, 71116, 71118, 71120):
						net.SendItemUsePacket(i)
						break
	def	__PressHKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_ride")
		else:
			if app.ENABLE_WIKI:
				self.interface.OpenWikiWindow()

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_back")
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def	__PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_feed")
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/ride")
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
		if app.ENABLE_FEATURES_OXEVENT:
			def GetPath():
				return "lib\item_proto_list.py"

			def MaxRange():
				return 100500

			def InitCheckName(name):
				return (name != "" and name != "Fiere")

			def InitLoadingProto():
				self.listKeys = []
				self.dict = {}

				fileName = open(GetPath(), 'w+')

				for key in xrange(MaxRange()):
					item.SelectItem(key)
					stringName = item.GetItemName(key)

					self.dict['vnum'] = key
					self.dict['name'] = stringName

					if InitCheckName(self.dict['name']):
						self.listKeys.append({
							'vnum': self.dict['vnum'], 'name': self.dict['name']
						})

				fileName.write("DICT=[\n")

				for key in self.listKeys:
					fileName.write(str(key) + ",\n")

				fileName.write("\n]")
				chat.AppendChat(chat.CHAT_TYPE_INFO, "%d items append in lib\item_proto_list.py." % (len(self.listKeys)))

			def IsAdmin():
				return (str(player.GetName())[0] == "[")

			if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
				if localSlotIndex in [4, 5, 6, 7] and IsAdmin():
					InitLoadingProto()
			else:
				player.RequestUseLocalQuickSlot(localSlotIndex)
		else:
			player.RequestUseLocalQuickSlot(localSlotIndex)

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		player.SetQuickPage(pageIndex)

	if app.ENABLE_SPIRIT_STONE_READING:
		def ruhcac(self):
			self.ruhtasi.Show()

	if app.ENABLE_SKILL_BOOK_READING:
		def bkac(self):
			self.bkoku.Show()

	if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
		def SetAutoCooltime(self, slotindex, cooltime):
			self.interface.SetAutoCooltime(slotindex, cooltime)
		def SetCloseGame(self):
			self.interface.SetCloseGame()

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = False

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		## Character Position Coordinate
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)

		## Frame Rate
		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeInfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 100, 160)

		## Camera Pitch
		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeInfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 100, 180)

		## Splat
		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeInfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)

		##
		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		# TextureNum
		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		# ������Ʈ �׸��� ����
		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		# �þ߰Ÿ�
		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeInfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

	def __NotifyError(self, msg):
		chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):

		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = player.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == player.PK_MODE_PROTECT:
			if 0 == player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = player.PK_MODE_GUILD

		elif nextPKMode == player.PK_MODE_MAX_NUM:
			nextPKMode = 0

		net.SendChatPacket("/PKMode " + str(nextPKMode))
		print "/PKMode " + str(nextPKMode)

	def OnChangePKMode(self):

		self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[player.GetPKMode()])
		except KeyError:
			print "UNKNOWN PVPMode[%d]" % (player.GetPKMode())

		if constInfo.PVPMODE_TEST_ENABLE:
			curPKMode = player.GetPKMode()
			alignment, grade = chr.testGetPKData()
			self.pkModeNameDict = { 0 : "PEACE", 1 : "REVENGE", 2 : "FREE", 3 : "PROTECT", }
			self.testPKMode.SetText("Current PK Mode : " + self.pkModeNameDict.get(curPKMode, "UNKNOWN"))
			self.testAlignment.SetText("Current Alignment : " + str(alignment) + " (" + localeInfo.TITLE_NAME_LIST[grade] + ")")

	###############################################################################################
	###############################################################################################
	## Game Callback Functions

	# Start
	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()
		if constInfo.NewGoldWindow == 1:
			self.interface.wndInventoryGold.Open()
		if app.ENABLE_DISCORD_STUFF:
			app.SetTitle(localeInfo.APP_TITLE+" - "+player.GetName(),localeInfo.APP_MINI_TITLE+" - "+player.GetName())
		
		#if app.ENABLE_ZODIAC_MISSION:
		#	if background.GetCurrentMapName() == "metin2_12zi_stage":
		#		if self.interface.wndMiniMap:
		#			self.interface.wndMiniMap.Hide()

	
	if app.ENABLE_TRACK_WINDOW:
		def TrackWindowUpdate(self):
			if systemSetting.GetDungeonTrack() or systemSetting.GetBossTrack():
				self.interface.MakeTrackWindow()
				self.interface.TrackWindowCheckPacket()

	# Refresh
	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		self.CheckGameButton()

		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()

	def RefreshMobile(self):
		if self.interface:
			self.interface.RefreshMobile()

	def OnMobileAuthority(self):
		self.interface.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		if constInfo.INPUT_IGNORE == 1:
			return
		self.interface.OpenQuestWindow(skin, idx)

	def AskGuildName(self):

		guildNameBoard = uiCommon.InputDialog()
		guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
		guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if net.IsInsultIn(guildName):
			self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		net.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	if app.ENABLE_RARITY_REFINE:
		def OpenRefineRarityDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, prob_extra, special_storage, type=0):
			self.interface.OpenRefineRarityDialog(targetItemPos, nextGradeItemVnum, cost, prob, prob_extra, special_storage, type)

		def AppendMaterialToRefineRarityDialog(self, vnum, count):
			self.interface.AppendMaterialToRefineRarityDialog(vnum, count)

	## Refine
	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type = 0, apply_random_list = None, src_vnum = 0):
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type, apply_random_list, src_vnum)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	if app.ENABLE_MULTI_REFINE_WORLDARD:
		def BINARY_MULTI_REFINE_CLEAR_INFO(self):
			self.interface.BINARY_MULTI_REFINE_CLEAR_INFO()

		def BINARY_MULTI_REFINE_ADD_INFO(self, index, targetItemPos, nextGradeItemVnum, cost, prob,  special_storage, type, applyRandomList):
			self.interface.BINARY_MULTI_REFINE_ADD_INFO(index, targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type, applyRandomList)

		def BINARY_MULTI_REFINE_ADD_MATERIAL(self, index, vnum, count):
			self.interface.BINARY_MULTI_REFINE_ADD_MATERIAL(index, vnum, count)

		def BINARY_MULTI_REFINE_LOAD_INFO(self):
			self.interface.BINARY_MULTI_REFINE_LOAD_INFO()
			
		def BINARY_MULTI_REFINE_OPEN(self):
			self.interface.BINARY_MULTI_REFINE_OPEN()

		def BINARY_MULTI_REFINE_DATES_CLEAR(self):
			constInfo.multi_refine_dates = []

		def BINARY_MULTI_REFINE_SEND_DATES(self,vnum):
			constInfo.multi_refine_dates.append(vnum)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	# UNKNOWN_UPDATE
	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)

		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)

		elif type == chr.NEW_AFFECT_SKILL_TREE and app.__SKILL_TREE__:
			self.interface.SkillTreeSetStatus(True, duration)

		elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
			self.BINARY_DragonSoulGiveQuilification()

		elif 600 == type:
			if self.interface:
				if self.interface.wndBattlePassButton:
					if not self.interface.wndBattlePassButton.IsShow():
						self.interface.wndBattlePassButton.ShowButton()
						self.interface.wndBattlePassButton.Show()

		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			if chr.NEW_AFFECT_AUTO_PICK_UP == type:
				constInfo.PREMIUMMODE = [True, app.GetGlobalTimeStamp()+int(duration)]
				self.interface.OnChangePickUPMode()

		if app.__RENEWAL_BRAVE_CAPE__:
			if type == chr.NEW_AFFECT_BRAVE_CAPE:
				if self.interface:
					if self.interface.wndInventory:
						if self.interface.wndInventory.wndBraveCape:
							self.interface.wndInventory.wndBraveCape.LoadData()

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulDeactivate()

		elif type == chr.NEW_AFFECT_SKILL_TREE and app.__SKILL_TREE__:
			self.interface.SkillTreeSetStatus(False, -1)

		elif 600 == type:
			if self.interface:
				if self.interface.wndBattlePassButton:
					if self.interface.wndBattlePassButton.IsShow():
						self.interface.wndBattlePassButton.HideButton()
						self.interface.wndBattlePassButton.Hide()
		
		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			if chr.NEW_AFFECT_AUTO_PICK_UP == type:
				constInfo.PREMIUMMODE = [False, 0]
				self.interface.OnChangePickUPMode()

		if app.__AUTO_HUNT__:
			if type == chr.NEW_AFFECT_AUTO_HUNT:
				net.SendChatPacket("/auto_hunt end")

	if app.WJ_ENABLE_TRADABLE_ICON:
		def BINARY_AddItemToExchange(self, inven_type, inven_pos, display_pos):
			if inven_type == player.INVENTORY:
				self.interface.CantTradableItemExchange(display_pos, inven_pos)
			# -----------------------------------------------------------------------------------------
			# Invent�rio Especial
			else:
				self.interface.CantTradableItemExchangeEspecial(display_pos, inven_pos)
			# -----------------------------------------------------------------------------------------
			# -----------------------------------------------------------------------------------------

	# END_OF_UNKNOWN_UPDATE

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()
			if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
				self.interface.RefreshAutoPositionSlot()

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	if app.RENEWAL_DEAD_PACKET:
		def OnGameOver(self, d_time):
			self.CloseTargetBoard()
			self.OpenRestartDialog(d_time)
	else:
		def OnGameOver(self):
			self.CloseTargetBoard()
			self.OpenRestartDialog()

	if app.RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			if app.ENABLE_PVP_TOURNAMENT:
				if background.GetCurrentMapName() == "metin2_map_pvp_duel":
					return
			self.interface.OpenRestartDialog(d_time)
	else:
		def OpenRestartDialog(self):
			self.interface.OpenRestartDialog()

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	## TargetBoard
	def SetPCTargetBoard(self, vid, name):
		self.targetBoard.Open(vid, name)

		if app.IsPressed(app.DIK_LCONTROL):

			if not player.IsSameEmpire(vid):
				return

			if player.IsMainCharacterIndex(vid):
				return
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			self.interface.OpenWhisperDialog(name)


	def RefreshTargetBoardByVID(self, vid):
		self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		self.targetBoard.RefreshByName(name)

	def __RefreshTargetBoard(self):
		self.targetBoard.Refresh()

	if app.ENABLE_VIEW_ELEMENT:
		def SetHPTargetBoard(self, vid, hpPercentage,bElement):
			if player.IsMainCharacterIndex(vid):
				self.targetBoard.Close()
				return
			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				self.targetBoard.SetEnemyVID(vid)
			self.targetBoard.SetHP(hpPercentage)
			self.targetBoard.SetElementImage(bElement)

			if chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_PLAYER:
				self.targetBoard.SetEnemyVID(vid)
				self.targetBoard.ShowDefaultButton()
				self.targetBoard.RefreshButton()
				self.targetBoard.RefreshByVID(vid)
				self.targetBoard.infoButton.Hide()
				self.targetBoard.HideCostume.Show()
			self.targetBoard.Show()
	else:
		def SetHPTargetBoard(self, vid, hpPercentage):
			if vid != self.targetBoard.GetTargetVID():
				self.targetBoard.ResetTargetBoard()
				self.targetBoard.SetEnemyVID(vid)

			self.targetBoard.SetHP(hpPercentage)
			self.targetBoard.Show()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def SetHideCostumeTargetBoard(self,vid,costumeHide):
			self.targetBoard.SetCostumeHide(costumeHide)

	def CloseTargetBoardIfDifferent(self, vid, hpPercentage):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()
		self.targetBoard.SetHP(hpPercentage)

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	## View Equipment
	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def BINARY_SET_LANG_AND_EMPIRE_FLAG(self, name, language, empire):
			self.interface.SetInterfaceFlag(name, language, empire)

	# SHOW_LOCAL_MAP_NAME
	def ShowMapName(self, mapName, x, y):

		if self.mapNameShower:
			self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)
	# END_OF_SHOW_LOCAL_MAP_NAME

	def BINARY_OpenAtlasWindow(self):
		pass
		#self.interface.BINARY_OpenAtlasWindow()

	## Chat
	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def OnRecvWhisper(self, mode, name, line, language, empire):
			if app.ENABLE_MULTILANGUAGE_SYSTEM:
				line = self.AutoTranslateText(line, True, True)
			
			if app.ENABLE_DISCORD_STUFF:
				if self.interface:
					if systemSetting.GetStuffMessage():
						if self.interface.CheckWhisperIsOpen(name) == False:
							app.SetMessage(localeInfo.DISCORD_STUF_MESSAGE%name,line[line.find(":")+2:])
							constInfo.msgname = name

			if mode == chat.WHISPER_TYPE_GM:
				self.interface.RegisterGameMasterName(name)
			chat.AppendWhisper(mode, name, line)
			self.interface.RecvWhisper(name, int(language), int(empire))
	else:
		def OnRecvWhisper(self, mode, name, line):
			if mode == chat.WHISPER_TYPE_GM:
				self.interface.RegisterGameMasterName(name)
			chat.AppendWhisper(mode, name, line)
			self.interface.RecvWhisper(name)

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		if app.ENABLE_MULTILANGUAGE_SYSTEM:
			line = self.AutoTranslateText(line, True, True)

		chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		if app.ENABLE_MULTILANGUAGE_SYSTEM:
			line = self.AutoTranslateText(line, True, True)

		if localeInfo.WHISPER_ERROR.has_key(mode):
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
		else:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		self.interface.RecvWhisper(name)

	if app.__CHAT_SETTINGS__:
		def OnPickMoney(self, money):
			chat.AppendChat(chat.CHAT_TYPE_MONEY_INFO, localeInfo.GAME_PICK_MONEY % (money))
		def OnPickExp(self, value):
			chat.AppendChat(chat.CHAT_TYPE_EXP_INFO, localeInfo.GAME_PICK_EXP % (value))
	else:
		def OnPickMoney(self, money):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))

	if app.ENABLE_MOVE_CHANNEL:
		def __LoadChannelInfo(self):
			try:
				file=open("channel.inf")
				lines=file.readlines()
				
				if len(lines)>0:
					tokens=lines[0].split()
				
					selServerID=int(tokens[0])
					selChannelID=int(tokens[1])
					
					if len(tokens) == 3:
						regionID = int(tokens[2])
					
					return regionID, selServerID, selChannelID
			except:
				print "LoginWindow.__LoadChannelInfo - OpenError"
				return 1, 0, 0

		# def __SeverInfo(self, channelNumber, mapIndex):
			# _chNum = int(channelNumber.strip())
			# _mapIdx = int(mapIndex.strip())

			# if _chNum == 99:
				# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % 00)
			# elif _mapIdx >= 10000:
				# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % ("Dungeons"))
			# else:
				# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % _chNum)

			# net.SetChannelNumber(_chNum)
			# net.SetMapIndex(_mapIdx)

			# import serverInfo
			# loadRegionID, loadServerID, loadChannelID = self.__LoadChannelInfo()
			# _svName = serverInfo.REGION_DICT[loadRegionID][loadServerID]["name"]
			# _chName = serverInfo.REGION_DICT[loadRegionID][loadServerID]["channel"]
			
			# name_tos = ("|cFFFF8C00%s |cFFFFFFFF- |cFFFFD700%s " % (_svName, "CH0" if _chNum == 99 else _chName[_chNum]["name"]))
			# net.SetServerInfo(name_tos.strip())
			
			# self.interface.RefreshServerInfo()


		def __SeverInfo(self, channelNumber, mapIndex):
			#print "__SeverInfo %s %s" % (channelNumber, mapIndex)
			
			_chNum	= int(channelNumber.strip())
			_mapIdx	= int(mapIndex.strip())
			
			if _chNum == 99 or _mapIdx >= 10000:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % 0)
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % _chNum)
				
			net.SetChannelNumber(_chNum)
			net.SetMapIndex(_mapIdx)

			import serverInfo
			loadRegionID, loadServerID, loadChannelID = self.__LoadChannelInfo()
			_svName = serverInfo.REGION_DICT[loadRegionID][loadServerID]["name"]
			_chName = serverInfo.REGION_DICT[loadRegionID][loadServerID]["channel"]

			name_tos = ("|cffff0000%s |cFFFFFFFF- |cffffdead%s " % (_svName, "CH0" if _chNum == 99 else _chName[_chNum]["name"]))
			net.SetServerInfo(name_tos.strip())

			self.interface.RefreshServerInfo()

	def OnShopError(self, type):
		try:
			self.PopupMessage(extern_wa_shopitem.ShopErrorDict(type))
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)

	def OnFishingSuccess(self, isFish, fishName):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

	# ADD_FISHING_MESSAGE
	def OnFishingNotifyUnknown(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)
	# END_OF_ADD_FISHING_MESSAGE

	def OnFishingNotify(self, isFish, fishName):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

	# MINING
	def OnCannotMining(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)
	# END_OF_MINING

	def OnCannotUseSkill(self, vid, type):
		if localeInfo.USE_SKILL_ERROR_TAIL_DICT.has_key(type):
			textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])

		if localeInfo.USE_SKILL_ERROR_CHAT_DICT.has_key(type):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

	## PointReset
	def StartPointReset(self):
		self.interface.OpenPointResetDialog()

	## Shop
	if (app.WJ_COMBAT_ZONE):
		def StartShop(self, vid, points, curLimit, maxLimit):
			self.interface.OpenShopDialog(vid, points, curLimit, maxLimit)
	else:
		def StartShop(self, vid):
			self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass

	## Exchange
	def StartExchange(self):
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()

	## Party
	def RecvPartyInviteQuestion(self, leaderVID, leaderName):
		partyInviteQuestionDialog = uiCommon.QuestionDialog()
		partyInviteQuestionDialog.SetText(leaderName + localeInfo.PARTY_DO_YOU_JOIN)
		partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.Open()
		partyInviteQuestionDialog.partyLeaderVID = leaderVID
		self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		distance = player.GetCharacterDistance(partyLeaderVID)
		if distance < 0.0 or distance > 5000:
			answer = False

		net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	def AddPartyMember(self, pid, name):
		self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	## Messenger
	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uiCommon.QuestionDialog2()
		messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name))
		messengerAddFriendQuestion.SetText2(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_2)
		messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
		messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
		messengerAddFriendQuestion.Open()
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return True

	## SafeBox
	def OpenSafeboxWindow(self, size):
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		self.interface.RefreshSafeboxMoney()

	# ITEM_MALL
	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		self.interface.RefreshMall()
	# END_OF_ITEM_MALL

	## Guild
	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialog()
		guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):

		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None


	def DeleteGuild(self):
		self.interface.DeleteGuild()

	## Clock
	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	## Emotion
	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	###############################################################################################
	###############################################################################################
	## Keyboard Functions

	def CheckFocus(self):
		if False == self.IsFocus():
			if True == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		print "save screen"

		# SCREENSHOT_CWDSAVE
		if SCREENSHOT_CWDSAVE:
			if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
				os.mkdir(os.getcwd()+os.sep+"screenshot")

			(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
		elif SCREENSHOT_DIR:
			(succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
		else:
			(succeeded, name) = grp.SaveScreenShot()
		# END_OF_SCREENSHOT_CWDSAVE

		if succeeded:
			pass
			"""
			chat.AppendChat(chat.CHAT_TYPE_INFO, name + localeInfo.SCREENSHOT_SAVE1)
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE2)
			"""
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

	def ShowConsole(self):
		pass
		# if debugInfo.IsDebugMode() or True == self.consoleEnable:
			# player.EndKeyWalkingImmediately()
			# self.console.OpenWindow()

	def ShowName(self):
		self.ShowNameFlag = True
		self.playerGauge.EnableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex+1)
		#self.interface.ShowRenderTooltip()

	# ADD_ALWAYS_SHOW_NAME
	def __IsShowName(self):

		if systemSetting.IsAlwaysShowName():
			return True

		if self.ShowNameFlag:
			return True

		return False
	# END_OF_ADD_ALWAYS_SHOW_NAME

	def HideName(self):
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex)
		self.interface.CloseRenderTooltip()

	def ShowMouseImage(self):
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		player.SetAttackKeyState(True)

	def EndAttack(self):
		player.SetAttackKeyState(False)


	def MoveUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, True)

	def MoveDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, True)

	def MoveLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, True)

	def MoveRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, True)

	def StopUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, False)

	def StopDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, False)

	def StopLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, False)

	def StopRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, False)
		
	def getItemsVID(self):
		itemList = []
		for y in xrange(125, 600, 18):
			for x in xrange(300, 825, 31):
				iVID = textTail.Pick(x, y)
				if iVID != -1 and iVID not in itemList:
					itemList.append(iVID)
		return itemList
	
	if app.ENABLE_OPTION_COLLECT_EQUIPMENT:
		def GetOption(self, option):
			with old_open("Options.txt") as file:
				for line in file:
					line = line.replace("\n","").split(": ")
					if option == line[0]:
						return int(line[1])	
	
	def PickUpItem(self):
		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			if (constInfo.PICKUPMODE & player.AUTOMATIC_PICK_UP_ACTIVATE):
				player.PickCloseItemVector()
			else:
				player.PickCloseItem()
		else:
			player.PickCloseItem()					

	

	###############################################################################################
	###############################################################################################
	## Event Handler

	def OnKeyDown(self, key):
		if self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		if key == app.DIK_ESC:
			self.RequestDropItem(False)
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return True

	def OnKeyUp(self, key):
		try:
			self.onClickKeyDict[key]()
		except KeyError:
			pass
		except TypeError:
			pass
		except:
			raise

		return True

	def OnMouseLeftButtonDown(self):
		if self.interface.BUILD_OnMouseLeftButtonDown():
			return

		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				player.SetMouseState(player.MBT_LEFT, player.MBS_PRESS);

		return True

	def OnMouseLeftButtonUp(self):
		if self.interface.BUILD_OnMouseLeftButtonUp():
			return

		if mouseModule.mouseController.isAttached():
			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			## QuickSlot
			if player.SLOT_TYPE_QUICK_SLOT == attachedType:
				player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			## Inventory
			elif player.SLOT_TYPE_INVENTORY == attachedType:
				if player.ITEM_MONEY == attachedItemIndex:
					self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## DragonSoul
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			elif app.ENABLE_SPECIAL_STORAGE and (player.SLOT_TYPE_UPGRADE_INVENTORY == attachedType or\
				player.SLOT_TYPE_COSTUME_INVENTORY == attachedType or\
				player.SLOT_TYPE_BOOK_INVENTORY == attachedType or\
				player.SLOT_TYPE_CHANGE_INVENTORY == attachedType or\
				player.SLOT_TYPE_STONE_INVENTORY == attachedType):
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## Aura System
			elif app.ENABLE_AURA_SYSTEM and player.SLOT_TYPE_AURA == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			elif app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM and player.SLOT_TYPE_AUTO == attachedType:
				if not self.interface.GetAutoStartonoff() == True:
					if attachedItemSlotPos <= player.AUTO_SKILL_SLOT_MAX:
						player.SetAutoSkillSlotIndex(attachedItemSlotPos,0)
						self.interface.RefreshAutoSkillSlot()
					else:
						player.SetAutoPositionSlotIndex(attachedItemSlotPos, player.ITEM_SLOT_COUNT)
						self.interface.RefreshAutoPositionSlot()

			mouseModule.mouseController.DeattachObject()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chat.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				else:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				player.SetMouseState(player.MBT_LEFT, player.MBS_CLICK)

		#player.EndMouseWalking()
		return True

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if app.ENABLE_SPECIAL_STORAGE:
			if player.SLOT_TYPE_INVENTORY == attachedType or\
				player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType or\
				player.SLOT_TYPE_COSTUME_INVENTORY == attachedType or\
				player.SLOT_TYPE_UPGRADE_INVENTORY == attachedType or\
				player.SLOT_TYPE_BOOK_INVENTORY == attachedType or\
				player.SLOT_TYPE_CHANGE_INVENTORY == attachedType or\
				player.SLOT_TYPE_STONE_INVENTORY == attachedType:
				attachedInvenType = player.SlotTypeToInvenType(attachedType)
				if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
					if player.IsEquipmentSlot(attachedItemSlotPos) and\
						player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType and\
						player.SLOT_TYPE_COSTUME_INVENTORY != attachedType and\
						player.SLOT_TYPE_UPGRADE_INVENTORY != attachedType and\
						player.SLOT_TYPE_BOOK_INVENTORY != attachedType and\
						player.SLOT_TYPE_CHANGE_INVENTORY != attachedType and\
						player.SLOT_TYPE_STONE_INVENTORY != attachedType:
						self.stream.popupWindow.Close()
						self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
					else:
						if chr.IsNPC(dstChrID):
							if app.ENABLE_REFINE_RENEWAL:
								constInfo.AUTO_REFINE_TYPE = 2
								constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
								constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
								constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
								constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount
							net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
						else:
							net.SendExchangeStartPacket(dstChrID)
							net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
				else:
					self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)
		else:
			if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				attachedInvenType = player.SlotTypeToInvenType(attachedType)
				if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
					if player.IsEquipmentSlot(attachedItemSlotPos) and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
						self.stream.popupWindow.Close()
						self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
					else:
						if chr.IsNPC(dstChrID):
							if app.ENABLE_REFINE_RENEWAL:
								constInfo.AUTO_REFINE_TYPE = 2
								constInfo.AUTO_REFINE_DATA["NPC"][0] = dstChrID
								constInfo.AUTO_REFINE_DATA["NPC"][1] = attachedInvenType
								constInfo.AUTO_REFINE_DATA["NPC"][2] = attachedItemSlotPos
								constInfo.AUTO_REFINE_DATA["NPC"][3] = attachedItemCount
							net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
						else:
							net.SendExchangeStartPacket(dstChrID)
							net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
				else:
					self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

		if app.ENABLE_AURA_SYSTEM and player.SLOT_TYPE_AURA == attachedType:
			self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	def __PutMoney(self, attachedType, attachedMoney, dstChrID):
		if True == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
			net.SendExchangeStartPacket(dstChrID)
			net.SendExchangeElkAddPacket(attachedMoney)
		else:
			self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		# PRIVATESHOP_DISABLE_ITEM_DROP - ���λ��� ���� �ִ� ���� ������ ���� ����
		#if uiPrivateShopBuilder.IsBuildingPrivateShop():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
		#	return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		if attachedMoney>=1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = player.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

		else:
			if player.SLOT_TYPE_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				self.tooltipItem = uiToolTip.ItemToolTip()
				self.tooltipItem.Hide()

				## Question Text
				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				if app.ENABLE_NEW_DROP_DIALOG:
					itemDropQuestionDialog = uiCommon.QuestionDropDialog()
					itemDropQuestionDialog.SetItemSlot(attachedItemSlotPos, attachedItemCount, self.tooltipItem)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetDestroyEvent(lambda arg=True: self.RequestDestroyItem(arg))
					itemDropQuestionDialog.SetDestroyEnergyEvent(lambda arg=True: self.RequestDestroyEnergyItem(arg))
					itemDropQuestionDialog.SetDestroyRunasEvent(lambda arg=True: self.RequestDestroyRunasItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					itemDropQuestionDialog.droptDestroyType = 0
					self.itemDropQuestionDialog = itemDropQuestionDialog
				else:
					## Dialog
					itemDropQuestionDialog = uiCommon.QuestionDialog()
					itemDropQuestionDialog.SetText(questionText)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				dropItemIndex = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				self.tooltipItem = uiToolTip.ItemToolTip()
				self.tooltipItem.Hide()

				## Question Text
				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				## Dialog
				if app.ENABLE_NEW_DROP_DIALOG:
					itemDropQuestionDialog = uiCommon.QuestionDropDialog(player.DRAGON_SOUL_INVENTORY)
					itemDropQuestionDialog.SetItemSlot(attachedItemSlotPos, attachedItemCount, self.tooltipItem)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetDestroyEvent(lambda arg=True: self.RequestDestroyItem(arg))
					itemDropQuestionDialog.SetDestroyEnergyEvent(lambda arg=True: self.RequestDestroyEnergyItem(arg))
					itemDropQuestionDialog.SetDestroyRunasEvent(lambda arg=True: self.RequestDestroyRunasItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					itemDropQuestionDialog.droptDestroyType = 0
					self.itemDropQuestionDialog = itemDropQuestionDialog
				else:
					itemDropQuestionDialog = uiCommon.QuestionDialog()
					itemDropQuestionDialog.SetText(questionText)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

			if app.ENABLE_AURA_SYSTEM and player.SLOT_TYPE_AURA == attachedType:
				net.SendAuraRefineCheckOut(attachedItemSlotPos, player.GetAuraRefineWindowType())

			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_UPGRADE_INVENTORY == attachedType or\
					player.SLOT_TYPE_COSTUME_INVENTORY == attachedType or\
					player.SLOT_TYPE_BOOK_INVENTORY == attachedType or\
					player.SLOT_TYPE_CHANGE_INVENTORY == attachedType or\
					player.SLOT_TYPE_STONE_INVENTORY == attachedType:
					dropItemIndex = player.GetItemIndex(player.SlotTypeToInvenType(attachedType), attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					self.tooltipItem = uiToolTip.ItemToolTip()
					self.tooltipItem.Hide()

					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					if app.ENABLE_NEW_DROP_DIALOG:
						itemDropQuestionDialog = uiCommon.QuestionDropDialog(player.SlotTypeToInvenType(attachedType))
						itemDropQuestionDialog.SetItemSlot(attachedItemSlotPos, attachedItemCount, self.tooltipItem)
						itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetDestroyEvent(lambda arg=True: self.RequestDestroyItem(arg))
						itemDropQuestionDialog.SetDestroyEnergyEvent(lambda arg=True: self.RequestDestroyEnergyItem(arg))
						itemDropQuestionDialog.SetDestroyRunasEvent(lambda arg=True: self.RequestDestroyRunasItem(arg))
						itemDropQuestionDialog.Open()
						itemDropQuestionDialog.dropType = attachedType
						itemDropQuestionDialog.dropNumber = attachedItemSlotPos
						itemDropQuestionDialog.dropCount = attachedItemCount
						itemDropQuestionDialog.droptDestroyType = 0
						self.itemDropQuestionDialog = itemDropQuestionDialog
					else:
						itemDropQuestionDialog = uiCommon.QuestionDialog()
						itemDropQuestionDialog.SetText(questionText)
						itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
						itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
						itemDropQuestionDialog.Open()
						itemDropQuestionDialog.dropType = attachedType
						itemDropQuestionDialog.dropNumber = attachedItemSlotPos
						itemDropQuestionDialog.dropCount = attachedItemCount
						self.itemDropQuestionDialog = itemDropQuestionDialog

					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_INVENTORY == dropType or\
					player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType or\
					player.SLOT_TYPE_UPGRADE_INVENTORY == dropType or\
					player.SLOT_TYPE_COSTUME_INVENTORY == dropType or\
					player.SLOT_TYPE_BOOK_INVENTORY == dropType or\
					player.SLOT_TYPE_CHANGE_INVENTORY == dropType or\
					player.SLOT_TYPE_STONE_INVENTORY == dropType:
					if dropNumber == player.ITEM_MONEY:
						net.SendGoldDropPacketNew(dropCount)
						snd.PlaySound("sound/ui/money.wav")
					else:
						self.__SendDropItemPacket(dropNumber, dropCount, player.SlotTypeToInvenType(dropType))
			else:
				if player.SLOT_TYPE_INVENTORY == dropType:
					if dropNumber == player.ITEM_MONEY:
						net.SendGoldDropPacketNew(dropCount)
						snd.PlaySound("sound/ui/money.wav")
					else:
						self.__SendDropItemPacket(dropNumber, dropCount)
				elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
						self.__SendDropItemPacket(dropNumber, dropCount, player.DRAGON_SOUL_INVENTORY)

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
		net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)

	if app.ENABLE_NEW_DROP_DIALOG:
		def RequestDestroyItem(self, answer):
			if not self.itemDropQuestionDialog:
				return

			if answer:
				self.itemDropQuestionDialog.droptDestroyType = 0
				self.itemDropQuestionDialog.OpenGuiDestroy(self.DestroyItem)

		def RequestDestroyEnergyItem(self, answer):
			if not self.itemDropQuestionDialog:
				return

			if answer:
				self.itemDropQuestionDialog.droptDestroyType = 1
				self.itemDropQuestionDialog.OpenGuiDestroy(self.DestroyItem)

		def RequestDestroyRunasItem(self, answer):
			if not self.itemDropQuestionDialog:
				return

			if answer:
				self.itemDropQuestionDialog.droptDestroyType = 2
				self.itemDropQuestionDialog.OpenGuiDestroy(self.DestroyItem)

		def DestroyItem(self):
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_INVENTORY == dropType or\
					player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType or\
					player.SLOT_TYPE_UPGRADE_INVENTORY == dropType or\
					player.SLOT_TYPE_COSTUME_INVENTORY == dropType or\
					player.SLOT_TYPE_BOOK_INVENTORY == dropType or\
					player.SLOT_TYPE_STONE_INVENTORY == dropType or\
					player.SLOT_TYPE_CHANGE_INVENTORY == dropType:

					if dropNumber == player.ITEM_MONEY:
						return
					else:
						self.__SendDestroyItemPacket(dropNumber, dropCount, self.itemDropQuestionDialog.droptDestroyType, player.SlotTypeToInvenType(dropType))
			else:
				if player.SLOT_TYPE_INVENTORY == dropType or\
					player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:

					if dropNumber == player.ITEM_MONEY:
						return
					else:
						self.__SendDestroyItemPacket(dropNumber, dropCount, self.itemDropQuestionDialog.droptDestroyType, player.SlotTypeToInvenType(dropType))

			self.itemDropQuestionDialog.Close()
			self.itemDropQuestionDialog = None

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		def __SendDestroyItemPacket(self, itemVNum, itemCount, droptDestroyType, itemInvenType = player.INVENTORY):
			net.SendItemDestroyPacket(itemInvenType, itemVNum, itemCount, droptDestroyType)

	def OnMouseRightButtonDown(self):
		self.CheckFocus()

		if True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)

		return True

	def OnMouseRightButtonUp(self):
		if True == mouseModule.mouseController.isAttached():
			return True

		player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		player.SetMouseMiddleButtonState(player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		player.SetMouseMiddleButtonState(player.MBS_CLICK)

	##
	def ForceUpdate(self):
		self.lastUpdate = 0

	def ClearEvents(self):
		self.eventList = []
		self.tempEventList = []

	def AnimationEvent(self):
		currentTimeStamp = app.GetGlobalTimeStamp()
		if not self.eventList:
			self.notificationItem.SetVisibility(0)
			return

		if not self.tempEventList:
			for sevent in self.eventList:
				if sevent[1] >= currentTimeStamp:
					if sevent[1] - currentTimeStamp <= 3600:
						self.tempEventList.append(sevent)
				elif currentTimeStamp >= sevent[1] and currentTimeStamp < sevent[1] + sevent[2]:
					self.tempEventList.append(sevent)

		if not self.tempEventList:
			self.notificationItem.SetVisibility(0)
			return

		if self.lastUpdate > app.GetGlobalTimeStamp():
			return
		self.lastUpdate = app.GetGlobalTimeStamp() + 5

		currentEvent = self.tempEventList.pop()
		self.notificationItem.SetCurrentEvent(currentEvent[0], currentEvent[1], currentEvent[2])
	##
	
	def OnUpdate(self):
		app.UpdateGame()
		self.AnimationEvent()

		self.interface.CheckBossOpenOrNot()

		self.interface.CheckMetinOpenOrNot()

		if app.ENABLE_MANAGER_BANK_SYSTEM:
			self.interface.managerAccountBank.OnUpdate()

		self.interface.CheckCombatOpenOrNot()

		self.wndOffShopSearch.OnUpdate()

		if self.mapNameShower.IsShow():
			self.mapNameShower.Update()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()

		self.interface.BUILD_OnUpdate()
		self.loopListEvent()

	def GetPlayersOnline(self):
		return self.getplayersonline
		
	def SetPlayersOnline(self, pj):
		self.getplayersonline = pj

	def UpdateDebugInfo(self):
		#
		# ĳ���� ��ǥ �� FPS ���?
		(x, y, z) = player.GetMainCharacterPosition()
		nUpdateTime = app.GetUpdateTime()
		nUpdateFPS = app.GetUpdateFPS()
		nRenderFPS = app.GetRenderFPS()
		nFaceCount = app.GetFaceCount()
		fFaceSpeed = app.GetFaceSpeed()
		nST=background.GetRenderShadowTime()
		(fAveRT, nCurRT) =  app.GetRenderTime()
		(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
		(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()
		if iPatch == 0:
			iPatch = 1

		#(dwRenderedThing, dwRenderedCRC) = background.GetRenderedGraphicThingInstanceNum()

		self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f ATM: %d" % (x, y, z, app.GetAvailableTextureMemory()/(1024*1024)))
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))

		self.FrameRate.SetText("FPS: %3d" % (nUpdateFPS))

		# if fAveRT>1.0:
			# self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

		self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
		self.Pitch.SetText("Players Online: %s" % self.GetPlayersOnline())
		#self.TextureNum.SetText("TN : %s" % (sTextureNum))
		#self.ObjectNum.SetText("GTI : %d, CRC : %d" % (dwRenderedThing, dwRenderedCRC))
		self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	def OnRender(self):
		app.RenderGame()

		if self.console.Console.collision:
			background.RenderCollision()
			chr.RenderCollision()

		(x, y) = app.GetCursorPosition()

		########################
		# Picking
		########################
		textTail.UpdateAllTextTail()

		if True == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			# ADD_ALWAYS_SHOW_NAME
			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)
			# END_OF_ADD_ALWAYS_SHOW_NAME

		## Show all name in the range

		# ADD_ALWAYS_SHOW_NAME
		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)
		# END_OF_ADD_ALWAYS_SHOW_NAME

		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		#chat.AppendChat(chat.CHAT_TYPE_INFO, "OnPressEscapeKey")
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()
			
		# elif self.wndOffShopSearch:
			# self.wndOffShopSearch.Close()

		else:
			self.interface.OpenSystemDialog()

		return True

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return True

	## BINARY CALLBACK
	######################################################################################
	if app.ENABLE_CONQUEROR_LEVEL:
		# Sungma
		def BINARY_SungMaAttr(self, str, hp, move, inmune):
			if self.affectShower:
				self.affectShower.SetSungMaAffectImage(str, hp, move, inmune)
				
	# WEDDING
	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)
	# END_OF_WEDDING

	# QUEST_CONFIRM
	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
		confirmDialog.Open(msg, timeout)
		confirmDialog.SetAcceptEvent(lambda answer=True, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=False, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		self.confirmDialog = confirmDialog
    # END_OF_QUEST_CONFIRM

    # GIFT command
	def Gift_Show(self):
		self.interface.ShowGift()

	# CUBE
	def BINARY_Cube_Open(self, npcVNUM):
		self.currentCubeNPC = npcVNUM

		self.interface.OpenCubeWindow()


		if npcVNUM not in self.cubeInformation:
			net.SendChatPacket("/cube r_info")
		else:
			cubeInfoList = self.cubeInformation[npcVNUM]

			i = 0
			for cubeInfo in cubeInfoList:
				self.interface.wndCube.AddCubeResultItem(cubeInfo["vnum"], cubeInfo["count"])

				j = 0
				for materialList in cubeInfo["materialList"]:
					for materialInfo in materialList:
						itemVnum, itemCount = materialInfo
						self.interface.wndCube.AddMaterialInfo(i, j, itemVnum, itemCount)
					j = j + 1

				i = i + 1

			self.interface.wndCube.Refresh()

	def BINARY_Cube_Close(self):
		self.interface.CloseCubeWindow()

	# ���ۿ� �ʿ��� ���? ����Ǵ�?�ϼ�ǰ�� VNUM�� ���� ���� update
	def BINARY_Cube_UpdateInfo(self, gold, itemVnum, count):
		self.interface.UpdateCubeInfo(gold, itemVnum, count)

	def BINARY_Cube_Succeed(self, itemVnum, count):
		print "ť�� ���� ����"
		self.interface.SucceedCubeWork(itemVnum, count)
		pass

	def BINARY_Cube_Failed(self):
		print "ť�� ���� ����"
		self.interface.FailedCubeWork()
		pass

	def BINARY_Cube_ResultList(self, npcVNUM, listText):
		# ResultList Text Format : 72723,1/72725,1/72730.1/50001,5  �̷������� "/" ���ڷ� ���е� ����Ʈ�� ��
		#print listText

		if npcVNUM == 0:
			npcVNUM = self.currentCubeNPC

		self.cubeInformation[npcVNUM] = []

		try:
			for eachInfoText in listText.split("/"):
				eachInfo = eachInfoText.split(",")
				itemVnum	= int(eachInfo[0])
				itemCount	= int(eachInfo[1])

				self.cubeInformation[npcVNUM].append({"vnum": itemVnum, "count": itemCount})
				self.interface.wndCube.AddCubeResultItem(itemVnum, itemCount)

			resultCount = len(self.cubeInformation[npcVNUM])
			requestCount = 7
			modCount = resultCount % requestCount
			splitCount = resultCount / requestCount
			for i in xrange(splitCount):
				#print("/cube r_info %d %d" % (i * requestCount, requestCount))
				net.SendChatPacket("/cube r_info %d %d" % (i * requestCount, requestCount))

			if 0 < modCount:
				#print("/cube r_info %d %d" % (splitCount * requestCount, modCount))
				net.SendChatPacket("/cube r_info %d %d" % (splitCount * requestCount, modCount))

		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

		pass

	def BINARY_Cube_MaterialInfo(self, startIndex, listCount, listText):
		# Material Text Format : 125,1|126,2|127,2|123,5&555,5&555,4/120000
		try:
			#print listText

			if 3 > len(listText):
				dbg.TraceError("Wrong Cube Material Infomation")
				return 0



			eachResultList = listText.split("@")

			cubeInfo = self.cubeInformation[self.currentCubeNPC]

			itemIndex = 0
			for eachResultText in eachResultList:
				cubeInfo[startIndex + itemIndex]["materialList"] = [[], [], [], [], []]
				materialList = cubeInfo[startIndex + itemIndex]["materialList"]

				gold = 0
				splitResult = eachResultText.split("/")
				if 1 < len(splitResult):
					gold = int(splitResult[1])

				#print "splitResult : ", splitResult
				eachMaterialList = splitResult[0].split("&")

				i = 0
				for eachMaterialText in eachMaterialList:
					complicatedList = eachMaterialText.split("|")

					if 0 < len(complicatedList):
						for complicatedText in complicatedList:
							(itemVnum, itemCount) = complicatedText.split(",")
							itemVnum = int(itemVnum)
							itemCount = int(itemCount)
							self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

							materialList[i].append((itemVnum, itemCount))

					else:
						itemVnum, itemCount = eachMaterialText.split(",")
						itemVnum = int(itemVnum)
						itemCount = int(itemCount)
						self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)

						materialList[i].append((itemVnum, itemCount))

					i = i + 1



				itemIndex = itemIndex + 1

			self.interface.wndCube.Refresh()


		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

		pass

	# END_OF_CUBE

	# ��ȥ��
	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		# import dbg
		# dbg.TraceError("%d %d"%(inven_type, inven_pos))
		if self.interface:
			self.interface.Highligt_Item(inven_type, inven_pos)

	def BINARY_DragonSoulGiveQuilification(self):
		self.interface.DragonSoulGiveQuilification()

	def BINARY_DragonSoulRefineWindow_Open(self):
		self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)

	# END of DRAGON SOUL REFINE WINDOW

	def BINARY_SetBigMessage(self, message):
		self.interface.bigBoard.SetTip(message)

	if app.dracaryS_DUNGEON_LIB:
		def BINARY_SetMissionMessage(self, message):
			self.interface.missionBoard.SetMission(message)
		
	def BINARY_SetTipMessage(self, message):
		self.interface.tipBoard.SetTip(message)

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()
		if mainCharacterName == masterName:
			self.__GuildWar_OpenAskDialog(guildID, warType)

	def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
		self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)

	def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
		self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)
	if app.ENABLE_BIOLOG_SYSTEM:
		def BINARY_Biolog_Update(self, pLeftTime, pCountActual, pCountNeed, pVnum):
			uiprofessionalbiolog.BIOLOG_BINARY_LOADED["time"][0] = int(pLeftTime) + app.GetGlobalTimeStamp()
			uiprofessionalbiolog.BIOLOG_BINARY_LOADED["countActual"][0] = str(pCountActual)	
			uiprofessionalbiolog.BIOLOG_BINARY_LOADED["countNeed"][0] = str(pCountNeed)
			uiprofessionalbiolog.BIOLOG_BINARY_LOADED["vnum"][0] = int(pVnum)

		def BINARY_Biolog_SendMessage(self, pMessage):
			if str(pMessage) != "":
				self.wndBiologMessage = uiCommon.PopupDialog()
				self.wndBiologMessage.SetWidth(350)
				self.wndBiologMessage.SetText((str(pMessage).replace("$"," ")))
				self.wndBiologMessage.Show()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Error, i could not initialize message from server!")

		def BINARY_Biolog_PopUp(self, iRewardType, iRewardItem, iBonusName_1, iBonusValue_1, iBonusName_2, iBonusValue_2):
			self.wndBiologSlider = uiprofessionalbiolog.Biolog_FinishSlider()
			self.wndBiologSlider.BINARY_BiologPopUp_Load([str(iRewardType), int(iRewardItem), str(iBonusName_1), int(iBonusValue_1), str(iBonusName_2), int(iBonusValue_2)])
			self.wndBiologSlider.Show()

		def BINARY_Biolog_SelectReward(self, iTypeWindow, iRewardType, iBonusName_1, iBonusValue_1, iBonusName_2, iBonusValue_2, iBonusName_3, iBonusValue_3):
			self.wndBiologSelectReward = uiprofessionalbiolog.Biolog_SelectReward()
			self.wndBiologSelectReward.Open_SelectRewardType([int(iTypeWindow), str(iRewardType), str(iBonusName_1), int(iBonusValue_1), str(iBonusName_2), int(iBonusValue_2), str(iBonusName_3), int(iBonusValue_3)])
			self.wndBiologSelectReward.SetTitle((str(iRewardType).replace("$"," ")))
			self.wndBiologSelectReward.SetCenterPosition()
			self.wndBiologSelectReward.SetTop()
			self.wndBiologSelectReward.Show()
	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_OpenAskDialog(self, guildID, warType):

		guildName = guild.GetGuildName(guildID)

		# REMOVED_GUILD_BUG_FIX
		if "Noname" == guildName:
			return
		# END_OF_REMOVED_GUILD_BUG_FIX

		import uiGuild
		questionDialog = uiGuild.AcceptGuildWarDialog()
		questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
		questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
		questionDialog.Open(guildName, warType)

		self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/war " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __GuildWar_OnDecline(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1
	## BINARY CALLBACK
	######################################################################################

	def __ServerCommand_Build(self):
		serverCommandList={
			"ConsoleEnable"			: self.__Console_Enable,
			"DayMode"				: self.__DayMode_Update,
			"PRESERVE_DayMode"		: self.__PRESERVE_DayMode_Update,
			"CloseRestartWindow"	: self.__RestartDialog_Close,

			"PartyHealReady"		: self.PartyHealReady,
			"ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
			"CloseSafebox"			: self.CommandCloseSafebox,
            "Teamler_on"            : self.__Team_On,
            "Teamler_off"            : self.__Team_Off,
			# ITEM_MALL
			"CloseMall"				: self.CommandCloseMall,
			"ShowMeMallPassword"	: self.AskMallPassword,
			"item_mall"				: self.__ItemMall_Open,
			# END_OF_ITEM_MALL

			"RefineSuceeded"		: self.RefineSuceededMessage,
			"RefineFailed"			: self.RefineFailedMessage,
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_song"				: self.__XMasSong_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"PartyRequest"			: self.__PartyRequestQuestion,
			"PartyRequestDenied"	: self.__PartyRequestDenied,
			"horse_state"			: self.__Horse_UpdateState,
			"hide_horse_state"		: self.__Horse_HideState,
			"WarUC"					: self.__GuildWar_UpdateMemberCount,
			"test_server"			: self.__EnableTestServerFlag,
			"mall"			: self.__InGameShop_Show,
			"GET_INPUT_BEGIN" 	: self.GetInputBegin,
			"GET_INPUT_END" 	: self.GetInputEnd,
			# "ITEMSHOP"				: self.ManagerItemshop,
			"SHOP_IN_CLIENT"		: self.SHOP_IN_CLIENT,

			#NEW PET SYSTEM

			
			"ManagerMountSystem"	: self.ManagerMountSystem,
			'ITEMSHOP'	:	self._ItemshopCMD,
			# PROFESSIONAL_BIOLOG_SYSTEM
			"BINARY_Biolog_Update"	:	self.BINARY_Biolog_Update,
			"BINARY_Biolog_SendMessage"	:	self.BINARY_Biolog_SendMessage,	
			"BINARY_Biolog_PopUp"	:	self.BINARY_Biolog_PopUp,
			"BINARY_Biolog_SelectReward"	:	self.BINARY_Biolog_SelectReward,
			# END_OF_PROFESSIONAL_BIOLOG_SYSTEM	
			# WEDDING
			"lover_login"			: self.__LoginLover,
			"lover_logout"			: self.__LogoutLover,
			"lover_near"			: self.__LoverNear,
			"lover_far"				: self.__LoverFar,
			"lover_divorce"			: self.__LoverDivorce,
			"PlayMusic"				: self.__PlayMusic,
			"SetPlayersOnline"		: self.SetPlayersOnline,
			# END_OF_WEDDING
			"input0"						: self.__Input0,
			"input1"						: self.__Input1,

			"ManagerInventoryUnlock": self.ManagerInventoryUnlock,


			"COMBAT_ZONE"			: self.COMBAT_ZONE,
			"BOSS_EVENT"			: self.BOSS_EVENT,
			"metines_event"			: self.METIN_EVENT,
			
			"TICKETS"					: self.ManagerTickets,
			"SupportLv"					: self.SetSupportLevel,
			"SupportName"				: self.SetSupportName,
			"SupportLeave"				: self.SupportLeave,
			"SupporInt"					: self.SupportInt,
			"SupportExp"				: self.SetSupportExp,
			"SupportIcon"				: self.SetSupportIcon,
			"SupportSpeciality"			: self.SetSupportSpeciality,
			"SupportArmor"					: self.SetSupportArmor,
			#"SupportArmorClear"				: self.SupportArmorClear,
			#"SupportHairClear"				: self.SupportHairClear,
			"SupportClear"					: self.SupportClear,
			"SupportWeapon"					: self.SetSupportWeapon,
			"SupportHair"					: self.SetSupportHair,
			"SetSupportSkill"			: self.SetSupportSkill,

			"sCantDestroyItemDialog"	: self.sCantDestroyItemDialog,
		}

		serverCommandList["AppendEvent"] = self.AppendEvent

		if app.NEW_PET_SYSTEM:
			serverCommandList.update({"PetEvolution" : self.SetPetEvolution })
			serverCommandList.update({"PetName" : self.SetPetName })
			serverCommandList.update({"PetLevel" : self.SetPetLevel })
			serverCommandList.update({"PetDuration" : self.SetPetDuration })
			serverCommandList.update({"PetBonus" : self.SetPetBonus })
			serverCommandList.update({"PetSkill" : self.SetPetskill })
			serverCommandList.update({"PetIcon" : self.SetPetIcon })
			serverCommandList.update({"PetExp" : self.SetPetExp })
			serverCommandList.update({"PetUnsummon" : self.PetUnsummon })
			serverCommandList.update({"OpenPetIncubator" : self.OpenPetIncubator })
		if app.ENABLE_MULTILANGUAGE_SYSTEM:
			serverCommandList["BINARY_SET_LANG_AND_EMPIRE_FLAG"] = self.BINARY_SET_LANG_AND_EMPIRE_FLAG
		
		if app.ENABLE_CALENDAR_SYSTEM:

			serverCommandList["BINARY_CALENDAR_OPEN"] = self.BINARY_CALENDAR_OPEN
			serverCommandList["BINARY_CALENDAR_LOAD_EVENTS"] = self.BINARY_CALENDAR_LOAD_EVENTS
			serverCommandList["BINARY_CALENDAR_CLEAR_EVENTS"] = self.BINARY_CALENDAR_CLEAR_EVENTS
			serverCommandList["BINARY_CALENDAR_LOADING_EVENTS"] = self.BINARY_CALENDAR_LOADING_EVENTS

			serverCommandList["BINARY_CALENDAR_OPEN_ADM"] = self.BINARY_CALENDAR_OPEN_ADM
			serverCommandList["BINARY_CALENDAR_LOAD_EVENTS_ADM"] = self.BINARY_CALENDAR_LOAD_EVENTS_ADM
			serverCommandList["BINARY_CALENDAR_CLEAR_EVENTS_ADM"] = self.BINARY_CALENDAR_CLEAR_EVENTS_ADM
			serverCommandList["BINARY_CALENDAR_LOADING_EVENTS_ADM"] = self.BINARY_CALENDAR_LOADING_EVENTS_ADM

		if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
			serverCommandList.update({
					"PickUPMode" : self.__PickUPMode,
				})

		if app.ELEMENT_SPELL_WORLDARD:
			serverCommandList["ElementsSpellSuceeded"] = self.ElementsSpellSuceededMessage
			serverCommandList["ElementsSpellFailed"] = self.ElementsSpellFailedMessage
			serverCommandList["ElementsSpellDownGradeSuceeded"] = self.ElementsSpellDownGradeSuceededMessage
			serverCommandList["ElementsSpellChangeSuceeded"] = self.ElementsSpellChangeSuceeded

		if app.ENABLE_OFFLINESHOP_SYSTEM:
			serverCommandList.update({"OpenBackAllItem" : self.OpenBackAllItem })
			serverCommandList.update({"OpenOfflineShop" : self.OpenOfflineShop })
			serverCommandList.update({"RefreshOfflineShop" : self.RefreshOfflineShop })
			serverCommandList.update({"OpenOfflineShopPanel" : self.OpenOfflineShopPanel })
			serverCommandList.update({"ClearOfflineShopLog" : self.ClearOfflineShopLog })
			# serverCommandList.update({"AppendShopLog" : self.AppendShopLog })
			serverCommandList.update({"OfflineShopSellMsg" : self.interface.AddOfflineShopMessage })
			if app.ENABLE_SHOP_SEARCH_SYSTEM:
				serverCommandList.update({"OfflineShopBuyed" : self.interface.OfflineShopBuyed })

		if app.ENABLE_NEW_PET_SYSTEM:
			serverCommandList.update({"PetSetSlotIndex" : self.PetSetSlotIndex})
			serverCommandList.update({"PetClearData" : self.PetClearData})
			serverCommandList.update({"UpdatePet" : self.PetUpdate})

		if app.ENABLE_BIYOLOG:
			serverCommandList.update({"biodata" : self.interface.SetBioData})
			serverCommandList.update({"biostone" : self.interface.SetBioStone})
			serverCommandList.update({"bioodul" : self.interface.SetBioGift})
			serverCommandList.update({"bioempty" : self.interface.SetBioEmpty})

		if app.dracaryS_DUNGEON_LIB:
			serverCommandList.update({"RefreshDungeonFloor" : self.RefreshDungeonFloor })
			serverCommandList.update({"RefreshDungeonTimer" : self.RefreshDungeonTimer })

		if app.ENABLE_DUNGEON_INFO:
			serverCommandList.update({"getinputbegin" : self.__Inputget1 })
			serverCommandList.update({"DungeonDataClear" : self.DungeonDataClear })
			serverCommandList.update({"getinputend" : self.__Inputget2 })
			serverCommandList.update({"get_index" : self.GetDungeonIndex })
			serverCommandList.update({"dungeon_index" : self.SetDungeonQIndex })
			serverCommandList.update({"DungeonInfoData" : self.DungeonInfoData })
			serverCommandList.update({"DungeonBackData" : self.DungeonBackData })

		if app.ENABLE_BATTLE_PASS:
			serverCommandList.update({"BattlePassSetStatusEx" : self.interface.BattlePassSetStatusEx})
			serverCommandList.update({"BattlePassSetStatus" : self.interface.BattlePassSetStatus})
			serverCommandList.update({"BattlePassSetMission" : self.interface.BattlePassSetMission})
			serverCommandList.update({"BattlePassAppendMission" : self.interface.BattlePassAppendMission})
			serverCommandList.update({"BattlePassClear" : self.interface.BattlePassClear})
		
		if app.ENABLE_DEFENSAWESHIP:
			serverCommandList.update({"gethydrahp" : self.__HydraGetHp })
		if app.ENABLE_RARITY:
			serverCommandList.update({"RarityMessage" : self.interface.AddRarityMessage})

		if app.ENABLE_ITEMSHOP:
			serverCommandList.update({"SetWheelItemData" : self.interface.SetWheelItemData})
			serverCommandList.update({"OnSetWhell" : self.interface.OnSetWhell})
			serverCommandList.update({"GetWheelGiftData" : self.interface.GetWheelGiftData})
			serverCommandList.update({"SetDragonCoin" : self.ItemShopSetDragonCoin})
			serverCommandList.update({"ItemShopAppendLog" : self.ItemShopAppendLogEx})

		if app.ENABLE_ANTI_EXP:
			serverCommandList.update({"SetAntiExp" : self.SetAntiExp})
		if app.ENABLE_MULTI_FARM_BLOCK:
			serverCommandList.update({"UpdateMultiFarmAffect" : self.UpdateMultiFarmAffect})
			serverCommandList.update({"UpdateMultiFarmPlayer" : self.UpdateMultiFarmPlayer})
		if app.ENABLE_ZODIAC_MISSION:
			serverCommandList.update({"zodiac_index" : self.ZodiacLuaIndex})
		if app.ENABLE_TRACK_WINDOW:
			serverCommandList.update({"TrackDungeonInfo" : self.interface.TrackDungeonInfo})
			serverCommandList.update({"TrackBossInfo" : self.interface.TrackBossInfo})
		if app.ENABLE_FISH_GAME:
			serverCommandList.update({"OpenFishGameWindow" : self.interface.OpenFishGameWindow})
			serverCommandList.update({"SetFishGameGoal" : self.interface.SetFishGameGoal})
			serverCommandList.update({"CloseFishGame" : self.interface.CloseFishGame})
		if app.ENABLE_GEM_SYSTEM:
			serverCommandList.update({"GemOpen" : self.interface.OpenGemShop})
			serverCommandList.update({"GemUpdateSlotCount" : self.interface.GemUpdateSlotCount})
			serverCommandList.update({"GemClear" : self.interface.GemClear})
			serverCommandList.update({"GemSetRefreshLeftTime" : self.interface.GemSetRefreshLeftTime})
			serverCommandList.update({"GemSetItemsWithString" : self.interface.GemSetItemsWithString})
			serverCommandList.update({"GemSetBuyedSlot" : self.interface.GemSetBuyedSlot})
		if app.RENEWAL_MISSION_BOOKS:
			serverCommandList.update({"ClearBookMission" : self.interface.ClearBookMission})
			serverCommandList.update({"UpdateMissionInfo" : self.interface.UpdateMissionInfo})
			serverCommandList.update({"UpdateMissionValue" : self.interface.UpdateMissionValue})
			serverCommandList.update({"RewardMissionData" : self.interface.RewardMissionData})
			serverCommandList.update({"RemoveMissionData" : self.interface.RemoveMissionData})
			serverCommandList.update({"UpdateMissionEndTime" : self.interface.UpdateMissionEndTime})

		if app.__RENEWAL_BRAVE_CAPE__:
			serverCommandList.update({"SetBraveCapeStatus" : self.SetBraveCapeStatus})

		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			serverCommandList["auto_off"] = self.__AutoOff
			serverCommandList["auto_on"] = self.__AutoOn
			serverCommandList["auto_loginoff"] = self.__AutoLoginOff

		if app.ENABLE_PVP_TOURNAMENT:
			serverCommandList.update({"OpenPvPDuelPanel" : self.interface.OpenPvPDuelPanel})

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			serverCommandList["BuffNPCSummon"] = self.__SetBuffNPCSummon
			serverCommandList["BuffNPCUnsummon"] = self.__SetBuffNPCUnsummon
			serverCommandList["BuffNPCClear"] = self.__SetBuffNPCClear
			serverCommandList["BuffNPCBasicInfo"] = self.__SetBuffNPCBasicInfo
			serverCommandList["BuffNPCEXPInfo"] = self.__SetBuffNPCEXPInfo
			serverCommandList["BuffNPCSkillInfo"] = self.__SetBuffNPCSkillInfo
			serverCommandList["BuffNPCSkillUseStatus"] = self.__SetBuffNPCSkillUseStatus
			serverCommandList["BuffNPCSkillCooltime"] = self.__SetBuffNPCSkillSetSkillCooltime
			serverCommandList["BuffNPCCreatePopup"] = self.__SetBuffNPCCreatePopup

		if app.ENABLE_DISCORD_STUFF:
			serverCommandList.update({"message_" : self.GetMessage})

		if app.ENABLE_MANAGER_BANK_SYSTEM:
			serverCommandList["BINARY_Account_Bank"] = self.interface.managerAccountBank.Loading

		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			serverCommandList["COSTUME_HIDE_CLEAR"] = self.COSTUME_HIDE_CLEAR
			serverCommandList["COSTUME_HIDE_LIST"] = self.COSTUME_HIDE_LIST
			serverCommandList["COSTUME_HIDE_LOAD"] = self.COSTUME_HIDE_LOAD

		if (app.WJ_COMBAT_ZONE):
			serverCommandList["COMBAT_ZONE_ESTADISTICAS"]  = self.COMBAT_ZONE_ESTADISTICAS

		if app.ENABLE_MINI_GAME_CATCH_KING:
			serverCommandList["MiniGameCatchKing"] = self.MiniGameCatchKing
			serverCommandList["StartCatchKing"] = self.StartCatchKing

		if app.ENABLE_MOVE_CHANNEL:
			serverCommandList.update({
				"server_info" : self.__SeverInfo
			})

		if app.__SKILL_TREE__:
			serverCommandList.update({
				"SkillTreeLoad" : self.interface.SkillTreeLoad,
				"SkillTreeSetTime" : self.interface.SkillTreeSetTime,
				"SkillTreeSetLevel" : self.interface.SkillTreeSetLevel,
				})

		if app.ENABLE_BLACKJACK_GAME:
			serverCommandList.update({"BJAddNewCard" : self.interface.BJAddNewCard})
			serverCommandList.update({"BJSetGameMode" : self.interface.BJSetGameMode})
			serverCommandList.update({"BJShowGameStatus" : self.interface.BJShowGameStatus})
			serverCommandList.update({"BJOpenGame" : self.interface.OpenBlackJackGame})

		if app.__AUTO_HUNT__:
			serverCommandList.update({"AutoHuntStatus" : self.interface.AutoHuntStatus})

		self.serverCommander = stringCommander.Analyzer()
		if app.ENABLE_SPIRIT_STONE_READING:
			serverCommandList["ruhtasiekranac"] = self.ruhcac
		if app.ENABLE_SKILL_BOOK_READING:
			serverCommandList["bkekranac"] = self.bkac
		if app.__ENABLE_ADVANCE_SKILL_SELECT__:
			self.serverCommander.SAFE_RegisterCallBack("AdvanceSkillSelectWindow", self.__AdvanceSkillSelectWindow)
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)

	if app.ENABLE_DUNGEON_INFO:
		def __Inputget1(self):
			constInfo.INPUT_IGNORE = 1 
		def __Inputget2(self):
			constInfo.INPUT_IGNORE = 0
		def SetDungeonQIndex(self,id):
			constInfo.dungeon_qf_index = int(id)
		def GetDungeonIndex(self):
			net.SendQuestInputStringPacket(constInfo.DungeonWarp)
			constInfo.DungeonWarp = ""
		def DungeonDataClear(self):
			constInfo.py_Flag.clear()
		def DungeonBackData(self, data):
			if len(data) > 0:
				first_list = data[:len(data)-1].split("#")
				for j in xrange(len(first_list)):
					second_list = first_list[j].split("|")
					if len(second_list) == 2:
						constInfo.SetFlag("%d_back"%int(second_list[0]),int(second_list[1])+app.GetGlobalTimeStamp())
		def DungeonInfoData(self, data):
			if len(data) > 0:
				first_list = data[:len(data)-1].split("#")
				for j in xrange(len(first_list)):
					second_list = first_list[j].split("|")
					if len(second_list) == 2:
						constInfo.SetFlag("%d_cooldown"%int(second_list[0]),int(second_list[1])+app.GetGlobalTimeStamp())

	if app.ENABLE_DROP_ITEM_WORLDARD:
		def BINARY_DROP_ITEM_OPEN(self):
			if self.interface:
				self.interface.BINARY_DROP_ITEM_OPEN()

	if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
		def __PickUPMode(self, mode, modeX):
			constInfo.PICKUPMODE = int(mode)
			constInfo.RARITYMODE = int(modeX)
			self.interface.OnChangePickUPMode()

	if app.ENABLE_DUNGEON_INFO:

		def OpenTableDungeonInfo(self):
			if self.interface:
				self.interface.DUNGEON_INFO_CHECK_SHOW()

				
		def BINARY_TABLE_DUNGEON_INFO_OPEN(self):
			if self.interface:
				self.interface.BINARY_TABLE_DUNGEON_INFO_OPEN()

		def BINARY_TABLE_DUNGEON_RANKING_LOAD(self):
			if self.interface:
				self.interface.BINARY_TABLE_DUNGEON_RANKING_LOAD()
		def BINARY_TABLE_DUNGEON_MISION_LOAD(self):
			if self.interface:
				self.interface.BINARY_TABLE_DUNGEON_MISION_LOAD()

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			if self.interface:
				self.interface.BINARY_CUBE_RENEWAL_OPEN()

	if app.__ENABLE_ADVANCE_SKILL_SELECT__: 
		def __AdvanceSkillSelectWindow(self, job):
			self.interface.OpenSkillSelectWindow(job)

	if app.ELEMENT_SPELL_WORLDARD:
		def BINARY_ELEMENTS_SPELL_OPEN(self, itemPos , func, cost, grade_add):
			self.interface.ElementsSpellOpen(itemPos, func, cost, grade_add)

		def BINARY_ELEMENTS_SPELL_OPEN_CHANGE(self, itemPos, cost):
			self.interface.ElementsSpellChangeOpen(itemPos, cost)

		def ElementsSpellSuceededMessage(self):
			self.PopupMessage(localeInfo.REFINE_ELEMENT_UPGRADE_SUCCESS_TEXT)

		def ElementsSpellFailedMessage(self):
			self.PopupMessage(localeInfo.REFINE_ELEMENT_UPGRADE_FAIL_TEXT)

		def ElementsSpellDownGradeSuceededMessage(self):
			self.PopupMessage(localeInfo.REFINE_ELEMENT_DOWNGRADE_TEXT)

		def ElementsSpellChangeSuceeded(self,vnum,element_type):
			import uiScriptLocale

			item.SelectItem(int(vnum))

			ELEMENT_NAME = {
				item.APPLY_ATTBONUS_ELEC : uiScriptLocale.REFINE_ELEMENT_CHANGE_ELECT,
				item.APPLY_ATTBONUS_FIRE : uiScriptLocale.REFINE_ELEMENT_CHANGE_FIRE,
				item.APPLY_ATTBONUS_ICE : uiScriptLocale.REFINE_ELEMENT_CHANGE_ICE,
				item.APPLY_ATTBONUS_WIND : uiScriptLocale.REFINE_ELEMENT_CHANGE_WIND,
				item.APPLY_ATTBONUS_EARTH : uiScriptLocale.REFINE_ELEMENT_CHANGE_EARTH,
				item.APPLY_ATTBONUS_DARK : uiScriptLocale.REFINE_ELEMENT_CHANGE_DARK,
			}

			self.PopupMessage(localeInfo.REFINE_ELEMENT_CHANGE_TEXT %(item.GetItemName(),ELEMENT_NAME[int(element_type)]))
	

	def BINARY_BATTLEPASS_OPEN(self):
		if self.interface:
			self.interface.BINARY_BATTLEPASS_OPEN()

	def BINARY_BATTLEPASS_MP(self):
		if self.interface:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, "BattlePass" ,"Enhorabuena! has terminado una mision del pase de batalla.")
			self.interface.RecvWhisper("BattlePass")

	if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
		def __AutoOff(self):
			chrmgr.SetAutoOnOff(False)
			self.interface.AutoOff()

		def __AutoOn(self):
			chrmgr.SetAutoOnOff(True)
			self.interface.AutoOn()

		def __AutoLoginOff(self):
			chrmgr.SetAutoOnOff(False)
			self.interface.AutoOff()

		def AutoException(self):
			wAuto = uiAuto.AutoWindow()
			wAuto.AutoOnOff(0, 1, 1)
			self.PopupMessage("No target, auto hunt stopped.")

		def AutoSlotRefresh(self):
			wAuto = uiAuto.AutoWindow()
			wAuto.RefreshAutoPositionSlot()
			wAuto.RefreshAutoSkillSlot()

	def BINARY_ServerCommand_Run(self, line):
		#dbg.TraceError(line)
		try:
			#print " BINARY_ServerCommand_Run", line
			return self.serverCommander.Run(line)
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = net.GetPreservedServerCommand()
			while command:
				print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = net.GetPreservedServerCommand()
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def PartyHealReady(self):
		self.interface.PartyHealReady()


	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	# ITEM_MALL
	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall();

	def CommandCloseMall(self):
		self.interface.CommandCloseMall()
	# END_OF_ITEM_MALL

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def __SetBuffNPCSummon(self):
			self.interface.BuffNPC_Summon()
			
		def __SetBuffNPCUnsummon(self):
			self.interface.BuffNPC_Unsummon()
			
		def __SetBuffNPCClear(self):
			self.interface.BuffNPC_Clear()

		def __SetBuffNPCBasicInfo(self, name, sex, intvalue):
			self.interface.BuffNPC_SetBasicInfo(str(name), int(sex), int(intvalue))
			
		def __SetBuffNPCEXPInfo(self, level, cur_exp, exp):
			self.interface.BuffNPC_SetEXPInfo(level, cur_exp, exp)

		def __SetBuffNPCSkillInfo(self, skill1, skill2, skill3, skill4, skill5, skill6, skillpoints):
			self.interface.BuffNPC_SetSkillInfo(skill1, skill2, skill3, skill4, skill5, skill6, int(skillpoints))
			
		def __SetBuffNPCSkillUseStatus(self, slot0, slot1, slot2, slot3, slot4, slot5):
			self.interface.BuffNPC_SkillUseStatus(slot0, slot1, slot2, slot3, slot4, slot5)
			
		def __SetBuffNPCSkillSetSkillCooltime(self, slot, timevalue):
			self.interface.BuffNPC_SetSkillCooltime(slot, timevalue)
			
		def __SetBuffNPCCreatePopup(self, type, value0, value1):
			self.interface.BuffNPC_CreatePopup(int(type), int(value0), int(value1))
			
		def BINARY_OpenCreateBuffWindow(self):
			self.interface.BuffNPC_OpenCreateWindow()

	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		if app.ENABLE_REFINE_RENEWAL:
			self.interface.CheckRefineDialog(False)
			if constInfo.IS_AUTO_REFINE:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_SUCCESS)
			else:
				self.PopupMessage(localeInfo.REFINE_SUCCESS)
		else:
			self.PopupMessage(localeInfo.REFINE_SUCCESS)

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		if app.ENABLE_REFINE_RENEWAL:
			self.interface.CheckRefineDialog(True)
			if constInfo.IS_AUTO_REFINE:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE)
			else:
				self.PopupMessage(localeInfo.REFINE_FAILURE)
		else:
			self.PopupMessage(localeInfo.REFINE_FAILURE)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	if app.NEW_PET_SYSTEM:
		def SetPetEvolution(self, evo):
			petname = ["Cucciolo", "Selvaggio", "Coraggioso", "Eroico"]
			self.petmain.SetEvolveName(petname[int(evo)])
			constInfo.PETMINIEVO = int(evo)

		def SetPetName(self, name):
			if len(name) > 1 and name != "":
				self.petmini.Show()
			self.petmain.SetName(name)

		def SetPetLevel(self, level):
			self.petmain.SetLevel(level)
			constInfo.PETMINILEVEL = int(level)

		def SetPetDuration(self, dur, durt):
			if int(durt) > 0:
				self.petmini.SetDuration(dur, durt)
			self.petmain.SetDuration(dur, durt)

		def SetPetBonus(self, hp, dif, sp):
			self.petmain.SetHp(hp)
			self.petmain.SetDef(dif)
			self.petmain.SetSp(sp)

		def SetPetskill(self, slot, idx, lv):
			self.petmini.SetSkill(slot, idx, lv)
			self.petmain.SetSkill(slot, idx, lv)
			self.affectShower.BINARY_NEW_AddAffect(5400+int(idx),int(constInfo.LASTAFFECT_POINT)+1,int(constInfo.LASTAFFECT_VALUE)+1, 0)
			if int(slot)==0:
				constInfo.SKILL_PET1=5400+int(idx)
			if int(slot)==1:
				constInfo.SKILL_PET2=5400+int(idx)
			if int(slot)==2:
				constInfo.SKILL_PET3=5400+int(idx)

		def SetPetIcon(self, vnum):
			if int(vnum) > 0:
				self.petmini.SetImageSlot(vnum)
			self.petmain.SetImageSlot(vnum)
			
		def SetPetExp(self, exp, expi, exptot):
			if int(exptot) > 0:
				self.petmini.SetExperience(exp, expi, exptot)
			self.petmain.SetExperience(exp, expi, exptot)

		def PetUnsummon(self):
			self.petmini.SetDefaultInfo()
			self.petmini.Close()
			self.petmain.SetDefaultInfo()
			self.affectShower.BINARY_NEW_RemoveAffect(int(constInfo.SKILL_PET1),0)
			self.affectShower.BINARY_NEW_RemoveAffect(int(constInfo.SKILL_PET2),0)
			self.affectShower.BINARY_NEW_RemoveAffect(int(constInfo.SKILL_PET3),0)
			constInfo.SKILL_PET1 = 0
			constInfo.SKILL_PET2 = 0
			constInfo.SKILL_PET3 = 0

		def OpenPetMainGui(self):
			if constInfo.PETGUI == 0:
				self.petmain.Show()
				self.petmain.SetTop()
				constInfo.PETGUI = 1
			else:
				self.petmain.Close()
				constInfo.PETGUI = 0

		def OpenPetIncubator(self, pet_new = 0):
			import uipetincubatrice
			self.petinc = uipetincubatrice.PetSystemIncubator(pet_new)
			self.petinc.Show()
			self.petinc.SetTop()

		def OpenPetMini(self):
			self.petmini.Show()
			self.petmini.SetTop()

		def OpenPetFeed(self):
			self.feedwind = uipetfeed.PetFeedWindow()
			self.feedwind.Show()
			self.feedwind.SetTop()

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

	if app.ENABLE_CONQUEROR_LEVEL:
		def BINARY_SungMaAttr(self, str, hp, move, immune):
			self.affectShower.SetSungMaAffectImage(str, hp, move, immune)

	def __IsXMasMap(self):
		mapDict = ( "metin2_map_n_flame_01",
					"metin2_map_n_desert_01",
					"metin2_map_spiderdungeon",
					"metin2_map_deviltower1", )

		if background.GetCurrentMapName() in mapDict:
			return False

		return True

	def __XMasSnow_Enable(self, mode):

		self.__XMasSong_Enable(mode)

		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_SNOW ON"
			background.EnableSnow(1)

		else:
			print "XMAS_SNOW OFF"
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_BOOM ON"
			self.__DayMode_Update("dark")
			self.enableXMasBoom = True
			self.startTimeXMasBoom = app.GetTime()
		else:
			print "XMAS_BOOM OFF"
			self.__DayMode_Update("light")
			self.enableXMasBoom = False

	def __XMasTree_Enable(self, grade):

		print "XMAS_TREE ", grade
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1"==mode:
			print "XMAS_SONG ON"

			XMAS_BGM = "xmas.mp3"

			if app.IsExistFile("BGM/" + XMAS_BGM)==1:
				if musicInfo.fieldMusic != "":
					snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

				musicInfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		else:
			print "XMAS_SONG OFF"

			if musicInfo.fieldMusic != "":
				snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

			musicInfo.fieldMusic=musicInfo.METIN2THEMA
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		constInfo.CONSOLE_ENABLE = True
		self.consoleEnable = True
		app.EnableSpecialCameraMode()
		ui.EnablePaste(True)

	## DayMode
	def __PRESERVE_DayMode_Update(self, mode):
		if "light"==mode:
			background.SetEnvironmentData(0)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

	def DayMode_Update(self, mode):
		self.__DayMode_Update(mode)

	def __DayMode_Update(self, mode):
		if "light"==mode:
			self.__DayMode_OnCompleteChangeToLight()
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			self.__DayMode_OnCompleteChangeToDark()

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(0)

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)

	## XMasBoom
	def __XMasBoom_Update(self):

		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in xrange(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = player.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)

		snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	def __PartyRequestQuestion(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uiCommon.QuestionDialog()
		partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
		partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/party_request_accept " + str(vid))
		else:
			net.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	if (app.WJ_COMBAT_ZONE):
		def BINARY_CombatZone_Manager(self, tokens, arg1 = 0, arg2 = 0, arg3 = 0, arg4 = 0):
			if tokens == "OpenWindow":
				self.wndCombatZone.Open(arg1, arg2, arg3, arg4)


			elif tokens == "RegisterRank":
				self.wndCombatZone.RegisterRanking()

			elif tokens == "StartFlashing":
				if self.interface:
					self.interface.wndMiniMap.btnCombatZone.FlashEx()

			elif tokens == "StartMp":
				if self.interface:
					chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, "Evento", "Se ha activado el EVENTO TOTAL WAR durante 1h. Para poder participar en el evento pulsa el boton B del minimapa")
					self.interface.RecvWhisper("Evento")

			elif tokens == "Time":
				if self.interface:
					self.interface.SetTimeCombatZone(arg1)

			elif tokens == "BonusClear":
				if self.interface:
					self.interface.SetBonusCombatZone("CLEAR")

			elif tokens == "Bonus":
				if self.interface:
					self.interface.SetBonusCombatZone("ADD",arg1,arg2)
					
			elif tokens == "RefreshShop":
				if self.interface:

					self.interface.dlgShop.SetCombatZonePoints(arg1)
					self.interface.dlgShop.SetLimitCombatZonePoints(arg2, arg3)

		def COMBAT_ZONE_ESTADISTICAS(self, tokens):
			if tokens == "OPEN":
				if self.interface:
					self.interface.OpenCZEstadisticas()
			elif tokens == "CLOSE":
				if self.interface:
					self.interface.CloseCZEstadisticas()

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.interface.OpenWebWindow(url)

	# def ManagerItemshop(self, cmd):
		# cmd = cmd.split('#')
		# if cmd[0] == 'QID':
			# constInfo.ItemShop['QID'] = int(cmd[1])
		# elif cmd[0] == 'INPUT':
			# constInfo.INPUT_IGNORE = int(cmd[1])
		# elif cmd[0] == 'SEND':
			# net.SendQuestInputStringPacket(str(constInfo.ItemShop['QCMD']))
			# constInfo.ItemShop['QCMD'] = ''
		# elif cmd[0] == 'CREATE_CATEGORY':
			# constInfo.ItemShop['ITEMS'][cmd[1]][int(cmd[2])] = []
		# elif cmd[0] == 'SET_ITEM':
			# constInfo.ItemShop['ITEMS'][cmd[1]][int(cmd[2])].append([int(cmd[3]), int(cmd[4]), int(cmd[5]), [(int(cmd[6]), int(cmd[7])), (int(cmd[8]), int(cmd[9])), (int(cmd[10]), int(cmd[11])), (int(cmd[12]), int(cmd[13])), (int(cmd[14]), int(cmd[15])), (int(cmd[16]), int(cmd[17])), (int(cmd[18]), int(cmd[19]))], [int(cmd[20]), int(cmd[21]), int(cmd[22])], int(cmd[23]), int(cmd[24]), int(cmd[25])])
		# elif cmd[0] == 'CLEAR_CONTENT':
			# constInfo.ItemShop['ITEMS']['mostBought'] = []
			# constInfo.ItemShop['ITEMS']['hotOffers'] = []
		# elif cmd[0] == 'SET_ITEM_MOSTBOUGHT':
			# constInfo.ItemShop['ITEMS']['mostBought'].append([int(cmd[1]), int(cmd[2]), int(cmd[3]), [(int(cmd[4]), int(cmd[5])), (int(cmd[6]), int(cmd[7])), (int(cmd[8]), int(cmd[9])), (int(cmd[10]), int(cmd[11])), (int(cmd[12]), int(cmd[13])), (int(cmd[14]), int(cmd[15])), (int(cmd[16]), int(cmd[17]))], [int(cmd[17]), int(cmd[19]), int(cmd[20])], int(cmd[21]), int(cmd[22]), int(cmd[23])])
		# elif cmd[0] == 'SET_ITEM_HOTOFFERS':
			# constInfo.ItemShop['ITEMS']['hotOffers'].append([int(cmd[1]), int(cmd[2]), int(cmd[3]), [(int(cmd[4]), int(cmd[5])), (int(cmd[6]), int(cmd[7])), (int(cmd[8]), int(cmd[9])), (int(cmd[10]), int(cmd[11])), (int(cmd[12]), int(cmd[13])), (int(cmd[14]), int(cmd[15])), (int(cmd[16]), int(cmd[17]))], [int(cmd[17]), int(cmd[19]), int(cmd[20])], int(cmd[21]), int(cmd[22]), int(cmd[23])])
		# elif cmd[0] == 'SET_LOG':
			# constInfo.ItemShop['LOGS'].append([int(cmd[1]), int(cmd[2]), int(cmd[3]), cmd[4], [(int(cmd[5]), int(cmd[6])), (int(cmd[7]), int(cmd[8])), (int(cmd[9]), int(cmd[10])), (int(cmd[11]), int(cmd[12])), (int(cmd[13]), int(cmd[14])), (int(cmd[15]), int(cmd[16])), (int(cmd[17]), int(cmd[18]))], [int(cmd[19]), int(cmd[20]), int(cmd[21])]])
		# elif cmd[0] == 'SEND_COINS':
			# constInfo.COINS_DRS = [int(cmd[1]), int(cmd[2])]
		# elif cmd[0] == 'SEND_3RD_SHOP_COIN':
			# self.interface.wndItemShop.Set3rdCoins(int(cmd[1]))
		# elif cmd[0] == 'ALLOW_SPIN_WHEEL':
			# self.interface.wndItemShop.SpinWheel()
		# elif cmd[0] == 'CLEAR_WHEEL_CONTENT':
			# constInfo.ItemShop['WOD'] = [[], []]
		# elif cmd[0] == 'SET_WHEEL_PRIZE':
			# prize = cmd[2].split(',')
			# if cmd[1] == 'G':
				# for i in xrange(len(prize)-1):
					# constInfo.ItemShop['WOD'][1].append(int(prize[i]))
			# elif cmd[1] == 'B':
				# for i in xrange(len(prize)-1):
					# constInfo.ItemShop['WOD'][0].append(int(prize[i]))
		# elif cmd[0] == 'OPEN':
			# self.interface.wndItemShop.Open(int(cmd[1]))
		# elif cmd[0] == 'REFRESH_CONTENT':
			# self.interface.wndItemShop.RefreshWindow()

	# WEDDING
	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	if app.ENABLE_FEATURES_OXEVENT:
		def BINARY_OxEvent_Append(self, event, participantsCount, observersCount):
			import oxevent
			tokens = int(event)

			if tokens == oxevent.APPEND_WINNERS:
				self.eventWindow.Append()

			elif tokens == oxevent.APPEND_REFRESH:
				self.eventWindowManager.RefreshCounter(participantsCount, observersCount)

			elif tokens == oxevent.APPEND_WINDOW:
				self.eventWindowManager.Show()

	if app.ENABLE_MANAGER_BANK_SYSTEM:
		def BINARY_Account_Bank_Logs(self):
			self.interface.managerAccountBank.BINARY_Account_Bank_Logs()

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

	if app.ENABLE_SEND_TARGET_INFO:
		def BINARY_AddTargetMonsterDropInfo(self, raceNum, itemVnum, itemCount):
			if not raceNum in constInfo.MONSTER_INFO_DATA:
				constInfo.MONSTER_INFO_DATA.update({raceNum : {}})
				constInfo.MONSTER_INFO_DATA[raceNum].update({"items" : []})
			curList = constInfo.MONSTER_INFO_DATA[raceNum]["items"]

			isUpgradeable = False
			isMetin = False
			item.SelectItem(itemVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
				isUpgradeable = True
			elif item.GetItemType() == item.ITEM_TYPE_METIN:
				isMetin = True

			for curItem in curList:
				if isUpgradeable:
					if curItem.has_key("vnum_list") and curItem["vnum_list"][0] / 10 * 10 == itemVnum / 10 * 10:
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				elif isMetin:
					if curItem.has_key("vnum_list"):
						baseVnum = curItem["vnum_list"][0]
					if curItem.has_key("vnum_list") and (baseVnum - baseVnum%1000) == (itemVnum - itemVnum%1000):
						if not (itemVnum in curItem["vnum_list"]):
							curItem["vnum_list"].append(itemVnum)
						return
				else:
					if curItem.has_key("vnum") and curItem["vnum"] == itemVnum and curItem["count"] == itemCount:
						return

			if isUpgradeable or isMetin:
				curList.append({"vnum_list":[itemVnum], "count":itemCount})
			else:
				curList.append({"vnum":itemVnum, "count":itemCount})

		def BINARY_RefreshTargetMonsterDropInfo(self, raceNum):
			self.targetBoard.RefreshMonsterInfoBoard()

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicInfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicInfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	if app.ENABLE_KINGDOMS_WAR:
		def ActKingdomsWar(self, act, score1, score2, score3, limitKills, deads, limiDeads, timeRemained):
			if self.interface:
				self.interface.ActKingdomsWar(act, score1, score2, score3, limitKills, deads, limiDeads, timeRemained)

	if app.ENABLE_SASH_SYSTEM:
		def ActSash(self, iAct, bWindow):
			if self.interface:
				self.interface.ActSash(iAct, bWindow)

		def AlertSash(self, bWindow):
			snd.PlaySound("sound/ui/make_soket.wav")
			if bWindow:
				self.PopupMessage(localeInfo.SASH_DEL_SERVEITEM)
			else:
				self.PopupMessage(localeInfo.SASH_DEL_ABSORDITEM)

	def OpenIShopWindow(self):
		import event
		constInfo.ItemShop['QCMD'] = 'OPEN_SHOP#'
		event.QuestButtonClick(constInfo.ItemShop['QID'])
	# END_OF_WEDDING

	##################################
	### Inventory By SeMa Start
	##################################
	def ManagerInventoryUnlock(self, cmd):
		cmd = cmd.split("|")
		if cmd[0] == "Reload":
			net.SendChatPacket("/reload_inventory")
		elif cmd[0] == "Hide":
			constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(int(cmd[2]))] = int(cmd[1])
		elif cmd[0] == "Message":
			dbg.LogBox("Necesitas "+str(cmd[1])+" items para desbloquearlo")
	##################################
	### Inventory By SeMa End
	##################################

	def ManagerTickets(self, cmd):
		cmd = cmd.split('#')
		if cmd[0] == 'QID':
			constInfo.Tickets['QID'] = int(cmd[1])
		elif cmd[0] == 'INPUT':
			constInfo.INPUT_IGNORE = int(cmd[1])
		elif cmd[0] == 'SEND':
			net.SendQuestInputLongStringPacket(str(constInfo.Tickets['QCMD']))
			constInfo.Tickets['QCMD'] = ''
		elif cmd[0] == 'CLEAR_CONTENT':
			constInfo.Tickets['MY_TICKETS'] = []
			constInfo.Tickets['GLOBAL_TICKETS'] = []
		elif cmd[0] == 'CLEAR_PERMISIONS':
			constInfo.Tickets['PERMISIONS'] = []
		elif cmd[0] == 'SET_TICKET':
			date = cmd[4].split('[_]')
			constInfo.Tickets['GLOBAL_TICKETS'].append([cmd[1], cmd[2].replace('[_]', ' '), int(cmd[3]), date[0], date[1], int(cmd[5]), cmd[6], cmd[7].replace('[_]', ' '), int(cmd[8])])
			if cmd[6] == player.GetName():
				constInfo.Tickets['MY_TICKETS'].append([cmd[1], cmd[2].replace('[_]', ' '), int(cmd[3]), date[0], date[1], int(cmd[5]), cmd[6], cmd[7].replace('[_]', ' '), int(cmd[8])])
		elif cmd[0] == 'CREATE_ANSWER':
			constInfo.Tickets['ANSWERS'][cmd[1]] = []
		elif cmd[0] == 'SET_ANSWER':
			date = cmd[3].split('[_]')
			constInfo.Tickets['ANSWERS'][cmd[1]].append([cmd[2], date[0], date[1], cmd[4].replace('[_]', ' ')])
		elif cmd[0] == 'SET_PERMISION':
			constInfo.Tickets['PERMISIONS'].append([cmd[1], int(cmd[2]), int(cmd[3]), int(cmd[4])])
		elif cmd[0] == 'OPEN':
			self.interface.wndTicket.Open(int(cmd[1]))
		elif cmd[0] == 'REFRESH_CONTENT':
			self.interface.wndTicket.RefreshPage()

	def ManagerMountSystem(self, status, vnum):
		constInfo.Mount_Affect = {"status":int(status),"vnum":int(vnum)}
		self.affectShower.SetMountActive()
		
	def _ItemshopCMD(self, command):
		cmd = command.split('/')

		if cmd[0] == 'QID': ## 1 argument
			constInfo.ITEMSHOP['qid'] = int(cmd[1])
		elif cmd[0] == 'QUESTCMD':
			net.SendQuestInputStringPacket(str(constInfo.ITEMSHOP['questCMD']))
			constInfo.ITEMSHOP['questCMD'] = 'NULL#'
		elif cmd[0] == 'UPDATETABLE_SET':
			constInfo.ITEMSHOP['tableUpdate'] = cmd[1]
		elif cmd[0] == 'CLEAR_ITEMS':
			constInfo.ITEMSHOP['items']['itemshop'] = {}
			constInfo.ITEMSHOP['items']['voteshop'] = {}
			constInfo.ITEMSHOP['items']['achievementshop'] = {}
			constInfo.ITEMSHOP['items']['startpage']['mostBought'] = []
			constInfo.ITEMSHOP['items']['startpage']['hotOffers'] = []
		## fill items
		elif cmd[0] == 'CREATE_CATEGORY': ## 2 arguments, shop, categoryID
			constInfo.ITEMSHOP['items'][cmd[1]][int(cmd[2])] = []
		elif cmd[0] == 'ADD_ITEM_IS': ## category, type, id, vnum, [socket], [attr], price, percent, time, runOut
			socket = cmd[5].split(",")
			attr = cmd[6].split(",")
			constInfo.ITEMSHOP['items']['itemshop'][int(cmd[1])].append([int(cmd[2]), int(cmd[3]), [int(cmd[4]),int(socket[0]),int(socket[1]),int(socket[2]), int(attr[0]),int(attr[1]),int(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]),int(attr[6]),int(attr[7]),int(attr[8]),int(attr[9]),int(attr[10]),int(attr[11]),int(attr[12]),int(attr[13])], int(cmd[7]), int(cmd[8]), int(cmd[9]), int(cmd[10])])
		elif cmd[0] == 'ADD_ITEM_VS': ## category, type, id, vnum, [socket], [attr], price, percent, time, runOut
			socket = cmd[5].split(",")
			attr = cmd[6].split(",")
			constInfo.ITEMSHOP['items']['voteshop'][int(cmd[1])].append([int(cmd[2]), int(cmd[3]), [int(cmd[4]),int(socket[0]),int(socket[1]),int(socket[2]), int(attr[0]),int(attr[1]),int(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]),int(attr[6]),int(attr[7]),int(attr[8]),int(attr[9]),int(attr[10]),int(attr[11]),int(attr[12]),int(attr[13])], int(cmd[7]), int(cmd[8]), int(cmd[9]), int(cmd[10])])
		elif cmd[0] == 'ADD_ITEM_AS': ## category, type, id, vnum, [socket], [attr], price, percent, time, runOut
			socket = cmd[5].split(",")
			attr = cmd[6].split(",")
			constInfo.ITEMSHOP['items']['achievementshop'][int(cmd[1])].append([int(cmd[2]), int(cmd[3]), [int(cmd[4]),int(socket[0]),int(socket[1]),int(socket[2]), int(attr[0]),int(attr[1]),int(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]),int(attr[6]),int(attr[7]),int(attr[8]),int(attr[9]),int(attr[10]),int(attr[11]),int(attr[12]),int(attr[13])], int(cmd[7]), int(cmd[8]), int(cmd[9]), int(cmd[10])])
		elif cmd[0] == 'ADD_ITEM_MOSTBOUGHT': ## type, id, vnum, [socket], [attr], price, percent, time, runOut
			socket = cmd[4].split(",")
			attr = cmd[5].split(",")
			constInfo.ITEMSHOP['items']['startpage']['mostBought'].append([int(cmd[1]), int(cmd[2]), [int(cmd[3]),int(socket[0]),int(socket[1]),int(socket[2]), int(attr[0]),int(attr[1]),int(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]),int(attr[6]),int(attr[7]),int(attr[8]),int(attr[9]),int(attr[10]),int(attr[11]),int(attr[12]),int(attr[13])], int(cmd[6]), int(cmd[7]), int(cmd[8]), int(cmd[9])])
		elif cmd[0] == 'ADD_ITEM_HOTOFFERS': ## type, id, vnum, [socket], [attr], price, percent, time, runOut
			socket = cmd[4].split(",")
			attr = cmd[5].split(",")
			constInfo.ITEMSHOP['items']['startpage']['hotOffers'].append([int(cmd[1]), int(cmd[2]), [int(cmd[3]),int(socket[0]),int(socket[1]),int(socket[2]), int(attr[0]),int(attr[1]),int(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]),int(attr[6]),int(attr[7]),int(attr[8]),int(attr[9]),int(attr[10]),int(attr[11]),int(attr[12]),int(attr[13])], int(cmd[6]), int(cmd[7]), int(cmd[8]), int(cmd[9])])
		elif cmd[0] == 'ADD_ITEM_CATEGORY':
			## hola_mundo => hola mundo
			constInfo.ITEMSHOP['category'].append([int(cmd[1]), cmd[2].replace("_", " "), cmd[3], cmd[4]])
		elif cmd[0] == 'ADD_ITEM_SUBCATEGORY':
			## hola_mundo => hola mundo
			#constInfo.ITEMSHOP['category'].append([int(cmd[1]), cmd[2].replace("_", " "), cmd[3]])
			#constInfo.ITEMSHOP['subCategories'].update({1: []})
			if not int(cmd[3]) in constInfo.ITEMSHOP['subCategories']:
				constInfo.ITEMSHOP['subCategories'].update({int(cmd[3]): []})

			constInfo.ITEMSHOP['subCategories'][int(cmd[3])].append([int(cmd[1]), cmd[2].replace("_", " ")])
		elif cmd[0] == 'SET_IS_COINS':
			self.interface.Itemshop_v2.SetItemshopCoins(int(cmd[1]))
		elif cmd[0] == 'SET_VS_COINS':
			self.interface.Itemshop_v2.SetVoteshopCoins(int(cmd[1]))
		elif cmd[0] == 'SET_AS_COINS':
			self.interface.Itemshop_v2.SetAchievementshopCoins(int(cmd[1]))
		elif cmd[0] == 'OPEN':
			self.interface.Itemshop_v2.Open(int(cmd[1]), int(cmd[2]),int(cmd[3]), cmd[4], cmd[5])
		elif cmd[0] == 'LOADING':
			self.LoadingBar.SetPercent(int(cmd[1]))
		elif cmd[0] == "COINS":
			constInfo.COINS_DRS[0] = int(cmd[1])
			constInfo.COINS_DRS[1] = int(cmd[2])

	def __Input0(self):
		constInfo.INPUT_IGNORE = 0
	
	def __Input1(self):
		constInfo.INPUT_IGNORE = 1

	def __Team_On(self, name):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogin(2, name)

	def __Team_Off(self, name):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogout(2, name)
		
	def SHOP_IN_CLIENT(self, arg):
		constInfo.SHOP_IN_CLIENT = int(arg)


	def COMBAT_ZONE(self, arg):
		constInfo.COMBAT_ZONE = int(arg)
		
	def BOSS_EVENT(self, arg1, status):
		constInfo.BOSS_EVENT = int(arg1)
		constInfo.BOSS_EVENT_STATUS = int(status)
	
	def METIN_EVENT(self, arg1, status):
		constInfo.METIN_EVENT = int(arg1)
		constInfo.METIN_EVENT_STATUS = int(status)

	def SetSupportArmor(self, armor, time, permanente):
		self.supportpg.SetArmor(armor, time, permanente)

	#def SupportArmorClear(self):
		#self.supportpg.SetArmorClear()		

	#def SupportHairClear(self):
		#self.supportpg.SupportHairClear()
	
	
	def SetSupportWeapon(self, weapon, time, permanente):
		self.supportpg.SetWeapon(weapon, time, permanente)

	def SetSupportHair(self, hair, time, permanente):
		self.supportpg.SetHair(hair, time, permanente)
		
	def SetSupportSkill(self, slot, vnum, time):
		self.supportpg.SetSkill(slot, vnum, time)

	def SupportClear(self,index):
		self.supportpg.SupportClear(int(index))
		
	def OpenSupportGui(self):
		if constInfo.SUPPORTGUI == 0:
			self.supportpg.Show()
			self.supportpg.SetTop()
			constInfo.SUPPORTGUI = 1
		else:
			self.supportpg.Close()
			constInfo.SUPPORTGUI = 0
			
	def SetSupportLevel(self, level):
		constInfo.SUPPORT_SHOW = 1
		
	def SetSupportName(self, name, name2):
		pass
		
	def SupportLeave(self):
		self.supportpg.SetDefaultInfo()
		self.supportpg.Close()
		constInfo.SUPPORT_SHOW = 0
		
	def SupportInt(self , ints):
		pass
		
	def SetSupportExp(self, exp, exptot):
		pass
		
	def SetSupportIcon(self, vnum):
		pass
		
	def SetSupportSpeciality(self,speciality):
		pass

	def BINARY_CALENDAR_OPEN_ADM(self):
		self.interface.BINARY_CALENDAR_OPEN_ADM()

	def BINARY_CALENDAR_LOAD_EVENTS_ADM(self,index_event,name_event,descrip_event):
		self.interface.BINARY_CALENDAR_LOAD_EVENTS_ADM(index_event,name_event,descrip_event)

	def BINARY_CALENDAR_CLEAR_EVENTS_ADM(self):
		self.interface.BINARY_CALENDAR_CLEAR_EVENTS_ADM()

	def BINARY_CALENDAR_LOADING_EVENTS_ADM(self):
		self.interface.BINARY_CALENDAR_LOADING_EVENTS_ADM()


	def BINARY_CALENDAR_OPEN(self, currentTimeStamp):
		self.interface.BINARY_CALENDAR_OPEN(app.GetGlobalTimeStamp())

	def BINARY_CALENDAR_LOAD_EVENTS(self,day,name,image,startAt, endAt,duration):
		self.interface.BINARY_CALENDAR_LOAD_EVENTS(day,name,image,startAt, endAt,duration)

	def BINARY_CALENDAR_CLEAR_EVENTS(self):
		#pass
		self.interface.BINARY_CALENDAR_CLEAR_EVENTS()

	def BINARY_CALENDAR_LOADING_EVENTS(self):
		self.interface.BINARY_CALENDAR_LOADING_EVENTS()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def COSTUME_HIDE_CLEAR(self):
			self.interface.costume_hide_clear()
		def COSTUME_HIDE_LIST(self,slot,index):
			self.interface.costume_hide_list(slot,index)
		def COSTUME_HIDE_LOAD(self):
			self.interface.costume_hide_load()

	if app.ENABLE_SWITCHBOT:
		def RefreshSwitchbotWindow(self):
			self.interface.RefreshSwitchbotWindow()
			
		def RefreshSwitchbotItem(self, slot):
			self.interface.RefreshSwitchbotItem(slot)

	def AppendEvent(self, image, timeStamp, duration):
		self.eventList.append([image, int(timeStamp), int(duration)])

	if app.ENABLE_OFFLINESHOP_SYSTEM:
		def StartOfflineShop(self, vid, isOwner):
			if self.interface:
				self.interface.OpenOfflineShopDialog(vid, isOwner)
		def StartOfflineShopPanel(self):
			if self.interface:
				self.interface.OpenOfflineShopPanel()

		def ClearOfflineShopLog(self):
			if self.interface:
				if self.interface.dlgOfflineShopPanel:
					if self.interface.dlgOfflineShopPanel.GetChild("ListBox"):
						self.interface.dlgOfflineShopPanel.GetChild("ListBox").RemoveAllItems()

		# def AppendShopLog(self, name, date, itemvnum, itemcount, price):
			# self.interface.AppendLogOfflineShopPanel(name, date, itemvnum, itemcount, price)

		# def AppendShopLogFirst(self, name, date, itemvnum, itemcount, price):
			# self.interface.AppendLogOfflineShopPanelFirst(str(name), str(date), int(itemvnum), int(itemcount), int(price))

		def EndOfflineShop(self):
			if self.interface:
				if self.interface.dlgOfflineShop:
					if self.interface.dlgOfflineShop.IsShow():
						self.interface.dlgOfflineShop.Close()
				if self.interface.dlgOfflineShopPanel:
					if self.interface.dlgOfflineShopPanel.IsShow():
						self.interface.dlgOfflineShopPanel.Close()
				if self.interface.offlineShopBuilder:
					if self.interface.offlineShopBuilder.IsShow():
						self.interface.offlineShopBuilder.Close()
		def RefreshOfflineShop(self):
			if self.interface:
				if self.interface.dlgOfflineShop:
					self.interface.dlgOfflineShop.Refresh()
				if self.interface.dlgOfflineShopPanel:
					if self.interface.dlgOfflineShopPanel.IsShow():
						self.interface.dlgOfflineShopPanel.Refresh()
				if self.interface.offlineShopBuilder:
					if self.interface.offlineShopBuilder.IsShow():
						self.interface.offlineShopBuilder.Refresh()
		def OpenOfflineShop(self):
			if self.interface:
				self.interface.OpenOfflineShopBuilder()
		def OpenBackAllItem(self):
			backItem = uiCommon.QuestionDialog()
			backItem.SetText(localeInfo.OFFLINESHOP_GET_BACK_ITEMS) # HELLO WORLD
			backItem.SetAcceptText(localeInfo.UI_ACCEPT)
			backItem.SetCancelText(localeInfo.UI_DENY)
			backItem.SetAcceptEvent(lambda arg=TRUE: self.__AnswerGetBackItems(arg))
			backItem.SetCancelEvent(lambda arg=FALSE: self.__AnswerGetBackItems(arg))
			backItem.Open()
			self.partyRequestQuestionDialog=backItem

		def __AnswerGetBackItems(self, answer):
			if not self.partyRequestQuestionDialog:
				return
			if answer:
				net.SendGetBackItems()
			self.partyRequestQuestionDialog.Close()
			self.partyRequestQuestionDialog = None

		def OpenOfflineShopPanel(self):
			if self.interface:
				self.interface.OpenOfflineShopPanel()
		def BINARY_OfflineShop_Appear(self, vid, text):	
			if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
				if self.interface:
					self.interface.AppearOfflineShop(vid, text)
			
		def BINARY_OfflineShop_Disappear(self, vid):
			if (chr.GetInstanceType(vid) == chr.INSTANCE_TYPE_NPC):
				if self.interface:
					self.interface.DisappearOfflineShop(vid)

	if app.BL_67_ATTR:
		def OpenAttr67AddDlg(self):
			if self.interface:
				self.interface.OpenAttr67AddDlg()

	def sCantDestroyItemDialog(self, iType = 0):
		iType = int(iType)
		if self.cantDestroyItemDialog:
			if iType == 1:
				self.cantDestroyItemDialog.SetText(localeInfo.NOTLVL_ITEMDESTROY_ITEM_FRAG)
			elif iType == 2:
				self.cantDestroyItemDialog.SetText(localeInfo.NOT_ITEMDESTROY_ITEM_FRAG)
			elif iType == 3:
				self.cantDestroyItemDialog.SetText(localeInfo.NOTLVL_ITEMDESTROY_ITEM_AURA)
			elif iType == 4:
				self.cantDestroyItemDialog.SetText(localeInfo.NOT_ITEMDESTROY_ITEM_LVL)
			elif iType == 5:
				self.cantDestroyItemDialog.SetText(localeInfo.NOT_ITEMDESTROY_ITEM_LVL)
			elif iType == 0:
				self.cantDestroyItemDialog.SetText(localeInfo.ITEM_NEVER_DESTROY_FORLIST)

			self.cantDestroyItemDialog.Open()

	if app.ENABLE_SHOP_SEARCH_SYSTEM:
		def OpenPrivateShopSearch(self, type):
			if self.interface:
				self.interface.OpenPrivateShopSearch(type)

		def RefreshShopSearch(self):
			if self.interface:
				self.interface.RefreshShopSearch()

		def BuyShopSearch(self):
			self.interface.RefreshShopSearch()

		def BuyShopSearch2(self):
			if self.interface:
				if self.interface.wndPrivateShopSearch.IsShow():
					self.interface.wndPrivateShopSearch.StartSearch()

	if app.ENABLE_NEW_PET_SYSTEM:
		def PetSetSlotIndex(self, index):
			self.interface.SetPetSlotIndex(index)
		def PetClearData(self):
			self.interface.ClearPetData()
		def PetOpenWindow(self):
			self.interface.OpenPetWindow()
		def PetUpdate(self, index):
			self.interface.PetUpdate(int(index))

	def AddLoopEvent(self, name, event):
		for i in self.loopList:
			if i[0] == name:
				i[1] = event
				return # already have.
		list = [name,event]
		self.loopList.append(list)
	def RemoveLoopEvent(self, name):
		for i in xrange(len(self.loopList)):
			if self.loopList[i][0] == name:
				del self.loopList[i]
				return
	def loopListEvent(self):
		for i in xrange(len(self.loopList)):
			returnValue = self.loopList[i][1]()
			if returnValue == True:
				del self.loopList[i]
	
	def BINARY_OnRecvBulkWhisper(self, content):
		content = content.replace("$", " ")
		self.interface.RegisterGameMasterName(localeInfo.SYSTEM_WHISPER)
		chat.AppendWhisper(chat.WHISPER_TYPE_CHAT, localeInfo.SYSTEM_WHISPER, content)
		self.interface.RecvWhisper(localeInfo.SYSTEM_WHISPER)

	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def AutoTranslateText(self, line,  localeText = False, isQuestText = False):
			new_buf = line
			if localeText:
				new_buf = self.GetLCText(line)
			if isQuestText:
				for j in xrange(new_buf.count("*^")):
					new_buf=self.GetQuestText(new_buf)
			return new_buf
		def IsFloat(self, string):
			try:
				number = float(string)
				return True
			except:
				return False
			return False
		def MakeStringToList(self, args):
			new_list=[]
			arg_list = args.split("&")
			for j in xrange(len(arg_list)):
				argText = arg_list[j]

				if not argText or argText == "" or argText == " ":
					continue
				elif argText.isdigit():
					new_list.append(int(argText))
				elif self.IsFloat(argText):
					new_list.append(float(argText))
				else:
					itemLink = argText.find("I")
					if itemLink>=0 and len(argText) > itemLink+1:
						itemVnum = argText[itemLink+1:]
						if itemVnum.isdigit() == True:
							itemVnum = int(itemVnum)
							item.SelectItem(itemVnum)
							new_list.append(item.GetItemName())
							continue

					mobLink = argText.find("M")
					if mobLink>=0 and len(argText) > mobLink+1:
						mobVnum = argText[mobLink+1:]
						if mobVnum.isdigit() == True:
							mobVnum = int(mobVnum)
							mobName = nonplayer.GetMonsterName(mobVnum)
							if not mobName or mobName == "":
								mobName = "None"
							new_list.append(mobName)
							continue

					if app.ENABLE_NEW_PET_SYSTEM:
						petLink = argText.find("P")
						if petLink>=0 and len(argText) > petLink+1:
							petSkill = argText[petLink+1:]
							if petSkill.isdigit() == True:
								petSkill = int(petSkill)
								new_list.append(str(constInfo.pet_skill_data[petSkill][0]))
								continue

					skillLink = argText.find("S")
					if skillLink>=0 and len(argText) > skillLink+1:
						skillIndex = argText[skillLink+1:]
						if skillIndex.isdigit() == True:
							skillIndex = int(skillIndex)
							skillName = skill.GetSkillName(skillIndex)
							if not skillName or skillName == "":
								skillName = "None"
							new_list.append(skillName)
							continue

					hyperLink = argText.find("H")
					if hyperLink>=0 and len(argText) > hyperLink+1:
						hyperlinkText = argText[hyperLink+1:]
						if hyperlinkText.find("item:") != -1:
							itemVnum = int(hyperlinkText.split(":")[1], 16)
							item.SelectItem(itemVnum)
							hyperText = "|cffffc700|H%s|h[%s]|h|r" %(hyperlinkText,item.GetItemName())
							new_list.append(hyperText)
							continue

					privLink = argText.find("'")
					if privLink>=0 and len(argText) > privLink+1:
						privIndex = argText[privLink+1:]
						if privIndex.isdigit() == True:
							privIndex = int(privIndex)
							privList = ["All","Shinsoo","Chunjo","Jinno"]
							new_list.append(privList[privIndex])
							continue

					goldLink = argText.find("Y")
					if goldLink>=0 and len(argText) > goldLink+1:
						goldPrice = argText[goldLink+1:]
						if goldPrice.isdigit() == True:
							goldPrice = int(goldPrice)
							new_list.append(constInfo.NumberToString(goldPrice))
							continue

					effectLink = argText.find("E")
					if effectLink>=0 and len(argText) > effectLink+1:
						effectText = argText[effectLink+1:]
						effectSplit = effectText.split(":")
						if len(effectSplit) == 2:
							if effectSplit[0].isdigit() and effectSplit[1].isdigit():
								new_list.append(ItemToolTip.AFFECT_DICT[int(effectSplit[0])](int(effectSplit[1])))
								continue
					valueLink = argText.find("%")
					if valueLink >= 0:
						new_list.append(int(argText[0]))
						continue
					new_list.append(argText)
			return new_list

		def GetLCText(self, buf):
			bufSplit = buf.split(" ")
			new_text=buf
			if bufSplit[0].isdigit() == True:
				if localeInfo.LC.has_key(int(bufSplit[0]))==True:
					if len(bufSplit) > 1:
						new_arg= ""
						for j in xrange(len(bufSplit)-1):
							new_arg+= "%s&"% str(bufSplit[1+j])
						try:
							new_text=localeInfo.LC[int(bufSplit[0])] % tuple(self.MakeStringToList(new_arg[:len(new_arg)-1]))
						except:
							new_text=buf
					else:
						try:
							new_text=localeInfo.LC[int(bufSplit[0])]
						except:
							new_text=buf
				else:
					new_text=buf
			return new_text

		def GetLocaleString(self, type, buf):
			buf = self.AutoTranslateText(buf, True, True)
			if type == chat.CHAT_TYPE_NOTICE:
				self.BINARY_SetTipMessage(buf)
			elif type == chat.CHAT_TYPE_BIG_NOTICE:
				self.BINARY_SetBigMessage(buf)
			elif type == chat.CHAT_TYPE_MISSION:
				self.BINARY_SetMissionMessage(buf)
			chat.AppendChat(type, buf)

		#Example: ^LC_NAME %d %s I%d M%d*^
		def GetQuestText(self, buf):
			firstpos = buf.find("^")
			secondpos = buf.find("*^")
			if firstpos < 0 or secondpos < 0:
				return buf
			cmd = buf[firstpos+1:secondpos]
			new_text=""
			bufSplit = cmd.split(" ")
			#if bufSplit[0].isdigit() == False:
			if localeInfo.QUEST.has_key(str(bufSplit[0]))==True:
				if len(bufSplit) > 1:
					new_arg= ""
					for j in xrange(len(bufSplit)-1):
						new_arg+= "%s&"% str(bufSplit[1+j])
					try:
						new_text=localeInfo.QUEST[str(bufSplit[0])] % tuple(self.MakeStringToList(new_arg[:len(new_arg)-1]))
					except:
						return buf
				else:
					try:
						new_text=localeInfo.QUEST[str(bufSplit[0])]
					except:
						return buf
			else:
				return buf

			return buf.replace("^"+cmd+"*^",new_text)

		def GetQuestString(self, buf, skin):
			buf = self.AutoTranslateText(buf, False, True)
			if buf.find("*^") != -1:
				buf = buf.replace("*^","")
			if buf.find("^") != -1:
				buf= buf.replace("^","")
			event.AddEvent(buf,skin)

		def GetQuestLetterName(self, packet_type, index, flag, title, clockname, countername, iconfilename, clockvalue, countervalue):
			title = self.AutoTranslateText(title, False, True)
			quest.Add(packet_type,index,title,clockname,clockvalue,countername,countervalue,iconfilename,flag)
			self.RefreshQuest()

	if app.dracaryS_DUNGEON_LIB:
		def RefreshDungeonTimer(self, Floor,Time):
			if self.interface:
				if self.interface.wndMiniMap:
					self.interface.wndMiniMap.Hide()
				self.interface.MakeDungeonTimerWindow()
				if self.interface.wndDungeonTimer:
					self.interface.wndDungeonTimer.RefreshDungeonTimer(Time, Floor)
		def RefreshDungeonFloor(self, Floor2):
			if self.interface:
				if self.interface.wndMiniMap:
					self.interface.wndMiniMap.Hide()
				self.interface.MakeDungeonTimerWindow()
				if self.interface.wndDungeonTimer:
					self.interface.wndDungeonTimer.RefreshDungeonFloor(Floor2)

	if app.ENABLE_ITEMSHOP:
		def ItemShopClear(self, updateTime):
			uiItemShopNew.ItemShopClear(int(updateTime))
		def ItemShopUpdateItem(self, itemID, itemVnum, itemPrice, itemDiscount, itemOffertime, itemTopSelling, itemAddedTime, itemSellingCount, itemMaxSellingCount):
			uiItemShopNew.ItemShopUpdateItem(int(itemID), int(itemVnum), long(itemPrice), int(itemDiscount), int(itemOffertime), int(itemTopSelling), int(itemAddedTime), long(itemSellingCount), int(itemMaxSellingCount))
			self.interface.ItemShopUpdateItem(int(itemID), int(itemMaxSellingCount))
		def ItemShopAppendItem(self, categoryIndex, categorySubIndex, itemID, itemVnum, itemPrice, itemDiscount, itemOffertime, itemTopSelling, itemAddedTime, itemSellingCount, itemMaxSellingCount):
			uiItemShopNew.ItemShopAppendItem(int(categoryIndex), int(categorySubIndex), int(itemID), int(itemVnum), long(itemPrice), int(itemDiscount), int(itemOffertime), int(itemTopSelling), int(itemAddedTime), long(itemSellingCount), int(itemMaxSellingCount))
		def ItemShopHideLoading(self):
			self.interface.ItemShopHideLoading()
		def ItemShopOpenMainPage(self):
			self.interface.OpenItemShopMainWindow()
		def ItemShopLogClear(self):
			uiItemShopNew.ItemShopLogClear()
		def ItemShopAppendLog(self, dateText, dateTime, playerName, ipAdress, itemVnum, itemCount, itemPrice):
			uiItemShopNew.ItemShopAppendLog(str(dateText), int(dateTime), str(playerName), str(ipAdress), int(itemVnum), int(itemCount), long(itemPrice))
		def ItemShopPurchasesWindow(self):
			self.interface.ItemShopPurchasesWindow()
		def ItemShopSetDragonCoin(self, dragonCoin):
			self.interface.ItemShopSetDragonCoin(long(dragonCoin))
		def ItemShopAppendLogEx(self, dateText, dateText2,dateTime, playerName, ipAdress, itemVnum, itemCount, itemPrice):
			uiItemShopNew.ItemShopAppendLog(str(dateText)+" "+str(dateText2), int(dateTime), str(playerName), str(ipAdress), int(itemVnum), int(itemCount), long(itemPrice))

	if app.ENABLE_EVENT_MANAGER:
		def ClearEventManager(self):
			self.interface.ClearEventManager()
		def RefreshEventManager(self):
			self.interface.RefreshEventManager()
		def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
			self.interface.RefreshEventStatus(int(eventID), int(eventStatus), int(eventendTime), str(eventEndTimeText))
		def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			self.interface.AppendEvent(int(dayIndex),int(eventID), int(eventIndex), str(startTime), str(endTime), int(empireFlag), int(channelFlag), int(value0), int(value1), int(value2), int(value3), int(startRealTime), int(endRealTime), int(isAlreadyStart))

	if app.ENABLE_DEFENSAWESHIP:
		def __ShipMastHPShow(self):
			if self.wndShipMastHP:
				self.wndShipMastHP.Open(10000000, 10000000)
		def __HydraGetHp(self, curPoint):
			if self.wndShipMastHP:
				new = int(curPoint)
				self.wndShipMastHP.SetShipMastHP(new, 10000000)

	if app.ENABLE_SHOW_CHEST_DROP:
		def OpenChestDrop(self, chestIndex):
			self.interface.OpenChestDropWindow(int(chestIndex),0, -1)
			#if u close this clear function only send 1 packet.
			item.GetDropClear(int(chestIndex))#every time clear for update.

	if app.ENABLE_ANTI_EXP:
		def SetAntiExp(self, flag):
			flag = int(flag)
			if self.interface:
				ptr = [self.interface.wndTaskBar]
				for gui in ptr:
					if gui:
						if flag:
							guiptr = gui.GetChild("AntiExp")
							guiptr.SetUpVisual("d:/ymir work/ui/game/anti_exp/no_exp_0.tga")
							guiptr.SetOverVisual("d:/ymir work/ui/game/anti_exp/no_exp_1.tga")
							guiptr.SetDownVisual("d:/ymir work/ui/game/anti_exp/no_exp_2.tga")

							if gui.IsChild("RestExp_Value"):
								gui.GetChild("Exp_Value").Hide()
							if gui.IsChild("Exp_Value"):
								gui.GetChild("RestExp_Value").Hide()
								
							for j in range(1,5):
								if gui.IsChild("EXPGauge_0%d"%j):
									gui.GetChild("EXPGauge_0%d"%j).SetDiffuseColor(104.0/255.0,104.0/255.0,104.0/255.0,1)

						else:
							guiptr = gui.GetChild("AntiExp")
							guiptr.SetUpVisual("d:/ymir work/ui/game/anti_exp/exp_0.tga")
							guiptr.SetOverVisual("d:/ymir work/ui/game/anti_exp/exp_1.tga")
							guiptr.SetDownVisual("d:/ymir work/ui/game/anti_exp/exp_2.tga")

							if gui.IsChild("RestExp_Value"):
								gui.GetChild("Exp_Value").Show()
							if gui.IsChild("Exp_Value"):
								gui.GetChild("RestExp_Value").Show()

							for j in range(1,5):
								if gui.IsChild("EXPGauge_0%d"%j):
									gui.GetChild("EXPGauge_0%d"%j).SetDiffuseColor(201,160,51,1)

	if app.ENABLE_MULTI_FARM_BLOCK:
		def UpdateMultiFarmPlayer(self, multiFarmPlayer):
			self.affectShower.SetMultiFarmPlayer(str(multiFarmPlayer))
		def UpdateMultiFarmAffect(self, multiFarmStatus, isNewStatus):
			self.affectShower.SetMultiFarmInfo(int(multiFarmStatus))
			if int(isNewStatus) == 1:
				if int(multiFarmStatus) == 1:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MULTI_FARM_ACTIVE_CHAT)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MULTI_FARM_DEACTIVE_CHAT)
			app.SetMultiFarmExeIcon(int(multiFarmStatus))

	if app.ENABLE_DISCORD_STUFF:
		def GetMessage(self):
			if self.interface:
				self.interface.OpenWhisperWithMessage(constInfo.msgname)
				constInfo.msgname=""
	if app.ENABLE_ZODIAC_MISSION:
		def ZodiacLuaIndex(self,p):
			constInfo.ZodiacLua = int(p)
		def ZodiacLuaIndex(self,p):
			constInfo.ZodiacLua = int(p)
		def BINARY_SetMissionMessage(self, message):
			if self.interface.missionBoard:
				self.interface.missionBoard.SetMission(message)
		def ZodiacJumpButtonShow(self):
			if self.interface:
				self.interface.wnd12ziTimer.Show12ziJumpButton()
		def ZodiacJumpButtonClose(self):
			if self.interface:
				self.interface.wnd12ziTimer.CloseJumpButton()
		def Refresh12ziTimer(self, Time, Nextfloor, Floor):
			if self.interface:
				self.interface.wnd12ziTimer.Refresh12ziTimer(Time, Nextfloor, Floor)
				self.interface.wnd12ziTimer.Show()
		def ZodiacDayorNight(self):
			if self.interface:
				self.interface.wnd12ziTimer.DayorNigh12zi()
		def OpenUI12zi(self,yellomark,greenmark,yellowreward,greenreward):
			if self.interface:
				self.interface.wnd12ziReward.Open(yellomark,greenmark,yellowreward,greenreward)
		def OpenZodiac(self):
			if self.interface:
				self.interface.wnd12ziReward.Show()
		# def SetBeadCount(self, count):
			# if self.interface:
				# self.interface.wndMiniMap.beadInfo.SetText("%d"%count)
				# self.interface.wndMiniMap.beadInfo.Show()
		def NextBeadUpdateTime(self, value):
			if self.interface:
				self.interface.wndMiniMap.beadTime = int(value)
		def OpenReviveDialog(self,count):
			constInfo.RevivePrismaCount = int(count)
		def OpenReviveDialog_Me(self,count_me):
			constInfo.RevivePrismaCount_Me = int(count_me)

	if app.ENABLE_EXCHANGE_LOG:
		def ExchangeLogClear(self, playerCode):
			self.interface.ExchangeLogClear(playerCode)
		def ExchangeLogRefresh(self, isLogItemRefresh):
			self.interface.ExchangeLogRefresh(isLogItemRefresh)
		def ExchangeLogAppend(self, logID, ownerName, ownerGold, ownerIP, targetName, targetGold, targetIP, date):
			self.interface.ExchangeLogAppend(logID, ownerName, ownerGold, ownerIP, targetName, targetGold, targetIP, date)
		def ExchangeLogItemAppend(self, logID, itemPos, itemVnum, itemCount, metinSlot, attrType, attrValue, isOwnerItem):
			self.interface.ExchangeLogItemAppend(logID, itemPos, itemVnum, itemCount, metinSlot, attrType, attrValue, isOwnerItem)

	def GetInputBegin(self):
		constInfo.INPUT_IGNORE = 1

	def GetInputEnd(self):
		constInfo.INPUT_IGNORE = 0

	def BINARY_Cards_UpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
		self.interface.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)
		
	def BINARY_Cards_FieldUpdateInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.interface.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def BINARY_Cards_PutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.interface.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def BINARY_Cards_ShowIcon(self):
		self.interface.CardsShowIcon()
		
	def BINARY_Cards_Open(self, safemode):
		self.interface.OpenCardsWindow(safemode)

	if app.ENABLE_MINI_GAME_CATCH_KING:
		def MiniGameCatchKingEvent(self, isEnable):
			pass

		def MiniGameCatchKingEventStart(self, bigScore):
			self.interface.MiniGameCatchKingEventStart(bigScore)

		def MiniGameCatchKingSetHandCard(self, cardNumber):
			self.interface.MiniGameCatchKingSetHandCard(cardNumber)

		def MiniGameCatchKingResultField(self, score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear):
			self.interface.MiniGameCatchKingResultField(score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear)

		def MiniGameCatchKingSetEndCard(self, cardPos, cardNumber):
			self.interface.MiniGameCatchKingSetEndCard(cardPos, cardNumber)

		def MiniGameCatchKingReward(self, rewardCode):
			self.interface.MiniGameCatchKingReward(rewardCode)

		def MiniGameCatchKing(self, value):
			player.SetEventGame(int(value))
			self.interface.MiniGameCatchKing(value)

		def StartCatchKing(self):
			self.interface.ClickCatchKingEventButton()

	if app.__RENEWAL_BRAVE_CAPE__:
		def SetBraveCapeStatus(self, status):
			if self.interface:
				if self.interface.wndInventory:
					if self.interface.wndInventory.wndBraveCape:
						self.interface.wndInventory.wndBraveCape.SetStatus(status)

	if app.ENABLE_MAINTENANCE_SYSTEM:
		def BINARY_ShowMaintenanceSign(self, timeLeft, duration):
			self.interface.ShowMaintenanceSign(timeLeft, duration)

		def BINARY_HideMaintenanceSign(self):
			self.interface.HideMaintenanceSign()

	if app.ENABLE_AURA_SYSTEM:
		def AuraWindowOpen(self, type):
			self.interface.AuraWindowOpen(type)

		def AuraWindowClose(self):
			self.interface.AuraWindowClose()

	if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
		def BINARY_OpenWarpWindow(self):
			if self.interface:
				self.interface.OpenWarpWindow()

	if app.ENABLE_PVP_TOURNAMENT:
		def SetPvPTournamentClear(self, arenaIndex):
			self.interface.SetPvPTournamentClear(int(arenaIndex))

		def SetPvPTournamentStartTime(self, arenaIndex, serverStartTime):
			self.interface.SetPvPTournamentStartTime(int(arenaIndex), int(serverStartTime))

		def SetPvPTournamentRace(self, arenaIndex, playerIndex, playerRace):
			self.interface.SetPvPTournamentRace(int(arenaIndex), int(playerIndex), int(playerRace))

		def SetPvPTournamentScore(self, arenaIndex, playerIndex, playerScore):
			self.interface.SetPvPTournamentScore(int(arenaIndex), int(playerIndex), int(playerScore))

		def SetPvPTournamentName(self, arenaIndex, playerIndex, playerName):
			self.interface.SetPvPTournamentName(int(arenaIndex), int(playerIndex), str(playerName))

		def SetPvPTournamentHP(self, arenaIndex, playerIndex, playerHPPercent, playerMinHP, playerMaxHP, isPoisoned):
			self.interface.SetPvPTournamentHP(int(arenaIndex), int(playerIndex), int(playerHPPercent), int(playerMinHP), int(playerMaxHP), int(isPoisoned))

	if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
		def AttributesBySet(self, itemCellPos, attrEnchantProb, attrDataList):
			if self.interface:
				self.interface.SetCustomAttributeWindow(itemCellPos, attrEnchantProb, attrDataList)
