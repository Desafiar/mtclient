import ui
import player
import mouseModule
import net
import app
import snd
import item
import player
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
#import uiPrivateShopBuilder # 개인상점 열동안 ItemMove 방지
import localeInfo
import constInfo
import ime
import dbg
import wndMgr
import uiToolTip
import game
from uiUtils import Edit2 as Edit2

if app.BL_67_ATTR:
	import uiAttr67Add

ITEM_MALL_BUTTON_ENABLE = True

import exception

ITEM_FLAG_APPLICABLE = 1 << 14

if app.ENABLE_SASH_SYSTEM:
	import sash

class CostumeWindow(ui.ScriptWindow):

	def __init__(self, wndInventory):
		if not app.ENABLE_COSTUME_SYSTEM:
			exception.Abort("What do you do?")
			return
		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return
		ui.ScriptWindow.__init__(self)
		self.wndInventory = wndInventory
		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.elemets_world = {}
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Open(self):
		self.RefreshCostumeSlot()
		self.Show()

	def Destroy(self):
		self.toolTip = None
		self.wndInventory = None
		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.elemets_world = {}
			self.elemets_hide = {}
		self.slot = {}

	def Close(self):
		self.SetOverOutEvent2()
		self.Hide()

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CostumeWindow.py")
		except:
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.ClearToolTip()
		self.slot = {
			item.COSTUME_SLOT_START : [self.__MakeSlot(item.COSTUME_SLOT_START, 1, 1, 53, 40, 64), localeInfo.COSTUME_SLOT_COSTUME_ARMOR],		# Armor
			item.COSTUME_SLOT_START + 1 : [self.__MakeSlot(item.COSTUME_SLOT_START + 1, 1, 1, 53, 0), localeInfo.COSTUME_SLOT_COSTUME_HAIR],	# Hair
			item.COSTUME_SLOT_START + 2 : [self.__MakeSlot(item.COSTUME_SLOT_START + 2, 1, 1, 100, 6), localeInfo.COSTUME_SLOT_MOUNT],			# Mount
			item.COSTUME_SLOT_START + 3 : [self.__MakeSlot(item.COSTUME_SLOT_START + 3, 1, 1, 102 + 33, 6), localeInfo.COSTUME_SLOT_CARCAJ],	# Sash
			# item.COSTUME_SLOT_START + 3 : [self.__MakeSlot(item.COSTUME_SLOT_START + 3, 1, 1, 101 + 33, 6), localeInfo.COSTUME_SLOT_SASH],	# Sash
			item.COSTUME_SLOT_WEAPON: [self.__MakeSlot(item.COSTUME_SLOT_WEAPON, 1, 1, 5, 6, 96), localeInfo.COSTUME_SLOT_COSTUME_WEAPON],		# Weapon
			item.SKIN_SASH_SLOT_START  : [self.__MakeSlot(item.SKIN_SASH_SLOT_START, 1, 1, 134, 70), localeInfo.COSTUME_SLOT_COSTUME_SASH],		# Sash Skin
			item.SLOT_MOUNT_SKIN : [self.__MakeSlot(item.SLOT_MOUNT_SKIN, 1, 1, 100 + 34, 38), localeInfo.COSTUME_SLOT_MOUNT_SKIN],				# Mount Skin
			item.EQUIPMENT_OLDPET : [self.__MakeSlot(item.EQUIPMENT_OLDPET, 1, 1, 100, 70), localeInfo.COSTUME_SLOT_PET],						# Pet Skin
			item.EQUIPMENT_PET : [self.__MakeSlot(item.EQUIPMENT_PET, 1, 1, 100, 38), localeInfo.COSTUME_SLOT_PET_OFICIAL],						# Pet
			# Shining Weapon
			item.SHINING_SLOT_START : [self.__MakeSlot(item.SHINING_SLOT_START, 1, 1, 32, 119), localeInfo.COSTUME_SLOT_EFECT_WEAPON],
			# Shining Armor
			item.SHINING_SLOT_START + 1 : [self.__MakeSlot(item.SHINING_SLOT_START + 1, 1, 1, 68, 119), localeInfo.COSTUME_SLOT_EFECT_ARMOR],
			# Shining Special
			# item.SHINING_SLOT_START + 2 : [self.__MakeSlot(item.SHINING_SLOT_START + 2, 1, 1, 1000, 1210), localeInfo.COSTUME_SLOT_EFECT_ARMOR],

			# ENABLE_AURA_SYSTEM
			item.COSTUME_SLOT_AURA : [self.__MakeSlot(item.COSTUME_SLOT_AURA, 1, 1, 135, 103), localeInfo.COSTUME_SLOT_AURA],

			# item.COSTUME_SLOT_START + 2            : [self.__MakeSlot(item.COSTUME_SLOT_START + 2, 1, 1, 100, 6), localeInfo.COSTUME_SLOT_MOUNT],
			# item.EQUIPMENT_PET           : [self.__MakeSlot(item.EQUIPMENT_PET, 1, 1, 100, 38), localeInfo.COSTUME_SLOT_PET_OFICIAL],
			# item.SLOT_MOUNT_SKIN           : [self.__MakeSlot(item.SLOT_MOUNT_SKIN, 1, 1, 100+34, 38), localeInfo.COSTUME_SLOT_MOUNT_SKIN],
			# item.EQUIPMENT_OLDPET         : [self.__MakeSlot(item.EQUIPMENT_OLDPET, 1, 1, 100, 70), localeInfo.COSTUME_SLOT_PET],
			# item.COSTUME_SLOT_START       : [self.__MakeSlot(item.COSTUME_SLOT_START, 1, 1, 53, 40, 64), localeInfo.COSTUME_SLOT_COSTUME_ARMOR],
			# item.COSTUME_SLOT_START + 1   : [self.__MakeSlot(item.COSTUME_SLOT_START + 1, 1, 1, 53, 0), localeInfo.COSTUME_SLOT_COSTUME_HAIR],
			# item.SKIN_SASH_SLOT_START  : [self.__MakeSlot(item.SKIN_SASH_SLOT_START, 1, 1, 134, 70), localeInfo.COSTUME_SLOT_COSTUME_SASH],
			# item.COSTUME_SLOT_WEAPON      : [self.__MakeSlot(item.COSTUME_SLOT_WEAPON, 1, 1, 5, 6, 96), localeInfo.COSTUME_SLOT_COSTUME_WEAPON],
			# player.EQUIPMENT_SLOT_START+9 : [self.__MakeSlot(player.EQUIPMENT_SLOT_START+9, 1, 1, 101 + 32, 5), localeInfo.COSTUME_SLOT_CARCAJ],

			# shining
			#Weapon
			# item.SHINING_SLOT_START       : [self.__MakeSlot(item.SHINING_SLOT_START, 1, 1, 32, 119), localeInfo.COSTUME_SLOT_EFECT_WEAPON],
			# item.SHINING_SLOT_START + 1   : [self.__MakeSlot(item.SHINING_SLOT_START + 1, 1, 1, 68, 119), localeInfo.COSTUME_SLOT_EFECT_ARMOR],
			# item.SHINING_SLOT_START + 2   : [self.__MakeSlot(item.SHINING_SLOT_START + 2, 1, 1, 103, 119), localeInfo.COSTUME_SLOT_EFECT_WEAPON],

			#Armor
			# item.SHINING_SLOT_START + 3     : [self.__MakeSlot(item.SHINING_SLOT_START + 3, 3, 1, 32, 150), localeInfo.COSTUME_SLOT_EFECT_ARMOR],
			# item.SHINING_SLOT_START + 4   : [self.__MakeSlot(item.SHINING_SLOT_START + 4, 1, 1, 68, 150), localeInfo.COSTUME_SLOT_EFECT_ARMOR],
			# item.SHINING_SLOT_START + 5   : [self.__MakeSlot(item.SHINING_SLOT_START + 5, 1, 1, 103, 150), localeInfo.COSTUME_SLOT_EFECT_ARMOR],

			#Special
			# item.SHINING_SLOT_START + 6   : [self.__MakeSlot(item.SHINING_SLOT_START + 6, 1, 1, 1000, 1210), localeInfo.COSTUME_SLOT_EFECT_ARMOR],
		}

	def __MakeSlot(self, StartIndex, xCount, yCount, pX, pY, sy = 32):
		slot = ui.SlotWindow()
		slot.SetParent(self.GetChild("Costume_Base"))
		slot.SetPosition(pX + 3, pY + 3)
		slot.SetSize(32, sy)
		slot.AppendSlot(StartIndex, xCount, yCount, 32, sy)
		slot.SetOverInEvent2(ui.__mem_func__(self.SetOverInEvent2))
		slot.SetOverOutEvent2(ui.__mem_func__(self.SetOverOutEvent2))
		slot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		slot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlotNew))
		slot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlotNew))
		slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		slot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))
		slot.Show()
		return slot

	def SetOverInEvent2(self, slotNumber):
		if slotNumber in self.slot:
			self.toolTip.ClearToolTip()
			self.toolTip.AlignHorizonalCenter()
			self.toolTip.AutoAppendNewTextLine(self.slot[slotNumber][1], grp.GenerateColor(1.0, 1.0, 0.0, 1.0))
			self.toolTip.Show()

	def SetOverOutEvent2(self):
		self.toolTip.Hide()

	def RefreshCostumeSlot(self):
		for key, v in self.slot.items():
			v[0].SetItemSlot(key, player.GetItemIndex(key), 0)
			v[0].RefreshSlot()
			
		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.elemets_hide = self.wndInventory.get_costume_hide_list()
			self.ButtonsHideCostume()
			self.costume_hide_load()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def ButtonsHideCostume(self):
			self.elemets_world["position"] = [
				[61 - 10,45 - 10],        # 0
				[61 - 10,8 - 10],         # 1
				[13- 10,15- 15],          # 2
				[62 + 22, 126 - 15],      # 3
				[134, 68]       # 4 hide shash
				# [33 ,118],       # 5 hide efect weapon 1
				# [66 ,118],       # 6 hide efect weapon 2
				# [99 ,118],       # 7 hide efect weapon 3
				# [33 ,150],       # 8 hide efect body 1
				# [33 ,170],       # 8 hide efect body 2
				# [33 ,180]        # 8 hide efect body 3
			]

			for i in xrange(self.GetSlotCount()):
				if i == 3:
					continue
				self.elemets_world["hide_button_%d"%i] = ui.Button()
				self.elemets_world["hide_button_%d"%i].SetParent(self)
				self.elemets_world["hide_button_%d"%i].SetPosition(self.elemets_world["position"][i][0]+12,self.elemets_world["position"][i][1]+37)
				self.elemets_world["hide_button_%d"%i].SetUpVisual("Modulo/HideCostume/button_show_0.tga")
				self.elemets_world["hide_button_%d"%i].SetOverVisual("Modulo/HideCostume/button_show_1.tga")
				self.elemets_world["hide_button_%d"%i].SetDownVisual("Modulo/HideCostume/button_show_0.tga")
				self.elemets_world["hide_button_%d"%i].SetEvent(self.FuncHide,i)
				self.elemets_world["hide_button_%d"%i].Hide()

		def FuncHide(self,index):
			net.SendChatPacket("/costume_hide %d" %index)

		def costume_hide_load(self):
			for i in xrange(self.GetSlotCount()):
				if i == 3:
					continue
				
				if len(self.elemets_hide) > 0:
					self.elemets_world["hide_button_%d"%self.elemets_hide[i][0]].SetUpVisual("Modulo/HideCostume/button_%s_0.tga"%self.ButtonInfoHide(self.elemets_hide[i][1]))
					self.elemets_world["hide_button_%d"%self.elemets_hide[i][0]].SetOverVisual("Modulo/HideCostume/button_%s_1.tga"%self.ButtonInfoHide(self.elemets_hide[i][1]))
					self.elemets_world["hide_button_%d"%self.elemets_hide[i][0]].SetDownVisual("Modulo/HideCostume/button_%s_0.tga"%self.ButtonInfoHide(self.elemets_hide[i][1]))
				self.elemets_world["hide_button_%d"%i].Show()

		def ButtonInfoHide(self,index):
			if index == 0:
				return "show"
			return "hide"

		def GetSlotCount(self):
			return len(self.elemets_world["position"]) if self.elemets_world.has_key("position") else 0
			slot_total = 2

			if app.ENABLE_HIDE_COSTUME_SYSTEM_ACCE:
				slot_total += 1
			if app.ENABLE_HIDE_COSTUME_SYSTEM_WEAPON_COSTUME:
				slot_total += 1

			slot_total += 3

			return slot_total

