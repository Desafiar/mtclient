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
import uiScriptLocale
import chr

class RefineDialog(ui.ScriptWindow):

	makeSocketSuccessPercentage = ( 100, 33, 20, 15, 10, 5, 0 )
	upgradeStoneSuccessPercentage = ( 30, 29, 28, 27, 26, 25, 24, 23, 22 )
	upgradeArmorSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )
	upgradeAccessorySuccessPercentage = ( 99, 88, 77, 66, 33, 33, 33, 33, 33 )
	upgradeSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadScript()

		self.scrollItemPos = 0
		self.targetItemPos = 0

	def __LoadScript(self):

		self.__LoadQuestionDialog()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refinedialog.py")

		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.successPercentage = self.GetChild("SuccessPercentage")
			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.Close)
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.BindObject")

		## 936 : 개량 확률 표시 안함
		##if 936 == app.GetDefaultCodePage():
		self.successPercentage.Show()

		toolTip = uiToolTip.ItemToolTip()
		toolTip.SetParent(self)
		toolTip.SetPosition(15, 38)
		toolTip.SetFollow(FALSE)
		toolTip.Show()
		self.toolTip = toolTip

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadQuestionDialog(self):
		self.dlgQuestion = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgQuestion, "uiscript/questiondialog2.py")
		except:
			import exception
			exception.Abort("RefineDialog.__LoadQuestionDialog.LoadScript")

		try:
			GetObject=self.dlgQuestion.GetChild
			GetObject("message1").SetText(localeInfo.REFINE_DESTROY_WARNING)
			GetObject("message2").SetText(localeInfo.REFINE_WARNING2)
			GetObject("accept").SetEvent(ui.__mem_func__(self.Accept))
			GetObject("cancel").SetEvent(ui.__mem_func__(self.dlgQuestion.Hide))
		except:
			import exception
			exception.Abort("SelectCharacterWindow.__LoadQuestionDialog.BindObject")

	def Destroy(self):
		self.ClearDictionary()
		self.board = 0
		self.successPercentage = 0
		self.titleBar = 0
		self.toolTip = 0
		self.dlgQuestion = 0

	def GetRefineSuccessPercentage(self, scrollSlotIndex, itemSlotIndex):

		if -1 != scrollSlotIndex:
			if player.IsRefineGradeScroll(scrollSlotIndex):
				curGrade = player.GetItemGrade(itemSlotIndex)
				itemIndex = player.GetItemIndex(itemSlotIndex)

				item.SelectItem(itemIndex)
				itemType = item.GetItemType()
				itemSubType = item.GetItemSubType()

				if item.ITEM_TYPE_METIN == itemType:

					if curGrade >= len(self.upgradeStoneSuccessPercentage):
						return 0
					return self.upgradeStoneSuccessPercentage[curGrade]

				elif item.ITEM_TYPE_ARMOR == itemType:

					if item.ARMOR_BODY == itemSubType:
						if curGrade >= len(self.upgradeArmorSuccessPercentage):
							return 0
						return self.upgradeArmorSuccessPercentage[curGrade]
					else:
						if curGrade >= len(self.upgradeAccessorySuccessPercentage):
							return 0
						return self.upgradeAccessorySuccessPercentage[curGrade]

				else:

					if curGrade >= len(self.upgradeSuccessPercentage):
						return 0
					return self.upgradeSuccessPercentage[curGrade]

		for i in xrange(player.METIN_SOCKET_MAX_NUM+1):
			if 0 == player.GetItemMetinSocket(itemSlotIndex, i):
				break

		return self.makeSocketSuccessPercentage[i]

	def Open(self, scrollItemPos, targetItemPos):
		self.scrollItemPos = scrollItemPos
		self.targetItemPos = targetItemPos

		percentage = self.GetRefineSuccessPercentage(scrollItemPos, targetItemPos)
		if 0 == percentage:
			return
		self.successPercentage.SetText(localeInfo.REFINE_SUCCESS_PROBALITY % (percentage))

		itemIndex = player.GetItemIndex(targetItemPos)
		self.toolTip.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))
		self.toolTip.AddItemData(itemIndex, metinSlot)

		self.UpdateDialog()
		self.SetTop()
		self.Show()

	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 30
		newHeight = self.toolTip.GetHeight() + 98
		self.board.SetSize(newWidth, newHeight)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):
		percentage = self.GetRefineSuccessPercentage(-1, self.targetItemPos)
		if 100 == percentage:
			self.Accept()
			return

		self.dlgQuestion.SetTop()
		self.dlgQuestion.Show()

	def Accept(self):
		net.SendItemUseToItemPacket(self.scrollItemPos, self.targetItemPos)
		self.Close()

	def Close(self):
		self.dlgQuestion.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

