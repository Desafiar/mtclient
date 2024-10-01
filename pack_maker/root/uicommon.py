import ui
import app
import ime
import item
import player
import constInfo
import uiToolTip
import localeInfo
import uiScriptLocale

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.accceptButton = self.GetChild("accept")
			self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		self.acceptEvent()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.message.SetText(text)

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetButtonName(self, name):
		self.accceptButton.SetText(name)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

class QuestionRemoveStoneSpecial(ui.BoardWithTitleBar):
	BOARD_WIDTH = 240
	BOARD_HEIGH = 153
	
	STONE_SLOTS_NUMB = 3
	SLOTS_ITEM_BLOCK = [constInfo.ERROR_METIN_STONE, 1, 0]
	
	def __init__(self):
		def LoadBoardPage():
			self.SetSize(self.BOARD_WIDTH, self.BOARD_HEIGH)
			self.SetCenterPosition()
			self.AddFlag('float')
			self.SetTitleName(localeInfo.SPECIAL_REMOVE_STONE_TITLE)
			self.SetCloseEvent(self.Close)
		ui.BoardWithTitleBar.__init__(self, True)
		LoadBoardPage()
		self.__initVariables__()
		self.__CreateUI()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
	
	def __initVariables__(self):
		self.selected_slot = None
		self.tooltipItem = None
		self.slotIndex = None
		self.itemVnum = None
		self.stone_slots = {i:0 for i in xrange(self.STONE_SLOTS_NUMB)}
		self.UI_Elements = {}

	def __CreateUI(self):
		self.UI_Elements['base_thinboard'] = self.__MakeThinBoard()
		self.UI_Elements['base_thinboard'].SetPosition(10, 32)
		self.UI_Elements['base_thinboard'].SetSize(self.BOARD_WIDTH-20, self.BOARD_HEIGH-42)
		self.UI_Elements['base_thinboard'].Show()
		
		self.UI_Elements['slot_item'] = ui.GridSlotWindow()
		self.UI_Elements['slot_item'].SetParent(self.UI_Elements['base_thinboard'])
		self.UI_Elements['slot_item'].SetPosition(15, 7)
		self.UI_Elements['slot_item'].ArrangeSlot(0, 1, 3, 32, 32, 0, 0)
		self.UI_Elements['slot_item'].SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		self.UI_Elements['slot_item'].SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
		self.UI_Elements['slot_item'].SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		self.UI_Elements['slot_item'].Show()
		
		self.UI_Elements['slots_stones'] = ui.GridSlotWindow()
		self.UI_Elements['slots_stones'].SetParent(self.UI_Elements['base_thinboard'])
		self.UI_Elements['slots_stones'].SetPosition(64, 7)
		self.UI_Elements['slots_stones'].ArrangeSlot(0, self.STONE_SLOTS_NUMB, 1, 32, 32, 20, 0)
		self.UI_Elements['slots_stones'].SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
		self.UI_Elements['slots_stones'].SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		self.UI_Elements['slots_stones'].SetOverInItemEvent(ui.__mem_func__(self.OverInStoneItem))
		self.UI_Elements['slots_stones'].SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))
		self.UI_Elements['slots_stones'].Show()
		
		for slot in xrange(self.STONE_SLOTS_NUMB):
			self.UI_Elements['slots_stones'].DeactivateSlot(slot)
		
		self.UI_Elements['accept_Button'] = ui.MakeButtonRemoveStone(self.UI_Elements['base_thinboard'], 58, 7+33+7, '', "d:/ymir work/ui/public/", "select_btn_01.sub", "select_btn_02.sub", "select_btn_03.sub", localeInfo.UI_REMOVE)
		self.UI_Elements['close_Button'] = ui.MakeButtonRemoveStone(self.UI_Elements['base_thinboard'], 58, 7+33+32+7, '', "d:/ymir work/ui/public/", "select_btn_01.sub", "select_btn_02.sub", "select_btn_03.sub", localeInfo.UI_CANCEL)

	def __MakeThinBoard(self):
		thinBoard = ui.ThinBoard()
		thinBoard.SetParent(self)
		thinBoard.Show()
		return thinBoard
	
	def Open(self):
		self.Show()

	def Close(self):
		self.Hide()

	def SetItemSlot(self, slot, count, tooltipItem):
		self.selected_slot = None
		self.tooltipItem = tooltipItem
		self.slotIndex = slot
		self.itemVnum = player.GetItemIndex(player.INVENTORY, slot)
		self.UI_Elements['slot_item'].SetItemSlot(0, self.itemVnum, count)

		for slot in xrange(self.STONE_SLOTS_NUMB):
			stone_vnum = player.GetItemMetinSocket(self.slotIndex, slot)
			self.stone_slots[slot] = [stone_vnum, 0][bool(stone_vnum in self.SLOTS_ITEM_BLOCK[1:])]
			if stone_vnum in self.SLOTS_ITEM_BLOCK[1:]:
				continue
			
			self.UI_Elements['slots_stones'].SetItemSlot(slot, stone_vnum, 1)
		self.UI_Elements['accept_Button'].Disable()
		self.UI_Elements['accept_Button'].Down()

	def ShowToolTipItem(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex, player.INVENTORY)

	def ShowToolTipStones(self, itemIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetItemToolTip(itemIndex)

	def OnOverInItem(self, slotIndex):
		if self.tooltipItem:
			if 0 != self.itemVnum:
				self.ShowToolTipItem(self.slotIndex)
	
	def OnOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
	
	def OverInStoneItem(self, slotIndex):
		item_vnum = self.stone_slots[int(slotIndex)]
		if self.tooltipItem:
			if 0 != item_vnum:
				self.ShowToolTipStones(item_vnum)

	def SetAcceptEvent(self, event):
		self.UI_Elements['accept_Button'].SetEvent(event)

	def SetCancelEvent(self, event):
		self.UI_Elements['close_Button'] .SetEvent(event)

	def SelectItemSlot(self, slotPos):
		if self.slotIndex == None:
			return
		
		if self.selected_slot == int(slotPos):
			self.UI_Elements['slots_stones'].DeactivateSlotEffect(slotPos)
			self.selected_slot = None
			self.UI_Elements['accept_Button'].Disable()
			self.UI_Elements['accept_Button'].Down()
			return
		
		stone_socket = player.GetItemMetinSocket(self.slotIndex, slotPos)
		if stone_socket in self.SLOTS_ITEM_BLOCK:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANT_CHOSE_STONE)
			return
		
		for slot in xrange(self.STONE_SLOTS_NUMB):
			self.UI_Elements['slots_stones'].DeactivateSlotEffect(slot)
		self.UI_Elements['slots_stones'].ActivateSlotEffect(slotPos, 1.0, 0.0, 0.0, 1.0)
		self.selected_slot = int(slotPos)
		self.UI_Elements['accept_Button'].Enable()
		self.UI_Elements['accept_Button'].SetUp()
	
	def OnPressEscapeKey(self):
		self.Close()
		return True