class BeltInventoryWindow(ui.ScriptWindow):
	def __init__(self, wndInventory):
		if not app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			exception.Abort("What do you do?")
			return
		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0
		self.wndInventory = wndInventory;

		self.wndBeltInventoryLayer = None
		self.wndBeltInventorySlot = None
		self.expandBtn = None
		self.minBtn = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self, openBeltSlot = False):
		self.__LoadWindow()
		self.RefreshSlot()
		ui.ScriptWindow.Show(self)
		if openBeltSlot:
			self.OpenInventory()
		else:
			self.CloseInventory()

	def Close(self):
		self.Hide()

	def IsOpeningInventory(self):
		return self.wndBeltInventoryLayer.IsShow()

	def OpenInventory(self):
		self.wndBeltInventoryLayer.Show()
		self.expandBtn.Hide()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	def CloseInventory(self):
		self.wndBeltInventoryLayer.Hide()
		self.expandBtn.Show()

		if localeInfo.IsARABIC() == 0:
			self.AdjustPositionAndSize()

	def GetBasePosition(self):
		x, y = self.wndInventory.GetGlobalPosition()
		return x - 148, y + 241	

	def AdjustPositionAndSize(self):
		bx, by = self.GetBasePosition()

		if self.IsOpeningInventory():
			self.SetPosition(bx, by)
			self.SetSize(self.ORIGINAL_WIDTH, self.GetHeight())

		else:
			self.SetPosition(bx + 138, by);
			self.SetSize(10, self.GetHeight())

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/BeltInventoryWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			self.ORIGINAL_WIDTH = self.GetWidth()
			wndBeltInventorySlot = self.GetChild("BeltInventorySlot")
			self.wndBeltInventoryLayer = self.GetChild("BeltInventoryLayer")
			self.expandBtn = self.GetChild("ExpandBtn")
			self.minBtn = self.GetChild("MinimizeBtn")

			self.expandBtn.SetEvent(ui.__mem_func__(self.OpenInventory))
			self.minBtn.SetEvent(ui.__mem_func__(self.CloseInventory))

			if localeInfo.IsARABIC() :
				self.expandBtn.SetPosition(self.expandBtn.GetWidth() - 2, 15)
				self.wndBeltInventoryLayer.SetPosition(self.wndBeltInventoryLayer.GetWidth() - 5, 0)
				self.minBtn.SetPosition(self.minBtn.GetWidth() + 3, 15)

			for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
				slotNumber = item.BELT_INVENTORY_SLOT_START + i
				wndBeltInventorySlot.SetCoverButton(slotNumber,	"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/quest/slot_button_01.sub",\
												"d:/ymir work/ui/game/belt_inventory/slot_disabled.tga", False, False)

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndBeltInventorySlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndBeltInventorySlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndBeltInventorySlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlotNew))
		wndBeltInventorySlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlotNew))
		wndBeltInventorySlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndBeltInventorySlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

		self.wndBeltInventorySlot = wndBeltInventorySlot

	def ReturnSlots(self):
		getItemVNum=player.GetItemIndex
		for i in xrange(player.NEW_EQUIPMENT_SLOT_COUNT):
			slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
			vnum = getItemVNum(slotNumber)

			if vnum != 0:
				item.SelectItem(vnum)
				if item.GetItemType() == item.ITEM_TYPE_BELT and item.GetItemType() != item.ITEM_TYPE_COSTUME:
					return item.GetValue(0), vnum

		return 0, 0

	def ReturnCountSlot(self):
		value0, vnum = self.ReturnSlots()
		list = {
			7: 16,
			6: 12,
			5: 9,
			4: 6,
			3: 4,
			2: 2,
			1: 1,
			0:0,
		}
		if vnum != 0:
			if list.has_key(value0):
				# dbg.TraceError("VNUM: "+str(vnum)+" Value0: "+str(value0)+ " Slots desbloquear: "+str(list[value0]))
				return list[value0]
		return 0

	def RefreshSlot(self):
		getItemVNum=player.GetItemIndex
		# slots = self.ReturnCountSlot()

		table = [
			1,2,4,6,
			3,3,4,6,
			5,5,5,6,
			7,7,7,7,
		]
		table2 = []
		
		value0, vnum = self.ReturnSlots()
		for i in xrange(len(table)):
			if value0 >= table[i]:
				table2.append(1)
			else:
				table2.append(0)

		for i in xrange(item.BELT_INVENTORY_SLOT_COUNT):
			slotNumber = item.BELT_INVENTORY_SLOT_START + i
			self.wndBeltInventorySlot.SetItemSlot(slotNumber, getItemVNum(slotNumber), player.GetItemCount(slotNumber))
			self.wndBeltInventorySlot.SetAlwaysRenderCoverButton(slotNumber, True)

			if table2[i] == 1:
				self.wndBeltInventorySlot.EnableCoverButton(slotNumber)
			else:
				self.wndBeltInventorySlot.DisableCoverButton(slotNumber)

		self.wndBeltInventorySlot.RefreshSlot()

