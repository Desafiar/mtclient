import grp
import app
import chr
import net
import snd
import wndMgr
import event
import systemSetting
import localeInfo
import constInfo
import ui
import networkModule
import math
import snd
import musicInfo
import playerSettingModule
import uiScriptLocale
import uiToolTip
import nano_interface
import dbg

PAGE_COUNT	= 2
BASE_CHR_ID	= 3
SLOT_COUNT	= 4
MALE_MAX = 3
FEMALE_MAX = 8
INDICATOR_RANCE = 9

class CreateCharacterWindow(ui.Window):

	SLOT_ROTATION = [135.0, 207.0, 279.0, 351.0, 63.0]

	START_STAT =	(  ## CON INT STR DEX
						[ 4, 3, 6, 3, ], ## Warrior
						[ 3, 3, 4, 6, ], ## Assassin
						[ 3, 5, 5, 3, ], ## Sura
						[ 4, 6, 3, 3, ], ## Shaman
						[ 4, 3, 6, 3, ], ## Warrior
						[ 3, 3, 4, 6, ], ## Assassin
						[ 3, 5, 5, 3, ], ## Sura
						[ 4, 6, 3, 3, ], ## Shaman
					)

	DESCRIPTION_FILE_NAME =	(
		uiScriptLocale.JOBDESC_WARRIOR_PATH,
		uiScriptLocale.JOBDESC_ASSASSIN_PATH,
		uiScriptLocale.JOBDESC_SURA_PATH,
		uiScriptLocale.JOBDESC_SHAMAN_PATH,
	)
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

			app.SetCenterPosition(-10.0, 120.0, 20.0) #pizitia caracterului
			app.SetCamera(1850.0, 15.0, 180.0, 95.0) #pizitia camerei
			grp.SetPerspective(11.0, newScreenWidth/newScreenHeight, 1000.0, 3000.0)

			(x, y) = app.GetCursorPosition()
			grp.SetCursorPosition(x, y)

			chr.Deform()
			chr.Render()

			grp.RestoreViewport()
			grp.PopState()
			grp.SetInterfaceRenderState()

	def __init__(self,stream):
		print "NEW CREATE WINDOW ----------------------------------------------------------------------------"
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, self)
		self.stream=stream

	def __del__(self):
		print "---------------------------------------------------------------------------- DELETE CREATE WINDOW"

		net.SetPhaseWindow(net.PHASE_WINDOW_CREATE, 0)
		ui.Window.__del__(self)
		
	def Open(self):
		print "OPEN CREATE WINDOW ----------------------------------------------------------------------------"
		self.Rotation = 0
		playerSettingModule.LoadGameData("INIT")

		self.reservingRaceIndex = -1
		self.reservingShapeIndex = -1
		self.reservingStartTime = 0
		self.stat = [0, 0, 0, 0]
		self.curShape = 0
		self.gender = 0
		self.slot = -1
		self.shapeList = [
			[0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0]]

		self.descIndex = 0
		
		## NEW
		self.Pos = [0,77,77*2,77*3,0,77,77*2,77*3,77*4,]

		try:
			dlgBoard = ui.ScriptWindow()
			pythonScriptLoader = ui.PythonScriptLoader()
			pythonScriptLoader.LoadScriptFile(dlgBoard, nano_interface.SCRIPTS + "createcharacterwindow.py")

		except:
			import exception
			exception.Abort("CreateCharacterWindow.Open.LoadObject")

		try:
			getChild = dlgBoard.GetChild
			
			self.board = {
				"backGround" : getChild("BackGround"),
				"male" : [getChild("male_%d_btn" % (i+1)) for i in xrange(4)],
				"female" : [getChild("female_%d_btn" % (i+1)) for i in xrange(4)],
				
				"male_text" : [getChild("male_%d_txt" % (i+1)) for i in xrange(4)],
				"female_text" : [getChild("female_%d_txt" % (i+1)) for i in xrange(4)],

				"indicator" : [getChild("indicate_%d" % (i)) for i in xrange(INDICATOR_RANCE)],

				"effect_male" : getChild("on_effect_male"),
				"effect_female" : getChild("on_effect_female"),
				
				## Action Buttons
				"shape" : getChild("shape_button"),
				"create" : getChild("create_button"),
				"exit" : getChild("exit_button"),
				
				"name" : getChild("character_name_value"),
				
			}

		except:
			import exception
			exception.Abort("CreateCharacterWindow.Open.BindObject")

		for shd in [self.board["effect_male"] , self.board["effect_female"]]:
			shd.Hide()

		for h in xrange(INDICATOR_RANCE):
			self.board["indicator"][h].Hide()
		
		self.board["create"].SetEvent(ui.__mem_func__(self.CreateCharacter))
		self.board["exit"].SetEvent(ui.__mem_func__(self.CancelCreate))
		self.board["shape"].SetEvent(ui.__mem_func__(self.__SelectShape))

		self.board["name"].SetReturnEvent(ui.__mem_func__(self.CreateCharacter))
		self.board["name"].SetEscapeEvent(ui.__mem_func__(self.CancelCreate))
		


		self.destRotation	= [] + self.SLOT_ROTATION
		self.destNameAlpha	= [0.0, 0.0, 0.0, 0.0, 0.0]

		self.chrRenderer = self.CharacterRenderer()
		self.chrRenderer.SetParent(self.board["backGround"])
		self.chrRenderer.Show()

		self.board["name"].SetText("")

		app.SetCamera(500.0, 10.0, 180.0, 95.0)
		
		self.SelectRace()
		self.__SelectShape()
		self.Presentation_shape()
		self.EnableWindow()
		self.OpenEvents(0,0,0)
		
		self.dlgBoard = dlgBoard
		self.dlgBoard.Show()
		self.Show()

		if musicInfo.createMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/"+musicInfo.createMusic)

		app.ShowCursor()

	def Close(self):
		print "---------------------------------------------------------------------------- CLOSE CREATE WINDOW"

		self.board["name"].Enable()
		self.dlgBoard.ClearDictionary()
		self.stream=0
		self.shapeButtonList = []
		
		self.board["name"] = 0

		if musicInfo.createMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.createMusic)

		for id in xrange(BASE_CHR_ID + SLOT_COUNT * PAGE_COUNT):
			chr.DeleteInstance(id)

		self.dlgBoard.Hide()
		self.Hide()

		app.HideCursor()
		event.Destroy()

	def SelectRace(self):
		self.Slot1 = (
			self.board["male"][0],
			self.board["male"][1],
			self.board["male"][2],
			self.board["male"][3],
			self.board["female"][0],
			self.board["female"][1],
			self.board["female"][2],
			self.board["female"][3],
		)
		self.Slot1_1 = (
			self.board["male_text"][0],
			self.board["male_text"][1],
			self.board["male_text"][2],
			self.board["male_text"][3],
			self.board["female_text"][0],
			self.board["female_text"][1],
			self.board["female_text"][2],
			self.board["female_text"][3],
		)

		self.Slot1[0].SetEvent((lambda : self.OpenEvents(0,0,0)))
		self.Slot1[0].Down()
		self.Slot1_1[1].SetPackedFontColor(nano_interface.COLOR_HOVER)
		self.Slot1[1].SetEvent((lambda : self.OpenEvents(1,0,1)))
		self.Slot1[2].SetEvent((lambda : self.OpenEvents(2,0,2)))
		self.Slot1[3].SetEvent((lambda : self.OpenEvents(3,0,3)))
		self.Slot1[4].SetEvent((lambda : self.OpenEvents(4,1,0)))
		self.Slot1[5].SetEvent((lambda : self.OpenEvents(5,1,1)))
		self.Slot1[6].SetEvent((lambda : self.OpenEvents(6,1,2)))
		self.Slot1[7].SetEvent((lambda : self.OpenEvents(7,1,3)))

	def OpenEvents(self,index,page,race):
		for btn in self.Slot1:
			btn.SetUp()
			for ex in self.Slot1_1:
				ex.SetPackedFontColor(nano_interface.COLOR_NORMAL)
		for ind in self.board["indicator"]:
			ind.Hide()
		self.Slot1[index].Down()
		self.Slot1_1[index].SetPackedFontColor(nano_interface.COLOR_HOVER)
		if	0 <= index and index <= FEMALE_MAX:
			self.__SelectChar(page,race)
			self.__OnSelectEffect(index)
			self.board["indicator"][index].Show()
	
	def __OnSelectEffect(self, effect_state):
		if 0 <= effect_state and effect_state <= MALE_MAX:
			self.board["effect_male"].SetPosition(18,13+1*self.Pos[effect_state])
			self.board["effect_male"].Show()
			#self.board["effect_male"].ResetFrame()
			self.board["effect_female"].Hide()
		elif 3 <= effect_state and effect_state <= FEMALE_MAX:
			self.board["effect_female"].SetPosition(193,13+1*self.Pos[effect_state])
			self.board["effect_female"].Show()
			#self.board["effect_female"].ResetFrame()
			self.board["effect_male"].Hide()
		else:
			self.board["effect_male"].Hide()
			self.board["effect_female"].Hide()
			
	def Presentation_shape(self):
		self.__MakeCharacter(0, 0, playerSettingModule.RACE_WARRIOR_M, 12019)
		self.__MakeCharacter(0, 1, playerSettingModule.RACE_ASSASSIN_M, 12029)
		self.__MakeCharacter(0, 2, playerSettingModule.RACE_SURA_M, 12039)
		self.__MakeCharacter(0, 3, playerSettingModule.RACE_SHAMAN_M, 12049)

		#
		self.__MakeCharacter(1, 0, playerSettingModule.RACE_WARRIOR_W, 12019)
		self.__MakeCharacter(1, 1, playerSettingModule.RACE_ASSASSIN_W, 12029)
		self.__MakeCharacter(1, 2, playerSettingModule.RACE_SURA_W, 12039)
		self.__MakeCharacter(1, 3, playerSettingModule.RACE_SHAMAN_W, 12049)
		
	def __SelectChar(self, page, race):
		self.__SelectSlot(race)
		self.__SelectGender(page)
	
	def __SelectGender(self, gender):
		self.gender = gender
		chr.Hide()
		chr.SelectInstance(self.__GetSlotChrID(self.gender, self.slot))
		chr.Show()
	
	def EnableWindow(self):
		self.reservingRaceIndex = -1
		self.reservingShapeIndex = -1
		self.board["name"].SetFocus()
		self.board["name"].Enable()

		for page in xrange(PAGE_COUNT):
			for slot in xrange(SLOT_COUNT):
				chr_id = self.__GetSlotChrID(page, slot)
				chr.SelectInstance(chr_id)
				chr.BlendLoopMotion(chr.MOTION_INTRO_WAIT, 0.1)

	## Manage Character
	def __GetSlotChrID(self, page, slot):
		return BASE_CHR_ID + page * SLOT_COUNT + slot

	def __MakeCharacter(self, page, slot, race, armor):

		chr_id = self.__GetSlotChrID(page, slot)

		chr.CreateInstance(chr_id)
		chr.SelectInstance(chr_id)
		chr.SetVirtualID(chr_id)

		chr.SetRace(race)
		chr.SetArmor(armor)
		chr.SetHair(0)

		chr.Refresh()
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

		chr.SetRotation(0.0)
		chr.Hide()

	def __SelectShape(self):
		if self.curShape == 0:
			self.curShape += 1
		else:
			self.curShape -= 1
	
		chr_id = self.__GetSlotChrID(self.gender, self.slot)
		chr.SelectInstance(chr_id)
		chr.ChangeShape(self.curShape)
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)

	def GetSlotIndex(self):
		return self.slot

	def __SelectSlot(self, slot):

		if slot < 0:
			return

		if slot >= SLOT_COUNT:
			return

		if self.slot == slot:
			return

		self.slot = slot

		for i in xrange(SLOT_COUNT):
			self.destNameAlpha[i] = 0.0

		self.destNameAlpha[slot] = 1.0

		for i in xrange(SLOT_COUNT):
			self.destRotation[(i+self.slot)%SLOT_COUNT] = self.SLOT_ROTATION[i]

		if self.IsShow():
			snd.PlaySound("sound/ui/click.wav")

		if localeInfo.IsARABIC():
			event.SetEventSetWidth(self.descIndex, 370)

		chr.Hide()
		self.Presentation_shape()
		chr_id = self.__GetSlotChrID(self.gender, slot)
		if chr.HasInstance(chr_id):

			chr.SelectInstance(chr_id)
			chr.Show()

	def CreateCharacter(self):

		if -1 != self.reservingRaceIndex:
			return

		textName = self.board["name"].GetText()
		if FALSE == self.__CheckCreateCharacter(textName):
			return

		if musicInfo.selectMusic != "":
			snd.FadeLimitOutMusic("BGM/"+musicInfo.selectMusic, systemSetting.GetMusicVolume()*0.05)

		chr_id = self.__GetSlotChrID(self.gender, self.slot)

		chr.SelectInstance(chr_id)
		self.reservingRaceIndex = chr.GetRace()

		self.reservingShapeIndex = self.shapeList[self.gender][self.slot]
		self.reservingStartTime = app.GetTime()

		chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED)

	def CancelCreate(self):
		self.stream.SetSelectCharacterPhase()

	def __CheckCreateCharacter(self, name):
		if len(name) == 0:
			self.PopupMessage(localeInfo.CREATE_INPUT_NAME, self.EnableWindow)
			return FALSE

		if name.find("GM")!=-1 or name.find("GA")!=-1 or name.find("ADM")!=-1 or name.find("Admin")!=-1 or name.find("admin")!=-1 or name.find("ADMIN")!=-1 or name.find("adm")!=-1 or name.find("ADIVI")!=-1 or name.find("GIVI")!=-1 or name.find("adm")!=-1 or name.find("adm")!=-1 or name.find("adm")!=-1 or name.find("adm")!=-1:
			self.PopupMessage(localeInfo.CREATE_ERROR_GM_NAME, self.EnableWindow)
			return FALSE

		if net.IsInsultIn(name):
			self.PopupMessage(localeInfo.CREATE_ERROR_INSULT_NAME, self.EnableWindow)
			return FALSE

		return TRUE
	## Event
	def OnCreateSuccess(self):
		self.stream.SetSelectCharacterPhase()

	def OnCreateFailure(self, type):
		if 1 == type:
			self.PopupMessage(localeInfo.CREATE_EXIST_SAME_NAME, self.EnableWindow)
		elif 2 == type:
			self.PopupMessage(localeInfo.CREATE_FAILURE_5RAZA, self.EnableWindow)
		elif 200 == type:
			self.PopupMessage(localeInfo.SELECT_ONLY_VIP, self.EnableWindow)
		else:
			self.PopupMessage(localeInfo.CREATE_FAILURE, self.EnableWindow)

	def OnUpdate(self):
		chr_id = self.__GetSlotChrID(self.gender, self.slot)
		chr.SelectInstance(chr_id)
		chr.Update()
		self.Rotation = self.Rotation - 0.5
		chr.SetRotation(self.Rotation)

		if -1 != self.reservingRaceIndex:
			if app.GetTime() - self.reservingStartTime >= 1.5:

				chrSlot=self.stream.GetCharacterSlot()
				textName = self.board["name"].GetText()
				raceIndex = self.reservingRaceIndex
				shapeIndex = self.reservingShapeIndex

				startStat = self.START_STAT[self.reservingRaceIndex]
				statCon = self.stat[0] - startStat[0]
				statInt = self.stat[1] - startStat[1]
				statStr = self.stat[2] - startStat[2]
				statDex = self.stat[3] - startStat[3]

				net.SendCreateCharacterPacket(chrSlot, textName, raceIndex, shapeIndex, statCon, statInt, statStr, statDex)

				self.reservingRaceIndex = -1

		###########################################################

	def EmptyFunc(self):
		pass

	def PopupMessage(self, msg, func=0):
		if not func:
			func=self.EmptyFunc

		import uiCommon

		self.Notification = uiCommon.PopupDialog()
		self.Notification.SetText(msg)
		self.Notification.SetAcceptEvent(func)
		self.Notification.Open()

	def OnPressExitKey(self):
		self.CancelCreate()
		return TRUE

if __name__ == "__main__":
	import wndMgr
	import systemSetting
	import mouseModule
	import networkModule

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(TRUE)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	mainStream = networkModule.MainStream()
	mainStream.Create()

	test = CreateCharacterWindow(mainStream)
	test.Open()

	app.Loop()
	

	
