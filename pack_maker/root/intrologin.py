import os
import dbg
import app
import net
import ui
import ime
import snd
import wndMgr
import musicInfo
import serverInfo
import systemSetting
import ServerStateChecker
import localeInfo
import constInfo
import uiCommon
import time
import serverCommandParser
import ime
import uiScriptLocale
import nano_interface

REG_PATH = r"SOFTWARE\Apollo"
used = 0

LOGIN_DELAY_SEC = 0

saveSrv = 0
saveInformation = 0

RUNUP_MATRIX_AUTH = False
NEWCIBN_PASSPOD_AUTH = False

LOGIN_DELAY_SEC = 0.0
SKIP_LOGIN_PHASE = False
SKIP_LOGIN_PHASE_SUPPORT_CHANNEL = False
FULL_BACK_IMAGE = False

PASSPOD_MSG_DICT = {}

VIRTUAL_KEYBOARD_NUM_KEYS = 46
VIRTUAL_KEYBOARD_RAND_KEY = True

def Suffle(src):
	if VIRTUAL_KEYBOARD_RAND_KEY:
		items = [item for item in src]

		itemCount = len(items)
		for oldPos in xrange(itemCount):
			newPos = app.GetRandom(0, itemCount-1)
			items[newPos], items[oldPos] = items[oldPos], items[newPos]

		return "".join(items)
	else:
		return src

if localeInfo.IsNEWCIBN() or localeInfo.IsCIBN10():
	LOGIN_DELAY_SEC = 60.0
	FULL_BACK_IMAGE = True
	NEWCIBN_PASSPOD_AUTH = True
	PASSPOD_MSG_DICT = {
		"PASERR1"	: localeInfo.LOGIN_FAILURE_PASERR1,
		"PASERR2"	: localeInfo.LOGIN_FAILURE_PASERR2,
		"PASERR3"	: localeInfo.LOGIN_FAILURE_PASERR3,
		"PASERR4"	: localeInfo.LOGIN_FAILURE_PASERR4,
		"PASERR5"	: localeInfo.LOGIN_FAILURE_PASERR5,
	}

elif localeInfo.IsYMIR() or localeInfo.IsCHEONMA():
	FULL_BACK_IMAGE = True

elif localeInfo.IsHONGKONG():
	FULL_BACK_IMAGE = True
	RUNUP_MATRIX_AUTH = True 
	PASSPOD_MSG_DICT = {
		"NOTELE"	: localeInfo.LOGIN_FAILURE_NOTELEBLOCK,
	}

elif localeInfo.IsJAPAN():
	FULL_BACK_IMAGE = True
	
elif localeInfo.IsBRAZIL():
	LOGIN_DELAY_SEC = 60.0

def IsFullBackImage():
	global FULL_BACK_IMAGE
	return FULL_BACK_IMAGE

def IsLoginDelay():
	global LOGIN_DELAY_SEC
	if LOGIN_DELAY_SEC > 0.0:
		return True
	else:
		return False

def GetLoginDelay():
	global LOGIN_DELAY_SEC
	return LOGIN_DELAY_SEC

def set_reg(name, value):
	try:
		_winreg.CreateKey(_winreg.HKEY_CURRENT_USER, REG_PATH)
		registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0,
									   _winreg.KEY_WRITE)
		_winreg.SetValueEx(registry_key, name, 0, _winreg.REG_SZ, value)
		_winreg.CloseKey(registry_key)
		return True
	except WindowsError:
		return False

def get_reg(name):
	try:
		registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0,
									   _winreg.KEY_READ)
		value, regtype = _winreg.QueryValueEx(registry_key, name)
		_winreg.CloseKey(registry_key)
		return value
	except WindowsError:
		return None

def IsRunupMatrixAuth():
	global RUNUP_MATRIX_AUTH
	return RUNUP_MATRIX_AUTH	

def IsNEWCIBNPassPodAuth():
	global NEWCIBN_PASSPOD_AUTH
	return NEWCIBN_PASSPOD_AUTH

def GetLoginDelay():
	global LOGIN_DELAY_SEC
	return LOGIN_DELAY_SEC

app.SetGuildMarkPath("test")

class ConnectingDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/ConnectingDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.countdownMessage = self.GetChild("countdown_message")

		except:
			import exception
			exception.Abort("ConnectingDialog.LoadDialog.BindObject")

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime

		self.Lock()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()		

	def Close(self):
		self.Unlock()
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def SetText(self, text):
		self.message.SetText(text)

	def SetCountDownMessage(self, waitTime):
		self.countdownMessage.SetText("%.0f%s" % (waitTime, localeInfo.SECOND))

	def SAFE_SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def SAFE_SetExitEvent(self, event):
		self.eventExit = ui.__mem_func__(event)

	AboutWindow = None
	def OnUpdate(self):
		if self.AboutWindow:
			if self.AboutWindow.x_counter > 1:
				self.AboutWindow.x_counter -=1
				self.AboutWindow.text6.SetText("Cargando : %0.1f" % (self.AboutWindow.x_counter/25.0))
			elif self.AboutWindow.x_counter == 1:
				self.AboutWindow.Hide()
				# self.AboutWindow.Delete()
		ServerStateChecker.Update()

	def OnPressExitKey(self):
		#self.eventExit()
		return True

class LoginWindow(ui.ScriptWindow):

	IS_TEST = net.IsTest()

	def __init__(self, stream):
		print "NEW LOGIN WINDOW  ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)
		if constInfo.NEW_LOGIN_INTERFACE == 1:
			playerSettingModule.LoadGameData("INIT")
			playerSettingModule.LoadGameData("NPC")
			playerSettingModule.LoadGameData("EFFECT")
			playerSettingModule.LoadGameData("ENEMY")
			playerSettingModule.LoadGameData("SKILL")
			playerSettingModule.LoadGameData("SHAMAN")
			playerSettingModule.LoadGameData("SURA")
			playerSettingModule.LoadGameData("ASSASSIN")
			playerSettingModule.LoadGameData("WARRIOR")
			self.map_options = None
		self.stream = stream
	
		self.aID = None
		
		self.BtnSrv = {}
		self.TxtSrv = {}
		self.keys = {}
		self.accountText = {}
		self.saveButton = {}
		self.deleteButton = {}
		
		self.index = 0
		count = 0	
		

	def __del__(self):
		ui.ScriptWindow.__del__(self)

		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)

	def Open(self):
		self.loginFailureMsgDict={

			"ALREADY"	: localeInfo.LOGIN_FAILURE_ALREAY,
			"NOID"		: localeInfo.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL"		: localeInfo.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN"	: localeInfo.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR"	: localeInfo.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK"		: localeInfo.LOGIN_FAILURE_BLOCK_ID,
			"WRONGMAT"	: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER,
			"QUIT"		: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER_TRIPLE,
			"BESAMEKEY"	: localeInfo.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL"	: localeInfo.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL"	: localeInfo.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN"	: localeInfo.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK"	: localeInfo.LOGIN_FAILURE_WEB_BLOCK,
		}

		self.loginFailureFuncDict = {
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"WRONGMAT"	: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER,
			"QUIT"		: app.Exit,
		}
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

### Script
		self.SetWindowName("LoginWindow")
		self.__LoadScript(nano_interface.SCRIPTS + "login.py")
