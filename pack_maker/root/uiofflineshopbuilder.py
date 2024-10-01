import uiCommon,ui,localeInfo,constInfo,exception,mouseModule
import app, chr, player, net, chat, systemSetting, item, snd, shop, renderTarget
from _weakref import proxy

g_itemPriceDict = []
g_offlineShopAdvertisementBoardDict = {}
shop_all_Money = long(0)

SHOP_VISIT_COLOR = 0xFF00C8FF

def SetPrivateShopItemPrice(itemVNum, itemPrice, count):
	global g_itemPriceDict
	pcs_price = long(itemPrice)/count
	for_q = False
	for i in xrange(len(g_itemPriceDict)):
		if g_itemPriceDict[i]["vnum"] == itemVNum and pcs_price != g_itemPriceDict[i]["price"]:
			g_itemPriceDict[i].update({"vnum":int(itemVNum),"price":long(pcs_price)})
			for_q = True
			break
	if for_q == False:
		g_itemPriceDict.append({"vnum":int(itemVNum),"price":long(pcs_price)})

def GetPrivateShopItemPrice(itemVNum, count):
	global g_itemPriceDict
	for i in xrange(len(g_itemPriceDict)):
		item = g_itemPriceDict[i]
		if item["vnum"] == itemVNum:
			return long(item["price"]*count)
	return 0

def Clear():
	global g_itemPriceDict
	global shop_all_Money
	global g_offlineShopAdvertisementBoardDict
	g_itemPriceDict = []
	shop_all_Money = long(0)
	for key in g_offlineShopAdvertisementBoardDict.keys():
		g_offlineShopAdvertisementBoardDict[key].Hide()
		del g_offlineShopAdvertisementBoardDict[key]
	g_offlineShopAdvertisementBoardDict = {}

def UpdateADText(vid,type,text):
	if g_offlineShopAdvertisementBoardDict.has_key(vid):
		item = g_offlineShopAdvertisementBoardDict[vid]
		if item == None:
			del g_offlineShopAdvertisementBoardDict[vid]
			return
		oldtext = item.textLine.GetText()
		oldType = item.type
		if oldType != type:
			DeleteADBoardwithKey(vid)
			board = OfflineShopAdvertisementBoard(type)
			board.Open(vid, text)
		elif oldtext != text:
			item.textLine.SetText(text)
			item.SetSize(len(text) * 6 + 80 * 2)
			item.Show()

def UpdateADBoard():
	global g_offlineShopAdvertisementBoardDict
	for key in g_offlineShopAdvertisementBoardDict.keys():
		g_offlineShopAdvertisementBoardDict[key].Show()

def HideADBoard():
	global g_offlineShopAdvertisementBoardDict
	for key in g_offlineShopAdvertisementBoardDict.keys():
		g_offlineShopAdvertisementBoardDict[key].Hide()

def HideADBoardWithKey(vid):
	if g_offlineShopAdvertisementBoardDict.has_key(vid):
		g_offlineShopAdvertisementBoardDict[vid].Hide()

def ShowADBoardWithKey(vid):
	if g_offlineShopAdvertisementBoardDict.has_key(vid):
		g_offlineShopAdvertisementBoardDict[vid].Show()
		return True
	return False

def DeleteADBoard():
	global g_offlineShopAdvertisementBoardDict
	for key in g_offlineShopAdvertisementBoardDict.keys():
		g_offlineShopAdvertisementBoardDict[key].Hide()
		del g_offlineShopAdvertisementBoardDict[key]

def DeleteADBoardwithKey(vid):
	if g_offlineShopAdvertisementBoardDict.has_key(vid):
		g_offlineShopAdvertisementBoardDict[vid].Hide()
		g_offlineShopAdvertisementBoardDict[vid].Destroy()
		g_offlineShopAdvertisementBoardDict[vid]=0
		del g_offlineShopAdvertisementBoardDict[vid]

