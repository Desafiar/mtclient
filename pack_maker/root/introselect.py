import grp
import app
import chr
import net
import math
import wndMgr
import snd
import systemSetting
import localeInfo
import constInfo
import ui
import uiScriptLocale
import networkModule
import musicInfo
import playerSettingModule
import dbg
import uiCommon
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget
import consoleModule
import interfaceModule
import uiTaskBar
import uiInventory
import nano_interface
###################################

LEAVE_BUTTON_FOR_POTAL = FALSE
NOT_NEED_DELETE_CODE = FALSE
ENABLE_ENGNUM_DELETE_CODE = TRUE

###################################

class SelectCharacterWindow(ui.Window):

	# SLOT4
	#SLOT_ROTATION = ( 140.0, 260.0, 20.0 )	
	#SLOT_COUNT = 3
	SLOT_ROTATION = [135.0, 225.0, 315.0, 45.0, 45.0]
	SLOT_COUNT = 5
	CHARACTER_TYPE_COUNT = 5
	SLOTS = [0,1,2,3,4,5]

	EMPIRE_NAME = {
		net.EMPIRE_A : localeInfo.EMPIRE_A,
		net.EMPIRE_B : localeInfo.EMPIRE_B,
		net.EMPIRE_C : localeInfo.EMPIRE_C 
	}

	EMPIRE_NAME_FLAGS_BIG = {
		net.EMPIRE_A : nano_interface.CHAR_SELECT + "blue_slot.png",
		net.EMPIRE_B : nano_interface.CHAR_SELECT + "green_slot.png",
		net.EMPIRE_C : nano_interface.CHAR_SELECT + "green_slot.png",
	}

	EMPIRE_NAME_FLAGS_SMALL = {
		net.EMPIRE_A : nano_interface.CHAR_SELECT + "blue_slot_small.png",
		net.EMPIRE_B : nano_interface.CHAR_SELECT + "green_slot_small.png",
		net.EMPIRE_C : nano_interface.CHAR_SELECT + "green_slot_small.png",
	}

	class CharacterRenderer(ui.Window):
		def OnRender(self):
			grp.ClearDepthBuffer()

			grp.SetGameRenderState()
			grp.PushState()
			grp.SetOmniLight()

			screenWidth = wndMgr.GetScreenWidth()
			screenHeight = wndMgr.GetScreenHeight()
			newScreenWidth = float(screenWidth - 70)
			newScreenHeight = float(screenHeight)

			grp.SetViewport(70.0/screenWidth, 0.0, newScreenWidth/screenWidth, newScreenHeight/screenHeight)

			app.SetCenterPosition(-10.0, 120.0, 20.0) #p0zitia caracterului
			app.SetCamera(1550.0, 15.0, 180.0, 95.0) #p0zitia camerei
			grp.SetPerspective(11.0, newScreenWidth/newScreenHeight, 1000.0, 3000.0)

			(x, y) = app.GetCursorPosition()
			grp.SetCursorPosition(x, y)

			chr.Deform()
			chr.Render()

			grp.RestoreViewport()
			grp.PopState()
			grp.SetInterfaceRenderState()

	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, self)

		self.stream=stream
		self.slot = self.stream.GetCharacterSlot()

		self.openLoadingFlag = FALSE
		self.startIndex = -1

		self.flagDict = {}
		self.curRotation = []
		self.destRotation = []
		for rot in self.SLOT_ROTATION:
			self.curRotation.append(rot)
			self.destRotation.append(rot)

		self.curNameAlpha = []
		self.destNameAlpha = []
		for i in xrange(self.CHARACTER_TYPE_COUNT):
			self.curNameAlpha.append(0.0)
			self.destNameAlpha.append(0.0)

		self.curGauge = [0.0, 0.0, 0.0, 0.0]
		self.destGauge = [0.0, 0.0, 0.0, 0.0]

		self.dlgBoard = 0
		self.changeNameFlag = FALSE
		self.nameInputBoard = None
		self.sendedChangeNamePacket = FALSE
		self.startIndex = -1
		self.isLoad = 0
		self.changeSlot = 0
		import constInfo
		constInfo.TitleSystem['load'] = 0

	def __del__(self):
		ui.Window.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, 0)

	def Open(self):
		if not self.__LoadBoardDialog("nano_scripts/selectcharacterwindow.py"):
			dbg.TraceError("SelectCharacterWindow.Open - __LoadScript Error")
			return

		if not self.__LoadQuestionDialog("uiscript/questiondialog.py"):
			return
		self.Rotation = 0
		playerSettingModule.LoadGameData("INIT")

		self.InitCharacterBoard()

		for objEnable in (self.board["start"],self.board["exit"],self.board["switch_main"][0],self.board["switch_main"][1],self.board["switch_main"][2],self.board["switch_main"][3],self.board["switch_main"][4],self.mainActor["swapSlots"],self.mainActor["startMain"]):
			objEnable.Enable()

		self.dlgBoard.Show()
		self.SetWindowName("SelectCharacterWindow")
		self.Show()

		if self.slot>=0:
			self.SelectSlot(self.slot)

		if musicInfo.selectMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/"+musicInfo.selectMusic)

		app.SetCenterPosition(0.0, 0.0, 0.0)
		app.SetCamera(1550.0, 15.0, 180.0, 95.0)

		self.isLoad=1
		self.Refresh()

		if self.stream.isAutoSelect:
			chrSlot=self.stream.GetCharacterSlot()
			self.SelectSlot(chrSlot)
			self.StartGame()

		self.SetEmpire(net.GetEmpireID())

		app.ShowCursor()
		self.onClickKeyDict = {}
		self.onClickKeyDict[app.DIK_RETURN] = lambda : self.StartGame()
		self.SetFocus()

	def Close(self):
		if musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.selectMusic)

		self.stream.popupWindow.Close()

		if self.dlgBoard:
			self.dlgBoard.ClearDictionary()

		self.empireName = None
		self.flagDict = {}
		self.dlgBoard = None

		self.dlgQuestion.ClearDictionary()
		self.dlgQuestion = None
		self.dlgQuestionText = None
		self.dlgQuestionAcceptButton = None
		self.dlgQuestionCancelButton = None
		self.privateInputBoard = None
		self.nameInputBoard = None

		self.board["start"] = None
		self.board["background"] = None

		self.mainActor["nameMain"]	= None
		self.mainActor["faceMain"]	= None
		self.mainActor["guildMain"]	= None
		self.mainActor["guildSymbolMain"]	= None
		self.mainActor["levelMain"]	= None
		self.mainActor["levelSymbolMain"]	= None

		self.mainActor["deleteMain"] = None
		self.mainActor["createMain"] = None

		self.mainActor["startMain"] = None
		self.mainActor["swapSlots"] = None
		## Main

		chr.DeleteInstance(0)
		chr.DeleteInstance(1)
		chr.DeleteInstance(2)
		chr.DeleteInstance(3)

		self.Hide()
		self.KillFocus()

		app.HideCursor()

	def Refresh(self):
		if not self.isLoad:
			return

		indexArray = (4, 3, 2, 1, 0)
		for index in indexArray:
			id=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_ID)
			race=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_RACE)
			form=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_FORM)
			name=net.GetAccountCharacterSlotDataString(index, net.ACCOUNT_CHARACTER_SLOT_NAME)
			hair=net.GetAccountCharacterSlotDataInteger(index, net.ACCOUNT_CHARACTER_SLOT_HAIR)

			if id:
				self.MakeCharacter(index, id, name, race, form, hair)

				self.SelectSlot(index)

		self.SelectSlot(self.slot)

	def RefreshSingleSlot(self):
		if not self.isLoad:
			return
		indexArray = (4, 3, 2, 1, 0)
		for i in xrange(8):
			if chr.HasInstance(i):
				chr.DeleteInstance(i)
		# SLOT4

		id=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
		race=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_RACE)
		form=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_FORM)
		name=net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_NAME)
		hair=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HAIR)

		if id:
			self.MakeCharacter(self.slot, id, name, race, form, hair)

	def GetCharacterSlotID(self, slotIndex):
		return net.GetAccountCharacterSlotDataInteger(slotIndex, net.ACCOUNT_CHARACTER_SLOT_ID)

	def __LoadQuestionDialog(self, fileName):
		self.dlgQuestion = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgQuestion, fileName)
		except:
			import exception
			exception.Abort("SelectCharacterWindow.LoadQuestionDialog.LoadScript")

		try:
			GetObject=self.dlgQuestion.GetChild
			self.dlgQuestionText=GetObject("message")
			self.dlgQuestionAcceptButton=GetObject("accept")
			self.dlgQuestionCancelButton=GetObject("cancel")
		except:
			import exception
			exception.Abort("SelectCharacterWindow.LoadQuestionDialog.BindObject")

		self.dlgQuestionText.SetText(localeInfo.SELECT_DO_YOU_DELETE_REALLY)
		self.dlgQuestionAcceptButton.SetEvent(ui.__mem_func__(self.RequestDeleteCharacter))
		self.dlgQuestionCancelButton.SetEvent(ui.__mem_func__(self.dlgQuestion.Hide))
		return 1

	def __LoadBoardDialog(self, fileName):
		self.dlgBoard = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgBoard, fileName)
		except:
			import exception
			exception.Abort("SelectCharacterWindow.LoadBoardDialog.LoadScript")

		try:
			GetObject=self.dlgBoard.GetChild

			self.board = {
				"proview"	: GetObject("proviewBoard"),
				"boardExit"	: GetObject("Exit_Board"),
				"slot" : [GetObject("Slot_%d" % (i)) for i in xrange(5)],
				"create" : [GetObject("create_slot_%d" % (i)) for i in xrange(5)],
				"delete" : [GetObject("delete_slot_%d" % (i)) for i in xrange(5)],
				"select" : [GetObject("Select_slot_%d" % (i)) for i in xrange(5)],

				"face" : [GetObject("face_small_%d" % (i)) for i in xrange(5)],

				"guild" : [GetObject("guild_text_small_%d" % (i)) for i in xrange(5)],
				"name" : [GetObject("name_small_%d" % (i)) for i in xrange(5)],
				"level" : [GetObject("level_value_%d" % (i)) for i in xrange(5)],

				"levelSym" : [GetObject("level_decoration_%d" % (i)) for i in xrange(5)],
				"guildSym" : [GetObject("guild_symbol_small_%d" % (i)) for i in xrange(5)],

				"ghostFlag" : [GetObject("effect_%d" % (i)) for i in xrange(5)],

				"start" : GetObject("confirm_button"),
				"exit" : GetObject("exit_button"),
				
				"switch_main" : [GetObject("switch_main_%d" % (i)) for i in xrange(5)],

				"exitBoard" : GetObject("Exit_Board"),

			}

			self.mainActor = {
				"mainActorBoard" : GetObject("Main_Actor"),
				"backGround" : GetObject("Shad_BackGround"),
			## Buttons
				"startMain" : GetObject("confirm_button_mainActor"),
				"exitMain" : GetObject("exit_button_mainActor"),
				"swapSlots" : GetObject("switch_MainSlots"),
				"deleteMain" : GetObject("deleteSlot_fromMainActor"),
				"createMain" : GetObject("createSlot_fromMainActor"),
				"flagMain" : GetObject("flag_main_actor"),

			## Texts
				"nameMain" : GetObject("name_mainActor"),
				"faceMain" : GetObject("face_race_mainActor"),
				"guildSymbolMain" : GetObject("guild_symbol_mainActor"),
				"guildMain" : GetObject("guild_name_mainActor"),
				"levelSymbolMain" : GetObject("level_symbol_fromMainActor"),
				"levelMain" : GetObject("level_name_fromMainActor"),

				"exitMainBoard" : GetObject("Exit_MainActor_Board"),

			}
			self.Status = {
				## Status
				0 : GetObject("gauge_hth"),
				1 : GetObject("gauge_int"),
				2 : GetObject("gauge_str"),
				3 : GetObject("gauge_dex"),
			}
			self.CharacterHTH	= GetObject("character_hth")
			self.CharacterINT	= GetObject("character_int")
			self.CharacterSTR	= GetObject("character_str")
			self.CharacterDEX	= GetObject("character_dex")

			self.NameList = []

		except:
			import exception
			exception.Abort("SelectCharacterWindow.LoadBoardDialog.BindObject")

		[name.SetAlpha(0.0) for name in self.NameList]
		self.__CloseMainActor()
		## Board
		self.board["start"].SetEvent(ui.__mem_func__(self.StartGame))
		self.board["exit"].SetEvent(ui.__mem_func__(self.OnPressExitKey))


		for i in xrange(5):
			if NOT_NEED_DELETE_CODE:
				self.mainActor["deleteMain"].SetEvent(ui.__mem_func__(self.PopupDeleteQuestion))
				self.board["delete"][i].SetEvent(ui.__mem_func__(self.PopupDeleteQuestionMulti),i)
			else:
				self.mainActor["deleteMain"].SetEvent(ui.__mem_func__(self.InputPrivateCode))
				self.board["delete"][i].SetEvent(ui.__mem_func__(self.InputPrivateCodeMulty),i)

			self.board["select"][i].SetEvent(ui.__mem_func__(self.SelectSlot),i)
			self.board["create"][i].SetEvent(ui.__mem_func__(self.CreateCharacterMulti),i)
			self.board["switch_main"][i].SetEvent(ui.__mem_func__(self.__ShowMainActor),i)

		self.mainActor["startMain"].SetEvent(ui.__mem_func__(self.StartGame))
		self.mainActor["createMain"].SetEvent(ui.__mem_func__(self.CreateCharacter))

		self.mainActor["swapSlots"].SetEvent(ui.__mem_func__(self.__SwitchSlotButton))
		self.mainActor["exitMain"].SetEvent(ui.__mem_func__(self.__CloseMainActor))

		self.chrRenderer = self.CharacterRenderer()
		self.chrRenderer.SetParent(self.mainActor["backGround"])
		self.chrRenderer.Show()

		self.Slots(0)
		return 1

	def MakeCharacter(self, index, id, name, race, form, hair):
		if 0 == id:
			return

		chr.CreateInstance(index)
		chr.SelectInstance(index)
		chr.SetVirtualID(index)
		chr.SetNameString(name)

		chr.SetRace(race)
		chr.SetArmor(form)
		chr.SetHair(hair)

		chr.Refresh()
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

		chr.SetRotation(0.0)

	def Slots(self, slot):
		def CreateSlot(key):
			id=net.GetAccountCharacterSlotDataInteger(key, net.ACCOUNT_CHARACTER_SLOT_ID)
			if 0 != id:
				self.board["start"].Enable()
				self.SetEmpire(net.GetEmpireID())
				name=net.GetAccountCharacterSlotDataString(key, net.ACCOUNT_CHARACTER_SLOT_NAME)
				level=net.GetAccountCharacterSlotDataInteger(key, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
				race=net.GetAccountCharacterSlotDataInteger(key, net.ACCOUNT_CHARACTER_SLOT_RACE)
				guildID=net.GetAccountCharacterSlotDataInteger(key, net.ACCOUNT_CHARACTER_SLOT_GUILD_ID)
				guildName=net.GetAccountCharacterSlotDataString(key, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME)
				job = chr.RaceToJob(race)
				if job >= 0 and job < self.CHARACTER_TYPE_COUNT:
					self.destNameAlpha[job] = 1.0

				self.board["name"][key].SetText(name)
				self.board["level"][key].SetText(str(level))
				self.board["create"][key].Hide()
				self.board["ghostFlag"][key].Hide()
				for showObj in (self.board["name"][key],self.board["slot"][key],self.board["levelSym"][key],self.board["guildSym"][key]):
					showObj.Show()
				if key == 0:
					self.board["face"][key].LoadImage(nano_interface.FACE_IMAGE_SELECT_BIG[race])
				else:
					self.board["face"][key].LoadImage(nano_interface.FACE_IMAGE_SELECT_SMALLER[race])
				if 0 != guildID:
					self.board["guild"][key].SetText(guildName)
					self.board["guildSym"][key].Show()
				else:
					self.board["guildSym"][key].Hide()
			else:
				self.InitChanges(key)

		for i in xrange(5):
			CreateSlot(i)
			if i == slot:
				self.board["select"][i].Down()
			else:
				self.board["select"][i].SetUp()

	def InitChanges(self,key):
		self.board["create"][key].Show()
		self.board["delete"][key].Hide()
		self.board["ghostFlag"][key].Show()
		self.board["face"][key].Show()

		for emptyList in (self.board["name"][key],self.board["level"][key]):
			emptyList.SetText("")

		for hideListas in (self.board["levelSym"][key],self.board["slot"][key]):
			hideListas.Hide()

	def __CloseMainActor(self):
		for hideObj in (self.mainActor["mainActorBoard"],self.mainActor["exitMainBoard"],self.mainActor["backGround"]):
			hideObj.Hide()
		self.board["exitBoard"].Show()

	def __ShowMainActor(self, index):
		self.SelectSlot(index)
		for hideObj in (self.mainActor["mainActorBoard"],self.mainActor["exitMainBoard"],self.mainActor["backGround"]):
			hideObj.Show()
		self.board["exitBoard"].Hide()

	def __SwitchSlotButton(self):
		slotIndex = (self.GetSlotIndex() + 1) % self.SLOT_COUNT
		self.SelectSlot(slotIndex)

	## Manage Character
	def StartGame(self):
		if self.sendedChangeNamePacket:
			return

		if self.changeNameFlag:
			self.OpenChangeNameDialog()
			return

		if -1 != self.startIndex:
			return

		if musicInfo.selectMusic != "":
			snd.FadeLimitOutMusic("BGM/"+musicInfo.selectMusic, systemSetting.GetMusicVolume()*0.05)

		for setUpObjects in [self.board["start"], self.mainActor["swapSlots"],self.mainActor["startMain"]]:
			setUpObjects.SetUp()

		for disableObjects in [self.board["start"], self.mainActor["swapSlots"],self.mainActor["startMain"]]:
			disableObjects.Disable()

		for btn in (self.board["create"][:]+self.board["delete"][:]):
			btn.SetUp(),btn.Disable()

		self.dlgQuestion.Hide()

		self.stream.SetCharacterSlot(self.slot)

		self.startIndex = self.slot

		for i in xrange(self.SLOT_COUNT):
			if FALSE == chr.HasInstance(i):
				continue
			chr.SelectInstance(i)

	def OpenChangeNameDialog(self):
		import uiCommon
		nameInputBoard = uiCommon.InputDialogWithDescription()
		nameInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputName))
		nameInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputName))
		nameInputBoard.SetDescription(localeInfo.SELECT_INPUT_CHANGING_NAME)
		nameInputBoard.Open()
		nameInputBoard.slot = self.slot
		self.nameInputBoard = nameInputBoard

	def OnChangeName(self, id, name):
		self.SelectSlot(id)
		self.sendedChangeNamePacket = FALSE
		self.PopupMessage(localeInfo.SELECT_CHANGED_NAME)

	def AcceptInputName(self):
		changeName = self.nameInputBoard.GetText()
		if not changeName:
			return

		self.sendedChangeNamePacket = TRUE
		net.SendChangeNamePacket(self.nameInputBoard.slot, changeName)
		return self.CancelInputName()

	def CancelInputName(self):
		self.nameInputBoard.Close()
		self.nameInputBoard = None
		return TRUE

	def OnCreateFailure(self, type):
		self.sendedChangeNamePacket = FALSE
		if 0 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_NAME)
		elif 1 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_ALREADY_EXIST_NAME)
		elif 2 == type:
			self.PopupMessage(localeInfo.CREATE_FAILURE_5RAZA)
		elif 100 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_INDEX)

	def CreateCharacter(self):
		id = self.GetCharacterSlotID(self.slot)
		if 0==id:
			self.stream.SetCharacterSlot(self.slot)

			EMPIRE_MODE = 1

			if EMPIRE_MODE:
				if self.__AreAllSlotEmpty():
					self.stream.SetReselectEmpirePhase()
				else:
					self.stream.SetCreateCharacterPhase()
			else:
				self.stream.SetCreateCharacterPhase()

	def CreateCharacterMulti(self,slot):
		id = self.GetCharacterSlotID(slot)
		if 0==id:
			self.stream.SetCharacterSlot(slot)
			EMPIRE_MODE = 1

			if EMPIRE_MODE:
				if self.__AreAllSlotEmpty():
					self.stream.SetReselectEmpirePhase()
				else:
					self.stream.SetCreateCharacterPhase()
			else:
				self.stream.SetCreateCharacterPhase()

	def __AreAllSlotEmpty(self):
		for iSlot in xrange(self.SLOT_COUNT):
			if 0!=net.GetAccountCharacterSlotDataInteger(iSlot, net.ACCOUNT_CHARACTER_SLOT_ID):
				return 0
		return 1

	def PopupDeleteQuestion(self):
		id = self.GetCharacterSlotID(self.slot)
		self.SelectSlot(self.slot)
		if 0 == id:
			return

		self.dlgQuestion.Show()
		self.dlgQuestion.SetTop()

	def PopupDeleteQuestionMulti(self,slot):
		id = self.GetCharacterSlotID(slot)
		if 0 == id:
			return

		self.dlgQuestion.Show()
		self.dlgQuestion.SetTop()
		#dbg.LogBox("%d" % slot)
	def RequestDeleteCharacter(self):
		self.dlgQuestion.Hide()

		id = self.GetCharacterSlotID(self.slot)
		if 0 == id:
			self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
			return

		net.SendDestroyCharacterPacket(self.slot, "1234567")
		self.PopupMessage(localeInfo.SELECT_DELEING)

	def InputPrivateCode(self):
		import uiCommon
		privateInputBoard = uiCommon.InputDialogWithDescription()
		privateInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrivateCode))
		privateInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrivateCode))

		if not ENABLE_ENGNUM_DELETE_CODE:
			privateInputBoard.SetNumberMode()

		privateInputBoard.SetSecretMode()
		privateInputBoard.SetMaxLength(7)

		privateInputBoard.SetDescription("CODE:")
		privateInputBoard.Open()
		self.privateInputBoard = privateInputBoard

	def InputPrivateCodeMulty(self, slot):
		self.SelectSlot(slot)
		import uiCommon
		privateInputBoard = uiCommon.InputDialogWithDescription()
		privateInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrivateCode))
		privateInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrivateCode))

		if not ENABLE_ENGNUM_DELETE_CODE:
			privateInputBoard.SetNumberMode()

		privateInputBoard.SetSecretMode()
		privateInputBoard.SetMaxLength(7)

		privateInputBoard.SetDescription("CODE:")
		privateInputBoard.Open()
		self.privateInputBoard = privateInputBoard

	def AcceptInputPrivateCodeMulty(self,slot):
		privateCode = self.privateInputBoard.GetText()
		if not privateCode:
			return

		id = self.GetCharacterSlotID(slot)
		self.SelectSlot(self.slot)
		if 0 == id:
			self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
			return

		net.SendDestroyCharacterPacket(slot, privateCode)
		self.PopupMessage(localeInfo.SELECT_DELEING)

		self.CancelInputPrivateCode()
		return TRUE

	def AcceptInputPrivateCode(self):
		privateCode = self.privateInputBoard.GetText()
		if not privateCode:
			return

		id = self.GetCharacterSlotID(self.slot)
		self.SelectSlot(self.slot)
		if 0 == id:
			self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
			return

		net.SendDestroyCharacterPacket(self.slot, privateCode)
		self.PopupMessage(localeInfo.SELECT_DELEING)

		self.CancelInputPrivateCode()
		return TRUE

	def CancelInputPrivateCode(self):
		self.privateInputBoard = None
		return TRUE

	def OnDeleteSuccess(self, slot):
		self.PopupMessage(localeInfo.SELECT_DELETED)
		self.DeleteCharacter(slot)

	def OnDeleteFailure(self):
		self.PopupMessage(localeInfo.SELECT_CAN_NOT_DELETE)

	def DeleteCharacter(self, index):
		chr.DeleteInstance(index)
		self.SelectSlot(self.slot)

	def ExitSelect(self):
		self.dlgQuestion.Hide()

		if LEAVE_BUTTON_FOR_POTAL:
			if app.loggined:
				self.stream.SetPhaseWindow(0)
			else:
				self.stream.setloginphase()
		else:
			self.stream.SetLoginPhase()

		self.Hide()

	def GetSlotIndex(self):
		return self.slot

	def SetEmpire(self, id):
		for wnd in self.board["slot"][1:]:
			wnd.LoadImage(self.EMPIRE_NAME_FLAGS_SMALL[id])
		self.board["slot"][0].LoadImage(self.EMPIRE_NAME_FLAGS_BIG[id])
		self.mainActor["flagMain"].LoadImage(self.EMPIRE_NAME_FLAGS_BIG[id])

	def SelectSlot(self, index):
		if index < 0:
			return
		if index >= self.SLOT_COUNT:
			return
		self.slot = index
		self.RefreshSingleSlot()
		chr.SelectInstance(self.slot)

		for i in xrange(self.CHARACTER_TYPE_COUNT):
			self.destNameAlpha[i] = 0.0

		for i in xrange(self.SLOT_COUNT):
			self.destRotation[(i+self.slot)%self.SLOT_COUNT] = self.SLOT_ROTATION[i]

		self.destGauge = [0.0, 0.0, 0.0, 0.0, 0.0]

		id=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
		if index == id:
			self.board["delete"][index].Hide()
			self.board["start"].Disable()
		else:
			self.board["delete"][index].Show()
			self.board["start"].Enable()
			self.Slots(index)

		if 0 != id:
			self.SetEmpire(net.GetEmpireID())

			self.board["start"].Enable()
			self.mainActor["startMain"].Enable()

			playTime=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
			level=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
			race=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_RACE)
			valueHTH=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_HTH)
			valueINT=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_INT)
			valueSTR=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_STR)
			valueDEX=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_DEX)
			name=net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_NAME)
			guildID=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_GUILD_ID)
			guildName=net.GetAccountCharacterSlotDataString(self.slot, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME)
			self.changeNameFlag=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_CHANGE_NAME_FLAG)

			job = chr.RaceToJob(race)
			if job >= 0 and job < self.CHARACTER_TYPE_COUNT:
				self.destNameAlpha[job] = 1.0

			self.mainActor["nameMain"].SetText(name)
			self.mainActor["levelMain"].SetText(str(level))
			self.mainActor["faceMain"].LoadImage(nano_interface.FACE_IMAGE_SELECT_BIG[race])
			self.mainActor["levelSymbolMain"].Show()
			self.mainActor["createMain"].Hide()
			self.mainActor["deleteMain"].Show()

			if guildName:
				self.mainActor["guildMain"].SetText(guildName)
				self.mainActor["guildSymbolMain"].Show()
			else:
				self.mainActor["guildSymbolMain"].Hide()

			self.destGauge = [0.0, 0.0, 0.0, 0.0, 0.0]
			self.destGauge =	[
						((float(valueHTH) * 10) / 150) / 10,
						((float(valueINT) * 10) / 150) / 10,
						((float(valueSTR) * 10) / 150) / 10,
						((float(valueDEX) * 10) / 150) / 10
						]

		else:
			self.InitCharacterBoard()

	### Problemaaa
	def InitCharacterBoard(self):
		self.board["start"].Disable()
		self.mainActor["startMain"].Disable()

		for emptyObjects in [self.mainActor["nameMain"], self.mainActor["levelMain"], self.CharacterHTH, self.CharacterINT, self.CharacterSTR, self.CharacterDEX]:
			emptyObjects.SetText("")

		for hideObjects in [self.mainActor["guildSymbolMain"], self.mainActor["levelSymbolMain"], self.mainActor["deleteMain"]]:
			hideObjects.Hide()

		for showObjects in [self.mainActor["createMain"]]:
			showObjects.Show()

		self.mainActor["faceMain"].LoadImage(nano_interface.PATCH + "faces/select_big_face/icon_mwarrior.png")

	## Event
	def OnKeyDown(self, key):
		if 1 == key:
			self.ExitSelect()
		if 2 == key:
			self.SelectSlot(0)
		if 3 == key:
			self.SelectSlot(1)
		if 4 == key:
			self.SelectSlot(2)
		if 5 == key:
			self.SelectSlot(3)
		if 6 == key:
			self.SelectSlot(4)

		if 28 == key:
			id = net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
			if 0 == id:
				self.CreateCharacter()
			else:
				self.StartGame()

		if 203 == key:
			self.slot = (self.GetSlotIndex() - 1 + self.SLOT_COUNT) % self.SLOT_COUNT
			self.SelectSlot(self.slot)
		if 205 == key:
			self.slot = (self.GetSlotIndex() + 1) % self.SLOT_COUNT
			self.SelectSlot(self.slot)

		return TRUE

	def OnUpdate(self):
		chr.Update()
		self.Rotation = self.Rotation - 0.5
		chr.SetRotation(self.Rotation)
		## If slot 0 is deleted
		id=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_ID)
		if self.slot == 0 and id == 0:
			self.board["slot"][0].Hide()
			self.board["create"][0].Show()
			self.board["ghostFlag"][0].Show()

		for i in xrange(4):
			self.curGauge[i] += (self.destGauge[i] - self.curGauge[i]) / 10.0
			if abs(self.curGauge[i] - self.destGauge[i]) < 0.005:
				self.curGauge[i] = self.destGauge[i]
			self.Status[i].SetPercentage(self.curGauge[i], 1.0)

		for i in xrange(self.CHARACTER_TYPE_COUNT):
			self.curNameAlpha[i] += (self.destNameAlpha[i] - self.curNameAlpha[i]) / 10.0
			if len(self.NameList) > i:
				self.NameList[i].SetAlpha(self.curNameAlpha[i])

		if -1 != self.startIndex:
			if FALSE == self.openLoadingFlag:
				chrSlot=self.stream.GetCharacterSlot()
				net.DirectEnter(chrSlot)
				self.openLoadingFlag = TRUE

				playTime=net.GetAccountCharacterSlotDataInteger(self.slot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)

				import player
				player.SetPlayTime(playTime)
				import chat
				chat.Clear()
			## Temporary
		#######################################################

	def EmptyFunc(self):
		pass

	def PopupMessage(self, msg, func=0):
		if not func:
			func=self.EmptyFunc

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def OnPressExitKey(self):	
		self.ExitSelect()
		return TRUE
