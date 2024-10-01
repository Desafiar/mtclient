import ui
import wndMgr
import dbg
import app
import net
import event
import _weakref
import localeInfo
import uiScriptLocale
import time
LOCALE_PATH = "uiscript/"+uiScriptLocale.CODEPAGE+"_"

class SelectEmpireWindow(ui.ScriptWindow):

	EMPIRE_DESCRIPTION_TEXT_FILE_NAME = {
		net.EMPIRE_A : localeInfo.ASBEL,
		net.EMPIRE_B : localeInfo.RAKSA,
		net.EMPIRE_C : localeInfo.MONSTER
		}

	class EmpireButton(ui.Window):
		def __init__(self, owner, arg):
			ui.Window.__init__(self)
			self.owner = owner
			self.arg = arg
		def OnMouseOverIn(self):
			self.owner.OnOverInEmpire(self.arg)
		def OnMouseOverOut(self):
			self.owner.OnOverOutEmpire(self.arg)
		def OnMouseLeftButtonDown(self):
			if self.owner.empireID != self.arg:
				self.owner.OnSelectEmpire(self.arg)

	def __init__(self,stream):
		print "NEW EMPIRE WINDOW  ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_EMPIRE, self)

		self.stream=stream
		self.empireID=app.GetRandom(1, 2)
		self.descIndex=0
		self.empireArea = {}
		self.empireAreaFlag = {}
		self.empireFlag = {}
		self.empireAreaButton = {}
		self.empireAreaCurAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0 }
		self.empireAreaDestAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0 }
		self.empireAreaFlagCurAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0 }
		self.empireAreaFlagDestAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0 }
		self.empireFlagCurAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0 }
		self.empireFlagDestAlpha = { net.EMPIRE_A:0.0, net.EMPIRE_B:0.0 }
		self.Open()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_EMPIRE, 0)
		print "---------------------------------------------------------------------------- DELETE EMPIRE WINDOW"

	def Close(self):
		print "---------------------------------------------------------------------------- CLOSE EMPIRE WINDOW"

		self.ClearDictionary()
		self.leftButton = None
		self.rightButton = None
		self.descriptionBox = None
		self.empireArea = None
		self.empireAreaButton = None

		self.KillFocus()
		self.Hide()

		app.HideCursor()
		event.Destroy()

	def Open(self):
		print "OPEN EMPIRE WINDOW ----------------------------------------------------------------------------"

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("SelectEmpireWindow")
		self.Show()

		if not self.__LoadScript("nano_scripts/SelectEmpireWindow.py"):
			dbg.TraceError("SelectEmpireWindow.Open - __LoadScript Error")
			return

		self.SelectFlag(self.empireID)
		self.__CreateButtons()
		self.__CreateDescriptionBox()
		app.ShowCursor()

	def __CreateButtons(self):
		for key, img in self.empireArea.items():

			img.SetAlpha(0.0)

			(x, y) = img.GetGlobalPosition()
			btn = self.EmpireButton(_weakref.proxy(self), key)
			btn.SetParent(self)
			btn.SetPosition(x, y)
			btn.SetSize(img.GetWidth(), img.GetHeight())
			btn.Show()
			self.empireAreaButton[key] = btn

	def __CreateDescriptionBox(self):
		pass

	def OnOverInEmpire(self, arg):
		self.empireAreaDestAlpha[arg] = 1.0

	def OnOverOutEmpire(self, arg):
		if arg != self.empireID:
			self.empireAreaDestAlpha[arg] = 0.0

	def OnSelectEmpire(self, arg):
		for key in self.empireArea.keys():
			self.empireAreaDestAlpha[key] = 0.0
			self.empireAreaFlagDestAlpha[key] = 0.0
			self.empireFlagDestAlpha[key] = 0.0
		self.empireAreaDestAlpha[arg] = 1.0
		self.empireAreaFlagDestAlpha[arg] = 1.0
		self.empireFlagDestAlpha[arg] = 1.0
		self.empireID = arg

		event.ClearEventSet(self.descIndex)
		if self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME.has_key(arg):
			self.descIndex = event.RegisterEventSet(self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME[arg])
			event.SetRestrictedCount(self.descIndex, 35)
			self.board["description"].SetText(self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME[arg])

	def __LoadScript(self, fileName):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("SelectEmpireWindow.__LoadScript.LoadObject")

		try:
			GetObject=self.GetChild
			
			self.board = {
				## Background
				"slot_flags" : [GetObject("back_flags_%d" % (i)) for i in xrange(3)],
				"select_slot" : [GetObject("start_slot_%d" % (i)) for i in xrange(3)],
				"effects" : [GetObject("effect_%d" % (i)) for i in xrange(3)],
				"description" : GetObject("description_text"),
				
				## Buttons
				"exit" :	GetObject("exit_button"),
				"confirm" :	GetObject("confirm_button"),
			}
			
		except:
			import exception
			exception.Abort("SelectEmpireWindow.__LoadScript.BindObject")
		
		self.board["confirm"].SetEvent(self.ClickSelectButton)
		self.board["exit"].SetEvent(self.ClickExitButton)
		
		for x in xrange(3):
			self.board["effects"][x].Hide()
			self.board["select_slot"][x].SetEvent(ui.__mem_func__(self.SelectFlag), x)
		
		return 1
		
	def SelectFlag(self, flag):
		self.empireID = flag+1
		for i in xrange(3):
			if i == flag:
				self.board["select_slot"][i].Down()
				self.OnSelectEmpire(self.empireID)
				self.board["effects"][i].Show()
				#self.board["effects"][i].ResetFrame()
			else:
				self.board["select_slot"][i].SetUp()
				self.board["effects"][i].Hide()
			

	def ClickLeftButton(self):
		self.empireID-=1
		if self.empireID<1:
			self.empireID=2

		self.OnSelectEmpire(self.empireID)

	def ClickRightButton(self):
		self.empireID+=1
		if self.empireID>2:
			self.empireID=1

		self.OnSelectEmpire(self.empireID)

	def ClickCenterButton(self):
		self.empireID+=1
		if self.empireID>3:
			self.empireID=1

		self.OnSelectEmpire(self.empireID)

	def ClickSelectButton(self):
		net.SendSelectEmpirePacket(self.empireID)
		self.stream.SetSelectCharacterPhase()

	def ClickExitButton(self):
		self.stream.SetLoginPhase()

	def OnUpdate(self):
		self.__UpdateAlpha(self.empireArea, self.empireAreaCurAlpha, self.empireAreaDestAlpha)
		self.__UpdateAlpha(self.empireAreaFlag, self.empireAreaFlagCurAlpha, self.empireAreaFlagDestAlpha)
		self.__UpdateAlpha(self.empireFlag, self.empireFlagCurAlpha, self.empireFlagDestAlpha)

	def __UpdateAlpha(self, dict, curAlphaDict, destAlphaDict):
		for key, img in dict.items():

			curAlpha = curAlphaDict[key]
			destAlpha = destAlphaDict[key]

			if abs(destAlpha - curAlpha) / 10 > 0.0001:
				curAlpha += (destAlpha - curAlpha) / 7
			else:
				curAlpha = destAlpha

			curAlphaDict[key] = curAlpha
			img.SetAlpha(curAlpha)

	def OnPressEscapeKey(self):
		self.ClickExitButton()
		return TRUE

class ReselectEmpireWindow(SelectEmpireWindow):
	def ClickSelectButton(self):
		net.SendSelectEmpirePacket(self.empireID)
		self.stream.SetCreateCharacterPhase()

	def ClickExitButton(self):
		self.stream.SetSelectCharacterPhase()