class OfflineShopAdvertisementBoard(ui.ThinBoardNorm):

	def __init__(self, type):
		ui.ThinBoardNorm.__init__(self, "UI_BOTTOM", type)
		self.shopAdvertismentBoardSeen = []
		self.vid = None
		self.title = None
		self.type = int(type)
		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetWindowHorizontalAlignCenter()
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		if (self.type==0):
			self.textLine.SetPosition(0,0)
		else:
			self.textLine.SetPosition(-10,5)
		self.textLine.Show()

	def __del__(self):
		ui.ThinBoardNorm.__del__(self)

	def SetBoard(self, a):
		ui.ThinBoardNorm.SetBoard(self, a)

	def Destroy(self):
		self.vid = 0
		self.title = 0
		self.type = 0
		self.textLine = 0
		self.Hide()

	def Open(self, vid, text):
		self.vid = vid
		self.title = text
		self.SetSize(len(text) * 6 + 80 * 2)
		self.textLine.SetText(text)
		self.textLine.Show()
		if vid in self.shopAdvertismentBoardSeen:
			self.textLine.SetPackedFontColor(SHOP_VISIT_COLOR)
		self.textLine.UpdateRect()
		DeleteADBoardwithKey(vid)
		g_offlineShopAdvertisementBoardDict[vid] = self
		self.Show()

	def OnMouseLeftButtonUp(self):
		if (not self.vid):
			return

		if chr.GetNameByVID(self.vid) == player.GetName():
			net.SendOfflineShopButton()
			# chat.AppendChat(chat.CHAT_TYPE_INFO, "SendOfflineShopButton")
		else:
			net.SendOnClickPacket(self.vid)
			# chat.AppendChat(chat.CHAT_TYPE_INFO, "SendOnClickPacket shop")

		if self.vid != player.GetMainCharacterIndex():
			self.textLine.SetPackedFontColor(SHOP_VISIT_COLOR)
			self.shopAdvertismentBoardSeen.append(self.vid)

		return True

	def OnUpdate(self):
		if (not self.vid):
			DeleteADBoardwithKey(self.vid)
			return

		if systemSetting.IsShowSalesText():
			self.SetPosition(-800, -300)
			return

		#LIMIT_RANGE = abs(constInfo.SHOPNAMES_RANGE * systemSetting.GetShopNamesRange())

		shopRange = [10000, 6000, 4000, 2000, 1000]
		try:
			LIMIT_RANGE = shopRange[systemSetting.GetShopNamesRange()]
		except:
			LIMIT_RANGE = shopRange[0]

		if chr.GetPixelPosition(self.vid) == None:
			DeleteADBoardwithKey(self.vid)
			return
		(to_x, to_y, to_z) = chr.GetPixelPosition(self.vid)
		(my_x, my_y, my_z) = player.GetMainCharacterPosition()
		if abs(my_x - to_x) <= LIMIT_RANGE and abs(my_y - to_y) <= LIMIT_RANGE:
			(x, y) = chr.GetProjectPosition(self.vid, 220)
			x_new = (x-self.GetWidth()/2)
			y_new = (y-self.GetHeight()/2)
			self.SetPosition(x_new, y_new)
			self.Show()
		else:
			self.SetPosition(-800, -300)
			#self.Hide()

