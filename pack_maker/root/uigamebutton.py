import app
import ui
import player
import net
import dbg
if app.ENABLE_PVP_TOURNAMENT:
	import constInfo

class GameButtonWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow("UIScript/gamewindow.py")

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self, filename):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, filename)
		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return False

		try:
			self.gameButtonDict={
				"STATUS" : self.GetChild("StatusPlusButton"),
				"SKILL" : self.GetChild("SkillPlusButton"),
				"QUEST" : self.GetChild("QuestButton"),
				"HELP" : self.GetChild("HelpButton"),
				"BUILD" : self.GetChild("BuildGuildBuilding"),
				"GIFT" : self.GetChild("GiftIcon"),
				"EXIT_OBSERVER" : self.GetChild("ExitObserver"),
				"COMBAT_ZONE" : self.GetChild("CombatZone"),
				"BOSS_EVENT" : self.GetChild("BossEvent"),
				"METIN_EVENT" : self.GetChild("MetinEvent"),
			}

			if app.ENABLE_PVP_TOURNAMENT:
				self.gameButtonDict["EXIT_CAMERA_MODE"] = self.GetChild("ExitCameraMode")
				self.gameButtonDict["EXIT_CAMERA_MODE"].SetEvent(ui.__mem_func__(self.__OnClickExitCameraMode))

			self.gameButtonDict["EXIT_OBSERVER"].SetEvent(ui.__mem_func__(self.__OnClickExitObserver))

		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return False

		self.__HideAllGameButton()
		self.SetObserverMode(player.IsObserverMode())
		return True

	def ShowBossButton(self):
		self.gameButtonDict["BOSS_EVENT"].Show()
		
	def HideBossButton(self):
		self.gameButtonDict["BOSS_EVENT"].Hide()

	def ShowMetinButton(self):
		self.gameButtonDict["METIN_EVENT"].Show()

	def HideMetinButton(self):
		self.gameButtonDict["METIN_EVENT"].Hide()

	def ShowCombatButton(self):
		self.gameButtonDict["COMBAT_ZONE"].Show()
		
	def HideCombatButton(self):
		self.gameButtonDict["COMBAT_ZONE"].Hide()

	def ShowGiftButton(self):
		self.gameButtonDict["GIFT"].Show()

	def HideGiftButton(self):
		self.gameButtonDict["GIFT"].Hide()

	def Destroy(self):
		for key in self.gameButtonDict:
			self.gameButtonDict[key].SetEvent(0)

		self.gameButtonDict={}

	def SetButtonEvent(self, name, event):
		try:
			self.gameButtonDict[name].SetEvent(event)
		except Exception, msg:
			print "GameButtonWindow.LoadScript - %s" % (msg)
			app.Abort()
			return

	def ShowBuildButton(self):
		self.gameButtonDict["BUILD"].Show()

	def HideBuildButton(self):
		self.gameButtonDict["BUILD"].Hide()

	def CheckGameButton(self):

		if not self.IsShow():
			return

		statusPlusButton=self.gameButtonDict["STATUS"]
		skillPlusButton=self.gameButtonDict["SKILL"]
		helpButton=self.gameButtonDict["HELP"]

		if player.GetStatus(player.STAT) > 0:
			statusPlusButton.Show()
		else:
			statusPlusButton.Hide()

		if self.__IsSkillStat():
			skillPlusButton.Show()
		else:
			skillPlusButton.Hide()

		if 0 == player.GetPlayTime():
			helpButton.Show()
		else:
			helpButton.Hide()

	def __IsSkillStat(self):
		if player.GetStatus(player.SKILL_ACTIVE) > 0:
			return True

		return False

	def __OnClickExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def __HideAllGameButton(self):
		for btn in self.gameButtonDict.values():
			btn.Hide()

	def SetObserverMode(self, isEnable):
		if isEnable:
			self.gameButtonDict["EXIT_OBSERVER"].Show()
		else:
			self.gameButtonDict["EXIT_OBSERVER"].Hide()

	if app.ENABLE_PVP_TOURNAMENT:
		def __OnClickExitCameraMode(self):
			if app.GUILD_WAR_COUNTER:
				interface = constInfo.GetInterfaceInstance()
				if interface != None:
					if interface.wndGuildWar:
						interface.wndGuildWar.ExitCameraMode()

			if app.ENABLE_PVP_TOURNAMENT:
				interface = constInfo.GetInterfaceInstance()
				if interface != None:
					if interface.wndPvPDuel:
						interface.wndPvPDuel.ExitCameraMode()

		def UpdateCameraMode(self):
			isEnable = player.GetCameraMode()
			if isEnable:
				self.gameButtonDict["EXIT_CAMERA_MODE"].Show()
			else:
				self.gameButtonDict["EXIT_CAMERA_MODE"].Hide()
