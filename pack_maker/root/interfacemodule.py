##
## Interface
##
import constInfo
import systemSetting
import wndMgr
import chat
import app
import player
import uiTaskBar
import uiCharacter
import uiInventory
import uiDragonSoul
import uiChat
import uiMessenger
import guild
import net
import item
import uiCards

if app.RENEWAL_MISSION_BOOKS:
	import uiMission

if app.ENABLE_TRACK_WINDOW:
	import uiTrack

if app.ENABLE_ZODIAC_MISSION:
	import ui12zi

if app.ENABLE_RENDER_TARGET:
	import uiRenderTarget

if app.ENABLE_EXCHANGE_LOG:
	import uiExchangeLog

if app.ENABLE_EVENT_MANAGER:
	import uiEventCalendarNew

if app.ENABLE_WIKI:
	import uiWiki

if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
	import uiTeleport

if app.__SKILL_TREE__:
	import uiSkillTree

if app.ENABLE_BLACKJACK_GAME:
	import uiBlackJack

if app.THANOS_GLOVE:
	import uiThanos

if app.__AUTO_HUNT__:
	import uiAutoHunt

if app.__ENABLE_ADVANCE_SKILL_SELECT__:
	import uiSkillSelectNew

import ui
import uiHelp
import uiWhisper
import uiPointReset
import uiShop
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiQuest
#import uiPrivateShopBuilder
import uiCommon
import uiRefine
import uiEquipmentDialog
import uiGameButton
import uiTip
import uiCube
if app.ENABLE_SWITCHBOT:
	import uiSwitchbot
import miniMap
# ACCESSORY_REFINE_ADD_METIN_STONE
import uiselectitem
# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
import uiScriptLocale
if app.ENABLE_BIYOLOG:
	import uiBiyolog
if app.ENABLE_BATTLE_PASS:
	import uiBattlePassEx
if app.ENABLE_OFFLINESHOP_SYSTEM:
	import uiOfflineShopBuilder
	import uiOfflineShop
	import chr
	import net
if app.ENABLE_NEW_PET_SYSTEM:
	import uiPetSystemNew
	import uiChangeName
import event
import localeInfo
# import uiItemShop
import uiTicket
import uiitemshop_v2
import dbg
if app.ENABLE_FISH_GAME:
	import uiFishGame

if app.ENABLE_ITEMSHOP:
	import uiItemShopNew

if app.ENABLE_SHOP_SEARCH_SYSTEM:
	import uiPrivateShopSearch

if app.BL_67_ATTR:
	import uiAttr67Add

if app.ENABLE_KINGDOMS_WAR:
	import uikingdomswar

import uiSpecialInventory

if app.dracaryS_DUNGEON_LIB:
	import uiDungeonTimer

IsQBHide = 0

if app.ENABLE_PVP_TOURNAMENT:
	import uiPvPDuel

if app.ENABLE_SASH_SYSTEM:
	import uisash

if app.ENABLE_MANAGER_BANK_SYSTEM:
	import uibankamanger

if app.ENABLE_SPECIAL_STORAGE:
	import uiSpecialStorage

if app.ENABLE_SHOW_CHEST_DROP:
	import uiChestDropInfo

if app.ENABLE_MINI_GAME_CATCH_KING:
	import uiMiniGameCatchKing

import uicalendar
#import uiEventCalendar
if app.LINK_IN_CHAT:
	import os

if app.ENABLE_DUNGEON_INFO:
	import uiDungeonInfo

if app.ENABLE_DUNGEON_INFO:
	import uitabledungeon
#import uidiscord
import uiguias
import grp

if app.ELEMENT_SPELL_WORLDARD:
	import uielementspelladd
	import uielementchange
if app.ENABLE_GEM_SYSTEM:
	import uiGem
import uicz_estadisticas
import uiswitch
import uitablabonus

if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
	import uiAuto

if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
	import uiBuffNPC

if app.ENABLE_MAINTENANCE_SYSTEM:
	import uiMaintenance

if app.ENABLE_AURA_SYSTEM:
	import uiAura

if app.ENABLE_RARITY_REFINE:
	import uiRefineRarity

if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
	import uiSetCustomAttribute