class OfflineShopBuilder(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.itemStock = {}
		self.tooltipItem = None
		self.priceInputBoard = None
		self.title = ""
		self.thinboard=None
		self.playerChoose =None

		self.shopVnum = 0
		self.shopTitle = 0
		self.isLoaded = 0
		self.LoadWindow()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
			self.wndInventory = None
			self.lockedItems = {i:(-1,-1) for i in range(shop.OFFLINE_SHOP_SLOT_COUNT)}

			# -----------------------------------------------------------------------------------------
			# Inventário Especial
			self.wndInventoryNew = None
			self.lockedItemsNew = {i:(-1,-1) for i in range(shop.OFFLINE_SHOP_SLOT_COUNT)}
			# -----------------------------------------------------------------------------------------
			# -----------------------------------------------------------------------------------------

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = proxy(tooltipItem)

	def LoadWindow(self):
		if self.isLoaded:
			return
		self.isLoaded=1
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/Offlineshop/OfflineShopBuilder.py")

			self.GetChild("FirstButton").SetEvent(ui.__mem_func__(self.CheckPlayerAccept))
			self.GetChild("Board").SetCloseEvent(ui.__mem_func__(self.CloseReal))
			self.GetChild("ItemSlot").SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
			self.GetChild("ItemSlot").SAFE_SetButtonEvent("LEFT", "EXIST", self.OnSelectItemSlot)
			self.GetChild("ItemSlot").SAFE_SetButtonEvent("RIGHT", "EXIST", self.OnSelectItemSlot)
			self.GetChild("ItemSlot").SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
			self.GetChild("ItemSlot").SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
			self.GetChild("ItemSlot2").SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlotNew))
			self.GetChild("ItemSlot2").SAFE_SetButtonEvent("LEFT", "EXIST", self.OnSelectItemSlotNew)
			self.GetChild("ItemSlot2").SAFE_SetButtonEvent("RIGHT", "EXIST", self.OnSelectItemSlotNew)
			self.GetChild("ItemSlot2").SetOverInItemEvent(ui.__mem_func__(self.OnOverInItemNew))
			self.GetChild("ItemSlot2").SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
			self.GetChild("NameLine").OnPressEscapeKey = ui.__mem_func__(self.CloseReal)
			renderTarget.SetVisibility(1, True)
		except:
			exception.Abort("OfflineShopBuilderWindow.LoadWindow.LoadObject")

	def Destroy(self):
		self.ClearDictionary()
		if self.thinboard:
			self.thinboard.Destroy()

		self.thinboard=0
		self.itemStock.clear()
		self.itemStock=0
		self.tooltipItem = 0
		self.priceInputBoard = 0
		self.title = 0
		self.shopVnum = 0
		self.shopTitle = 0
		self.playerChoose =None
		self.isLoaded = 0

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.interface = None
			self.wndInventory = None
			self.lockedItems = {i:(-1,-1) for i in range(shop.OFFLINE_SHOP_SLOT_COUNT)}

			# -----------------------------------------------------------------------------------------
			# Inventário Especial
			self.wndInventoryNew = None
			self.lockedItemsNew = {i:(-1,-1) for i in range(shop.OFFLINE_SHOP_SLOT_COUNT)}
			# -----------------------------------------------------------------------------------------
			# -----------------------------------------------------------------------------------------

		self.Hide()

	def Open(self, title):
		self.title = title
		self.itemStock = {}

		shop.ClearOfflineShopStock()
		self.GetChild("NameLine").SetText(title)

		self.shopVnum = 0
		self.shopTitle = 0
		self.SetYang(0, True)
		self.Refresh()

		self.Show()
		self.SetCenterPosition()
		self.SetTop()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItems = {i:(-1,-1) for i in range(shop.OFFLINE_SHOP_SLOT_COUNT)}

			# -----------------------------------------------------------------------------------------
			# Inventário Especial
			self.lockedItemsNew = {i:(-1,-1) for i in range(shop.OFFLINE_SHOP_SLOT_COUNT)}
			# -----------------------------------------------------------------------------------------
			# -----------------------------------------------------------------------------------------

			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_PRIVATE_SHOP)
				self.interface.RefreshMarkInventoryBag()

	def CloseReal(self):
		self.Close()
		net.SendOfflineShopEndPacket()
		return True

	def Close(self):
		global shop_all_Money
		shop_all_Money = 0
		renderTarget.SetVisibility(1,False)
		shop.ClearOfflineShopStock()

		if self.priceInputBoard:
			self.priceInputBoard.Close()
			self.priceInputBoard = None

		if self.playerChoose:
			self.playerChoose.Close()
			self.playerChoose =None

		if app.WJ_ENABLE_TRADABLE_ICON:
			for privatePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
				if self.wndInventory:
					if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
						self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

			self.lockedItems = {i:(-1,-1) for i in range(shop.OFFLINE_SHOP_SLOT_COUNT)}

			# -----------------------------------------------------------------------------------------
			# Inventário Especial
			for privatePos, (itemInvenPage, itemSlotPos) in self.lockedItemsNew.items():
				if self.wndInventoryNew:
					if itemInvenPage == self.wndInventoryNew.GetInventoryPageIndex():
						self.wndInventoryNew.wndItem.SetCanMouseEventSlot(itemSlotPos)

			self.lockedItemsNew = {i:(-1,-1) for i in range(shop.OFFLINE_SHOP_SLOT_COUNT)}
			# -----------------------------------------------------------------------------------------
			# -----------------------------------------------------------------------------------------

			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
				self.interface.RefreshMarkInventoryBag()

		self.Hide()

	def Refresh(self):
		pointer = [self.GetChild("ItemSlot"),self.GetChild("ItemSlot2")]
		for ptr in pointer:
			for i in xrange(shop.OFFLINE_SHOP_SLOT_COUNT/2):
				ptr.SetCoverButton(i, "d:/ymir work/ui/game/quest/slot_button_01.sub","d:/ymir work/ui/game/quest/slot_button_01.sub","d:/ymir work/ui/game/quest/slot_button_01.sub", "d:/ymir work/ui/pattern/slot_disable.tga", False, False)

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
				if (not self.itemStock.has_key(real_index)):
					ptr.ClearSlot(i)
					continue
				pos = self.itemStock[real_index]
				itemCount = player.GetItemCount(*pos)
				if (itemCount <= 1):
					itemCount = 0
				ptr.SetItemSlot(i, player.GetItemIndex(*pos), itemCount)

				if app.WJ_CHANGELOOK_SYSTEM:
					itemTransmutation = player.GetItemTransmutation(*pos)
					if itemTransmutation > 0:
						ptr.ActivateTransmutationSlot(i)
					else:
						ptr.DeactivateTransmutationSlot(i)

				ptr.EnableCoverButton(i)

			ptr.RefreshSlot()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.RefreshLockedSlot()

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

			if app.WJ_ENABLE_TRADABLE_ICON:
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
					self.CantTradableItem(selectedSlotPos, attachedSlotPos)
				# -----------------------------------------------------------------------------------------
				# Inventário Especial
				else:
					self.CantTradableItemEspecial(selectedSlotPos, attachedSlotPos)
				# -----------------------------------------------------------------------------------------
				# -----------------------------------------------------------------------------------------

			priceInputBoard = uiCommon.MoneyInputDialog()
			priceInputBoard.SetTitle(localeInfo.OFFLINESHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
			priceInputBoard.Open()

			(itemPrice) = GetPrivateShopItemPrice(itemVNum,count)

			priceInputBoard.SetValue(itemPrice)

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

			if app.WJ_ENABLE_TRADABLE_ICON:
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
					self.CantTradableItem(selectedSlotPos, attachedSlotPos)
				# -----------------------------------------------------------------------------------------
				# Inventário Especial
				else:
					self.CantTradableItemEspecial(selectedSlotPos, attachedSlotPos)
				# -----------------------------------------------------------------------------------------
				# -----------------------------------------------------------------------------------------

			priceInputBoard = uiCommon.MoneyInputDialog()
			priceInputBoard.SetTitle(localeInfo.OFFLINESHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
			priceInputBoard.Open()

			(itemPrice) = GetPrivateShopItemPrice(itemVNum,count)

			priceInputBoard.SetValue(itemPrice)

			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos+40

	def OnSelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if (isAttached):
			snd.PlaySound("sound/ui/loginfail.wav")
			mouseModule.mouseController.DeattachObject()
		else:
			if (not selectedSlotPos in self.itemStock):
				return

			if app.IsCanOpenRender() and app.ENABLE_RENDER_TARGET:
				interface = constInfo.GetInterfaceInstance()
				if interface:
					interface.OpenRenderTargetWindow(0, player.GetItemIndex(*self.itemStock[selectedSlotPos]))
				return

			invenType, invenPos = self.itemStock[selectedSlotPos]
			self.SetYang(0, False, invenType, invenPos)
			shop.DelOfflineShopItemStock(invenType, invenPos)
			snd.PlaySound("sound/ui/drop.wav")

			if app.WJ_ENABLE_TRADABLE_ICON:
				if player.SLOT_TYPE_INVENTORY == invenType:
					(itemInvenPage, itemSlotPos) = self.lockedItems[selectedSlotPos]
					if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
						self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

					self.lockedItems[selectedSlotPos] = (-1, -1)
				# -----------------------------------------------------------------------------------------
				# Inventário Especial
				else:
					(itemInvenPage, itemSlotPos) = self.lockedItemsNew[selectedSlotPos]
					if itemInvenPage == self.wndInventoryNew.GetInventoryPageIndex():
						self.wndInventoryNew.wndItem.SetCanMouseEventSlot(itemSlotPos)

					self.lockedItemsNew[selectedSlotPos] = (-1, -1)
				# -----------------------------------------------------------------------------------------
				# -----------------------------------------------------------------------------------------

			del self.itemStock[selectedSlotPos]
			self.Refresh()

	def OnSelectItemSlotNew(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		if (isAttached):
			snd.PlaySound("sound/ui/loginfail.wav")
			mouseModule.mouseController.DeattachObject()
		else:
			if not constInfo.IS_SET(shop.GetShopFlag(),1<<selectedSlotPos):
				priceInputBoard = uiCommon.QuestionDialog()
				priceInputBoard.SetText(localeInfo.DO_YOU_WANT_OPEN_SLOT)
				priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptOpenSlot))
				priceInputBoard.pos = selectedSlotPos
				priceInputBoard.sourceWindowType = 0 # Teste
				priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
				priceInputBoard.Open()
				self.priceInputBoard = priceInputBoard
				return

			selectedSlotPos+=40
			if (not selectedSlotPos in self.itemStock):
				return
			if app.IsCanOpenRender() and app.ENABLE_RENDER_TARGET:
				interface = constInfo.GetInterfaceInstance()
				if interface:
					interface.OpenRenderTargetWindow(0, player.GetItemIndex(*self.itemStock[selectedSlotPos]))
				return
			invenType, invenPos = self.itemStock[selectedSlotPos]
			self.SetYang(0, False, invenType, invenPos)
			shop.DelOfflineShopItemStock(invenType, invenPos)
			snd.PlaySound("sound/ui/drop.wav")
			del self.itemStock[selectedSlotPos]
			self.Refresh()

	def AcceptOpenSlot(self):
		if constInfo.IS_SET(shop.GetShopFlag(),1<<self.priceInputBoard.pos):
			return

		net.SendOpenShopSlot(self.priceInputBoard.pos)
		self.priceInputBoard = None
		self.Refresh()

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
		itemVNum = player.GetItemIndex(attachedInvenType, sourceSlotPos)
		count = player.GetItemCount(attachedInvenType, sourceSlotPos)

		if itemVNum != self.priceInputBoard.itemVNum:
			self.priceInputBoard.Close()
			self.priceInputBoard=None
			return

		SetPrivateShopItemPrice(self.priceInputBoard.itemVNum, price, count)
		self.SetYang(price, True)

		for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():
			if (itemWindowType == attachedInvenType and itemSlotIndex == sourceSlotPos):
				self.SetYang(0, False, itemWindowType, itemSlotIndex)
				shop.DelOfflineShopItemStock(itemWindowType, itemSlotIndex)
				del self.itemStock[privatePos]

		shop.AddOfflineShopItemStock(attachedInvenType, sourceSlotPos, targetSlotPos, price)
		self.itemStock[targetSlotPos] = (attachedInvenType, sourceSlotPos)
		snd.PlaySound("sound/ui/drop.wav")

		if self.priceInputBoard:
			self.priceInputBoard.Close()
			self.priceInputBoard=None

		self.Refresh()
		return True

	def CancelInputPrice(self):
		if app.WJ_ENABLE_TRADABLE_ICON:
			if player.SLOT_TYPE_INVENTORY == self.priceInputBoard.sourceWindowType:
				itemInvenPage = self.priceInputBoard.sourceSlotPos / player.INVENTORY_PAGE_SIZE
				itemSlotPos = self.priceInputBoard.sourceSlotPos - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
				if self.wndInventory:
					if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
						self.wndInventory.wndItem.SetCanMouseEventSlot(itemSlotPos)

				self.lockedItems[self.priceInputBoard.targetSlotPos] = (-1, -1)
			# -----------------------------------------------------------------------------------------
			# Inventário Especial
			else:
				itemInvenPage = self.priceInputBoard.sourceSlotPos / player.SPECIAL_PAGE_SIZE
				itemSlotPos = self.priceInputBoard.sourceSlotPos - (itemInvenPage * player.SPECIAL_PAGE_SIZE)
				if self.wndInventoryNew:
					if self.wndInventoryNew.GetInventoryPageIndex() == itemInvenPage:
						self.wndInventoryNew.wndItem.SetCanMouseEventSlot(itemSlotPos)

				self.lockedItemsNew[self.priceInputBoard.targetSlotPos] = (-1, -1)
			# -----------------------------------------------------------------------------------------
			# -----------------------------------------------------------------------------------------

		if self.priceInputBoard:
			self.priceInputBoard.Close()
		self.priceInputBoard = None
		return 1

	def CancelPlayerChoose(self):
		if self.playerChoose:
			self.playerChoose.Close()
		self.playerChoose = None

	def CheckPlayerAccept(self):
		if self.playerChoose != None:
			self.CancelPlayerChoose()

		playerChoose = uiCommon.QuestionDialog()
		playerChoose.SetText(localeInfo.DO_YOU_WANT_CREATE_SHOP % localeInfo.DottedNumber(2000000))
		playerChoose.SetAcceptEvent(ui.__mem_func__(self.AcceptPlayerChoose))
		playerChoose.SetCancelEvent(ui.__mem_func__(self.CancelPlayerChoose))
		playerChoose.Open()
		self.playerChoose = playerChoose

	def AcceptPlayerChoose(self):
		self.OnOk()
		self.CancelPlayerChoose()

	def OnOk(self):
		self.title = self.GetChild("NameLine").GetText()
		if (not self.title):
			return
		if (len(self.itemStock) == 0):
			return
		elif net.IsChatInsultIn(self.title):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHAT_INSULT_STRING)
			return
		elif constInfo.getInjectCheck(self.title):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHAT_INSULT_STRING)
			return
		shop.BuildOfflineShop(self.title, 30000+self.shopVnum, self.shopTitle)
		self.Close()

	def OnPressEscapeKey(self):
		self.CloseReal()
		return True

	def OnPressExitKey(self):
		self.CloseReal()
		return True

	def OnOverInItem(self, slotIndex):
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		if None == interface.tooltipItem:
			return
		if self.itemStock.has_key(slotIndex):
			interface.tooltipItem.SetOfflineShopBuilderItem(*self.itemStock[slotIndex] + (slotIndex,))

	def OnOverInItemNew(self, slotIndex):
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		if None == interface.tooltipItem:
			return
		slotIndex+=40
		if self.itemStock.has_key(slotIndex):
			interface.tooltipItem.SetOfflineShopBuilderItem(*self.itemStock[slotIndex] + (slotIndex,))

	def OnOverOutItem(self):
		interface = constInfo.GetInterfaceInstance()
		if not interface:
			return
		if None == interface.tooltipItem:
			return
		interface.tooltipItem.HideToolTip()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItem(self, destSlotIndex, srcSlotIndex):
			itemInvenPage = srcSlotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = srcSlotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItems[destSlotIndex] = (itemInvenPage, localSlotPos)

			if self.wndInventory:
				if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
					self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		# -----------------------------------------------------------------------------------------
		# Inventário Especial
		def CantTradableItemEspecial(self, destSlotIndex, srcSlotIndex):
			itemInvenPage = srcSlotIndex / player.SPECIAL_PAGE_SIZE
			localSlotPos = srcSlotIndex - (itemInvenPage * player.SPECIAL_PAGE_SIZE)
			self.lockedItemsNew[destSlotIndex] = (itemInvenPage, localSlotPos)

			if self.wndInventoryNew:
				if self.wndInventoryNew.GetInventoryPageIndex() == itemInvenPage:
					self.wndInventoryNew.wndItem.SetCantMouseEventSlot(localSlotPos)
		# -----------------------------------------------------------------------------------------
		# -----------------------------------------------------------------------------------------

		def RefreshLockedSlot(self):
			if self.wndInventory:
				for privatePos, (itemInvenPage, itemSlotPos) in self.lockedItems.items():
					if self.wndInventory:
						if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
							self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventory.wndItem.RefreshSlot()

			# -----------------------------------------------------------------------------------------
			# Inventário Especial
			if self.wndInventoryNew:
				for privatePos, (itemInvenPage, itemSlotPos) in self.lockedItemsNew.items():
					if self.wndInventoryNew:
						if self.wndInventoryNew.GetInventoryPageIndex() == itemInvenPage:
							self.wndInventoryNew.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventoryNew.wndItem.RefreshSlot()
			# -----------------------------------------------------------------------------------------
			# -----------------------------------------------------------------------------------------

		def BindInterface(self, interface):
			self.interface = interface

		def OnTop(self):
			if self.interface:
				self.interface.SetOnTopWindow(player.ON_TOP_WND_PRIVATE_SHOP)
				self.interface.RefreshMarkInventoryBag()

		def SetInven(self, wndInventory):
			from _weakref import proxy
			self.wndInventory = proxy(wndInventory)

		# -----------------------------------------------------------------------------------------
		# Inventário Especial
		def SetInvenNew(self, wndInventoryNew):
			from _weakref import proxy
			self.wndInventoryNew = proxy(wndInventoryNew)
		# -----------------------------------------------------------------------------------------
		# -----------------------------------------------------------------------------------------

	def SetYang(self, value, flag, invenType = 0, invenPos = 0):
		global shop_all_Money
		long_value = long(value)
		if flag == True:
			shop_all_Money += long_value
			self.GetChild("Money").SetText("%s" % localeInfo.NumberToMoneyString(shop_all_Money))
		else:
			p = shop.GetOfflineShopItemPriceReal(invenType, invenPos)
			shop_all_Money -= long(p)
			self.GetChild("Money").SetText("%s" % localeInfo.NumberToMoneyString(shop_all_Money))