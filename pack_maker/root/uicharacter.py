import ui
import uiScriptLocale
import app
import net
import dbg
import snd
import player
import mouseModule
import wndMgr
import skill
import playerSettingModule
import quest
import localeInfo
import uiToolTip
import constInfo
import emotion
import chr
import playerLoad

if app.ENABLE_NEW_DETAILS_GUI:
	import uiCharacterDetails

SHOW_ONLY_ACTIVE_SKILL = False
SHOW_LIMIT_SUPPORT_SKILL_LIST = []
HIDE_SUPPORT_SKILL_POINT = False

if app.ENABLE_CONQUEROR_LEVEL:
	HIDE_SUPPORT_SKILL_POINT = TRUE
	SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 123, 124, 126, 127, 129, 128, 131, 137, 138, 139, 140, 132, 133, 134, 246]
else:
	if localeInfo.IsYMIR():
		SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 123, 124, 126, 127, 129, 128, 131, 137, 138, 139, 140,141,142]
		[121, 122, 123, 124, 126, 127, 129, 128, 131, 137, 138, 139, 140, 0, 0, 0, 0]
		if not localeInfo.IsCHEONMA():
			HIDE_SUPPORT_SKILL_POINT = TRUE 
			SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 123, 124, 126, 127, 129, 128, 131, 137, 138, 139, 140,141,142]
	elif localeInfo.IsJAPAN() or   (localeInfo.IsEUROPE() and app.GetLocalePath() != "locale/ca") and (localeInfo.IsEUROPE() and app.GetLocalePath() != "locale/br"):
		HIDE_SUPPORT_SKILL_POINT = TRUE	
		SHOW_LIMIT_SUPPORT_SKILL_LIST = [121, 122, 123, 124, 126, 127, 129, 128, 131, 137, 138, 139, 140]

	else:
		HIDE_SUPPORT_SKILL_POINT = TRUE


FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
	playerSettingModule.RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
	playerSettingModule.RACE_SURA_M		: "icon/face/sura_m.tga",
	playerSettingModule.RACE_SURA_W		: "icon/face/sura_w.tga",
	playerSettingModule.RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
	playerSettingModule.RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
}
if app.ENABLE_WOLFMAN_CHARACTER:
	FACE_IMAGE_DICT.update({playerSettingModule.RACE_WOLFMAN_M  : "icon/face/wolfman_m.tga",})

def unsigned32(n):
	return n & 0xFFFFFFFFL

