import app
import net
import player
import item
import ui
import uiToolTip
import mouseModule
import localeInfo
import uiCommon
import constInfo
import snd
import wndMgr
import chat

class RefineRarityDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = FALSE

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.wndInventory = None

	def __Initialize(self):
		self.dlgQuestion = None
		self.children = []
		self.materialList = []
		self.materialText = []
		self.materialCount = []
		self.vnum = 0
		self.targetItemPos = 0
		self.dialogHeight = 0
		self.percentage = 0
		self.percentage_extra = 0
		self.cost = 0
		self.type = 0
		self.special_storage = 0

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1,-1)

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refineraritydialog.py")
		except:
			import exception
			exception.Abort("RefineRarityDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.background = self.GetChild("Background")
			self.probText = self.GetChild("SuccessPercentage")
			self.probIncreaseText = self.GetChild("SuccessPercentageIncreased")
			self.costText = self.GetChild("Cost")

			self.DesignIncrease = self.GetChild("DesignIncrease")
			self.DesignCost = self.GetChild("DesignCost")
			self.SlotCost = self.GetChild("SlotCost")

			self.button_accept = self.GetChild("AcceptButton")
			self.button_cancel = self.GetChild("CancelButton")

			self.button_accept.SetEvent(self.OpenQuestionDialog)
			self.button_cancel.SetEvent(self.CancelRefine)
		except:
			import exception
			exception.Abort("RefineRarityDialog.__LoadScript.BindObject")

		self.toolTipNext = uiToolTip.ItemToolTip()
		self.toolTipNext.HideToolTip()

		self.toolTipCur = uiToolTip.ItemToolTip()
		self.toolTipCur.HideToolTip()

		self.tooltipMode = uiToolTip.ItemToolTip()
		self.tooltipMode.HideToolTip()

		self.toolTipMaterial = uiToolTip.ItemToolTip()
		self.toolTipMaterial.HideToolTip()

		self.slotCurrent, self.slotAfter = {}, {}
		posY = 61
		for i in xrange(3):
			self.slotCurrent[i] = ui.MakeImageBox(self, "d:/ymir work/ui/public/Slot_Base.sub", 22 * 2, posY)
			self.slotAfter[i] = ui.MakeImageBox(self, "d:/ymir work/ui/public/Slot_Base.sub", 102 * 2 - 20, posY)
			posY += 32

		self.itemImageCur = ui.MakeImageBox(self, "d:/ymir work/ui/public/Slot_Base.sub", 46, 60)
		self.itemImageNext = ui.MakeImageBox(self, "d:/ymir work/ui/public/Slot_Base.sub", 102 * 2 - 20, 60)

		self.materialList = []
		self.materialText = []
		self.materialCount = []

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.CancelRefine))
		self.isLoaded = TRUE

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __MakeItemSlot(self, c):
		itemslot = ui.SlotWindow()
		itemslot.SetParent(self)
		itemslot.SetSize(32, 32)
		itemslot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		itemslot.AppendSlot(c, 0, 0, 32, 32)
		itemslot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		itemslot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		itemslot.RefreshSlot()
		itemslot.Show()
		self.children.append(itemslot)
		return itemslot

	def __MakeThinBoard(self):
		thinBoard = ui.ThinBoard()
		thinBoard.SetParent(self)
		thinBoard.Show()
		self.children.append(thinBoard)
		return thinBoard

	def Destroy(self):
		self.ClearDictionary()
		self.dlgQuestion = None
		self.board = 0
		self.background = 0
		self.probText = 0
		self.probIncreaseText = 0
		self.costText = 0
		self.titleBar = 0
		self.toolTipNext = 0
		self.toolTipCur = 0
		self.special_storage = 0
		self.itemImageCur = 0
		self.itemImageNext = 0
		self.children = []
		self.materialList = []
		self.materialText = []
		self.materialCount = []
		self.toolTipMaterial = 0
		self.slotCurrent = None
		self.slotAfter = None

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.wndInventory = None
			self.lockedItem = (-1,-1)

	def Open(self, targetItemPos, nextGradeItemVnum, cost, prob, prob_extra, special_storage, type):
		if FALSE == self.isLoaded:
			self.__LoadScript()

		self.__Initialize()

		self.targetItemPos = targetItemPos
		self.vnum = nextGradeItemVnum
		self.cost = cost
		self.percentage = prob
		self.percentage_extra = prob_extra
		self.type = type
		self.special_storage = int(special_storage)

		self.probText.SetText(localeInfo.REFINE_CURRENT_PERCENTAGE % (self.percentage))
		self.probIncreaseText.SetText(localeInfo.REFINE_INCREASE_PERCENTAGE % (self.percentage_extra))
		self.costText.SetText("%s" % (localeInfo.NumberToMoneyString(self.cost)))

		self.toolTipNext.ClearToolTip()
		self.toolTipCur.ClearToolTip()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.SetCantMouseEventSlot(self.targetItemPos)

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(targetItemPos, i))

		apply_random_list = []
		if app.ENABLE_GLOVE_SYSTEM:
			for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(player.GetItemApplyRandom(targetItemPos, i))

		self.toolTipCur.SetInventoryItem(targetItemPos)
		self.toolTipNext.AddRefineRarityItemData(nextGradeItemVnum, metinSlot, attrSlot, apply_random_list)

		curItemIndex = player.GetItemIndex(targetItemPos)

		if curItemIndex != 0:
			item.SelectItem(curItemIndex)

			try:
				self.itemImageCur.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("Refine.CurrentItem.LoadImage - Failed to find item data")

		item.SelectItem(nextGradeItemVnum)
		self.itemImageNext.LoadImage(item.GetIconImageFileName())

		self.dialogHeight = 200
		self.UpdateDialog()

		self.SetCenterPosition()
		self.Show()

	def Close(self):
		self.dlgQuestion = None
		self.Hide()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1, -1)
			self.SetCanMouseEventSlot(self.targetItemPos)

	def AppendMaterial(self, vnum, count):
		grid = self.__MakeItemSlot(len(self.materialList))
		grid.SetPosition(15, self.dialogHeight)
		grid.SetItemSlot(len(self.materialList), vnum, 0)

		self.materialList.append(vnum)

		thinBoard = self.__MakeThinBoard()
		thinBoard.SetPosition(54, self.dialogHeight)
		thinBoard.SetSize(191, 20)

		textLine = ui.TextLine()
		textLine.SetParent(thinBoard)
		textLine.SetFontName(localeInfo.UI_DEF_FONT)

		item.SelectItem(vnum)

		if player.GetItemCountByTT(vnum) < count and player.GetItemCountByVnum(vnum) < count:
			textLine.SetPackedFontColor(0xffFF0033)

		elif player.GetItemCountByVnum(vnum) >= count and player.GetItemCountByTT(vnum) < count:
			textLine.SetPackedFontColor(0xffdddddd)

		elif player.GetItemCountByTT(vnum) >= count and player.GetItemCountByVnum(vnum) < count:
			textLine.SetPackedFontColor(0xffdddddd)
		else:
			textLine.SetPackedFontColor(0xffFF0033)

		if player.GetItemCountByVnum(vnum) > 0 and player.GetItemCountByTT(vnum) <= 0:
			textLine.SetText("%s x%d  |cFFffce00(%d)" % (item.GetItemName(), count, player.GetItemCountByVnum(vnum)))
		else:
			textLine.SetText("%s x%d  |cFFffce00(%d)" % (item.GetItemName(), count, player.GetItemCountByTT(vnum)))

		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.SetWindowVerticalAlignCenter()
		textLine.SetVerticalAlignCenter()
		textLine.SetPosition(15, 0)
		textLine.Show()

		self.children.append(textLine)
		self.materialText.append(textLine)
		self.materialCount.append(count)

		self.dialogHeight += 36
		self.UpdateDialog()

	def UpdateDialog(self):
		countLen = 0
		count = 3
		newcount = 0

		for i in xrange(len(self.materialList)):
			count += i
			countLen += 1

		if countLen == 4:
			newcount = (25 * count) - 40
		else:
			newcount = 25 * count

		self.SetSize(263, 280 + newcount + 30)
		self.board.SetSize(263, 280 + newcount + 30)
		self.background.SetSize(263 - 14, 280 + newcount + 30 - 40)

		self.DesignIncrease.SetPosition(14, 141 + newcount + 30)
		self.DesignCost.SetPosition(14, 171 + newcount + 30)
		self.SlotCost.SetPosition(74, 202 + newcount + 30)

		self.button_accept.SetPosition(30, 241 + newcount + 30)
		self.button_cancel.SetPosition(150, 241 + newcount + 30)

		self.titleBar.SetWidth(263 - 15)

		self.SetCenterPosition()

	def OpenQuestionDialog(self):
		totalPerc = self.percentage + self.percentage_extra

		if 100 == totalPerc:
			self.Accept()
			return

		if 10 == self.type:
			self.Accept()
			return

		dlgQuestion = uiCommon.QuestionDialog2()
		dlgQuestion.SetText2(localeInfo.REFINE_RARITY_WARNING)
		dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.Accept))
		dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))

		if self.type == 0:
			# dlgQuestion.SetText1(localeInfo.REFINE_RARITY_WARNING_WITH_BONUS_PERCENT_2)
			dlgQuestion.SetText1(localeInfo.REFINE_RARITY_WARNING_WITH_BONUS_PERCENT_1)
			dlgQuestion.SetText2(localeInfo.REFINE_RARITY_DOWN_GRADE_WARNING)
		else:
			dlgQuestion.SetText1(localeInfo.REFINE_RARITY_WARNING_WITH_BONUS_PERCENT_1)
			dlgQuestion.SetText2(localeInfo.REFINE_RARITY_NOT_GRADE_WARNING)

		dlgQuestion.Open()
		self.dlgQuestion = dlgQuestion

	def Accept(self):
		net.SendRefineRarityPacket(self.targetItemPos, self.type, self.special_storage)
		self.Close()

	def OnUpdate(self):
		for i in xrange(len(self.materialList)):
			count_item = self.materialCount[i]
			vnum_item = self.materialList[i]
			item.SelectItem(vnum_item)

			if player.GetItemCountByTT(vnum_item) < count_item and player.GetItemCountByVnum(vnum_item) < count_item:
				self.materialText[i].SetPackedFontColor(0xffFF0033)

			elif player.GetItemCountByVnum(vnum_item) >= count_item and player.GetItemCountByTT(vnum_item) < count_item:
				self.materialText[i].SetPackedFontColor(0xffdddddd)

			elif player.GetItemCountByTT(vnum_item) >= count_item and player.GetItemCountByVnum(vnum_item) < count_item:
				self.materialText[i].SetPackedFontColor(0xffdddddd)
			else:
				self.materialText[i].SetPackedFontColor(0xffFF0033)

			if player.GetItemCountByVnum(vnum_item) > 0 and player.GetItemCountByTT(vnum_item) <= 0:
				self.materialText[i].SetText("%s x%d  |cFFffce00(%d)" % (item.GetItemName(), count_item, player.GetItemCountByVnum(vnum_item)))
			else:
				self.materialText[i].SetText("%s x%d  |cFFffce00(%d)" % (item.GetItemName(), count_item, player.GetItemCountByTT(vnum_item)))

		if self.itemImageCur:
			if self.itemImageCur.IsIn():
				self.toolTipCur.ShowToolTip()
			else:
				self.toolTipCur.HideToolTip()

		if self.itemImageNext:
			if self.itemImageNext.IsIn():
				self.toolTipNext.ShowToolTip()
			else:
				self.toolTipNext.HideToolTip()

	def CancelRefine(self):
		net.SendRefineRarityPacket(255, 255, 255)
		self.Close()

	def OverInItem(self, slot):
		if self.toolTipMaterial:
			self.toolTipMaterial.SetItemToolTip(self.materialList[slot])

	def OverOutItem(self):
		if self.toolTipMaterial:
			self.toolTipMaterial.HideToolTip()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetCanMouseEventSlot(self, slotIndex):
			try:
				itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
				localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
				self.lockedItem = (-1, -1)

				if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
					self.wndInventory.wndItem.SetCanMouseEventSlot(localSlotPos)
			except Exception as e:
				pass

		def SetCantMouseEventSlot(self, slotIndex):
			itemInvenPage = slotIndex / player.INVENTORY_PAGE_SIZE
			localSlotPos = slotIndex - (itemInvenPage * player.INVENTORY_PAGE_SIZE)
			self.lockedItem = (itemInvenPage, localSlotPos)

			if itemInvenPage == self.wndInventory.GetInventoryPageIndex():
				self.wndInventory.wndItem.SetCantMouseEventSlot(localSlotPos)

		def SetInven(self, wndInventory):
			from _weakref import proxy
			self.wndInventory = proxy(wndInventory)

		def RefreshLockedSlot(self):
			if self.wndInventory:
				itemInvenPage, itemSlotPos = self.lockedItem
				if self.wndInventory.GetInventoryPageIndex() == itemInvenPage:
					self.wndInventory.wndItem.SetCantMouseEventSlot(itemSlotPos)

				self.wndInventory.wndItem.RefreshSlot()

	def OnPressEscapeKey(self):
		self.CancelRefine()
		return TRUE