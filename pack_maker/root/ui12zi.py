import app,chr,chrmgr,player,net,systemSetting,background,chat,event
import wndMgr, mouseModule, grp, ui, localeInfo, uiToolTip, uiCommon, constInfo
from _weakref import proxy

class MapTextToolTip(ui.Window):
	def __init__(self):			
		ui.Window.__init__(self)
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetOutline()
		if localeInfo.IsARABIC():
			textLine.SetHorizontalAlignLeft()
		else:
			textLine.SetHorizontalAlignRight()
		textLine.Show()
		self.textLine = textLine

	def __del__(self):			
		ui.Window.__del__(self)
	def SetText(self, text):
		self.textLine.SetText(text)
	def SetTooltipPosition(self, PosX, PosY):
		self.textLine.SetPosition(PosX - 5, PosY)
	def SetTextColor(self, TextColor):
		self.textLine.SetPackedFontColor(TextColor)
	def GetTextSize(self):
		return self.textLine.GetTextSize()
class BeadWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		#self.SetWindowName("Bead")
		self.BeadIcon = None
		self.beadInfo = None
		self.time =  0
		#self.count =  0
		self.tooltipInfo = None
		self.ShowButtonToolTip = False
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/Bead.py")

		except:
			import exception
			exception.Abort("BeadWindow.__LoadWindow.UIScript/Bead.py")

		self.BeadIcon = self.GetChild("Bead_image")
		self.beadInfo = self.GetChild("beadInfo")

		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.SetText(localeInfo.BEAD)
		self.tooltipInfo.Show()
		self.beadInfo.Show()
		(ButtonPosX, ButtonPosY) = self.BeadIcon.GetGlobalPosition()
		self.tooltipInfo.SetTooltipPosition(ButtonPosX, ButtonPosY)

	def NextBeadUpdateTime(self, value):
		self.time = int(value)
	def SetBeadCount(self, count):
		self.beadInfo.SetText("%d" % int(count))
	def OnUpdate(self):
		import time
		current_milli_time = int(app.GetGlobalTimeStamp())
		if self.time > 0:
			self.tooltipInfo.SetText(localeInfo.BEAD_TIME_REMAINING_TO_GET+str(localeInfo.BeadTime(int(self.time)-current_milli_time)))
		else:
			self.tooltipInfo.SetText("")
		self.tooltipInfo.Show()
	def Close(self):
		self.Hide()
	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

class FloorLimitTimeWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.JumpStep = None
		self.LeftTime = None
		self.CurrentFloor = None
		self.Time = 0
		self.NextFloor = 0
		self.Floor = 0
		self.CoolTime = 0.
		self.CoolTimeImage = None
		self.btnJump = None
		self.startTime = 0.
		if background.GetCurrentMapName() == "metin2_12zi_stage":
			self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/12FloorInfo.py")

		except:
			import exception
			exception.Abort("FloorLimitTimeWindow.__LoadWindow.UIScript/12FloorInfo.py")

		self.LeftTime = self.GetChild("LeftTime")
		self.JumpStep = self.GetChild("JumpStep")
		self.CurrentFloor = self.GetChild("CurrentFloor")
		self.CoolTimeImage = self.GetChild("CoolTime")
		self.btnJump = self.GetChild("JumpButton")
		self.btnJump.SetEvent(ui.__mem_func__(self.PressJumpButton))
		self.btnJump.Hide()

	def Refresh12ziTimer(self, Time, Nextfloor, Floor):
		self.CoolTimeImage.Hide()
		self.Time = int(Time)
		self.NextFloor = int(Nextfloor)
		self.Floor = int(Floor)
		self.CoolTimeImage.Show()

		if self.Time == 1: # First
			self.CoolTime = 10.
		elif self.Time ==2: # Second
			self.CoolTime = 300.
		elif self.Time ==3: # Third
			self.CoolTime = 600.
		else:
			self.CoolTime = 0.
		self.startTime = app.GetTime() + 0.5
		self.CoolTimeImage.SetCoolTime(self.CoolTime)
		self.CoolTimeImage.SetStartCoolTime(self.startTime)
		self.CurrentFloor.SetText("%dF" % int(self.Floor))
		self.JumpStep.SetText("%dF" % int(self.NextFloor))

	def OnUpdate(self):
		leftTime = max(0, self.startTime + self.CoolTime - app.GetTime() + 0.5)
		leftMin = int(leftTime/60)
		leftSecond = int(leftTime%60)
		self.LeftTime.SetText("%02d:%02d" % (leftMin, leftSecond))
		if self.btnJump.IsShow() and leftTime == 0:
			self.PressJumpButton()
		elif self.NextFloor == 1 and leftTime == 0:
			self.PressJumpButton()
			self.btnJump.Hide()

	def Show12ziJumpButton(self):
		self.btnJump.Show()
		self.btnJump.Enable()

	def PressJumpButton(self):
		event.QuestButtonClick(constInfo.ZodiacLua)
		#net.SendChatPacket("/next_floor")
		self.btnJump.Hide()

	def CloseJumpButton(self):
		self.btnJump.Hide()

	def NextMission(self):
		net.SendChatPacket("/next_floor")
		self.btnJump.Hide()

	def DayorNigh12zi(self):
		if constInfo.ZodiacDayorNight == 0:
			background.RegisterEnvironmentData(1, "d:/ymir work/environment/moonlight04.msenv")
			background.SetEnvironmentData(1)
			constInfo.ZodiacDayorNight=1
		else:
			background.SetEnvironmentData(0)
			constInfo.ZodiacDayorNight=0

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