### END Script

		if musicInfo.loginMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/" + musicInfo.loginMusic)

		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		ime.AddExceptKey(91)
		ime.AddExceptKey(93)

		self.SetServerAndCh(0)
		self.board["ID"].SetFocus()
		#self.board["remebermeTxt"].Hide()
		
		if constInfo.TEST_FUNCTION == 1:
			self.pressKey()
			

		#if get_reg("1_id"):
		#	self.board["remebermeTxt"].SetText("%s" % binascii.a2b_base64("%s" % get_reg("1_id")))
		#	if self.board["remebermeTxt"].GetText() == "":
		#		self.board["remebermeBtn"].SetUp()
		#	else:
		#		self.board["ID"].SetText("%s" % binascii.a2b_base64("%s" % get_reg("1_id")))
		#		self.board["PW"].SetText("%s" % binascii.a2b_base64("%s" % get_reg("1_pwd")))
		#		self.board["PW"].HidePlace()
		#		self.board["remebermeBtn"].Down()
			
		self.Show()
		app.ShowCursor()
	
	def Close(self):
		if musicInfo.loginMusic != "" and musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.loginMusic)

		self.board["ID"].SetTabEvent(0)
		self.board["ID"].SetReturnEvent(0)
		self.board["PW"].SetReturnEvent(0)
		self.board["PW"].SetTabEvent(0)

		self.board["ID"] = None
		self.board["PW"] = None

		if self.stream.popupWindow:
			self.stream.popupWindow.Close()

		self.Hide()
		app.HideCursor()
		ime.ClearExceptKey()

		if constInfo.NEW_LOGIN_INTERFACE:
			background.Destroy()

	def __SaveChannelInfo(self):
		try:
			file=open("channel.inf", "w")
			file.write("%d %d %d" % (self.__GetServerID(), self.__GetChannelID(), self.__GetRegionID()))
		except:
			print "LoginWindow.__SaveChannelInfo - SaveError"

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
			return -1, -1, -1

	def OnConnectFailure(self):
		snd.PlaySound("sound/ui/loginfail.wav")

		self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE)

	def OnHandShake(self):
		if not IsLoginDelay():
			snd.PlaySound("sound/ui/loginok.wav")
			self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_SUCCESS)

	def OnLoginStart(self):
		if not IsLoginDelay():
			self.PopupNotifyMessage(localeInfo.LOGIN_PROCESSING)

	def OnLoginFailure(self, error):
		try:
			loginFailureMsg = self.loginFailureMsgDict[error]
		except KeyError:
			loginFailureMsg = localeInfo.LOGIN_FAILURE_UNKNOWN  + error

		loginFailureFunc=self.loginFailureFuncDict.get(error)

		self.PopupNotifyMessage(loginFailureMsg)
		snd.PlaySound("sound/ui/loginfail.wav")

	def PopupNotifyMessage(self, message, color = nano_interface.COLOR_RED, status=1):
		self.board["loginDialog"].SetText(message)
		self.board["loginDialog"].SetPackedFontColor(color)
		self.board["loginDialog"].SetOutline()
		self.board["loginDialog"].SetFeather(False)
		
		if status == 1:
			self.board["loginDialog"].Show()
			return

		self.board["loginDialog"].Hide()


	def __LoadScript(self, fileName):
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, fileName)

			self.board = {
				#"backgr"	: self.GetChild("background_el"),
				#"board"	: self.GetChild("board"),
				## Inputs
				"ID" : self.GetChild("placeHolderId"),
				"PW" : self.GetChild("placeHolderPw"),
				"loadingAnimation" : self.GetChild("loadAnim"),
				"loginDialog" : self.GetChild("loginInfor"),
				"loginButton" : self.GetChild("loginBtn"),
				## Channels
				"Channels" : [self.GetChild("channel_%d" % (i+1)) for i in xrange(4)],
				#"chText" : [self.GetChild("chText_%d" % (i+1)) for i in xrange(4)],
				## Remember Me
				#"remebermeBtn" : self.GetChild("remeberBtn"),
				#"remebermeTxt" : self.GetChild("remeberTxt"),
				#"remebermeInf" : self.GetChild("remebermeInf"),
				"textLink_user" : self.GetChild("link_user"),
				"textLink_account" : self.GetChild("link_acc"),

				"account" : [self.GetChild("account_%d" % (i+1)) for i in xrange(6)],
				"account_1_txt" : self.GetChild("account_1_txt"),
				"account_2_txt" : self.GetChild("account_2_txt"),
				"account_3_txt" : self.GetChild("account_3_txt"),
				"account_4_txt" : self.GetChild("account_4_txt"),
				"account_5_txt" : self.GetChild("account_5_txt"),
				"account_6_txt" : self.GetChild("account_6_txt"),
				"account_1_delete" : self.GetChild("account_1_delete"),
				"account_2_delete" : self.GetChild("account_2_delete"),
				"account_3_delete" : self.GetChild("account_3_delete"),
				"account_4_delete" : self.GetChild("account_4_delete"),
				"account_5_delete" : self.GetChild("account_5_delete"),
				"account_6_delete" : self.GetChild("account_6_delete"),
				
				"saveBtn" : self.GetChild("saveBtn"),
				"saveInf" : self.GetChild("saveInf"),
				
				#"change_es" : self.GetChild("change_es"),
				#"change_en" : self.GetChild("change_en"),
				#"change_de" : self.GetChild("change_de"),
				#"change_pt" : self.GetChild("change_pt"),
				#"change_ru" : self.GetChild("change_ru"),
				#"change_pl" : self.GetChild("change_pl"),
			}

		except:
			import exception
			exception.Abort("LoginWindow.__LoadScript.BindObject")

		self.board["loadingAnimation"].Hide()
		self.board["loginDialog"].Hide()
		
		self.board["loginButton"].SetEvent(self.__OnClickLoginButton)
		#self.board["remebermeBtn"].SetToggleUpEvent(self.deleteAccountFunction)
		#self.board["remebermeBtn"].SetToggleDownEvent(self.saveAccountFunction)
		
		self.board["textLink_user"].SetEvent(self.supportProblems,1)
		self.board["textLink_account"].SetEvent(self.supportProblems,2)
		#### Inputs
		self.board["PW"].SetSecret(1)
		self.board["ID"].SetPlaceHolderText(localeInfo.ID_HOLD)
		self.board["PW"].SetPlaceHolderText(localeInfo.PW_HOLD)
		
		self.board["ID"].SetReturnEvent(ui.__mem_func__(self.board["PW"].SetFocus))
		self.board["ID"].SetTabEvent(ui.__mem_func__(self.board["PW"].SetFocus))

		self.board["PW"].SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
		self.board["PW"].SetTabEvent(ui.__mem_func__(self.board["ID"].SetFocus))
		#### AcountSave
		self.board["saveBtn"].SetToggleDownEvent(self.__GuardarCuenta)
	
		self.board["account"][0].SetEvent(lambda arg=0: self.__OnClickAccounts(arg))
		self.board["account"][1].SetEvent(lambda arg=1: self.__OnClickAccounts(arg))
		self.board["account"][2].SetEvent(lambda arg=2: self.__OnClickAccounts(arg))
		self.board["account"][3].SetEvent(lambda arg=3: self.__OnClickAccounts(arg))
		self.board["account"][4].SetEvent(lambda arg=3: self.__OnClickAccounts(arg))
		self.board["account"][5].SetEvent(lambda arg=3: self.__OnClickAccounts(arg))

		self.board["account_1_delete"].SetEvent(self.__OnClickCleanAccounts_1)
		self.board["account_2_delete"].SetEvent(self.__OnClickCleanAccounts_2)
		self.board["account_3_delete"].SetEvent(self.__OnClickCleanAccounts_3)
		self.board["account_4_delete"].SetEvent(self.__OnClickCleanAccounts_4)
		self.board["account_5_delete"].SetEvent(self.__OnClickCleanAccounts_5)
		self.board["account_6_delete"].SetEvent(self.__OnClickCleanAccounts_6)
		#### ModoPerros

		#self.board["change_es"].SetEvent(self.__OnClickChangeEs)
		#self.board["change_en"].SetEvent(self.__OnClickChangeEn)
		#self.board["change_de"].SetEvent(self.__OnClickChangeDe)
		#self.board["change_pt"].SetEvent(self.__OnClickChangePt)
		#self.board["change_ru"].SetEvent(self.__OnClickChangeRu)
		#self.board["change_pl"].SetEvent(self.__OnClickChangePl)

		self.__CargarCuentas()
		self.Channel_select()
				
	def Channel_select(self):
		self.board["Channels"][0].SetEvent(lambda : self.ChannelEvents(0,1))
		self.board["Channels"][0].Down()
		#self.board["chText"][0].SetPackedFontColor(nano_interface.COLOR_HOVER)
		self.board["Channels"][1].SetEvent(lambda : self.ChannelEvents(1,2))
		self.board["Channels"][2].SetEvent(lambda : self.ChannelEvents(2,3))	
		self.board["Channels"][3].SetEvent(lambda : self.ChannelEvents(3,4))	

	def ChannelEvents(self,arg,channel):
		global saveSrv
		for btn in self.board["Channels"]:
			btn.SetUp()
			#for ex in self.board["chText"]:
			#	ex.SetPackedFontColor(nano_interface.COLOR_NORMAL)

		self.board["Channels"][arg].Down()
		#self.board["chText"][arg].SetPackedFontColor(nano_interface.COLOR_HOVER)

		if	1 <= channel and channel <= 4:
			nano_interface.SERVERS_LIST_DICT[saveSrv]['CH%s' % channel]
			self.stream.SetConnectInfo(nano_interface.SERVERS_LIST_DICT[0]['ip'], nano_interface.SERVERS_LIST_DICT[0]['CH%s' % channel], nano_interface.SERVERS_LIST_DICT[0]['ip'], nano_interface.SERVERS_LIST_DICT[0]['auth'])
			if channel == 1:
				net.SetServerInfo(nano_interface.name+nano_interface.name_channel1)
			elif channel == 2:
				net.SetServerInfo(nano_interface.name+nano_interface.name_channel2)
			elif channel == 3:
				net.SetServerInfo(nano_interface.name+nano_interface.name_channel3)
			elif channel == 4:
				net.SetServerInfo(nano_interface.name+nano_interface.name_channel4)
			self.__SaveChannelInfo()
	
			# dbg.LogBox("%s" % nano_interface.SERVERS_LIST_DICT[saveSrv]['CH%s' % channel])
	
	def SetServerAndCh(self, srv=0):
		self.stream.SetConnectInfo(nano_interface.SERVERS_LIST_DICT[srv]['ip'], nano_interface.SERVERS_LIST_DICT[srv]['CH1'], nano_interface.SERVERS_LIST_DICT[srv]['ip'], nano_interface.SERVERS_LIST_DICT[srv]['auth'])
		net.SetMarkServer(nano_interface.SERVERS_LIST_DICT[srv]['ip'], nano_interface.SERVERS_LIST_DICT[srv]['CH1'])
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")
		net.SetServerInfo(nano_interface.name+nano_interface.name_channel1)
	
	def __SetServerInfo(self, name):
		net.SetServerInfo(name.strip())

	def __GetRegionID(self):
		return 0

	def __GetServerID(self):
		return

	def __GetChannelID(self):
		return

	def __ActivarPerros_1(self):
		constInfo.mob_perro = 0

	def __ActivarPerros_2(self):
		constInfo.mob_perro = 1
		
	def __ActivarPerros_3(self):
		constInfo.mob_perro = 2

	def __OnClickAccounts(self, arg):
		ind = int(arg)
		self.Valuebottonpostfile = ind
		listafiles = ["account1.txt","account2.txt","account3.txt","account4.txt","account5.txt","account6.txt"]
		vardiraccount = "lib/accountsave/"
		file = open(vardiraccount+listafiles[self.Valuebottonpostfile], "r")
		c = 0
		for btn in self.board["account"]:
			btn.SetUp()		
		self.board["account"][arg].Down()
		
		self.board["ID"].SetText("")
		self.board["PW"].SetText("")

		for i in file:
			if c == 0:
				self.board["ID"].SetText(i.replace("\n",""))
			else:
				self.board["PW"].SetText(i.replace("\n",""))
				
			c = 1
		file.close()

	def __GuardarCuenta(self):
		id = self.board["ID"].GetText()
		pwd = self.board["PW"].GetText()
		
		fd = open("lib/accountsave/account1.txt")
		login1 = fd.readline()
		login1.replace( "\n", "" )
		fd.close()

		fd = open("lib/accountsave/account2.txt")
		login2 = fd.readline()
		login2.replace( "\n", "" )
		fd.close()

		fd = open("lib/accountsave/account3.txt")
		login3 = fd.readline()
		login3.replace( "\n", "" )
		fd.close()

		fd = open("lib/accountsave/account4.txt")
		login4 = fd.readline()
		login4.replace( "\n", "" )
		fd.close()
		
		if login1 == "":
			slot = 1
		elif login2 == "":
			slot = 2
		elif login3 == "":
			slot = 3
		elif login4 == "":
			slot = 4
		else:
			self.PopupNotifyMessage("��dn� m�sto pro ulo�en� dal��ch ��t�!")
			return
			
		if id == "":
			self.PopupNotifyMessage("Mus�te napsat ID a heslo.")
			return

		if pwd == "":
			self.PopupNotifyMessage("Mus�te napsat heslo.")
			return

		f = open("lib/accountsave/account" + str(slot) + ".txt", "w")
		f.write(id +"\n")
		f.write(pwd)
		f.close()
		
		self.PopupNotifyMessage("V� ��et byl ulo�en!.")
		self.__CargarCuentas()
	
	def __CargarCuentas(self):
		fd = open("lib/accountsave/account1.txt")
		login1 = fd.readline()
		login1.replace( "\n", "" )
		fd.close()

		fd = open("lib/accountsave/account2.txt")
		login2 = fd.readline()
		login2.replace( "\n", "" )
		fd.close()

		fd = open("lib/accountsave/account3.txt")
		login3 = fd.readline()
		login3.replace( "\n", "" )
		fd.close()

		fd = open("lib/accountsave/account4.txt")
		login4 = fd.readline()
		login4.replace( "\n", "" )
		fd.close()

		fd = open("lib/accountsave/account5.txt")
		login5 = fd.readline()
		login5.replace( "\n", "" )
		fd.close()

		fd = open("lib/accountsave/account6.txt")
		login6 = fd.readline()
		login6.replace( "\n", "" )
		fd.close()
	
		if login1 != "":
			self.board["account_1_txt"].SetText(login1)
		else:
			self.board["account_1_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT)
			
		if login2 != "":
			self.board["account_2_txt"].SetText(login2)
		else:
			self.board["account_2_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT)
			
		if login3 != "":
			self.board["account_3_txt"].SetText(login3)
		else:
			self.board["account_3_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT)
			
		if login4 != "":
			self.board["account_4_txt"].SetText(login4)
		else:
			self.board["account_4_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT)
			
		if login5 != "":
			self.board["account_5_txt"].SetText(login5)
		else:
			self.board["account_5_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT)
			
		if login6 != "":
			self.board["account_6_txt"].SetText(login6)
		else:
			self.board["account_6_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT)

	def __OnClickCleanAccounts_1(self):
		f = open("lib/accountsave/account1.txt", "w")
		f.write ("")
		f.close()
		self.board["account_1_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT+" 1 - "+uiScriptLocale.INTRO_LOGIN_EMPTY)
		self.__CargarCuentas()
		
	def __OnClickCleanAccounts_2(self):
		f = open("lib/accountsave/account2.txt", "w")
		f.write ("")
		f.close()
		self.board["account_2_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT+" 2 - "+uiScriptLocale.INTRO_LOGIN_EMPTY)
		self.__CargarCuentas()
		
	def __OnClickCleanAccounts_3(self):
		f = open("lib/accountsave/account3.txt", "w")
		f.write ("")
		f.close()
		self.board["account_3_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT+" 3 - "+uiScriptLocale.INTRO_LOGIN_EMPTY)
		self.__CargarCuentas()
		
	def __OnClickCleanAccounts_4(self):
		f = open("lib/accountsave/account4.txt", "w")
		f.write ("")
		f.close()
		self.board["account_4_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT+" 4 - "+uiScriptLocale.INTRO_LOGIN_EMPTY)
		self.__CargarCuentas()
		
	def __OnClickCleanAccounts_5(self):
		f = open("lib/accountsave/account4.txt", "w")
		f.write ("")
		f.close()
		self.board["account_5_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT+" 5 - "+uiScriptLocale.INTRO_LOGIN_EMPTY)
		self.__CargarCuentas()
		
	def __OnClickCleanAccounts_6(self):
		f = open("lib/accountsave/account4.txt", "w")
		f.write ("")
		f.close()
		self.board["account_6_txt"].SetText(uiScriptLocale.INTRO_LOGIN_ACCOUNT+" 6 - "+uiScriptLocale.INTRO_LOGIN_EMPTY)
		self.__CargarCuentas()
		
	def __OnClickChangeEs(self):
		file = open("locale.cfg", "w")
 		file.write("10002 65001 es") 
		file.close()
		dbg.LogBox("El idioma ha sido cambiado a Espanol!")
		dbg.LogBox("El cliente se Reiniciara.")
		dbg.LogBox("Puedes cambiar el idioma del servidor en Uriel NPC")
		os.system('start Angel2Launcher.exe')
		app.Exit()
		
	def __OnClickChangeEn(self):
		file = open("locale.cfg", "w")
 		file.write("10002 65001 en") 
		file.close()
		dbg.LogBox("The laguage of client was changed to English!")
		dbg.LogBox("Client will restart.")
		dbg.LogBox("You can change language server in Uriel NPC")
		os.system('start Angel2Launcher.exe')
		app.Exit()

	def __OnClickChangeDe(self):
		file = open("locale.cfg", "w")
 		file.write("10002 65001 de") 
		file.close()
		dbg.LogBox("Die Spielsprache wurde auf Deutsch verandert.")
		dbg.LogBox("Das Spiel wird neugestartet.")
		dbg.LogBox("Du kannst die Sprache jederzeit bei Uriel andern.")
		os.system('start Angel2Launcher.exe')
		app.Exit()
		
	def __OnClickChangePt(self):
		file = open("locale.cfg", "w")
 		file.write("10002 65001 pt") 
		file.close()
		dbg.LogBox("Foi mudado o idioma para Portugues!")
		dbg.LogBox("O cliente vai ser Reiniciado.")
		dbg.LogBox("Podes mudar o idioma do servidor no NPC Uriel")
		os.system('start Angel2Launcher.exe')
		app.Exit()
		
	def __OnClickChangeRu(self):
		file = open("locale.cfg", "w")
 		file.write("10002 65001 ro") 
		file.close()
		dbg.LogBox("Limba a fost schimbata in roman?!")
		dbg.LogBox("Clientul se va restarta.")
		dbg.LogBox("Poti schimba limba serverului la Uriel NPC")
		os.system('start Angel2Launcher.exe')
		app.Exit()
		
	def __OnClickChangePl(self):
		file = open("locale.cfg", "w")
 		file.write("10002 65001 pl") 
		file.close()
		dbg.LogBox("The laguage of client was changed to Polish!")
		dbg.LogBox("Client will restart.")
		dbg.LogBox("You can change language server in Uriel NPC")
		os.system('start Angel2Launcher.exe')
		app.Exit()

	def Connect(self, id, pwd):
		if constInfo.SEQUENCE_PACKET_ENABLE:
			net.SetPacketSequenceMode()

		self.stream.popupWindow.Close()
		self.PopupNotifyMessage(localeInfo.LOGIN_CONNETING, nano_interface.SING_IN_COLOR)

		self.stream.SetLoginInfo(id, pwd)
		self.stream.Connect()

	def __OnClickLoginButton(self):
		id = self.board["ID"].GetText()
		pwd = self.board["PW"].GetText()
		if len(id)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_ID)
			return

		if len(pwd)==0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_PASSWORD)
			return

		self.Connect(id, pwd)
		
	if constInfo.TEST_FUNCTION == 1:
		def pressKey(self):
			onPressKeyDict = {}

			onPressKeyDict[app.DIK_F1]	= lambda : self.debug_script()
			# onPressKeyDict[app.DIK_F2]	= lambda : self.autoLogin(1)
			# onPressKeyDict[app.DIK_F3]	= lambda : self.autoLogin(2)
			# onPressKeyDict[app.DIK_F4]	= lambda : self.autoLogin(3)

			self.onPressKeyDict = onPressKeyDict

		def OnKeyDown(self, key):
			try:
				self.onPressKeyDict[key]()
			except KeyError:
				pass
			except:
				raise

			return True
		
		def debug_script(self):
			import mtdbg
			mtdbg.LoadMichaFile("test_script.py", "TestWindow")
	
	def OnPressExitKey(self):
		if self.stream.popupWindow:
			self.stream.popupWindow.Close()
		self.stream.SetPhaseWindow(0)
		return TRUE

	#def deleteAccountFunction(self):
	#	if get_reg("1_id"):
	#		set_reg("1_id", "")
	#		set_reg("1_pwd", "")
	#		self.board["remebermeTxt"].SetText("")
	#		self.board["ID"].SetText("")
	#		self.board["PW"].SetText("")
	#	else:
	#		self.PopupNotifyMessage(localeInfo.DELETE_FAIL)
	#		self.board["remebermeBtn"].Down()

	def saveAccountFunction(self):
		return
	#	if self.board["ID"].GetText() == "" or self.board["PW"].GetText() == "":
	#		self.PopupNotifyMessage(localeInfo.SAVE_FAIL)
	#		self.board["remebermeBtn"].SetUp()
	#		return
			
	#	if get_reg("1_id"):
	#		set_reg("1_id", "")
	#		set_reg("1_pwd", "")

	#	if get_reg("1_id") == "" or get_reg("1_id") == None:
	#		set_reg("1_id", str(binascii.b2a_base64(self.board["ID"].GetText())))
	#		set_reg("1_pwd", str(binascii.b2a_base64(self.board["PW"].GetText())))
	#		self.board["remebermeTxt"].SetText(self.board["ID"].GetText())
	#		self.PopupNotifyMessage(localeInfo.SAVE_SUCCESFULLY, 0xff03969b)

	def supportProblems(self, switch):
		if switch == 1:
			os.system("start " + nano_interface.FORGOT_PASSWORD)
		elif switch == 2:
			os.system("start " + nano_interface.CREATE_ACCOUNT)

	def OnRender(self): #really..care e sensul la pass..
		if constInfo.NEW_LOGIN_INTERFACE:
			app.RenderGame()
			import grp
			grp.PopState()
			grp.SetInterfaceRenderState()