if app.ENABLE_NEW_DROP_DIALOG:
	class QuestionDropDialog(ui.ScriptWindow):
		class ConfirmItemDestroy(ui.ScriptWindow):
			def __init__(self, mainclass):
				ui.ScriptWindow.__init__(self)
				self.mainclass = mainclass;
				self.eventdestroy = None
				self.acceptButton = None
				self.cancel = None
				self.__CreateDialog()

			def __del__(self):
				ui.ScriptWindow.__del__(self)

			def __CreateDialog(self):
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog_confirmdestroy.py")
				self.acceptButton = self.GetChild("accept")
				self.acceptButton.SAFE_SetEvent(self.AcceptEvent)
				self.cancel = self.GetChild("cancel")
				self.cancel.SAFE_SetEvent(self.Close)

			def Open(self, event):
				self.eventdestroy = event
				if self.IsShow():
					self.Close()
				else:
					self.Show()

			def AcceptEvent(self):
				if self.eventdestroy:
					self.eventdestroy()

			def Close(self):
				self.Hide()

			def Destroy(self):
				self.ClearDictionary()
				self.eventdestroy = None
				self.acceptButton = None
				self.cancel = None
				self.Close()

			def GetBasePosition(self):
				x, y = self.mainclass.GetGlobalPosition()
				return x+235, y + 42

			def AdjustPositionAndSize(self):
				bx, by = self.GetBasePosition()
				self.SetPosition(bx, by);

		def __init__(self, inveType = player.INVENTORY):
			ui.ScriptWindow.__init__(self)
			self.board = None
			self.titleBar = None
			self.acceptButton = None
			self.destroyButton = None
			self.energyButton = None
			self.runasButton = None
			self.cancelButton = None
			self.tooltipItem = None
			self.ItemSlot = None
			self.itemVnum = 0
			self.slotIndex = 0
			self.invenType = inveType
			self.ConfirmItemDestroy = self.ConfirmItemDestroy(self)
			self.__CreateDialog()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self):
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/questiondropdialogitem.py")
			self.board = self.GetChild("board")
			self.acceptButton = self.GetChild("accept")
			self.ItemSlot = self.GetChild("ItemSlot")
			self.destroyButton = self.GetChild("destroy")
			self.energyButton = self.GetChild("energy")
			self.runasButton = self.GetChild("runas")
			self.cancelButton = self.GetChild("cancel")
			self.titleBar = self.GetChild("TitleBar")

			self.ItemSlot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
			self.ItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))

			if self.ConfirmItemDestroy:
				self.ConfirmItemDestroy.Close()

		def Open(self):
			self.SetCenterPosition()
			self.SetTop()
			if self.ConfirmItemDestroy:
				self.ConfirmItemDestroy.AdjustPositionAndSize()
			self.Show()

		def Close(self):
			self.Hide()
			if self.ConfirmItemDestroy:
				self.ConfirmItemDestroy.Close()
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		def Destroy(self):
			self.ClearDictionary()
			self.board = None
			self.titleBar = None
			self.acceptButton = None
			self.destroyButton = None
			self.energyButton = None
			self.runasButton = None
			self.cancelButton = None
			self.tooltipItem = None
			self.ItemSlot = None
			self.itemVnum = 0
			self.slotIndex = 0

			if self.ConfirmItemDestroy:
				self.ConfirmItemDestroy.Close()

		def SAFE_SetAcceptEvent(self, event):
			self.acceptButton.SAFE_SetEvent(event)

		def SAFE_SetCancelEvent(self, event):
			self.cancelButton.SAFE_SetEvent(event)

		def SetAcceptEvent(self, event):
			self.acceptButton.SetEvent(event)

		def SetItemSlot(self, slot, count, tooltipItem):
			self.itemVnum = player.GetItemIndex(self.invenType, slot)
			self.slotIndex = slot
			self.tooltipItem = tooltipItem
			if 0 == count:
				count = 1
			level = player.GetStatus(player.LEVEL)
			self.ItemSlot.SetItemSlot(0, self.itemVnum, count)

			if player.IsAntiFlagBySlot(self.invenType, self.slotIndex, item.ITEM_ANTIFLAG_PKDROP) or\
			player.IsAntiFlagBySlot(self.invenType, self.slotIndex, item.ITEM_ANTIFLAG_DROP):
				self.acceptButton.Down()
				self.acceptButton.Disable()
			else:
				self.acceptButton.SetUp()
				self.acceptButton.Enable()

			# if player.IsAntiFlagBySlot(self.invenType, self.slotIndex, item.ITEM_ANTIFLAG_DESTROY):
				# self.destroyButton.Down()
				# self.destroyButton.Disable()
			# else:

			self.destroyButton.SetUp()
			self.destroyButton.Enable()

			#ENERGY R
			if level < 50:
				self.energyButton.Down()
				self.energyButton.Disable()
			else:
				self.energyButton.SetUp()
				self.energyButton.Enable()

			#RUNE
			if level < 50:
				self.runasButton.Down()
				self.runasButton.Disable()
			else:
				self.runasButton.SetUp()
				self.runasButton.Enable()

		def SetItemToolTip(self, tooltipItem):
			self.tooltipItem = tooltipItem

		def ShowToolTip(self, slotIndex):
			if None != self.tooltipItem:
				self.tooltipItem.SetInventoryItem(slotIndex, self.invenType)

		def SetDestroyEvent(self, event):
			self.destroyButton.SetEvent(event)

		def SetDestroyEnergyEvent(self, event):
			self.energyButton.SetEvent(event)

		def SetDestroyRunasEvent(self, event):
			self.runasButton.SetEvent(event)

		def OpenGuiDestroy(self, event):
			if self.ConfirmItemDestroy:
				self.ConfirmItemDestroy.Open(event)

		def SetCancelEvent(self, event):
			self.cancelButton.SetEvent(event)

		def SetAcceptText(self, text):
			self.acceptButton.SetText(text)

		def SetCancelText(self, text):
			self.cancelButton.SetText(text)

		def OnTop(self):
			if self.ConfirmItemDestroy:
				self.ConfirmItemDestroy.SetTop()

		def __OnOverInItem(self, slotIndex):
			if self.tooltipItem:
				if 0 != self.itemVnum:
					self.ShowToolTip(self.slotIndex)

		def __OnOverOutItem(self):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()

		def OnMoveWindow(self, x, y):
			if self.ConfirmItemDestroy:
				self.ConfirmItemDestroy.AdjustPositionAndSize()

		def OnPressEscapeKey(self):
			self.Close()
			return True