class Reward12ziWindow(ui.ScriptWindow):
	COLUMN_SIZE = 12
	ROW_SIZE = 10

	COLUMN_ITEM_LIST = ( 33001, 33002, 33003, 33004, 33005, 33006, 33007, 33008, 33009, 33010, 33011, 33012 )
	ROW_ITEM_LIST = ( 33013, 33014, 33015, 33016, 33017, 33018, 33019, 33020, 33021, 33022 )

	WEEKLY_ROW_LIST = ( localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_MON, localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_TUE, localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_WED, localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_THU, localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_FRI, localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_SAT )
	WEEKLY_COLUMN_LIST = ( localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_MON, localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_TUE, localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_WED, localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_THU, localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_FRI, localeInfo.CZ_REWARD_TOOLTIP_WEEKLY_SAT_SUN )

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.enableYellow = True
		self.enableGreen = True
		self.CoverImage1 = {}
		self.btnYellow = None
		self.btnGreen = None
		self.btnAll = None
		self.YellowRewardCount = None
		self.GreenRewardCount = None
		self.questionDialog = None
		self.COLUMN_ITEM_COUNT = {}
		self.COLUMN_ITEM = {}
		self.ROW_ITEM_COUNT = {}
		self.ROW_ITEM = {}
		self.CHECK_BUTTON = ({},{},)
		self.buttontooltip = None
		self.tooltipItem = None
		self.ShowButtonToolTip = False

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def OverInToolTipButton(self, arg):
		arglen = len(str(arg))
		pos_x, pos_y = wndMgr.GetMousePosition()

		self.buttontooltip.ClearToolTip()
		self.buttontooltip.SetThinBoardSize(11 * arglen)
		self.buttontooltip.SetToolTipPosition(pos_x + 50, pos_y + 50)
		self.buttontooltip.AppendTextLine(arg, 0xffffffff)
		self.buttontooltip.Show()
		self.ShowButtonToolTip = True

	def OverOutToolTipButton(self):
		self.buttontooltip.Hide()
		self.ShowButtonToolTip = False

	def ButtonToolTipProgress(self):
		if self.buttontooltip and self.ShowButtonToolTip:
			pos_x, pos_y = wndMgr.GetMousePosition()
			self.buttontooltip.SetToolTipPosition(pos_x, pos_y - 20)

	def EventProgress(self, event_type, arg) :
		print "EventProcess %s " %(event_type)
		if "mouse_click" == event_type :
			self.OverInToolTipButton(arg)
		elif "mouse_over_in" == event_type :
			self.OverInToolTipButton(arg)
		elif "mouse_over_out" == event_type :
			self.OverOutToolTipButton()
		else:
			print " New_introSelect.py ::EventProgress : False"

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def ItemToolTipEvent(self, event_type, arg):
		if "mouse_over_in" == event_type :
			self.tooltipItem.SetItemToolTip(arg)
		elif "mouse_over_out" == event_type :
			self.tooltipItem.HideToolTip()

	## Update
	def OnUpdate(self):
		self.ButtonToolTipProgress()

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/12ziRewardWindow.py")
		except:
			import exception
			exception.Abort("Reward12ziWindow.__LoadWindow.UIScript/12ziRewardWindow.py")

		self.buttontooltip = uiToolTip.ToolTip()
		self.buttontooltip.ClearToolTip()

		self.GetChild("bg_weekly_row").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.CZ_REWARD_TOOLTIP_WEEKLY)
		self.GetChild("bg_weekly_row").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

		self.GetChild("bg_weekly_column").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.CZ_REWARD_TOOLTIP_WEEKLY)
		self.GetChild("bg_weekly_column").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

		for i in xrange(6):
			self.GetChild("bg_weekly_row_%d" % (i+1)).SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", self.WEEKLY_ROW_LIST[i])
			self.GetChild("bg_weekly_row_%d" % (i+1)).SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")
			self.GetChild("bg_weekly_column_%d" % (i+1)).SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", self.WEEKLY_COLUMN_LIST[i])
			self.GetChild("bg_weekly_column_%d" % (i+1)).SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

		self.GetChild("bg_charm_12zi").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.CZ_REWARD_TOOLTIP_12ZI)
		self.GetChild("bg_charm_12zi").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

		for i in xrange(self.COLUMN_SIZE):
			self.GetChild("bg_charm_12zi_%d" % (i+1)).SetEvent(ui.__mem_func__(self.ItemToolTipEvent), "mouse_over_in", self.COLUMN_ITEM_LIST[i])
			self.GetChild("bg_charm_12zi_%d" % (i+1)).SetEvent(ui.__mem_func__(self.ItemToolTipEvent), "mouse_over_out", "")

		self.GetChild("bg_charm_10gan").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.CZ_REWARD_TOOLTIP_10GAN)
		self.GetChild("bg_charm_10gan").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

		for i in xrange(self.ROW_SIZE):
			self.GetChild("bg_charm_10gan_%d" % (i+1)).SetEvent(ui.__mem_func__(self.ItemToolTipEvent), "mouse_over_in", self.ROW_ITEM_LIST[i])
			self.GetChild("bg_charm_10gan_%d" % (i+1)).SetEvent(ui.__mem_func__(self.ItemToolTipEvent), "mouse_over_out", "")

		self.GetChild("bg_count_slot_row").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.CZ_REWARD_TOOLTIP_12ZI_COUNT)
		self.GetChild("bg_count_slot_row").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")
		self.GetChild("bg_count_slot_column").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.CZ_REWARD_TOOLTIP_10GAN_COUNT)
		self.GetChild("bg_count_slot_column").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")
		self.GetChild("bg_need_count_slot_row").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.CZ_REWARD_TOOLTIP_12ZI_NEED_COUNT)
		self.GetChild("bg_need_count_slot_row").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")
		self.GetChild("bg_need_count_slot_column").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.CZ_REWARD_TOOLTIP_10GAN_NEED_COUNT)
		self.GetChild("bg_need_count_slot_column").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

		self.GetChild("YellowInactive").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.CZ_REWARD_TOOLTIP_YELLOW_BOX)
		self.GetChild("YellowInactive").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")
		self.GetChild("GreenInactive").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", localeInfo.CZ_REWARD_TOOLTIP_GREEN_BOX)
		self.GetChild("GreenInactive").SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", "")

		self.btnYellow = self.GetChild("YellowButton")
		# self.btnYellow.SetAlwaysToolTip(True)
		self.btnGreen = self.GetChild("GreenButton")
		# self.btnGreen.SetAlwaysToolTip(True)
		self.btnAll = self.GetChild("AllClearButton")
		# self.btnAll.SetAlwaysToolTip(True)

		self.btnYellow.SetEvent(ui.__mem_func__(self.PressButton),1)
		# self.btnYellow.SetAlwaysToolTip(True)
		self.btnYellow.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_YELLOW_BOX)
		self.btnYellow.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.btnGreen.SetEvent(ui.__mem_func__(self.PressButton),2)
		# self.btnGreen.SetAlwaysToolTip(True)
		self.btnGreen.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_GREEN_BOX)
		self.btnGreen.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.btnAll.SetEvent(ui.__mem_func__(self.PressButton),3)
		# self.btnAll.SetAlwaysToolTip(True)
		self.btnAll.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_ALL_BOX)
		self.btnAll.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		self.CheckButtonWindow = self.GetChild("CheckButtonWindow")
		self.YellowRewardCount = self.GetChild("YellowRewardCount")
		self.GreenRewardCount = self.GetChild("GreenRewardCount")
		


		if len(self.COLUMN_ITEM_COUNT) == 0:
			for i in xrange(self.COLUMN_SIZE):
				TempText = ui.MakeTextLine(self.GetChild("12zi%d" % (i+1)))
				TempText.SetPosition( 0, -21)
				TempText.SetText("%d" % (0))
				self.COLUMN_ITEM_COUNT[i] = TempText
				self.InsertChild("12ziCount%d" % (i), TempText)

			for i in xrange(self.ROW_SIZE):
				TempText = ui.MakeTextLine(self.GetChild("10gan%d" % (i+1)))
				TempText.SetPosition( -28, 7)
				TempText.SetText("%d" % (0))
				self.ROW_ITEM_COUNT[i] = TempText
				self.InsertChild("10ganCount%d" % (i), TempText)

		if self.CheckButtonWindow.GetChildCount() != 0:
			return
		else:
			for i in xrange(self.COLUMN_SIZE):
				for j in xrange(self.ROW_SIZE):
					if i%2 == j%2:
						if j%2 == 0:
							CheckButton = ui.MakeButton(self.CheckButtonWindow, i*28, j*28, "", "d:/ymir work/ui/game/12zi/reward/", "check_yellow.sub", "clear_yellow.sub", "clear_yellow.sub")

							index = i/2+(j/2)*6
							self.CHECK_BUTTON[0][index] = CheckButton
							CheckButton.SAFE_SetEvent(self.PressCheckButton, index)
							CheckButton.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_COMPLETABLE)
							CheckButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_COMPLETABLE)
							#CheckButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
							self.InsertChild("%d_%d" % (i,j), CheckButton)
						else:
							CheckButton = ui.MakeButton(self.CheckButtonWindow, i*28, j*28, "", "d:/ymir work/ui/game/12zi/reward/", "check_green.sub", "clear_green.sub", "clear_green.sub")

							index = i/2+(j/2)*6
							self.CHECK_BUTTON[1][index] = CheckButton
							CheckButton.SAFE_SetEvent(self.PressCheckButton, 30+index)
							CheckButton.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_COMPLETABLE)
							CheckButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_COMPLETABLE)
							# CheckButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
							self.InsertChild("%d_%d" % (i,j), CheckButton)

	def PressButton(self, type):
		if type == 1:
			self.btnYellow.Down()
			self.btnYellow.Disable()
		elif type == 2:
			self.btnGreen.Down()
			self.btnGreen.Disable()
		else:
			self.btnAll.Down()
			self.btnAll.Disable()
		#chat.AppendChat(chat.CHAT_TYPE_INFO, "Type:%d" % (type))
		net.SendChatPacket("/cz_reward %d" % (type))

	def PressCheckButton(self, value):
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.CZ_REWARD_QUESTION_COMPLETE)
		questionDialog.SetAcceptEvent(lambda arg1=value: self.SendClear(arg1))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		questionDialog.Open()
		self.questionDialog = questionDialog

	def SendClear(self, value):
		type = 0
		if value >= 30:
			type = 1
			value = value - 30
		#chat.AppendChat(chat.CHAT_TYPE_INFO, "Type:%d Value:%d" % (type, value))
		net.SendChatPacket("/cz_check_box %d %d" % (type, value))
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return
		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def Open(self, yellowmark, greenmark, yellowreward, greenreward):
		for i in xrange(self.COLUMN_SIZE):
			itemCount = player.GetItemCountByVnum(self.COLUMN_ITEM_LIST[i])
			self.COLUMN_ITEM_COUNT[i].SetText("%d" % itemCount)

			if itemCount >= 50:
				self.COLUMN_ITEM[i] = True
			else:
				self.COLUMN_ITEM[i] = False

		for i in xrange(self.ROW_SIZE):
			itemCount = player.GetItemCountByVnum(self.ROW_ITEM_LIST[i])
			self.ROW_ITEM_COUNT[i].SetText("%d" % itemCount)

			if itemCount >= 50:
				self.ROW_ITEM[i] = True
			else:
				self.ROW_ITEM[i] = False

		self.enableYellow = True
		self.enableGreen = True

		for i in xrange(self.COLUMN_SIZE): #12
			for j in xrange(self.ROW_SIZE): #10
				if i%2 == j%2: # 6 == 5 #
					color = i%2 # 3
					index = i/2+(j/2)*6 # 19.5
					#chat.AppendChat(chat.CHAT_TYPE_INFO, "%d %d" % (color,index))
					if color == 0:
						if yellowmark & (1<<index):
							# self.CHECK_BUTTON[color][index].SetAlwaysToolTip(False)
							self.CHECK_BUTTON[color][index].Show()
							self.CHECK_BUTTON[color][index].Down()
							self.CHECK_BUTTON[color][index].Disable()
							#chat.AppendChat(chat.CHAT_TYPE_INFO, "%d %d" % (color,index))
							continue
						else:
							self.enableYellow = False
					else:
						if greenmark & (1<<index):
							# self.CHECK_BUTTON[color][index].SetAlwaysToolTip(False)
							self.CHECK_BUTTON[color][index].Show()
							self.CHECK_BUTTON[color][index].Down()
							self.CHECK_BUTTON[color][index].Disable()
							#chat.AppendChat(chat.CHAT_TYPE_INFO, "%d %d" % (color,index))
							continue
						else:
							self.enableGreen = False

					count = 0
					if self.COLUMN_ITEM[i]:
						count += 1

					if self.ROW_ITEM[j]:
						count += 1

					if count==2:
						# self.CHECK_BUTTON[color][index].SetAlwaysToolTip(True)
						self.CHECK_BUTTON[color][index].Show()
						self.CHECK_BUTTON[color][index].SetUp()
						self.CHECK_BUTTON[color][index].Enable()
					else:
						self.CHECK_BUTTON[color][index].Hide()

		if self.enableYellow:
			self.btnYellow.Show()
			self.btnYellow.SetUp()
			self.btnYellow.Enable()
			self.btnYellow.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_CAN_GET_YELLOW_BOX)
		else:
			#if yellowreward > goldreward:
			self.btnYellow.Show()
			self.btnYellow.Down()
			self.btnYellow.Disable()
			self.btnYellow.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_YELLOW_BOX_COMP_CNT % (yellowreward))
			#else:
			#	self.btnYellow.Disable()
			#	self.btnYellow.Hide()

		if self.enableGreen:
			self.btnGreen.Show()
			self.btnGreen.SetUp()
			self.btnGreen.Enable()
			self.btnGreen.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_CAN_GET_GREEN_BOX)
		else:
			#if greenreward > goldreward:
			self.btnGreen.Show()
			self.btnGreen.Down()
			self.btnGreen.Disable()
			self.btnGreen.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_GREEN_BOX_COMP_CNT % (greenreward))
			#else:
			#	self.btnGreen.Disable()
			#	self.btnGreen.Hide()

		if yellowreward >= 1 and yellowreward == greenreward:
			self.btnAll.SetUp()
			self.btnAll.Enable()
			self.btnAll.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_CAN_GET_ALL_BOX)
		else:
			self.btnAll.Down()
			self.btnAll.Disable()
			self.btnAll.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.CZ_REWARD_TOOLTIP_ALL_BOX)
		self.YellowRewardCount.SetText("%d" % yellowreward)
		self.GreenRewardCount.SetText("%d" % greenreward)
		self.Show()

	def Close(self):
		if self.buttontooltip:
			self.buttontooltip.Hide()
			self.ShowButtonToolTip = False

		self.OnCloseQuestionDialog()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Destroy(self):
		self.Hide()
		self.enableYellow = True
		self.enableGreen = True
		self.CoverImage1 = {}
		self.btnYellow = None
		self.btnGreen = None
		self.btnAll = None
		self.ClearDictionary()
