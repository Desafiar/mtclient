import os
import app
import dbg
import item
import chat
import net
import localeinfo
import ime
import time
import ui
import uiCommon
import uiToolTip
import colorInfo
import player
import snd
import grp
import mouseModule
import shop
import wndMgr
#import uiPrivateShopBuilder
import constInfo
import uiScriptLocale
from uiUtils import Edit2 as Edit2

c = colorInfo.CHAT_RGB_NOTICE
already_opened = 0
titleColor = ui.GenerateColor(c[0],c[1],c[2])
NEGATIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)
POSITIVE_COLOR = grp.GenerateColor(0.6911, 0.8754, 0.7068, 1.0)
##Should be disabled becouse this is only for my client UI ##
POSITION_FIX=False
#############################################################
import uiUtils

RUTA_IMG = "rework_offlineshop/"

class ShopDialogCreate(ui.ScriptWindow):
	UI={}

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()
		#self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		#self.privateShopBuilder.Hide()
		#self.privateShopBuilder.SetItemToolTip(self.tooltipItem)
		self.pop=None
		self.interface = None
		self.MoneyActual = 0
		# self.bank = None
		self.withdrawMoneyTime = 0
		self.__LoadQuestionDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def __LoadQuestionDialog(self):

		self.UI["windows_shop"] = ui.Window()
		self.UI["windows_shop"].SetCenterPosition()
		self.UI["windows_shop"].AddFlag("movable")
		self.UI["windows_shop"].AddFlag("animate")
		self.UI["windows_shop"].SetSize(324+1, 326)
		self.UI["windows_shop"].SetCenterPosition()
		self.UI["windows_shop"].SetTop()
		self.UI["windows_shop"].Hide()



		self.UI["board"] = ui.BoardWithTitleBar()
		self.UI["board"].SetParent(self.UI["windows_shop"])
		self.UI["board"].AddFlag("attach")
		self.UI["board"].AddFlag("float")
		self.UI["board"].AddFlag("animate")
		if POSITION_FIX:
			self.UI["board"].SetSize(324+1, 326)
		else:
			self.UI["board"].SetSize(324+1, 326)
		self.UI["board"].SetPosition(0,0)
		self.UI["board"].SetTitleName("Tienda Offline")
		self.UI["board"].SetCloseEvent(self.Close)
		self.UI["board"].Hide()

		self.UI["base_transparente"] = ui.MakeImageBox(self.UI["board"],RUTA_IMG+"base_transparente.tga",9,35)
		self.UI["base_transparente"].Show()

		self.UI["bar_information"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_informacion.tga",4,3)
		self.UI["bar_information"].Show()

		self.UI["icono_formulario"] = ui.MakeImageBox(self.UI["bar_information"],RUTA_IMG+"icono_formulario.tga",80,2)
		self.UI["icono_formulario"].Show()

		self.UI["info_tienda"] = ui.MakeText(self.UI["bar_information"], "Informacion de la tienda" , 110, 3, None)
		self.UI["info_tienda"].Show()

		self.UI["barra_nombre_tienda"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_nombre_tienda.tga",15,38)
		self.UI["barra_nombre_tienda"].Show()

		self.UI["nameText"] = ui.MakeText(self.UI["barra_nombre_tienda"], uiScriptLocale.SHOP_NAME, 85, 1, None)
		self.UI["nameEdit"]=Edit2(self.UI["board"],"",24,93,210,25,FALSE,0,30)
		self.UI["nameEdit"].SetEscapeEvent(ui.__mem_func__(self.Close))

		self.UI["barra_tiempo"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_datos_offline.tga",15,88)
		self.UI["barra_tiempo"].Show()

		self.UI["campo_tiempo_1"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"campo_tiempo_1.tga",192,88)
		self.UI["campo_tiempo_1"].Show()

		self.UI["selectText"] = ui.TextLine()
		self.UI["selectText"].SetParent(self.UI["barra_tiempo"])
		self.UI["selectText"].SetPosition(10, 1)
		self.UI["selectText"].SetFeather()
		self.UI["selectText"].SetDefaultFontName()
		self.UI["selectText"].SetOutline()
		self.UI["selectText"].SetText("Tiempo de la Tienda:")
		self.UI["selectText"].Show()

		self.UI["barra_costo"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_datos_offline.tga",15,88+22)
		self.UI["barra_costo"].Show()


		self.UI["campo_yang_corto"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"campo_yang_corto.tga",192,88+22)
		self.UI["campo_yang_corto"].Show()


		self.UI["costText"] = ui.TextLine()
		self.UI["costText"].SetParent(self.UI["barra_costo"])
		self.UI["costText"].SetPosition(10,1)
		self.UI["costText"].SetFeather()
		self.UI["costText"].SetDefaultFontName()
		self.UI["costText"].SetOutline()
		self.UI["costText"].SetText("Coste de Apertura:")
		self.UI["costText"].Show()

		self.UI["costBar"] = ui.Bar()
		self.UI["costBar"].SetParent(self.UI["board"])
		self.UI["costBar"].SetPosition(156,117+5)
		self.UI["costBar"].SetSize(85,20)
		self.UI["costBar"].SetColor(0xff0a0a0a)
		self.UI["costBar"].Hide()

		self.UI["price"] = ui.TextLine()
		self.UI["price"].SetParent(self.UI["campo_yang_corto"])
		self.UI["price"].SetPosition(24,2)
		self.UI["price"].SetText("")
		self.UI["price"].Show()
		
		self.UI["create"] = ui.MakeButton(self.UI["board"], 100, 184 , "", RUTA_IMG, "boton_1.tga", "boton_2.tga", "boton_3.tga")
		self.UI["create"].SetText(uiScriptLocale.SHOP_CREATE)
		self.UI["create"].SetEvent(ui.__mem_func__(self.CreateShop))
		self.UI["create"].Show()

		self.UI["bar_information_1"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_informacion.tga",4,195)
		self.UI["bar_information_1"].Show()

		self.UI["info_tienda_1"] = ui.MakeText(self.UI["bar_information_1"], "Yang obtenido de ventas" , 95, 3, None)
		self.UI["info_tienda_1"].Show()

		self.UI["cancel"] = ui.MakeButton(self.UI["board"], 25, 160, "", "d:/ymir work/ui/public/public_intro_btn/", "cancel_btn_01.sub", "cancel_btn_02.sub", "cancel_btn_03.sub")
		self.UI["cancel"].SetEvent(ui.__mem_func__(self.Close))
		self.UI["cancel"].Hide()


		self.UI["campo_yang_largo"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"campo_yang_largo.tga",15,222)
		self.UI["campo_yang_largo"].Show()

		self.UI["text_yang"] = ui.TextLine()
		self.UI["text_yang"].SetParent(self.UI["campo_yang_largo"])
		self.UI["text_yang"].SetPosition(0,1)
		self.UI["text_yang"].SetText("2.000.000.000 yang")
		self.UI["text_yang"].SetWindowHorizontalAlignCenter()
		self.UI["text_yang"].SetHorizontalAlignCenter()
		self.UI["text_yang"].Show()

		self.UI["barra_retirar_yang"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_datos_offline.tga",15,222+23)
		self.UI["barra_retirar_yang"].Show()

		self.UI["retirar_yang_text"] = ui.TextLine()
		self.UI["retirar_yang_text"].SetParent(self.UI["barra_retirar_yang"])
		self.UI["retirar_yang_text"].SetPosition(10,1)
		self.UI["retirar_yang_text"].SetFeather()
		self.UI["retirar_yang_text"].SetDefaultFontName()
		self.UI["retirar_yang_text"].SetOutline()
		self.UI["retirar_yang_text"].SetText("Retirar Yang:")
		self.UI["retirar_yang_text"].Show()

		self.UI["retirar_yang"] = ui.MakeButton(self.UI["base_transparente"], 200, 222+22 , "", RUTA_IMG, "retiro_yang_1.tga", "retiro_yang_2.tga", "retiro_yang_3.tga")
		self.UI["retirar_yang"].SetEvent(ui.__mem_func__(self.GiveBank))
		self.UI["retirar_yang"].Show()


		self.CreateList()

	def BindInterface(self, interface):
		self.interface = interface

	def Destroy(self):
		self.UI["board"].Hide()
		self.UI["windows_shop"].Hide()
		self.__OnClosePopupDialog()
		self.UI={}
		return TRUE
		#self.ClearDictionary()
	def CreateList(self):
		if "select" in self.UI.keys():
			self.UI["select"].Hide()
			self.UI["select"].Destroy()
		self.UI["select"] = None
		self.UI["select"] = DropDown(self.UI["board"],"---")
		self.UI["select"].SetPosition(222,125)
		self.UI["select"].SetSize(78,15)
		self.UI["select"].SetTop()
		self.UI["select"].OnChange=self.Load
		self.UI["select"].Show()


	def CreateShop(self):

		if constInfo.GET_OFFSHOP_OPENED() == 1:
			return
			
		if len(constInfo.gift_items) > 0:
			self.PopupMessage("You must get all items from gifts before open a new shop")
			return
		if len(self.UI["nameEdit"].GetText()) <=0:
			self.PopupMessage(uiScriptLocale.SHOP_NAME_EMPTY)
			return
		id=int(self.UI["select"].DropList.GetSelectedItem().value)
		if int(id) <=0:
			self.PopupMessage(uiScriptLocale.SHOP_TIMEOUT_EMPTY)
			return
		item = constInfo.shop_cost[id-1]
		
		if int(item["id"]) <=0:
			self.PopupMessage(uiScriptLocale.SHOP_TIMEOUT_EMPTY)
			return
		self.__OnClosePopupDialog()


		self.interface.NewShopPrivateShopOpen(self.UI["nameEdit"].GetText(),int(item["id"]))
		self.Close()	
		
	# def OnUpdate(self):
		# if self.bank != None:
			# self.bank.OnUpdate()

	# def OpenBank(self):
		# import uibank
		# self.bank = uibank.BankDialog()
		# self.bank.Show()

	def ShopBank(self,money):
		self.UI["text_yang"].SetText(localeinfo.NumberToMoneyString(int(money)))
		self.MoneyActual = int(money)

	def GetMoney(self):
		return self.MoneyActual

	def GiveBank(self):
		if self.GetMoney() <= 0:
			return

		if (app.GetTime() < self.withdrawMoneyTime + 5):
			chat.AppendChat(chat.CHAT_TYPE_INFO, "You must wait 5 seconds to withdraw the money again.")
			return

		net.SendChatPacket("/shop_bank")

		self.withdrawMoneyTime = app.GetTime()

	def __OnClosePopupDialog(self):
		if self.pop != None:
			if self.pop.IsShow():
				self.pop.Hide()
		self.pop = None
	def Hide(self):
		if "board" in self.UI.keys():
			self.UI["board"].Hide()
			self.UI["windows_shop"].Hide()
			self.UI["price"].Hide()
			self.UI["select"].dropped = 0
			self.UI["select"].ClearItems()
			self.UI["nameEdit"].SetText("")
			self.MoneyActual = 0
			self.Days=0
		ui.ScriptWindow.Hide(self)
		
	def Show(self):
		self.UI["board"].SetTop()
		self.UI["board"].Show()
		self.UI["windows_shop"].Show()
		
		self.UnLoad()
		self.CreateList()
		for i in xrange(len(constInfo.shop_cost)):	
			item=constInfo.shop_cost[i]
			name=uiScriptLocale.SHOP_CREATE_NORMAL
			if item["time"]>0:
				name=str(item["time"])+" "
				if item["time"] == 1:
					if item["time_val"]==3600:
						name+=uiScriptLocale.SHOP_CREATE_HOUR
					else:
						name+=uiScriptLocale.SHOP_CREATE_DAY
				else:
					if item["time_val"]==86400:
						name+=uiScriptLocale.SHOP_CREATE_DAYS
					else:
						name+=uiScriptLocale.SHOP_CREATE_HOURS
			
			self.UI["select"].AppendItem(name,i+1)
		
		ui.ScriptWindow.Show(self)
		self.UI["board"].Show()
		self.UI["windows_shop"].Show()
	def Load(self):
		id=self.UI["select"].DropList.GetSelectedItem().value
		if int(id) == 0:
			print "unload"
			self.UnLoad()
			return
		item = constInfo.shop_cost[id-1]
		if item["price"]>0:
			self.UI["price"].SetText(localeinfo.NumberToMoneyString(item["price"]))
			self.UI["price"].Show()
		else:
			self.UI["price"].Show()
	def UnLoad(self):
		self.UI["price"].Hide()
		self.UI["select"].Clear()	
	def Clear(self):
		self.UI["select"].Clear()
	def PopupMessage(self,text):
		pop = uiCommon.PopupDialog()
		pop.SetText(text)
		pop.SetAcceptEvent(self.__OnClosePopupDialog)
		pop.Open()
		self.pop = pop
		self.pop.SetTop()


	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Close(self):
		self.__OnClosePopupDialog()
		self.UnLoad()
		self.UI["board"].Hide()
		self.UI["windows_shop"].Hide()
		self.MoneyActual = 0

		self.Hide()	

class DropDown(ui.Window):
	dropped  = 0
	dropstat = 0
	last = 0
	lastS = 0
	maxh = 95
	tt = ""
	OnChange = None
	class Item(ui.ListBoxEx.Item):
		def __init__(self,parent, text,value=0):
			ui.ListBoxEx.Item.__init__(self)

			self.textBox=ui.TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			# self.textBox.SetLimitWidth(parent.GetWidth()-132)
			self.textBox.Show()
			self.value = value
		def GetValue(self):
			return self.value
		def __del__(self):
			ui.ListBoxEx.Item.__del__(self)
			
	def __init__(self,parent,tt = "",down=1):
		ui.Window.__init__(self,"TOP_MOST")
		self.tt=tt
		self.down = down
		self.SetParentProxy(parent)
		self.bg = ui.Bar("TOP_MOST")
		self.bg.SetParent(self)
		self.bg.SetPosition(0,0)
		self.bg.SetColor(0xc0000000)
		self.bg.OnMouseOverIn = self.bgMouseIn
		self.bg.OnMouseOverOut = self.bgMouseOut
		self.bg.OnMouseLeftButtonDown = self.ExpandMe
		self.bg.Show()
		self.act = ui.TextLine()
		self.act.SetParent(self.bg)
		self.act.SetPosition(4,0)
		self.act.SetText(self.tt)
		self.act.Show()
		self.GetText = self.act.GetText
		
		self.Drop = ui.Bar("TOP_MOST")
		self.Drop.SetParent(self.GetParentProxy())
		self.Drop.SetPosition(0,21)
		# self.Drop.SetSize(150,95)
		self.Drop.SetSize(150,0)
		# self.Drop.SetColor(0xc00a0a0a)
		self.Drop.SetColor(0xff0a0a0a)
		
		
		self.ScrollBar = ui.ThinScrollBar()
		self.ScrollBar.SetParent(self.Drop)
		self.ScrollBar.SetPosition(132,0)
		# self.ScrollBar.SetScrollBarSize(95)
		self.ScrollBar.SetScrollBarSize(0)
		# self.ScrollBar.Show()
		
		self.DropList = ui.ListBoxEx()
		self.DropList.SetParent(self.Drop)
		self.DropList.itemHeight = 12
		self.DropList.itemStep = 13
		self.DropList.SetPosition(0,0)
		# self.DropList.SetSize(132,self.maxh)
		self.DropList.SetSize(132,13) 
		self.DropList.SetScrollBar(self.ScrollBar)
		self.DropList.SetSelectEvent(self.SetTitle)
		self.DropList.SetViewItemCount(0)
		self.DropList.Show()
		if self.tt != "":
			self.AppendItemAndSelect(self.tt)
		self.selected = self.DropList.GetSelectedItem()
		
			
		self.SetSize(120,20)
	def __del__(self): 
		ui.Window.__del__(self)
	c = 1
	def AppendItem(self,text,value=0):
		self.c+=1   
		self.DropList.AppendItem(self.Item(self,text,value))
		self.maxh = min(95,13*self.c)
		if self.c > 7:
			self.ScrollBar.Show()
			
		
	def AppendItemAndSelect(self,text,value=0):
		self.DropList.AppendItem(self.Item(self,text,value))
		self.DropList.SelectIndex(len(self.DropList.itemList)-1)
		
		
	def ClearItems(self):
		self.DropList.RemoveAllItems()
		self.AppendItemAndSelect(self.tt)
		self.act.SetText(self.tt)


	def Clear(self):
		self.DropList.SelectIndex(0)
	def SelectByAffectId(self,id):
		for x in self.DropList.itemList:
			if x.value == id:
				self.DropList.SelectItem(x)
				break
				
	def SetTitle(self,item):
		self.act.SetText(str(item.textBox.GetText()))
		self.last = self.DropList.basePos
		self.lastS = self.ScrollBar.GetPos()
		self.dropped = 0
		self.selected = item
		if self.OnChange:
			self.OnChange()
		# self.Drop.Hide()
		
	def SetPosition(self,w,h):
		ui.Window.SetPosition(self,w,h)
		if self.down == 1:
			self.Drop.SetPosition(w,h+21)
		else:
			self.Drop.SetPosition(w,h-self.Drop.GetHeight())
		
	def SetSize(self,w,h):
		ui.Window.SetSize(self,w,h)
		self.bg.SetSize(w,h)
		self.Drop.SetSize(w,0)
		self.DropList.SetSize(w-18,self.maxh)
		for x in self.DropList.itemList:
			x.SetSize(w-18,12)
		self.ScrollBar.SetPosition(w-18,0)
		
		
	def ExpandMe(self):
		if self.dropped == 1:
			# self.Drop.Hide()
			self.dropped = 0
		else:
			# self.Drop.Show()
			self.dropped = 1
			
	def OnUpdate(self):
		iter = 6
		if self.Drop.GetHeight() < 50:
			self.ScrollBar.Hide()
		else:
			self.ScrollBar.Show()
			
		if self.dropped == 0 and self.dropstat == 1:
			if self.Drop.GetHeight() <=0:
				self.dropstat = 0
				self.Drop.SetSize(self.Drop.GetWidth(),0)
				self.ScrollBar.SetScrollBarSize(self.Drop.GetHeight())
				self.Drop.Hide()
			else:
				if self.Drop.GetHeight()-iter < 0:
					self.Drop.SetSize(self.Drop.GetWidth(),0)
				else:
					self.Drop.SetSize(self.Drop.GetWidth(),self.Drop.GetHeight()-iter)
					(w,h) = self.GetLocalPosition()
					self.SetPosition(w,h)
						
					
				self.ScrollBar.SetScrollBarSize(self.Drop.GetHeight())
			self.DropList.SetViewItemCount(int(self.Drop.GetHeight()/13))
			self.DropList.SetBasePos(self.last+1)
			self.DropList.SetBasePos(self.last)
		elif self.dropped == 1 and self.dropstat == 0:
			self.Drop.Show()
			self.SetTop()
			if self.Drop.GetHeight() >=self.maxh:
				self.Drop.SetSize(self.Drop.GetWidth(),self.maxh)
				self.ScrollBar.SetScrollBarSize(self.maxh)
				self.dropstat = 1
				self.DropList.SetViewItemCount(7)
				self.ScrollBar.SetPos(self.lastS)
			else:
				self.ScrollBar.SetScrollBarSize(self.Drop.GetHeight()+iter)
				self.Drop.SetSize(self.Drop.GetWidth(),self.Drop.GetHeight()+iter)
				(w,h) = self.GetLocalPosition()
				self.SetPosition(w,h)
			self.DropList.SetViewItemCount(int(self.Drop.GetHeight()/13))
			self.DropList.SetBasePos(self.last+1)
			self.DropList.SetBasePos(self.last)
		
	## BG Hover
	def bgMouseIn(self):
		self.bg.SetColor(0xc00a0a0a)
	def bgMouseOut(self):
		self.bg.SetColor(0xc0000000)

class ShopEditWindow(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.items={}
		self.Edit={}
		self.pop=None
		self.id=0
		self.lastUpdate=0
		self.priceInputBoard=None
		self.__Load()

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()	
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Close()

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("ShopEditWindow.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			self.titleBar = self.GetChild("TitleBar")
			self.titleName = self.GetChild("TitleName")
			self.ItemSlot = self.GetChild("ItemSlot")
			if (app.WJ_COMBAT_ZONE):
				self.boardBattleShop = self.GetChild("BattleShopSubBoard")
			else:
				self.boardBattleShop = None
			try:
				for key in ["BuyButton","SellButton","MiddleTab1","MiddleTab2","MiddleTab2","SmallTab1","SmallTab2","SmallTab3"]:
					self.GetChild(key).Hide()
			except Exception:
				pass
			self.CloseButton = self.GetChild("CloseButton")
		except:
			import exception
			exception.Abort("StoneDialog.__Load_BindObject")
			
		self.CloseButton.SetText(uiScriptLocale.SHOP_EDIT_SHOP_CANCEL)
		self.CloseButton.SetEvent(ui.__mem_func__(self.Close))
		self.titleName.SetText(uiScriptLocale.SHOP_EDIT_SHOP_WINDOW)
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		self.ItemSlot.SAFE_SetButtonEvent("LEFT", "EMPTY", self.OnSelectEmptySlot)
		self.ItemSlot.SAFE_SetButtonEvent("LEFT", "EXIST", self.OnSelectItemSlot)
		self.ItemSlot.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)
		self.ItemSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.ItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
	
		self.Edit["Board"] = ui.BoardWithTitleBar()
		self.Edit["Board"].SetSize(150, 100)
		self.Edit["Board"].AddFlag("movable")
		self.Edit["Board"].AddFlag("animate")
		self.Edit["Board"].SetPosition(0,0)
		self.Edit["Board"].SetTitleName(uiScriptLocale.SHOP_SELECT)
		self.Edit["Board"].SetCloseEvent(self.CloseEdit)
		self.Edit["Board"].Show()
		
		


		self.Edit["ChangePrice"] = ui.Button()
		self.Edit["ChangePrice"].SetParent(self.Edit["Board"])
		self.Edit["ChangePrice"].SetPosition(30,35)
		self.Edit["ChangePrice"].SetUpVisual('d:/ymir work/ui/public/Large_button_01.sub')
		self.Edit["ChangePrice"].SetOverVisual('d:/ymir work/ui/public/Large_button_02.sub')
		self.Edit["ChangePrice"].SetDownVisual('d:/ymir work/ui/public/Large_button_03.sub')
		self.Edit["ChangePrice"].SetText(uiScriptLocale.SHOP_CHANGE_PRICE)
		self.Edit["ChangePrice"].Show()
		
		self.Edit["Remove"] = ui.Button()
		self.Edit["Remove"].SetParent(self.Edit["Board"])
		self.Edit["Remove"].SetPosition(30,65)
		self.Edit["Remove"].SetUpVisual('d:/ymir work/ui/public/Large_button_01.sub')
		self.Edit["Remove"].SetOverVisual('d:/ymir work/ui/public/Large_button_02.sub')
		self.Edit["Remove"].SetDownVisual('d:/ymir work/ui/public/Large_button_03.sub')
		self.Edit["Remove"].SetText(uiScriptLocale.SHOP_REMOVE_ITEM)
		self.Edit["Remove"].Show()
	def __Load(self):
		self.__Load_LoadScript("UIScript/ShopDialog.py")
		self.__Load_BindObject()
	def CloseEdit(self):
		self.Edit["Board"].Hide()
	def Show(self,id):
		if self.IsShow():
			self.Close()
		else:
			ui.ScriptWindow.Show(self)
			net.SendChatPacket("/refresh_shop_items "+id)
			self.id=id
		self.Refresh()
		if self.boardBattleShop != None:
			self.boardBattleShop.Hide()
	def OnPressEscapeKey(self):
		self.Close()
		return True
	def __OnClosePopupDialog(self):
		if self.pop != None:
			if self.pop.IsShow():
				self.pop.Hide()
		self.pop = None	
	def __GetRealIndex(self, i):
		return shop.SHOP_SLOT_COUNT + i
		
	def Close(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.CancelInputPrice()
		self.__OnClosePopupDialog()
		self.Edit["Board"].Hide()
		self.Hide()
		return TRUE
	def Clear(self):
		self.items={}
		self.CancelInputPrice()
		self.__OnClosePopupDialog()
		self.Edit["Board"].Hide()
		self.Refresh()
	def GetItemCount(self,slot):
		try:
			return int(self.items[int(slot)]["count"])
		except KeyError:
			return 0
		
	def GetItemID(self,slot):
		try:
			return int(self.items[int(slot)]["vnum"])
		except KeyError:
			return 0
		
	def AddItem(self,slot,data):
		self.items[int(slot)]=data
		self.Refresh()
	def Refresh(self):
		self.CancelInputPrice()
		self.__OnClosePopupDialog()
		self.Edit["Board"].Hide()
		setItemID=self.ItemSlot.SetItemSlot
		for i in xrange(shop.SHOP_SLOT_COUNT):
			vnum=self.GetItemID(i)
			itemCount = self.GetItemCount(i)
			
			setItemID(i, vnum, itemCount)
		wndMgr.RefreshSlot(self.ItemSlot.GetWindowHandle())
		self.ItemSlot.RefreshSlot()

	def __ShowToolTip(self, slot):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			if int(slot) in self.items.keys():
				it=self.items[int(slot)]
				if it.get("sourceSlot",-1)!=-1:
					self.tooltipItem.SetEditPrivateShopItem(int(it["sourceWindow"]),int(it["sourceSlot"]),it["price"])
				else:
					self.tooltipItem.AppendSellingPrice(it["price"])
					self.tooltipItem.AddItemData(int(it["vnum"]),it["sockets"],it["attrs"])
			else:
				self.tooltipItem.HideToolTip()
			
	def OverInItem(self, slotIndex):
		#slotIndex = self.__GetRealIndex(slotIndex)
		self.ItemSlot.SetUsableItem(FALSE)
		self.__ShowToolTip(slotIndex)

	def OverOutItem(self):
		self.ItemSlot.SetUsableItem(FALSE)
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
	def OnSelectEmptySlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			if player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType:
				return
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			count = player.GetItemCount(attachedInvenType, attachedSlotPos)
				
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)

			
			
			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeinfo.PRIVATE_SHOP_CANNOT_SELL_ITEM)
				return
			
			priceInputBoard = uiCommon.MoneyInputDialog()
			priceInputBoard.SetTitle(localeinfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
			priceInputBoard.SetMaxLength(16)
			priceInputBoard.Open()
			
			#self.ItemSlot.ActivateSlot(int(selectedSlotPos))
			
			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos
	def UnselectItemSlot(self,selectedSlotPos):
		self.Edit["Board"].Hide()
		#self.ItemSlot.DeactivateSlot(int(selectedSlotPos))
		self.CancelInputPrice()
		self.__OnClosePopupDialog()
	def OnSelectItemSlot(self, selectedSlotPos):
		isAttached = mouseModule.mouseController.isAttached()
		#selectedSlotPos = self.__GetRealIndex(selectedSlotPos)
		if isAttached:
			snd.PlaySound("sound/ui/loginfail.wav")
			#self.ItemSlot.DeactivateSlot(int(selectedSlotPos))
			mouseModule.mouseController.DeattachObject()
			self.Edit["Board"].Hide()
		else:
			if not int(selectedSlotPos) in self.items.keys():
				self.Edit["Board"].Hide()
				return

			snd.PlaySound("sound/ui/drop.wav")
			#self.ItemSlot.ActivateSlot(selectedSlotPos)
			self.EditItem(selectedSlotPos)

	def AcceptInputPrice(self):

		if not self.priceInputBoard:
			return True

		text = self.priceInputBoard.GetText()

		if not text:
			return True

		if not text.isdigit():
			return True

		if int(text) <= 0:
			return True
		
		attachedInvenType = self.priceInputBoard.sourceWindowType
		sourceSlotPos = self.priceInputBoard.sourceSlotPos
		targetSlotPos = self.priceInputBoard.targetSlotPos
		price = int(self.priceInputBoard.GetText())
		count = player.GetItemCount(attachedInvenType, sourceSlotPos)
		vnum = player.GetItemIndex(attachedInvenType, sourceSlotPos)
		self.items[int(targetSlotPos)]={
			"vnum":int(vnum),
			"count":int(count),
			"price":int(price),
			"sourceSlot":sourceSlotPos,
			"sourceWindow":attachedInvenType
		}
		snd.PlaySound("sound/ui/pick.wav")
		#self.ItemSlot.DeactivateSlot(targetSlotPos)
		net.SendChatPacket("/update_shop_item add|%d|%d|%d|%d|%s"%(int(self.id),int(targetSlotPos),int(sourceSlotPos),int(attachedInvenType),str(price)))
		self.Refresh()		

		#####

		self.priceInputBoard = None
		return True

	def CancelInputPrice(self):
		self.priceInputBoard = None
		return True
	def EditItem(self,slot):
		self.Edit["ChangePrice"].SetEvent(ui.__mem_func__(self.EditPrice),int(slot))
		self.Edit["Remove"].SetEvent(ui.__mem_func__(self.RemoveItem),int(slot))
		(w,h)=(170,328)
		(x,y)=self.GetLocalPosition()
		self.Edit["Board"].SetPosition((x-w),(y+(h/2)))
		self.Edit["Board"].Show()
	def EditPrice(self,slot):
		self.priceInputBoard = uiCommon.MoneyInputDialog()
		self.priceInputBoard.SetTitle(localeinfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
		self.priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptEditPrice))
		self.priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
		self.priceInputBoard.SetMaxLength(16)
		self.priceInputBoard.Open()
		self.priceInputBoard.targetSlotPos = int(slot)
	def RemoveItem(self,slot):
		self.pop = uiCommon.QuestionDialog()
		self.pop.SetText(uiScriptLocale.SHOP_REMOVE_ITEM_QUEST)
		self.pop.SetAcceptEvent(lambda arg1=str(slot): self.AcceptRemoveItem(arg1))
		self.pop.SetCancelEvent(ui.__mem_func__(self.__OnClosePopupDialog))
		self.pop.Open()
	def AcceptRemoveItem(self,slot):
		if int(slot) in self.items.keys():
			snd.PlaySound("sound/ui/drop.wav")
			net.SendChatPacket("/update_shop_item remove|"+str(self.id)+"|"+str(self.items[int(slot)]["id"]))
			#self.ItemSlot.DeactivateSlot(int(slot))
			del self.items[int(slot)]
		self.Refresh()	
		
		self.__OnClosePopupDialog()
	def AcceptEditPrice(self):

		if not self.priceInputBoard:
			return True

		text = self.priceInputBoard.GetText()

		if not text:
			return True

		if not text.isdigit():
			return True

		if int(text) <= 0:
			return True
		
		targetSlotPos = self.priceInputBoard.targetSlotPos
		price = int(self.priceInputBoard.GetText())
		#self.ItemSlot.DeactivateSlot(int(targetSlotPos))
		self.items[int(targetSlotPos)]["price"]=price
		snd.PlaySound("sound/ui/drop.wav")
		net.SendChatPacket("/update_shop_item price|"+str(self.id)+"|"+str(self.items[int(targetSlotPos)]["id"])+"|"+str(price))
		self.Refresh()	
		self.priceInputBoard = None
		return True
	# def OnUpdate(self):
		# if self.lastUpdate < app.GetGlobalTime():
			# self.lastUpdate=app.GetGlobalTime()+10000
			# if int(self.id)>0:
				# net.SendChatPacket("/refresh_shop_items "+str(self.id))	

class ShopDialog(ui.ScriptWindow):

	Edit={}
	UI={}
	pop=None
	uiNewShopCreate = ShopDialogCreate()
	uiNewShopCreate.Hide()
	uiNewShopEdit = ShopEditWindow()
	uiNewShopEdit.Close()
	tooltip = uiToolTip.ToolTip(220) 
	tooltip.Hide()	
	BoardHeight=40+30
	CurrentEdit=0
	EditBoardY=35
	lastUpdate=0
	sema = 0
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.MoneyActual = 0
		self.withdrawMoneyTime = 0

		self.LoadDialog()
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		self.UI["board"]=ui.BoardWithTitleBar()	
		self.UI["board"].SetParent(self)
		self.UI["board"].SetSize(324+1, self.BoardHeight)
		self.UI["board"].SetTitleName(uiScriptLocale.SHOP_WINDOW_NAME)
		self.UI["board"].SetCloseEvent(self.Close)
		self.UI["board"].Show()
		self.UI["shops"]={}		
		
		self.Edit["Board"] = ui.BoardWithTitleBar()
		self.Edit["Board"].SetParent(self)
		self.Edit["Board"].SetSize(150, 100)
		if POSITION_FIX:
			self.Edit["Board"].SetPosition(250,0)
		else:
			self.Edit["Board"].SetPosition(220,0)
		self.Edit["Board"].SetTitleName(uiScriptLocale.SHOP_SELECT)
		self.Edit["Board"].SetCloseEvent(self.CloseEdit)
		self.Edit["Board"].Hide()	


		self.UI["base_transparente"] = ui.MakeImageBox(self.UI["board"],RUTA_IMG+"base_transparente.tga",9,35)
		self.UI["base_transparente"].Show()

		self.UI["bar_information"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_informacion.tga",4,3)
		self.UI["bar_information"].Show()

		self.UI["icono_formulario"] = ui.MakeImageBox(self.UI["bar_information"],RUTA_IMG+"icono_formulario.tga",80,2)
		self.UI["icono_formulario"].Show()

		self.UI["info_tienda"] = ui.MakeText(self.UI["bar_information"], "Informacion de la tienda" , 110, 3, None)
		self.UI["info_tienda"].Show()

		self.UI["barra_nombre_tienda"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_nombre_tienda.tga",15,38)
		self.UI["barra_nombre_tienda"].Show()

		self.UI["nameText"] = ui.MakeText(self.UI["barra_nombre_tienda"], uiScriptLocale.SHOP_NAME, 0, 1, None)
		self.UI["nameText"].SetWindowHorizontalAlignCenter()
		self.UI["nameText"].SetHorizontalAlignCenter()


		self.UI["barra_tiempo"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_datos_offline.tga",15,88)
		self.UI["barra_tiempo"].Show()


		self.UI["texto_title_tiempo"] = ui.TextLine()
		self.UI["texto_title_tiempo"].SetParent(self.UI["barra_tiempo"])
		self.UI["texto_title_tiempo"].SetPosition(10, 1)
		self.UI["texto_title_tiempo"].SetFeather()
		self.UI["texto_title_tiempo"].SetDefaultFontName()
		self.UI["texto_title_tiempo"].SetOutline()
		self.UI["texto_title_tiempo"].SetText("Tiempo Restante:")
		self.UI["texto_title_tiempo"].Show()


		self.UI["campo_tiempo_1"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"campo_tiempo_1.tga",192,88)
		self.UI["campo_tiempo_1"].Show()

		self.UI["texto_tiempo"] = ui.TextLine()
		self.UI["texto_tiempo"].SetParent(self.UI["campo_tiempo_1"])
		self.UI["texto_tiempo"].SetPosition(4,2)
		self.UI["texto_tiempo"].SetText("")
		self.UI["texto_tiempo"].SetWindowHorizontalAlignCenter()
		self.UI["texto_tiempo"].SetHorizontalAlignCenter()
		self.UI["texto_tiempo"].Show()


		self.UI["bar_information_1"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_informacion.tga",4,195)
		self.UI["bar_information_1"].Show()

		self.UI["info_tienda_1"] = ui.MakeText(self.UI["bar_information_1"], "Yang obtenido de ventas" , 95, 3, None)
		self.UI["info_tienda_1"].Show()

		self.UI["change_name"] = ui.Button()
		self.UI["change_name"].SetParent(self.UI["board"])
		self.UI["change_name"].SetUpVisual(RUTA_IMG+'boton_1.tga')
		self.UI["change_name"].SetOverVisual(RUTA_IMG+'boton_2.tga')
		self.UI["change_name"].SetDownVisual(RUTA_IMG+'boton_3.tga')
		self.UI["change_name"].SetText(uiScriptLocale.SHOP_CHANGE_NAME)
		self.UI["change_name"].Show()

		self.UI["campo_yang_largo"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"campo_yang_largo.tga",15,222)
		self.UI["campo_yang_largo"].Show()

		self.UI["text_yang"] = ui.TextLine()
		self.UI["text_yang"].SetParent(self.UI["campo_yang_largo"])
		self.UI["text_yang"].SetPosition(0,1)
		self.UI["text_yang"].SetText("2.000.000.000 yang")
		self.UI["text_yang"].SetWindowHorizontalAlignCenter()
		self.UI["text_yang"].SetHorizontalAlignCenter()
		self.UI["text_yang"].Show()

		self.UI["barra_retirar_yang"] = ui.MakeImageBox(self.UI["base_transparente"],RUTA_IMG+"barra_datos_offline.tga",15,222+23)
		self.UI["barra_retirar_yang"].Show()

		self.UI["retirar_yang_text"] = ui.TextLine()
		self.UI["retirar_yang_text"].SetParent(self.UI["barra_retirar_yang"])
		self.UI["retirar_yang_text"].SetPosition(10,1)
		self.UI["retirar_yang_text"].SetFeather()
		self.UI["retirar_yang_text"].SetDefaultFontName()
		self.UI["retirar_yang_text"].SetOutline()
		self.UI["retirar_yang_text"].SetText("Retirar Yang:")
		self.UI["retirar_yang_text"].Show()

		self.UI["retirar_yang"] = ui.MakeButton(self.UI["base_transparente"], 200, 222+22 , "", RUTA_IMG, "retiro_yang_1.tga", "retiro_yang_2.tga", "retiro_yang_3.tga")
		self.UI["retirar_yang"].SetEvent(ui.__mem_func__(self.GiveBank))
		self.UI["retirar_yang"].Show()


		self.SetCenterPosition()
		self.AddFlag("movable")
		self.AddFlag("animate")
		self.UpdateSize()

	def ShopBank(self,money):
		self.UI["text_yang"].SetText(localeinfo.NumberToMoneyString(int(money)))
		self.MoneyActual = int(money)

	def GetMoney(self):
		return self.MoneyActual

	def GiveBank(self):
		if self.GetMoney() <= 0:
			return

		if (app.GetTime() < self.withdrawMoneyTime + 5):
			chat.AppendChat(chat.CHAT_TYPE_INFO, "You must wait 5 seconds to withdraw the money again.")
			return

		net.SendChatPacket("/shop_bank")

	def AddEditOption(self,name,text,func):
		self.Edit[name] = ui.Button()
		self.Edit[name].SetParent(self.Edit["Board"])
		self.Edit[name].SetPosition(30,self.EditBoardY)
		self.Edit[name].SetUpVisual('d:/ymir work/ui/public/Large_button_01.sub')
		self.Edit[name].SetOverVisual('d:/ymir work/ui/public/Large_button_02.sub')
		self.Edit[name].SetDownVisual('d:/ymir work/ui/public/Large_button_03.sub')
		self.Edit[name].SetText(text)
		self.Edit[name].Show()
		self.EditBoardY+=30
		self.Edit["Board"].SetSize(150, self.EditBoardY)
		self.Edit[name].SetEvent(func)
		self.UpdateSize()
	def CloseEdit(self):
		if "Board" in self.Edit.keys():
			self.Edit["Board"].Hide()
		self.CurrentEdit=0
		
	def Load(self,data):
		title=data["name"]
		self.sema = data
		if len(title) > 22:
			title = title[:19] + "..."
		gui={}
		gui["nameTextImage"] = ui.MakeImageBox(self.UI["board"], RUTA_IMG+"slot_offline.tga", 24, self.BoardHeight+53)
		gui["nameTextImage"].SAFE_SetStringEvent("MOUSE_OVER_IN", lambda arg=data: self.__ShowToolTip(arg),TRUE)
		gui["nameTextImage"].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideItemToolTip)

		gui["name"] = ui.MakeTextLine(gui["nameTextImage"])
		gui["name"].SetWindowHorizontalAlignCenter()
		gui["name"].SetHorizontalAlignCenter()
		gui["name"].SetText(title)
		gui["name"].SetPosition(0,-1)

		gui["manage"] = ui.MakeButton(self.UI["board"],130, self.BoardHeight,"","d:/ymir work/ui/public/","middle_Button_01.sub","middle_Button_02.sub","middle_Button_03.sub")
		gui["manage"].SetText(uiScriptLocale.SHOP_MANAGE)
		gui["manage"].SetEvent(ui.__mem_func__(self.ManageShop),data)
		gui["manage"].Hide()
		if self.CurrentEdit==data["id"]:
			self.ManageShop(data,1)
		gui["data"]=data

		self.UI["texto_tiempo"].SetText(str(localeinfo.SecondOfflineToDHM(int(data["time"])-int(time.time()))))

		self.ManageShop(data)
		
		self.UI["shops"][str(data["id"])]=gui

		
		
		self.BoardHeight+=30+30+191
		self.UpdateSize()
		
	def __OnClosePopupDialog(self):
		if self.pop != None:
			if self.pop.IsShow():
				self.pop.Hide()
		self.pop = None
		
	def ManageShop(self,data,force=0):
		self.EditBoardY=35
		#self.AddEditOption("change_name",uiScriptLocale.SHOP_CHANGE_NAME,lambda arg1=data: self.OnChangeButtonClick(arg1))
		self.UI["change_name"].SetEvent(ui.__mem_func__(self.OnChangeButtonClick),data)
		# self.AddEditOption("get_yang",uiScriptLocale.SHOP_GET_YANG,lambda arg1=data: self.GetShopYang(arg1))
		# self.AddEditOption("edit",uiScriptLocale.SHOP_EDIT,lambda arg1=data["id"]: self.OnEditButtonClick(arg1))
		# self.AddEditOption("close",uiScriptLocale.SHOP_CLOSE,lambda arg1=data: self.CloseShop(arg1))
		if self.Edit["Board"].IsShow() and self.CurrentEdit==data["id"] and force==0:
			self.Edit["Board"].Hide()
			self.CurrentEdit=0
		else:
			title=data["name"]
			if len(title) > 22:
				title = title[:19] + "..."
			self.Edit["Board"].SetTitleName(title)
			self.Edit["Board"].Hide()
			self.CurrentEdit=data["id"]



	def UpdateSize(self):
		Y=25
		if POSITION_FIX:
			Y=45

		self.UI["change_name"].SetPosition(40,self.UI["board"].GetHeight()-Y-34-95)

		self.UI["create_button"] = ui.MakeButton(self.UI["board"], 145, self.UI["board"].GetHeight()-Y-30,"",RUTA_IMG,"boton_1.tga","boton_2.tga","boton_3.tga")
		self.UI["create_button"].SetText(uiScriptLocale.SHOP_CLOSE)
		self.UI["create_button"].SetEvent(lambda arg=self.sema: self.CloseShop(arg))
		self.UI["create_button"].Show()

		# self.UI["bank"] = ui.MakeButton(self.UI["board"],10, self.UI["board"].GetHeight()-Y-10,"","d:/ymir work/ui/public/","Xlarge_Button_01.sub","Xlarge_Button_02.sub","Xlarge_Button_03.sub")
		# self.UI["bank"].SetText("BANK")
		# self.UI["bank"].SetEvent(lambda : self.OpenBank())
		# self.UI["bank"].Show()
		if POSITION_FIX:
			self.UI["board"].SetSize(324+1, self.BoardHeight+55)
		else:
			self.UI["board"].SetSize(324+1, self.BoardHeight+35)
		if self.BoardHeight < self.EditBoardY:
			self.SetSize(324+1, self.EditBoardY+50+80)
		else:		
			self.SetSize(324+1, self.BoardHeight+60+80)	
		
		#self.UI["board_yang"].SetPosition(-1,self.UI["board"].GetHeight()+5)

	# def OpenBank(self):
		# import uibank
		# self.bank = uibank.BankDialog()
		# self.bank.Show()

	def CreateShop(self):
		self.Hide();
		self.uiNewShopCreate.Show()
		
	def CloseShop(self,shop):
		self.pop = uiCommon.QuestionDialog()
		self.pop.SetText(uiScriptLocale.SHOP_CLOSE_QUEST%(shop["name"]))
		self.pop.SetAcceptEvent(lambda arg1=str(shop["id"]): self.OnCloseShop(arg1))
		self.pop.SetCancelEvent(ui.__mem_func__(self.__OnClosePopupDialog))
		self.pop.Open()
		
	def OnCloseShop(self,id):
		self.__OnClosePopupDialog()
		net.SendChatPacket("/close_shop %d" %(int(id)))
		if len(self.UI["shops"].keys())==1:
			self.Close()
		
	def GetShopYang(self,shop):
		if int(shop["gold"]) <=0:
			self.PopupMessage(uiScriptLocale.SHOP_NOT_EARNED_YANG)
			return
		self.pop = uiCommon.QuestionDialog()
		self.pop.SetText(uiScriptLocale.SHOP_YANG_QUEST%(localeinfo.NumberToMoneyString(shop["gold"]),shop["name"]))
		self.pop.SetAcceptEvent(lambda arg1=str(shop["id"]): self.OnGetYang(arg1))
		self.pop.SetCancelEvent(ui.__mem_func__(self.__OnClosePopupDialog))
		self.pop.Open()
	def AddItem(self,slot,data):
		self.uiNewShopEdit.AddItem(slot,data)
	def ClearItems(self):
		self.uiNewShopEdit.Clear()
	def OnGetYang(self,id):
		self.__OnClosePopupDialog()
		net.SendChatPacket("/shop_yang %d" %(int(id)))
	
	def OnChangeButtonClick(self,shop):
		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(uiScriptLocale.SHOP_ENTER_NEW_NAME)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(lambda arg1=str(shop["id"]): self.OnChangeName(arg1))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.CloseInputNameDialog))
		inputDialog.Open()

		self.inputDialog = inputDialog

	def CloseInputNameDialog(self):
		if not self.inputDialog:
			return
		self.inputDialog = None
		return True

	def OnChangeName(self,id):
		if not self.inputDialog:
			return
		name=self.inputDialog.GetText()
		if not len(name):
			return
		name=name.replace(" ","\\")
		net.SendChatPacket("/shop_name %d %s" %(int(id),name))
		self.CloseInputNameDialog()

	def Destroy(self):
		self.Hide()
		self.__OnClosePopupDialog()
		self.UI={}
		self.wndPopupDialog = None
		self.inputDialog = None
		if self.uiNewShopEdit:
			self.uiNewShopEdit.Close()
		self.uiNewShopEdit = None
	def OnPressEscapeKey(self):
		self.Hide()
		return TRUE
	def Hide(self):
		self.CloseEdit()

		self.__OnClosePopupDialog()
		if self.uiNewShopEdit:
			self.uiNewShopEdit.Close()
		self.__HideItemToolTip()

		ui.ScriptWindow.Hide(self)
	def Close(self):
		self.Hide()
		
	def __ShowToolTip(self,shop):
		if self.tooltip:
			self.tooltip.ClearToolTip()
			self.tooltip.AutoAppendTextLine(uiScriptLocale.SHOP_INFORMATION+str(shop["name"]), titleColor)
			self.tooltip.AppendSpace(5)
			self.tooltip.AutoAppendTextLine(uiScriptLocale.SHOP_EARNED_YANG+str(localeinfo.NumberToMoneyString((shop["gold"]))), POSITIVE_COLOR)	
			self.tooltip.AppendSpace(5)
			self.tooltip.AutoAppendTextLine(uiScriptLocale.SHOP_REST_ITEMS+str(int(shop["sold"])), POSITIVE_COLOR)	
			self.tooltip.AppendSpace(5)
			self.tooltip.AutoAppendTextLine(uiScriptLocale.SHOP_SOLD_ITEMS+str(shop["items"]), POSITIVE_COLOR)	
			self.tooltip.AppendSpace(5)
			self.tooltip.AutoAppendTextLine(uiScriptLocale.SHOP_TIME_TO_CLOSE+str(localeinfo.SecondToDHM(int(shop["time"])-int(time.time()))), NEGATIVE_COLOR)	
			self.tooltip.AppendSpace(5)
			self.tooltip.ShowToolTip()
		
	
	def __HideItemToolTip(self):
		if self.tooltip:
			self.tooltip.HideToolTip()
			
	def OnEditButtonClick(self,id):
		if self.uiNewShopEdit.IsShow():
			self.uiNewShopEdit.Close()
		else:
			self.uiNewShopEdit.Show(str(id))
	def Show(self):
		if len(self.UI["shops"].keys())==0:
			self.CreateShop()
		else:
			ui.ScriptWindow.Show(self)
	def HideAll(self):
		self.BoardHeight=40
		for key,item in self.UI["shops"].iteritems():		
			for k,v in item.iteritems():
				if k !="data":
					v.Hide()
			self.UI["shops"][key]["data"]={}
		self.UI["shops"]={}
	def PopupMessage(self, msg):
		self.wndPopupDialog = uiCommon.PopupDialog()
		self.wndPopupDialog.SetText(msg)
		self.wndPopupDialog.Open()
	def OnUpdate(self):
		if self.lastUpdate < app.GetGlobalTime():
			self.lastUpdate=app.GetGlobalTime()+900
			if "shops" in self.UI.keys():
				if str(self.CurrentEdit) not in self.UI["shops"].keys():
					self.CloseEdit()
		if "create_button" in self.UI.keys():
			if POSITION_FIX:
				self.UI["create_button"].SetPosition(30, self.UI["board"].GetHeight()-45)
			else:
				self.UI["create_button"].SetPosition(165, self.UI["board"].GetHeight()-35-95-25)
				# self.UI["bank"].SetPosition(10, self.UI["board"].GetHeight()-35)