class RefineDialogNew(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = FALSE

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.wndInventory = None

	def __Initialize(self):
		self.dlgQuestion = None
		self.children = []
		self.vnum = 0
		self.targetItemPos = 0
		self.dialogHeight = 0
		self.cost = 0
		self.percentage = 0
		self.type = 0
		self.special_storage = 0
		self.apply_random_list = None
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1,-1)

		if app.ENABLE_MULTI_REFINE_WORLDARD:
			self.multi_refine_info = []
			self.multi_refine_material = []
			self.total_count_material = 5
			self.material_elements = {}
			self.pages_view = 1
			self.pages_actual = 1
			self.index_select = -1

		self.tooltipItem = uiToolTip.ItemToolTip()

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refinedialog.py")

		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.probText = self.GetChild("SuccessPercentage")
			self.costText = self.GetChild("Cost")
			self.successPercentage = self.GetChild("SuccessPercentage")
			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.CancelRefine)
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.BindObject")

		#self.successPercentage.Hide()

		toolTip = uiToolTip.ItemToolTip()
		toolTip.SetParent(self)
		toolTip.SetFollow(FALSE)
		toolTip.SetPosition(15, 38)
		toolTip.Show()
		self.toolTip = toolTip

		self.slotList = []
		for i in xrange(3):
			slot = self.__MakeSlot()
			slot.SetParent(toolTip)
			slot.SetWindowVerticalAlignCenter()
			self.slotList.append(slot)

		itemImage = self.__MakeItemImage()
		itemImage.SetParent(toolTip)
		itemImage.SetWindowVerticalAlignCenter()
		itemImage.SetPosition(-35, 0)
		self.itemImage = itemImage

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.CancelRefine))

		if app.ENABLE_REFINE_RENEWAL:
			self.checkBox = ui.CheckBox()
			self.checkBox.SetParent(self)
			self.checkBox.SetPosition(-3, 83+8)
			self.checkBox.SetWindowHorizontalAlignCenter()
			self.checkBox.SetWindowVerticalAlignBottom()
			self.checkBox.SetEvent(ui.__mem_func__(self.AutoRefine), "ON_CHECK", True)
			self.checkBox.SetEvent(ui.__mem_func__(self.AutoRefine), "ON_UNCKECK", False)
			self.checkBox.SetCheckStatus(constInfo.IS_AUTO_REFINE)
			self.checkBox.SetTextInfo(uiScriptLocale.UPGRADE)
			self.checkBox.Show()

		self.isLoaded = TRUE

		if app.ENABLE_MULTI_REFINE_WORLDARD:
			self.elements_multi_refine = {}

			self.elements_multi_refine["config_elements"] = [
			["first_prev",-40-11,75,"MOSTBOUGHT_RIGHT_LAST"],
			["prev",-20-11,75,"MOSTBOUGHT_RIGHT"],
			["last_next",60-11,75,"MOSTBOUGHT_LEFT_LAST"],
			["next",40-11,75,"MOSTBOUGHT_LEFT"]
			]

			for i in self.elements_multi_refine["config_elements"]:
				name = i[0]
				po_x = i[1]
				po_y = i[2]
				event = i[3]

				self.elements_multi_refine["buttons_{}".format(name)] = ui.Button()
				self.elements_multi_refine["buttons_{}".format(name)].SetParent(self)
				self.elements_multi_refine["buttons_{}".format(name)].SetUpVisual("d:/ymir work/ui/buttons_multi/private_{}_btn_01.sub".format(name))
				self.elements_multi_refine["buttons_{}".format(name)].SetOverVisual("d:/ymir work/ui/buttons_multi/private_{}_btn_02.sub".format(name))
				self.elements_multi_refine["buttons_{}".format(name)].SetDownVisual("d:/ymir work/ui/buttons_multi/private_{}_btn_03.sub".format(name))
				self.elements_multi_refine["buttons_{}".format(name)].SetWindowHorizontalAlignCenter()
				self.elements_multi_refine["buttons_{}".format(name)].SetWindowVerticalAlignBottom()
				self.elements_multi_refine["buttons_{}".format(name)].SetPosition(po_x,po_y+40)
				self.elements_multi_refine["buttons_{}".format(name)].SetEvent(self.__OnClickPage, event)
				self.elements_multi_refine["buttons_{}".format(name)].Show()

			self.elements_multi_refine["slot_pages"] = ui.ImageBox()
			self.elements_multi_refine["slot_pages"].SetParent(self)
			self.elements_multi_refine["slot_pages"].SetPosition(10-11,77+40)
			self.elements_multi_refine["slot_pages"].SetWindowHorizontalAlignCenter()
			self.elements_multi_refine["slot_pages"].SetWindowVerticalAlignBottom()
			self.elements_multi_refine["slot_pages"].LoadImage("d:/ymir work/ui/buttons_multi/private_pagenumber_00.sub")
			self.elements_multi_refine["slot_pages"].Show()

			self.elements_multi_refine["total_pages"] = ui.TextLine()
			self.elements_multi_refine["total_pages"].SetParent(self.elements_multi_refine["slot_pages"])
			self.elements_multi_refine["total_pages"].SetPosition(0,-1)
			self.elements_multi_refine["total_pages"].SetText("0/0")
			self.elements_multi_refine["total_pages"].SetHorizontalAlignCenter()
			self.elements_multi_refine["total_pages"].SetVerticalAlignCenter()
			self.elements_multi_refine["total_pages"].SetWindowHorizontalAlignCenter()
			self.elements_multi_refine["total_pages"].SetWindowVerticalAlignCenter()
			self.elements_multi_refine["total_pages"].Show()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __MakeSlot(self):
		slot = ui.ImageBox()
		slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
		slot.Show()
		self.children.append(slot)
		return slot

	def __MakeItemImage(self):
		itemImage = ui.ImageBox()
		itemImage.Show()
		self.children.append(itemImage)
		return itemImage

	def __MakeThinBoard(self):
		thinBoard = ui.ThinBoard()
		thinBoard.SetParent(self)
		thinBoard.Show()
		if not app.ENABLE_MULTI_REFINE_WORLDARD:
			self.children.append(thinBoard)
		return thinBoard

	if app.ENABLE_MULTI_REFINE_WORLDARD:
		def __MakeItemSlot(self,c):
			itemslot = ui.SlotWindow()
			itemslot.SetParent(self)
			itemslot.SetSize(32, 32)
			itemslot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
			itemslot.AppendSlot(c, 0, 0, 32, 32)
			itemslot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			itemslot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			itemslot.RefreshSlot()
			itemslot.Show()
			return itemslot

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
			self.tooltipItem.ClearToolTip()

	def OverInItem(self, slotIndex):
		(index, vnum, count) = self.multi_refine_material[slotIndex]
		if self.tooltipItem:
			self.tooltipItem.AddItemData(vnum, 0, 0)

	def Destroy(self):
		self.ClearDictionary()
		self.dlgQuestion = None
		self.board = 0
		self.probText = 0
		self.costText = 0
		self.titleBar = 0
		self.toolTip = 0
		self.successPercentage = None
		self.special_storage = 0
		self.slotList = []
		self.children = []
		self.tooltipItem = None
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.wndInventory = None
			self.lockedItem = (-1,-1)

	if app.ENABLE_REFINE_RENEWAL:
		def __InitializeOpen(self):
			self.children = []
			self.vnum = 0
			self.targetItemPos = 0
			self.dialogHeight = 0
			self.cost = 0
			self.percentage = 0
			self.type = 0
			self.xRefineStart = 0
			self.yRefineStart = 0

			if app.ENABLE_MULTI_REFINE_WORLDARD:
				self.multi_refine_info = []
				self.multi_refine_material = []
				self.total_count_material = 5
				self.material_elements = {}
				self.pages_view = 1
				self.pages_actual = 1
				self.index_select = -1

	if app.ENABLE_MULTI_REFINE_WORLDARD:
		def func_clear_info(self):
			self.multi_refine_info = []
			self.multi_refine_material = []

			self.pages_view = 1
			self.pages_actual = 1

			for ia in xrange(0,self.total_count_material):
				self.material_elements["grid_{}".format(ia)] = self.__MakeItemSlot(ia)
				self.material_elements["grid_{}".format(ia)].ClearSlot(ia)
				self.material_elements["grid_{}".format(ia)].Hide()

				self.material_elements["thinboard_{}".format(ia)] = self.__MakeThinBoard()
				self.material_elements["thinboard_{}".format(ia)].Hide()

				self.material_elements["textline_{}".format(ia)] = ui.TextLine()
				self.material_elements["textline_{}".format(ia)].SetParent(self.material_elements["thinboard_{}".format(ia)])
				self.material_elements["textline_{}".format(ia)].SetFontName(localeInfo.UI_DEF_FONT)
				self.material_elements["textline_{}".format(ia)].Hide()

		def func_set_info(self,index, targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type, applyRandomList):
			self.multi_refine_info.append([index,targetItemPos,nextGradeItemVnum,cost,prob,special_storage, type, applyRandomList])

		def Load(self):
			if FALSE == self.isLoaded:
				self.__LoadScript()

			self.dialogHeight = 62

			for i in xrange(min(self.pages_view, len(self.multi_refine_info) - self.pages_actual * self.pages_view +self.pages_view)):
				index = i + (self.pages_actual - 1)*self.pages_view
				
				if index >= len(self.multi_refine_info):
					continue

				self.index_select = self.multi_refine_info[index][0]
				self.targetItemPos = self.multi_refine_info[index][1]
				self.vnum= self.multi_refine_info[index][2]
				self.cost = self.multi_refine_info[index][3]
				self.percentage = self.multi_refine_info[index][4]
				self.special_storage = int(self.multi_refine_info[index][5])
				self.type = self.multi_refine_info[index][6]
				applyRandomList = self.multi_refine_info[index][7]

				self.probText.SetText(localeInfo.REFINE_SUCCESS_PROBALITY % (self.percentage))
				self.costText.SetText(localeInfo.REFINE_COST % (self.cost))

				self.toolTip.ClearToolTip()

				if app.WJ_ENABLE_TRADABLE_ICON:
					self.SetCantMouseEventSlot(self.targetItemPos)

				metinSlot = []
				for i in xrange(player.METIN_SOCKET_MAX_NUM):
					metinSlot.append(player.GetItemMetinSocket(self.targetItemPos, i))

				attrSlot = []
				for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					attrSlot.append(player.GetItemAttribute(self.targetItemPos, i))

				if app.ELEMENT_SPELL_WORLDARD:
					self.toolTip.FuncElementSpellItemDate(self.targetItemPos)

				self.toolTip.AddRefineItemData(self.vnum, metinSlot, attrSlot, apply_random_list = applyRandomList)

				item.SelectItem(self.vnum)
				self.itemImage.LoadImage(item.GetIconImageFileName())

				xSlotCount, ySlotCount = item.GetItemSize()
				for slot in self.slotList:
					slot.Hide()

				for i in xrange(min(3, ySlotCount)):
					self.slotList[i].SetPosition(-35, i*32 - (ySlotCount-1)*16)
					self.slotList[i].Show()

				if app.ENABLE_REFINE_RENEWAL:
					if constInfo.AUTO_REFINE_TYPE == 2 and chr.GetVirtualNumber(constInfo.AUTO_REFINE_DATA["NPC"][0]) == 20091:
						constInfo.IS_AUTO_REFINE = False
						self.checkBox.Hide()
					else:
						self.checkBox.Show()

				self.dialogHeight = self.toolTip.GetHeight() + 46
				self.UpdateDialog()

			for ia in xrange(0,self.total_count_material):
				self.material_elements["grid_{}".format(ia)] = self.__MakeItemSlot(ia)
				self.material_elements["grid_{}".format(ia)].ClearSlot(ia)
				self.material_elements["grid_{}".format(ia)].Hide()

				self.material_elements["thinboard_{}".format(ia)] = self.__MakeThinBoard()
				self.material_elements["thinboard_{}".format(ia)].Hide()

				self.material_elements["textline_{}".format(ia)] = ui.TextLine()
				self.material_elements["textline_{}".format(ia)].SetParent(self.material_elements["thinboard_{}".format(ia)])
				self.material_elements["textline_{}".format(ia)].SetFontName(localeInfo.UI_DEF_FONT)
				self.material_elements["textline_{}".format(ia)].Hide()

			count = 0

			if len(self.multi_refine_material)  != 0:
				for i in self.multi_refine_material:
					index = i[0]
					vnum_item = i[1]
					count_item = i[2]

					if index == self.index_select:
						
						self.material_elements["grid_{}".format(count)].SetPosition(50-35, self.dialogHeight)
						self.material_elements["grid_{}".format(count)].SetItemSlot(count, vnum_item, 0)
						self.material_elements["grid_{}".format(count)].Show()

						self.material_elements["thinboard_{}".format(count)].SetPosition(50, self.dialogHeight)
						self.material_elements["thinboard_{}".format(count)].SetSize(191, 20)
						self.material_elements["thinboard_{}".format(count)].Show()

						item.SelectItem(vnum_item)

						if player.GetItemCountByTT(vnum_item) < count_item and player.GetItemCountByVnum(vnum_item) < count_item:
							self.material_elements["textline_{}".format(count)].SetPackedFontColor(0xffFF0033)

						elif player.GetItemCountByVnum(vnum_item) >= count_item and player.GetItemCountByTT(vnum_item) < count_item:
							self.material_elements["textline_{}".format(count)].SetPackedFontColor(0xffdddddd)

						elif player.GetItemCountByTT(vnum_item) >= count_item and player.GetItemCountByVnum(vnum_item) < count_item:
							self.material_elements["textline_{}".format(count)].SetPackedFontColor(0xffdddddd)
						else:
							self.material_elements["textline_{}".format(count)].SetPackedFontColor(0xffFF0033)

						if player.GetItemCountByVnum(vnum_item) > 0 and player.GetItemCountByTT(vnum_item) <= 0:
							self.material_elements["textline_{}".format(count)].SetText("%s x%d  |cFFffce00(%d)" % (item.GetItemName(), count_item, player.GetItemCountByVnum(vnum_item)))
						else:
							self.material_elements["textline_{}".format(count)].SetText("%s x%d  |cFFffce00(%d)" % (item.GetItemName(), count_item, player.GetItemCountByTT(vnum_item)))


						self.material_elements["textline_{}".format(count)].SetOutline()
						self.material_elements["textline_{}".format(count)].SetFeather(FALSE)
						self.material_elements["textline_{}".format(count)].SetWindowVerticalAlignCenter()
						self.material_elements["textline_{}".format(count)].SetVerticalAlignCenter()

						if localeInfo.IsARABIC():
							(x,y) = self.material_elements["textline_{}".format(count)].GetTextSize()
							self.material_elements["textline_{}".format(count)].SetPosition(x, 0)
						else:
							self.material_elements["textline_{}".format(count)].SetPosition(15, 0)

						self.material_elements["textline_{}".format(count)].Show()

						self.dialogHeight += 34
						self.UpdateDialog()

						count+=1

			self.dialogHeight += 5
			self.UpdateDialog()

			Left_Last = self.WFunction(float(len(self.multi_refine_info))/float(self.pages_view))
			self.elements_multi_refine["total_pages"].SetText("%d/%d"%(self.pages_actual,Left_Last))

			if self.pages_actual * self.pages_view >= len(self.multi_refine_info):
				self.elements_multi_refine["buttons_{}".format("next")].Hide()
				self.elements_multi_refine["buttons_{}".format("last_next")].Hide()
			else:
				self.elements_multi_refine["buttons_{}".format("next")].Show()
				self.elements_multi_refine["buttons_{}".format("last_next")].Show()

			if self.pages_actual > 1:
				self.elements_multi_refine["buttons_{}".format("first_prev")].Show()
				self.elements_multi_refine["buttons_{}".format("prev")].Show()
			else:
				self.elements_multi_refine["buttons_{}".format("first_prev")].Hide()
				self.elements_multi_refine["buttons_{}".format("prev")].Hide()

		def WFunction(self, num):
			if (num + 1) != int(num+1):
				return int(num+1)
			else:
				return int(num)

		def __OnClickPage(self, func):
			Left_Last = self.WFunction(float(len(self.multi_refine_info))/float(self.pages_view))

			if func == 'MOSTBOUGHT_LEFT':
				self.pages_actual += 1
				self.Load()
			elif func == 'MOSTBOUGHT_LEFT_LAST':
				self.pages_actual = Left_Last
				self.Load()
			elif func == 'MOSTBOUGHT_RIGHT':
				self.pages_actual -= 1
				self.Load()
			elif func == 'MOSTBOUGHT_RIGHT_LAST':
				self.pages_actual = 1
				self.Load()

		def Open(self):
			self.UpdateDialog()

			self.SetTop()
			self.Show()

	else:

		def Open(self, targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type, apply_random_list = None):

			if FALSE == self.isLoaded:
				self.__LoadScript()

			if app.ENABLE_REFINE_RENEWAL:
				self.__InitializeOpen()
			else:
				self.__Initialize()

			self.targetItemPos = targetItemPos
			self.vnum = nextGradeItemVnum
			self.cost = cost
			self.percentage = prob
			self.type = type
			self.special_storage = int(special_storage)
			self.apply_random_list = apply_random_list

			self.probText.SetText(localeInfo.REFINE_SUCCESS_PROBALITY % (self.percentage))
			self.costText.SetText(localeInfo.REFINE_COST % (self.cost))

			self.toolTip.ClearToolTip()

			if app.WJ_ENABLE_TRADABLE_ICON:
				self.SetCantMouseEventSlot(targetItemPos)

			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))

			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(player.GetItemAttribute(targetItemPos, i))

			#def AddRefineItemData(self, item_vnum, sockets, attributes, rare_attr_slot = None, flags = 0, refine_element = None, apply_random_list = None, set_value = 0):
			self.toolTip.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot, applyRandomList = apply_random_list)


			item.SelectItem(nextGradeItemVnum)
			self.itemImage.LoadImage(item.GetIconImageFileName())
			xSlotCount, ySlotCount = item.GetItemSize()
			for slot in self.slotList:
				slot.Hide()
			for i in xrange(min(3, ySlotCount)):
				self.slotList[i].SetPosition(-35, i*32 - (ySlotCount-1)*16)
				self.slotList[i].Show()
				
			if app.ENABLE_REFINE_RENEWAL:
				if constInfo.AUTO_REFINE_TYPE == 2 and chr.GetVirtualNumber(constInfo.AUTO_REFINE_DATA["NPC"][0]) == 20091:
					constInfo.IS_AUTO_REFINE = False
					self.checkBox.Hide()
				else:
					self.checkBox.Show()

			self.dialogHeight = self.toolTip.GetHeight() + 46
			self.UpdateDialog()

			self.SetTop()
			self.Show()

	def Close(self):
		self.dlgQuestion = None
		self.Hide()

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.lockedItem = (-1, -1)
			self.SetCanMouseEventSlot(self.targetItemPos)

	if app.ENABLE_MULTI_REFINE_WORLDARD:
		def AppendMaterial(self, index, vnum, count):
			self.multi_refine_material.append([index,vnum,count])
	else:
		def AppendMaterial(self, vnum, count):
			slot = self.__MakeSlot()
			slot.SetParent(self)
			slot.SetPosition(15, self.dialogHeight)

			itemImage = self.__MakeItemImage()
			itemImage.SetParent(slot)
			item.SelectItem(vnum)
			itemImage.LoadImage(item.GetIconImageFileName())

			thinBoard = self.__MakeThinBoard()
			thinBoard.SetPosition(50, self.dialogHeight)
			thinBoard.SetSize(191, 20)

			textLine = ui.TextLine()
			textLine.SetParent(thinBoard)
			textLine.SetFontName(localeInfo.UI_DEF_FONT)

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

			if localeInfo.IsARABIC():
				(x,y) = textLine.GetTextSize()
				textLine.SetPosition(x, 0)
			else:
				textLine.SetPosition(15, 0)

			textLine.Show()
			self.children.append(textLine)

			self.dialogHeight += 34
			self.UpdateDialog()

	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 60
		newHeight = self.dialogHeight + 100+10

		## 936 : 개량 확률 표시 안함
		##if 936 == app.GetDefaultCodePage():
		newHeight -= 8

		if localeInfo.IsARABIC():
			self.board.SetPosition( newWidth, 0 )

			(x, y) = self.titleBar.GetLocalPosition()
			self.titleBar.SetPosition( newWidth - 15, y )

		if app.ENABLE_MULTI_REFINE_WORLDARD:
			newHeight += 20

		self.board.SetSize(newWidth, newHeight)
		self.toolTip.SetPosition(15 + 35, 38)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):
		if 100 == self.percentage:
			self.Accept()
			return

		if 5 == self.type: ## 무신의 축복서
			self.Accept()
			return

		dlgQuestion = uiCommon.QuestionDialog2()
		dlgQuestion.SetText2(localeInfo.REFINE_WARNING2)
		dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.Accept))
		dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))

		if 3 == self.type: ## 현철
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_1)
			dlgQuestion.SetText2(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_2)
		elif 2 == self.type: ## 축복서
			dlgQuestion.SetText1(localeInfo.REFINE_DOWN_GRADE_WARNING)
		else:
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING)

		dlgQuestion.Open()
		self.dlgQuestion = dlgQuestion

	def Accept(self):
		if app.ENABLE_MULTI_REFINE_WORLDARD:
			net.SendRefinePacket(self.targetItemPos, self.type, self.special_storage, self.index_select)
		else:
			net.SendRefinePacket(self.targetItemPos, self.type, self.special_storage)

		
		if not app.ENABLE_REFINE_RENEWAL:
			self.Close()

	if app.ENABLE_REFINE_RENEWAL:	
		def AutoRefine(self, checkType, autoFlag):
			constInfo.IS_AUTO_REFINE = autoFlag
		
		def CheckRefine(self, isFail):
			import chat

			#chat.AppendChat(1,"test 1")

			if constInfo.IS_AUTO_REFINE == True:
				if constInfo.AUTO_REFINE_TYPE == 1:
					if constInfo.AUTO_REFINE_DATA["ITEM"][0] != -1 and constInfo.AUTO_REFINE_DATA["ITEM"][1] != -1:
						scrollIndex = player.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][0])
						itemIndex = player.GetItemIndex(constInfo.AUTO_REFINE_DATA["ITEM"][1])
						
						#chat.AppendChat(1,"test 2")
						# chat.AppendChat(chat.CHAT_TYPE_INFO, "%d %d" % (itemIndex, int(itemIndex %10)))
						if scrollIndex == 0 or (itemIndex % 10 == 8 and not isFail):
							#chat.AppendChat(1,"test 3")
							self.Close()
						else:
							net.SendItemUseToItemPacket(constInfo.AUTO_REFINE_DATA["ITEM"][0], constInfo.AUTO_REFINE_DATA["ITEM"][1])
				elif constInfo.AUTO_REFINE_TYPE == 2:
					npcData = constInfo.AUTO_REFINE_DATA["NPC"]					
					if npcData[0] != 0 and npcData[1] != -1 and npcData[2] != -1 and npcData[3] != 0:
						itemIndex = player.GetItemIndex(npcData[1], npcData[2])
						if (itemIndex % 10 == 8 and not isFail) or isFail:
							self.Close()
						else:
							net.SendGiveItemPacket(npcData[0], npcData[1], npcData[2], npcData[3])
				else:
					#chat.AppendChat(1,"test 4")
					self.Close()
			else:
				#chat.AppendChat(1,"test 5")
				self.Close()

	def CancelRefine(self):
		if app.ENABLE_MULTI_REFINE_WORLDARD:
			net.SendRefinePacket(255, 255, 255, -1)
		else:
			net.SendRefinePacket(255, 255, 255)

		self.Close()
		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 0
			constInfo.AUTO_REFINE_DATA = {
				"ITEM" : [-1, -1],
				"NPC" : [0, -1, -1, 0]
			}

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