class CharacterWindow(ui.ScriptWindow):

	if app.ENABLE_CONQUEROR_LEVEL:
		ACTIVE_PAGE_SLOT_COUNT = 9
		SUPPORT_PAGE_SLOT_COUNT = 18
	else:
		ACTIVE_PAGE_SLOT_COUNT = 8	
		SUPPORT_PAGE_SLOT_COUNT = 12

	PAGE_SLOT_COUNT = 12
	PAGE_HORSE = 2
	
	if app.ENABLE_NEW_DETAILS_GUI:
		chDetailsWnd = None
		isOpenedDetailsWnd = False

	SKILL_GROUP_NAME_DICT = {
		playerSettingModule.JOB_WARRIOR	: { 1 : localeInfo.SKILL_GROUP_WARRIOR_1,	2 : localeInfo.SKILL_GROUP_WARRIOR_2, },
		playerSettingModule.JOB_ASSASSIN	: { 1 : localeInfo.SKILL_GROUP_ASSASSIN_1,	2 : localeInfo.SKILL_GROUP_ASSASSIN_2, },
		playerSettingModule.JOB_SURA		: { 1 : localeInfo.SKILL_GROUP_SURA_1,		2 : localeInfo.SKILL_GROUP_SURA_2, },
		playerSettingModule.JOB_SHAMAN		: { 1 : localeInfo.SKILL_GROUP_SHAMAN_1,	2 : localeInfo.SKILL_GROUP_SHAMAN_2, },
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		SKILL_GROUP_NAME_DICT.update({playerSettingModule.JOB_WOLFMAN		: { 1 : localeInfo.JOB_WOLFMAN1,	2 : localeInfo.JOB_WOLFMAN2, },})

	STAT_DESCRIPTION =	{
		"HTH" : localeInfo.STAT_TOOLTIP_CON,
		"INT" : localeInfo.STAT_TOOLTIP_INT,
		"STR" : localeInfo.STAT_TOOLTIP_STR,
		"DEX" : localeInfo.STAT_TOOLTIP_DEX,
	}

	if app.ENABLE_CONQUEROR_LEVEL:
		STAT_SUNGMA_DESCRIPTION = {
			"SMH_STR" : localeInfo.STAT_TOOLTIP_SUNGMA_STR,
			"SMH_HP" : localeInfo.STAT_TOOLTIP_SUNGMA_HP,
			"SMH_MOVE" : localeInfo.STAT_TOOLTIP_SUNGMA_MOVE,
			"SMH_INMUNE" : localeInfo.STAT_TOOLTIP_SUNGMA_IMMUNE,
		}


	STAT_MINUS_DESCRIPTION = localeInfo.STAT_MINUS_DESCRIPTION

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.state = "STATUS"

		self.isLoaded = 0

		self.toolTipSkill = 0

		self.__Initialize()
		self.__LoadWindow()

		self.statusPlusCommandDict={
			"HTH" : "/s_val_w ht ",
			"INT" : "/s_val_w iq ",
			"STR" : "/s_val_w st ",
			"DEX" : "/s_val_w dx ",
		}
		
		if app.DISABLE_OLD_MINUS:
			self.statusMinusCommandDict={
				"HTH-" : "/stat_val- ht",
				"INT-" : "/stat_val- iq",
				"STR-" : "/stat_val- st",
				"DEX-" : "/stat_val- dx",
			}
		else:
			self.statusMinusCommandDict={
				"HTH-" : "/stat- ht",
				"INT-" : "/stat- iq",
				"STR-" : "/stat- st",
				"DEX-" : "/stat- dx",
			}

		if app.ENABLE_CONQUEROR_LEVEL:
			self.substate = "BASE"
	
			self.statusConquerorPlusCommandDict={
				"SMH_STR" : "/conqueror_stat smh_str",
				"SMH_HP" : "/conqueror_stat smh_hp",
				"SMH_MOVE" : "/conqueror_stat smh_move",
				"SMH_INMUNE" : "/conqueror_stat smh_inmune",
			}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.refreshToolTip = 0
		self.curSelectedSkillGroup = 0
		self.canUseHorseSkill = -1
		if app.ENABLE_NEW_DETAILS_GUI:
			self.ExpandBtn = None
			self.MinimizeBtn = None
			self.chDetailsWnd = None
			self.isOpenedDetailsWnd = False

		self.toolTip = None
		self.toolTipJob = None
		self.toolTipAlignment = None
		self.toolTipSkill = None

		self.faceImage = None
		self.statusPlusLabel = None
		self.statusPlusValue = None
		self.activeSlot = None
		self.tabDict = None
		self.tabButtonDict = None
		self.pageDict = None
		self.titleBarDict = None
		self.statusPlusButtonDict = None

		if app.ENABLE_CONQUEROR_LEVEL:
			self.statusConquerorPlusButtonDict = None

		self.statusMinusButtonDict = None

		self.skillPageDict = None
		self.questShowingStartIndex = 0
		self.questScrollBar = None
		self.questSlot = None
		self.questNameList = None
		self.questLastTimeList = None
		self.questLastCountList = None
		self.skillGroupButton = ()

		self.activeSlot = None
		self.activeSkillPointValue = None
		self.supportSkillPointValue = None
		self.skillGroupButton1 = None
		self.skillGroupButton2 = None
		self.activeSkillGroupName = None

		self.guildNameSlot = None
		self.guildNameValue = None
		self.characterNameSlot = None
		self.characterNameValue = None

		self.emotionToolTip = None
		self.soloEmotionSlot = None
		self.dualEmotionSlot = None

		if app.ENABLE_CONQUEROR_LEVEL:
			self.toolTipConquerorInfoButton = None
			
			self.tabSungmaButtonDict = None
			self.SungmaButton = None

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)
		if app.ENABLE_NEW_DETAILS_GUI:
			self.__InitCharacterDetailsUIButton()
			if self.chDetailsWnd and self.isOpenedDetailsWnd:
				self.chDetailsWnd.Show()
				self.SetTop()

	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)

	def __BindObject(self):
		self.toolTip = uiToolTip.ToolTip()
		self.toolTipJob = uiToolTip.ToolTip()
		self.toolTipAlignment = uiToolTip.ToolTip(130)

		if app.ENABLE_CONQUEROR_LEVEL:
			self.toolTipConquerorInfoButton = uiToolTip.ToolTip()

		self.faceImage = self.GetChild("Face_Image")

		faceSlot=self.GetChild("Face_Slot")
		if 949 == app.GetDefaultCodePage():
			faceSlot.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowJobToolTip)
			faceSlot.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideJobToolTip)

		self.statusPlusLabel = self.GetChild("Status_Plus_Label")
		self.statusPlusValue = self.GetChild("Status_Plus_Value")

		self.characterNameSlot = self.GetChild("Character_Name_Slot")
		self.characterNameValue = self.GetChild("Character_Name")
		self.guildNameSlot = self.GetChild("Guild_Name_Slot")
		self.guildNameValue = self.GetChild("Guild_Name")
		self.characterNameSlot.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowAlignmentToolTip)
		self.characterNameSlot.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideAlignmentToolTip)

		self.activeSlot = self.GetChild("Skill_Active_Slot")
		self.activeSkillPointValue = self.GetChild("Active_Skill_Point_Value")
		self.supportSkillPointValue = self.GetChild("Support_Skill_Point_Value")
		self.skillGroupButton1 = self.GetChild("Skill_Group_Button_1")
		self.skillGroupButton2 = self.GetChild("Skill_Group_Button_2")
		self.activeSkillGroupName = self.GetChild("Active_Skill_Group_Name")

		self.tabDict = {
			"STATUS"	: self.GetChild("Tab_01"),
			"SKILL"		: self.GetChild("Tab_02"),
			"EMOTICON"	: self.GetChild("Tab_03"),
			"QUEST"		: self.GetChild("Tab_04"),
		}

		self.tabButtonDict = {
			"STATUS"	: self.GetChild("Tab_Button_01"),
			"SKILL"		: self.GetChild("Tab_Button_02"),
			"EMOTICON"	: self.GetChild("Tab_Button_03"),
			"QUEST"		: self.GetChild("Tab_Button_04")
		}

		self.pageDict = {
			"STATUS"	: self.GetChild("Character_Page"),
			"SKILL"		: self.GetChild("Skill_Page"),
			"EMOTICON"	: self.GetChild("Emoticon_Page"),
			"QUEST"		: self.GetChild("Quest_Page")
		}

		self.titleBarDict = {
			"STATUS"	: self.GetChild("Character_TitleBar"),
			"SKILL"		: self.GetChild("Skill_TitleBar"),
			"EMOTICON"	: self.GetChild("Emoticon_TitleBar"),
			"QUEST"		: self.GetChild("Quest_TitleBar")
		}

		self.statusPlusButtonDict = {
			"HTH"		: self.GetChild("HTH_Plus"),
			"INT"		: self.GetChild("INT_Plus"),
			"STR"		: self.GetChild("STR_Plus"),
			"DEX"		: self.GetChild("DEX_Plus"),
		}

		self.statusMinusButtonDict = {
			"HTH-"		: self.GetChild("HTH_Minus"),
			"INT-"		: self.GetChild("INT_Minus"),
			"STR-"		: self.GetChild("STR_Minus"),
			"DEX-"		: self.GetChild("DEX_Minus"),
		}

		self.skillPageDict = {
			"ACTIVE" : self.GetChild("Skill_Active_Slot"),
			"SUPPORT" : self.GetChild("Skill_ETC_Slot"),
			"HORSE" : self.GetChild("Skill_Active_Slot"),
		}

		self.skillPageStatDict = {
			"SUPPORT"	: player.SKILL_SUPPORT,
			"ACTIVE"	: player.SKILL_ACTIVE,
			"HORSE"		: player.SKILL_HORSE,
		}

		self.skillGroupButton = (
			self.GetChild("Skill_Group_Button_1"),
			self.GetChild("Skill_Group_Button_2"),
		)

		if app.ENABLE_CONQUEROR_LEVEL:
			self.tabSungmaButtonDict = {
				"BASE"		: self.GetChild("change_base_button"),
				"SUNGMA"	: self.GetChild("change_conqueror_button")
			}
			
			self.SungmaPageDict = {
				"BASE" : self.GetChild("base_info"),
				"SUNGMA" : self.GetChild("sungma_info"),
			}
			
			self.statusConquerorPlusButtonDict = {
				"SMH_STR"		: self.GetChild("sungma_str_plus"),
				"SMH_HP"		: self.GetChild("sungma_hp_plus"),
				"SMH_MOVE"		: self.GetChild("sungma_move_plus"),
				"SMH_INMUNE"		: self.GetChild("sungma_immune_plus"),
			}			
			
			self.HTH_IMG = self.GetChild("HTH_IMG")
			self.INT_IMG = self.GetChild("INT_IMG")
			self.STR_IMG = self.GetChild("STR_IMG")
			self.DEX_IMG = self.GetChild("DEX_IMG")
			

			## TabButton1 (Character)
			self.GetChild("Tab_Button_01").SetShowToolTipEvent(ui.__mem_func__(self.__ShowToolTipButton), localeInfo.STAT_TOOLTIP_TAB_CHARACTER)
			self.GetChild("Tab_Button_01").SetHideToolTipEvent(ui.__mem_func__(self.__HideToolTip))
			## TabButton2 (Skill)
			self.GetChild("Tab_Button_02").SetShowToolTipEvent(ui.__mem_func__(self.__ShowToolTipButton), localeInfo.STAT_TOOLTIP_TAB_SKILL)
			self.GetChild("Tab_Button_02").SetHideToolTipEvent(ui.__mem_func__(self.__HideToolTip))
			## TabButton3 (Emoticon)
			self.GetChild("Tab_Button_03").SetShowToolTipEvent(ui.__mem_func__(self.__ShowToolTipButton), localeInfo.STAT_TOOLTIP_TAB_EMOTICON)
			self.GetChild("Tab_Button_03").SetHideToolTipEvent(ui.__mem_func__(self.__HideToolTip))
			## TabButton4 (Quest)
			self.GetChild("Tab_Button_04").SetShowToolTipEvent(ui.__mem_func__(self.__ShowToolTipButton), localeInfo.STAT_TOOLTIP_TAB_QUEST)
			self.GetChild("Tab_Button_04").SetHideToolTipEvent(ui.__mem_func__(self.__HideToolTip))

			## Level
			self.GetChild("Lv_ToolTip").SetShowToolTipEvent(ui.__mem_func__(self.__ShowToolTipButton), localeInfo.STAT_TOOLTIP_LEVEL)
			self.GetChild("Lv_ToolTip").SetHideToolTipEvent(ui.__mem_func__(self.__HideToolTip))
			## EXP
			self.GetChild("Exp_ToolTip").SetShowToolTipEvent(ui.__mem_func__(self.__ShowToolTipButton), localeInfo.STAT_TOOLTIP_EXP)
			self.GetChild("Exp_ToolTip").SetHideToolTipEvent(ui.__mem_func__(self.__HideToolTip))

			## Base Level
			self.GetChild("change_base_button").SetShowToolTipEvent(ui.__mem_func__(self.__ShowToolTipButton), localeInfo.STAT_TOOLTIP_BASE_LEVEL)
			self.GetChild("change_base_button").SetHideToolTipEvent(ui.__mem_func__(self.__HideToolTip))
			## Conqueror Level
			self.GetChild("change_conqueror_button").SetShowToolTipEvent(ui.__mem_func__(self.__ShowToolTipButton), localeInfo.STAT_TOOLTIP_CONQUEROR_LEVEL)
			self.GetChild("change_conqueror_button").SetHideToolTipEvent(ui.__mem_func__(self.__HideToolTip))
			## Passive Relic
			self.passive_expanded_btn = self.GetChild("passive_expanded_btn")
			self.passive_expanded_btn.SetShowToolTipEvent(ui.__mem_func__(self.__ShowToolTipButton), localeInfo.STAT_TOOLTIP_PASSIVE)
			self.passive_expanded_btn.SetHideToolTipEvent(ui.__mem_func__(self.__HideToolTip))
			self.passive_expanded_btn.Hide()

			## Char Status Info
			self.GetChild("Char_Info_Status_img").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_STAT : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("Char_Info_Status_img").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## Status Plus Points
			self.GetChild("Status_Plus_Label").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_POINT : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("Status_Plus_Label").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

			## CON (Constitution)
			self.GetChild("HTH_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_IMG_CON : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("HTH_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## INT (Intelligence)
			self.GetChild("INT_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_IMG_INT : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("INT_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## STR (Strength)
			self.GetChild("STR_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_IMG_STR : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("STR_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## DEX (Dexterity)
			self.GetChild("DEX_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_IMG_DEX : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("DEX_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

			## HP (Health)
			self.GetChild("HEL_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_HP : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("HEL_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## SP (Stamina)
			self.GetChild("SP_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SP : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("SP_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## ATT (Attack)
			self.GetChild("ATT_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_ATT : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("ATT_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## DEF (Defense)
			self.GetChild("DEF_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_DEF : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("DEF_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

			## MSPD (Move Speed)
			self.GetChild("MSPD_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_MOVE_SPEED : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("MSPD_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## ASPD (Attack Speed)
			self.GetChild("ASPD_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_ATT_SPEED : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("ASPD_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## CSPD (Cast Speed)
			self.GetChild("CSPD_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_CAST_SPEED : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("CSPD_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## MATT (Magic Attack)
			self.GetChild("MATT_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_MAG_ATT : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("MATT_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## MDEF (Magic Defense)
			self.GetChild("MDEF_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_MAG_DEF : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("MDEF_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## EF (Evasion Resistance)
			self.GetChild("ER_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_DODGE_PER : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("ER_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

			## SUNGMA_STR
			self.GetChild("SUNGMA_STR_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SUNGMA_STR : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("SUNGMA_STR_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## SUNGMA_HP
			self.GetChild("SUNGMA_HP_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SUNGMA_HP : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("SUNGMA_HP_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## SUNGMA_MOVE
			self.GetChild("SUNGMA_MOVE_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SUNGMA_MOVE : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("SUNGMA_MOVE_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## SUNGMA_IMMUNE
			self.GetChild("SUNGMA_IMMUNE_IMG").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SUNGMA_IMMUNE : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("SUNGMA_IMMUNE_IMG").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

			## Active Skill Point Label
			self.GetChild("Active_Skill_Point_Label").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_POINT : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("Active_Skill_Point_Label").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			## Support Skill Point Label
			self.GetChild("Support_Skill_ToolTip").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SUPPORT_SKILL : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("Support_Skill_ToolTip").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

			self.GetChild("Action_Bar_Img").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_ACTION : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("Action_Bar_Img").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			self.GetChild("Reaction_Bar_Img").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_REACTION : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("Reaction_Bar_Img").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()
			self.GetChild("Special_Action_Bar_Img").OnMouseOverIn = lambda arg = localeInfo.STAT_TOOLTIP_SPECIAL_ACTION : ui.__mem_func__(self.__ShowToolTip)(arg)
			self.GetChild("Special_Action_Bar_Img").OnMouseOverOut = lambda : ui.__mem_func__(self.__HideToolTip)()

			self.HTH_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowHTHToolTip)
			self.HTH_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideHTHToolTip)
			
			self.INT_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowINTToolTip)
			self.INT_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideINTToolTip)
			
			self.STR_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowSTRToolTip)
			self.STR_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideSTRToolTip)
			
			self.DEX_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowDEXToolTip)
			self.DEX_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideDEXToolTip)
			
			self.MSPD_IMG = self.GetChild("MSPD_IMG")
			self.ASPD_IMG = self.GetChild("ASPD_IMG")
			self.CSPD_IMG = self.GetChild("CSPD_IMG")
			self.MATT_IMG = self.GetChild("MATT_IMG")
			self.MDEF_IMG = self.GetChild("MDEF_IMG")
			#self.DEX_IMG = self.GetChild("ER_IMG")
			
			self.MSPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowMSPDToolTip)
			self.MSPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideMSPDToolTip)
			
			self.ASPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowASPDToolTip)
			self.ASPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideASPDToolTip)
			
			self.CSPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowCSPDToolTip)
			self.CSPD_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideCSPDToolTip)
			
			self.MATT_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowMATTToolTip)
			self.MATT_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideMATTToolTip)

			self.MDEF_IMG.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__ShowMDEFToolTip)
			self.MDEF_IMG.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__HideMDEFToolTip)
	
		global SHOW_ONLY_ACTIVE_SKILL
		global HIDE_SUPPORT_SKILL_POINT
		if SHOW_ONLY_ACTIVE_SKILL or HIDE_SUPPORT_SKILL_POINT:
			self.GetChild("Support_Skill_Point_Label").Hide()

		self.soloEmotionSlot = self.GetChild("SoloEmotionSlot")
		self.dualEmotionSlot = self.GetChild("DualEmotionSlot")
		self.__SetEmotionSlot()

		self.questShowingStartIndex = 0
		self.questScrollBar = self.GetChild("Quest_ScrollBar")
		self.questScrollBar.SetScrollEvent(ui.__mem_func__(self.OnQuestScroll))
		self.questSlot = self.GetChild("Quest_Slot")
		for i in xrange(quest.QUEST_MAX_NUM):
			self.questSlot.HideSlotBaseImage(i)
			self.questSlot.SetCoverButton(i,\
											"d:/ymir work/ui/game/quest/slot_button_01.sub",\
											"d:/ymir work/ui/game/quest/slot_button_02.sub",\
											"d:/ymir work/ui/game/quest/slot_button_03.sub",\
											"d:/ymir work/ui/game/quest/slot_button_03.sub", True)

		self.questNameList = []
		self.questLastTimeList = []
		self.questLastCountList = []
		for i in xrange(quest.QUEST_MAX_NUM):
			self.questNameList.append(self.GetChild("Quest_Name_0" + str(i)))
			self.questLastTimeList.append(self.GetChild("Quest_LastTime_0" + str(i)))
			self.questLastCountList.append(self.GetChild("Quest_LastCount_0" + str(i)))
		
		if app.ENABLE_NEW_DETAILS_GUI:
			MainBoard = self.GetChild("board")
			self.ExpandBtn = ui.MakeButton(MainBoard, 240, 120, "", "d:/ymir work/ui/game/belt_inventory/", "btn_minimize_normal.tga", "btn_minimize_over.tga", "btn_minimize_down.tga")
			self.ExpandBtn.SetEvent(ui.__mem_func__(self.__ClickExpandButton))
			self.MinimizeBtn = ui.MakeButton(MainBoard, 240, 120, "", "d:/ymir work/ui/game/belt_inventory/", "btn_expand_normal.tga", "btn_expand_over.tga", "btn_expand_down.tga")
			self.MinimizeBtn.SetEvent(ui.__mem_func__(self.__ClickMinimizeButton))

	if app.ENABLE_NEW_DETAILS_GUI:
		def __InitCharacterDetailsUIButton(self):
			self.ExpandBtn.Show()
			self.MinimizeBtn.Hide()
		def __ClickExpandButton(self):
			if not self.chDetailsWnd:
				self.chDetailsWnd = uiCharacterDetails.CharacterDetailsUI()
			self.chDetailsWnd.Show()
			self.SetTop()
			self.ExpandBtn.Hide()
			self.MinimizeBtn.Show()
		def __ClickMinimizeButton(self):
			self.chDetailsWnd.Hide()
			self.MinimizeBtn.Hide()
			self.ExpandBtn.Show()
		def OnMoveWindow(self, x, y):
			if self.chDetailsWnd:
				self.chDetailsWnd.AdjustPosition(x, y)

	def __SetSkillSlotEvent(self):
		for skillPageValue in self.skillPageDict.itervalues():
			skillPageValue.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			skillPageValue.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectSkill))
			skillPageValue.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			skillPageValue.SetUnselectItemSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetUseSlotEvent(ui.__mem_func__(self.ClickSkillSlot))
			skillPageValue.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			skillPageValue.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			skillPageValue.SetPressedSlotButtonEvent(ui.__mem_func__(self.OnPressedSlotButton))
			skillPageValue.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_down.sub")

	def __SetEmotionSlot(self):

		self.emotionToolTip = uiToolTip.ToolTip()

		for slot in (self.soloEmotionSlot, self.dualEmotionSlot):
			slot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			slot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectEmotion))
			slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
			slot.SetUseSlotEvent(ui.__mem_func__(self.__ClickEmotionSlot))
			slot.SetOverInItemEvent(ui.__mem_func__(self.__OverInEmotion))
			slot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutEmotion))
			slot.AppendSlotButton("d:/ymir work/ui/game/windows/btn_plus_up.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_over.sub",\
											"d:/ymir work/ui/game/windows/btn_plus_down.sub")

		for slotIdx, datadict in emotion.EMOTION_DICT.items():
			emotionIdx = slotIdx

			slot = self.soloEmotionSlot
			if slotIdx > 50:
				slot = self.dualEmotionSlot

			slot.SetEmotionSlot(slotIdx, emotionIdx)
			slot.SetCoverButton(slotIdx)

	def __SelectEmotion(self, slotIndex):
		if not slotIndex in emotion.EMOTION_DICT:
			return

		if app.IsPressed(app.DIK_LCONTROL):
			player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_EMOTION, slotIndex)
			return

		mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_EMOTION, slotIndex, slotIndex)

	def __ClickEmotionSlot(self, slotIndex):
		print "click emotion"
		if not slotIndex in emotion.EMOTION_DICT:
			return

		print "check acting"
		if player.IsActingEmotion():
			return

		command = emotion.EMOTION_DICT[slotIndex]["command"]
		print "command", command

		if slotIndex > 50:
			vid = player.GetTargetVID()

			if 0 == vid or vid == player.GetMainCharacterIndex() or chr.IsNPC(vid) or chr.IsEnemy(vid):
				import chat
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EMOTION_CHOOSE_ONE)
				return

			command += " " + chr.GetNameByVID(vid)

		print "send_command", command
		net.SendChatPacket(command)

	def ActEmotion(self, emotionIndex):
		self.__ClickEmotionSlot(emotionIndex)

	def __OverInEmotion(self, slotIndex):
		if self.emotionToolTip:

			if not slotIndex in emotion.EMOTION_DICT:
				return

			self.emotionToolTip.ClearToolTip()
			self.emotionToolTip.SetTitle(emotion.EMOTION_DICT[slotIndex]["name"])
			self.emotionToolTip.AlignHorizonalCenter()
			self.emotionToolTip.ShowToolTip()

	def __OverOutEmotion(self):
		if self.emotionToolTip:
			self.emotionToolTip.HideToolTip()

	def __BindEvent(self):
		for i in xrange(len(self.skillGroupButton)):
			self.skillGroupButton[i].SetEvent(lambda arg=i: self.__SelectSkillGroup(arg))

		self.RefreshQuest()
		self.__HideJobToolTip()

		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)

		if app.ENABLE_CONQUEROR_LEVEL:
			for (tabKey, tabButton) in self.tabSungmaButtonDict.items():
				tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabSungmaButton), tabKey)
	
			for (statusPlusKey, statusPlusButton) in self.statusConquerorPlusButtonDict.items():
				statusPlusButton.SAFE_SetEvent(self.__OnClickConquerorStatusPlusButton, statusPlusKey)
				statusPlusButton.ShowToolTip = lambda arg=statusPlusKey: self.__OverInStatButton(arg)
				statusPlusButton.HideToolTip = lambda arg=statusPlusKey: self.__OverOutStatButton()	
			
		for (statusPlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.SAFE_SetEvent(self.__OnClickStatusPlusButton, statusPlusKey)
			statusPlusButton.ShowToolTip = lambda arg=statusPlusKey: self.__OverInStatButton(arg)
			statusPlusButton.HideToolTip = lambda arg=statusPlusKey: self.__OverOutStatButton()

		for (statusMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.SAFE_SetEvent(self.__OnClickStatusMinusButton, statusMinusKey)
			statusMinusButton.ShowToolTip = lambda arg=statusMinusKey: self.__OverInStatMinusButton(arg)
			statusMinusButton.HideToolTip = lambda arg=statusMinusKey: self.__OverOutStatMinusButton()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.SetCloseEvent(ui.__mem_func__(self.Close))

		self.questSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectQuest))
		self.questSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__SelectQuest))

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			if localeInfo.IsARABIC() or localeInfo.IsVIETNAM() or localeInfo.IsJAPAN():
				self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "CharacterWindow.py")
			else:
				self.__LoadScript("UIScript/CharacterWindow.py")

			self.__BindObject()
			self.__BindEvent()
		except:
			import exception
			exception.Abort("CharacterWindow.__LoadWindow")

		#self.tabButtonDict["EMOTICON"].Disable()
		self.SetState("STATUS")

		if app.ENABLE_CONQUEROR_LEVEL:
			self.SetSubState("BASE")

	def Destroy(self):
		self.ClearDictionary()
		
		if app.ENABLE_NEW_DETAILS_GUI:
			if self.chDetailsWnd:
				self.chDetailsWnd.Destroy()
				self.chDetailsWnd=None

		self.__Initialize()


	def Close(self):
		if None != self.toolTipSkill:
			self.toolTipSkill.Hide()
		
		if app.ENABLE_NEW_DETAILS_GUI:
			if self.chDetailsWnd:
				self.isOpenedDetailsWnd = self.chDetailsWnd.IsShow()
				self.chDetailsWnd.Close()

		self.Hide()

	def SetSkillToolTip(self, toolTipSkill):
		self.toolTipSkill = toolTipSkill

	if app.ENABLE_CONQUEROR_LEVEL:
		def __OnClickConquerorStatusPlusButton(self, statusKey):
			try:
				statusConquerorPlusCommand=self.statusConquerorPlusCommandDict[statusKey]
				net.SendChatPacket(statusConquerorPlusCommand)
			except KeyError, msg:
				dbg.TraceError("CharacterWindow.__OnClickStatusPlusButton KeyError: %s", msg)

	def __OnClickStatusPlusButton(self, statusKey):
		cmd = self.statusPlusCommandDict[statusKey]

		if app.IsPressed(app.DIK_LCONTROL):
			cmd = cmd + "10"
		else:
			cmd = cmd + "1"
			
		net.SendChatPacket(cmd)

	def __OnClickStatusMinusButton(self, statusKey):
		try:
			statusMinusCommand=self.statusMinusCommandDict[statusKey]
			if app.DISABLE_OLD_MINUS:
				if app.IsPressed(app.DIK_LCONTROL):
					statusMinusCommand += " 10"
				else:
					statusMinusCommand += " 1"
				
			net.SendChatPacket(statusMinusCommand)
		except KeyError, msg:
			dbg.TraceError("CharacterWindow.__OnClickStatusMinusButton KeyError: %s", msg)


	def __OnClickTabButton(self, stateKey):
		self.SetState(stateKey)

	if app.ENABLE_CONQUEROR_LEVEL:
		def __OnClickTabSungmaButton(self, stateKey):
			self.SetSubState(stateKey)

	def SetState(self, stateKey):

		self.state = stateKey

		for (tabKey, tabButton) in self.tabButtonDict.items():
			if stateKey!=tabKey:
				tabButton.SetUp()

		for tabValue in self.tabDict.itervalues():
			tabValue.Hide()

		for pageValue in self.pageDict.itervalues():
			pageValue.Hide()

		for titleBarValue in self.titleBarDict.itervalues():
			titleBarValue.Hide()

		self.titleBarDict[stateKey].Show()
		self.tabDict[stateKey].Show()
		self.pageDict[stateKey].Show()


	def GetState(self):
		return self.state

	if app.ENABLE_CONQUEROR_LEVEL:
		def SetSubState(self, stateSubKey):
			
			self.substate = stateSubKey

			for (tabKey, tabButton) in self.tabSungmaButtonDict.items():
				if stateSubKey!=tabKey:
					tabButton.SetUp()

			for pageValue in self.SungmaPageDict.itervalues():
				pageValue.Hide()

			self.__RefreshStatusPlusButtonList()
			self.SungmaPageDict[stateSubKey].Show()
			

		def GetSubState(self):
			return self.substate	

	def __GetTotalAtkText(self):
		minAtk=player.GetStatus(player.ATT_MIN)
		maxAtk=player.GetStatus(player.ATT_MAX)
		atkBonus=player.GetStatus(player.ATT_BONUS)
		attackerBonus=player.GetStatus(player.ATTACKER_BONUS)

		if app.ELEMENT_SPELL_WORLDARD:
			atkBonusElements=player.GetStatus(player.ATT_ELEMENTS)

		if minAtk==maxAtk:
			if app.ELEMENT_SPELL_WORLDARD:
				return "%d" % (minAtk+atkBonus+attackerBonus+atkBonusElements)
			else:
				return "%d" % (minAtk+atkBonus+attackerBonus)
		else:
			if app.ELEMENT_SPELL_WORLDARD:
				return "%d-%d" % (minAtk+atkBonus+attackerBonus+atkBonusElements, maxAtk+atkBonus+attackerBonus+atkBonusElements)
			else:
				return "%d-%d" % (minAtk+atkBonus+attackerBonus, maxAtk+atkBonus+attackerBonus)

	def __GetTotalMagAtkText(self):
		minMagAtk=player.GetStatus(player.MAG_ATT)+player.GetStatus(player.MIN_MAGIC_WEP)
		maxMagAtk=player.GetStatus(player.MAG_ATT)+player.GetStatus(player.MAX_MAGIC_WEP)

		if minMagAtk==maxMagAtk:
			return "%d" % (minMagAtk)
		else:
			return "%d-%d" % (minMagAtk, maxMagAtk)

	def __GetTotalDefText(self):
		defValue=player.GetStatus(player.DEF_GRADE)
		if constInfo.ADD_DEF_BONUS_ENABLE:
			defValue+=player.GetStatus(player.DEF_BONUS)
		return "%d" % (defValue)

	def RefreshStatus(self):
		if self.isLoaded==0:
			return

		try:
			if app.ENABLE_CONQUEROR_LEVEL:
				if player.GetStatus(player.CONQUEROR_LEVEL) >= 1:
					self.GetChild("Level_Value").SetText(str(player.GetStatus(player.CONQUEROR_LEVEL)))
					self.GetChild("Exp_Value").SetText(str(unsigned32(player.GetConquerorEXP())))
					self.GetChild("RestExp_Value").SetText(str(unsigned32(player.GetStatus(player.CONQUEROR_NEXT_EXP)) - unsigned32(player.GetStatus(player.CONQUEROR_EXP))))
				else:
					self.GetChild("Level_Value").SetText(str(player.GetStatus(player.LEVEL)))
					self.GetChild("Exp_Value").SetText(str(unsigned32(player.GetEXP())))
					self.GetChild("RestExp_Value").SetText(str(unsigned32(player.GetStatus(player.NEXT_EXP)) - unsigned32(player.GetStatus(player.EXP))))
			else:
				self.GetChild("Level_Value").SetText(str(player.GetStatus(player.LEVEL)))
				self.GetChild("Exp_Value").SetText(str(unsigned32(player.GetEXP())))
				self.GetChild("RestExp_Value").SetText(str(unsigned32(player.GetStatus(player.NEXT_EXP)) - unsigned32(player.GetStatus(player.EXP))))

			self.GetChild("HP_Value").SetText(str(player.GetStatus(player.HP)) + '/' + str(player.GetStatus(player.MAX_HP)))
			self.GetChild("SP_Value").SetText(str(player.GetStatus(player.SP)) + '/' + str(player.GetStatus(player.MAX_SP)))

			self.GetChild("STR_Value").SetText(str(player.GetStatus(player.ST)))
			self.GetChild("DEX_Value").SetText(str(player.GetStatus(player.DX)))
			self.GetChild("HTH_Value").SetText(str(player.GetStatus(player.HT)))
			self.GetChild("INT_Value").SetText(str(player.GetStatus(player.IQ)))

			self.GetChild("ATT_Value").SetText(self.__GetTotalAtkText())
			self.GetChild("DEF_Value").SetText(self.__GetTotalDefText())

			self.GetChild("MATT_Value").SetText(self.__GetTotalMagAtkText())
			#self.GetChild("MATT_Value").SetText(str(player.GetStatus(player.MAG_ATT)))

			self.GetChild("MDEF_Value").SetText(str(player.GetStatus(player.MAG_DEF)))
			self.GetChild("ASPD_Value").SetText(str(player.GetStatus(player.ATT_SPEED)))
			self.GetChild("MSPD_Value").SetText(str(player.GetStatus(player.MOVING_SPEED)))
			self.GetChild("CSPD_Value").SetText(str(player.GetStatus(player.CASTING_SPEED)))
			self.GetChild("ER_Value").SetText(str(player.GetStatus(player.EVADE_RATE)))

			if app.ENABLE_CONQUEROR_LEVEL:
				self.GetChild("sungma_str_value").SetText(str(player.GetStatus(player.SUNGMA_STR)))
				self.GetChild("sungma_hp_value").SetText(str(player.GetStatus(player.SUNGMA_HP)))
				self.GetChild("sungma_move_value").SetText(str(player.GetStatus(player.SUNGMA_MOVE)))
				self.GetChild("sungma_immune_value").SetText(str(player.GetStatus(player.SUNGMA_INMUNE)))
		except:
			#import exception
			#exception.Abort("CharacterWindow.RefreshStatus.BindObject")
			## 게임이 튕겨 버림
			pass

		self.__RefreshStatusPlusButtonList()
		self.__RefreshStatusMinusButtonList()
		self.RefreshAlignment()

		if self.refreshToolTip:
			self.refreshToolTip()
		
		if app.ENABLE_NEW_DETAILS_GUI:
			if self.chDetailsWnd:
				if self.chDetailsWnd.IsShow():
					self.chDetailsWnd.Refresh()

	def __RefreshStatusPlusButtonList(self):
		if self.isLoaded==0:
			return

		if app.ENABLE_CONQUEROR_LEVEL:
			if self.GetSubState() == "SUNGMA":
				statusPlusPoint=player.GetStatus(player.CONQUEROR_POINT)
			else:
				statusPlusPoint=player.GetStatus(player.STAT)
		else:
			statusPlusPoint=player.GetStatus(player.STAT)

		if statusPlusPoint>0:
			self.statusPlusValue.SetText(str(statusPlusPoint))
			self.statusPlusLabel.Show()
			self.ShowStatusPlusButtonList()
		else:
			self.statusPlusValue.SetText(str(0))
			self.statusPlusLabel.Hide()
			self.HideStatusPlusButtonList()

	def __RefreshStatusMinusButtonList(self):
		if self.isLoaded==0:
			return

		if app.DISABLE_OLD_MINUS:
			self.__ShowStatusMinusButtonList()
		else:
			statusMinusPoint=self.__GetStatMinusPoint()
			if statusMinusPoint>0:
				self.__ShowStatusMinusButtonList()
			else:
				self.__HideStatusMinusButtonList()

		if app.ENABLE_CONQUEROR_LEVEL:
			statusConquerorMinusPoint=self.__GetStatConquerorMinusPoint()
			if statusConquerorMinusPoint>0:
				self.ShowConquerorStatusPlusButtonList()
			else:
				self.HideConquerorStatusPlusButtonList()

	def RefreshAlignment(self):
		point, grade = player.GetAlignmentData()

		import colorInfo
		COLOR_DICT = {	0 : colorInfo.TITLE_RGB_GOOD_4,
						1 : colorInfo.TITLE_RGB_GOOD_3,
						2 : colorInfo.TITLE_RGB_GOOD_2,
						3 : colorInfo.TITLE_RGB_GOOD_1,
						4 : colorInfo.TITLE_RGB_NORMAL,
						5 : colorInfo.TITLE_RGB_EVIL_1,
						6 : colorInfo.TITLE_RGB_EVIL_2,
						7 : colorInfo.TITLE_RGB_EVIL_3,
						8 : colorInfo.TITLE_RGB_EVIL_4, }
		colorList = COLOR_DICT.get(grade, colorInfo.TITLE_RGB_NORMAL)
		gradeColor = ui.GenerateColor(colorList[0], colorList[1], colorList[2])

		self.toolTipAlignment.ClearToolTip()
		self.toolTipAlignment.AutoAppendTextLine(localeInfo.TITLE_NAME_LIST[grade], gradeColor)
		self.toolTipAlignment.AutoAppendTextLine(localeInfo.ALIGNMENT_NAME + str(point))
		self.toolTipAlignment.AlignHorizonalCenter()

	def __ShowStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Show()

	def __HideStatusMinusButtonList(self):
		for (stateMinusKey, statusMinusButton) in self.statusMinusButtonDict.items():
			statusMinusButton.Hide()

	def ShowStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Show()

	def HideStatusPlusButtonList(self):
		for (statePlusKey, statusPlusButton) in self.statusPlusButtonDict.items():
			statusPlusButton.Hide()

	if app.ENABLE_CONQUEROR_LEVEL:
		def __GetStatConquerorMinusPoint(self):
			return player.GetStatus(player.CONQUEROR_POINT)

		def ShowConquerorStatusPlusButtonList(self):
			for (statePlusKey, statusPlusButton) in self.statusConquerorPlusButtonDict.items():
				statusPlusButton.Show()
				
		def HideConquerorStatusPlusButtonList(self):
			for (statePlusKey, statusPlusButton) in self.statusConquerorPlusButtonDict.items():
				statusPlusButton.Hide()

	def SelectSkill(self, skillSlotIndex):

		mouseController = mouseModule.mouseController

		if False == mouseController.isAttached():

			srcSlotIndex = self.__RealSkillSlotToSourceSlot(skillSlotIndex)
			selectedSkillIndex = player.GetSkillIndex(srcSlotIndex)

			if skill.CanUseSkill(selectedSkillIndex):

				if app.IsPressed(app.DIK_LCONTROL):

					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_SKILL, srcSlotIndex)
					return

				mouseController.AttachObject(self, player.SLOT_TYPE_SKILL, srcSlotIndex, selectedSkillIndex)

		else:

			mouseController.DeattachObject()

	def SelectEmptySlot(self, SlotIndex):
		mouseModule.mouseController.DeattachObject()

	if app.ENABLE_CONQUEROR_LEVEL:
		def __ShowToolTip(self, desc):
			if not self.toolTip:
				return

			descLen = len(desc)
			self.toolTip.ClearToolTip()
			self.toolTip.SetThinBoardSize(11 * descLen)
			self.toolTip.AppendTextLine(desc)
			self.toolTip.AlignHorizonalCenter()
			self.toolTip.Show()

		def __HideToolTip(self):
			self.__HideStatToolTip()

		def __ShowToolTipButton(self, desc):
			self.__ShowToolTip(desc)

		def __ShowToolTipImg(self, event_type, text):
			if "mouse_over_in" == event_type :
				textLen = len(text)

				self.toolTip.ClearToolTip()
				self.toolTip.SetThinBoardSize(11 * arglen)
				self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
				self.toolTip.AppendTextLine(text, 0xffffffff)
				self.toolTip.AlignHorizonalCenter()
				self.toolTip.Show()
			elif "mouse_over_out" == event_type:
				self.__HideToolTip()

		def __TogglePassiveAttrWindow(self, event_type): pass
		def __ToolTipProgress(self): pass

	## ToolTip
	def OverInItem(self, slotNumber):

		if mouseModule.mouseController.isAttached():
			return

		if 0 == self.toolTipSkill:
			return

		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		skillLevel = player.GetSkillLevel(srcSlotIndex)
		skillGrade = player.GetSkillGrade(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			overInSkillGrade = self.__GetSkillGradeFromSlot(slotNumber)

			if overInSkillGrade == skill.SKILL_GRADE_COUNT-1 and skillGrade == skill.SKILL_GRADE_COUNT:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)
			elif overInSkillGrade == skillGrade:
				self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, overInSkillGrade, skillLevel)
			else:
				self.toolTipSkill.SetSkillOnlyName(srcSlotIndex, skillIndex, overInSkillGrade)

		else:
			self.toolTipSkill.SetSkillNew(srcSlotIndex, skillIndex, skillGrade, skillLevel)

	def OverOutItem(self):
		if 0 != self.toolTipSkill:
			self.toolTipSkill.HideToolTip()

	## Quest
	def __SelectQuest(self, slotIndex):
		# import dbg
		# dbg.TraceError("i am wroking")
		questIndex = quest.GetQuestIndex(self.questShowingStartIndex+slotIndex)

		import event
		event.QuestButtonClick(-2147483648 + questIndex)

	def RefreshQuest(self):

		if self.isLoaded==0:
			return

		questCount = quest.GetQuestCount()
		questRange = range(quest.QUEST_MAX_NUM)

		if questCount > quest.QUEST_MAX_NUM:
			self.questScrollBar.Show()
		else:
			self.questScrollBar.Hide()

		for i in questRange[:questCount]:
			(questName, questIcon, questCounterName, questCounterValue) = quest.GetQuestData(self.questShowingStartIndex+i)
			self.questNameList[i].SetText(questName)
			self.questNameList[i].Show()
			self.questLastCountList[i].Show()
			self.questLastTimeList[i].Show()

			if len(questCounterName) > 0:
				self.questLastCountList[i].SetText("%s : %d" % (questCounterName, questCounterValue))
			else:
				self.questLastCountList[i].SetText("")

			## Icon
			self.questSlot.SetSlot(i, i, 1, 1, questIcon)

		for i in questRange[questCount:]:
			self.questNameList[i].Hide()
			self.questLastTimeList[i].Hide()
			self.questLastCountList[i].Hide()
			self.questSlot.ClearSlot(i)
			self.questSlot.HideSlotBaseImage(i)

		self.__UpdateQuestClock()

	def __UpdateQuestClock(self):
		if "QUEST" == self.state:
			# QUEST_LIMIT_COUNT_BUG_FIX
			for i in xrange(min(quest.GetQuestCount(), quest.QUEST_MAX_NUM)):
			# END_OF_QUEST_LIMIT_COUNT_BUG_FIX
				(lastName, lastTime) = quest.GetQuestLastTime(i)

				clockText = localeInfo.QUEST_UNLIMITED_TIME
				if len(lastName) > 0:

					if lastTime <= 0:
						clockText = localeInfo.QUEST_TIMEOVER

					else:
						questLastMinute = lastTime / 60
						questLastSecond = lastTime % 60

						clockText = lastName + " : "

						if questLastMinute > 0:
							clockText += str(questLastMinute) + localeInfo.QUEST_MIN
							if questLastSecond > 0:
								clockText += " "

						if questLastSecond > 0:
							clockText += str(questLastSecond) + localeInfo.QUEST_SEC

				self.questLastTimeList[i].SetText(clockText)

	def __GetStatMinusPoint(self):
		POINT_STAT_RESET_COUNT = 112
		return player.GetStatus(POINT_STAT_RESET_COUNT)

	def __OverInStatMinusButton(self, stat):
		try:
			if app.DISABLE_OLD_MINUS:
				self.__ShowStatToolTip(self.STAT_MINUS_DESCRIPTION[stat], localeInfo.EMOJI_CHARACTER_STATS_DELETE, True)
			else:
				self.__ShowStatToolTip(self.STAT_MINUS_DESCRIPTION[stat] % self.__GetStatMinusPoint())
		except KeyError:
			pass

		self.refreshToolTip = lambda arg=stat: self.__OverInStatMinusButton(arg)

	def __OverOutStatMinusButton(self):
		self.__HideStatToolTip()
		self.refreshToolTip = 0

	def __OverInStatButton(self, stat):	
		try:
			if app.ENABLE_CONQUEROR_LEVEL:
				if self.GetSubState() == "SUNGMA":
					self.__ShowStatToolTip(self.STAT_SUNGMA_DESCRIPTION[stat], localeInfo.EMOJI_CHARACTER_STATS_ADD, False)
				else:
					self.__ShowStatToolTip(self.STAT_DESCRIPTION[stat], localeInfo.EMOJI_CHARACTER_STATS_ADD, True)			
			else:
				self.__ShowStatToolTip(self.STAT_DESCRIPTION[stat], localeInfo.EMOJI_CHARACTER_STATS_ADD, True)

		except KeyError:
			pass

	def __OverOutStatButton(self):
		self.__HideStatToolTip()

	def __ShowStatToolTip(self, statDesc, statDesc2 = False, arg2 = False):
		self.toolTip.ClearToolTip()
		self.toolTip.AutoAppendTextLine(statDesc)
		self.toolTip.AppendSpace(5)
		self.toolTip.AlignHorizonalCenter()
		if arg2 == True:
			self.toolTip.AppendTextLine(statDesc2)
			self.toolTip.AppendSpace(5)
			self.toolTip.AlignHorizonalCenter()
		self.toolTip.Show()
			

	def __HideStatToolTip(self):
		self.toolTip.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnUpdate(self):
		self.__UpdateQuestClock()

	## @John, actualizacion de skill tiempo en monturas 
	## Skill Process
	def __RefreshSkillPage(self, name, slotCount):
		global SHOW_LIMIT_SUPPORT_SKILL_LIST

		skillPage = self.skillPageDict[name]

		startSlotIndex = skillPage.GetStartIndex()
		if "ACTIVE" == name:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				startSlotIndex += slotCount

		getSkillType = skill.GetSkillType
		getSkillIndex = player.GetSkillIndex
		getSkillGrade = player.GetSkillGrade
		getSkillLevel = player.GetSkillLevel
		getSkillLevelUpPoint = skill.GetSkillLevelUpPoint
		getSkillMaxLevel = skill.GetSkillMaxLevel

		for i in xrange(slotCount + 1):
			slotIndex = i + startSlotIndex
			skillIndex = getSkillIndex(slotIndex)

			for j in xrange(skill.SKILL_GRADE_COUNT):
				skillPage.ClearSlot(self.__GetRealSkillSlot(j, i))

			if 0 == skillIndex:
				continue

			skillGrade = getSkillGrade(slotIndex)
			skillLevel = getSkillLevel(slotIndex)
			skillType = getSkillType(skillIndex)

			## 승마 스킬 예외 처리
			if player.SKILL_INDEX_RIDING == skillIndex:
				if skillGrade == 1:
					skillLevel += 19
				elif skillGrade == 2:
					skillLevel += 29
				elif skillGrade == 3:
					skillLevel = 40

				skillPage.SetSkillSlotNew(slotIndex, skillIndex, max(skillLevel - 1, 0), skillLevel)
				skillPage.SetSlotCount(slotIndex, skillLevel)

			## ACTIVE
			elif skill.SKILL_TYPE_ACTIVE == skillType:
				for j in xrange(skill.SKILL_GRADE_COUNT):
					realSlotIndex = self.__GetRealSkillSlot(j, slotIndex)
					skillPage.SetSkillSlotNew(realSlotIndex, skillIndex, j, skillLevel)
					skillPage.SetCoverButton(realSlotIndex)

					if (skillGrade == skill.SKILL_GRADE_COUNT) and j == (skill.SKILL_GRADE_COUNT-1):
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)
					elif (not self.__CanUseSkillNow()) or (skillGrade != j):
						skillPage.SetSlotCount(realSlotIndex, 0)
						skillPage.DisableCoverButton(realSlotIndex)
						skillPage.DeactivateSlot(realSlotIndex) # hotfix
					else:
						skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

					if player.IsSkillActive(slotIndex) and (skillGrade == j): # hotfix
						skillPage.ActivateSlot(realSlotIndex)
			## 그외
			else:
				if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
					realSlotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)
					skillPage.SetSkillSlot(realSlotIndex, skillIndex, skillLevel)
					skillPage.SetSlotCountNew(realSlotIndex, skillGrade, skillLevel)

					if skill.CanUseSkill(skillIndex):
						skillPage.SetCoverButton(realSlotIndex)

					if player.IsSkillActive(slotIndex): # hotfix
						skillPage.ActivateSlot(realSlotIndex)
					else:
						skillPage.DeactivateSlot(realSlotIndex)

			skillPage.RefreshSlot()

		## 쿨 타임 복원
		self.__RestoreSlotCoolTime(skillPage)

	def __RestoreSlotCoolTime(self, skillPage):
		restoreType = skill.SKILL_TYPE_NONE
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			restoreType = skill.SKILL_TYPE_HORSE
		else:
			restoreType = skill.SKILL_TYPE_ACTIVE

		skillPage.RestoreSlotCoolTime(restoreType)

	def RefreshSkill(self):
		if self.isLoaded==0:
			return

		if self.__IsChangedHorseRidingSkillLevel():
			self.RefreshCharacter()
			return

		global SHOW_ONLY_ACTIVE_SKILL
		if SHOW_ONLY_ACTIVE_SKILL:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
		else:
			self.__RefreshSkillPage("ACTIVE", self.ACTIVE_PAGE_SLOT_COUNT)
			self.__RefreshSkillPage("SUPPORT", self.SUPPORT_PAGE_SLOT_COUNT)

		self.RefreshSkillPlusButtonList()

	def CanShowPlusButton(self, skillIndex, skillLevel, curStatPoint):
		## 스킬이 있으면
		if 0 == skillIndex:
			return False

		## 레벨업 조건을 만족한다면
		if not skill.CanLevelUpSkill(skillIndex, skillLevel):
			return False

		return True

	def __RefreshSkillPlusButton(self, name):
		global HIDE_SUPPORT_SKILL_POINT
		if HIDE_SUPPORT_SKILL_POINT and "SUPPORT" == name:
			return

		slotWindow = self.skillPageDict[name]
		slotWindow.HideAllSlotButton()

		slotStatType = self.skillPageStatDict[name]
		if 0 == slotStatType:
			return

		statPoint = player.GetStatus(slotStatType)
		startSlotIndex = slotWindow.GetStartIndex()
		if "HORSE" == name:
			startSlotIndex += self.ACTIVE_PAGE_SLOT_COUNT

		if statPoint > 0:
			for i in xrange(self.PAGE_SLOT_COUNT):
				slotIndex = i + startSlotIndex
				skillIndex = player.GetSkillIndex(slotIndex)
				skillGrade = player.GetSkillGrade(slotIndex)
				skillLevel = player.GetSkillLevel(slotIndex)

				if skillIndex == 0:
					continue
				if skillGrade != 0:
					continue

				if name == "HORSE":
					if player.GetStatus(player.LEVEL) >= skill.GetSkillLevelLimit(skillIndex):
						if skillLevel < 20:
							slotWindow.ShowSlotButton(self.__GetETCSkillRealSlotIndex(slotIndex))
				else:
					if "SUPPORT" == name:
						if not SHOW_LIMIT_SUPPORT_SKILL_LIST or skillIndex in SHOW_LIMIT_SUPPORT_SKILL_LIST:
							if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
								slotWindow.ShowSlotButton(slotIndex)
					else:
						if self.CanShowPlusButton(skillIndex, skillLevel, statPoint):
							slotWindow.ShowSlotButton(slotIndex)

	def RefreshSkillPlusButtonList(self):
		if self.isLoaded==0:
			return

		self.RefreshSkillPlusPointLabel()

		if not self.__CanUseSkillNow():
			return

		try:
			if self.PAGE_HORSE == self.curSelectedSkillGroup:
				self.__RefreshSkillPlusButton("HORSE")
			else:
				self.__RefreshSkillPlusButton("ACTIVE")

			self.__RefreshSkillPlusButton("SUPPORT")

		except:
			import exception
			exception.Abort("CharacterWindow.RefreshSkillPlusButtonList.BindObject")

	def RefreshSkillPlusPointLabel(self):
		if self.isLoaded==0:
			return

		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			activeStatPoint = player.GetStatus(player.SKILL_HORSE)
			self.activeSkillPointValue.SetText(str(activeStatPoint))

		else:
			activeStatPoint = player.GetStatus(player.SKILL_ACTIVE)
			self.activeSkillPointValue.SetText(str(activeStatPoint))

		supportStatPoint = max(0, player.GetStatus(player.SKILL_SUPPORT))
		self.supportSkillPointValue.SetText(str(supportStatPoint))

	## Skill Level Up Button
	def OnPressedSlotButton(self, slotNumber):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotNumber)

		skillIndex = player.GetSkillIndex(srcSlotIndex)
		curLevel = player.GetSkillLevel(srcSlotIndex)
		maxLevel = skill.GetSkillMaxLevel(skillIndex)

		net.SendChatPacket("/skillup " + str(skillIndex))

	## Use Skill
	def ClickSkillSlot(self, slotIndex):
		srcSlotIndex = self.__RealSkillSlotToSourceSlot(slotIndex)
		skillIndex = player.GetSkillIndex(srcSlotIndex)
		skillType = skill.GetSkillType(skillIndex)

		if not self.__CanUseSkillNow():
			if skill.SKILL_TYPE_ACTIVE == skillType:
				return

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				if skill.CanUseSkill(skillIndex):
					player.ClickSkillSlot(srcSlotIndex)
					return

		mouseModule.mouseController.DeattachObject()

	## FIXME : 스킬을 사용했을때 슬롯 번호를 가지고 해당 슬롯을 찾아서 업데이트 한다.
	## 매우 불합리. 구조 자체를 개선해야 할듯.
	def OnUseSkill(self, slotIndex, coolTime):
		skillIndex = player.GetSkillIndex(slotIndex)
		skillType = skill.GetSkillType(skillIndex)

		## ACTIVE
		if skill.SKILL_TYPE_ACTIVE == skillType:
			skillGrade = player.GetSkillGrade(slotIndex)
			slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)
		## ETC
		else:
			slotIndex = self.__GetETCSkillRealSlotIndex(slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.StoreSlotCoolTime(skillType, slotIndex, coolTime)
				self.__RestoreSlotCoolTime(slotWindow)
				#slotWindow.SetSlotCoolTime(slotIndex, coolTime)
				return

	def OnActivateSkill(self, slotIndex):
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.ActivateSlot(slotIndex)
				return

		self.RefreshSkill()

	def OnDeactivateSkill(self, slotIndex):
		skillGrade = player.GetSkillGrade(slotIndex)
		slotIndex = self.__GetRealSkillSlot(skillGrade, slotIndex)

		for slotWindow in self.skillPageDict.values():
			if slotWindow.HasSlot(slotIndex):
				slotWindow.DeactivateSlot(slotIndex)
				return

		self.RefreshSkill()

	def __ShowJobToolTip(self):
		self.toolTipJob.ShowToolTip()

	def __HideJobToolTip(self):
		self.toolTipJob.HideToolTip()
	## @John, end actualizacion de skill tiempo en monturas 

	def __SetJobText(self, mainJob, subJob):
		if player.GetStatus(player.LEVEL)<5:
			subJob=0

		if 949 == app.GetDefaultCodePage():
			self.toolTipJob.ClearToolTip()

			try:
				jobInfoTitle=localeInfo.JOBINFO_TITLE[mainJob][subJob]
				jobInfoData=localeInfo.JOBINFO_DATA_LIST[mainJob][subJob]
			except IndexError:
				print "uiCharacter.CharacterWindow.__SetJobText(mainJob=%d, subJob=%d)" % (mainJob, subJob)
				return

			self.toolTipJob.AutoAppendTextLine(jobInfoTitle)
			self.toolTipJob.AppendSpace(5)

			for jobInfoDataLine in jobInfoData:
				self.toolTipJob.AutoAppendTextLine(jobInfoDataLine)

			self.toolTipJob.AlignHorizonalCenter()

	def __ShowAlignmentToolTip(self):
		self.toolTipAlignment.ShowToolTip()

	def __HideAlignmentToolTip(self):
		self.toolTipAlignment.HideToolTip()

	if app.ENABLE_CONQUEROR_LEVEL:
		def __ShowHTHToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_CON)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideHTHToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()

		def __ShowINTToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_INT)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideINTToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()

		def __ShowSTRToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_STR)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideSTRToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()
			
		def __ShowDEXToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_IMG_DEX)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideDEXToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()

		###############################################################################
		def __ShowBaseToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_BASE_LEVEL)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideBaseToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()
		###
		def __ShowSungmaToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_CONQUEROR_LEVEL)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideSungmaToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()			
		
		###
		
		def __ShowMSPDToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_MOVE_SPEED)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideMSPDToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()
		####
		def __ShowASPDToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_ATT_SPEED)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideASPDToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()
		###	
		def __ShowCSPDToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_CAST_SPEED)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideCSPDToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()
			
		###	
		def __ShowMATTToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_MAG_ATT)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideMATTToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()
			
		###	
		def __ShowMDEFToolTip(self):
			self.toolTipConquerorInfoButton.ClearToolTip()
			self.toolTipConquerorInfoButton.AutoAppendTextLine(localeInfo.STAT_TOOLTIP_MAG_DEF)
			self.toolTipConquerorInfoButton.AlignHorizonalCenter()
			
			self.toolTipConquerorInfoButton.ShowToolTip()

		def __HideMDEFToolTip(self):
			self.toolTipConquerorInfoButton.HideToolTip()
		##############################################################################################	
	def RefreshCharacter(self):

		if self.isLoaded==0:
			return

		## Name
		try:
			characterName = player.GetName()
			guildName = player.GetGuildName()
			self.characterNameValue.SetText(characterName)
			self.guildNameValue.SetText(guildName)
			if not guildName:
				if localeInfo.IsARABIC():
					self.characterNameSlot.SetPosition(190, 34)
				else:
					self.characterNameSlot.SetPosition(109, 34)

				self.guildNameSlot.Hide()
			else:
				if localeInfo.IsJAPAN():
					self.characterNameSlot.SetPosition(143, 34)
				else:
					self.characterNameSlot.SetPosition(153, 34)
				self.guildNameSlot.Show()
		except:
			import exception
			exception.Abort("CharacterWindow.RefreshCharacter.BindObject")

		race = net.GetMainActorRace()
		group = net.GetMainActorSkillGroup()
		empire = net.GetMainActorEmpire()

		## Job Text
		job = chr.RaceToJob(race)
		self.__SetJobText(job, group)

		## FaceImage
		try:
			faceImageName = FACE_IMAGE_DICT[race]

			try:
				self.faceImage.LoadImage(faceImageName)
			except:
				print "CharacterWindow.RefreshCharacter(race=%d, faceImageName=%s)" % (race, faceImageName)
				self.faceImage.Hide()

		except KeyError:
			self.faceImage.Hide()

		## GroupName
		self.__SetSkillGroupName(race, group)

		## Skill
		if 0 == group:
			self.__SelectSkillGroup(0)

		else:
			self.__SetSkillSlotData(race, group, empire)

			if self.__CanUseHorseSkill():
				self.__SelectSkillGroup(0)

	def __SetSkillGroupName(self, race, group):

		job = chr.RaceToJob(race)

		if not self.SKILL_GROUP_NAME_DICT.has_key(job):
			return

		nameList = self.SKILL_GROUP_NAME_DICT[job]

		if 0 == group:
			self.skillGroupButton1.SetText(nameList[1])
			self.skillGroupButton2.SetText(nameList[2])
			self.skillGroupButton1.Show()
			self.skillGroupButton2.Show()
			self.activeSkillGroupName.Hide()

		else:

			if self.__CanUseHorseSkill():
				self.activeSkillGroupName.Hide()
				self.skillGroupButton1.SetText(nameList.get(group, "Noname"))
				self.skillGroupButton2.SetText(localeInfo.SKILL_GROUP_HORSE)
				self.skillGroupButton1.Show()
				self.skillGroupButton2.Show()

			else:
				self.activeSkillGroupName.SetText(nameList.get(group, "Noname"))
				self.activeSkillGroupName.Show()
				self.skillGroupButton1.Hide()
				self.skillGroupButton2.Hide()

	def __SetSkillSlotData(self, race, group, empire=0):

		## SkillIndex
		playerLoad.RegisterSkill(race, group, empire)

		## Event
		self.__SetSkillSlotEvent()

		## Refresh
		self.RefreshSkill()

	def __SelectSkillGroup(self, index):
		for btn in self.skillGroupButton:
			btn.SetUp()
		self.skillGroupButton[index].Down()

		if self.__CanUseHorseSkill():
			if 0 == index:
				index = net.GetMainActorSkillGroup()-1
			elif 1 == index:
				index = self.PAGE_HORSE

		self.curSelectedSkillGroup = index
		self.__SetSkillSlotData(net.GetMainActorRace(), index+1, net.GetMainActorEmpire())

	def __CanUseSkillNow(self):
		if 0 == net.GetMainActorSkillGroup():
			return False

		return True

	def __CanUseHorseSkill(self):

		slotIndex = player.GetSkillSlotIndex(player.SKILL_INDEX_RIDING)

		if not slotIndex:
			return False

		grade = player.GetSkillGrade(slotIndex)
		level = player.GetSkillLevel(slotIndex)
		if level < 0:
			level *= -1
		if grade >= 1 and level >= 1:
			return True

		return False

	def __IsChangedHorseRidingSkillLevel(self):
		ret = False

		if -1 == self.canUseHorseSkill:
			self.canUseHorseSkill = self.__CanUseHorseSkill()

		if self.canUseHorseSkill != self.__CanUseHorseSkill():
			ret = True

		self.canUseHorseSkill = self.__CanUseHorseSkill()
		return ret

	def __GetRealSkillSlot(self, skillGrade, skillSlot):
		return skillSlot + min(skill.SKILL_GRADE_COUNT-1, skillGrade)*skill.SKILL_GRADE_STEP_COUNT

	def __GetETCSkillRealSlotIndex(self, skillSlot):
		if skillSlot > 100:
			return skillSlot
		return skillSlot % self.ACTIVE_PAGE_SLOT_COUNT

	def __RealSkillSlotToSourceSlot(self, realSkillSlot):
		if realSkillSlot > 100:
			return realSkillSlot
		if self.PAGE_HORSE == self.curSelectedSkillGroup:
			return realSkillSlot + self.ACTIVE_PAGE_SLOT_COUNT
		return realSkillSlot % skill.SKILL_GRADE_STEP_COUNT

	def __GetSkillGradeFromSlot(self, skillSlot):
		return int(skillSlot / skill.SKILL_GRADE_STEP_COUNT)

	def SelectSkillGroup(self, index):
		self.__SelectSkillGroup(index)

	def OnQuestScroll(self):
		questCount = quest.GetQuestCount()
		scrollLineCount = max(0, questCount - quest.QUEST_MAX_NUM)
		startIndex = int(scrollLineCount * self.questScrollBar.GetPos())

		if startIndex != self.questShowingStartIndex:
			self.questShowingStartIndex = startIndex
			self.RefreshQuest()
