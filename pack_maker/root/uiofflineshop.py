import app, chr, chrmgr, player, net, item, snd, shop, chat, background, renderTarget, nonplayer, skill
import wndMgr, uisystem, ui, uiCommon, uiToolTip, mouseModule, localeInfo, constInfo, exception
import uiOfflineShopBuilder
g_isEditingOfflineShop = False
from _weakref import proxy

def IsEditingOfflineShop():
	global g_isEditingOfflineShop
	if (g_isEditingOfflineShop):
		return True
	else:
		return False

class OfflineShopDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = 0
		self.xShopStart = 0
		self.yShopStart = 0
		self.thinboard = None
		self.questionDialog = None
		self.popup = None
		self.vid = 0
		self.shopTitle = 0
		self.shopVnum = 0
		self.itemBuyQuestionDialog = None
		

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/Offlineshop/OfflineShopDialog.py")

			self.GetChild("ItemSlot").SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			self.GetChild("ItemSlot").SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
			self.GetChild("ItemSlot").SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)
			self.GetChild("ItemSlot").SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.GetChild("ItemSlot").SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

			self.GetChild("ItemSlot2").SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			self.GetChild("ItemSlot2").SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlotNew)
			self.GetChild("ItemSlot2").SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlotNew)
			self.GetChild("ItemSlot2").SetOverInItemEvent(ui.__mem_func__(self.OverInItemNew))
			self.GetChild("ItemSlot2").SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

			self.GetChild("Board").SetCloseEvent(ui.__mem_func__(self.CloseReal))
			
			# renderTarget.SetBackground(1, "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")

		except:
			exception.Abort("OfflineShopDialog.LoadDialog.LoadObject")

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def Open(self, vid):
		self.Refresh()
		self.SetTop()
		self.Show()
		self.vid = vid
		(self.xShopStart, self.yShopStart, z) = player.GetMainCharacterPosition()

	def CloseReal(self):
		self.Close()
		net.SendOfflineShopEndPacket()

	def Close(self):
		# renderTarget.SetVisibility(1,False)
		if self.itemBuyQuestionDialog:
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		self.OnCloseQuestionDialog()
		self.Hide()

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = 0
		self.xShopStart = 0
		self.yShopStart = 0
		self.thinboard = None
		self.shopTitle = 0
		self.shopVnum = 0
		self.questionDialog = 0
		self.popup = 0
		self.vid = 0
		self.itemBuyQuestionDialog = 0
		self.Hide()

	def Refresh(self):
		pointer = [self.GetChild("ItemSlot"),self.GetChild("ItemSlot2")]

		for ptr in pointer:
			index = pointer.index(ptr)+1
			for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT/2):
				real_index = i
				if index == 2:
					real_index+=40
					if not constInfo.IS_SET(shop.GetShopFlag(),1<<i):
						ptr.SetItemSlot(i, 50300, 0)
						ptr.SetCoverButton(i, "d:/ymir work/ui/game/offlineshop/lock_0.tga", "d:/ymir work/ui/game/offlineshop/lock_1.tga", "d:/ymir work/ui/game/offlineshop/lock_0.tga", "d:/ymir work/ui/public/slot_cover_button_04.sub", 1, 0)
						#ptr.EnableSlot(i)
						continue

				itemCount = shop.GetOfflineShopItemCount(real_index)
				if (itemCount <= 1):
					itemCount = 0
				itemVnum = shop.GetOfflineShopItemID(real_index)

				if shop.GetOfflineShopItemStatus(real_index) == 1:
					item.SelectItem(itemVnum)
					(itemWidth, itemHeight) = item.GetItemSize()
					if itemHeight == 1:
						ptr.SetCoverButton(i, "d:/ymir work/ui/pattern/negative_frame1.tga", "d:/ymir work/ui/pattern/negative_frame1.tga", "d:/ymir work/ui/pattern/negative_frame1.tga", "d:/ymir work/ui/public/slot_cover_button_04.sub", 0, 0)
					elif itemHeight == 2:
						ptr.SetCoverButton(i, "d:/ymir work/ui/pattern/negative_frame2.tga", "d:/ymir work/ui/pattern/negative_frame2.tga", "d:/ymir work/ui/pattern/negative_frame2.tga", "d:/ymir work/ui/public/slot_cover_button_04.sub", 0, 0)
					elif itemHeight == 3:
						ptr.SetCoverButton(i, "d:/ymir work/ui/pattern/negative_frame3.tga", "d:/ymir work/ui/pattern/negative_frame3.tga", "d:/ymir work/ui/pattern/negative_frame3.tga", "d:/ymir work/ui/public/slot_cover_button_04.sub", 0, 0)
				else:
					ptr.SetCoverButton(i, "d:/ymir work/ui/game/quest/slot_button_01.sub","d:/ymir work/ui/game/quest/slot_button_01.sub","d:/ymir work/ui/game/quest/slot_button_01.sub", "d:/ymir work/ui/pattern/slot_disable.tga", True, False)
				#ptr.EnableSlot(i)
				
				ptr.SetItemSlot(i, itemVnum, itemCount)
				if app.WJ_CHANGELOOK_SYSTEM:
					itemTransmutedVnum = shop.GetOfflineShopItemTransmutation(real_index)
					if itemTransmutedVnum:
						ptr.ActivateTransmutationSlot(i)
					else:
						ptr.DeactivateTransmutationSlot(i)

				wndMgr.RefreshSlot(ptr.GetWindowHandle())

		if len(shop.GetSign())>0:
			sign = shop.GetSign()
			if sign[0].isdigit():
				self.GetChild("Board").SetTitleName(sign[1:])
				#if self.shopTitle != int(sign[0]):
				# self.shopTitle = int(sign[0])
				# self.ChangeThinboard(self.shopTitle)
			# else:
				# self.ChangeThinboard(0)
	
		# self.GetChild("see").SetText(localeInfo.OFFLINESHOP_SEEN%(shop.GetRealWatcherCount(),shop.GetDisplayedCount()))

		#if self.shopVnum != shop.GetShopType():
		self.shopVnum = shop.GetShopType()
		#renderTarget.ResetModel(1)
		# renderTarget.SelectModel(1, shop.GetShopType())
		# renderTarget.SetVisibility(1, True)

	def OnPressEscapeKey(self):
		self.CloseReal()
		return True

	def OnPressExitKey(self):
		self.CloseReal()
		return True
	
	# def ChangeThinboard(self, index):
		# if self.thinboard:
			# self.thinboard.Destroy()
			# del self.thinboard
			# self.thinboard =None
		# self.thinboard = ui.ThinBoardNorm()
		# self.thinboard.__init__("UI_BOTTOM",index)
		# self.thinboard.SetParent(self.GetChild("RenderTarget"))
		# t_position = [[34,23],[25,10],[25,10],[25,10],[25,10],[25,10]]
		# self.thinboard.SetPosition(t_position[index][0],t_position[index][1])
		# self.thinboard.SetSize(150)
		# self.thinboard.Show()

	def OnCloseQuestionDialog(self):
		if (not self.questionDialog):
			return
		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def UnselectItemSlot(self, selectedSlotPos):
		if (constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1):
			return
		# if app.IsCanOpenRender() and app.ENABLE_RENDER_TARGET:
			# interface = constInfo.GetInterfaceInstance()
			# if interface:
				# interface.OpenRenderTargetWindow(0, shop.GetOfflineShopItemID(selectedSlotPos))
			# return
		self.AskBuyItem(selectedSlotPos)

	def UnselectItemSlotNew(self, selectedSlotPos):
		if (constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1):
			return
		if not constInfo.IS_SET(shop.GetShopFlag(),1<<selectedSlotPos):
			return
		selectedSlotPos+=40

		# if app.IsCanOpenRender() and app.ENABLE_RENDER_TARGET:
			# interface = constInfo.GetInterfaceInstance()
			# if interface:
				# interface.OpenRenderTargetWindow(0, shop.GetOfflineShopItemID(selectedSlotPos))
			# return

		self.AskBuyItem(selectedSlotPos)

	def SelectItemSlot(self, selectedSlotPos):
		if (constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1):
			return
		if shop.GetOfflineShopItemStatus(selectedSlotPos) == 1:
			return
		isAttached = mouseModule.mouseController.isAttached()
		if (not isAttached):
			curCursorNum = app.GetCursor()
			if (app.BUY == curCursorNum):
				net.SendOfflineShopBuyPacket(self.vid, selectedSlotPos)
			# elif app.IsCanOpenRender() and app.ENABLE_RENDER_TARGET:
				# interface = constInfo.GetInterfaceInstance()
				# if interface:
					# interface.OpenRenderTargetWindow(0, shop.GetOfflineShopItemID(selectedSlotPos))
				# return
			else:
				selectedItemID = shop.GetOfflineShopItemID(selectedSlotPos)
				itemCount = shop.GetOfflineShopItemCount(selectedSlotPos)
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				mouseModule.mouseController.AttachObject(self, attachedSlotType, selectedSlotPos, selectedItemID, itemCount)
				mouseModule.mouseController.SetCallBack("INVENTORY", ui.__mem_func__(self.DropToInventory))
				snd.PlaySound("sound/ui/pick.wav")

	def SelectItemSlotNew(self, selectedSlotPos):
		if (constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1):
			return
		if not constInfo.IS_SET(shop.GetShopFlag(),1<<selectedSlotPos):
			return
		selectedSlotPos+=40
		# if app.IsCanOpenRender() and app.ENABLE_RENDER_TARGET:
			# interface = constInfo.GetInterfaceInstance()
			# if interface:
				# interface.OpenRenderTargetWindow(0, shop.GetOfflineShopItemID(selectedSlotPos))
			# return
		
		if shop.GetOfflineShopItemStatus(selectedSlotPos) == 1:
			return
		isAttached = mouseModule.mouseController.isAttached()
		if (not isAttached):
			curCursorNum = app.GetCursor()
			if (app.BUY == curCursorNum):
				net.SendOfflineShopBuyPacket(self.vid, selectedSlotPos)
			else:
				selectedItemID = shop.GetOfflineShopItemID(selectedSlotPos)
				itemCount = shop.GetOfflineShopItemCount(selectedSlotPos)
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				mouseModule.mouseController.AttachObject(self, attachedSlotType, selectedSlotPos, selectedItemID, itemCount)
				mouseModule.mouseController.SetCallBack("INVENTORY", ui.__mem_func__(self.DropToInventory))
				snd.PlaySound("sound/ui/pick.wav")

	def DropToInventory(self):
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		self.AskBuyItem(attachedSlotPos)

	def AskBuyItem(self, slotPos):
		if shop.GetOfflineShopItemStatus(slotPos) == 1:
			return
		itemIndex = shop.GetOfflineShopItemID(slotPos)
		itemCount = shop.GetOfflineShopItemCount(slotPos)
		itemPrice = shop.GetOfflineShopItemPrice(slotPos)

		item.SelectItem(itemIndex)

		itemBuyQuestionDialog = uiCommon.QuestionDialog2()

		if itemIndex == 70104:
			text = localeInfo.DO_YOU_BUY_ITEM(nonplayer.GetMonsterName(shop.GetOfflineShopItemMetinSocket(slotPos,0))+ " "+item.GetItemName(),itemCount,itemPrice)
		elif itemIndex == 50300:
			text = localeInfo.DO_YOU_BUY_ITEM(skill.GetSkillName(shop.GetOfflineShopItemMetinSocket(slotPos,0))+ " "+item.GetItemName(),itemCount,itemPrice)
		else:
			text = localeInfo.DO_YOU_BUY_ITEM(item.GetItemName(),itemCount,itemPrice)

		itemBuyQuestionDialog.SetText1(text)
		itemBuyQuestionDialog.SetText2(localeInfo.OFFLINESHOP_BUY_DIALOG)
		itemBuyQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerBuyItem(arg))
		itemBuyQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerBuyItem(arg))
		#itemBuyQuestionDialog.SetWidth(len(text)*5)
		itemBuyQuestionDialog.Open()
		itemBuyQuestionDialog.pos = slotPos
		self.itemBuyQuestionDialog = itemBuyQuestionDialog
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def AnswerBuyItem(self, flag):
		pos = self.itemBuyQuestionDialog.pos
		if (flag):
			shopid = shop.GetOfflineShopID(pos)
			net.SendOfflineShopBuyPacket(shopid, pos)
		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def OverInItem(self, slotIndex):
		if (mouseModule.mouseController.isAttached()):
			return
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		if None == interface.tooltipItem:
			return
		interface.tooltipItem.SetOfflineShopItem(slotIndex)

	def OverInItemNew(self, slotIndex):
		if (mouseModule.mouseController.isAttached()):
			return
		slotIndex+=40
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		if None == interface.tooltipItem:
			return
		interface.tooltipItem.SetOfflineShopItem(slotIndex)

	def OverOutItem(self):
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		if None == interface.tooltipItem:
			return
		interface.tooltipItem.HideToolTip()

	def OnUpdate(self):
		USE_SHOP_LIMIT_RANGE = 1500
		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xShopStart) > USE_SHOP_LIMIT_RANGE or abs(y - self.yShopStart) > USE_SHOP_LIMIT_RANGE:
			self.CloseReal()

