import app, player,ui,wndMgr,grp,grpText,localeInfo,chat,item

class ThanosWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.itemSlotLeft = 0
		self.itemSlotRight = 0
		self.itemNameList = []
		self.tooltipItem = 0
		self.wndInventory = 0
		self.btnClose = 0
		self.Initialize()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Initialize(self):
		self.mainBoard=None
		self.Clear()
		self._LoadWindow()

	def Clear(self):
		self.itemSlotLeft = 0
		self.itemSlotRight = 0
		self.itemNameList = []
		self.tooltipItem = 0
		self.wndInventory = 0
		self.btnClose = 0

	def Destroy(self):
		self.ClearDictionary()
		self.mainBoard=None
		self.Clear()

	def _LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/thanos_window.py")
		except:
			import exception
			exception.Abort("ThanosWindow.LoadDialog.LoadObject")
		try:
			GetObject = self.GetChild
			self.mainBoard = GetObject("ThanosBoard")
			for i in xrange(item.GLOVE_SLOT_COUNT):
				self.itemNameList.append(GetObject("itemName_"+str(i+1)))
			self.itemSlotLeft = GetObject("itemSlotLeft")
			self.itemSlotRight = GetObject("itemSlotRight")
			self.btnClose = GetObject("CloseButton")
		except:
			import exception
			exception.Abort("ThanosWindow.LoadDialog.BindObject")
		self.btnClose.SetEvent(ui.__mem_func__(self.ToggleWindow))
		self.SetCenterPosition()

	def BindInventory(self, wndInven):
		self.wndInventory = wndInven
		self.itemSlotLeft.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		self.itemSlotLeft.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		self.itemSlotLeft.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		self.itemSlotLeft.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		self.itemSlotLeft.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		self.itemSlotLeft.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))
		
		self.itemSlotRight.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		self.itemSlotRight.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		self.itemSlotRight.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		self.itemSlotRight.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		self.itemSlotRight.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		self.itemSlotRight.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

	def ToggleWindow(self):
		if not self.IsShow(): 
			self.Show()
			self.SetTop()
		else: self.Hide()
	def OnUpdate(self):
		for i in xrange(item.GLOVE_SLOT_COUNT / 2):
			slotIdx = item.GLOVE_SLOT_START + i
			itemVnum = player.GetItemIndex(slotIdx)
			if itemVnum != 0:
				item.SelectItem(itemVnum)
				self.itemSlotLeft.SetItemSlot(slotIdx, itemVnum, 0)
				self.itemNameList[i].SetText(item.GetItemName())
			else:
				self.itemSlotLeft.ClearSlot(slotIdx)
				self.itemNameList[i].SetText(localeInfo.BOS_SLOT)
		for i in xrange(item.GLOVE_SLOT_COUNT / 2, item.GLOVE_SLOT_COUNT):
			slotIdx = item.GLOVE_SLOT_START + i
			itemVnum = player.GetItemIndex(slotIdx)
			if itemVnum != 0:
				item.SelectItem(itemVnum)
				self.itemSlotRight.SetItemSlot(slotIdx, itemVnum, 0)
				self.itemNameList[i].SetText(item.GetItemName())
			else:
				self.itemSlotRight.ClearSlot(slotIdx)
				self.itemNameList[i].SetText(localeInfo.BOS_SLOT)
		self.itemSlotLeft.RefreshSlot()
		self.itemSlotRight.RefreshSlot()