class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 6 + 10
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
		if self.IsRTL():
			self.inputValue.SetPosition(self.inputValue.GetWidth(), 0)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		if localeInfo.IsARABIC() :
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "inputdialogwithdescription.py")
		else:
			pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description = getObject("Description")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription(self, text):
		self.description.SetText(text)

class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description1 = getObject("Description1")
			self.description2 = getObject("Description2")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class QuestionDialog(ui.ScriptWindow):
	def __init__(self, size = "default"):
		ui.ScriptWindow.__init__(self)
		self.size = size
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

		if self.size == "thin":
			self.SetSize(340, 70)
			self.board.SetSize(340, 70)
			self.textLine.SetPosition(0, 20)
			self.acceptButton.SetPosition(-40, 35)
			self.cancelButton.SetPosition(40, 35)

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True

class QuestionDialogItem(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.slot = None
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialogitem.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.destroyButton = self.GetChild("destroy")
		self.cancelButton = self.GetChild("cancel")
		
		self.ItemSlot = self.GetChild("ItemSlot")
		self.ItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.ItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()
		height = self.GetHeight()
		width = self.GetWidth()
		self.SetSize(width, height+(32*3)+20)
		self.board.SetSize(width, height+(32*3)+20)
		
		self.acceptButton.SetPosition(-60,63 +(32*3)+10)
		self.destroyButton.SetPosition(0,63 +(32*3)+10)
		self.cancelButton.SetPosition(60,63 +(32*3)+10)
		
	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()
		
	def SetItem(self, vnum, attachedItemSlotPos, count):
		self.ItemSlot.SetItemSlot(0,vnum, count)
		self.slot = attachedItemSlotPos

	def OverOutItem(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, slotIndex=0):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(self.slot)

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetDestroyEvent(self, event):
		self.destroyButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

class QuestionDialog2(QuestionDialog):

	def __init__(self, size = "default"):
		ui.ScriptWindow.__init__(self)
		self.size = size
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text):
		self.textLine1.SetText(text)

	def SetText2(self, text):
		self.textLine2.SetText(text)

class QuestionDialogWithTimeLimit(QuestionDialog2):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0

	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, msg, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeInfo.UI_LEFT_TIME % (leftTime))

class MoneyInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()
		self.SetMaxLength(13)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		#self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		length = min(13, length)

		self.inputValue.SetMax(length)
		self.inputValue.SetUserMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))		


	def GetText(self):
		return self.inputValue.GetText()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputValue)

		text = self.inputValue.GetText()
		for i in xrange(len(text)):
			if not text[i].isdigit():
				text=text[0:i]+text[i+1:]
				self.inputValue.SetText(text)
		self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(text))

