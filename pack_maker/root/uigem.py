#author: dracaryS

import ui, constInfo, uiCommon, localeInfo, app, net, item, player, chat, skill

IMG_DIR = "d:/ymir work/ui/gemshop/"

class GemShop(ui.ScriptWindow):

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.__data = {}

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Destroy()
		self.LoadWindow()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Open(self):
		self.Show()
		self.SetTop()
		loadStatus = self.__data["serverPacket"] if self.__data.has_key("serverPacket") else False
		if not loadStatus:
			self.__data["serverPacket"] = True
			net.SendChatPacket("/gem load")

	def Close(self):
		self.Hide()

	def LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/gemshopwindow.py")
		except:
			import exception
			exception.Abort("GemShop.LoadDialog.LoadObject")

		GetObject = self.GetChild

		GetObject("refresh_button").SetEvent(ui.__mem_func__(self.__ClickRefreshButton))
		GetObject("back_btn").SetEvent(ui.__mem_func__(self.__BackPage))
		GetObject("next_btn").SetEvent(ui.__mem_func__(self.__NextPage))
		GetObject("board").SetCloseEvent(ui.__mem_func__(self.Close))

		board = GetObject("bg_slots")

		itemSlot = ui.GridSlotWindow()
		itemSlot.SetParent(board)
		itemSlot.SetPosition(8, 28)
		itemSlot.ArrangeSlot(0, 3, 3, 32, 32, 13, 26)
		itemSlot.SAFE_SetButtonEvent("LEFT", "EXIST", self.__SelectItemSlot)
		itemSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
		itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		itemSlot.Show()
		self.ElementDictionary["itemSlot"] = itemSlot

		i = 0
		for j in xrange(3):
			for x in xrange(3):
				gayaIcon = ui.ImageBox()
				gayaIcon.SetParent(board)
				gayaIcon.SetPosition((8+(x*45))-2,(28+(j*58))+40)
				gayaIcon.LoadImage("d:/ymir work/ui/gemshop/gemshop_gemicon.sub")
				# gayaIcon.Show()
				self.ElementDictionary["icon_{}".format(i)] = gayaIcon

				gayaPrice = ui.TextLine()
				gayaPrice.SetParent(board)
				gayaPrice.SetPosition((8+(x*45))+14,(28+(j*58))+39)
				# gayaPrice.Show()
				self.ElementDictionary["price_{}".format(i)] = gayaPrice
				i+=1
		self.SetCenterPosition()
		self.Clear()

	def __BackPage(self):
		self.__GoToPage(self.__data["pageIndex"] - 1)

	def __NextPage(self):
		self.__GoToPage(self.__data["pageIndex"] + 1)

	def __GoToPage(self, pageIndex):
		if pageIndex < 0 or pageIndex > 2:
			return
		self.__data["pageIndex"] = pageIndex
		self.GetChild("page_text").SetText("{}/3".format(pageIndex+1))
		self.Refresh()

	def Clear(self):
		itemSlot = self.GetChild("itemSlot")

		for j in xrange(9):
			self.GetChild("price_{}".format(j)).SetText("0")
			itemSlot.ClearSlot(j)

		self.__data["items"] = {}
		self.__data["leftTime"] = app.GetGlobalTimeStamp() + 60
		self.__GoToPage(0)

	def Refresh(self):
		itemSlot = self.GetChild("itemSlot")
		startIndex = self.__data["pageIndex"] * 9
		for i in xrange(9):
			itemSlot.ClearSlot(i)

			itemData = self.__data["items"][i+startIndex] if self.__data["items"].has_key(i+startIndex) else None
			if itemData:
				if startIndex+i >= 9:
					slotCount = self.__data["slotCount"] if self.__data.has_key("slotCount") else 0
					if slotCount < ((i+startIndex)-9)+1:
						blockIcon = skill.GetIconImageNewEx(IMG_DIR+"block.tga")
						if 0 == blockIcon:
							continue
						itemSlot.SetSlot(i, itemData["itemVnum"], 32, 32, blockIcon)
						self.GetChild("icon_{}".format(i)).Hide()
						self.GetChild("price_{}".format(i)).Hide()
						continue
				itemSlot.SetItemSlot(i, itemData["itemVnum"], itemData["itemCount"])
				if itemData["itemBuyed"]:
					itemSlot.DisableSlot(i)
				self.GetChild("price_{}".format(i)).SetText(str(itemData["itemPrice"]))
				self.GetChild("icon_{}".format(i)).Show()
				self.GetChild("price_{}".format(i)).Show()
		itemSlot.RefreshSlot()

	def EmptyFunc(self):
		pass

	def __PopupNotifyMessage(self, msg, func = 0):
		if not func:
			func = self.EmptyFunc
		game = constInfo.GetGameInstance()
		if game:
			game.stream.popupWindow.Close()
			game.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def __SelectItemSlot(self, slotPos):
		startIndex = self.__data["pageIndex"] * 9
		itemData = self.__data["items"][slotPos+startIndex] if self.__data["items"].has_key(slotPos+startIndex) else None
		if itemData:
			if itemData["itemBuyed"]:
				self.__PopupNotifyMessage(localeInfo.GAYA_BOUGHT)
				return

			questionDialog = self.GetChild("questionDialog") if self.IsChild("questionDialog") else None
			if not questionDialog:
				questionDialog = uiCommon.QuestionDialog()
				questionDialog.SetCancelEvent(self.__CloseQuestionDialog)
				self.ElementDictionary["questionDialog"] = questionDialog

			slotCount = self.__data["slotCount"] if self.__data.has_key("slotCount") else 0
			if slotCount < (startIndex+slotPos-9)+1:
				questionDialog.SetText(localeInfo.GAYA_OPEN_SLOT)
				questionDialog.SetAcceptEvent(self.__OpenSlot)
			else:
				item.SelectItem(itemData["itemVnum"])
				questionDialog.SetText(localeInfo.GAYA_BUY.format(item.GetItemName(), itemData["itemPrice"]))
				questionDialog.SetAcceptEvent(self.__Buy)
				questionDialog.buyPos = startIndex+slotPos
			questionDialog.Open()

	def __OverOutItem(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.HideToolTip()

	def __OverInItem(self, slotIndex):
		startIndex = self.__data["pageIndex"] * 9
		itemData = self.__data["items"][slotIndex+startIndex] if self.__data["items"].has_key(slotIndex+startIndex) else None
		if not itemData:
			return

		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				slotCount = self.__data["slotCount"] if self.__data.has_key("slotCount") else 0
				if slotCount < ((slotIndex+startIndex)-9)+1:
					interface.tooltipItem.HideToolTip()
					return
				interface.tooltipItem.SetItemToolTip(itemData["itemVnum"])

	def __OpenSlot(self):
		net.SendChatPacket("/gem slot")
		self.__CloseQuestionDialog()

	def __Buy(self):
		questionDialog = self.GetChild("questionDialog") if self.IsChild("questionDialog") else None
		if questionDialog:
			questionDialog.Close()

			itemData = self.__data["items"][questionDialog.buyPos] if self.__data["items"].has_key(questionDialog.buyPos) else None
			if itemData:
				if itemData["itemPrice"] > player.GetGem():
					chat.AppendChat(1, localeInfo.GAYA_NO_GEM)
					return
				net.SendChatPacket("/gem buy {}".format(questionDialog.buyPos))

	def __CloseQuestionDialog(self):
		questionDialog = self.GetChild("questionDialog") if self.IsChild("questionDialog") else None
		if questionDialog:
			questionDialog.Close()

	def __ClickRefreshButton(self):
		questionDialog = self.GetChild("questionDialog") if self.IsChild("questionDialog") else None
		if not questionDialog:
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetCancelEvent(self.__CloseQuestionDialog)
			self.ElementDictionary["questionDialog"] = questionDialog

		questionDialog.SetText(localeInfo.GAYA_REFRESH)
		questionDialog.SetAcceptEvent(self.__RefreshItems)
		questionDialog.Open()

	def __RefreshItems(self):
		questionDialog = self.GetChild("questionDialog") if self.IsChild("questionDialog") else None
		if questionDialog:
			net.SendChatPacket("/gem refresh")
			questionDialog.Close()

	def SetRefreshLeftTime(self, leftTime):
		self.__data["leftTime"] = leftTime + app.GetGlobalTimeStamp()

	def __SetTimeText(self, time):
		timeText = self.GetChild("time_gaya")
		if time == -1:
			if timeText.GetText() != "0s":
				timeText.SetText("0s")
			return

		leftTime = time - app.GetGlobalTimeStamp()
		if leftTime <= 0:
			timeText.SetText("0s")
			self.__data["leftTime"] = -1
			net.SendChatPacket("/gem time")
			return

		m, s = divmod(leftTime, 60)
		h, m = divmod(m, 60)
		timeText.SetText("%02d:%02d:%02d"%(h,m,s))

	def OnUpdate(self):
		self.__SetTimeText(self.__data["leftTime"] if self.__data.has_key("leftTime") else -1)

	def SetBuyedSlot(self, slotPos, itemBuyed):
		itemData = self.__data["items"][slotPos] if self.__data["items"].has_key(slotPos) else None
		if itemData:
			itemData["itemBuyed"] = itemBuyed
		self.__GoToPage(self.__data["pageIndex"])

	def UpdateSlotCount(self, slotCount):
		self.__data["slotCount"] = slotCount
		self.__GoToPage(self.__data["pageIndex"])

	def SetItemData(self, slotPos, itemVnum, itemCount, itemPrice, itemBuyed):
		self.__data["items"][int(slotPos)] = {
			"itemVnum":  int(itemVnum),
			"itemCount": int(itemCount),
			"itemPrice": int(itemPrice),
			"itemBuyed": int(itemBuyed),
		}

	def SetItemsWithString(self, cmdString):
		itemsList = cmdString.split("|")
		for itemData in itemsList:
			itemSplit = itemData.split("#")
			if len(itemSplit) != 5:
				continue
			self.SetItemData(*itemSplit)
		self.__GoToPage(self.__data["pageIndex"])