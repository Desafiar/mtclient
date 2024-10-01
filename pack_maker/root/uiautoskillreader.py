# author: dracaryS

import ui, constInfo

import net, player, chat, wndMgr

SKILL_MASTER = 0
SKILL_GRAND_MASTER = 1
SKILL_PERFECT_MASTER = 2
SKILL_L_MASTER = 3

USE_YMIR_50300_SKILLBOOK = True

class Window(ui.BoardWithTitleBar):
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.__LoadWindow()
	def Destroy(self):
		self.__children = {}
	def __LoadWindow(self):
		self.Destroy()

		self.AddFlag("movable")
		self.AddFlag("float")
		self.AddFlag("attach")
		self.SetTitleName("Auto Skill Reader")
		self.SetCloseEvent(self.Close)
		self.SetSize(260, 252)
		self.SetCenterPosition()

		board = CreateWindow(ui.ThinBoardCircle(), self, (11, 60), "", "", (240, 185))
		self.__children["board"] = board

		text1 = CreateWindow(ui.TextLine(), board, (240/2, 7), "Select the skill you want to upgrade and", "horizontal:center")
		self.__children["text1"] = text1

		text2 = CreateWindow(ui.TextLine(), board, (240/2, 24), "press the Start Button", "horizontal:center")
		self.__children["text2"] = text2

		__data = {
			0 : {
				"name": "Normal",
				"exorcism" : 71001,
				"concentrated" : 76034,
				"slots" : {
					1 : [17 + (36 * 0), 80],
					2 : [17 + (36 * 1), 80],
					3 : [17 + (36 * 2), 80],
					4 : [17 + (36 * 3), 80],
					5 : [17 + (36 * 4), 80],
					6 : [17 + (36 * 5), 80],
				},
			},
			1 : {
				"name": "Passive",
				"exorcism" : 71001,
				"concentrated" : 76034,
				"slots" : {
					122 : [17 + (36 * 0), 80],
					121 : [17 + (36 * 1), 80],
					124 : [17 + (36 * 2), 80],
					129 : [17 + (36 * 3), 80],
					0   : [17 + (36 * 4), 80],
					1   : [17 + (36 * 5), 80],
				},
			},
			2 : {
				"name": "Special",
				"exorcism" : 71001,
				"concentrated" : 76034,
				"slots" : {
					0 : [28 + (36 * 0), 80],
					1 : [28 + (36 * 1), 80],
					2 : [28 + (36 * 2), 80],
					3 : [28 + (36 * 3), 80],
					4 : [28 + (36 * 0), 116],
					5 : [28 + (36 * 1), 116],
					6 : [28 + (36 * 2), 116],
					7 : [28 + (36 * 3), 116],
					8 : [175, 100],
				},
			},
		}
		self.__children["data"] = __data

		i = 0
		for key, data in __data.items():
			categoryBtn = CreateWindow(ui.RadioButton(), self, (11 + (60 * i), 39))
			categoryBtn.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
			categoryBtn.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
			categoryBtn.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
			categoryBtn.SetText(data["name"])
			categoryBtn.SAFE_SetEvent(self.__SetPage, i)
			self.__children["categoryBtn"+str(key)] = categoryBtn

			slots = data["slots"]
			for slotIdx, slotData in slots.items():
				self.__children["slotImg"+str(key)+str(slotIdx)] = self.__CreateSlot(board, *slotData)

			slotWindow = CreateWindow(ui.SlotWindow(), board, (0, 0), "", "", (board.GetWidth(), board.GetHeight()))
			slotWindow.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
			slotWindow.SetUnselectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemSlot))
			slotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			slotWindow.SetOverInItemEvent(ui.__mem_func__(self.OverInSkill))
			slotWindow.SetOverOutItemEvent(ui.__mem_func__(self.OverOutSkill))

			for slotIdx, slotData in slots.items():
				slotWindow.AppendSlot(slotIdx, slotData[0], slotData[1], 32, 32)
			self.__children["slotWindow"+str(key)] = slotWindow
			i += 1

		for j in xrange(3):
			x = j * (32 + 4)
			self.__children["defaultslotImg"+str(j)] = self.__CreateSlot(board, 71+x, 40+0)

		defaultSlotWindow = CreateWindow(ui.SlotWindow(), board, (71, 40), "", "", (104, 32))
		for j in xrange(3):
			x = j * (32 + 4)
			defaultSlotWindow.AppendSlot(j, x, 0, 32, 32)
		defaultSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		defaultSlotWindow.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItem))
		defaultSlotWindow.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		defaultSlotWindow.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.__children["defaultSlotWindow"] = defaultSlotWindow

		startBtn = CreateWindow(ui.RadioButton(), board, (36, 161))
		startBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		startBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		startBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		startBtn.SetText("Start")
		startBtn.SAFE_SetEvent(self.__SetStatus, 1)
		self.__children["startBtn"] = startBtn

		stopBtn = CreateWindow(ui.RadioButton(), board, (126, 161))
		stopBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		stopBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		stopBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		stopBtn.SetText("Stop")
		stopBtn.SAFE_SetEvent(self.__SetStatus, 0)
		self.__children["stopBtn"] = stopBtn

		self.__children["botStatus"] = 0
		self.__children["selectedSkillIdx"] = -1

		self.__SetPage(0)

	def ServerSetStatus(self, status):
		self.__children["botStatus"] = True if int(status) else False
		self.Refresh()

	def __SetStatus(self, status):
		botStatus = self.__children["botStatus"] if self.__children.has_key("botStatus") else 0
		if botStatus == status:
			self.Refresh()
			return
		self.Refresh()
		selectedSkill = self.__children["selectedSkill"] if self.__children.has_key("selectedSkill") else 0
		if status:
			if selectedSkill == 0:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "First you need select a skill.")
				return
			elif self.__SkillToBook(selectedSkill) == 0:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "You can't upgrade this skill!")
				return
		net.SendChatPacket("/auto_skill_reader status {} {}".format(player.GetSkillIndex(selectedSkill) if selectedSkill >= 1 and selectedSkill <= 6 else selectedSkill, int(status)))

	def __SkillToMaxGrade(self, skillIdx):
		if skillIdx >= 1 and skillIdx <= 6:
			return SKILL_L_MASTER
		else:
			__skillToMaxGrade = {
				122 : SKILL_PERFECT_MASTER,
				124 : SKILL_PERFECT_MASTER,
				121 : SKILL_PERFECT_MASTER,
				129 : SKILL_PERFECT_MASTER,
			}
			if __skillBookItemList.has_key(skillIdx):
				return __skillBookItemList[skillIdx]
		return 0
	def __SkillToBook(self, skillIdx):
		if skillIdx >= 1 and skillIdx <= 6:
			grade = player.GetSkillGrade(skillIdx)
			if grade == 1:
				global USE_YMIR_50300_SKILLBOOK
				return [50300, player.GetSkillIndex(skillIdx)] if USE_YMIR_50300_SKILLBOOK else 50400 + player.GetSkillIndex(skillIdx)
			elif grade == 2:
				return 50513
		else:
			if 122 == skillIdx and player.GetSkillLevelNew(skillIdx) >= 2:#combo_checking_level
				return 0
		
			# if skill has 1 book put here
			__skillBookItemList = {
				122 : 50304,
				124 : 50600,
			}
			if __skillBookItemList.has_key(skillIdx):
				return __skillBookItemList[skillIdx]

			#if skill different book for every stage(M | G | P)
			__skillBookItemList = {
				121 : {
					SKILL_MASTER : 50301,
					SKILL_GRAND_MASTER : 50302,
					SKILL_PERFECT_MASTER : 50303,
				},
				129 : {
					SKILL_MASTER : 50314,
					SKILL_GRAND_MASTER : 50315,
					SKILL_PERFECT_MASTER : 50316,
				},
			}
			if __skillBookItemList.has_key(skillIdx):
				grade = player.GetSkillGradeNew(skillIdx)
				if __skillBookItemList[skillIdx].has_key(grade):
					return __skillBookItemList[skillIdx][grade]
		return 0
	def __OnSelectItem(self, selectedSlotPos):
		botStatus = self.__children["botStatus"] if self.__children.has_key("botStatus") else 0
		if botStatus:
			return
		self.__children["selectedSkill"] = 0
		self.Refresh()
		return True
	def __OnSelectItemSlot(self, selectedSlotPos):
		botStatus = self.__children["botStatus"] if self.__children.has_key("botStatus") else 0
		if botStatus:
			return
		selectedSkill = self.__children["selectedSkill"] if self.__children.has_key("selectedSkill") else 0
		self.__children["selectedSkill"] = 0 if selectedSkill == selectedSlotPos else selectedSlotPos
		self.Refresh()
		return True

	def Refresh(self):
		__data = self.__children["data"] if self.__children.has_key("data") else {}

		currentPage = self.__children["currentPage"]
		selectedSkill = self.__children["selectedSkill"] if self.__children.has_key("selectedSkill") else 0
		i = 0
		for key, data in __data.items():
			if currentPage == i:
				slots = data["slots"]
				for slotIdx, slotData in slots.items():
					self.__children["slotImg"+str(key)+str(slotIdx)].Show()

				self.__children["categoryBtn"+str(key)].Down()
				slotWindow = self.__children["slotWindow"+str(key)]

				for slotIdx, slotData in slots.items():
					skillGrade = player.GetSkillGrade(slotIdx) if currentPage == 0 else player.GetSkillGradeNew(slotIdx)
					skillLevel = player.GetSkillLevel(slotIdx) if currentPage == 0 else player.GetSkillLevelNew(slotIdx)
					if currentPage == 0:
						slotWindow.SetSkillSlotNew(slotIdx, player.GetSkillIndex(slotIdx), skillGrade, skillLevel)
					else:
						slotWindow.SetSkillSlot(slotIdx, slotIdx, skillLevel)
					slotWindow.SetSlotCountNew(slotIdx, skillGrade, skillLevel)
					
					if selectedSkill == slotIdx:
						slotWindow.ActivateSlot(slotIdx, 8.0 / 255.0, 159.0 / 255.0, 205.0 / 255.0)
					else:
						slotWindow.DeactivateSlot(slotIdx)

				slotWindow.RefreshSlot()
				slotWindow.Show()

				# default slot window!

				defaultSlotWindow = self.__children["defaultSlotWindow"]
				book = self.__SkillToBook(selectedSkill)
				if isinstance(book, list):
					book_count = player.GetItemCountByVnumNew(book[0], book[1])
					book = book[0]
				else:
					book_count = player.GetItemCountByVnum(book)
				defaultSlotWindow.SetItemSlot(0, book, book_count)
				if book_count:
					defaultSlotWindow.EnableSlot(0)
				else:
					defaultSlotWindow.DisableSlot(0)

				exorcism = data["exorcism"] if data.has_key("exorcism") else 0
				exorcism_count = player.GetItemCountByVnum(exorcism)

				defaultSlotWindow.SetItemSlot(1, exorcism, exorcism_count)
				if exorcism_count:
					defaultSlotWindow.EnableSlot(1)
				else:
					defaultSlotWindow.DisableSlot(1)

				concentrated = data["concentrated"] if data.has_key("concentrated") else 0
				concentrated_count = player.GetItemCountByVnum(concentrated)
				defaultSlotWindow.SetItemSlot(2, concentrated, concentrated_count)
				if concentrated_count:
					defaultSlotWindow.EnableSlot(2)
				else:
					defaultSlotWindow.DisableSlot(2)
				defaultSlotWindow.RefreshSlot()

			else:
				for slotIdx, slotData in data["slots"].items():
					self.__children["slotImg"+str(key)+str(slotIdx)].Hide()
				self.__children["categoryBtn"+str(key)].SetUp()
				self.__children["slotWindow"+str(key)].Hide()
			i+=1

		botStatus = self.__children["botStatus"]
		self.__children["startBtn" if not botStatus else "stopBtn"].SetUp()
		self.__children["startBtn" if botStatus else "stopBtn"].Down()


	def OverInItem(self, slotNumber):
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		elif not interface.tooltipItem:
			return
		currentPage = self.__children["currentPage"]
		__data = self.__children["data"] if self.__children.has_key("data") else {}
		i = 0
		for key, data in __data.items():
			if currentPage == i:
				if slotNumber == 1:
					itemIdx = data["exorcism"] if data.has_key("exorcism") else 0
				elif slotNumber == 2:
					itemIdx = data["concentrated"] if data.has_key("concentrated") else 0
				else:
					itemIdx = 0
					selectedSkill = self.__children["selectedSkill"] if self.__children.has_key("selectedSkill") else 0
					if selectedSkill:
						book = self.__SkillToBook(selectedSkill)
						if not isinstance(book, list):
							itemIdx = book
						else:
							tooltipItem = interface.tooltipItem
							tooltipItem.ClearToolTip()
							metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)]
							attrSlot = [(0, 0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
							metinSlot[0] = book[1]
							tooltipItem.AddItemData(book[0], metinSlot, attrSlot)
							return
				if itemIdx:
					interface.tooltipItem.SetItemToolTip(itemIdx)
				return
			i += 1
	def OverOutItem(self):
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		elif not interface.tooltipItem:
			return
		interface.tooltipItem.HideToolTip()
	def OverOutSkill(self):
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		elif not interface.tooltipSkill:
			return
		interface.tooltipSkill.HideToolTip()
	def OverInSkill(self, slotNumber):
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		elif not interface.tooltipSkill:
			return
		currentPage = self.__children["currentPage"]
		skillIndex = player.GetSkillIndex(slotNumber) if currentPage == 0 else slotNumber
		skillLevel = player.GetSkillLevel(slotNumber) if currentPage == 0 else player.GetSkillLevelNew(slotNumber)
		skillGrade = player.GetSkillGrade(slotNumber) if currentPage == 0 else player.GetSkillGradeNew(slotNumber)
		interface.tooltipSkill.SetSkillNew(slotNumber, skillIndex, skillGrade, skillLevel)
	def __SetPage(self, pageIdx):
		self.__children["currentPage"] = pageIdx
		self.Refresh()
	def __CreateSlot(self, parent, x, y):
		return CreateWindow(ui.ImageBox(), parent, (x, y), "d:/ymir work/ui/public/slot_base.sub")
	def Open(self):
		self.Refresh()
		self.Show()
	def Close(self):
		self.Hide()
		return True
	def OnPressEscapeKey(self):
		self.Close()
		return True

def CreateWindow(window, parent, windowPos, windowArgument = "", windowPositionRule = "", windowSize = (-1, -1), windowFontName = -1):
	window.SetParent(parent)
	window.SetPosition(*windowPos)
	if windowSize != (-1, -1):
		window.SetSize(*windowSize)
	if windowPositionRule:
		splitList = windowPositionRule.split(":")
		if len(splitList) == 2:
			(type, mode) = (splitList[0], splitList[1])
			if type == "horizontal":
				if isinstance(window, ui.TextLine):
					if mode == "center":
						window.SetHorizontalAlignCenter()
					elif mode == "right":
						window.SetHorizontalAlignRight()
					elif mode == "left":
						window.SetHorizontalAlignLeft()
				else:
					if mode == "center":
						window.SetWindowHorizontalAlignCenter()
					elif mode == "right":
						window.SetWindowHorizontalAlignRight()
					elif mode == "left":
						window.SetWindowHorizontalAlignLeft()
			elif type == "vertical":
				if isinstance(window, ui.TextLine):
					if mode == "center":
						window.SetVerticalAlignCenter()
					elif mode == "top":
						window.SetVerticalAlignTop()
					elif mode == "bottom":
						window.SetVerticalAlignBottom()
				else:
					if mode == "top":
						window.SetWindowVerticalAlignTop()
					elif mode == "center":
						window.SetWindowVerticalAlignCenter()
					elif mode == "bottom":
						window.SetWindowVerticalAlignBottom()
	if windowArgument:
		if isinstance(window, ui.TextLine):
			if windowFontName != -1:
				window.SetFontName(windowFontName)
			window.SetText(windowArgument)
		elif isinstance(window, ui.NumberLine):
			window.SetNumber(windowArgument)
		elif isinstance(window, ui.ExpandedImageBox) or isinstance(window, ui.ImageBox):
			window.LoadImage(windowArgument if windowArgument.find("gr2") == -1 else "icon/item/27995.tga")
	window.Show()
	return window