class NewGoldWindow(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.toolTip = uiToolTip.ToolTip()
		self.LoadDialog()
		
	
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def CheckIfICanOpen(self):
		if constInfo.NewGoldWindow == 1:
			self.Open()

	def Open(self):
		if not self.board.IsShow():
			self.board.Show()
			self.RefreshStatus()

	def CloseWithoutWindow(self):
		if self.board.IsShow():
			self.RefreshStatus()
			self.toolTip.Hide()
			self.board.Hide()

	def Close(self):
		if self.board.IsShow():
			self.RefreshStatus()
			self.toolTip.Hide()
			self.board.Hide()
			# constInfo.NewGoldWindow = 0

	def LoadDialog(self):
		self.boardsizex = 330-130

		self.board = ui.Board()
		self.board.SetPosition(wndMgr.GetScreenWidth()-self.boardsizex,wndMgr.GetScreenHeight()-100+30)
		self.board.SetSize(self.boardsizex, 50)
		self.board.Hide()
		
		self.currencies = [["02","locale/es/ui/itemshop/dr_icon.tga",3],["02","locale/es/ui/itemshop/coin_icon.tga",2]]
		
		self.obj = {}
		for i in xrange(len(self.currencies)):
			self.obj["slot"+str(i)] = ui.ImageBox()
			self.obj["slot"+str(i)].SetParent(self.board)
			self.obj["slot"+str(i)].LoadImage("d:/ymir work/ui/public/Parameter_Slot_"+self.currencies[i][0]+".sub")
			
			self.obj["icon"+str(i)] = ui.ImageBox()
			self.obj["icon"+str(i)].SetParent(self.obj["slot"+str(i)])
			self.obj["icon"+str(i)].SetPosition(-20, 2)
			self.obj["icon"+str(i)].LoadImage(self.currencies[i][1])

			if i > 0:
				sum = 0
				if i == 1:
					sum += (self.obj["icon"+str(i-1)].GetWidth() + self.obj["slot"+str(i-1)].GetWidth())
				elif i == 2:
					sum += (self.obj["icon"+str(i-1)].GetWidth() + self.obj["slot"+str(i-1)].GetWidth()) + (self.obj["icon"+str(i-2)].GetWidth() + self.obj["slot"+str(i-2)].GetWidth()) + 10
				self.obj["slot"+str(i)].SetPosition(self.board.GetWidth() - self.obj["slot"+str(i)].GetWidth() - 15 - (sum)-10, 10)
			else:
				self.obj["slot"+str(i)].SetPosition(self.board.GetWidth() - self.obj["slot"+str(i)].GetWidth() - 15, 10)

			self.obj["slot"+str(i)].Show()
			self.obj["icon"+str(i)].Show()
		
			self.obj["text"+str(i)] = ui.TextLine()
			self.obj["text"+str(i)].SetParent(self.obj["slot"+str(i)])
			self.obj["text"+str(i)].SetText("-1")
			self.obj["text"+str(i)].SetPosition(5, 2)
			self.obj["text"+str(i)].SetHorizontalAlignRight()
			self.obj["text"+str(i)].SetWindowHorizontalAlignRight()
			self.obj["text"+str(i)].Show()

	def OnUpdate(self):
		self.texts = [localeInfo.MONETARY_UNIT0,uiScriptLocale.VCOINS,uiScriptLocale.COINS]
		if self.obj["slot0"].IsIn():
			self.toolTip.ClearToolTip()
			self.toolTip.AppendTextLine(self.texts[1])
			self.toolTip.Show()
		elif self.obj["slot1"].IsIn():
			self.toolTip.ClearToolTip()
			self.toolTip.AppendTextLine(self.texts[2])
			self.toolTip.Show()
		else:
			self.toolTip.Hide()

	def RefreshStatus(self):
		for i in xrange(len(self.currencies)):
			if int(self.currencies[i][2]) == 1:
				self.obj["text"+str(i)].SetText(localeInfo.NumberToMoneyString(player.GetElk()))
			elif int(self.currencies[i][2]) == 2:
				self.obj["text"+str(i)].SetText(localeInfo.NumberToMoneyString(constInfo.COINS_DRS[0]).replace(" "+localeInfo.MONETARY_UNIT0, ""))
			elif int(self.currencies[i][2]) == 3:
				self.obj["text"+str(i)].SetText(localeInfo.NumberToMoneyString(constInfo.COINS_DRS[1]).replace(" "+localeInfo.MONETARY_UNIT0, ""))

	def Destroy(self):
		self.Close()

	def Show(self):
		if self.board.IsShow():
			self.board.Hide()
			constInfo.NewGoldWindow = 0
		else:
			constInfo.NewGoldWindow = 1
			self.board.Show()
			ui.ScriptWindow.Show(self)
			self.RefreshStatus()

class InventoryWindow(ui.ScriptWindow):
	liHighlightedItems = []

	USE_TYPE_TUPLE = ("USE_SPECIAL", "USE_CLEAN_SOCKET", "USE_CHANGE_ATTRIBUTE", "USE_CHANGE_ATTRIBUTE2", "USE_ADD_ATTRIBUTE", "USE_ADD_ATTRIBUTE2", "USE_ADD_ACCESSORY_SOCKET", "USE_PUT_INTO_ACCESSORY_SOCKET", "USE_PUT_INTO_BELT_SOCKET", "USE_PUT_INTO_RING_SOCKET", "USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR")

	if app.ENABLE_AURA_SYSTEM:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_PUT_INTO_AURA_SOCKET"])

	if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
		USE_TYPE_TUPLE += ("USE_SET_CUSTOM_ATTRIBUTE",)

	if app.ELEMENT_SPELL_WORLDARD:
		spell_elements = list(USE_TYPE_TUPLE)
		spell_elements.append("USE_ELEMENT_UPGRADE")
		spell_elements.append("USE_ELEMENT_DOWNGRADE")
		spell_elements.append("USE_ELEMENT_CHANGE")
		USE_TYPE_TUPLE = tuple(spell_elements)

	NORMAL_TYPE = 0
	UPGRADE_TYPE = 1
	BOOK_TYPE = 2
	STONE_TYPE = 3
	CHANGE_TYPE = 4
	COSTUME_TYPE = 5

	SLOT_WINDOW_TYPE = {
		NORMAL_TYPE		:	{"name": uiScriptLocale.STORAGE_0, "window" : player.INVENTORY, 		"slot" : player.SLOT_TYPE_INVENTORY},
		UPGRADE_TYPE	:	{"name": uiScriptLocale.STORAGE_1, "window" : player.UPGRADE_INVENTORY, "slot" : player.SLOT_TYPE_UPGRADE_INVENTORY},
		BOOK_TYPE		:	{"name": uiScriptLocale.STORAGE_2, "window" : player.BOOK_INVENTORY, 	"slot" : player.SLOT_TYPE_BOOK_INVENTORY},
		STONE_TYPE		:	{"name": uiScriptLocale.STORAGE_3, "window" : player.STONE_INVENTORY, 	"slot" : player.SLOT_TYPE_STONE_INVENTORY},
		CHANGE_TYPE		:	{"name": uiScriptLocale.STORAGE_4, "window" : player.CHANGE_INVENTORY, 	"slot" : player.SLOT_TYPE_CHANGE_INVENTORY},
		COSTUME_TYPE		:	{"name": uiScriptLocale.STORAGE_5, "window" : player.COSTUME_INVENTORY, 	"slot" : player.SLOT_TYPE_COSTUME_INVENTORY},
	}

	questionDialog = None
	tooltipItem = None
	wndCostume = None
	dlgPickMoney = None
	sellingSlotNumber = -1

	isLoaded = 0

	isOpenedCostumeWindowWhenClosingInventory = 0
	isOpenedBeltWindowWhenClosingInventory = 0
	
	if app.ENABLE_EXPANDED_MONEY_TASKBAR:
		wndExpandedMoneyBar = None
	if app.ENABLE_GEM_SYSTEM:
		wndGem = None

	interface = None
	if app.WJ_ENABLE_TRADABLE_ICON:
		bindWnds = []

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isOpenedBeltWindowWhenClosingInventory = 0		# 인벤토리 닫을 때 벨트 인벤토리가 열려있었는지 여부-_-; 네이밍 ㅈㅅ

		self.wndItem = None
		self.categoryPageIndex = 0
		self.inventoryPageIndex = 0
		self.ChangeEquipIndex = 0
		self.grid = ui.Grid(width = 5, height = (9*4))
		if app.ENABLE_SASH_SYSTEM:
			self.listAttachedSashs = []
		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.elemets_hide = []
		
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		ui.ScriptWindow.Show(self)
		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			self.wndCostume.Show()

		#if self.wndBelt:
			#self.wndBelt.Show(self.isOpenedBeltWindowWhenClosingInventory)
		
		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Show()

	def BindInterfaceClass(self, interface):
		self.interface = interface

	if app.WJ_ENABLE_TRADABLE_ICON:
		def BindWindow(self, wnd):
			self.bindWnds.append(wnd)

	def __LoadWindow(self):

		try:
			pyScrLoader = ui.PythonScriptLoader()

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindowEx.py")
 			else:
				if ITEM_MALL_BUTTON_ENABLE:
					pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
				else:
					pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			
			if app.ENABLE_RARITY:
				wndItem.AppendRequirementSignImage("d:/ymir work/ui/game/rarity/broken_item.tga")
				wndEquip.AppendRequirementSignImage("d:/ymir work/ui/game/rarity/broken_item.tga")
			
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.wndBoard = self.GetChild("board")
			self.wndMoney = self.GetChild("Money")
			self.wndMoneySlot = self.GetChild("Money_Slot")
			
			if app.ENABLE_EXPANDED_MONEY_TASKBAR:
				self.wndMoneyIcon = self.GetChild("Money_Icon")
				self.wndMoneyIcon.Hide()
				self.wndMoneySlot.Hide()

				## l?E 조R?
				height = self.GetHeight()
				width = self.GetWidth()
				self.SetSize(width, height - 22)
				self.GetChild("board").SetSize(width, height - 22)

			else:
				self.wndMoneyIcon = self.GetChild("Money_Icon")
				self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_in", 0)
				self.wndMoneyIcon.SetEvent(ui.__mem_func__(self.EventProgress), "mouse_over_out", 0)
				self.toolTip = uiToolTip.ToolTip()
				self.toolTip.ClearToolTip()
				
			#self.wndMoneyIcon = self.GetChild("Money_Icon")
			self.DSSButton = self.GetChild2("DSSButton")

			#self.change_equip = self.GetChild("ChangeEquipment")

			#self.change_equip_buttons = []
			#for x in xrange(1,player.CHANGE_EQUIP_PAGE_EXTRA+2):
			#	self.change_equip_buttons.append(self.GetChild("Change_Equip_Tab_0%d"%x))

			self.inventoryTab = []
			for i in xrange(player.INVENTORY_PAGE_COUNT):
				self.inventoryTab.append(self.GetChild("Inventory_Tab_%02d" % (i+1)))

			self.equipmentTab = []
			self.equipmentTab.append(self.GetChild("Equipment_Tab_01"))
			self.equipmentTab.append(self.GetChild("Equipment_Tab_02"))

			#self.ChangeEquipButton = self.GetChild("ChangeEquipButton")

			self.GetChild("CostumeButton").SetEvent(self.OpenCostumeWindow)
			self.GetChild("NewInvButton").SetEvent(self.OpenNewStorage)
			self.GetChild("OfflineShopButton").SetEvent(self.OfflineShopButton)
			self.nowyButton1 = self.GetChild2("Button1")
			self.nowyButton2 = self.GetChild2("Button2")
			self.nowyButton3 = self.GetChild2("Button3")
			self.nowyButton4 = self.GetChild2("Button4")
			self.nowyButton5 = self.GetChild2("Button5")
			self.nowyButton6 = self.GetChild2("Button6")
			self.nowyButton7 = self.GetChild2("Button7")
			self.nowyButton8 = self.GetChild2("Button8")
			self.nowyButton9 = self.GetChild2("Button9")
			self.nowyButton10 = self.GetChild2("Button10")

			# Belt Inventory Window
			#self.wndBelt = None

			#if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
				#self.wndBelt = BeltInventoryWindow(self)

		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlotNew))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlotNew))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		
		if app.ENABLE_HIDE_COSTUME_SYSTEM:
			self.elemets_world = {}
			self.elemets_world["hide_button_3"] = ui.Button()
			self.elemets_world["hide_button_3"].SetParent(self.GetChild("Equipment_Base"))
			self.elemets_world["hide_button_3"].SetPosition(110, 0)
			self.elemets_world["hide_button_3"].SetUpVisual("Modulo/HideCostume/button_show_0.tga")
			self.elemets_world["hide_button_3"].SetOverVisual("Modulo/HideCostume/button_show_1.tga")
			self.elemets_world["hide_button_3"].SetDownVisual("Modulo/HideCostume/button_show_0.tga")
			self.elemets_world["hide_button_3"].SetEvent(self.FuncHide, 3)
			self.elemets_world["hide_button_3"].Hide()

		#self.change_equip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlotNew))
		#self.change_equip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlotNew))
		##self.change_equip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlotNew))
		##self.change_equip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlotNew))
		#self.change_equip.SetOverInItemEvent(ui.__mem_func__(self.OverInItemNew))
		#self.change_equip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItemNew))

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.Hide()

		## RefineDialog
		self.refineDialog = uiRefine.RefineDialog()
		self.refineDialog.Hide()

		## AttachMetinDialog
		if app.WJ_ENABLE_TRADABLE_ICON:  
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog(self)
			self.BindWindow(self.attachMetinDialog)
		else:
			self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()

		self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		for i in xrange(player.INVENTORY_PAGE_COUNT):
			self.inventoryTab[i].SetEvent(lambda arg=i: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()

		self.equipmentTab[0].SetEvent(lambda arg=0: self.SetEquipmentPage(arg))
		self.equipmentTab[1].SetEvent(lambda arg=1: self.SetEquipmentPage(arg))
		self.equipmentTab[0].Down()
		self.equipmentTab[0].Hide()
		self.equipmentTab[1].Hide()

		self.wndItem = wndItem
		self.wndEquip = wndEquip
		self.dlgPickMoney = dlgPickMoney

		if self.DSSButton:
			self.DSSButton.SetEvent(ui.__mem_func__(self.ClickDSSButton))

		if self.nowyButton1:
			self.nowyButton1.SetEvent(ui.__mem_func__(self.OpenNewStorage3))

		if self.nowyButton2:
			self.nowyButton2.SetEvent(ui.__mem_func__(self.OpenNewStorage1))

		if self.nowyButton3:
			self.nowyButton3.SetEvent(ui.__mem_func__(self.OpenNewStorage2))

		if self.nowyButton4:
			self.nowyButton4.SetEvent(ui.__mem_func__(self.OpenNewStorage10))

		if self.nowyButton5:
			self.nowyButton5.SetEvent(ui.__mem_func__(self.OpenNewStorage4))

		if self.nowyButton6:
			self.nowyButton6.SetEvent(ui.__mem_func__(self.OpenNewStorage6))

		if self.nowyButton7:
			self.nowyButton7.SetEvent(ui.__mem_func__(self.OpenNewStorage7))

		if self.nowyButton8:
			self.nowyButton8.SetEvent(ui.__mem_func__(self.OpenNewStorage5))

		if self.nowyButton9:
			self.nowyButton9.SetEvent(ui.__mem_func__(self.OpenNewStorage8))

		self.wndCostume = None

		if app.__RENEWAL_BRAVE_CAPE__:
			self.wndBraveCape = None

		## inventory locked
		self.lock, self.lock2, u, e = {}, {}, 0, 0
		for i in xrange(18):
			self.lock[i] = ui.Button()
			self.lock[i].SetParent(self.wndItem)
			if i >= 9:
				self.lock[i].SetPosition(0,0+e)
				e+=32
			else:
				self.lock[i].SetPosition(0,0+u)
			self.lock[i].SetUpVisual("d:/ymir work/drakon2/inventory/0.tga")
			self.lock[i].SetOverVisual("d:/ymir work/drakon2/inventory/0.tga")
			self.lock[i].SetDownVisual("d:/ymir work/drakon2/inventory/0.tga")
			self.lock[i].SetEvent(lambda x=i: self.ClickUnlockInventory(x))
			self.lock[i].Hide()

			u+=32

		if app.__RENEWAL_BRAVE_CAPE__:
			disbandBtn = ui.Button()
			disbandBtn.SetParent(self)
			disbandBtn.SetPosition(0, 220)
			disbandBtn.SetUpVisual("d:/ymir work/ui/game/belt_inventory/btn_expand_normal.tga")
			disbandBtn.SetOverVisual("d:/ymir work/ui/game/belt_inventory/btn_expand_over.tga")
			disbandBtn.SetDownVisual("d:/ymir work/ui/game/belt_inventory/btn_expand_down.tga")
			disbandBtn.SAFE_SetEvent(self.ClickBraveCape)
			disbandBtn.Show()
			self.disbandBtn = disbandBtn

			self.wndBraveCape = BraveCapeWindow()
			self.OnMoveWindow(*self.GetGlobalPosition())

		self.SetInventoryPage(0)
		self.SetCategoryPage(0)
		self.SetEquipmentPage(0)
		#self.SetChangeEquipPage(0)
		self.RefreshItemSlot()
		self.RefreshStatus()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def FuncHide(self,index):
			net.SendChatPacket("/costume_hide %d" %index)

		def costume_hide_load2(self):
			self.elemets_hide = self.get_costume_hide_list()
			
			for i in xrange(self.GetSlotCount()):
				if not i == 3:
					continue
				
				if len(self.elemets_hide) > 0:
					self.elemets_world["hide_button_%d"%self.elemets_hide[i][0]].SetUpVisual("Modulo/HideCostume/button_%s_0.tga"%self.ButtonInfoHide(self.elemets_hide[i][1]))
					self.elemets_world["hide_button_%d"%self.elemets_hide[i][0]].SetOverVisual("Modulo/HideCostume/button_%s_1.tga"%self.ButtonInfoHide(self.elemets_hide[i][1]))
					self.elemets_world["hide_button_%d"%self.elemets_hide[i][0]].SetDownVisual("Modulo/HideCostume/button_%s_0.tga"%self.ButtonInfoHide(self.elemets_hide[i][1]))
				self.elemets_world["hide_button_%d"%i].Show()

		def ButtonInfoHide(self,index):
			if index == 0:
				return "show"
			return "hide"

		def GetSlotCount(self):
			return len(self.elemets_world["position"]) if self.elemets_world.has_key("position") else 0

			slot_total = 2
			if app.ENABLE_HIDE_COSTUME_SYSTEM_ACCE:
				slot_total += 1
			if app.ENABLE_HIDE_COSTUME_SYSTEM_WEAPON_COSTUME:
				slot_total += 1
			slot_total += 3
			return slot_total

	if app.__RENEWAL_BRAVE_CAPE__:
		def ClickBraveCape(self):
			if self.wndBraveCape:
				if self.wndBraveCape.IsShow():
					self.wndBraveCape.Close()
				else:
					self.wndBraveCape.Open()

	def OnMoveWindow(self, x, y):
		if app.__RENEWAL_BRAVE_CAPE__:
			if self.wndBraveCape:
				self.wndBraveCape.AdjustPosition(x, y)

	def OpenCostumeWindow(self):
		self.ClickCostumeButton()

	def OpenNewStorage(self):
		interface = constInfo.GetInterfaceInstance()
		if interface == None:
			return
		interface.ToggleInventoryNewWindow()

	def OpenNewStorage1(self):
		self.interface.OpenTrackWindow()

	def OpenNewStorage2(self):
		self.interface.OpenBiologWindow()

	def OpenNewStorage3(self):
		self.interface.ToggleSwitchbotWindow()

	def OpenNewStorage4(self):
		self.interface.OpenBattlePass()

	def OpenNewStorage5(self):
		self.interface.OpenPrivateShopSearch()

	def OpenNewStorage6(self):
		self.interface.BuffNPCOpenWindow()

	def OpenNewStorage7(self):
		self.interface.OpenWikiWindow()

	def OpenNewStorage8(self):
		self.interface.ToggleThanosWindow()

	def OpenNewStorage10(self):
		self.interface.OpenWarpWindow()

	def OfflineShopButton(self):
		interface = constInfo.GetInterfaceInstance()
		if interface == None:
			return
		if interface.dlgOfflineShopPanel:
			if interface.dlgOfflineShopPanel.IsShow():
				interface.dlgOfflineShopPanel.CloseReal()
				return
		if interface.offlineShopBuilder:
			if interface.offlineShopBuilder.IsShow():
				interface.offlineShopBuilder.CloseReal()
				return
		net.SendOfflineShopButton()

	def SelectEmptySlotNew(self, selectedSlotPos):
		#if uiPrivateShopBuilder.IsBuildingPrivateShop():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
		#	return

		isAttached = mouseModule.mouseController.isAttached()
		index_change_equip = self.GetChangeEquipIndex()

		selectedSlotPos = player.CHANGE_EQUIP_SLOT_COUNT/player.CHANGE_EQUIP_PAGE_EXTRA*(index_change_equip-1) + (selectedSlotPos-player.CHANGE_EQUIP_SLOT_START)

		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()
			itemIndex = player.GetItemIndex(attachedSlotPos)
			itemCount = player.GetItemCount(attachedSlotPos)

			item.SelectItem(itemIndex)
			itemType = item.GetItemType()

			#if item.ITEM_TYPE_WEAPON == itemType or item.ITEM_TYPE_ARMOR == itemType :
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.INVENTORY, attachedSlotPos, player.CHANGE_EQUIP, selectedSlotPos, attachedCount)

	def SelectItemSlotNew(self, selectedSlotPos):
		#if uiPrivateShopBuilder.IsBuildingPrivateShop():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
		#	return

		isAttached = mouseModule.mouseController.isAttached()
		index_change_equip = self.GetChangeEquipIndex()
		selectedSlotPos = player.CHANGE_EQUIP_SLOT_COUNT/player.CHANGE_EQUIP_PAGE_EXTRA*(index_change_equip-1) + (selectedSlotPos-player.CHANGE_EQUIP_SLOT_START)
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()
			itemIndex = player.GetItemIndex(attachedSlotPos)
			itemCount = player.GetItemCount(attachedSlotPos)

			item.SelectItem(itemIndex)
			itemType = item.GetItemType()

			#if item.ITEM_TYPE_WEAPON == itemType or item.ITEM_TYPE_ARMOR == itemType :
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.INVENTORY, attachedSlotPos, player.CHANGE_EQUIP, selectedSlotPos, attachedCount)
		# else:
			# itemVnum = player.GetItemIndex(player.CHANGE_EQUIP, selectedSlotPos)
			# itemCount = player.GetItemCount(player.CHANGE_EQUIP, selectedSlotPos)
			# mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_CHANGE_EQUIP, selectedSlotPos, itemVnum, itemCount)

	def OverInItemNew(self,index):
		index_change_equip = self.GetChangeEquipIndex()
		index = player.CHANGE_EQUIP_SLOT_COUNT/player.CHANGE_EQUIP_PAGE_EXTRA*(index_change_equip-1) + (index-player.CHANGE_EQUIP_SLOT_START)

		if None != self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.SetInventoryItem(index,player.CHANGE_EQUIP)

	def OverOutItemNew(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def GetCategoryIndex(self):
		return self.categoryPageIndex

	def SetCategoryPage(self,index):
		self.categoryPageIndex = index
		for x in xrange(18):
			self.lock[x].SetUpVisual("d:/ymir work/drakon2/inventory/0.tga")
			self.lock[x].SetOverVisual("d:/ymir work/drakon2/inventory/0.tga")
			self.lock[x].SetDownVisual("d:/ymir work/drakon2/inventory/0.tga")
			self.lock[x].Show()

		self.RefreshItemSlot()

	def GetPageSizeCategory(self):
		if self.GetIsCategorySpecial():
			return player.SPECIAL_PAGE_SIZE
		return player.INVENTORY_PAGE_SIZE

	def GetPageCountCategory(self):
		if self.GetIsCategorySpecial():
			return 4
		return player.INVENTORY_PAGE_COUNT

	def GetIsCategorySpecial(self):
		#if self.GetUseItemSlotNew():
			#return False

		if self.categoryPageIndex <= 0:
			return False
		return True

	def __CustomeEvent(self):
		self.question = uiCommon.QuestionDialog()
		self.question.SetCenterPosition()
		self.question.SetText(uiScriptLocale.SORT_QUESTION)
		self.question.SetAcceptEvent(ui.__mem_func__(self.ClickSort))
		self.question.SetCancelEvent(ui.__mem_func__(self.NoOpenInventory))
		self.question.SetAcceptText(uiScriptLocale.YES)
		self.question.SetCancelText(uiScriptLocale.NO)
		self.question.Open()

	def ClickSort(self):
		#
		category = self.GetCategoryIndex()
		if category == 0:
			net.SendChatPacket("/click_sort_items")
		else:
			net.SendChatPacket("/click_sort_special_storage %d"%(category))
		self.question.Close()

	def ClickUnlockInventory(self, index):
		if index > constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())]:
			pass
		else:
			if constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())] <= 18:
				self.question = uiCommon.QuestionDialog()
				self.question.SetCenterPosition()
				self.question.SetText(uiScriptLocale.INVENTORY_UNLOCK % int((constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())]*2)+2))
				self.question.SetAcceptEvent(ui.__mem_func__(self.OpenInventory))
				self.question.SetCancelEvent(ui.__mem_func__(self.NoOpenInventory))
				self.question.SetAcceptText(uiScriptLocale.YES)
				self.question.SetCancelText(uiScriptLocale.NO)
				self.question.Open()

	def OpenInventory(self):
		if constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())] <= 18:
			net.SendChatPacket("/unlock_inventory %d"%(self.GetCategoryIndex()))
		self.question.Close()

	def NoOpenInventory(self):
		self.question.Close()
		
	def Destroy(self):
		self.ClearDictionary()
		if app.__RENEWAL_BRAVE_CAPE__:
			if self.wndBraveCape:
				self.wndBraveCape.Destroy()
				self.wndBraveCape = None
		self.grid.reset()
		self.grid=None

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0

		self.refineDialog.Destroy()
		self.refineDialog = 0

		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0
		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.dlgPickMoney = 0
		self.wndMoney = 0
		self.wndMoneySlot = 0
		self.questionDialog = None
		self.dlgQuestion = None
		self.ChangeEquipButton = None
		self.DSSButton = None
		self.interface = None
		if app.ENABLE_DSS_ACTIVE_EFFECT_BUTTON:
			self.DSSButtonEffect = None

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.bindWnds = []

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0

		#if self.wndBelt:
			#self.wndBelt.Destroy()
			#self.wndBelt = None

		self.inventoryTab = []
		self.equipmentTab = []
		if app.ENABLE_GEM_SYSTEM:
			self.wndGem = None
		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndExpandedMoneyBar = None

		self.Hide()

	#def ClickChangeEquip(self):
	#	index_change_equip = self.GetChangeEquipIndex()
	#	if index_change_equip != 0:
	#		net.SendChatPacket("/change_equip_wa %d"%(index_change_equip))
	#		self.SetChangeEquipPage(0)

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()			# 인벤토리 창이 닫힐 때 코스츔이 열려 있었는가?
			self.wndCostume.Close()

		#if self.wndBelt:
			#self.isOpenedBeltWindowWhenClosingInventory = self.wndBelt.IsOpeningInventory()		# 인벤토리 창이 닫힐 때 벨트 인벤토리도 열려 있었는가?
			#print "Is Opening Belt Inven?? ", self.isOpenedBeltWindowWhenClosingInventory
			#self.wndBelt.Close()

		if self.dlgPickMoney:
			self.dlgPickMoney.Close()
		
		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Close()

		wndMgr.Hide(self.hWnd)
		
				
	def Close(self):
		self.Hide()

		if app.__RENEWAL_BRAVE_CAPE__:
			if self.wndBraveCape:
				self.wndBraveCape.Close()

	if app.ENABLE_EXPANDED_MONEY_TASKBAR:
		def SetExpandedMoneyBar(self, wndBar):
			self.wndExpandedMoneyBar = wndBar
			if self.wndExpandedMoneyBar:
				self.wndMoneySlot = self.wndExpandedMoneyBar.GetMoneySlot()
				self.wndMoney = self.wndExpandedMoneyBar.GetMoney()
				if app.ENABLE_GEM_SYSTEM:
					self.wndGem = self.wndExpandedMoneyBar.GetGaya()
				if self.wndMoneySlot:
					self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

	def SetInventoryPage(self, page):
		self.inventoryPageIndex = page
		for i in xrange(player.INVENTORY_PAGE_COUNT):
			if i!=page:
				self.inventoryTab[i].SetUp()
		self.RefreshBagSlotWindow()

	def SetEquipmentPage(self, page):
		self.equipmentPageIndex = page
		self.equipmentTab[1-page].SetUp()
		self.RefreshEquipSlotWindow()

	#def SetChangeEquipPage(self,page):
	#	if page != 0:
	#		self.wndEquip.Hide()
	#		self.change_equip.Show()
	#	else:
	#		self.wndEquip.Show()
	#		self.change_equip.Hide()
	#
	#	self.ChangeEquipIndex = page
	#
	#	for x in self.change_equip_buttons:
	#		x.SetUp()
	#	self.change_equip_buttons[page].Down()
	#
	#	self.RefreshEquipSlotWindow()

	def GetChangeEquipIndex(self):
		return self.ChangeEquipIndex

	if app.ENABLE_DSS_ACTIVE_EFFECT_BUTTON:
		def UseDSSButtonEffect(self, enable):
			if self.DSSButton:
				DSSButtonEffect = ui.SlotWindow()
				DSSButtonEffect.AddFlag("attach")
				DSSButtonEffect.SetParent(self.DSSButton)
				DSSButtonEffect.SetPosition(3.2, 0)

				DSSButtonEffect.AppendSlot(0, 0, 0, 32, 32)
				DSSButtonEffect.SetRenderSlot(0)
				DSSButtonEffect.RefreshSlot()

				if enable == True:
					DSSButtonEffect.ActivateSlot(0)
					DSSButtonEffect.Show()
				else:
					DSSButtonEffect.DeactivateSlot(0)
					DSSButtonEffect.Hide()
				self.DSSButtonEffect = DSSButtonEffect
				
	# DSSButton
	def ClickDSSButton(self):
		print "click_dss_button"
		self.interface.ToggleDragonSoulWindow()

	def ClickCostumeButton(self):
		print "Click Costume Button"
		if self.wndCostume:
			if self.wndCostume.IsShow():
				self.wndCostume.Close()
			else:
				self.wndCostume.Open()
		else:
			self.wndCostume = CostumeWindow(self)
			self.wndCostume.Open()

	def OpenPickMoneyDialog(self):

		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_SAFEBOX == mouseModule.mouseController.GetAttachedType():

				if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

			mouseModule.mouseController.DeattachObject()

		else:
			curMoney = player.GetElk()

			if curMoney <= 0:
				return

			self.dlgPickMoney.SetTitleName(localeInfo.PICK_MONEY_TITLE)
			self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
			self.dlgPickMoney.Open(curMoney)
			self.dlgPickMoney.SetMax(9) # 인벤토리 990000 제한 버그 수정

	def OnPickMoney(self, money):
		mouseModule.mouseController.AttachMoney(self, player.SLOT_TYPE_INVENTORY, money)

	def OnPickItem(self, count):
		itemSlotIndex = self.dlgPickMoney.itemGlobalSlotIndex
		selectedItemVNum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],itemSlotIndex)
		mouseModule.mouseController.AttachObject(self, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"], itemSlotIndex, selectedItemVNum, count)

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if self.GetIsCategorySpecial():
			return self.inventoryPageIndex * player.SPECIAL_PAGE_SIZE + local

		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local
	
	def __InventoryLocalSlotPosToGlobalSlotPosWithPage(self, page, local):
		if self.GetIsCategorySpecial():
			return page * player.SPECIAL_PAGE_SIZE + local

		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		return page*player.INVENTORY_PAGE_SIZE + local
	
	
	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	if app.WJ_ENABLE_TRADABLE_ICON:
		def RefreshMarkSlots(self, localIndex=None):
			if not self.interface:
				return
			if not self.wndItem:
				return

			onTopWnd = self.interface.GetOnTopWindow()
			if localIndex:
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(localIndex)
				
				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				elif app.BL_67_ATTR and onTopWnd == player.ON_TOP_WND_ATTR_67:
					mark = (not self.interface.IsAttr67RegistItem() and not uiAttr67Add.Attr67AddWindow.CantAttachToAttrSlot(slotNumber, True)) or \
						(self.interface.IsAttr67RegistItem() and not self.interface.IsAttr67SupportItem() and not uiAttr67Add.Attr67AddWindow.IsSupportItem(slotNumber))

					if mark:
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

				return

			for i in xrange(player.INVENTORY_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

				if onTopWnd == player.ON_TOP_WND_NONE:
					self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SELL):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_EXCHANGE:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_GIVE):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_PRIVATE_SHOP:
					if player.IsAntiFlagBySlot(slotNumber, item.ITEM_ANTIFLAG_MYSHOP):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

				elif app.BL_67_ATTR and onTopWnd == player.ON_TOP_WND_ATTR_67:
					mark = (not self.interface.IsAttr67RegistItem() and not uiAttr67Add.Attr67AddWindow.CantAttachToAttrSlot(slotNumber, True)) or \
						(self.interface.IsAttr67RegistItem() and not self.interface.IsAttr67SupportItem() and not uiAttr67Add.Attr67AddWindow.IsSupportItem(slotNumber))

					if mark:
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot

		self.grid.reset()
		for j in xrange(4):
			for i in xrange(self.GetPageSizeCategory()):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPosWithPage(j,i)
				itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)
				if itemCount == 0:
					continue
				itemVnum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)
				if itemVnum == 0:
					continue
				item.SelectItem(itemVnum)
				(w, h) = item.GetItemSize()
				self.grid.put(slotNumber,w, h)

		for i in xrange(self.GetPageSizeCategory()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)
			# itemCount == 0이면 소켓을 비운다.
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotNumber)

			setItemVNum(i, itemVnum, itemCount)
			
			if not self.GetIsCategorySpecial():
				if itemVnum == 0 and slotNumber in self.liHighlightedItems:
					self.liHighlightedItems.remove(slotNumber)

			## 자동물약 (HP: #72723 ~ #72726, SP: #72727 ~ #72730) 특수처리 - 아이템인데도 슬롯에 활성화/비활성화 표시를 위한 작업임 - [hyo]
			if constInfo.IS_AUTO_POTION(itemVnum):
				# metinSocket - [0] : 활성화 여부, [1] : 사용한 양, [2] : 최대 용량
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				if slotNumber >= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
					slotNumber -= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex
				isActivated = 0 != metinSocket[0]

				if isActivated:
					self.wndItem.ActivateSlot(i)
					potionType = 0;
					if constInfo.IS_AUTO_POTION_HP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_HP
					elif constInfo.IS_AUTO_POTION_SP(itemVnum):
						potionType = player.AUTO_POTION_TYPE_SP
					
					usedAmount = int(metinSocket[1])
					totalAmount = int(metinSocket[2])
					if app.ENABLE_NEW_AUTOPOTION:
						if not constInfo.IS_NEW_AUTO_POTION(itemVnum):
							player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))
					else:
						player.SetAutoPotionInfo(potionType, isActivated, (totalAmount - usedAmount), totalAmount, self.__InventoryLocalSlotPosToGlobalSlotPos(i))

				else:
					self.wndItem.DeactivateSlot(slotNumber)

			else:
				self.wndItem.DeactivateSlot(slotNumber)


			if app.ENABLE_SASH_SYSTEM:
				slotNumberChecked = 0
				if not constInfo.IS_AUTO_POTION(itemVnum):
					self.wndItem.DeactivateSlot(i)
				
				for j in xrange(sash.WINDOW_MAX_MATERIALS):
					(isHere, iCell) = sash.GetAttachedItem(j)
					if isHere:
						if iCell == slotNumber:
							self.wndItem.ActivateSlot(i, (36.00 / 255.0), (222.00 / 255.0), (3.00 / 255.0), 1.0)
							if not slotNumber in self.listAttachedSashs:
								self.listAttachedSashs.append(slotNumber)
							
							slotNumberChecked = 1
					else:
						if slotNumber in self.listAttachedSashs and not slotNumberChecked:
							self.wndItem.DeactivateSlot(i)
							self.listAttachedSashs.remove(slotNumber)

			if itemVnum == 72501:
				metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
				isActivated = metinSocket[0]
				if isActivated == 1:
					self.wndItem.ActivateSlot(i)
				else:
					self.wndItem.DeactivateSlot(i)

			if app.ENABLE_RARITY:
				if item.IsRarityItem(itemVnum) and player.GetItemMetinSocket(slotNumber, item.RARITY_VALUE_INDEX) <= 0:
					self.wndItem.ShowRequirementSign(i)
				else:
					self.wndItem.HideRequirementSign(i)

			if app.NEW_PET_SYSTEM:
				if self.tooltipItem:
					pets = self.tooltipItem.GetPetList()
					for date in pets:
						if itemVnum == date[0]:
							metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
							isActivated = metinSocket[2]
							if isActivated:
								self.wndItem.ActivateSlot(i)
							else:
								self.wndItem.DeactivateSlot(i)

				mount  = self.tooltipItem.GetMountList()
				for date in mount:
					if itemVnum == date[0]:
						metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
						isActivated = metinSocket[2]
						if isActivated:
							self.wndItem.ActivateSlot(i)
						else:
							self.wndItem.DeactivateSlot(i)


			if app.WJ_ENABLE_TRADABLE_ICON:
				self.RefreshMarkSlots(i)

		#if not self.GetIsCategorySpecial():
		self.__RefreshHighlights()
		self.wndItem.RefreshSlot()

		#if self.wndBelt:
			#self.wndBelt.RefreshSlot()

		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)


	def HighlightSlot(self, slot):
		# import dbg
		# dbg.TraceError("slotIndex %d"%slot)
		if not slot in self.liHighlightedItems:
			self.liHighlightedItems.append(slot)
	
	def __RefreshHighlights(self):
		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
			if slotNumber in self.liHighlightedItems:
				self.wndItem.ActivateSlot(i)

	def RefreshEquipSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndEquip.SetItemSlot
		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			itemCount = getItemCount(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

			if app.ENABLE_RARITY:
				if item.IsRarityItem(player.GetItemIndex(slotNumber)) and player.GetItemMetinSocket(slotNumber, item.RARITY_VALUE_INDEX) <= 0:
					self.wndEquip.ShowRequirementSign(slotNumber)
				else:
					self.wndEquip.HideRequirementSign(slotNumber)

		if app.ENABLE_NEW_EQUIPMENT_SYSTEM:
			for i in xrange(player.NEW_EQUIPMENT_SLOT_COUNT):
				slotNumber = player.NEW_EQUIPMENT_SLOT_START + i
				itemCount = getItemCount(slotNumber)
				if itemCount <= 1:
					itemCount = 0

				setItemVNum(slotNumber, getItemVNum(slotNumber), itemCount)

				if app.ENABLE_RARITY:
					if item.IsRarityItem(player.GetItemIndex(slotNumber)) and player.GetItemMetinSocket(slotNumber, item.RARITY_VALUE_INDEX) <= 0:
						self.wndEquip.ShowRequirementSign(slotNumber)
					else:
						self.wndEquip.HideRequirementSign(slotNumber)

		#index_change_equip = self.GetChangeEquipIndex()
		#count = 0
		#if index_change_equip != 0:
		#	if index_change_equip > 1:
		#		index_old = player.CHANGE_EQUIP_SLOT_COUNT/player.CHANGE_EQUIP_PAGE_EXTRA*(index_change_equip-1)
		#	else:
		#		index_old = player.CHANGE_EQUIP_SLOT_COUNT-(player.CHANGE_EQUIP_SLOT_COUNT/index_change_equip)
		#
		#	for i in xrange(index_old ,player.CHANGE_EQUIP_SLOT_COUNT/player.CHANGE_EQUIP_PAGE_EXTRA*index_change_equip):
		#		slotNumber = player.CHANGE_EQUIP_SLOT_START + count
		#
		#		itemCount = player.GetItemCount(player.CHANGE_EQUIP,i)
		#		if itemCount <= 1:
		#			itemCount = 0
		#
		#
		#		self.change_equip.SetItemSlot(slotNumber, player.GetItemIndex(player.CHANGE_EQUIP,i), itemCount)
		#		count += 1
		
		#self.change_equip.RefreshSlot()
		self.wndEquip.RefreshSlot()

		#if self.wndBelt:
			#self.wndBelt.RefreshSlot()
			
		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def costume_hide_clear(self):
			self.elemets_hide = []

		def costume_hide_list(self,slot,index):
			self.elemets_hide.append([int(slot),int(index)])

		def costume_hide_load(self):
			if self.wndCostume:
				self.wndCostume.costume_hide_load()
				
			#self.costume_hide_load2()

		def get_costume_hide_list(self):
			return self.elemets_hide
			
	def RefreshItemSlot(self):
		self.RefreshStatus()
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def RefreshStatus(self):
		money = player.GetElk()
		self.wndMoney.SetText(localeInfo.NumberToMoneyString(money))
		if app.ENABLE_GEM_SYSTEM:
			if self.wndGem:
				self.wndGem.SetText(localeInfo.NumberToMoneyStringNEW(player.GetGem()))

	def OnUpdate(self):
		if constInfo.Inventory_Locked["Active"]:
			if constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())] >= 18:
				for i in xrange(18):
					self.lock[i].Hide()
			else:
				if self.inventoryPageIndex >= 2:
					self.lock[constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())]].SetUpVisual("d:/ymir work/drakon2/inventory/1.tga")
					self.lock[constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())]].SetOverVisual("d:/ymir work/drakon2/inventory/1.tga")
					self.lock[constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())]].SetDownVisual("d:/ymir work/drakon2/inventory/1.tga")

					for i in xrange(9):
						self.lock[i].Show()
						if constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())] > i:
							self.lock[i].Hide()
				else:
					for i in xrange(9):
						self.lock[i].Hide()
						
				if self.inventoryPageIndex == 3:
					self.lock[constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())]].SetUpVisual("d:/ymir work/drakon2/inventory/1.tga")
					self.lock[constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())]].SetOverVisual("d:/ymir work/drakon2/inventory/1.tga")
					self.lock[constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())]].SetDownVisual("d:/ymir work/drakon2/inventory/1.tga")

					for i in xrange(9,18):
						self.lock[i].Show()
						if constInfo.Inventory_Locked["Keys_Can_Unlock_%d"%(self.GetCategoryIndex())] > i:
							self.lock[i].Hide()
				else:
					for i in xrange(9,18):
						self.lock[i].Hide()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SellItem(self):
		if self.sellingSlotitemIndex == player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],self.sellingSlotNumber):
				## 용혼석도 팔리게 하는 기능 추가하면서 인자 type 추가
				net.SendShopSellPacketNew(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], self.sellingSlotNumber, self.questionDialog.count)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		#net.SendItemUseToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.__SendUseItemToItemPacket(self.questionDialog.sourceInv, self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def __OpenQuestionDialog(self, srcItemPos, dstItemPos):
		self.dlgQuestion = uiCommon.QuestionDialog2()

		self.dlgQuestion.SetAcceptEvent(lambda arg=srcItemPos, arg1=dstItemPos : self.__Accept(arg,arg1))
		self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.__Cancel))

		self.dlgQuestion.SetText1(localeInfo.DRAGON_SOUL_UNEQUIP_WARNING1)
		self.dlgQuestion.SetText2(localeInfo.DRAGON_SOUL_UNEQUIP_WARNING2)

		self.dlgQuestion.Open()

	def __Accept(self,srcItemPos,dstItemSlotPos):
		(attachedInvenType,attachedSlotPos) = srcItemPos
		(attachedInvenType1, selectedSlotPos, attachedCount) = dstItemSlotPos
		self.__SendMoveItemPacket(attachedInvenType, attachedSlotPos, attachedInvenType1, selectedSlotPos, attachedCount)
		self.dlgQuestion.Close()

	def __Cancel(self):
		self.dlgQuestion.Close()

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		if app.ENABLE_AURA_SYSTEM:
			if player.IsAuraRefineWindowOpen():
				return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if self.interface:
				if self.interface.GetPosChangeItemManual() != -1:
					if self.interface.GetPosChangeItemManual() == attachedSlotPos:
						mouseModule.mouseController.DeattachObject()
						return

			slot_type_list = [player.SLOT_TYPE_INVENTORY,player.SLOT_TYPE_UPGRADE_INVENTORY,player.SLOT_TYPE_BOOK_INVENTORY,player.SLOT_TYPE_STONE_INVENTORY,player.SLOT_TYPE_CHANGE_INVENTORY,player.SLOT_TYPE_COSTUME_INVENTORY]

			if attachedSlotType in slot_type_list:
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				itemCount = player.GetItemCount(attachedInvenType,attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				#self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				#if attachedInvenType == player.DRAGON_SOUL_INVENTORY:
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					srcItemPos = (attachedInvenType, attachedSlotPos)
					dstItemPos = (self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos, attachedCount)
					self.__OpenQuestionDialog(srcItemPos, dstItemPos)
				else:
					self.__SendMoveItemPacket(attachedInvenType, attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			# if player.SLOT_TYPE_CHANGE_EQUIP == attachedSlotType:
				# attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				# net.SendItemMovePacket(player.CHANGE_EQUIP, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

			elif app.ENABLE_SWITCHBOT and player.SLOT_TYPE_SWITCHBOT == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.SWITCHBOT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_BUFF_EQUIPMENT == attachedSlotType and app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.BUFF_EQUIPMENT, attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos, attachedCount)
				# net.SendItemMovePacket(player.BUFF_EQUIPMENT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:
				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")
				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif app.ENABLE_AURA_SYSTEM and player.SLOT_TYPE_AURA == attachedSlotType:
				net.SendAuraRefineCheckOut(attachedSlotPos, player.GetAuraRefineWindowType())

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		if self.interface:
			if self.interface.GetPosChangeItemManual() != -1:
				if self.interface.GetPosChangeItemManual() == itemSlotIndex:
					#mouseModule.mouseController.DeattachObject()
					return

		if app.IsPressed(app.DIK_LCONTROL):
			if self.interface and player.IsEquipmentSlot(itemSlotIndex) == 0 and self.interface.AttachInvenItemToOtherWindowSlot(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex):
				return

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_STONE_INVENTORY == attachedSlotType or player.SLOT_TYPE_CHANGE_INVENTORY == attachedSlotType or player.SLOT_TYPE_UPGRADE_INVENTORY == attachedSlotType or player.SLOT_TYPE_BOOK_INVENTORY == attachedSlotType or player.SLOT_TYPE_COSTUME_INVENTORY == attachedSlotType:
					self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedInvenType, attachedSlotPos, itemSlotIndex, attachedSlotType)
			else:
				if player.SLOT_TYPE_INVENTORY == attachedSlotType:
					self.__DropSrcItemToDestItemInInventory(attachedItemVID, attachedInvenType, attachedSlotPos, itemSlotIndex, attachedSlotType)

			mouseModule.mouseController.DeattachObject()
		else:
			if self.interface:
				if self.interface.GetPosChangeItemManual() != -1:
					if self.interface.GetPosChangeItemManual() == itemSlotIndex:
						return

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			elif app.IsCanOpenRender() and app.ENABLE_RENDER_TARGET:
				self.interface.OpenRenderTargetWindow(0, player.GetItemIndex(itemSlotIndex))

			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(app.DIK_LSHIFT):
				itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],itemSlotIndex)

				if itemCount > 1:
					self.dlgPickMoney.SetTitleName(localeInfo.PICK_ITEM_TITLE)
					self.dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickItem))
					self.dlgPickMoney.Open(itemCount)
					self.dlgPickMoney.itemGlobalSlotIndex = itemSlotIndex
				#else:
					#selectedItemVNum = player.GetItemIndex(itemSlotIndex)
					#mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum)

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],itemSlotIndex)

				if not self.GetIsCategorySpecial():
					if True == item.CanAddToQuickSlotItem(itemIndex):
						player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)
			else:
				selectedItemVNum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],itemSlotIndex)
				itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["slot"], itemSlotIndex, selectedItemVNum, itemCount)

				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.wndItem.SetUseMode(True)
				else:
					self.wndItem.SetUseMode(False)

				snd.PlaySound("sound/ui/pick.wav")

	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemInv, srcItemSlotPos, dstItemSlotPos, attachedSlotType):
		if app.ENABLE_AURA_SYSTEM and player.IsAuraRefineWindowOpen():
			return

		destItemVnum = player.GetItemIndex(dstItemSlotPos)
		item.SelectItem(destItemVnum)
		destItemType = item.GetItemType()
		destItemSubType = item.GetItemSubType()

		if app.ENABLE_SPECIAL_STORAGE:
			if srcItemSlotPos == dstItemSlotPos and (attachedSlotType != player.SLOT_TYPE_STONE_INVENTORY and attachedSlotType != player.SLOT_TYPE_CHANGE_INVENTORY):
				return

			if srcItemSlotPos == dstItemSlotPos and item.IsMetin(srcItemVID) and self.GetIsCategorySpecial() and attachedSlotType == player.SLOT_TYPE_STONE_INVENTORY:
				return

			if srcItemSlotPos == dstItemSlotPos and item.GetUseType(srcItemVID) == "USE_CHANGE_ATTRIBUTE" and self.GetIsCategorySpecial() and attachedSlotType == player.SLOT_TYPE_CHANGE_INVENTORY:
				return

		else:
			if srcItemSlotPos == dstItemSlotPos:
				return

		if app.ENABLE_RARITY_REFINE and (srcItemVID >= 25050 and srcItemVID <= 25057) and item.IsRarityItem(destItemVnum) == True:
			rarityType = item.GetSocket(item.RARITY_TYPE_INDEX)
			if rarityType < 5:
				self.__SendUseItemToItemPacket(srcItemInv, srcItemSlotPos, dstItemSlotPos)
			return

		if app.ENABLE_RARITY:
			if item.IsRarityItem(destItemVnum):
				if srcItemVID >= 6880 and srcItemVID <= 6884:
					self.questionDialog = uiCommon.QuestionDialog()
					self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM % item.GetItemName())
					self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemToItemQuestionDialog_OnAccept))
					self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
					self.questionDialog.Open()
					self.questionDialog.srcItemSlotPos = srcItemSlotPos
					self.questionDialog.dstItemSlotPos = dstItemSlotPos
					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
					return
	
		# cyh itemseal 2013 11 08
		if app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemInv, srcItemSlotPos, dstItemSlotPos)

		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemInv, srcItemSlotPos, dstItemSlotPos)
			self.wndItem.SetUseMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemInv, srcItemSlotPos, dstItemSlotPos)

		
		elif destItemType == item.ITEM_TYPE_PET and destItemSubType == item.PET_LEVELABLE:
			if srcItemVID == 55008:
				self.interface.OpenChangeNameWindow(srcItemSlotPos,dstItemSlotPos,destItemVnum, 1)
			elif srcItemVID == 72325:
				self.DetachMetinFromItem(srcItemInv,srcItemSlotPos, dstItemSlotPos)
			elif (srcItemVID == 55001 or srcItemVID == 55033 or (srcItemVID >= 55010 and srcItemVID <= 55031)):
				self.questionDialog = uiCommon.QuestionDialog()
				if 55001 == srcItemVID:
					self.questionDialog.SetText(localeInfo.PET_PROTEIN_QUESTION_TEXT)
				elif 55033 == srcItemVID:
					self.questionDialog.SetText(localeInfo.PET_REMOVE_QUESTION_TEXT)
				else:
					self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM % item.GetItemName())
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemToItemQuestionDialog_OnAccept))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
				self.questionDialog.Open()
				self.questionDialog.srcItemSlotPos = srcItemSlotPos
				self.questionDialog.dstItemSlotPos = dstItemSlotPos
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemInv,srcItemSlotPos, dstItemSlotPos)

		elif app.ELEMENT_SPELL_WORLDARD and item.IsElement(srcItemVID):
			self.ElementItem(srcItemInv,srcItemSlotPos,dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemInv, srcItemSlotPos, dstItemSlotPos)

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemInv, srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemInv, srcItemSlotPos, dstItemSlotPos, srcItemVID)

		else:
			#snd.PlaySound("sound/ui/drop.wav")

			## 이동시킨 곳이 장착 슬롯일 경우 아이템을 사용해서 장착 시킨다 - [levites]

			if app.THANOS_GLOVE:
				if srcItemVID == 500007:
					if player.GetItemIndex(dstItemSlotPos) >= 500001 and player.GetItemIndex(dstItemSlotPos) <= 500006:
						self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

			if player.IsEquipmentSlot(dstItemSlotPos):

				## 들고 있는 아이템이 장비일때만
				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			elif self.CheckCrystalTime(player.GetItemIndex(srcItemSlotPos), player.GetItemIndex(dstItemSlotPos)) and app.__RENEWAL_CRYSTAL__:
				self.__SendUseItemToItemPacket(srcItemInv, srcItemSlotPos, dstItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
				#net.SendItemMovePacket(srcItemSlotPos, dstItemSlotPos, 0)

				net.SendItemMovePacket(srcItemInv, srcItemSlotPos, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], dstItemSlotPos, 0)

				#self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
				#return
				#net.SendItemMovePacket(srcItemSlotPos, dstItemSlotPos, 0)

	def __SellItem(self, itemSlotPos):
		if not player.IsEquipmentSlot(itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],itemSlotPos)
			itemCount = player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],itemSlotPos)


			self.sellingSlotitemIndex = itemIndex
			self.sellingSlotitemCount = itemCount

			item.SelectItem(itemIndex)
			## 안티 플레그 검사 빠져서 추가
			## 20140220
			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				#itemPrice = itemCount / itemPrice / 5
				itemPrice = itemCount / itemPrice
			else:
				#itemPrice = itemPrice * itemCount / 5
				itemPrice = itemPrice * itemCount

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def __OnClosePopupDialog(self):
		self.pop = None

	if app.ELEMENT_SPELL_WORLDARD:
		def ElementItem(self, srcInv, srcItemSlotPos,dstItemSlotPos):
			itemElement = player.GetItemIndex(srcInv, srcItemSlotPos)

			if player.ELEMENT_UPGRADE_CANT_ADD == player.GetElements(itemElement,dstItemSlotPos) or\
				player.ELEMENT_DOWNGRADE_CANT_ADD == player.GetElements(itemElement,dstItemSlotPos) or\
				player.ELEMENT_CANT_WORLDARD == player.GetElements(itemElement,dstItemSlotPos) or\
				player.ELEMENT_CHANGE_CANT_ADD == player.GetElements(itemElement,dstItemSlotPos):
				chat.AppendChat(chat.CHAT_TYPE_INFO, "No se puede realizar esta funcion.")
				return

			self.__SendUseItemToItemPacket(srcInv, srcItemSlotPos, dstItemSlotPos)

	def RefineItem(self, scrollInv, scrollSlotPos, targetSlotPos):

		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if app.ENABLE_MULTI_REFINE_WORLDARD:
			if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos) and self.CheckVnumMultiRefine(targetIndex) == False:
				return
		else:
			if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
				return

		if app.ENABLE_REFINE_RENEWAL:
			constInfo.AUTO_REFINE_TYPE = 1
			constInfo.AUTO_REFINE_DATA["ITEM"][0] = scrollSlotPos
			constInfo.AUTO_REFINE_DATA["ITEM"][1] = targetSlotPos

		###########################################################
		self.__SendUseItemToItemPacket(scrollInv, scrollSlotPos, targetSlotPos)
		#net.SendItemUseToItemPacket(scrollSlotPos, targetSlotPos)
		return
		###########################################################

		###########################################################
		#net.SendRequestRefineInfoPacket(targetSlotPos)
		#return
		###########################################################

		result = player.CanRefine(scrollIndex, targetSlotPos)

		if player.REFINE_ALREADY_MAX_SOCKET_COUNT == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_MORE_SOCKET)

		elif player.REFINE_NEED_MORE_GOOD_SCROLL == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NEED_BETTER_SCROLL)

		elif player.REFINE_CANT_MAKE_SOCKET_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_SOCKET_DISABLE_ITEM)

		elif player.REFINE_NOT_NEXT_GRADE_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_UPGRADE_DISABLE_ITEM)

		elif player.REFINE_CANT_REFINE_METIN_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.REFINE_OK != result:
			return

		self.refineDialog.Open(scrollSlotPos, targetSlotPos)

	def DetachMetinFromItem(self, scroolInv, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scroolInv, scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)
		if app.ENABLE_SASH_SYSTEM:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == sash.CLEAN_ATTR_VALUE0:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SASH_FAILURE_CLEAN)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				
				return
		else:
			if not player.CanDetach(scrollIndex, targetSlotPos):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
				return
		
		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.SetText(localeInfo.REFINE_DO_YOU_SEPARATE_METIN)
		if app.ENABLE_SASH_SYSTEM:
			item.SelectItem(targetIndex)
			if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_SASH:
				item.SelectItem(scrollIndex)
				if item.GetValue(0) == sash.CLEAN_ATTR_VALUE0:
					self.questionDialog.SetText(localeInfo.SASH_DO_YOU_CLEAN)
		
		self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
		self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		self.questionDialog.Open()
		self.questionDialog.sourceInv = scroolInv
		self.questionDialog.sourcePos = scrollSlotPos
		self.questionDialog.targetPos = targetSlotPos

	def AttachMetinToItem(self, metinInv, metinSlotPos, targetSlotPos):
		metinIndex = player.GetItemIndex(metinInv, metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinInv, metinSlotPos, targetSlotPos)

	def OverOutItem(self):
		if self.wndCostume:
			self.wndCostume.SetOverOutEvent2()
		if self.wndItem:
			self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		if self.wndCostume:
			self.wndCostume.SetOverOutEvent2()
		
		overSlotPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		if self.wndItem:
			self.wndItem.SetUsableItem(False)

		if not self.GetIsCategorySpecial():
			if overSlotPosGlobal in self.liHighlightedItems:
				self.liHighlightedItems.remove(overSlotPosGlobal)
				self.wndItem.DeactivateSlot(overSlotPos)
				
		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if app.ENABLE_SPECIAL_STORAGE:
				if player.SLOT_TYPE_INVENTORY == attachedItemType or player.SLOT_TYPE_STONE_INVENTORY == attachedItemType or player.SLOT_TYPE_CHANGE_INVENTORY == attachedItemType:
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

					if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
						self.wndItem.SetUsableItem(True)
						self.wndItem.SetUseMode(True)
						#self.ShowToolTip(overSlotPos)
						self.ShowToolTip(overSlotPosGlobal)
						return
			else:
				if player.SLOT_TYPE_INVENTORY == attachedItemType:

					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

					if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPos):
						self.wndItem.SetUsableItem(True)
						self.ShowToolTip(overSlotPosGlobal)
						#self.ShowToolTip(overSlotPos)
						return

		self.ShowToolTip(overSlotPosGlobal)


	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		"다른 아이템에 사용할 수 있는 아이템인가?"

		if app.THANOS_GLOVE:
			if srcItemVNum == 500007:
				return TRUE

		if app.ENABLE_RARITY:
			if srcItemVNum >= 6880 and srcItemVNum <= 6884:
				return True

		if app.ENABLE_RARITY_REFINE:
			if srcItemVNum >= 25050 and srcItemVNum <= 25057:
				return True

		if item.IsRefineScroll(srcItemVNum):
			return True
		elif app.ENABLE_SOULBIND_SYSTEM and (item.IsSealScroll(srcItemVNum) or item.IsUnSealScroll(srcItemVNum)):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		if srcItemVNum >= 55701 and srcItemVNum <= 55704:
			return True
		if srcItemVNum == 71051 or srcItemVNum == 71052 or srcItemVNum == 90000:
			return True
		if srcItemVNum == 55001:
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif srcItemVNum >= 55701 and srcItemVNum <= 55715:
			return TRUE
		elif srcItemVNum == 55008:
			return TRUE
		elif srcItemVNum == 55001:
			return TRUE
		elif srcItemVNum == 55033:
			return TRUE
		elif srcItemVNum >= 55101 and srcItemVNum <= 55121:
			return TRUE
		elif srcItemVNum >= 55010 and srcItemVNum <= 55031:
			return TRUE
		elif app.ELEMENT_SPELL_WORLDARD and item.IsElement(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		elif self.CheckCrystalTime(srcItemVNum, player.GetItemIndex(srcSlotPos)):
			return True	
		else:
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True

		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		itemIndex = player.GetItemIndex(dstSlotPos)
		item.SelectItem(itemIndex)
		destItemType = item.GetItemType()
		destItemSubType = item.GetItemSubType()

		if app.ENABLE_SPECIAL_STORAGE:
			#if srcSlotPos == dstSlotPos and not item.IsMetin(srcItemVNum):
			if srcSlotPos == dstSlotPos and (not item.IsMetin(srcItemVNum) and item.GetUseType(srcItemVNum) != "USE_CHANGE_ATTRIBUTE"):
				return False
			if item.IsMetin(srcItemVNum):
				return True
		else:
			if srcSlotPos == dstSlotPos:
				return False

		if app.ENABLE_RARITY:
			if srcItemVNum >= 6880 and srcItemVNum <= 6884 and item.IsRarityItem(itemIndex) == True:
				return TRUE

		if app.ENABLE_RARITY_REFINE and (srcItemVNum >= 25050 and srcItemVNum <= 25057) and item.IsRarityItem(itemIndex) == True:
			rarityType = item.GetSocket(item.RARITY_TYPE_INDEX)
			if rarityType < 5:
				return True
			else:
				return False

		if srcItemVNum >= 55701 and  srcItemVNum <= 55704 and player.GetItemIndex(dstSlotPos) == 55002:			
			return True

		if srcItemVNum == 55001 and player.GetItemIndex(dstSlotPos) >= 55701 and player.GetItemIndex(dstSlotPos) <= 55704:			
			return True

		if srcItemVNum == 71051 or srcItemVNum == 71052 or srcItemVNum == 90000:
			return True

		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if item.IsRefineScroll(srcItemVNum):
			if app.__RENEWAL_CRYSTAL__:
				if self.CheckCrystalTime(srcItemVNum, player.GetItemIndex(dstSlotPos)):
					return True
			if app.ENABLE_MULTI_REFINE_WORLDARD:
				if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos) or self.CheckVnumMultiRefine(dstItemVNum) == True:
					return True
			else:
				if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
					return True

		elif destItemType == item.ITEM_TYPE_PET and destItemSubType == item.PET_LEVELABLE:
			if srcItemVNum == 55008:
				return TRUE
			elif srcItemVNum == 55001:
				return TRUE
			elif srcItemVNum == 55033:
				return TRUE
			elif srcItemVNum >= 55101 and srcItemVNum <= 55121:
				return TRUE
			elif srcItemVNum >= 55010 and srcItemVNum <= 55031:
				return TRUE

		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True
		elif app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVNum):
			if (item.IsSealScroll(srcItemVNum) and player.CanSealItem(dstSlotPos)) or (item.IsUnSealScroll(srcItemVNum) and player.CanUnSealItem(dstSlotPos)):
				return True
		elif app.ELEMENT_SPELL_WORLDARD and item.IsElement(srcItemVNum):
			if player.ELEMENT_UPGRADE_ADD == player.GetElements(srcItemVNum, dstSlotPos) or\
				player.ELEMENT_DOWNGRADE_ADD == player.GetElements(srcItemVNum, dstSlotPos) or\
				player.ELEMENT_CHANGE_ADD == player.GetElements(srcItemVNum, dstSlotPos):
				return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True

		else:

			useType = item.GetUseType(srcItemVNum)

			if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
				if "USE_SET_CUSTOM_ATTRIBUTE" == useType:
					if self.__CanSetCustomAttr(player.INVENTORY, dstSlotPos):
						return True

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos,srcItemVNum):
					return True
			elif app.BL_67_ATTR and "USE_CHANGE_ATTRIBUTE2" == useType:
				if self.__CanChangeItemAttrList2(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return True;
			elif "USE_PUT_INTO_BELT_SOCKET" == useType:
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum

				item.SelectItem(dstItemVNum)

				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True
			elif "USE_CHANGE_COSTUME_ATTR" == useType:
				if self.__CanChangeCostumeAttrList(dstSlotPos):
					return True
			elif "USE_RESET_COSTUME_ATTR" == useType:
				if self.__CanResetCostumeAttr(dstSlotPos):
					return True

			elif "USE_PUT_INTO_AURA_SOCKET" == useType and app.ENABLE_AURA_SYSTEM:
				dstItemVnum = player.GetItemIndex(dstSlotPos)
				item.SelectItem(dstItemVnum)
				if item.ITEM_TYPE_COSTUME == item.GetItemType() and item.COSTUME_TYPE_AURA == item.GetItemSubType():
					if player.GetItemMetinSocket(dstSlotPos, player.ITEM_SOCKET_AURA_BOOST) == 0:
						return True

		return False

	if app.ENABLE_MULTI_REFINE_WORLDARD:
		def CheckVnumMultiRefine(self,vnum):
			if len(constInfo.multi_refine_dates) != 0:
				for i in constInfo.multi_refine_dates:
					if i == vnum:
						return True

			return False

	if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
		def __CanSetCustomAttr(self, dstSlotWindow, dstSlotPos):
			dstItemVnum = player.GetItemIndex(dstSlotWindow, dstSlotPos)
			if dstItemVnum == 0:
				return False

			item.SelectItem(dstItemVnum)
			if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				return False

			if (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() == item.WEAPON_ARROW) or \
				(app.ENABLE_QUIVER_SYSTEM and item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() == item.WEAPON_QUIVER) or \
				(app.ENABLE_COSTUME_SYSTEM and app.ENABLE_ACCE_COSTUME_SYSTEM and item.GetItemSubType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_ACCE):
				return False

			attrCount = 0
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
					attrCount += 1

			if attrCount >= (player.ATTRIBUTE_SLOT_CUSTOM_MAX_NUM - 2):
				return True

			return False

	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.ITEM_TYPE_WEAPON != item.GetItemType():
			return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
				return True

		return False

	if app.BL_67_ATTR:
		def __CanChangeItemAttrList2(self, dstSlotPos):
			return uiAttr67Add.Attr67AddWindow.CantAttachToAttrSlot(dstSlotPos, False)

	def __CanChangeItemAttrList(self, dstSlotPos, srcItemVNum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() == item.ITEM_TYPE_DS and srcItemVNum != 71097:
			return False

		elif srcItemVNum == 71097 and item.GetItemType() != item.ITEM_TYPE_DS:
			return False

		elif not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_RINGS) and srcItemVNum != 71097:
			return False


		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanChangeCostumeAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_COSTUME:
			return False

		if app.ENABLE_AURA_SYSTEM:
			if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
				return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanResetCostumeAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_COSTUME:
			return False

		if app.ENABLE_AURA_SYSTEM:
			if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
				return False

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				return True

		return False

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)


		if item.GetItemType() != item.ITEM_TYPE_ARMOR and item.GetItemType() != item.ITEM_TYPE_RINGS:
			return False

		if item.GetItemType() == item.ITEM_TYPE_ARMOR:
			if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		type = item.GetItemSubType()

		if item.GetItemType() == item.ITEM_TYPE_RINGS:
			type = item.GetItemType()

		if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, type):
			return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR and item.GetItemType() != item.ITEM_TYPE_RINGS:
			return False

		if item.GetItemType() == item.ITEM_TYPE_ARMOR:
			if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_RINGS):
			return False

		attrCount = 0
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			if player.GetItemAttribute(dstSlotPos, i) != 0:
				attrCount += 1

		if attrCount<4:
			return True

		return False

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"])

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

		if app.WJ_ENABLE_TRADABLE_ICON:
			map(lambda wnd:wnd.RefreshLockedSlot(), self.bindWnds)
			self.RefreshMarkSlots()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def UseItemSlotNew(self,slotIndex,index_default = 0):
		#self.SetInventoryPage(index_default)
		#self.inventoryTab[index_default].Down()
		self.UseItemSlot(slotIndex)

	def UseItemSlot(self, slotIndex):
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		if self.interface:
			if self.interface.GetPosChangeItemManual() != -1:
				if self.interface.GetPosChangeItemManual() == slotIndex:
					return

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
				return

		if app.ENABLE_SASH_SYSTEM:
			if self.isShowSashWindow():
				sash.Add(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex, 255)
				return

		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def AttachSpecialToInv(self, window, index):
		itemVnum = player.GetItemIndex(window, index)
		item.SelectItem(itemVnum)
		(w, h) = item.GetItemSize()
		pos = self.grid.find_blank(w, h)
		if pos == -1:
			return False
		self.__SendMoveItemPacket(window, index, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], pos, player.GetItemCount(window, index))
		return True

	def AttachItemFromSafebox(self, slotIndex, item_type, itemIndex):
		item.SelectItem(itemIndex)
		if item.GetItemType() == item.ITEM_TYPE_DS:
			return
		(w, h) = item.GetItemSize()
		pos = self.grid.find_blank(w, h)
		if pos == -1:
			return False
		net.SendSafeboxCheckoutPacket(slotIndex, item_type, pos)
		return True

	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],slotIndex)
		item.SelectItem(ItemVNum)

		if ItemVNum == 71998 or ItemVNum == 71999:
			if app.WJ_ENABLE_TRADABLE_ICON:
				# self.wndItem.SetCanMouseEventSlot(slotIndex)
				# self.wndItem.SetUnusableSlotOnTopWnd(slotIndex)
				self.wndItem.LockSlot(slotIndex)
				self.wndItem.SetCantMouseEventSlot(slotIndex)
				self.wndItem.RefreshSlot()

		if app.ENABLE_AURA_SYSTEM:
			if player.IsAuraRefineWindowOpen():
				self.__UseItemAura(slotIndex)
				return

		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM % item.GetItemName())
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		elif app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM and (ItemVNum == 20171 or ItemVNum == 20172 or ItemVNum == 20173):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM % item.GetItemName())
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		elif app.ENABLE_SHOW_CHEST_DROP and item.GetItemType() == item.ITEM_TYPE_GIFTBOX and app.IsPressed(app.DIK_LCONTROL):
			if app.IsPressed(app.DIK_Z):
				net.SendChatPacket("/chest_drop %d %d %d"%(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex,player.GetItemCount(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)))
			else:
				if self.interface:
					self.interface.OpenChestDropWindow(ItemVNum, self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"], slotIndex)
			return
		else:
			if app.ENABLE_NEW_PET_SYSTEM and item.GetItemType() == item.ITEM_TYPE_PET and item.GetItemSubType() == item.PET_EGG:
				self.interface.OpenChangeNameWindow(slotIndex,slotIndex,ItemVNum, 2)
			else:
				self.__SendUseItemPacket(slotIndex)
			#net.SendItemUsePacket(slotIndex)

	if app.ENABLE_RARITY:
		def __UseItemToItemQuestionDialog_OnAccept(self):
			self.__SendUseItemToItemPacket(player.INVENTORY, self.questionDialog.srcItemSlotPos,self.questionDialog.dstItemSlotPos)
			self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemToItemPacket(self, srcInv, srcSlotPos, dstSlotPos, srcItemVID = -1):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		#if uiPrivateShopBuilder.IsBuildingPrivateShop():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
		#	return

		net.SendItemUseToItemPacket(srcInv, srcSlotPos, player.INVENTORY, dstSlotPos)


	def __SendUseItemPacket(self, slotPos):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		#if uiPrivateShopBuilder.IsBuildingPrivateShop():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
		#	return

		#chat.AppendChat(1,"test")
		net.SendItemUsePacket(self.SLOT_WINDOW_TYPE[self.categoryPageIndex]["window"],slotPos)

	#def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):
		# 개인상점 열고 있는 동안 아이템 사용 방지
		#if uiPrivateShopBuilder.IsBuildingPrivateShop():
			#chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			#return

		#net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)

	def __SendMoveItemPacket(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount):
		#if uiPrivateShopBuilder.IsBuildingPrivateShop():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
		#	return

		net.SendItemMovePacket(srcSlotWindow , srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount)

	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoulRefine = wndDragonSoulRefine

	if app.__RENEWAL_CRYSTAL__:
		def CheckCrystalTime(self, slotItemIdx, desSlotItemIdx):
			if ((slotItemIdx >= 51005 and slotItemIdx <= 51006) and (desSlotItemIdx >= 51010 and desSlotItemIdx <= 51035)):
				return True
			return False

	if app.ENABLE_SASH_SYSTEM:
		def SetSashWindow(self, wndSashCombine, wndSashAbsorption):
			self.wndSashCombine = wndSashCombine
			self.wndSashAbsorption = wndSashAbsorption

		def isShowSashWindow(self):
			if self.wndSashCombine:
				if self.wndSashCombine.IsShow():
					return 1

			if self.wndSashAbsorption:
				if self.wndSashAbsorption.IsShow():
					return 1
			
			return 0

	if app.ENABLE_AURA_SYSTEM:
		def __UseItemAuraQuestionDialog_OnAccept(self):
			self.questionDialog.Close()
			net.SendAuraRefineCheckIn(*(self.questionDialog.srcItem + self.questionDialog.dstItem + (player.GetAuraRefineWindowType(),)))
			self.questionDialog.srcItem = (0, 0)
			self.questionDialog.dstItem = (0, 0)

		def __UseItemAuraQuestionDialog_Close(self):
			self.questionDialog.Close()
			self.questionDialog.srcItem = (0, 0)
			self.questionDialog.dstItem = (0, 0)

		def __UseItemAura(self, slotIndex):
			AuraSlot = player.FineMoveAuraItemSlot()
			UsingAuraSlot = player.FindActivatedAuraSlot(player.INVENTORY, slotIndex)
			AuraVnum = player.GetItemIndex(slotIndex)
			item.SelectItem(AuraVnum)
			if player.GetAuraCurrentItemSlotCount() >= player.AURA_SLOT_MAX <= UsingAuraSlot:
				return

			if player.IsEquipmentSlot(slotIndex):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EQUIPITEM)
				return

			# if app.ENABLE_SOUL_BIND_SYSTEM and player.IsSealedItemBySlot(player.INVENTORY, slotIndex):
				# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_SEALITEM)
				# return

			# if app.ENABLE_SOUL_BIND_SYSTEM:
				# if player.GetItemSealDate(player.INVENTORY, slotIndex) == -1 or player.GetItemSealDate(player.INVENTORY, slotIndex) > 0:
					# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_SEALITEM)
					# return

			if player.GetAuraRefineWindowType() == player.AURA_WINDOW_TYPE_ABSORB:
				isAbsorbItem = False
				if item.GetItemType() == item.ITEM_TYPE_COSTUME:
					if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
						if player.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM) == 0:
							if UsingAuraSlot == player.AURA_SLOT_MAX:
								if AuraSlot != player.AURA_SLOT_MAIN:
									return

								net.SendAuraRefineCheckIn(player.INVENTORY, slotIndex, player.AURA_REFINE, AuraSlot, player.GetAuraRefineWindowType())

						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
							return

					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
						return

				elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
					if item.GetItemSubType() in [item.ARMOR_SHIELD, item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR]:
						if player.FindUsingAuraSlot(player.AURA_SLOT_MAIN) == player.NPOS():
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

						isAbsorbItem = True
					else:
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
						return

				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_ABSORBITEM)
					return

				if isAbsorbItem:
					if UsingAuraSlot == player.AURA_SLOT_MAX:
						if AuraSlot != player.AURA_SLOT_SUB:
							if player.FindUsingAuraSlot(player.AURA_SLOT_SUB) == player.NPOS():
								AuraSlot = player.AURA_SLOT_SUB
							else:
								return

						self.questionDialog = uiCommon.QuestionDialog()
						self.questionDialog.SetText(localeInfo.AURA_NOTICE_DEL_ABSORDITEM)
						self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemAuraQuestionDialog_OnAccept))
						self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemAuraQuestionDialog_Close))
						self.questionDialog.srcItem = (player.INVENTORY, slotIndex)
						self.questionDialog.dstItem = (player.AURA_REFINE, AuraSlot)
						self.questionDialog.Open()

			elif player.GetAuraRefineWindowType() == player.AURA_WINDOW_TYPE_GROWTH:
				if UsingAuraSlot == player.AURA_SLOT_MAX:
					if AuraSlot == player.AURA_SLOT_MAIN:
						if item.GetItemType() == item.ITEM_TYPE_COSTUME:
							if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
								socketLevelValue = player.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
								curLevel = (socketLevelValue / 100000) - 1000
								curExp = socketLevelValue % 100000;
								if curLevel >= player.AURA_MAX_LEVEL:
									chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
									return

								if curExp >= player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_NEED_EXP):
									chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_GROWTHITEM)
									return

								net.SendAuraRefineCheckIn(player.INVENTORY, slotIndex, player.AURA_REFINE, AuraSlot, player.GetAuraRefineWindowType())

							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
								return

						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
							return

					elif AuraSlot == player.AURA_SLOT_SUB:
						if player.FindUsingAuraSlot(player.AURA_SLOT_MAIN) != player.NPOS():
							if item.GetItemType() == item.ITEM_TYPE_RESOURCE:
								if item.GetItemSubType() == item.RESOURCE_AURA:
									if UsingAuraSlot == player.AURA_SLOT_MAX:
										if AuraSlot != player.AURA_SLOT_SUB:
											return

										net.SendAuraRefineCheckIn(player.INVENTORY, slotIndex, player.AURA_REFINE, AuraSlot, player.GetAuraRefineWindowType())
								else:
									chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURARESOURCE)
									return

							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURARESOURCE)
								return

						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

			elif player.GetAuraRefineWindowType() == player.AURA_WINDOW_TYPE_EVOLVE:
				if UsingAuraSlot == player.AURA_SLOT_MAX:
					if AuraSlot == player.AURA_SLOT_MAIN:
						if item.GetItemType() == item.ITEM_TYPE_COSTUME:
							if item.GetItemSubType() == item.COSTUME_TYPE_AURA:
								socketLevelValue = player.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
								curLevel = (socketLevelValue / 100000) - 1000
								curExp = socketLevelValue % 100000;
								if curLevel >= player.AURA_MAX_LEVEL:
									chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
									return

								if curLevel != player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_LEVEL_MAX) or curExp < player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_NEED_EXP):
									chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
									return

								if player.FindUsingAuraSlot(AuraSlot) != player.NPOS():
									return

								net.SendAuraRefineCheckIn(player.INVENTORY, slotIndex, player.AURA_REFINE, AuraSlot, player.GetAuraRefineWindowType())

							else:
								chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
								return

						else:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_AURAITEM)
							return

					elif AuraSlot == player.AURA_SLOT_SUB:
						Cell = player.FindUsingAuraSlot(player.AURA_SLOT_MAIN)
						if Cell == player.NPOS():
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_POSSIBLE_REGISTER_AURAITEM)
							return

						socketLevelValue = player.GetItemMetinSocket(*(Cell + (player.ITEM_SOCKET_AURA_CURRENT_LEVEL,)))
						curLevel = (socketLevelValue / 100000) - 1000
						curExp = socketLevelValue % 100000;
						if curLevel >= player.AURA_MAX_LEVEL:
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_MAX_LEVEL)
							return

						if curExp < player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_NEED_EXP):
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
							return

						if player.GetItemIndex(slotIndex) != player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_MATERIAL_VNUM):
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEM)
							return

						if player.GetItemCount(slotIndex) < player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_MATERIAL_COUNT):
							chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.AURA_IMPOSSIBLE_EVOLUTION_ITEMCOUNT)
							return

						if UsingAuraSlot == player.AURA_SLOT_MAX:
							if AuraSlot != player.AURA_SLOT_MAX:
								if player.FindUsingAuraSlot(AuraSlot) != player.NPOS():
									return

							net.SendAuraRefineCheckIn(player.INVENTORY, slotIndex, player.AURA_REFINE, AuraSlot, player.GetAuraRefineWindowType())