class OfflineMyShop(ui.ScriptWindow):
	# class LogsItem(ui.ImageBox):
		# def Destroy(self):
			# self.log_text=None
		# def __del__(self):
			# ui.ImageBox.__del__(self)
		# def __init__(self, parent, name, date, itemvnum, itemcount, price):
			# ui.ImageBox.__init__(self)
			# self.SetParent(parent)
			# item.SelectItem(itemvnum)
			# self.LoadImage("d:/ymir work/ui/game/offlineshop/logs_table.tga")

			# self.log_text = ui.TextLine()
			# self.log_text.SetParent(self)
			# self.log_text.SetPosition(10, 5)
			# self.log_text.SetFontName("Tahoma:11")
			# if int(itemcount) == 1:
				# self.log_text.SetText(localeInfo.OFFLINESHOP_LOG_TEXT%(str(date),item.GetItemName(),constInfo.NumberToString(long(price)),str(name)))
			# else:
				# self.log_text.SetText(localeInfo.OFFLINESHOP_LOG_TEXT_COUNT%(str(date),int(itemcount),item.GetItemName(),constInfo.NumberToString(long(price)),str(name)))
			# self.log_text.Show()

			# self.Show()

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = None
		self.priceInputBoard = None
		self.interface = None
		# self.shopLogs = False
		self.logIndex = 0
		self.thinboard = 0
		self.title = ""
		self.time = 0
		self.money_time = 0
		self.shopTitle = 0
		self.shopVnum = 0
		self.lastUpdateTime=0
		self.offlineDecoration = None
		self.title_time = 0
		

		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		#import dbg
		#dbg.TraceError("Hi from OfflineMyShop")

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/Offlineshop/offlineshoppanel.py")

			self.GetChild("ItemSlot").SAFE_SetButtonEvent("LEFT", "EXIST", self.UnselectItemSlot)
			self.GetChild("ItemSlot").SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)
			self.GetChild("ItemSlot").SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.GetChild("ItemSlot").SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.GetChild("ItemSlot").SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))

			self.GetChild("ItemSlot2").SAFE_SetButtonEvent("LEFT", "EXIST", self.UnselectItemSlotNew)
			self.GetChild("ItemSlot2").SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlotNew)
			self.GetChild("ItemSlot2").SetOverInItemEvent(ui.__mem_func__(self.OverInItemNew))
			self.GetChild("ItemSlot2").SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.GetChild("ItemSlot2").SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlotNew))
			self.GetChild("Board").SetCloseEvent(ui.__mem_func__(self.CloseReal))
			self.GetChild("FirstButton").SetEvent(ui.__mem_func__(self.CloseShop))
			self.GetChild("refresh_title").SetEvent(ui.__mem_func__(self.RefreshTitle))
			self.GetChild("time_btn").SetEvent(ui.__mem_func__(self.AddTime))
			self.GetChild("refresh_yang").SetEvent(ui.__mem_func__(self.MoneyCheck))
			self.GetChild("LogsWindow").Hide()
			self.GetChild("ListBox").SetScrollBar(self.GetChild("ScrollBar"))
			self.GetChild("ListBox").SetViewItemCount(14)
			self.GetChild("ListBox").SetItemStep(22)
			self.GetChild("ListBox").SetItemSize(400,38)
			self.GetChild("ListBox").RemoveAllItems()
			self.GetChild("NameLine").OnPressEscapeKey = ui.__mem_func__(self.CloseReal)
			self.closeQuestionDialog = uiCommon.QuestionDialog()
			self.closeQuestionDialog.Hide()
		except:
			exception.Abort("OfflineShopChangePriceWindow.LoadWindow.LoadObject")

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def AddTime(self):
		priceInputBoard = uiCommon.QuestionDialog()
		text = localeInfo.OFFLINESHOP_ADD_TIME_DIALOG%localeInfo.NumberToMoneyString(20000000)
		priceInputBoard.SetText(text)
		priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptAddTime))
		priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelRemoveItem))
		#priceInputBoard.SetWidth(len(text)*5)
		priceInputBoard.Open()
		self.priceInputBoard = priceInputBoard

	def AcceptAddTime(self):
		net.SendAddTime()
		self.CancelRemoveItem()

	def MoneyCheck(self):
		if shop.GetCurrentOfflineShopMoney() > 0:
			net.SendTakeOfflineMoney()

	def RefreshTitle(self):
		newsign = self.GetChild("NameLine").GetText()
		if newsign.isdigit() or newsign == "" or newsign == " ":
			return
		sign = shop.GetSign()[1:]
		if newsign != sign:
			net.SendOfflineShopChangeTitle(newsign)

	def CloseShop(self):
		self.closeQuestionDialog.SetText(localeInfo.OFFLINESHOP_CLOSE_DIALOG)
		self.closeQuestionDialog.SetAcceptEvent(lambda arg = True: self.AnswerCloseOfflineShop(arg))
		self.closeQuestionDialog.SetCancelEvent(lambda arg = False: self.AnswerCloseOfflineShop(arg))
		self.closeQuestionDialog.Open()

	def AnswerCloseOfflineShop(self, flag):
		self.closeQuestionDialog.Hide()
		if flag:
			net.SendDestroyOfflineShop()

	def Destroy(self):
		self.GetChild("ListBox").RemoveAllItems()

		self.ClearDictionary()
		self.itemSlot = None
		self.itemSlot2 = None
		self.btnOk = None
		self.lastUpdateTime=0
		self.priceInputBoard = None

	def Open(self):
		global g_isEditingOfflineShop
		g_isEditingOfflineShop = True
		self.Show()
		self.Refresh()

	def CloseReal(self):
		self.Close()
		net.SendOfflineShopEndPacket()
		return True

	def Close(self):
		global g_isEditingOfflineShop
		g_isEditingOfflineShop = False
		self.Hide()

	def OnSelectEmptySlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if (isAttached):
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			slot_type_list = [player.SLOT_TYPE_INVENTORY,player.SLOT_TYPE_UPGRADE_INVENTORY,player.SLOT_TYPE_BOOK_INVENTORY,player.SLOT_TYPE_STONE_INVENTORY,player.SLOT_TYPE_CHANGE_INVENTORY,player.SLOT_TYPE_DRAGON_SOUL_INVENTORY,player.SLOT_TYPE_COSTUME_INVENTORY]
			if not attachedSlotType in slot_type_list:
				return

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			count = player.GetItemCount(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)
			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANNOT_SELL_ITEM)
				return
			priceInputBoard = uiCommon.MoneyInputDialog()
			priceInputBoard.SetTitle(localeInfo.OFFLINESHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelRemoveItem))
			priceInputBoard.Open()

			priceInputBoard.SetValue(0)

			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos

	def OnSelectEmptySlotNew(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if not constInfo.IS_SET(shop.GetShopFlag(),1<<selectedSlotPos):
			return
		if (isAttached):
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			slot_type_list = [player.SLOT_TYPE_INVENTORY,player.SLOT_TYPE_UPGRADE_INVENTORY,player.SLOT_TYPE_BOOK_INVENTORY,player.SLOT_TYPE_STONE_INVENTORY,player.SLOT_TYPE_CHANGE_INVENTORY,player.SLOT_TYPE_DRAGON_SOUL_INVENTORY,player.SLOT_TYPE_COSTUME_INVENTORY]
			if not attachedSlotType in slot_type_list:
				return

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			count = player.GetItemCount(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)
			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OFFLINESHOP_CANNOT_SELL_ITEM)
				return
			priceInputBoard = uiCommon.MoneyInputDialog()
			priceInputBoard.SetTitle(localeInfo.OFFLINESHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelRemoveItem))
			priceInputBoard.Open()

			priceInputBoard.SetValue(0)

			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos+40

	def AcceptInputPrice(self):
		if (not self.priceInputBoard):
			return True
		price = long(self.priceInputBoard.GetText())
		if not price:
			return True
		if long(price) <= 0:
			return True
		attachedInvenType = self.priceInputBoard.sourceWindowType
		sourceSlotPos = self.priceInputBoard.sourceSlotPos
		targetSlotPos = self.priceInputBoard.targetSlotPos
		itemVnum = player.GetItemIndex(attachedInvenType, sourceSlotPos)
		count = player.GetItemCount(attachedInvenType, sourceSlotPos)
		if itemVnum !=self.priceInputBoard.itemVNum:
			self.priceInputBoard.Close()
			self.priceInputBoard = None
			return
		net.SendAddOfflineShopItem(sourceSlotPos,targetSlotPos,price,attachedInvenType)
		#self.itemStock[targetSlotPos] = (attachedInvenType, sourceSlotPos)
		snd.PlaySound("sound/ui/drop.wav")
		self.priceInputBoard = None
		return True

	def Refresh(self):
		if not self.IsShow():
			return
		pointer = [self.GetChild("ItemSlot"),self.GetChild("ItemSlot2")]
		for ptr in pointer:
			for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT/2):
				ptr.ClearSlot(i)
				wndMgr.RefreshSlot(ptr.GetWindowHandle())
		for ptr in pointer:
			index = pointer.index(ptr)+1
			for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT/2):
				real_index = i
				if index == 2:
					real_index+=40
					if not constInfo.IS_SET(shop.GetShopFlag(),1<<i):
						ptr.SetItemSlot(i, 50300, 0)
						ptr.SetCoverButton(i, "d:/ymir work/ui/game/offlineshop/lock_0.tga", "d:/ymir work/ui/game/offlineshop/lock_1.tga", "d:/ymir work/ui/game/offlineshop/lock_0.tga", "d:/ymir work/ui/public/slot_cover_button_04.sub", 1, 0)
						ptr.EnableSlot(i)
						continue
				itemCount = shop.GetOfflineShopItemCount(real_index)
				if (itemCount <= 1):
					itemCount = 0
				itemVnum = shop.GetOfflineShopItemID(real_index)
				ptr.SetItemSlot(i, itemVnum, itemCount)
				if app.WJ_CHANGELOOK_SYSTEM:
					itemTransmutedVnum = shop.GetOfflineShopItemTransmutation(real_index)
					if itemTransmutedVnum:
						ptr.ActivateTransmutationSlot(i)
					else:
						ptr.DeactivateTransmutationSlot(i)

				if shop.GetOfflineShopItemStatus(real_index) == 1:
					item.SelectItem(itemVnum)
					(itemWidth, itemHeight) = item.GetItemSize()
					if itemHeight == 1:
						ptr.SetCoverButton(i, "d:/ymir work/ui/pattern/negative_frame1.tga", "d:/ymir work/ui/pattern/negative_frame1.tga", "d:/ymir work/ui/pattern/negative_frame1.tga", "d:/ymir work/ui/public/slot_cover_button_04.sub", 1, 0)
						ptr.EnableSlot(i)
					elif itemHeight == 2:
						ptr.SetCoverButton(i, "d:/ymir work/ui/pattern/negative_frame2.tga", "d:/ymir work/ui/pattern/negative_frame2.tga", "d:/ymir work/ui/pattern/negative_frame2.tga", "d:/ymir work/ui/public/slot_cover_button_04.sub", 1, 0)
						ptr.EnableSlot(i)
					elif itemHeight == 3:
						ptr.SetCoverButton(i, "d:/ymir work/ui/pattern/negative_frame3.tga", "d:/ymir work/ui/pattern/negative_frame3.tga", "d:/ymir work/ui/pattern/negative_frame3.tga", "d:/ymir work/ui/public/slot_cover_button_04.sub", 1, 0)
						ptr.EnableSlot(i)
				else:
					ptr.SetCoverButton(i, "d:/ymir work/ui/game/quest/slot_button_01.sub","d:/ymir work/ui/game/quest/slot_button_01.sub","d:/ymir work/ui/game/quest/slot_button_01.sub", "d:/ymir work/ui/pattern/slot_disable.tga", False, False)
					ptr.EnableSlot(i)

			wndMgr.RefreshSlot(ptr.GetWindowHandle())

		if len(shop.GetSign())>0:
			sign = shop.GetSign()
			title = int(sign[0])
			if sign[0].isdigit():
				self.GetChild("NameLine").SetText("")
				self.GetChild("NameLine").SetInfoMessage(sign[1:])
				self.shopTitle=title
			else:
				self.GetChild("NameLine").SetText("")
				self.GetChild("NameLine").SetInfoMessage(sign)
				self.shopTitle=0
		self.shopVnum = shop.GetShopType()-30000
		self.GetChild("Money").SetText(localeInfo.NumberToMoneyString(shop.GetCurrentOfflineShopMoney()))
		self.GetChild("time").SetText(localeInfo.SecondOfflineToDHM(shop.GetShopTime()-app.GetGlobalTimeStamp()))
		
	def SetItemData(self, pos, itemID, itemCount, itemPrice):
		shop.SetOfflineShopItemData(pos, itemID, itemCount, itemPrice)

	def OnPressEscapeKey(self):
		self.CloseReal()
		return True

	def OnPressExitKey(self):
		self.CloseReal()
		return True

	def UnselectItemSlot(self, selectedSlotPos):
		if (constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1):
			return
		itemIndex = shop.GetOfflineShopItemID(selectedSlotPos)
		item.SelectItem(itemIndex)
		priceInputBoard = uiCommon.QuestionDialog()
		if itemIndex == 70104:
			text = localeInfo.DO_YOU_WANT_GET_BACK_ITEM%(nonplayer.GetMonsterName(shop.GetOfflineShopItemMetinSocket(selectedSlotPos,0))+ " "+item.GetItemName())
		elif itemIndex == 50300:
			text = localeInfo.DO_YOU_WANT_GET_BACK_ITEM%(skill.GetSkillName(shop.GetOfflineShopItemMetinSocket(selectedSlotPos,0))+ " "+item.GetItemName())
		else:
			text = localeInfo.DO_YOU_WANT_GET_BACK_ITEM%item.GetItemName()

		priceInputBoard.SetText(text)
		priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptRemoveItem))
		priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelRemoveItem))
		#priceInputBoard.SetWidth(len(text)*5)
		priceInputBoard.Open()
		self.priceInputBoard = priceInputBoard
		self.priceInputBoard.pos = selectedSlotPos

	def UnselectItemSlotNew(self, selectedSlotPos):
		if (constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1):
			return

		priceInputBoard = uiCommon.QuestionDialog()
		if not constInfo.IS_SET(shop.GetShopFlag(),1<<selectedSlotPos):
			priceInputBoard.SetText(localeInfo.DO_YOU_WANT_OPEN_SLOT)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptOpenSlot))
			priceInputBoard.pos = selectedSlotPos
		else:
			selectedSlotPos+=40
			itemIndex = shop.GetOfflineShopItemID(selectedSlotPos)
			item.SelectItem(itemIndex)
			if itemIndex == 70104:
				text = localeInfo.DO_YOU_WANT_GET_BACK_ITEM%(nonplayer.GetMonsterName(shop.GetOfflineShopItemMetinSocket(selectedSlotPos,0))+ " "+item.GetItemName())
			elif itemIndex == 50300:
				text = localeInfo.DO_YOU_WANT_GET_BACK_ITEM%(skill.GetSkillName(shop.GetOfflineShopItemMetinSocket(selectedSlotPos,0))+ " "+item.GetItemName())
			else:
				text = localeInfo.DO_YOU_WANT_GET_BACK_ITEM%item.GetItemName()
			priceInputBoard.SetText(text)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptRemoveItem))
			#priceInputBoard.SetWidth(len(text)*5)
			priceInputBoard.pos = selectedSlotPos
		
		priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelRemoveItem))
		priceInputBoard.Open()
		self.priceInputBoard = priceInputBoard

	def AcceptOpenSlot(self):
		if constInfo.IS_SET(shop.GetShopFlag(),1<<self.priceInputBoard.pos):
			return
		net.SendOpenShopSlot(self.priceInputBoard.pos)
		self.priceInputBoard = None
		self.Refresh()
		return True

	def AcceptRemoveItem(self):
		net.SendRemoveOfflineShopItem(self.priceInputBoard.pos)
		self.priceInputBoard = None
		return True

	def CancelRemoveItem(self):
		self.priceInputBoard = None
		return True

	def OverInItem(self, slotIndex):
		#if (mouseModule.mouseController.isAttached()):
		#	return
		if self.priceInputBoard != None:
			return
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		if None == interface.tooltipItem:
			return
		interface.tooltipItem.SetOfflineShopItem(slotIndex)

	def OverInItemNew(self, slotIndex):
		if self.priceInputBoard != None:
			return
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		if None == interface.tooltipItem:
			return
		interface.tooltipItem.SetOfflineShopItem(slotIndex+40)

	def OverOutItem(self):
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		if None == interface.tooltipItem:
			return
		interface.tooltipItem.HideToolTip()

	def OnUpdate(self):
		if app.GetGlobalTime() - self.lastUpdateTime > 500:
			self.lastUpdateTime = app.GetGlobalTime()
			self.GetChild("time").SetText(localeInfo.SecondOfflineToDHM(shop.GetShopTime()-app.GetGlobalTimeStamp()))