class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2
	
	wndParty = None
	
	if app.ENABLE_EXPANDED_MONEY_TASKBAR:
		wndExpandedMoneyTaskBar = None

	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		if app.ENABLE_GEM_SYSTEM:
			self.wndGemShop = None
		if app.ENABLE_TRACK_WINDOW:
			self.wndTrackWindow = None
		if app.ENABLE_EXCHANGE_LOG:
			self.wndExchangeLog = None
		if app.ENABLE_RENDER_TARGET:
			self.wndRenderTarget = None
		if app.RENEWAL_MISSION_BOOKS:
			self.wndBookMission = None
		self.windowOpenPosition = 0
		if app.ENABLE_BLACKJACK_GAME:
			self.wndBlackJackGame = None
		if app.ENABLE_FISH_GAME:
			self.wndFishGame=None
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None
		self.wndGiftBox = None
		if app.ENABLE_ZODIAC_MISSION:
			self.wnd12ziReward = None
			self.wnd12ziTimer = None
		if app.ENABLE_WIKI:
			self.wndWiki = None
		if app.ENABLE_RARITY:
			self.wndRarityQueque = None
		if app.ENABLE_SHOW_CHEST_DROP:
			self.wndChestDropInfo = None
		if app.ENABLE_EVENT_MANAGER:
			self.wndEventManager = None
			self.wndEventIcon = None
		if app.ENABLE_BATTLE_PASS:
			self.wndBattlePassEx = None
		if app.ENABLE_BIYOLOG:
			self.wndBio = None
		if app.ENABLE_DUNGEON_INFO:
			self.wndDungeonInfo = None
		if app.__SKILL_TREE__:
			self.wndSkillTree = None
		if app.__AUTO_HUNT__:
			self.wndAutoHunt = None

		if app.ENABLE_PVP_TOURNAMENT:
			self.wndPvPDuel=None
			self.wndPvPDuelPanel=None

		self.questButtonList = []

		if app.dracaryS_DUNGEON_LIB:
			self.missionBoard = None
			self.wndDungeonTimer=None
		
		if app.ENABLE_ITEMSHOP:
			self.wndItemShop=None

		# ITEM_MALL
		self.mallPageDlg = None
		# END_OF_ITEM_MALL
		
		if app.ENABLE_SHOP_SEARCH_SYSTEM:
			self.wndPrivateShopSearch=None
		
		if app.ENABLE_OFFLINESHOP_SYSTEM:
			self.dlgOfflineShop=None
			self.dlgOfflineShopPanel=None
			self.offlineShopBuilder=None
			self.dlgShopMessage=None

		if app.ENABLE_DROP_ITEM_WORLDARD:
			self.wndDropItem = None

		self.wndTableBonus = None

		if app.ENABLE_NEW_PET_SYSTEM:
			self.wndPet=None
			self.change_window=None

		self.wndBattlePass = None
		self.wndBattlePassButton = None

		if app.ENABLE_MINI_GAME_CATCH_KING:
			self.wndCatchKingGame = None
			self.wndCatchKingIcon = None

		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			self.wndCubeRenewal = None
		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = None
			self.wndSwitchbotMenu = None
			self.wndSwitchbotManual = None
		self.wndWeb = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.managerAccountBank = None
		self.wndInventory = None
		self.wndInventoryNew = None
		self.wndInventoryGold = None
		self.wndExpandedTaskBar = None
		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
		self.wndChat = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		self.wndGuildBuilding = None

		if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
			self.wndSetCustomAttribute = None

		if app.ENABLE_MAINTENANCE_SYSTEM:
			self.wndMaintenance = None

		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage = None

		if app.LINK_IN_CHAT:
			self.OpenLinkQuestionDialog = None

		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			self.wndAutoWindow = None

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow = None
			self.wndBuffNPCCreateWindow = None

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			self.wndWarpWindow = None

		self.wndAlmacenMenu = None

		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		event.SetInterfaceWindow(self)

		if app.WJ_ENABLE_TRADABLE_ICON:
			self.onTopWindow = player.ON_TOP_WND_NONE


	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)
	
	def OpenCombatZoneWindow(self):
		if player.IsCombatZoneMap():
			self.OnAskCombatZoneQuestionDialog()
		else:
			net.SendCombatZoneRequestActionPacket(net.COMBAT_ZONE_ACTION_OPEN_RANKING, net.COMBAT_ZONE_EMPTY_DATA)

	def __OnClickGiftButton(self):
		if self.wndGameButton:
			if not self.wndGiftBox.IsShow():
				self.wndGiftBox.Open()
			else:
				self.wndGiftBox.Close()

	def ClearGift(self):
		if self.wndGameButton:
			self.wndGameButton.HideGiftButton()
		if self.wndGiftBox:
			self.wndGiftBox.Clear()
			self.wndGiftBox.Refresh()
	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):

		wndChat = uiChat.ChatWindow()

		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))


		
	def __MakeTaskBar(self):
		import uiGift
		wndGiftBox=uiGift.GiftDialog()
		wndGiftBox.Hide()
		self.wndGiftBox=wndGiftBox

		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		#self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_GOLD, ui.__mem_func__(self.ToggleGoldWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		#if app.ENABLE_EVENT_MANAGER:
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CALENDAR, ui.__mem_func__(self.OpenEventCalendar))
		#else:
		#self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CALENDAR, ui.__mem_func__(self.CalendarDialog))
		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, ui.__mem_func__(self.ToggleDragonSoulWindow))

			if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_AUTO_WINDOW, ui.__mem_func__(self.ToggleAutoWindow))

			if app.ENABLE_SWITCHBOT:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_SWITCHBOT, ui.__mem_func__(self.ToggleSwitchbotWindow))

			if app.ENABLE_WIKI:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_WIKI, ui.__mem_func__(self.OpenWikiWindow))

			if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_BUFF_NPC, ui.__mem_func__(self.BuffNPCOpenWindow))

			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()
		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

		self.wndEnergyBar = None

		if app.ENABLE_ENERGY_SYSTEM:
			wndEnergyBar = uiTaskBar.EnergyBar()
			wndEnergyBar.LoadWindow()
			self.wndEnergyBar = wndEnergyBar
		
		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND_MONEY, ui.__mem_func__(self.ToggleExpandedMoneyButton))
			self.wndExpandedMoneyTaskBar = uiTaskBar.ExpandedMoneyTaskBar()
			self.wndExpandedMoneyTaskBar.LoadWindow()
			if self.wndInventory:
				self.wndInventory.SetExpandedMoneyBar(self.wndExpandedMoneyTaskBar)

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def CalendarDialog(self):
		pass
		if self.wndCalendar.IsShow():
			self.wndCalendar.Close()
		else:
			net.CalendarOpen()

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("HELP", ui.__mem_func__(self.__OnClickHelpButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))
		wndGameButton.SetButtonEvent("GIFT", ui.__mem_func__(self.__OnClickGiftButton))
		wndGameButton.SetButtonEvent("COMBAT_ZONE", ui.__mem_func__(self.OpenCombatZoneWindow))
		wndGameButton.SetButtonEvent("BOSS_EVENT", ui.__mem_func__(self.OpenBOSS_EVENT))
		wndGameButton.SetButtonEvent("METIN_EVENT", ui.__mem_func__(self.OpenMETIN_EVENT))

		self.wndGameButton = wndGameButton

	def OpenBOSS_EVENT(self):
		import event
		event.QuestButtonClick(constInfo.BOSS_EVENT)

	def CheckBossOpenOrNot(self):
		if constInfo.BOSS_EVENT_STATUS == 0:
			self.wndGameButton.HideBossButton()
		else:
			self.wndGameButton.ShowBossButton()

	def OpenMETIN_EVENT(self):
		import event
		event.QuestButtonClick(constInfo.METIN_EVENT)

	def CheckMetinOpenOrNot(self):
		if constInfo.METIN_EVENT_STATUS == 0:
			self.wndGameButton.HideMetinButton()
		else:
			self.wndGameButton.ShowMetinButton()

	def CheckCombatOpenOrNot(self):
		if constInfo.COMBAT_ZONE == 0:
			self.wndGameButton.HideCombatButton()
		else:
			self.wndGameButton.ShowCombatButton()

	def __IsChatOpen(self):
		return True

	if app.ENABLE_REFINE_RENEWAL:
		def CheckRefineDialog(self, isFail):
			self.dlgRefineNew.CheckRefine(isFail)

	if app.ENABLE_RARITY_REFINE:
		def CheckRefineRarityDialog(self, isFail):
			self.dlgRefineRarity.CheckRefine(isFail)

	def __MakeWindows(self):
		wndCharacter = uiCharacter.CharacterWindow()
		wndInventory = uiInventory.InventoryWindow()
		wndInventoryNew = uiSpecialInventory.InventoryWindowNew()
		wndInventory.SetTop()
		wndInventoryNew.SetTop()
		wndInventoryGold = uiInventory.NewGoldWindow()
		wndInventory.BindInterfaceClass(self)
		wndInventoryNew.BindInterfaceClass(self)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			wndDragonSoul = uiDragonSoul.DragonSoulWindow()
			wndDragonSoul.BindInterfaceClass(self)
			wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()
		else:
			wndDragonSoul = None
			wndDragonSoulRefine = None


		wndMiniMap = uiMiniMap.MiniMap()
		wndSafebox = uiSafebox.SafeboxWindow()
		#if app.WJ_ENABLE_TRADABLE_ICON:
		wndSafebox.BindInterface(self)
		# ITEM_MALL
		wndMall = uiSafebox.MallWindow()
		self.wndMall = wndMall
		# END_OF_ITEM_MALL

		self.wndAlmacenMenu = uiSafebox.AlmacenMenu()
		self.wndAlmacenMenu.Hide()


		wndChatLog = uiChat.ChatLogWindow()
		wndChatLog.BindInterface(self)

		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory
		self.wndInventoryNew = wndInventoryNew
		self.wndInventoryGold = wndInventoryGold
		self.wndDragonSoul = wndDragonSoul
		self.wndDragonSoulRefine = wndDragonSoulRefine
		self.wndMiniMap = wndMiniMap
		self.wndMiniMap.BindInterface(self)
		self.wndSafebox = wndSafebox
		self.wndChatLog = wndChatLog

		if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
			self.wndSetCustomAttribute = uiSetCustomAttribute.SetCustomAttributeWindow()
			self.wndSetCustomAttribute.BindInterface(self)
			self.wndSetCustomAttribute.SetInven(self.wndInventory)

		if app.ENABLE_SHOW_CHEST_DROP:
			self.wndChestDropInfo = uiChestDropInfo.ChestDropInfoWindow()

		if app.ENABLE_KINGDOMS_WAR:
			self.wndKingdomsWar = uikingdomswar.Window()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
			self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
			self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)

		if app.ENABLE_MINI_GAME_CATCH_KING:
			self.wndCatchKingGame = uiMiniGameCatchKing.MiniGameCatchKing()

		if app.BL_67_ATTR:
			self.wndAttr67Add = uiAttr67Add.Attr67AddWindow()
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.wndAttr67Add.BindInterface(self)
				self.wndAttr67Add.SetInven(self.wndInventory)
				self.wndInventory.BindWindow(self.wndAttr67Add)
				#self.wndInventoryNew.BindWindow(self.wndAttr67Add)

		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			self.wndAutoWindow = uiAuto.AutoWindow()

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = uiSwitchbot.SwitchbotWindow()
			self.wndSwitchbotManual = uiswitch.DopadorManual()
			self.wndSwitchbotManual.Hide()
			self.wndSwitchbotMenu = uiswitch.DopadorMenu()
			self.wndSwitchbotMenu.Hide()
			self.wndSwitchbotMenu.BindInterface(self)

		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage = uiSpecialStorage.SpecialStorageWindow()
			self.wndSpecialStorage.BindInterface(self)
		else:
			self.wndSpecialStorage = None

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow = uiBuffNPC.BuffNPCWindow()
			self.wndBuffNPCCreateWindow = uiBuffNPC.BuffNPCCreateWindow()
			self.wndBuffNPCCreateWindow.SetInven(self.wndInventory)

		if app.ENABLE_MAINTENANCE_SYSTEM:
			self.wndMaintenance = uiMaintenance.MaintenanceBoard()

		if app.THANOS_GLOVE:
			self.wndThanosGlove = uiThanos.ThanosWindow()
			self.wndThanosGlove.BindInventory(self.wndInventory)

		if app.ENABLE_AURA_SYSTEM:
			wndAura = uiAura.AuraWindow()
			self.wndAura = wndAura
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.wndAura.BindInterface(self)
				self.wndAura.SetInven(self.wndInventory)

		self.wndczestadisticas = uicz_estadisticas.CombatZoneEstadisticas()
		self.wndczestadisticas.Hide()

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			self.wndWarpWindow = uiTeleport.TeleportWindow()

	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgExchange.BindInterface(self)
			self.dlgExchange.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgExchange)
			# -----------------------------------------------------------------------------------------
			# Inventário Especial
			self.dlgExchange.SetInvenNew(self.wndInventoryNew)
			self.wndInventoryNew.BindWindow(self.dlgExchange)
			# -----------------------------------------------------------------------------------------
			# -----------------------------------------------------------------------------------------
			#self.wndInventoryNew.BindWindow(self.dlgExchange)
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		self.dlgExchange.Hide()

		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		if app.ENABLE_MANAGER_BANK_SYSTEM:
			self.managerAccountBank = uibankamanger.BankGui()
			self.managerAccountBank.Hide()
		
		self.dlgShop = uiShop.ShopDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgShop.BindInterface(self)
		self.dlgShop.LoadDialog()
		self.dlgShop.Hide()
		
		self.wndTicket = uiTicket.TicketWindow()
		self.wndTicket.Hide()

		# self.wndItemShop = uiItemShop.ItemShopWindow()
		# self.wndItemShop.Hide()
		
		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uiSystem.SystemDialog()
		self.dlgSystem.LoadDialog()
		self.dlgSystem.SetOpenHelpWindowEvent(ui.__mem_func__(self.OpenHelpWindow))

		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.BindInterface(self)
		self.tooltipItem.Hide()

		if app.ENABLE_SHOW_CHEST_DROP:
			self.wndChestDropInfo.SetTooltipItem(self.tooltipItem)

		self.Itemshop_v2 = uiitemshop_v2.Itemshop()
		self.Itemshop_v2.BindToolTipItem(self.tooltipItem)

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		self.dlgRefineNew = uiRefine.RefineDialogNew()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgRefineNew.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.dlgRefineNew)
			#self.wndInventoryNew.BindWindow(self.dlgRefineNew)
		self.dlgRefineNew.Hide()

		if app.ENABLE_RARITY_REFINE:
			self.dlgRefineRarity = uiRefineRarity.RefineRarityDialog()
			if app.WJ_ENABLE_TRADABLE_ICON:
				self.dlgRefineRarity.SetInven(self.wndInventory)
				self.wndInventory.BindWindow(self.dlgRefineRarity)
			self.dlgRefineRarity.Hide()

		if app.ELEMENT_SPELL_WORLDARD:
			self.dlgElementSpell = uielementspelladd.ElementsSpellAdd()
			self.dlgElementSpell.Hide()

			self.dlgElementSpellChange = uielementchange.ElementsSpellChange()
			self.dlgElementSpellChange.Hide()

		#self.wndDiscord = uidiscord.Discord()
		#self.wndDiscord.LoadWindow()
		#self.wndDiscord.Show()

		#self.wndGuias = uiguias.Guias()
		#self.wndGuias.LoadWindow()
		#self.wndGuias.Show()

	def __MakeTableBonus(self):
		self.wndTableBonus = uitablabonus.TableBonusWindows()
		self.wndTableBonus.LoadWindow()
		self.wndTableBonus.Hide()

	def __MakeHelpWindow(self):
		self.wndHelp = uiHelp.HelpWindow()
		self.wndHelp.LoadDialog()
		self.wndHelp.SetCloseEvent(ui.__mem_func__(self.CloseHelpWindow))
		self.wndHelp.Hide()

	def __MakeTipBoard(self):
		if app.__RENEWAL_NOTICE__:
			self.tipBoard = uiTip.TipBoardNew()
		else:
			self.tipBoard = uiTip.TipBoard()

		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()
		
		if app.dracaryS_DUNGEON_LIB:
			self.missionBoard = uiTip.MissionBoard()
			self.missionBoard.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	def __MakeCubeWindow(self):
		self.wndCube = uiCube.CubeWindow()
		self.wndCube.LoadWindow()
		self.wndCube.Hide()

	if app.ENABLE_SASH_SYSTEM:
		def __MakeSashWindow(self):
			self.wndSashCombine = uisash.CombineWindow()
			self.wndSashCombine.LoadWindow()
			self.wndSashCombine.Hide()
			
			self.wndSashAbsorption = uisash.AbsorbWindow()
			self.wndSashAbsorption.LoadWindow()
			self.wndSashAbsorption.Hide()
			
			if self.wndInventory:
				self.wndInventory.SetSashWindow(self.wndSashCombine, self.wndSashAbsorption)
				self.wndInventoryNew.SetSashWindow(self.wndSashCombine, self.wndSashAbsorption)

	def __MakeCubeResultWindow(self):
		self.wndCubeResult = uiCube.CubeResultWindow()
		self.wndCubeResult.LoadWindow()
		self.wndCubeResult.Hide()

	def __MakeCardsInfoWindow(self):
		self.wndCardsInfo = uiCards.CardsInfoWindow()
		self.wndCardsInfo.LoadWindow()
		self.wndCardsInfo.Hide()

	def __MakeCardsWindow(self):
		self.wndCards = uiCards.CardsWindow()
		self.wndCards.LoadWindow()
		self.wndCards.Hide()
		
	def __MakeCardsIconWindow(self):
		self.wndCardsIcon = uiCards.IngameWindow()
		self.wndCardsIcon.LoadWindow()
		self.wndCardsIcon.Hide()

	if app.ENABLE_MINI_GAME_CATCH_KING:
		def __MakeCatchKingIconWindow(self):
			self.wndCatchKingIcon = uiMiniGameCatchKing.IngameWindow()
			self.wndCatchKingIcon.LoadWindow()
			self.wndCatchKingIcon.Hide()

	if app.__ENABLE_ADVANCE_SKILL_SELECT__:
		def __MakeSkillSelectWindow(self):
			self.wndSkillSelect = uiSkillSelectNew.SkillSelectWindowNew()
			self.wndSkillSelect.LoadWindow()
			self.wndSkillSelect.Hide()

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiselectitem.SelectItemWindow()
		self.wndItemSelect.Hide()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	#def __MakeCalendar(self):
		#self.wndCalendarADM = uicalendar.UiCalendarAdm()
		#self.wndCalendarADM.LoadWindow()
		#self.wndCalendarADM.Hide()

		#self.wndCalendar = uicalendar.UiCalendar()
		#self.wndCalendar.LoadWindow()
		#self.wndCalendar.()
		#self.wndCalendar.Close()
		
		#self.wndCalendar = uiEventCalendar.EventCalendarWindow()
		#self.wndCalendar.ClearEvents()
		#self.wndCalendar.Close()

		#self.wndCalendarIcon = uicalendar.CalendarIngameWindow()
		#self.wndCalendarIcon.LoadWindow()
		#self.wndCalendarIcon.Show()

	if app.ENABLE_DUNGEON_INFO:
		def __MakeTableDungeonInfo(self):
			self.wndTableDungeonInfo = uitabledungeon.TableDungeonWindows()
			self.wndTableDungeonInfo.Hide()


	if app.ENABLE_DROP_ITEM_WORLDARD:
		def __MakeDropItem(self):
			import uidropitem
			self.wndDropItem = uidropitem.DropItemWindows()
			self.wndDropItem.Hide()
		def OpenDropItem(self):
			if self.wndDropItem == None:
				self.__MakeDropItem()
			if self.wndDropItem.IsShow():
				self.wndDropItem.Close()
			else:
				self.wndDropItem.Show()

	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def __MakeCubeRenewal(self):
			import uicuberenewal
			self.wndCubeRenewal = uicuberenewal.CubeRenewalWindows()
			self.wndCubeRenewal.BindToolTipItem(self.tooltipItem)
			self.wndCubeRenewal.Hide()


		def __MakeBattlePass(self):
			import uibattlepass
			self.wndBattlePass = uibattlepass.UiBattlePass()
			self.wndBattlePass.Hide()

			self.wndBattlePassButton = uibattlepass.UiBattlePassButton()
			self.wndBattlePassButton.Hide()

	def __MakeRenderTooltip(self):
		import uirendertooltip
		self.rendertooltip = uirendertooltip.RenderTooltip(self.tooltipItem)
		self.rendertooltip.CloseRenderTooltip()

	def MakeInterface(self):
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeHelpWindow()
		self.__MakeTipBoard()
		self.__MakeWebWindow()

		self.__MakeTableBonus()
		self.__MakeBattlePass()

		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			self.__MakeCubeRenewal()

		self.__MakeCubeWindow()
		if app.ENABLE_SASH_SYSTEM:
			self.__MakeSashWindow()
		self.__MakeCubeResultWindow()
		self.__MakeCardsInfoWindow()
		self.__MakeCardsWindow()
		self.__MakeCardsIconWindow()
		if app.ENABLE_MINI_GAME_CATCH_KING:
			self.__MakeCatchKingIconWindow()
		#self.__MakeCalendar()

		if app.ENABLE_DROP_ITEM_WORLDARD:
			self.__MakeDropItem()

		if app.ENABLE_DUNGEON_INFO:
			self.__MakeTableDungeonInfo()

		self.__MakeRenderTooltip()

		if app.__ENABLE_ADVANCE_SKILL_SELECT__:
			self.__MakeSkillSelectWindow()

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.__MakeItemSelectWindow()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		
		if app.ENABLE_ZODIAC_MISSION:
			self.__Make12ziTimerWindow()
			self.__Make12ziRewardWindow()

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		self.wndInventoryNew.SetItemToolTip(self.tooltipItem)
		
		if app.ENABLE_SASH_SYSTEM:
			self.wndSashAbsorption.SetItemToolTip(self.tooltipItem)
			self.wndSashCombine.SetItemToolTip(self.tooltipItem)
			
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
			self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		self.wndCube.SetItemToolTip(self.tooltipItem)
		self.wndCubeResult.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_AURA_SYSTEM:
			self.wndAura.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage.SetItemToolTip(self.tooltipItem)

		# ITEM_MALL
		self.wndMall.SetItemToolTip(self.tooltipItem)
		# END_OF_ITEM_MALL

		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			self.wndAutoWindow.SetSkillToolTip(self.tooltipSkill)
			self.wndAutoWindow.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow.SetSkillToolTip(self.tooltipSkill)

		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)

		# if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			# self.wndPrivateShopSearch.SetItemToolTip(self.tooltipItem)

		self.__InitWhisper()
		self.DRAGON_SOUL_IS_QUALIFIED = False

		if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
			if self.wndSetCustomAttribute:
				self.wndSetCustomAttribute.SetItemToolTip(self.tooltipItem)

	if app.LINK_IN_CHAT:
		def AnswerOpenLink(self, answer):
			if not self.OpenLinkQuestionDialog:
				return

			self.OpenLinkQuestionDialog.Close()
			self.OpenLinkQuestionDialog = None

			if not answer:
				return

			link = constInfo.link
			
			
	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
			elif "msg" == type and str(tokens[1]) != player.GetMainCharacterName():
				self.OpenWhisperDialog(str(tokens[1]))				
			elif app.LINK_IN_CHAT and "web" == type and tokens[1].startswith("httpXxX") or "web" == type and tokens[1].startswith("httpsXxX"):
					os.system("start " + tokens[1].replace("XxX", "://").replace("&","^&"))
			elif app.LINK_IN_CHAT and "sysweb" == type:
				os.system("start " + tokens[1].replace("XxX", "://"))
			elif "chat_mp" == type:    
				self.OpenWhisperDialog(str(tokens[1]))

	## Make Windows & Dialogs
	################################
	def OpenGift(self):
		if self.wndGameButton:
			self.wndGameButton.ShowGiftButton()
	
	def Close(self):
		if app.RENEWAL_MISSION_BOOKS:
			if self.wndBookMission:
				self.wndBookMission.Close()
				self.wndBookMission.Destroy()
				self.wndBookMission = None
		if app.ENABLE_GEM_SYSTEM:
			if self.wndGemShop:
				self.wndGemShop.Close()
				self.wndGemShop.Destroy()
				self.wndGemShop=None
		if app.ENABLE_EXCHANGE_LOG:
			if self.wndExchangeLog:
				self.wndExchangeLog.Close()
				self.wndExchangeLog.Destroy()
				self.wndExchangeLog = None
		if app.ENABLE_FISH_GAME:
			if self.wndFishGame:
				self.wndFishGame.Hide()
				self.wndFishGame.Destroy()
				self.wndFishGame=None
		if app.ENABLE_TRACK_WINDOW:
			if self.wndTrackWindow:
				self.wndTrackWindow.Close()
				self.wndTrackWindow.Destroy()
				self.wndTrackWindow=None
		if app.ENABLE_RENDER_TARGET:
			if self.wndRenderTarget:
				self.wndRenderTarget.Close()
				self.wndRenderTarget.Destroy()
				self.wndRenderTarget=None
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Hide()
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if app.__SKILL_TREE__:
			if self.wndSkillTree:
				self.wndSkillTree.Close()
				self.wndSkillTree.Destroy()
				self.wndSkillTree = None

		if app.__AUTO_HUNT__:
			if self.wndAutoHunt:
				self.wndAutoHunt.Close()
				self.wndAutoHunt.Destroy()
				self.wndAutoHunt = None

		if app.ENABLE_BLACKJACK_GAME:
			if self.wndBlackJackGame:
				self.wndBlackJackGame.Close()
				self.wndBlackJackGame.Destroy()
				self.wndBlackJackGame=None

		if app.ENABLE_ZODIAC_MISSION:
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Hide()
				self.wnd12ziTimer=None
			if self.wnd12ziReward:
				self.wnd12ziReward.Hide()
				self.wnd12ziReward=None

		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.Hide()
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}
		
		if app.ENABLE_WIKI:
			if self.wndWiki:
				self.wndWiki.Close()
				self.wndWiki.Destroy()
				self.wndWiki=None
		
		if app.ENABLE_RARITY:
			if self.wndRarityQueque:
				self.wndRarityQueque.Hide()
				self.wndRarityQueque.Destroy()
				self.wndRarityQueque = None

		if app.ENABLE_EVENT_MANAGER:
			if self.wndEventManager:
				self.wndEventManager.Hide()
				self.wndEventManager.Destroy()
				self.wndEventManager = None
			if self.wndEventIcon:
				self.wndEventIcon.Hide()
				self.wndEventIcon.Destroy()
				self.wndEventIcon = None
	
		if app.ENABLE_ITEMSHOP:
			if self.wndItemShop:
				self.wndItemShop.Hide()
				self.wndItemShop.Destroy()
				self.wndItemShop = None
	
		if app.ENABLE_DUNGEON_INFO:
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Close()
				self.wndDungeonInfo.Destroy()
				self.wndDungeonInfo = None

		if app.ENABLE_MINI_GAME_CATCH_KING:
			if self.wndCatchKingGame:
				self.wndCatchKingGame.Destroy()
				del self.wndCatchKingGame
			if self.wndCatchKingIcon:
				self.wndCatchKingIcon.Destroy()
				del self.wndCatchKingIcon

		if self.wndGiftBox:
			self.wndGiftBox.Clear()
			self.wndGiftBox.Hide()
			self.wndGiftBox.Destroy()
		del self.wndGiftBox
		
		if app.ENABLE_BATTLE_PASS:
			if self.wndBattlePassEx:
				self.wndBattlePassEx.Close()
				self.wndBattlePassEx.Destroy()
				self.wndBattlePassEx = None

		if app.ENABLE_NEW_PET_SYSTEM:
			if self.wndPet:
				self.wndPet.Close()
				self.wndPet.Destroy()
				del self.wndPet
				self.wndPet = None

			if self.change_window:
				self.change_window.Hide()
				self.change_window.Destroy()
				del self.change_window
				self.change_window = None

		#if self.wndDiscord:
			#self.wndDiscord.Destroy()

		#if self.wndGuias:
			#self.wndGuias.Destroy()

		if self.wndChat:
			self.wndChat.Hide()
			self.wndChat.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Hide()
			self.wndTaskBar.Destroy()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()
			self.wndExpandedTaskBar.Destroy()

		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()
			self.wndEnergyBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Hide()
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Hide()
			self.wndInventory.Destroy()
		if self.wndInventoryNew:
			self.wndInventoryNew.Hide()
			self.wndInventoryNew.Destroy()

		if self.wndInventoryGold:
			self.wndInventoryGold.Hide()
			self.wndInventoryGold.Destroy()

		if self.wndDragonSoul:
			self.wndDragonSoul.Hide()
			self.wndDragonSoul.Destroy()

		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Hide()
			self.wndDragonSoulRefine.Destroy()
		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndSpecialStorage:
				self.wndSpecialStorage.Hide()
				self.wndSpecialStorage.Destroy()
		if self.dlgExchange:
			self.dlgExchange.Hide()
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Hide()
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Hide()
			self.dlgShop.Destroy()

		if self.wndTicket:
			self.wndTicket.Hide()
			self.wndTicket.Destroy()
			
		# if self.wndItemShop:
			# self.wndItemShop.Destroy()
			
		if self.dlgRestart:
			self.dlgRestart.Hide()
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Hide()
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Hide()
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Hide()
			self.wndSafebox.Destroy()

		if self.wndWeb:
			self.wndWeb.Hide()
			self.wndWeb.Destroy()
			self.wndWeb = None

		if self.wndMall:
			self.wndMall.Hide()
			self.wndMall.Destroy()

		if self.Itemshop_v2:
			self.Itemshop_v2.Hide()
			self.Itemshop_v2.Destroy()
			
		if app.ENABLE_MANAGER_BANK_SYSTEM:
			if self.managerAccountBank:
				self.managerAccountBank.Hide()
				self.managerAccountBank.Destroy()
			
		if self.wndParty:
			self.wndParty.Hide()
			self.wndParty.Destroy()
		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()
				self.wndSwitchbot.Destroy()

			if self.wndSwitchbotMenu:
				self.wndSwitchbotMenu.Close()
				self.wndSwitchbotMenu.Destroy()

			if self.wndSwitchbotManual:
				self.wndSwitchbotManual.Close()
				self.wndSwitchbotManual.Destroy()


		if self.wndczestadisticas:
			self.wndczestadisticas.Close()
			self.wndczestadisticas.Destroy()

		if self.wndAlmacenMenu:
			self.wndAlmacenMenu.Close()
			self.wndAlmacenMenu.Destroy()

		if self.wndHelp:
			self.wndHelp.Hide()
			self.wndHelp.Destroy()
		if self.wndCardsInfo:
			self.wndCardsInfo.Destroy()

		if self.wndCards:
			self.wndCards.Destroy()

		if self.wndCardsIcon:
			self.wndCardsIcon.Destroy()
		if self.wndCube:
			self.wndCube.Hide()
			self.wndCube.Destroy()

		if self.wndCubeResult:
			self.wndCubeResult.Hide()
			self.wndCubeResult.Destroy()


		if app.ENABLE_DUNGEON_INFO:
			if self.wndTableDungeonInfo:
				self.wndTableDungeonInfo.Close()
				self.wndTableDungeonInfo.Destroy()

		if self.rendertooltip:
			self.rendertooltip.Hide()
			self.rendertooltip.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Hide()
			self.wndMessenger.Destroy()

		if self.wndGuild:
			self.wndGuild.Hide()
			self.wndGuild.Destroy()

		#if self.wndCalendarIcon:
			#self.wndCalendarIcon.Show()

		#if self.wndCalendarADM:
			#self.wndCalendarADM.Destroy()

		#if self.wndCalendar:
		#	self.wndCalendar.Hide()
		#	self.wndCalendar.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Close()
			self.dlgRefineNew.Destroy()

		if app.ENABLE_RARITY_REFINE:
			if self.dlgRefineRarity:
				self.dlgRefineRarity.Close()
				self.dlgRefineRarity.Destroy()

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Hide()
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Hide()
			self.wndGameButton.Destroy()
		
		if app.ENABLE_SHOW_CHEST_DROP:
			if self.wndChestDropInfo:
				del self.wndChestDropInfo

		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			if self.wndAutoWindow:
				self.wndAutoWindow.Destroy()

		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Hide()
			self.mallPageDlg.Destroy()

		if app.BL_67_ATTR:
			if self.wndAttr67Add:
				del self.wndAttr67Add

		# END_OF_ITEM_MALL

		if app.ENABLE_MAINTENANCE_SYSTEM:
			if self.wndMaintenance:
				self.wndMaintenance.Hide()
				self.wndMaintenance.Destroy()

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			if self.wndWarpWindow:
				self.wndWarpWindow.Destroy()

		# ACCESSORY_REFINE_ADD_METIN_STONE
		if self.wndItemSelect:
			self.wndItemSelect.Hide()
			self.wndItemSelect.Destroy()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.THANOS_GLOVE:
			if self.wndThanosGlove:
				self.wndThanosGlove.Destroy()

		if app.ENABLE_AURA_SYSTEM:
			if self.wndAura:
				self.wndAura.Destroy()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.Destroy()
			if self.wndBuffNPCCreateWindow:
				self.wndBuffNPCCreateWindow.Destroy()

		if app.ENABLE_OFFLINESHOP_SYSTEM:
			if self.dlgOfflineShop:
				self.dlgOfflineShop.Hide()
				self.dlgOfflineShop.Destroy()
				del self.dlgOfflineShop

			if self.dlgOfflineShopPanel:
				self.dlgOfflineShopPanel.Hide()
				self.dlgOfflineShopPanel.Destroy()
				del self.dlgOfflineShopPanel

			if self.offlineShopBuilder:
				self.offlineShopBuilder.Hide()
				self.offlineShopBuilder.Destroy()
				del self.offlineShopBuilder
			
			if self.dlgShopMessage:
				self.dlgShopMessage.Hide()
				self.dlgShopMessage.Destroy()
				self.dlgShopMessage=None
		
		if app.ENABLE_SHOP_SEARCH_SYSTEM:
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Hide()
				self.wndPrivateShopSearch.Destroy()
				del self.wndPrivateShopSearch
				self.wndPrivateShopSearch=0


		if app.ENABLE_DROP_ITEM_WORLDARD:
			if self.wndDropItem:
				self.wndDropItem.Close()
				self.wndDropItem.Destroy()

		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			if self.wndCubeRenewal:
				self.wndCubeRenewal.Close()
				self.wndCubeRenewal.Destroy()

		if self.wndBattlePass:
			self.wndBattlePass.Close()
			self.wndBattlePass.Destroy()


		if self.wndBattlePassButton:
			self.wndBattlePassButton.Hide()
			self.wndBattlePassButton.Destroy()
			#self.wndBattlePassButton.Close()

		if self.wndTableBonus:
			self.wndTableBonus.Close()
			self.wndTableBonus.Destroy()

		if app.ELEMENT_SPELL_WORLDARD:
			if self.dlgElementSpell:
				self.dlgElementSpell.Hide()
				self.dlgElementSpell.Destroy()

			if self.dlgElementSpellChange:
				self.dlgElementSpellChange.Hide()
				self.dlgElementSpellChange.Destroy()

			del self.dlgElementSpell
			del self.dlgElementSpellChange

		if app.ENABLE_BIYOLOG:
			if self.wndBio:
				self.wndBio.Hide()
				self.wndBio.Destroy()
				del self.wndBio

		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			if self.wndAutoWindow:
				del self.wndAutoWindow

		if app.ENABLE_PVP_TOURNAMENT:
			if self.wndPvPDuel:
				self.wndPvPDuel.Hide()
				self.wndPvPDuel.Destroy()
				self.wndPvPDuel=None
			if self.wndPvPDuelPanel:
				self.wndPvPDuelPanel.Hide()
				self.wndPvPDuelPanel.Destroy()
				self.wndPvPDuelPanel=None

		if app.__ENABLE_ADVANCE_SKILL_SELECT__:
			if self.wndSkillSelect:
				self.wndSkillSelect.Destroy()

		self.wndChatLog.Destroy()
		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Hide()
				self.wndExpandedMoneyTaskBar.Destroy()

		for btn in self.questButtonList:
			btn.SetEvent(0)
			btn.Hide()
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Hide()
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Hide()
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Hide()
			dlg.Destroy()


		del self.wndczestadisticas

		del self.wndSwitchbotManual

		del self.wndSwitchbotMenu

		del self.wndAlmacenMenu

		# ITEM_MALL
		del self.mallPageDlg
		# END_OF_ITEM_MALL
		
		if app.ENABLE_DROP_ITEM_WORLDARD:
			del self.wndDropItem

		del self.Itemshop_v2
		if app.ENABLE_MANAGER_BANK_SYSTEM:
			del self.managerAccountBank
		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat

		del self.wndBattlePass
		del self.wndBattlePassButton

		if app.ENABLE_CUBE_RENEWAL_WORLDARD:
			del self.wndCubeRenewal

		del self.wndTableBonus
		del self.wndTaskBar
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar
		del self.wndEnergyBar
		del self.wndCharacter
		del self.wndInventory
		del self.wndInventoryNew
		del self.wndInventoryGold
		if self.wndDragonSoul:
			del self.wndDragonSoul
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine
		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndSpecialStorage:
				del self.wndSpecialStorage
		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		del self.wndHelp
		del self.wndCardsInfo
		del self.wndCards
		del self.wndCardsIcon
		del self.wndCube
		del self.wndCubeResult
		del self.inputDialog
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		del self.wndGameButton

		if app.ENABLE_MAINTENANCE_SYSTEM:
			del self.wndMaintenance

		del self.tipBoard
		del self.bigBoard

		if app.dracaryS_DUNGEON_LIB:
			del self.missionBoard
			if self.wndDungeonTimer:
				self.wndDungeonTimer.Hide()
				self.wndDungeonTimer=0

		del self.wndItemSelect
		del self.wndTicket

		if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
			if self.wndSetCustomAttribute:
				self.wndSetCustomAttribute.Destroy()
				del self.wndSetCustomAttribute

		if app.THANOS_GLOVE:
			del self.wndThanosGlove

		if app.ENABLE_AURA_SYSTEM:
			del self.wndAura

		if app.ENABLE_DUNGEON_INFO:
			del self.wndTableDungeonInfo

		if app.ENABLE_RARITY_REFINE:
			del self.dlgRefineRarity

		del self.rendertooltip
		
		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar = None

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			del self.wndBuffNPCWindow
			del self.wndBuffNPCCreateWindow

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			del self.wndWarpWindow

		if app.__ENABLE_ADVANCE_SKILL_SELECT__:
			del self.wndSkillSelect

		# del self.wndItemShop
		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}

		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		if app.ENABLE_KINGDOMS_WAR:
			if self.wndKingdomsWar:
				self.wndKingdomsWar.Hide()
				self.wndKingdomsWar.Destroy()
			
			del self.wndKingdomsWar

		event.SetInterfaceWindow(None)
		uiChat.DestroyChatInputSetWindow()

	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)
		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			self.wndAutoWindow.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)
		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			self.wndAutoWindow.OnActivateSkill()

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)
		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			self.wndAutoWindow.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	if app.BL_67_ATTR:
		def OpenAttr67AddDlg(self):
			if self.wndAttr67Add:
				self.wndAttr67Add.Show()

		if app.WJ_ENABLE_TRADABLE_ICON:
			def IsAttr67RegistItem(self):
				return self.wndAttr67Add and self.wndAttr67Add.RegistSlotIndex != -1

			def IsAttr67SupportItem(self):
				return self.wndAttr67Add and self.wndAttr67Add.SupportSlotIndex != -1

	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndInventory.RefreshStatus()
		self.wndInventoryNew.RefreshStatus()
		self.wndInventoryGold.RefreshStatus()
		if self.wndEnergyBar:
			self.wndEnergyBar.RefreshStatus()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshStatus()

		if self.wndTableBonus:
			self.wndTableBonus.RefreshBonus()

		#if self.wndczestadisticas:
		#	self.wndczestadisticas.RefreshStatus()

	if app.ENABLE_HIDE_COSTUME_SYSTEM:
		def costume_hide_clear(self):
			self.wndInventory.costume_hide_clear()
		def costume_hide_list(self,slot,index):
			self.wndInventory.costume_hide_list(slot,index)
		def costume_hide_load(self):
			self.wndInventory.costume_hide_load()
			
	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()
		self.wndInventoryNew.RefreshItemSlot()
		self.wndInventoryGold.RefreshStatus()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshItemSlot()

		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage.RefreshItemSlot()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow.RefreshEquipSlotWindow()

		if app.ENABLE_AURA_SYSTEM:
			if player.IsAuraRefineWindowOpen():
				if self.wndAura and self.wndAura.IsShow():
					self.wndAura.RefreshAuraWindow()

	def RefreshCharacter(self): ## Character ÆäÀÌÝöÀÇ ¾ó±¼, Inventory ÆäÀÌÝöÀÇ Àü½Å ±×¸² µîÀÇ Refresh
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		#self.wndSafebox.RefreshSafebox()
		self.wndInventoryNew.RefreshSafebox()

	# ITEM_MALL
	def RefreshMall(self):
		#self.wndSafebox.RefreshMall()
		self.wndInventoryNew.RefreshMall()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def RefreshMobile(self):
		self.dlgSystem.RefreshMobile()

	def OnMobileAuthority(self):
		self.dlgSystem.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	if (app.WJ_COMBAT_ZONE):
		def OpenShopDialog(self, vid, points, curLimit, maxLimit):
			self.wndInventory.Show()
			self.wndInventory.SetTop()
			self.dlgShop.Open(vid, points, curLimit, maxLimit)
			self.dlgShop.SetTop()
	else:
		def OpenShopDialog(self, vid):
			self.wndInventory.Show()
			self.wndInventory.SetTop()
			self.dlgShop.Open(vid)
			self.dlgShop.SetTop()

	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):

		wnds = ()
		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q
		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE

	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItemExchange(self, dstSlotIndex, srcSlotIndex):
			self.dlgExchange.CantTradableItem(dstSlotIndex, srcSlotIndex)

		# -----------------------------------------------------------------------------------------
		# Inventário Especial
		def CantTradableItemExchangeEspecial(self, dstSlotIndex, srcSlotIndex):
			self.dlgExchange.CantTradableItemEspecial(dstSlotIndex, srcSlotIndex)
		# -----------------------------------------------------------------------------------------
		# -----------------------------------------------------------------------------------------

	def BINARY_CALENDAR_OPEN_ADM(self):
		return
		#self.wndCalendarADM.Show()

	def BINARY_CALENDAR_LOAD_EVENTS_ADM(self,index_event,name_event,descrip_event):
		return
		#self.wndCalendarADM.RegistroEventos(index_event,name_event)

	def BINARY_CALENDAR_CLEAR_EVENTS_ADM(self):
		return
		#self.wndCalendarADM.ClearRegistro()

	def BINARY_CALENDAR_LOADING_EVENTS_ADM(self):
		return
		#self.wndCalendarADM.LoadEvents()


	def BINARY_CALENDAR_OPEN(self, currentTimeStamp):
		pass
		#self.wndCalendar.Open(currentTimeStamp)

	def BINARY_CALENDAR_LOAD_EVENTS(self,day,name,image,startAt, endAt,duration):
		pass
		#wndEventCalendar.AppendEvent(1, "Evento Caja Luz de Luna 1", "alquimia.tga", 1633654036, 7200)
		#self.wndCalendar.AppendEvent(day,name,image,startAt, endAt,duration)

	def BINARY_CALENDAR_CLEAR_EVENTS(self):
		pass
		#self.wndCalendar.ClearEvents()

	def BINARY_CALENDAR_LOADING_EVENTS(self):
		pass
		#self.wndCalendar.LoadingEventos()

	## Party
	def AddPartyMember(self, pid, name):
		self.wndParty.AddPartyMember(pid, name)

		self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)

		##!! 20061026.levites.Äù½ºÆ®_À§Ä¡_º¸Ý¤
		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()

		##!! 20061026.levites.Äù½ºÆ®_À§Ä¡_º¸Ý¤
		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	## Safebox
	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		# SAFEBOX_PASSWORD
		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")
		# END_OF_SAFEBOX_PASSWORD

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		self.dlgPassword.CloseDialog()
		#self.wndSafebox.ShowWindow(size)
		self.wndInventoryNew.ShowWindow(size)

	def RefreshSafeboxMoney(self):
		return
		self.wndSafebox.RefreshSafeboxMoney()

	def CommandCloseSafebox(self):
		self.wndInventoryNew.CommandCloseSafebox()
		#self.wndSafebox.CommandCloseSafebox()

	if app.ELEMENT_SPELL_WORLDARD:
		def ElementsSpellOpen(self,itemPos, func, cost, grade_add):
			self.dlgElementSpell.Open(itemPos, func, cost, grade_add)

		def ElementsSpellChangeOpen(self, itemPos, cost):
			self.dlgElementSpellChange.Open(itemPos, cost)
			
	# ITEM_MALL
	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return
		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		self.dlgPassword.CloseDialog()
		#self.wndMall.ShowWindow(size)
		self.wndInventoryNew.ShowWindow(size)

	def CommandCloseMall(self):
		#self.wndMall.CommandCloseMall()
		self.wndInventoryNew.CommandCloseMall()
	# END_OF_ITEM_MALL

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Hide()
		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
		key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
		if not self.guildScoreBoardDict.has_key(key):
			return

		guildBoard = self.guildScoreBoardDict[key]
		guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	if app.ENABLE_AUTOMATIC_PICK_UP_SYSTEM:
		def OnChangePickUPMode(self):
			self.dlgSystem.OnChangePickUPMode()

	## Refine
	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type):
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type)

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type, apply_random_list, src_vnum):
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type, apply_random_list, src_vnum)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	if app.ENABLE_MULTI_REFINE_WORLDARD:
		def BINARY_MULTI_REFINE_ADD_INFO(self, index, targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type, applyRandomList):
			self.dlgRefineNew.func_set_info(index, targetItemPos, nextGradeItemVnum, cost, prob, special_storage, type, applyRandomList)

		def BINARY_MULTI_REFINE_ADD_MATERIAL(self,index, vnum, count):
			self.dlgRefineNew.AppendMaterial(index, vnum, count)

		def BINARY_MULTI_REFINE_CLEAR_INFO(self):
			self.dlgRefineNew.func_clear_info()

		def BINARY_MULTI_REFINE_LOAD_INFO(self):
			self.dlgRefineNew.Load()

		def BINARY_MULTI_REFINE_OPEN(self):
			self.dlgRefineNew.Open()

	if app.ENABLE_RARITY_REFINE:
		def OpenRefineRarityDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, prob_extra, special_storage, type):
			self.dlgRefineRarity.Open(targetItemPos, nextGradeItemVnum, cost, prob, prob_extra, special_storage, type)

		def AppendMaterialToRefineRarityDialog(self, vnum, count):
			self.dlgRefineRarity.AppendMaterial(vnum, count)

	## Show & Hide
	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Show()
			self.wndDragonSoulRefine.Show()
		self.wndChat.Show()

		self.wndMiniMap.Show()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()
	
		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()
		
		if app.ENABLE_ZODIAC_MISSION:
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Show()
			if self.wnd12ziReward:
				self.wnd12ziReward.Show()

	def HideAllWindows(self):
		if self.wndTaskBar:
			self.wndTaskBar.Hide()

		if self.wndAlmacenMenu:
			self.wndAlmacenMenu.Hide()

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()
			if self.wndSwitchbotMenu:
				self.wndSwitchbotMenu.Hide()
			if self.wndSwitchbotManual:
				self.wndSwitchbotManual.Hide()

		if self.wndczestadisticas:
			self.wndczestadisticas.Hide()

		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()

		if self.wndCharacter:
			self.wndCharacter.Close()

		if self.wndInventory:
			self.wndInventory.Hide()
		
		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Hide()
			
		if self.wndInventoryGold:
			self.wndInventoryGold.Hide()

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.Hide()
			self.wndDragonSoulRefine.Hide()

		if self.wndChat:
			self.wndChat.Hide()
		
		if app.ENABLE_ZODIAC_MISSION:
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Hide()
			if self.wnd12ziReward:
				self.wnd12ziReward.Hide()

		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			if self.wndAutoWindow:
				self.wndAutoWindow.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()
		
		if app.ENABLE_SHOW_CHEST_DROP:
			if self.wndChestDropInfo:
				self.wndChestDropInfo.Hide()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.Hide()
			if self.wndBuffNPCCreateWindow:
				self.wndBuffNPCCreateWindow.Hide()

		if app.THANOS_GLOVE:
			if self.wndThanosGlove:
				self.wndThanosGlove.Hide()

		if app.ENABLE_AURA_SYSTEM:
			if self.wndAura:
				self.wndAura.Hide()

		if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
			if self.wndSetCustomAttribute:
				self.wndSetCustomAttribute.Hide()

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			if self.wndWarpWindow:
				self.wndWarpWindow.Hide()

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()

	def ToggleChat(self):
		if True == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			# À¥ÆäÀÌÝö°¡ ¿­·ÈÀ»¶§´Â Ã¤ÆÃ ÀÔ·ÂÀÌ ¾ÈµÊ
			if self.wndWeb and self.wndWeb.IsShow():
				pass
			else:
				self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	if app.RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.dlgRestart.OpenDialog(d_time)
			self.dlgRestart.SetTop()
	else:
		def OpenRestartDialog(self):
			self.dlgRestart.OpenDialog()
			self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if False == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if False == player.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					self.wndCharacter.Close()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	def ToggleGoldWindow(self):
		return

		if False == player.IsObserverMode():
			self.wndInventoryGold.Show()

	def ToggleInventoryWindow(self):
		if False == player.IsObserverMode():
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()

	def ToggleInventoryNewWindow(self):
		if False == player.IsObserverMode():
			if False == self.wndInventoryNew.IsShow():
				self.wndInventoryNew.Show()
				self.wndInventoryNew.SetTop()
			else:
				self.wndInventoryNew.OverOutItem()
				self.wndInventoryNew.Close()

	def ToggleExpandedButton(self):
		if False == player.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()
	
	if app.ENABLE_EXPANDED_MONEY_TASKBAR:
		def ToggleExpandedMoneyButton(self):
			if False == self.wndExpandedMoneyTaskBar.IsShow():
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()
			else:
				self.wndExpandedMoneyTaskBar.Close()

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def BuffNPC_OpenCreateWindow(self):
			if self.wndBuffNPCWindow:
				if False == self.wndBuffNPCCreateWindow.IsShow():
					self.wndBuffNPCCreateWindow.Show()
					self.wndBuffNPCCreateWindow.SetTop()

		def BuffNPCOpenWindow(self):
			if self.wndBuffNPCWindow:
				if False == self.wndBuffNPCWindow.IsShow():
					self.wndBuffNPCWindow.Show()
					self.wndBuffNPCWindow.SetTop()
				else:
					self.wndBuffNPCWindow.Close()

		def BuffNPC_Summon(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSummon()
				self.wndBuffNPCWindow.Show()
				self.wndBuffNPCWindow.SetTop()

		def BuffNPC_Unsummon(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetUnsummon()

		def BuffNPC_Clear(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetClear()
				
		def BuffNPC_SetBasicInfo(self, name, sex, intvalue):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetBasicInfo(name, sex, intvalue)

		def BuffNPC_SetEXPInfo(self, level, cur_exp, exp):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetEXPInfo(level, cur_exp, exp)
				
		def BuffNPC_SetSkillInfo(self, skill1, skill2, skill3, skill4, skill5, skill6, skillpoints):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSkillInfo(skill1, skill2, skill3, skill4, skill5, skill6, skillpoints)

		def BuffNPC_SkillUseStatus(self, slot0, slot1, slot2, slot3, slot4, slot5):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSkillUseStatus(slot0, slot1, slot2, slot3, slot4, slot5)
				
		def BuffNPC_SetSkillCooltime(self, slot, timevalue):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSkillCooltime(slot, timevalue)

		def BuffNPC_CreatePopup(self, type, value0, value1):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.CreatePopup(type, value0, value1)

	# ¿ëÈ¥¼®
	def DragonSoulActivate(self, deck):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	def DragonSoulDeactivate(self):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.DeactivateDragonSoul()

	def Highligt_Item(self, inven_type, inven_pos):
		if player.DRAGON_SOUL_INVENTORY == inven_type:
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				self.wndDragonSoul.HighlightSlot(inven_pos)
		elif player.SLOT_TYPE_INVENTORY == inven_type:
			self.wndInventory.HighlightSlot(inven_pos)
		else:
			self.wndInventoryNew.HighlightSlot(inven_type, inven_pos)

	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = True
		self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, uiScriptLocale.TASKBAR_DRAGON_SOUL)

	def ToggleDragonSoulWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					if self.DRAGON_SOUL_IS_QUALIFIED:
						self.wndDragonSoul.Show()
					else:
						try:
							self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
							self.wndPopupDialog.Open()
						except:
							self.wndPopupDialog = uiCommon.PopupDialog()
							self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
							self.wndPopupDialog.Open()
				else:
					self.wndDragonSoul.Close()

	def ToggleDragonSoulWindowWithNoInfo(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					if self.DRAGON_SOUL_IS_QUALIFIED:
						self.wndDragonSoul.Show()
				else:
					self.wndDragonSoul.Close()
	if app.ENABLE_SPECIAL_STORAGE:
		def ToggleSpecialStorageWindow(self):
			return
			if False == player.IsObserverMode():
				if False == self.wndSpecialStorage.IsShow():
					self.wndSpecialStorage.Show()
				else:
					self.wndSpecialStorage.Close()
	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)

	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)

	def OpenDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Show()
					if None != self.wndDragonSoul:
						if False == self.wndDragonSoul.IsShow():
							self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Close()

	if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
		def ToggleAutoWindow(self):
			if False == player.IsObserverMode():
				if not self.wndAutoWindow.IsShow():
					self.wndAutoWindow.Show()
				else:
					self.wndAutoWindow.Close()

		def SetAutoCooltime(self, slotindex, cooltime):
			self.wndAutoWindow.SetAutoCooltime(slotindex, cooltime)

		def SetCloseGame(self):
			self.wndAutoWindow.SetCloseGame()

		def GetAutoStartonoff(self):
			return self.wndAutoWindow.GetAutoStartonoff()

		def RefreshAutoSkillSlot(self):
			if self.wndAutoWindow:
				self.wndAutoWindow.RefreshAutoSkillSlot()

		def RefreshAutoPositionSlot(self):
			if self.wndAutoWindow:
				self.wndAutoWindow.RefreshAutoPositionSlot()

		def AutoOff(self):
			if self.wndAutoWindow:
				self.wndAutoWindow.AutoOnOff(0, self.wndAutoWindow.AUTO_ONOFF_START, 1, True)
				self.wndAutoWindow.Refresh()

			# if self.wndExpandedTaskBar:
				# self.wndExpandedTaskBar.EnableAutoButton(False)

		def AutoOn(self):
			if self.wndAutoWindow:
				# self.wndAutoWindow.AutoOnOff(0, self.wndAutoWindow.AUTO_ONOFF_START, 1, True)
				self.wndAutoWindow.Refresh()

			# if self.wndExpandedTaskBar:
				# self.wndExpandedTaskBar.EnableAutoButton(True)

	def ToggleGuildWindow(self):
		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()


	def ToggleAlmacenMenu(self):
		if self.wndAlmacenMenu:
			self.wndAlmacenMenu.Open()


	def OpenCZEstadisticas(self):
		if self.wndczestadisticas:
			self.wndczestadisticas.Show()

	def SetBonusCombatZone(self,arg,type=0,value=0):
		if self.wndczestadisticas:
			self.wndczestadisticas.SetBonus(arg,type,value)

	def SetTimeCombatZone(self,time):
		if self.wndczestadisticas:
			self.wndczestadisticas.SetTime(time)

	def CloseCZEstadisticas(self):
		if self.wndczestadisticas:
			self.wndczestadisticas.Hide()

	if app.ENABLE_SWITCHBOT:
		def ToggleSwitchBotMenu(self):
			if self.wndSwitchbotMenu:
				self.wndSwitchbotMenu.Open()


		def ToggleSwitchBotManual(self):
			if self.wndSwitchbotManual:
				self.wndSwitchbotManual.Show()

		def GetPosChangeItemManual(self):
			if self.wndSwitchbotManual:
				return self.wndSwitchbotManual.GetPosItemChange()

		def ToggleSwitchbotWindow(self):
			if self.wndSwitchbot.IsShow():
				self.wndSwitchbot.Close()
			else:
				self.wndSwitchbot.Open()
				
		def RefreshSwitchbotWindow(self):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotItem(slot)
			
	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	def __OnClickHelpButton(self):
		player.SetPlayTime(1)
		self.CheckGameButton()
		self.OpenHelpWindow()

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()

	def OpenHelpWindow(self):
		self.wndUICurtain.Show()
		self.wndHelp.Open()

	def CloseHelpWindow(self):
		self.wndUICurtain.Hide()
		self.wndHelp.Close()

	def OpenWebWindow(self, url):
		self.wndWeb.Open(url)

		# À¥ÆäÀÌÝö¸¦ ¿­¸é Ã¤ÆÃÀ» ´Ý´Â´Ù
		self.wndChat.CloseChat()

	if app.ENABLE_DUNGEON_INFO:
		def DUNGEON_INFO_CHECK_SHOW(self):
			if self.wndTableDungeonInfo:
				if self.wndTableDungeonInfo.IsShow():
					self.wndTableDungeonInfo.Close()
				else:
					import dungeon_info
					dungeon_info.Open()
		def BINARY_TABLE_DUNGEON_INFO_OPEN(self):
			if self.wndTableDungeonInfo:
				self.wndTableDungeonInfo.LoadDateInfo()
				self.wndTableDungeonInfo.Show()

		def BINARY_TABLE_DUNGEON_RANKING_LOAD(self):
			if self.wndTableDungeonInfo:
				self.wndTableDungeonInfo.LoadRanking()

		def BINARY_TABLE_DUNGEON_MISION_LOAD(self):
			if self.wndTableDungeonInfo:
				self.wndTableDungeonInfo.LoadMision()
	
	def CloseRenderTooltip(self):
		self.rendertooltip.CloseRenderTooltip()

	def ShowRenderTooltip(self):
		self.rendertooltip.ShowRenderTooltip()

	def RenderClearDates(self):
		self.rendertooltip.RenderClearDates()

	def SetRenderDates(self, vnum, type, value3 = None):
		self.rendertooltip.SetRenderDates(vnum, type, value3)

	def SetRenderWeapon(self, itemVnum):
		self.rendertooltip.SetRenderWeapon(itemVnum)

	def SetRenderArmor(self, itemVnum):
		self.rendertooltip.SetRenderArmor(itemVnum)

	def SetRenderAcce(self,itemVnum):
		self.rendertooltip.SetRenderAcce(itemVnum)

	def SetRenderHair(self,itemVnum,value3):
		self.rendertooltip.SetRenderHair(itemVnum,value3)

	def SetRenderArmor(self,itemVnum):
		self.rendertooltip.SetRenderArmor(itemVnum)

	def IsRenderTooltip(self):
		if self.rendertooltip.IsRenderTooltip():
			return True
		return False

	# show GIFT
	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	if app.ENABLE_DROP_ITEM_WORLDARD:
		def BINARY_DROP_ITEM_OPEN(self):
			self.wndDropItem.Show()
	
	if app.ENABLE_CUBE_RENEWAL_WORLDARD:
		def BINARY_CUBE_RENEWAL_OPEN(self):
			self.wndCubeRenewal.Show()
	
	def BINARY_BATTLEPASS_OPEN(self):
		self.wndBattlePass.Show()

	def OpenTableBonus(self):
		if self.wndTableBonus:
			if self.wndTableBonus.IsShow():
				self.wndTableBonus.Hide()
			else:
				self.wndTableBonus.Show()

	def CloseWbWindow(self):
		self.wndWeb.Close()
	def OpenCardsInfoWindow(self):
		self.wndCardsInfo.Open()
		
	def OpenCardsWindow(self, safemode):
		self.wndCards.Open(safemode)
		
	def UpdateCardsInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points):
		self.wndCards.UpdateCardsInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, hand_4, hand_4_v, hand_5, hand_5_v, cards_left, points)
		
	def UpdateCardsFieldInfo(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.wndCards.UpdateCardsFieldInfo(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def CardsPutReward(self, hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points):
		self.wndCards.CardsPutReward(hand_1, hand_1_v, hand_2, hand_2_v, hand_3, hand_3_v, points)
		
	def CardsShowIcon(self):
		self.wndCardsIcon.Show()
	if app.ENABLE_SASH_SYSTEM:
		def ActSash(self, iAct, bWindow):
			if iAct == 1:
				if bWindow == True:
					if not self.wndSashCombine.IsOpened():
						self.wndSashCombine.Open()
					
					if not self.wndInventory.IsShow():
						self.wndInventory.Show()
				else:
					if not self.wndSashAbsorption.IsOpened():
						self.wndSashAbsorption.Open()
					
					if not self.wndInventory.IsShow():
						self.wndInventory.Show()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 2:
				if bWindow == True:
					if self.wndSashCombine.IsOpened():
						self.wndSashCombine.Close()
				else:
					if self.wndSashAbsorption.IsOpened():
						self.wndSashAbsorption.Close()
				
				self.wndInventory.RefreshBagSlotWindow()
			elif iAct == 3 or iAct == 4:
				if bWindow == True:
					if self.wndSashCombine.IsOpened():
						self.wndSashCombine.Refresh(iAct)
				else:
					if self.wndSashAbsorption.IsOpened():
						self.wndSashAbsorption.Refresh(iAct)
				
				self.wndInventory.RefreshBagSlotWindow()

	if app.__ENABLE_ADVANCE_SKILL_SELECT__:
		def OpenSkillSelectWindow(self, job):
			self.wndSkillSelect.Open(job)

	def OpenCubeWindow(self):
		self.wndCube.Open()

		if False == self.wndInventory.IsShow():
			self.wndInventory.Show()

	def UpdateCubeInfo(self, gold, itemVnum, count):
		self.wndCube.UpdateInfo(gold, itemVnum, count)

	def CloseCubeWindow(self):
		self.wndCube.Close()

	def FailedCubeWork(self):
		self.wndCube.Refresh()

	def SucceedCubeWork(self, itemVnum, count):
		self.wndCube.Clear()

		print "Å¥ºê Ý¦ÀÛ ¼º°ø! [%d:%d]" % (itemVnum, count)

		if 0: # °á°ú ¸Þ½ÃÝö Ãâ·ÂÀº »ý·« ÇÑ´Ù
			self.wndCubeResult.SetPosition(*self.wndCube.GetGlobalPosition())
			self.wndCubeResult.SetCubeResultItem(itemVnum, count)
			self.wndCubeResult.Open()
			self.wndCubeResult.SetTop()

	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndInventoryGold,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.wndEnergyBar:
			hideWindows += self.wndEnergyBar,
		
		if app.ENABLE_ZODIAC_MISSION:
			if self.wnd12ziTimer:
				hideWindows += self.wnd12ziTimer,
			if self.wnd12ziReward:
				hideWindows += self.wnd12ziReward,

		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			hideWindows += self.wndDragonSoul,\
						self.wndDragonSoulRefine,

		if app.ENABLE_SWITCHBOT and self.wndSwitchbot:
			hideWindows += self.wndSwitchbot,

		if self.wndSwitchbotManual:
			hideWindows += self.wndSwitchbotManual,
		
		if app.ENABLE_EXPANDED_MONEY_TASKBAR:
			if self.wndExpandedMoneyTaskBar:
				hideWindows += self.wndExpandedMoneyTaskBar,

		if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
			if self.wndAutoWindow:
				hideWindows += self.wndAutoWindow,

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				hideWindows += self.wndBuffNPCWindow,
			if self.wndBuffNPCCreateWindow:
				hideWindows += self.wndBuffNPCCreateWindow,

		if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
			if self.wndSetCustomAttribute:
				hideWindows += self.wndSetCustomAttribute,

		if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
			if self.wndWarpWindow:
				hideWindows += self.wndWarpWindow,

		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)
		import sys

		if self.wndSwitchbotMenu.IsShowNew():
			self.wndSwitchbotMenu.Open()

		if self.wndAlmacenMenu.IsShowNew():
			self.wndAlmacenMenu.Open()

		self.wndInventoryGold.CloseWithoutWindow()
		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return hideWindows

	def __ShowWindows(self, wnds):
		# opened = False
		# if constInfo.NewGoldWindow == 0:
			# opened = True
			
		import sys
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		# if opened:
			# self.wndInventoryGold.Close()

		self.ShowAllWhisperButton()
		# if constInfo.NewGoldWindow == 1:
			# self.wndInventoryGold.Open()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	def BINARY_SetObserverMode(self, flag):
		self.wndGameButton.SetObserverMode(flag)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE


	#####################################################################################
	### Equipment ###

	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	#####################################################################################

	#####################################################################################
	### Quest ###
	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		# QUEST_LETTER_IMAGE
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
		# END_OF_QUEST_LETTER_IMAGE

	def BINARY_RecvQuest(self, index, name, iconType, iconName):

		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		# QUEST_LETTER_IMAGE
		##!! 20061026.levites.Äù½ºÆ®_ÀÌ¹ÌÝö_±³Ã¼
		import item
		if "item"==iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName=item.GetIconImageFileName()
		else:
			buttonImageFileName=iconName

		if iconName and (iconType not in ("item", "file")): # type "ex" implied
			btn.SetUpVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName.replace("open", "close")))
			btn.SetOverVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
			btn.SetDownVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
		else:
			if localeInfo.IsEUROPE():
				btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
				btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
				btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			else:
				btn.SetUpVisual(buttonImageFileName)
				btn.SetOverVisual(buttonImageFileName)
				btn.SetDownVisual(buttonImageFileName)
				btn.Flash()
		# END_OF_QUEST_LETTER_IMAGE

		if localeInfo.IsARABIC():
			btn.SetToolTipText(name, 0, 35)
			btn.ToolTipText.SetHorizontalAlignCenter()
		else:
			btn.SetToolTipText(name, -20, 35)
			btn.ToolTipText.SetHorizontalAlignLeft()

		listOfTypes = iconType.split(",")
		if "blink" in listOfTypes:
			btn.Flash()

		listOfColors = {
			"golden":	0xFFffa200,
			"green":	0xFF00e600,
			"blue":		0xFF0099ff,
			"purple":	0xFFcc33ff,

			"fucsia":	0xFFcc0099,
			"aqua":		0xFF00ffff,
		}
		for k,v in listOfColors.iteritems():
			if k in listOfTypes:
				btn.ToolTipText.SetPackedFontColor(v)

		btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
		btn.Show()

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

	def __ArrangeQuestButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		##!! 20061026.levites.Äù½ºÆ®_À§Ä¡_º¸Ý¤
		if self.wndParty:
			xPos = 100 + 30 if self.wndParty.IsShow() else 20
		else:
			xPos = 20

		if localeInfo.IsARABIC():
			xPos = xPos + 15

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:

			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1
			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				btn.Show()

	def __StartQuest(self, btn):
		event.QuestButtonClick(btn.index)
		self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		btn.Hide()
		btn.Destroy()
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		if app.ENABLE_KINGDOMS_WAR:
			if self.wndKingdomsWar.IsShow():
				return
		
		for btn in self.questButtonList:
			btn.Show()
	#####################################################################################

	#####################################################################################
	### Whisper ###

	def __InitWhisper(self):
		chat.InitWhisper(self)

	## Ã¤ÆÃÃ¢ÀÇ "¸Þ½ÃÝö º¸³»±â"¸¦ ´­·¶À»¶§ ÀÌ¸§ ¾ø´Â ´ëÈ­Ã¢À» ¿©´Â ÇÔ¼ö
	## ÀÌ¸§ÀÌ ¾ø±â ¶§¹®¿¡ ±âÝ¸ÀÇ WhisperDialogDict ¿Ý º°µµ·Î °ü¸®µÈ´Ù.
	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	## ÀÌ¸§ ¾ø´Â ´ëÈ­Ã¢¿¡¼­ ÀÌ¸§À» °áÝ¤ÇßÀ»¶§ WhisperDialogDict¿¡ Ã¢À» ³Ö¾îÝÖ´Â ÇÔ¼ö
	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def RegisterTemporaryWhisperDialog(self, name):
			if not self.dlgWhisperWithoutTarget:
				return

			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

			elif self.whisperDialogDict.has_key(name.lower()):
				oldDialog = self.whisperDialogDict[name.lower()]
				oldDialog.Hide()
				oldDialog.Destroy()
				del self.whisperDialogDict[name.lower()]

			self.whisperDialogDict[name.lower()] = self.dlgWhisperWithoutTarget
			self.dlgWhisperWithoutTarget.OpenWithTarget(name)
			self.dlgWhisperWithoutTarget = None
			self.__CheckGameMaster(name)
	else:
		def RegisterTemporaryWhisperDialog(self, name):
			if not self.dlgWhisperWithoutTarget:
				return

			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

			elif self.whisperDialogDict.has_key(name):
				oldDialog = self.whisperDialogDict[name]
				oldDialog.Hide()
				oldDialog.Destroy()
				del self.whisperDialogDict[name]

			self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
			self.dlgWhisperWithoutTarget.OpenWithTarget(name)
			self.dlgWhisperWithoutTarget = None
			self.__CheckGameMaster(name)

	## Ä³¸¯ÅÝ ¸Þ´ºÀÇ 1:1 ´ëÈ­ ÇÝ±â¸¦ ´­·¶À»¶§ ÀÌ¸§À» °¡Ýö°í ¹Ù·Î Ã¢À» ¿©´Â ÇÔ¼ö
	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def OpenWhisperDialog(self, name, language = 0, empire = 0):
			if not self.whisperDialogDict.has_key(name.lower()):
				dlg = self.__MakeWhisperDialog(name)
				dlg.OpenWithTarget(name)
				language = int(language)
				empire = int(empire)
				if language != 0 and empire != 0:
					dlg.SetFlag(language, empire)
				dlg.chatLine.SetFocus()
				dlg.Show()

				self.__CheckGameMaster(name)
				btn = self.__FindWhisperButton(name)
				if 0 != btn:
					dlg.SetFlag(btn.languageID, btn.empireID)
					self.__DestroyWhisperButton(btn)
	else:
		def OpenWhisperDialog(self, name):
				if not self.whisperDialogDict.has_key(name):
					dlg = self.__MakeWhisperDialog(name)
					dlg.OpenWithTarget(name)
					dlg.chatLine.SetFocus()
					dlg.Show()

					self.__CheckGameMaster(name)
					btn = self.__FindWhisperButton(name)
					if 0 != btn:
						self.__DestroyWhisperButton(btn)

	## ´Ù¸¥ Ä³¸¯ÅÝ·ÎºÎÅÝ ¸Þ¼¼Ýö¸¦ ¹Þ¾ÒÀ»¶§ ÀÝ´Ü ¹öÆ°¸¸ ¶ç¿ö µÎ´Â ÇÔ¼ö
	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def RecvWhisper(self, name, language = 0, empire = 0):
			if not self.whisperDialogDict.has_key(name.lower()):
				btn = self.__FindWhisperButton(name)

				if 0 == btn:
					btn = self.__MakeWhisperButton(name, int(language), int(empire))
					btn.Flash()
					# if app.ENABLE_WHISPER_FLASHING:
						# app.FlashApplication()
					chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))
				else:
					language = int(language)
					empire = int(empire)
					if language != 0 and empire != 0:
						btn.languageID = language
						btn.empireID = empire
					btn.Flash()
					# if app.ENABLE_WHISPER_FLASHING:
						# app.FlashApplication()
			elif self.IsGameMasterName(name.lower()):
				dlg = self.whisperDialogDict[name.lower()]
				dlg.SetGameMasterLook()

				if language != "" and empire != "":
					dlg.SetFlag(language, empire)
	else:
		def RecvWhisper(self, name):
			if not self.whisperDialogDict.has_key(name):
				btn = self.__FindWhisperButton(name)
				if 0 == btn:
					btn = self.__MakeWhisperButton(name)
					btn.Flash()
					# if app.ENABLE_WHISPER_FLASHING:
						# app.FlashApplication()
					chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))
				else:
					btn.Flash()
					# if app.ENABLE_WHISPER_FLASHING:
						# app.FlashApplication()
			elif self.IsGameMasterName(name):
				dlg = self.whisperDialogDict[name]
				dlg.SetGameMasterLook()

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def SetInterfaceFlag(self, name, language, empire):
			if self.whisperDialogDict.has_key(name.lower()):
				self.whisperDialogDict[name.lower()].SetFlag(language, empire)
			else:
				btn = self.__FindWhisperButton(name)
				if btn != 0:
					btn.languageID = language
					btn.empireID = empire

	## ¹öÆ°À» ´­·¶À»¶§ Ã¢À» ¿©´Â ÇÔ¼ö
	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def ShowWhisperDialog(self, btn):
			try:
				self.__MakeWhisperDialog(btn.name)
				dlgWhisper = self.whisperDialogDict[btn.name.lower()]
				dlgWhisper.OpenWithTarget(btn.name)
				if btn.languageID != 0 and btn.empireID != 0:
					dlgWhisper.SetFlag(btn.languageID, btn.empireID)
				dlgWhisper.Show()
				self.__CheckGameMaster(btn.name)
			except:
				import dbg
				dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")
			self.__DestroyWhisperButton(btn)
	else:
		def ShowWhisperDialog(self, btn):
			try:
				self.__MakeWhisperDialog(btn.name)
				dlgWhisper = self.whisperDialogDict[btn.name]
				dlgWhisper.OpenWithTarget(btn.name)
				dlgWhisper.Show()
				self.__CheckGameMaster(btn.name)
			except:
				import dbg
				dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")
			self.__DestroyWhisperButton(btn)

		## ¹öÆ° ÃÊ±âÈ­
		#self.__DestroyWhisperButton(btn)

	## WhisperDialog Ã¢¿¡¼­ ÃÖ¼ÒÈ­ ¸í·ÉÀ» ¼öÇàÇßÀ»¶§ È£ÃâµÇ´Â ÇÔ¼ö
	## Ã¢À» ÃÖ¼ÒÈ­ ÇÕ´Ý´Ù.
	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def MinimizeWhisperDialog(self, name, languageID, empireID):
			if 0 != name:
				self.__MakeWhisperButton(name, languageID, empireID)
			self.CloseWhisperDialog(name)
	else:
		def MinimizeWhisperDialog(self, name):
			if 0 != name:
				self.__MakeWhisperButton(name)
			self.CloseWhisperDialog(name)

	## WhisperDialog Ã¢¿¡¼­ ´Ý±â ¸í·ÉÀ» ¼öÇàÇßÀ»¶§ È£ÃâµÇ´Â ÇÔ¼ö
	## Ã¢À» Ýö¿ó´Ý´Ù.
	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Hide()
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			if app.ENABLE_MULTILANGUAGE_SYSTEM:
				dlgWhisper = self.whisperDialogDict[name.lower()]
				dlgWhisper.Hide()
				dlgWhisper.Destroy()
				del self.whisperDialogDict[name.lower()]
			else:
				dlgWhisper = self.whisperDialogDict[name]
				dlgWhisper.Hide()
				dlgWhisper.Destroy()
				del self.whisperDialogDict[name]
		except:
			import dbg
			# dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")
			# dbg.TraceError("name: "+str(self.whisperDialogDict[name]))

	## ¹öÆ°ÀÇ °³¼ö°¡ ¹Ù²î¾úÀ»¶§ ¹öÆ°À» ÀçÝ¤·Ä ÇÝ´Â ÇÔ¼ö
	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63
		#yCount = (screenHeight - 285) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	## ÀÌ¸§À¸·Î Whisper ¹öÆ°À» Ã£¾Æ ¸®ÅÝÇØ ÝÖ´Â ÇÔ¼ö
	## ¹öÆ°Àº µñ¼Å³Ê¸®·Î ÇÝÝö ¾Ê´Â °ÝÀº Ý¤·Ä µÇ¾î ¹ö·Ý ¼ø¼­°¡ À¯Ýö µÇÝö ¾ÊÀ¸¸ç
	## ÀÌ·Î ÀÎÇØ ToolTipµéÀÌ ´Ù¸¥ ¹öÆ°µé¿¡ ÀÇÇØ °¡·ÝÝö±â ¶§¹®ÀÌ´Ù.
	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def __FindWhisperButton(self, name):
			for button in self.whisperButtonList:
				if button.name.lower() == name.lower():
					return button
			return 0
	else:
		def __FindWhisperButton(self, name):
			for button in self.whisperButtonList:
				if button.name == name:
					return button
			return 0

	## Ã¢À» ¸¸µì´Ý´Ù.
	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		
		if app.ENABLE_MULTILANGUAGE_SYSTEM:
			self.whisperDialogDict[name.lower()] = dlgWhisper
		else:
			self.whisperDialogDict[name] = dlgWhisper
		self.windowOpenPosition = (self.windowOpenPosition+1) % 5
		return dlgWhisper

	## ¹öÆ°À» ¸¸µì´Ý´Ù.
	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def __MakeWhisperButton(self, name, languageID = 0, empireID = 0):
			whisperButton = uiWhisper.WhisperButton()
			whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			if self.IsGameMasterName(name):
				whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
			else:
				whisperButton.SetToolTipText(name)
			whisperButton.ToolTipText.SetHorizontalAlignCenter()
			whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
			whisperButton.Show()
			whisperButton.name = name
			whisperButton.languageID = int(languageID)
			whisperButton.empireID = int(empireID)
			self.whisperButtonList.insert(0, whisperButton)
			self.__ArrangeWhisperButton()
			return whisperButton
	else:
		def __MakeWhisperButton(self, name):
			whisperButton = uiWhisper.WhisperButton()
			whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
			if self.IsGameMasterName(name):
				whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
			else:
				whisperButton.SetToolTipText(name)
			whisperButton.ToolTipText.SetHorizontalAlignCenter()
			whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
			whisperButton.Show()
			whisperButton.name = name
			self.whisperButtonList.insert(0, whisperButton)
			self.__ArrangeWhisperButton()
			return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	if app.ENABLE_MULTILANGUAGE_SYSTEM:
		def __CheckGameMaster(self, name):
			if not self.listGMName.has_key(name.lower()):
				return
			if self.whisperDialogDict.has_key(name.lower()):
				dlg = self.whisperDialogDict[name.lower()]
				dlg.SetGameMasterLook()
	else:
		def __CheckGameMaster(self, name):
			if not self.listGMName.has_key(name):
				return
			if self.whisperDialogDict.has_key(name):
				dlg = self.whisperDialogDict[name]
				dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return True
		else:
			return False

	#####################################################################################

	#####################################################################################
	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)

	if app.THANOS_GLOVE:
		def ToggleThanosWindow(self):
			self.wndThanosGlove.ToggleWindow()

	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return True
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return True
		# END_OF_GUILD_BUILDING
		return False

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return True

		return False

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != player.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()

	#####################################################################################

	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	def GetInventoryPageIndex(self):
		if self.wndInventory:
			return self.wndInventory.GetInventoryPageIndex()
		else:
			return -1

	def AttachItemFromSafebox(self, slotIndex, item_type, itemIndex):
		if self.wndInventory and self.wndInventory.IsShow():
			self.wndInventory.AttachItemFromSafebox(slotIndex, item_type, itemIndex)
		return True

	def AttachItemSpecialFromSafebox(self, slotIndex, item_type, itemIndex):
		if self.wndSpecialStorage and self.wndSpecialStorage.IsShow():
			self.wndSpecialStorage.AttachItemFromSafebox(slotIndex, item_type, itemIndex)

		return True

	def AttachSpecialToInv(self, slotWindow, slotIndex):
		if self.wndInventory and self.wndInventory.IsShow():
			self.wndInventory.AttachSpecialToInv(slotWindow, slotIndex)
		return True

	def AttachInvenItemToOtherWindowSlot(self, slotWindow, slotIndex):
		if self.wndInventoryNew and self.wndInventoryNew.IsShow():
			if self.wndInventoryNew.categoryPageIndex == 6:
				return self.wndInventoryNew.AttachItemFromInventoryToSafebox(slotWindow, slotIndex)
			elif self.wndInventoryNew.categoryPageIndex <= 5:
				return self.wndInventoryNew.AttachItemFromInventoryToSpecial(slotWindow, slotIndex)
		#if self.wndSafebox and self.wndSafebox.IsShow():
		#	return self.wndSafebox.AttachItemFromInventory(slotWindow, slotIndex)

		return False


	def SafeboxIsShow(self):
		if self.wndBuffNPCWindow:
			return False
		if self.wndInventoryNew and self.wndInventory:
			if self.wndInventoryNew.IsShow() and self.wndInventory.IsShow():
				return True

		if self.wndSafebox and self.wndInventory:
			if self.wndSafebox.IsShow() and self.wndInventory.IsShow():
				return True

		return False

	if app.WJ_ENABLE_TRADABLE_ICON:
		def SetOnTopWindow(self, onTopWnd):
			self.onTopWindow = onTopWnd

		def GetOnTopWindow(self):
			return self.onTopWindow

		def RefreshMarkInventoryBag(self):
			self.wndInventory.RefreshMarkSlots()
			self.wndInventoryNew.RefreshMarkSlots()

	if app.ENABLE_KINGDOMS_WAR:
		def ActKingdomsWar(self, act, score1, score2, score3, limitKills, deads, limiDeads, timeRemained):
			if self.wndKingdomsWar:
				if act == 1:
					self.wndKingdomsWar.ShowWindow(score1, score2, score3, limitKills, deads, limiDeads, timeRemained)
					global IsQBHide
					IsQBHide = 1
					for btn in self.questButtonList:
						btn.Hide()
				elif act == 2:
					self.wndKingdomsWar.RefreshScore(score1, score2, score3, limitKills)
				elif act == 3:
					self.wndKingdomsWar.RefreshDeads(deads, limiDeads)

	def EmptyFunction(self):
		pass

	if app.ENABLE_DSS_ACTIVE_EFFECT_BUTTON:
		def UseDSSButtonEffect(self, enable):
			if self.wndInventory:
				self.wndInventory.UseDSSButtonEffect(enable)

	if app.ENABLE_OFFLINESHOP_SYSTEM:
		def MakeOfflineShopMessage(self):
			if self.dlgShopMessage == None:
				self.dlgShopMessage = ui.MessageWindow()
		def AddOfflineShopMessage(self, itemVnum, itemCount, itemPrice):
			itemVnum, itemCount, itemPrice = (int(itemVnum), int(itemCount), int(itemPrice))
			self.MakeOfflineShopMessage()
			item.SelectItem(itemVnum)
			if itemCount > 1:
				self.dlgShopMessage.AddMessage(localeInfo.OFFLINESHOP_MESSAGE_WITH_COUNT % (itemCount, item.GetItemName(),localeInfo.NumberToMoneyStringNEW(itemPrice)),5)
			else:
				self.dlgShopMessage.AddMessage(localeInfo.OFFLINESHOP_MESSAGE % (item.GetItemName(),localeInfo.NumberToMoneyStringNEW(itemPrice)),5)
		def OpenOfflineShopDialog(self, vid, isOwner):
			self.wndInventory.Show()
			self.wndInventory.SetTop()

			if isOwner:
				self.OpenOfflineShopPanel()
			else:
				if self.dlgOfflineShop==None:
					self.MakeOfflineShop()

				if self.dlgOfflineShop:
					self.dlgOfflineShop.Open(vid)
					self.dlgOfflineShop.SetCenterPosition()
					self.dlgOfflineShop.SetTop()

		def OpenOfflineShopPanel(self):
			if self.dlgOfflineShopPanel==None:
				self.MakeOfflineShopPanel()
			self.dlgOfflineShopPanel.Open()
			self.dlgOfflineShopPanel.SetTop()
			self.dlgOfflineShopPanel.SetCenterPosition()

		#def OpenOfflineShopInputNameDialog(self):
		#	import uiOfflineShop
		#	self.inputDialog = uiOfflineShop.OfflineShopInputDialog()
		#	self.inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenOfflineShopBuilder))
		#	self.inputDialog.SetCancelEvent(ui.__mem_func__(self.CloseOfflineShopInputNameDialog))
		#	self.inputDialog.Open()
		#
		#def CloseOfflineShopInputNameDialog(self):
		#	self.inputDialog.Close()
		#	self.inputDialog = None
		#	return True

		def OpenOfflineShopBuilder(self):
			#if (not self.inputDialog):
			#	return True
			#if (not len(self.inputDialog.GetTitle())):
			#	return True
			#if (self.inputDialog.GetType() < 0 or self.inputDialog.GetType() == 0):
			#	return True
			#self.CloseOfflineShopInputNameDialog()

			if self.offlineShopBuilder==None:
				self.MakeOfflineShopBuilder()
			self.offlineShopBuilder.Open(".....")
			self.offlineShopBuilder.SetTop()

		def DisappearOfflineShop(self, vid):
			uiOfflineShopBuilder.HideADBoardWithKey(vid)

		def AppearOfflineShop(self, vid, text):
			type = 0
			if text[0].isdigit():
				type = int(text[0])
				text = text[1:]
			if uiOfflineShopBuilder.ShowADBoardWithKey(vid) == False:
				board = uiOfflineShopBuilder.OfflineShopAdvertisementBoard(type)
				board.Open(vid, text)
			else:
				uiOfflineShopBuilder.UpdateADText(vid,type,text)

		def MakeOfflineShopBuilder(self):
			self.offlineShopBuilder = uiOfflineShopBuilder.OfflineShopBuilder()
			#self.offlineShopBuilder.SetItemToolTip(self.tooltipItem)

			self.offlineShopBuilder.SetInven(self.wndInventory)
			self.wndInventory.BindWindow(self.offlineShopBuilder)

			self.offlineShopBuilder.SetInvenNew(self.wndInventoryNew)
			self.wndInventoryNew.BindWindow(self.offlineShopBuilder)

			self.offlineShopBuilder.Hide()

		def MakeOfflineShop(self):
			self.dlgOfflineShop = uiOfflineShop.OfflineShopDialog()
			self.dlgOfflineShop.LoadDialog()
			#self.dlgOfflineShop.SetItemToolTip(self.tooltipItem)
			self.dlgOfflineShop.Hide()

		def MakeOfflineShopPanel(self):
			self.dlgOfflineShopPanel = uiOfflineShop.OfflineMyShop()
			self.dlgOfflineShopPanel.LoadWindow()
			#self.dlgOfflineShopPanel.SetItemToolTip(self.tooltipItem)

		def AppendLogOfflineShopPanel(self,name, date, itemvnum, itemcount, price):
			if self.dlgOfflineShopPanel==None:
				self.MakeOfflineShopPanel()
			self.dlgOfflineShopPanel.AppendLog(name, date, itemvnum, itemcount, price)
		
		def AppendLogOfflineShopPanelFirst(self,name, date, itemvnum, itemcount, price):
			if self.dlgOfflineShopPanel==None:
				self.MakeOfflineShopPanel()
			self.dlgOfflineShopPanel.AppendLogFirst(name, date, itemvnum, itemcount, price)

	if app.ENABLE_SHOP_SEARCH_SYSTEM:
		def __MakePrivateShopSearchWindow(self):
			self.wndPrivateShopSearch = uiPrivateShopSearch.PrivateShopSearchDialog()
			self.wndPrivateShopSearch.LoadWindow()
			#self.wndPrivateShopSearch.Hide()
		def OfflineShopBuyed(self, itemID):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.SetItemBuyStatus(int(itemID))
		def OpenPrivateShopSearch(self, type = 0):
			if self.wndPrivateShopSearch == None:
				self.__MakePrivateShopSearchWindow()
				self.wndPrivateShopSearch.Open(type)
				return

			if self.wndPrivateShopSearch.IsShow():
				self.wndPrivateShopSearch.Hide()
			else:
				self.wndPrivateShopSearch.Open(type)
		def RefreshShopSearch(self):
			if self.wndPrivateShopSearch == None:
				self.__MakePrivateShopSearchWindow()
			self.wndPrivateShopSearch.RefreshMe()
			self.wndPrivateShopSearch.RefreshList()

	if app.ENABLE_NEW_PET_SYSTEM:
		def MakeChangeNameWindow(self):
			self.change_window = uiChangeName.NameInputWindow()

		def OpenChangeNameWindow(self, srcitemPos, destitemPos, itemVnum, type = False):
			if self.change_window == None:
				self.MakeChangeNameWindow()
			self.change_window.LoadItemData(srcitemPos,destitemPos, itemVnum, type)
			self.change_window.Show()
			self.change_window.SetTop()
		def MakePetWindow(self):
			self.wndPet = uiPetSystemNew.PetSystemMain()
			self.wndPet.Hide()

		def ClearPetData(self):
			if self.wndPet == None:
				return
			self.wndPet.ClearData()

		def SetPetSlotIndex(self, index):
			if self.wndPet == None:
				self.MakePetWindow()
			self.wndPet.SetSlotIndex(index)

			if self.wndPet.IsShow():
				self.wndPet.Open()

		def PetUpdate(self, index):
			if self.wndPet == None:
				return
			if index == 0:
				self.wndPet.UpdateTime()
			elif index == 1:
				self.wndPet.UpdateLevel()
				self.wndPet.CheckEvolveFlash()
				self.wndPet.CheckFeedWindow()
			elif index == 2:
				self.wndPet.UpdateExp()
			elif index == 3:
				self.wndPet.UpdateAge()
				self.wndPet.CheckEvolveFlash()
				self.wndPet.CheckFeedWindow()
				self.wndPet.UpdateSkill()
			elif index >= 5 and index <= 7:
				self.wndPet.UpdateBonus()
			elif ((index >= 100 and index <= 114) or (index >= 150 and index <= 164)):
				self.wndPet.UpdateSkill()

		def OpenPetWindow(self):
			if self.wndPet == None:
				self.MakePetWindow()
			if self.wndPet.IsShow():
				self.wndPet.Hide()
			else:
				self.wndPet.Open()

	if app.ENABLE_BIYOLOG:
		def MakeBioWindow(self):
			if self.wndBio == None:
				self.wndBio = uiBiyolog.BiologWindow()
				self.wndBio.LoadEmpty()
				return True
			return False
		def OpenBiologWindow(self):
			self.MakeBioWindow()
			if self.wndBio.IsShow():
				self.wndBio.Close()
			else:
				self.wndBio.Open()
		def SetBioData(self, level, count, time):
			self.MakeBioWindow()
			self.wndBio.LoadData(int(level), int(count), int(time))
		def SetBioStone(self, level):
			self.MakeBioWindow()
			self.wndBio.LoadStone(int(level))
		def SetBioGift(self, level):
			self.MakeBioWindow()
			self.wndBio.LoadGift(int(level))
		def SetBioEmpty(self):
			if self.MakeBioWindow() == False:
				self.wndBio.LoadEmpty()

	if app.dracaryS_DUNGEON_LIB:
		def MakeDungeonTimerWindow(self):
			self.wndDungeonTimer = uiDungeonTimer.Cooldown()
			self.wndDungeonTimer.Hide()

	if app.ENABLE_DUNGEON_INFO:
		def MakeDungeonInfo(self):
			if self.wndDungeonInfo == None:
				self.wndDungeonInfo = uiDungeonInfo.DungeonInfo()
		def OpenDungeonInfo(self):
			self.MakeDungeonInfo()
			if self.wndDungeonInfo.IsShow():
				self.wndDungeonInfo.Close()
			else:
				self.wndDungeonInfo.Open()

	if app.ENABLE_BATTLE_PASS:
		def MakeBattlePassWindow(self):
			if self.wndBattlePassEx == None:
				self.wndBattlePassEx = uiBattlePassEx.BattlePassWindow()
		def OpenBattlePass(self):
			self.MakeBattlePassWindow()
			if self.wndBattlePassEx.IsShow():
				self.wndBattlePassEx.Close()
			else:
				self.wndBattlePassEx.Open()
		def BattlePassSetStatusEx(self, status):
			self.MakeBattlePassWindow()
			self.wndBattlePassEx.SetBattlePassStatusEx(int(status))
		def BattlePassSetStatus(self, status, leftTime, reward):
			self.MakeBattlePassWindow()
			self.wndBattlePassEx.SetBattlePassStatus(int(status), int(leftTime), str(reward))
		def BattlePassSetMission(self, missionIndex, missionValue):
			self.MakeBattlePassWindow()
			self.wndBattlePassEx.SetMission(int(missionIndex), int(missionValue))
		def BattlePassAppendMission(self, missionIndex, missionReward, missionValue, missionMaxValue, missionSubValue, missinVecIndex):
			self.MakeBattlePassWindow()
			self.wndBattlePassEx.AppendMission(int(missionIndex), str(missionReward), int(missionValue), int(missionMaxValue), int(missionSubValue), int(missinVecIndex))
		def BattlePassClear(self):
			self.MakeBattlePassWindow()
			self.wndBattlePassEx.BattlePassClear()

	if app.ENABLE_ITEMSHOP:
		def MakeItemShopWindow(self):
			if self.wndItemShop == None:
				self.wndItemShop = uiItemShopNew.ItemShopWindow()
		def OpenItemShopWindow(self):
			self.MakeItemShopWindow()
			if self.wndItemShop.IsShow():
				self.wndItemShop.Close()
			else:
				self.wndItemShop.Open()
		def OpenItemShopMainWindow(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.LoadFirstOpening()
		def ItemShopHideLoading(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.CloseLoading()
		def ItemShopPurchasesWindow(self):
			self.MakeItemShopWindow()
			self.wndItemShop.Open()
			self.wndItemShop.OpenPurchasesWindow()
		def ItemShopUpdateItem(self, itemID, itemMaxSellingCount):
			self.MakeItemShopWindow()
			self.wndItemShop.UpdateItem(itemID, itemMaxSellingCount)
		def ItemShopSetDragonCoin(self,dragonCoin):
			self.MakeItemShopWindow()
			self.wndItemShop.SetDragonCoin(dragonCoin)
		def SetWheelItemData(self, cmd):
			self.MakeItemShopWindow()
			self.wndItemShop.SetWheelItemData(str(cmd))
		def OnSetWhell(self, giftIndex):
			self.MakeItemShopWindow()
			self.wndItemShop.OnSetWhell(int(giftIndex))
		def GetWheelGiftData(self, itemVnum, itemCount):
			self.MakeItemShopWindow()
			self.wndItemShop.GetWheelGiftData(int(itemVnum), int(itemCount))
	
	if app.ENABLE_EVENT_MANAGER:
		def MakeEventIcon(self):
			if self.wndEventIcon == None:
				self.wndEventIcon = uiEventCalendarNew.MovableImage()
				self.wndEventIcon.Show()
		def MakeEventCalendar(self):
			if self.wndEventManager == None:
				self.wndEventManager = uiEventCalendarNew.EventCalendarWindow()
		def OpenEventCalendar(self):
			self.MakeEventCalendar()
			if self.wndEventManager.IsShow():
				self.wndEventManager.Close()
			else:
				self.wndEventManager.Open()
		def RefreshEventStatus(self, eventID, eventStatus, eventendTime, eventEndTimeText):
			if eventendTime != 0:
				eventendTime += app.GetGlobalTimeStamp()
			uiEventCalendarNew.SetEventStatus(eventID, eventStatus, eventendTime, eventEndTimeText)
			self.RefreshEventManager()
		def ClearEventManager(self):
			uiEventCalendarNew.server_event_data={}
		def RefreshEventManager(self):
			if self.wndEventManager:
				self.wndEventManager.Refresh()
			if self.wndEventIcon:
				self.wndEventIcon.Refresh()
		def AppendEvent(self, dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart):
			self.MakeEventCalendar()
			self.MakeEventIcon()
			#import dbg
			#dbg.TraceError("startTime: %d endTime: %d"%(startRealTime, endRealTime))
			if startRealTime != 0:
				startRealTime += app.GetGlobalTimeStamp()
			if endRealTime != 0:
				endRealTime += app.GetGlobalTimeStamp()
			uiEventCalendarNew.SetServerData(dayIndex, eventID, eventIndex, startTime, endTime, empireFlag, channelFlag, value0, value1, value2, value3, startRealTime, endRealTime, isAlreadyStart)
	
	if app.ENABLE_SHOW_CHEST_DROP:
		def OpenChestDropWindow(self, itemVnum, itemWindow, itemCell):
			if self.wndChestDropInfo:
				self.wndChestDropInfo.Open(itemVnum, itemWindow, itemCell)

	if app.ENABLE_RARITY:
		def MakeRarityMessageProcess(self):
			if self.wndRarityQueque == None:
				self.wndRarityQueque = ui.RarityNotification()
		def AddRarityMessage(self, type, percent):
			self.MakeRarityMessageProcess()
			self.wndRarityQueque.OnMessage(int(type),int(percent))

	if app.ENABLE_WIKI:
		def OpenWikiWindow(self):
			self.__MakeWiki()
			if self.wndWiki.IsShow():
				self.wndWiki.Close()
			else:
				self.wndWiki.Open()
		def __MakeWiki(self):
			if self.wndWiki == None:
				self.wndWiki = uiWiki.EncyclopediaofGame()

	if app.ENABLE_RENDER_TARGET:
		def MakeRenderTargetWindow(self):
			if self.wndRenderTarget == None:
				self.wndRenderTarget = uiRenderTarget.RenderTargetWindow()
		def OpenRenderTargetWindow(self, renderType = 0, renderVnum = 11299):
			self.MakeRenderTargetWindow()
			self.wndRenderTarget.Open(renderType, renderVnum)

	if app.ENABLE_DISCORD_STUFF:
		def OpenWhisperWithMessage(self, name):
			if not self.whisperDialogDict.has_key(name):
				btn = self.__FindWhisperButton(name)
				if 0 != btn:
					self.ShowWhisperDialog(btn)
		def CheckWhisperIsOpen(self, name):
			if self.whisperDialogDict:
				if self.whisperDialogDict.has_key(name):
					return self.whisperDialogDict[name].IsShow()
			return False

	if app.ENABLE_ZODIAC_MISSION:
		def __Make12ziRewardWindow(self):
			self.wnd12ziReward = ui12zi.Reward12ziWindow()
			self.wnd12ziReward.SetItemToolTip(self.tooltipItem)
			self.wnd12ziReward.Hide()
		def __Make12ziTimerWindow(self):
			self.wnd12ziTimer = ui12zi.FloorLimitTimeWindow()
			self.wnd12ziTimer.Hide()

	if app.ENABLE_TRACK_WINDOW:
		def TrackWindowCheckPacket(self):
			self.wndTrackWindow.CheckPacket()
		def MakeTrackWindow(self):
			if self.wndTrackWindow == None:
				self.wndTrackWindow = uiTrack.TrackWindow()
		def OpenTrackWindow(self):
			self.MakeTrackWindow()
			if self.wndTrackWindow.IsShow():
				self.wndTrackWindow.Close()
			else:
				self.wndTrackWindow.Open()
		def TrackDungeonInfo(self, cmdData):
			self.MakeTrackWindow()
			self.wndTrackWindow.TrackDungeonInfo(cmdData)
		def TrackBossInfo(self, bossID, bossLeftTime, bossChannel):
			self.MakeTrackWindow()
			self.wndTrackWindow.TrackBossInfo(int(bossID), int(bossLeftTime), int(bossChannel))

	if app.ENABLE_FISH_GAME:
		def MakeFishGameWindow(self):
			if self.wndFishGame == None:
				self.wndFishGame = uiFishGame.FishGameWindow()
		def OpenFishGameWindow(self, gameKey):
			self.MakeFishGameWindow()
			self.wndFishGame.Open(int(gameKey))
		def SetFishGameGoal(self, goalCount):
			self.MakeFishGameWindow()
			self.wndFishGame.SetFishScore(int(goalCount))
		def CloseFishGame(self):
			self.MakeFishGameWindow()
			self.wndFishGame.Hide()

	if app.ENABLE_EXCHANGE_LOG:
		def MakeExchangeLogWindow(self):
			if self.wndExchangeLog == None:
				self.wndExchangeLog = uiExchangeLog.ExchangeLog()
		def OpenExchangeLog(self):
			self.MakeExchangeLogWindow()
			if self.wndExchangeLog.IsShow():
				self.wndExchangeLog.Close()
			else:
				self.wndExchangeLog.Open()
		def ExchangeLogClear(self, playerCode):
			if self.wndExchangeLog:
				self.wndExchangeLog.Clear(playerCode)
		def ExchangeLogRefresh(self, isLogItemRefresh):
			if self.wndExchangeLog:
				if isLogItemRefresh:
					self.wndExchangeLog.RefreshItems(isLogItemRefresh)
				else:
					self.wndExchangeLog.Refresh()
		def ExchangeLogAppend(self, logID, ownerName, ownerGold, ownerIP, targetName, targetGold, targetIP, date):
			if self.wndExchangeLog:
				self.wndExchangeLog.ExchangeLogAppend(logID, ownerName, ownerGold, ownerIP, targetName, targetGold, targetIP, date)
		def ExchangeLogItemAppend(self, logID, itemPos, itemVnum, itemCount, metinSlot, attrType, attrValue, isOwnerItem):
			if self.wndExchangeLog:
				self.wndExchangeLog.ExchangeLogItemAppend(logID, itemPos, itemVnum, itemCount, metinSlot, attrType, attrValue, isOwnerItem)

	if app.ENABLE_GEM_SYSTEM:
		def MakeGemShopWindow(self):
			if self.wndGemShop == None:
				self.wndGemShop = uiGem.GemShop()
		def OpenGemShop(self):
			self.MakeGemShopWindow()
			if self.wndGemShop.IsShow():
				self.wndGemShop.Close()
			else:
				self.wndGemShop.Open()
		def GemUpdateSlotCount(self, slotCount):
			if self.wndGemShop:
				self.wndGemShop.UpdateSlotCount(int(slotCount))
		def GemClear(self):
			if self.wndGemShop:
				self.wndGemShop.Clear()
		def GemSetRefreshLeftTime(self, leftTime):
			if self.wndGemShop:
				self.wndGemShop.SetRefreshLeftTime(int(leftTime))
		def GemSetItemsWithString(self, cmdData):
			if self.wndGemShop:
				self.wndGemShop.SetItemsWithString(cmdData)
		def GemSetBuyedSlot(self, slotIndex, buyedStatus):
			if self.wndGemShop:
				self.wndGemShop.SetBuyedSlot(int(slotIndex), int(buyedStatus))

	if app.ENABLE_MINI_GAME_CATCH_KING:
		def MiniGameCatchKingEventStart(self, bigScore):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.GameStart(bigScore)

		def MiniGameCatchKingSetHandCard(self, cardNumber):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingSetHandCard(cardNumber)

		def MiniGameCatchKingResultField(self, score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingResultField(score, rowType, cardPos, cardValue, keepFieldCard, destroyHandCard, getReward, isFiveNear)

		def MiniGameCatchKingSetEndCard(self, cardPos, cardNumber):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingSetEndCard(cardPos, cardNumber)

		def MiniGameCatchKingReward(self, rewardCode):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.CatchKingReward(rewardCode)

		def ClickCatchKingEventButton(self):
			if self.wndCatchKingGame:
				self.wndCatchKingGame.Open()

		def MiniGameCatchKing(self, value):
			import dbg
			if int(value) == 0:
				self.wndCatchKingIcon.Hide()
			else:
				self.wndCatchKingIcon.Show()

	if app.RENEWAL_MISSION_BOOKS:
		def MakeBookMission(self):
			if self.wndBookMission == None:
				self.wndBookMission = uiMission.MissionWindow()
		def OpenBookMission(self):
			self.MakeBookMission()
			if self.wndBookMission.IsShow():
				self.wndBookMission.Close()
			else:
				self.wndBookMission.Open()
		def ClearBookMission(self):
			self.MakeBookMission()
			self.wndBookMission.Clear()
		def UpdateMissionInfo(self, cmd):
			self.wndBookMission.UpdateMissionInfo(cmd)
		def UpdateMissionValue(self, missionID, value):
			self.wndBookMission.UpdateMissionValue(int(missionID), int(value))
		def RewardMissionData(self, missionID, rewardStatus):
			self.wndBookMission.RewardMissionData(int(missionID), int(rewardStatus))
		def RemoveMissionData(self, missionID):
			self.wndBookMission.RemoveMissionData(int(missionID))
		def UpdateMissionEndTime(self, missionID, endTime):
			self.wndBookMission.UpdateMissionEndTime(int(missionID), str(endTime))

	if app.ENABLE_PVP_TOURNAMENT:
		def MakePvPDuel(self):
			if self.wndPvPDuel == None:
				self.wndPvPDuel= uiPvPDuel.DuelInfoWindow()

		def SetPvPTournamentClear(self, arenaIndex):
			self.MakePvPDuel()
			self.wndPvPDuel.ClearArena(arenaIndex)

		def SetPvPTournamentStartTime(self, arenaIndex, serverStartTime):
			self.MakePvPDuel()
			self.wndPvPDuel.SetStartTime(arenaIndex, serverStartTime)

		def SetPvPTournamentRace(self, arenaIndex, playerIndex, playerRace):
			self.MakePvPDuel()
			self.wndPvPDuel.SetRace(arenaIndex, playerIndex, playerRace)

		def SetPvPTournamentScore(self, arenaIndex, playerIndex, playerScore):
			self.MakePvPDuel()
			self.wndPvPDuel.SetScore(arenaIndex, playerIndex, playerScore)

		def SetPvPTournamentName(self, arenaIndex, playerIndex, playerName):
			self.MakePvPDuel()
			self.wndPvPDuel.SetName(arenaIndex, playerIndex, playerName)

		def SetPvPTournamentHP(self, arenaIndex, playerIndex, playerHPPercent, playerMinHP, playerMaxHP, isPoisoned):
			self.MakePvPDuel()
			self.wndPvPDuel.SetHP(arenaIndex, playerIndex, playerHPPercent, playerMinHP, playerMaxHP, isPoisoned)

		def MakePvPDuelPanel(self):
			if self.wndPvPDuelPanel == None:
				self.wndPvPDuelPanel = uiPvPDuel.PvPDuelAdminPanel()

		def OpenPvPDuelPanel(self):
			self.MakePvPDuelPanel()
			self.wndPvPDuelPanel.Show()

	if app.__SKILL_TREE__:
		def MakeOpenSkillTree(self):
			if self.wndSkillTree == None:
				self.wndSkillTree = uiSkillTree.SkillTreeWindow()
		def OpenSkillTree(self):
			self.MakeOpenSkillTree()
			if self.wndSkillTree.IsShow():
				self.wndSkillTree.Close()
			else:
				self.wndSkillTree.Open()
		def SkillTreeLoad(self, skillData, leftTime, isActive):
			self.MakeOpenSkillTree()
			self.wndSkillTree.SkillTreeLoad(str(skillData), int(leftTime), int(isActive))
		def SkillTreeSetTime(self, leftTime):
			if self.wndSkillTree:
				self.wndSkillTree.SkillTreeSetTime(int(leftTime))
		def SkillTreeSetLevel(self, skillIdx, newLevel):
			if self.wndSkillTree:
				self.wndSkillTree.SkillTreeSetLevel(int(skillIdx), int(newLevel))
		def SkillTreeSetStatus(self, newStatus, leftTime):
			self.MakeOpenSkillTree()
			self.wndSkillTree.SkillTreeSetStatus(newStatus, int(leftTime))

	if app.ENABLE_BLACKJACK_GAME:
		def MakeBlackJackGameWindow(self):
			if self.wndBlackJackGame == None:
				self.wndBlackJackGame = uiBlackJack.BlackJackGame()
		def OpenBlackJackGame(self):
			self.MakeBlackJackGameWindow()
			if self.wndBlackJackGame.IsShow():
				self.wndBlackJackGame.Close()
			else:
				self.wndBlackJackGame.Open()
		def BJAddNewCard(self, isBot, cardType, cardIndex, returnValue):
			self.MakeBlackJackGameWindow()
			self.wndBlackJackGame.AddNewCard(int(isBot), int(cardType), int(cardIndex), int(returnValue))
		def BJSetGameMode(self, gameKey):
			self.MakeBlackJackGameWindow()
			self.wndBlackJackGame.SetGameMode(int(gameKey))
		def BJShowGameStatus(self, isBotWin):
			self.MakeBlackJackGameWindow()
			self.wndBlackJackGame.ShowGameStatus(int(isBotWin))

	if app.ENABLE_RENEWAL_TELEPORT_SYSTEM:
		def OpenWarpWindow(self):
			if self.wndWarpWindow.IsShow():
				self.wndWarpWindow.Close()
			else:
				self.wndWarpWindow.Open()

	if app.__AUTO_HUNT__:
		def AutoHuntStatus(self, status):
			if self.wndAutoHunt:
				self.wndAutoHunt.SetStatus(True if int(status) else False)
		def OpenAutoHunt(self):
			if self.wndAutoHunt == None:
				self.wndAutoHunt = uiAutoHunt.Window()
			if self.wndAutoHunt.IsShow():
				self.wndAutoHunt.Close()
			else:
				self.wndAutoHunt.Open()

	if app.ENABLE_MOVE_CHANNEL:
		def RefreshServerInfo(self):
			if self.wndMiniMap:
				self.wndMiniMap.RefreshServerInfo()

	if app.ENABLE_MAINTENANCE_SYSTEM:
		def ShowMaintenanceSign(self, timeLeft, duration):
			if self.wndMaintenance:
				self.wndMaintenance.Open(timeLeft, duration)

		def HideMaintenanceSign(self):
			if self.wndMaintenance:
				self.wndMaintenance.Close()

	if app.ENABLE_AURA_SYSTEM:
		def AuraWindowOpen(self, type):
			if self.wndAura.IsShow():
				return

			# if self.inputDialog or self.privateShopBuilder.IsShow():# or shop.GetNameDialogOpen():
				# chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_OPEN_PRIVATE_SHOP)
				# return

			if self.dlgRefineNew and self.dlgRefineNew.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_OPEN_REFINE)
				return

			self.wndAura.Open(type)

			if not self.wndInventory.IsShow():
				self.wndInventory.Show()

		def AuraWindowClose(self):
			if not self.wndAura.IsShow():
				return

			self.wndAura.CloseWindow()

	if app.ENABLE_SET_CUSTOM_ATTRIBUTE_SYSTEM:
		def SetCustomAttributeWindow(self, itemCellPos, attrEnchantProb, attrDataList):
			if not self.wndSetCustomAttribute:
				return

			self.wndSetCustomAttribute.Open(itemCellPos, attrEnchantProb, attrDataList)

if __name__ == "__main__":

	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui
	import localeInfo

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	class TestGame(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)

			localeInfo.LoadLocaleData()
			player.SetItemData(0, 27001, 10)
			player.SetItemData(1, 27004, 10)

			self.interface = Interface()
			self.interface.MakeInterface()
			self.interface.ShowDefaultWindows()
			self.interface.RefreshInventory()
			#self.interface.OpenCubeWindow()

		def __del__(self):
			ui.Window.__del__(self)

		def OnUpdate(self):
			app.UpdateGame()

		def OnRender(self):
			app.RenderGame()
			grp.PopState()
			grp.SetInterfaceRenderState()

	game = TestGame()
	game.SetSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	game.Show()

	app.Loop()