if app.__RENEWAL_BRAVE_CAPE__:
	import os
	class BraveCapeWindow(ui.Board):
		__children={}
		class SliderBarNew(ui.Window):
			def __init__(self):
				ui.Window.__init__(self)
				self.curPos = 1.0
				self.pageSize = 1.0
				self.eventChange = None
				self.__Load()

			def __Load(self):
				IMG_DIR = "d:/ymir work/ui/game/bravery_cape/"

				img = ui.ImageBox()
				img.SetParent(self)
				img.LoadImage(IMG_DIR+"slider_bg.tga")
				img.Show()
				self.backGroundImage = img

				self.SetSize(self.backGroundImage.GetWidth(), self.backGroundImage.GetHeight())

				cursor = ui.DragButton()
				cursor.AddFlag("movable")
				cursor.AddFlag("restrict_y")
				cursor.SetParent(self)
				cursor.SetMoveEvent(ui.__mem_func__(self.__OnMove))
				cursor.SetUpVisual(IMG_DIR+"drag.tga")
				cursor.SetOverVisual(IMG_DIR+"drag.tga")
				cursor.SetDownVisual(IMG_DIR+"drag.tga")
				cursor.Show()
				self.cursor = cursor

				##
				self.cursor.SetRestrictMovementArea(0, 0, self.backGroundImage.GetWidth(), 0)
				self.pageSize = self.backGroundImage.GetWidth() - self.cursor.GetWidth()

			def __OnMove(self):
				(xLocal, yLocal) = self.cursor.GetLocalPosition()
				self.curPos = float(xLocal) / float(self.pageSize)
				if self.eventChange:
					self.eventChange()
			def SetSliderPos(self, pos):
				self.curPos = pos
				self.cursor.SetPosition(int(self.pageSize * pos), 0)
			def GetSliderPos(self):
				return self.curPos
			def SetEvent(self, event):
				self.eventChange = event
			def Enable(self):
				self.cursor.Show()
			def Disable(self):
				self.cursor.Hide()

		def Destroy(self):
			self.SaveData()
			self.__children={}
		def CreateWindow(self, classPtr, parent, pos):
			window = classPtr
			window.SetParent(parent)
			window.SetPosition(*pos)
			window.Show()
			return window
		def __OverOutItem(self):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipItem:
					interface.tooltipItem.HideToolTip()
		def __OverInItem(self, itemIdx):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipItem:
					interface.tooltipItem.SetItemToolTip(itemIdx)
		def __init__(self):
			ui.Board.__init__(self)
			self.SetSize(140, 130 + 44)
			self.AddFlag("attach")
			self.AddFlag("float")

			self.__children["firstOpened"] = app.GetGlobalTimeStamp() + 5

			IMG_DIR = "d:/ymir work/ui/game/bravery_cape/"

			BRAVE_CAPE_ITEM_IDX = 20570

			item.SelectItem(BRAVE_CAPE_ITEM_IDX)

			bgImg = self.CreateWindow(ui.ImageBox(), self, (5, 6))
			bgImg.LoadImage(IMG_DIR+"bg.tga")
			self.__children["bgImg"] = bgImg

			timeTextVisual = self.CreateWindow(ui.TextLine(), bgImg, (13, 60))
			timeTextVisual.SetText("Second")
			self.__children["timeTextVisual"] = timeTextVisual

			timeSlider = self.CreateWindow(self.SliderBarNew(), bgImg, (13, 73 + 5))
			timeSlider.SetEvent(ui.__mem_func__(self.OnChangeTimeSlider))
			self.__children["timeSlider"] = timeSlider

			timeBg = self.CreateWindow(ui.ImageBox(), bgImg, (77, 64))
			timeBg.LoadImage(IMG_DIR+"input_output.tga")
			self.__children["timeBg"] = timeBg

			timeText = self.CreateWindow(ui.TextLine(), timeBg, (0, 0))
			timeText.SetAllAlign()
			timeText.SetText("0")
			self.__children["timeText"] = timeText

			rangeTextVisual = self.CreateWindow(ui.TextLine(), bgImg, (13, 73 + 22 + 17 + 5 - 18))
			rangeTextVisual.SetText("Range")
			self.__children["rangeTextVisual"] = rangeTextVisual

			rangeSlider = self.CreateWindow(self.SliderBarNew(), bgImg, (13, 73 + 22 + 17 + 5))
			rangeSlider.SetEvent(ui.__mem_func__(self.OnChangeRangeSlider))
			self.__children["rangeSlider"] = rangeSlider

			rangeBg = self.CreateWindow(ui.ImageBox(), bgImg, (77, 95 + 8))
			rangeBg.LoadImage(IMG_DIR+"input_output.tga")
			self.__children["rangeBg"] = rangeBg

			rangeText = self.CreateWindow(ui.TextLine(), rangeBg, (0, 0))
			rangeText.SetAllAlign()
			rangeText.SetText("0")
			self.__children["rangeText"] = rangeText

			itemIcon = self.CreateWindow(ui.ImageBox(), bgImg, (50, 13))
			itemIcon.LoadImage(item.GetIconImageFileName())
			itemIcon.SAFE_SetStringEvent("MOUSE_OVER_OUT",self.__OverOutItem)
			itemIcon.SAFE_SetStringEvent("MOUSE_OVER_IN",self.__OverInItem, BRAVE_CAPE_ITEM_IDX)
			self.__children["itemIcon"] = itemIcon

			startBtn = self.CreateWindow(ui.Button(), bgImg, (6, 95 + 39))
			startBtn.SetUpVisual(IMG_DIR+"start_btn_0.tga")
			startBtn.SetOverVisual(IMG_DIR+"start_btn_1.tga")
			startBtn.SetDownVisual(IMG_DIR+"start_btn_2.tga")
			startBtn.SetDisableVisual(IMG_DIR+"start_btn_2.tga")
			startBtn.SAFE_SetEvent(self.__ClickStatusBtn, "ACTIVE")
			startBtn.SetText("Start")
			self.__children["startBtn"] = startBtn

			stopBtn = self.CreateWindow(ui.Button(), bgImg, (66, 95 + 39))
			stopBtn.SetUpVisual(IMG_DIR+"start_btn_0.tga")
			stopBtn.SetOverVisual(IMG_DIR+"start_btn_1.tga")
			stopBtn.SetDownVisual(IMG_DIR+"start_btn_2.tga")
			stopBtn.SetDisableVisual(IMG_DIR+"start_btn_2.tga")
			stopBtn.SAFE_SetEvent(self.__ClickStatusBtn, "DEACTIVE")
			stopBtn.SetText("Stop")
			self.__children["stopBtn"] = stopBtn

			expandBtn = self.CreateWindow(ui.Button(), self, (0, 10))
			expandBtn.SetUpVisual("d:/ymir work/ui/game/belt_inventory/btn_minimize_normal.tga")
			expandBtn.SetOverVisual("d:/ymir work/ui/game/belt_inventory/btn_minimize_over.tga")
			expandBtn.SetDownVisual("d:/ymir work/ui/game/belt_inventory/btn_minimize_down.tga")
			expandBtn.SAFE_SetEvent(self.Close)
			self.__children["expandBtn"] = expandBtn

			self.__children["second"] = 0
			self.__children["range"] = 0
			self.__children["status"] = False
			self.Refresh()

		def Refresh(self):
			(second, range, posTime, posSlider) = (self.__children["second"], self.__children["range"], 0.0, 0.0)
			if second > 5800:
				second = 5800
			if range > 7000:
				range = 7000

			self.__children["timeText"].SetText(str((second/100)+2))
			self.__children["rangeText"].SetText(str(range+1000))

			self.__children["timeSlider"].SetSliderPos((1.0/5800.0)*second)
			self.__children["rangeSlider"].SetSliderPos((1.0/7000.0)*range)

			self.__children["second"] = second
			self.__children["range"] = range

		def Open(self):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.wndInventory:
					interface.wndInventory.disbandBtn.Hide()
			self.Show()

		def Close(self):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.wndInventory:
					interface.wndInventory.disbandBtn.Show()
			self.Hide()

		def __ClickStatusBtn(self, type):
			if type == "ACTIVE":
				net.SendChatPacket("/brave_cape active {} {}".format((self.__children["second"]/100)+2, self.__children["range"] + 1000))
			elif type == "DEACTIVE":
				net.SendChatPacket("/brave_cape deactive")

		def AdjustPosition(self, x, y):
			self.SetPosition(x + 10 - self.GetWidth(), y + 220)
		def OnChangeRangeSlider(self):
			val = int(((1.0/14000.0)*(self.__children["rangeSlider"].GetSliderPos()*14000))*14000)
			self.__children["range"] = val
			self.Refresh()
		def OnChangeTimeSlider(self):
			val = int(((1.0/5800.0)*(self.__children["timeSlider"].GetSliderPos()*5800))*5800)
			self.__children["second"] = val
			self.Refresh()
		def SetStatus(self, status):
			self.__children["status"] = True if int(status) == 1 else False
			if self.__children["status"]:
				self.__children["startBtn"].Disable()
				self.__children["stopBtn"].Enable()
			else:
				self.__children["stopBtn"].Disable()
				self.__children["startBtn"].Enable()
			self.Refresh()
		def SaveData(self):
			try:
				file = open("lib/{}_brave_cape".format(player.GetName()), "w+")
				file.write("{}#{}#{}\n".format(1 if (self.__children["status"] if self.__children.has_key("status") else False) == True else 0, self.__children["second"], self.__children["range"]))
				file.close()
			except:
				pass
		def LoadData(self):
			try:
				splitList = open("lib/{}_brave_cape".format(player.GetName()), "r").readlines()[0].split("#")
				self.__children["status"] = True if int(splitList[0]) == 1 else False
				self.__children["second"] = int(splitList[1])
				self.__children["range"] = int(splitList[2])
				self.Refresh()
				if self.__children["status"]:
					self.__ClickStatusBtn("ACTIVE")
				os.remove("lib/{}_brave_cape".format(player.GetName()))
			except:
				pass