import dbg
import player
import item
import grp
import wndMgr
import skill
import shop
import exchange
import grpText
import safebox
import localeInfo
import app
import background
import nonplayer
import chr
import uiScriptLocale
import ui
import mouseModule
import constInfo
import pack
import chat
import extern_wa_shopitem

if app.ENABLE_RENDER_TARGET:
	import uiRenderTarget

if app.ENABLE_SASH_SYSTEM:
	import sash

WARP_SCROLLS = [22011, 22000, 22010]

DESC_DEFAULT_MAX_COLS = 26
DESC_WESTERN_MAX_COLS = 35
DESC_WESTERN_MAX_WIDTH = 220

def chop(n):
	return round(n - 0.5, 1)

def pointop(n):
	t = int(n)
	if t / 10 < 1:
		return "0."+n
	else:
		return n[0:len(n)-1]+"."+n[len(n)-1:]

def SplitDescription(desc, limit):
	total_tokens = desc.split()
	line_tokens = []
	line_len = 0
	lines = []
	for token in total_tokens:
		if "|" in token:
			sep_pos = token.find("|")
			line_tokens.append(token[:sep_pos])

			lines.append(" ".join(line_tokens))
			line_len = len(token) - (sep_pos + 1)
			line_tokens = [token[sep_pos+1:]]
		else:
			line_len += len(token)
			if len(line_tokens) + line_len > limit:
				lines.append(" ".join(line_tokens))
				line_len = len(token)
				line_tokens = [token]
			else:
				line_tokens.append(token)

	if line_tokens:
		lines.append(" ".join(line_tokens))

	return lines

###################################################################################################
## ToolTip
##
##   NOTE : 현재는 Item과 Skill을 상속으로 특화 시켜두었음
##          하지만 그다지 의미가 없어 보임
##
class ToolTip(ui.ThinBoard):

	TOOL_TIP_WIDTH = 190
	TOOL_TIP_HEIGHT = 10

	TEXT_LINE_HEIGHT = 17

	TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
	SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	PRICE_COLOR = 0xffFFB96D

	HIGH_PRICE_COLOR = SPECIAL_TITLE_COLOR
	MIDDLE_PRICE_COLOR = grp.GenerateColor(0.85, 0.85, 0.85, 1.0)
	LOW_PRICE_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

	ENABLE_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	DISABLE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

	NEGATIVE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)
	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
	SPECIAL_POSITIVE_COLOR = grp.GenerateColor(0.6911, 0.8754, 0.7068, 1.0)
	SPECIAL_POSITIVE_COLOR2 = grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0)

	if app.BL_67_ATTR:
		ATTR_6TH_7TH_COLOR = -102

	CONDITION_COLOR = 0xffBEB47D
	CAN_LEVEL_UP_COLOR = 0xff8EC292
	CANNOT_LEVEL_UP_COLOR = DISABLE_COLOR
	NEED_SKILL_POINT_COLOR = 0xff9A9CDB
	if app.ENABLE_APPLY_RANDOM:
		APPLY_RANDOM_TEXT_COLOR = 0xff7AF6D4
	if app.ENABLE_NEW_NAME_ITEM:
		TYRANIS_TOOLTIP_COLOR = 0xff5FFFF3
		CHANGELOOK_ITEMNAME_COLOR = 0xffBCE55C
		RENDER_TARGET = 0xff90ee90

	def __init__(self, width = TOOL_TIP_WIDTH, isPickable=False):
		ui.ThinBoard.__init__(self, "TOP_MOST")

		if isPickable:
			pass
		else:
			self.AddFlag("not_pick")

		self.AddFlag("float")
		self.AddFlag("animate")

		self.followFlag = True
		self.toolTipWidth = width

		self.xPos = -1
		self.yPos = -1

		self.defFontName = localeInfo.UI_DEF_FONT
		self.ClearToolTip()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def AutoAppendNewTextLineResize(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()
 
		(textWidth, textHeight) = textLine.GetTextSize()
		textWidth += 30
		textHeight += 10
		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth
 
		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)
 
		self.childrenList.append(textLine)
 
		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.AlignHorizonalCenter()
		return textLine

	def ClearToolTip(self):
		self.toolTipHeight = 12
		self.childrenList = []

	def SetFollow(self, flag):
		self.followFlag = flag

	def SetDefaultFontName(self, fontName):
		self.defFontName = fontName

	def AppendSpace(self, size):
		self.toolTipHeight += size
		self.ResizeToolTip()

	def AppendHorizontalLine(self):

		for i in xrange(2):
			horizontalLine = ui.Line()
			horizontalLine.SetParent(self)
			horizontalLine.SetPosition(0, self.toolTipHeight + 3 + i)
			horizontalLine.SetWindowHorizontalAlignCenter()
			horizontalLine.SetSize(150, 0)
			horizontalLine.Show()

			if 0 == i:
				horizontalLine.SetColor(0xff555555)
			else:
				horizontalLine.SetColor(0xff000000)

			self.childrenList.append(horizontalLine)

		self.toolTipHeight += 11
		self.ResizeToolTip()

	def AlignHorizonalCenter(self):
		for child in self.childrenList:
			(x, y)=child.GetLocalPosition()
			child.SetPosition(self.toolTipWidth/2, y)
		self.ResizeToolTip()

	if app.ENABLE_ZODIAC_MISSION:
		def SetThinBoardSize(self, width, height = 12):
			self.toolTipWidth = width 
			self.toolTipHeight = height

	def AutoAppendNewTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.Show()
		textLine.SetPosition(15, self.toolTipHeight)
		
		self.childrenList.append(textLine)
		(textWidth, textHeight) = textLine.GetTextSize()
		textWidth += 30
		textHeight += 10
		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth
		
		self.toolTipHeight += textHeight
		self.ResizeToolTipText(textWidth, self.toolTipHeight)
		return textLine
	
	def AutoAppendTextLineSpecial(self, text, color = FONT_COLOR, centerAlign = TRUE):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.Show()

		self.childrenList.append(textLine)
		(textWidth, textHeight)=textLine.GetTextSize()
		textWidth += 40
		textHeight += 5

		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth
		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)
		self.toolTipHeight += textHeight
		self.ResizeToolTip()
		return textLine

	def AutoAppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		(textWidth, textHeight)=textLine.GetTextSize()

		textWidth += 40
		textHeight += 5

		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		self.toolTipHeight += textHeight

		return textLine

	def SetThinBoardSize(self, width, height = 12) :
		self.toolTipWidth = width 
		self.toolTipHeight = height

	def GetToolTopHeight(self):
		return self.toolTipHeight

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

		return textLine

	def AppendDescription(self, desc, limit, color = FONT_COLOR):
		if localeInfo.IsEUROPE():
			self.__AppendDescription_WesternLanguage(desc, color)
		else:
			self.__AppendDescription_EasternLanguage(desc, limit, color)

	def __AppendDescription_EasternLanguage(self, description, characterLimitation, color=FONT_COLOR):
		length = len(description)
		if 0 == length:
			return

		lineCount = grpText.GetSplitingTextLineCount(description, characterLimitation)
		for i in xrange(lineCount):
			if 0 == i:
				self.AppendSpace(5)
			self.AppendTextLine(grpText.GetSplitingTextLine(description, characterLimitation, i), color)

	def __AppendDescription_WesternLanguage(self, desc, color=FONT_COLOR):
		lines = SplitDescription(desc, DESC_WESTERN_MAX_COLS)
		if not lines:
			return

		self.AppendSpace(5)
		for line in lines:
			self.AppendTextLine(line, color)

	def ResizeToolTip(self):
		self.SetSize(self.toolTipWidth, self.TOOL_TIP_HEIGHT + self.toolTipHeight)

	def ResizeToolTipText(self, x, y):
		self.SetSize(x, y)

	if app.ENABLE_FEATURES_OXEVENT:
		def AppendPlayersDesc(self, name, level, guild, empire, job, date, correct_answers):

			def IsExistKey(name):
				return (job == localeInfo.OXEVENT_TOOLTIP_EMPTY)

			if not IsExistKey(job):
				self.ClearToolTip()

				itemImage = ui.ImageBox()
				itemImage.SetParent(self)
				itemImage.LoadImage(job)
				itemImage.SetPosition(itemImage.GetWidth()/2 + 50, self.toolTipHeight)
				itemImage.Show()

				self.mainDescription = [
					name,
					level,
					guild,
					empire,
					date,
					correct_answers
				]

				self.AppendSpace(50)
				for i in xrange(len(self.mainDescription)):
					self.AppendTextLine(self.mainDescription[i], self.SPECIAL_POSITIVE_COLOR)

				self.toolTipHeight += 16
				self.childrenList.append(itemImage)
				self.ResizeToolTip()
			else:
				self.HideToolTip()

	def SetTitle(self, name):
		self.AppendTextLine(name, self.TITLE_COLOR)

	def GetLimitTextLineColor(self, curValue, limitValue):
		if curValue < limitValue:
			return self.DISABLE_COLOR

		return self.ENABLE_COLOR

	def GetChangeTextLineColor(self, value, isSpecial=False):
		if value > 0:
			if isSpecial:
				return self.SPECIAL_POSITIVE_COLOR
			else:
				return self.POSITIVE_COLOR

		if 0 == value:
			return self.NORMAL_COLOR

		return self.NEGATIVE_COLOR

	def SetToolTipPosition(self, x = -1, y = -1):
		self.xPos = x
		self.yPos = y

	def ShowToolTip(self):
		self.SetTop()
		self.Show()

		self.OnUpdate()

	def HideToolTip(self):
		self.Hide()

	def OnUpdate(self):

		if not self.followFlag:
			return

		x = 0
		y = 0
		width = self.GetWidth()
		height = self.toolTipHeight

		if -1 == self.xPos and -1 == self.yPos:

			(mouseX, mouseY) = wndMgr.GetMousePosition()

			if mouseY < wndMgr.GetScreenHeight() - 300:
				y = mouseY + 40
			else:
				y = mouseY - height - 30

			x = mouseX - width/2

		else:

			x = self.xPos - width/2
			y = self.yPos - height

		x = max(x, 0)
		y = max(y, 0)
		x = min(x + width/2, wndMgr.GetScreenWidth() - width/2) - width/2
		y = min(y + self.GetHeight(), wndMgr.GetScreenHeight()) - self.GetHeight()

		parentWindow = self.GetParentProxy()
		if parentWindow:
			(gx, gy) = parentWindow.GetGlobalPosition()
			x -= gx
			y -= gy

		self.SetPosition(x, y)

class ItemToolTip(ToolTip):

	if app.ENABLE_SEND_TARGET_INFO:
		isStone = False
		isBook = False
		isBook2 = False
		
	CHARACTER_NAMES = (
		localeInfo.TOOLTIP_WARRIOR,
		localeInfo.TOOLTIP_ASSASSIN,
		localeInfo.TOOLTIP_SURA,
		localeInfo.TOOLTIP_SHAMAN
	)
	if app.ENABLE_WOLFMAN_CHARACTER:
		CHARACTER_NAMES += (
			localeInfo.TOOLTIP_WOLFMAN,
		)

	CHARACTER_COUNT = len(CHARACTER_NAMES)
	WEAR_NAMES = (
		localeInfo.TOOLTIP_ARMOR,
		localeInfo.TOOLTIP_HELMET,
		localeInfo.TOOLTIP_SHOES,
		localeInfo.TOOLTIP_WRISTLET,
		localeInfo.TOOLTIP_WEAPON,
		localeInfo.TOOLTIP_NECK,
		localeInfo.TOOLTIP_EAR,
		localeInfo.TOOLTIP_UNIQUE,
		localeInfo.TOOLTIP_SHIELD,
		localeInfo.TOOLTIP_ARROW
	)
	WEAR_COUNT = len(WEAR_NAMES)

	if app.ELEMENT_SPELL_WORLDARD:
		AFFECT_DICT_ELEMENT = {
			item.APPLY_ATTBONUS_ELEC : [localeInfo.REFINE_ELEMENT_TEXT_ELECT,localeInfo.TOOLTIP_APPLY_ENCHANT_ELECT2,0xFF23B7E8],
			item.APPLY_ATTBONUS_FIRE : [localeInfo.REFINE_ELEMENT_TEXT_FIRE,localeInfo.TOOLTIP_APPLY_ENCHANT_FIRE2,0xFFDD483B],
			item.APPLY_ATTBONUS_ICE : [localeInfo.REFINE_ELEMENT_TEXT_ICE,localeInfo.TOOLTIP_APPLY_ENCHANT_ICE2,0xFF3D6CD0],
			item.APPLY_ATTBONUS_WIND : [localeInfo.REFINE_ELEMENT_TEXT_WIND,localeInfo.TOOLTIP_APPLY_ENCHANT_WIND2,0xFF37CF21],
			item.APPLY_ATTBONUS_EARTH : [localeInfo.REFINE_ELEMENT_TEXT_EARTH,localeInfo.TOOLTIP_APPLY_ENCHANT_EARTH2,0xFFF4CA10],
			item.APPLY_ATTBONUS_DARK : [localeInfo.REFINE_ELEMENT_TEXT_DARK,localeInfo.TOOLTIP_APPLY_ENCHANT_DARK2,0xFFB72EE0],
		}

		GetAddElementSpellOpen = False
		GetItemElementGrade = -1
		GetItemElementType = -1
		GetItemElementValue = -1
		GetItemElementAttack = -1
		GetFuncElementSpell = True


	AFFECT_DICT = {
		item.APPLY_MAX_HP : localeInfo.TOOLTIP_MAX_HP,
		item.APPLY_MAX_SP : localeInfo.TOOLTIP_MAX_SP,
		item.APPLY_CON : localeInfo.TOOLTIP_CON,
		item.APPLY_INT : localeInfo.TOOLTIP_INT,
		item.APPLY_STR : localeInfo.TOOLTIP_STR,
		item.APPLY_DEX : localeInfo.TOOLTIP_DEX,
		item.APPLY_ATT_SPEED : localeInfo.TOOLTIP_ATT_SPEED,
		item.APPLY_MOV_SPEED : localeInfo.TOOLTIP_MOV_SPEED,
		item.APPLY_CAST_SPEED : localeInfo.TOOLTIP_CAST_SPEED,
		item.APPLY_HP_REGEN : localeInfo.TOOLTIP_HP_REGEN,
		item.APPLY_SP_REGEN : localeInfo.TOOLTIP_SP_REGEN,
		item.APPLY_POISON_PCT : localeInfo.TOOLTIP_APPLY_POISON_PCT,
		item.APPLY_STUN_PCT : localeInfo.TOOLTIP_APPLY_STUN_PCT,
		item.APPLY_SLOW_PCT : localeInfo.TOOLTIP_APPLY_SLOW_PCT,
		item.APPLY_CRITICAL_PCT : localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,
		item.APPLY_PENETRATE_PCT : localeInfo.TOOLTIP_APPLY_PENETRATE_PCT,

		item.APPLY_ATTBONUS_WARRIOR : localeInfo.TOOLTIP_APPLY_ATTBONUS_WARRIOR,
		item.APPLY_ATTBONUS_ASSASSIN : localeInfo.TOOLTIP_APPLY_ATTBONUS_ASSASSIN,
		item.APPLY_ATTBONUS_SURA : localeInfo.TOOLTIP_APPLY_ATTBONUS_SURA,
		item.APPLY_ATTBONUS_SHAMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_SHAMAN,
		item.APPLY_ATTBONUS_MONSTER : localeInfo.TOOLTIP_APPLY_ATTBONUS_MONSTER,

		item.APPLY_ATTBONUS_HUMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_HUMAN,
		item.APPLY_ATTBONUS_ANIMAL : localeInfo.TOOLTIP_APPLY_ATTBONUS_ANIMAL,
		item.APPLY_ATTBONUS_ORC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ORC,
		item.APPLY_ATTBONUS_MILGYO : localeInfo.TOOLTIP_APPLY_ATTBONUS_MILGYO,
		item.APPLY_ATTBONUS_UNDEAD : localeInfo.TOOLTIP_APPLY_ATTBONUS_UNDEAD,
		item.APPLY_ATTBONUS_DEVIL : localeInfo.TOOLTIP_APPLY_ATTBONUS_DEVIL,
		item.APPLY_STEAL_HP : localeInfo.TOOLTIP_APPLY_STEAL_HP,
		item.APPLY_STEAL_SP : localeInfo.TOOLTIP_APPLY_STEAL_SP,
		item.APPLY_MANA_BURN_PCT : localeInfo.TOOLTIP_APPLY_MANA_BURN_PCT,
		item.APPLY_DAMAGE_SP_RECOVER : localeInfo.TOOLTIP_APPLY_DAMAGE_SP_RECOVER,
		item.APPLY_BLOCK : localeInfo.TOOLTIP_APPLY_BLOCK,
		item.APPLY_DODGE : localeInfo.TOOLTIP_APPLY_DODGE,
		item.APPLY_RESIST_SWORD : localeInfo.TOOLTIP_APPLY_RESIST_SWORD,
		item.APPLY_RESIST_TWOHAND : localeInfo.TOOLTIP_APPLY_RESIST_TWOHAND,
		item.APPLY_RESIST_DAGGER : localeInfo.TOOLTIP_APPLY_RESIST_DAGGER,
		item.APPLY_RESIST_BELL : localeInfo.TOOLTIP_APPLY_RESIST_BELL,
		item.APPLY_RESIST_FAN : localeInfo.TOOLTIP_APPLY_RESIST_FAN,
		item.APPLY_RESIST_BOW : localeInfo.TOOLTIP_RESIST_BOW,
		item.APPLY_RESIST_FIRE : localeInfo.TOOLTIP_RESIST_FIRE,
		item.APPLY_RESIST_ELEC : localeInfo.TOOLTIP_RESIST_ELEC,
		item.APPLY_RESIST_MAGIC : localeInfo.TOOLTIP_RESIST_MAGIC,
		item.APPLY_RESIST_WIND : localeInfo.TOOLTIP_APPLY_RESIST_WIND,
		item.APPLY_REFLECT_MELEE : localeInfo.TOOLTIP_APPLY_REFLECT_MELEE,
		item.APPLY_REFLECT_CURSE : localeInfo.TOOLTIP_APPLY_REFLECT_CURSE,
		item.APPLY_POISON_REDUCE : localeInfo.TOOLTIP_APPLY_POISON_REDUCE,
		item.APPLY_KILL_SP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_SP_RECOVER,
		item.APPLY_EXP_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_EXP_DOUBLE_BONUS,
		item.APPLY_GOLD_DOUBLE_BONUS : localeInfo.TOOLTIP_APPLY_GOLD_DOUBLE_BONUS,
		item.APPLY_ITEM_DROP_BONUS : localeInfo.TOOLTIP_APPLY_ITEM_DROP_BONUS,
		item.APPLY_POTION_BONUS : localeInfo.TOOLTIP_APPLY_POTION_BONUS,
		item.APPLY_KILL_HP_RECOVER : localeInfo.TOOLTIP_APPLY_KILL_HP_RECOVER,
		item.APPLY_IMMUNE_STUN : localeInfo.TOOLTIP_APPLY_IMMUNE_STUN,
		item.APPLY_IMMUNE_SLOW : localeInfo.TOOLTIP_APPLY_IMMUNE_SLOW,
		item.APPLY_IMMUNE_FALL : localeInfo.TOOLTIP_APPLY_IMMUNE_FALL,
		item.APPLY_BOW_DISTANCE : localeInfo.TOOLTIP_BOW_DISTANCE,
		item.APPLY_DEF_GRADE_BONUS : localeInfo.TOOLTIP_DEF_GRADE,
		item.APPLY_ATT_GRADE_BONUS : localeInfo.TOOLTIP_ATT_GRADE,
		item.APPLY_MAGIC_ATT_GRADE : localeInfo.TOOLTIP_MAGIC_ATT_GRADE,
		item.APPLY_MAGIC_DEF_GRADE : localeInfo.TOOLTIP_MAGIC_DEF_GRADE,
		item.APPLY_MAX_STAMINA : localeInfo.TOOLTIP_MAX_STAMINA,
		item.APPLY_MALL_ATTBONUS : localeInfo.TOOLTIP_MALL_ATTBONUS,
		item.APPLY_MALL_DEFBONUS : localeInfo.TOOLTIP_MALL_DEFBONUS,
		item.APPLY_MALL_EXPBONUS : localeInfo.TOOLTIP_MALL_EXPBONUS,
		item.APPLY_MALL_ITEMBONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS,
		item.APPLY_MALL_GOLDBONUS : localeInfo.TOOLTIP_MALL_GOLDBONUS,
		item.APPLY_SKILL_DAMAGE_BONUS : localeInfo.TOOLTIP_SKILL_DAMAGE_BONUS,
		item.APPLY_NORMAL_HIT_DAMAGE_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
		item.APPLY_SKILL_DEFEND_BONUS : localeInfo.TOOLTIP_SKILL_DEFEND_BONUS,
		item.APPLY_NORMAL_HIT_DEFEND_BONUS : localeInfo.TOOLTIP_NORMAL_HIT_DEFEND_BONUS,
		item.APPLY_PC_BANG_EXP_BONUS : localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC,
		item.APPLY_PC_BANG_DROP_BONUS : localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC,
		item.APPLY_RESIST_WARRIOR : localeInfo.TOOLTIP_APPLY_RESIST_WARRIOR,
		item.APPLY_RESIST_ASSASSIN : localeInfo.TOOLTIP_APPLY_RESIST_ASSASSIN,
		item.APPLY_RESIST_SURA : localeInfo.TOOLTIP_APPLY_RESIST_SURA,
		item.APPLY_RESIST_SHAMAN : localeInfo.TOOLTIP_APPLY_RESIST_SHAMAN,
		item.APPLY_MAX_HP_PCT : localeInfo.TOOLTIP_APPLY_MAX_HP_PCT,
		item.APPLY_MAX_SP_PCT : localeInfo.TOOLTIP_APPLY_MAX_SP_PCT,
		item.APPLY_ENERGY : localeInfo.TOOLTIP_ENERGY,
		item.APPLY_COSTUME_ATTR_BONUS : localeInfo.TOOLTIP_COSTUME_ATTR_BONUS,

		item.APPLY_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MAGIC_ATTBONUS_PER,
		item.APPLY_MELEE_MAGIC_ATTBONUS_PER : localeInfo.TOOLTIP_MELEE_MAGIC_ATTBONUS_PER,
		item.APPLY_RESIST_ICE : localeInfo.TOOLTIP_RESIST_ICE,
		item.APPLY_RESIST_EARTH : localeInfo.TOOLTIP_RESIST_EARTH,
		item.APPLY_RESIST_DARK : localeInfo.TOOLTIP_RESIST_DARK,
		item.APPLY_ANTI_CRITICAL_PCT : localeInfo.TOOLTIP_ANTI_CRITICAL_PCT,
		item.APPLY_ANTI_PENETRATE_PCT : localeInfo.TOOLTIP_ANTI_PENETRATE_PCT,

		item.APPLY_ATTBONUS_ELEC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ELEC,
		item.APPLY_ATTBONUS_FIRE : localeInfo.TOOLTIP_APPLY_ATTBONUS_FIRE,
		item.APPLY_ATTBONUS_ICE : localeInfo.TOOLTIP_APPLY_ATTBONUS_ICE,
		item.APPLY_ATTBONUS_WIND : localeInfo.TOOLTIP_APPLY_ATTBONUS_WIND,
		item.APPLY_ATTBONUS_EARTH : localeInfo.TOOLTIP_APPLY_ATTBONUS_EARTH,
		item.APPLY_ATTBONUS_DARK : localeInfo.TOOLTIP_APPLY_ATTBONUS_DARK,

	}
	if app.ENABLE_CONQUEROR_LEVEL:
		AFFECT_DICT.update({
			item.APPLY_SUNGMA_STR : localeInfo.TOOLTIP_SUNGMA_STR,
			item.APPLY_SUNGMA_HP : localeInfo.TOOLTIP_SUNGMA_HP,
			item.APPLY_SUNGMA_MOVE : localeInfo.TOOLTIP_SUNGMA_MOVE,
			item.APPLY_SUNGMA_INMUNE : localeInfo.TOOLTIP_SUNGMA_IMMUNE,
		})

	if app.ENABLE_WOLFMAN_CHARACTER:
		AFFECT_DICT.update({
			item.APPLY_BLEEDING_PCT : localeInfo.TOOLTIP_APPLY_BLEEDING_PCT,
			item.APPLY_BLEEDING_REDUCE : localeInfo.TOOLTIP_APPLY_BLEEDING_REDUCE,
			item.APPLY_ATTBONUS_WOLFMAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_WOLFMAN,
			item.APPLY_RESIST_CLAW : localeInfo.TOOLTIP_APPLY_RESIST_CLAW,
			item.APPLY_RESIST_WOLFMAN : localeInfo.TOOLTIP_APPLY_RESIST_WOLFMAN,
		})

	if app.ENABLE_MAGIC_REDUCTION_SYSTEM:
		AFFECT_DICT.update({
			item.APPLY_RESIST_MAGIC_REDUCTION : localeInfo.TOOLTIP_RESIST_MAGIC_REDUCTION,
		})

	AFFECT_DICT.update({
		item.APPLY_RESIST_HUMAN : localeInfo.TOOLTIP_RESIST_HUMAN,
		})
		
	AFFECT_DICT.update({
		item.APPLY_ENCHANT_ELEC : localeInfo.TOOLTIP_APPLY_ENCHANT_ELECT,
		item.APPLY_ENCHANT_FIRE : localeInfo.TOOLTIP_APPLY_ENCHANT_FIRE,
		item.APPLY_ENCHANT_ICE : localeInfo.TOOLTIP_APPLY_ENCHANT_ICE,
		item.APPLY_ENCHANT_WIND : localeInfo.TOOLTIP_APPLY_ENCHANT_WIND,
		item.APPLY_ENCHANT_EARTH : localeInfo.TOOLTIP_APPLY_ENCHANT_EARTH,
		item.APPLY_ENCHANT_DARK : localeInfo.TOOLTIP_APPLY_ENCHANT_DARK,
		
		item.APPLY_ATTBONUS_SWORD : localeInfo.TOOLTIP_APPLY_ATTBONUS_SWORD,
		item.APPLY_ATTBONUS_TWOHAND: localeInfo.TOOLTIP_APPLY_ATTBONUS_TWOHAND,
		item.APPLY_ATTBONUS_DAGGER : localeInfo.TOOLTIP_APPLY_ATTBONUS_DAGGER,
		item.APPLY_ATTBONUS_BELL : localeInfo.TOOLTIP_APPLY_ATTBONUS_BELL,
		item.APPLY_ATTBONUS_FAN : localeInfo.TOOLTIP_APPLY_ATTBONUS_FAN,
		item.APPLY_ATTBONUS_BOW : localeInfo.TOOLTIP_APPLY_ATTBONUS_BOW,
		item.APPLY_ATTBONUS_ZODIAC : localeInfo.TOOLTIP_APPLY_ATTBONUS_ZODIAC,
		item.APPLY_ATTBONUS_DESERT : localeInfo.TOOLTIP_APPLY_ATTBONUS_DESERT,
		item.APPLY_ATTBONUS_INSECT : localeInfo.TOOLTIP_APPLY_ATTBONUS_INSECT,
		#item.APPLY_ATTBONUS_CLAW : localeInfo.TOOLTIP_APPLY_ATTBONUS_CLAW,	
	})
	
	if app.NEW_BONUS:
		AFFECT_DICT.update({
			item.APPLY_ATTBONUS_STONE : localeInfo.TOOLTIP_APPLY_ATT_STONE,
			item.APPLY_ATTBONUS_BOSS : localeInfo.TOOLTIP_APPLY_ATT_BOSS,
		})

	POINT_DICT = {item.GetApplyPoint(affect): name for affect, name in AFFECT_DICT.items()}

	ATTRIBUTE_NEED_WIDTH = {
		23 : 230,
		24 : 230,
		25 : 230,
		26 : 220,
		27 : 210,

		35 : 210,
		36 : 210,
		37 : 210,
		38 : 210,
		39 : 210,
		40 : 210,
		41 : 210,

		42 : 220,
		43 : 230,
		45 : 230,
	}

	ANTI_FLAG_DICT = {
		0 : item.ITEM_ANTIFLAG_WARRIOR,
		1 : item.ITEM_ANTIFLAG_ASSASSIN,
		2 : item.ITEM_ANTIFLAG_SURA,
		3 : item.ITEM_ANTIFLAG_SHAMAN,
	}

	if app.ENABLE_WOLFMAN_CHARACTER:
		ANTI_FLAG_DICT.update({
			4 : item.ITEM_ANTIFLAG_WOLFMAN,
		})

	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)

	def __init__(self, *args, **kwargs):
		ToolTip.__init__(self, *args, **kwargs)
		self.itemVnum = 0
		self.isShopItem = False
		if app.ENABLE_OFFLINESHOP_SYSTEM:
			self.isOfflineShopItem = False

		# 아이템 툴팁을 표시할 때 현재 캐릭터가 착용할 수 없는 아이템이라면 강제로 Disable Color로 설정 (이미 그렇게 작동하고 있으나 꺼야 할 필요가 있어서)
		self.bCannotUseItemForceSetDisableColor = True

		self.interface = None

		#self.show_render = True
		self.show_render = False

		self.emoji_safebox = 0
		self.GetItemElementGrade = 0

	def __del__(self):
		ToolTip.__del__(self)

	def BindInterface(self,interface):
		self.interface = interface

	def ShowRender(self,value):
		#self.show_render = value
		self.show_render = False

	def ShowSafeboxEmoji(self,value):
		self.emoji_safebox = value

	def SetCannotUseItemForceSetDisableColor(self, enable):
		self.bCannotUseItemForceSetDisableColor = enable

	def CanEquip(self):
		if not item.IsEquipmentVID(self.itemVnum):
			return True

		race = player.GetRace()
		job = chr.RaceToJob(race)
		if not self.ANTI_FLAG_DICT.has_key(job):
			return False

		if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
			return False

		sex = chr.RaceToSex(race)

		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			return False

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
			return False

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if item.LIMIT_LEVEL == limitType:
				if player.GetStatus(player.LEVEL) < limitValue:
					return False
			"""
			elif item.LIMIT_STR == limitType:
				if player.GetStatus(player.ST) < limitValue:
					return False
			elif item.LIMIT_DEX == limitType:
				if player.GetStatus(player.DX) < limitValue:
					return False
			elif item.LIMIT_INT == limitType:
				if player.GetStatus(player.IQ) < limitValue:
					return False
			elif item.LIMIT_CON == limitType:
				if player.GetStatus(player.HT) < limitValue:
					return False
			"""

		return True

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		if not self.CanEquip() and self.bCannotUseItemForceSetDisableColor:
			color = self.DISABLE_COLOR

		return ToolTip.AppendTextLine(self, text, color, centerAlign)

	if app.ENABLE_AURA_SYSTEM:
		def AppendTextLineAbsorb(self, text, color = FONT_COLOR, centerAlign = True):
			return ToolTip.AppendTextLine(self, text, color, centerAlign)

	if app.ENABLE_SWITCHBOT:
		def SetSwitchBotItem(self, vnum):
			item.SelectItem(vnum)
			self.AppendTextLine(item.GetItemName(), self.SPECIAL_TITLE_COLOR)
			self.AppendSpace(5)
			itemDesc = localeInfo.SWITCHBOT_ACTIVE
			self.__AdjustMaxWidth(0, itemDesc)
			self.AppendDescription(itemDesc, 26)

	def ClearToolTip(self):
		self.isShopItem = False
		self.toolTipWidth = self.TOOL_TIP_WIDTH
		if app.ELEMENT_SPELL_WORLDARD:
			self.ClearElementsSpellItemDate()
		ToolTip.ClearToolTip(self)

	if app.ENABLE_OFFLINESHOP_SYSTEM:
		def SetOfflineShopBuilderItem(self, invenType, invenPos, offlineShopIndex, window_type = player.INVENTORY):
			self.ClearToolTip()

			itemVnum = player.GetItemIndex(invenType, invenPos)
			if (itemVnum == 0):
				return

			item.SelectItem(itemVnum)

			metinSlot = [player.GetItemMetinSocket(invenType, invenPos, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(invenType, invenPos, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			apply_random_list = []
			if app.ENABLE_APPLY_RANDOM:
				apply_random_list = [player.GetItemApplyRandom(invenType, invenPos, i) for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM)]

			if app.ENABLE_GLOVE_SYSTEM:
				attrRandomSlot = [player.GetItemRandomAttribute(invenType, invenPos, i) for i in xrange(item.GLOVE_ATTR_MAX_NUM)]
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, invenType, invenPos, 0, 0, attrRandomSlot, applyRandomList = apply_random_list)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, invenType, invenPos)

			price = shop.GetOfflineShopItemPriceReal(invenType, invenPos)
			if price > 0:
				self.AppendPrice(price)

		def SetOfflineShopItem(self, slotIndex):
			itemVnum = shop.GetOfflineShopItemID(slotIndex)
			if (itemVnum == 0):
				return

			self.ClearToolTip()

			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetOfflineShopItemMetinSocket(slotIndex, i))

			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetOfflineShopItemAttribute(slotIndex, i))

			apply_random_list = []
			if app.ENABLE_APPLY_RANDOM:
				for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM):
					apply_random_list.append(shop.GetOfflineShopItemAttributeRandom(slotIndex, i))
					# apply_random_list = [player.GetItemApplyRandom(window_type, slotIndex, i) for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM)]


			if app.WJ_CHANGELOOK_SYSTEM:
				transmutation = shop.GetOfflineShopItemTransmutation(slotIndex)
				if not transmutation:
					transmutation = 0

				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, player.INVENTORY, -1, -1, transmutation)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, applyRandomList = apply_random_list)

			price = shop.GetOfflineShopItemPrice(slotIndex)
			if price > 0:
				self.AppendPrice(price)

			if shop.GetOfflineShopItemStatus(slotIndex) == 1:
				self.AppendTextLine(localeInfo.OFFLINE_SHOP_ITEM_SOLD, self.DISABLE_COLOR)
				self.AppendTextLine(localeInfo.OFFLINE_SHOP_ITEM_SOLD2 % (shop.GetOfflineShopItemBuyerName(slotIndex)), self.DISABLE_COLOR)

	def SetInventoryItem(self, slotIndex, window_type = player.INVENTORY):
		itemVnum = player.GetItemIndex(window_type, slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		if shop.IsOpen():
			item.SelectItem(itemVnum)
			self.AppendSellingPrice(player.GetISellItemPrice(window_type, slotIndex))

		metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
		apply_random_list = []
		if app.ENABLE_APPLY_RANDOM:
			apply_random_list = [player.GetItemApplyRandom(window_type, slotIndex, i) for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM)]

		self.ShowSafeboxEmoji(1)
		if app.ELEMENT_SPELL_WORLDARD:
			self.FuncElementSpellItemDate(slotIndex)

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = [player.GetItemRandomAttribute(window_type, slotIndex, i) for i in xrange(item.GLOVE_ATTR_MAX_NUM)]
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, window_type, slotIndex, 0, 0, attrRandomSlot, applyRandomList = apply_random_list)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, window_type, slotIndex)

	if (app.WJ_COMBAT_ZONE):
		def SetShopItemByCombatZoneCoin(self, slotIndex):
			itemVnum = shop.GetItemID(slotIndex)
			if 0 == itemVnum:
				return

			price = shop.GetItemPrice(slotIndex)
			self.ClearToolTip()
			self.isShopItem = TRUE

			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetItemAttribute(slotIndex, i))

			if app.ENABLE_GLOVE_SYSTEM:
				attrRandomSlot = []
				for i in xrange(item.GLOVE_ATTR_MAX_NUM):
					attrRandomSlot.append(shop.GetItemRandomAttribute(slotIndex, i))
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0, 0, attrRandomSlot)		
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)


			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToCombatZoneCoinString(price)), self.HIGH_PRICE_COLOR)
			
	def SetShopItem(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))
		apply_random_list = []
		if app.ENABLE_APPLY_RANDOM:
			for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(shop.GetItemApplyRandom(slotIndex, i))
			
		if app.ENABLE_ITEMSHOP:
			item.SelectItem(itemVnum)
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					metinSlot[2] = limitValue
				elif item.LIMIT_REAL_TIME == limitType or item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					#metinSlot[2] = app.GetGlobalTimeStamp()+limitValue
					metinSlot[2] = limitValue

		if app.ELEMENT_SPELL_WORLDARD:
			(grade_element,attack_element,type_element,value_element) = shop.GetItemElements(slotIndex)
			self.ElementSpellItemDateDirect(grade_element,attack_element,type_element,value_element)

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = []
			for i in xrange(item.GLOVE_ATTR_MAX_NUM):
				attrRandomSlot.append(shop.GetItemRandomAttribute(slotIndex, i))
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0, 0, attrRandomSlot, applyRandomList = apply_random_list)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

		if app.ENABLE_SEND_TARGET_INFO:
			def SetItemToolTipStone(self, itemVnum):
				self.itemVnum = itemVnum
				item.SelectItem(itemVnum)
				itemType = item.GetItemType()

				itemDesc = item.GetItemDescription()
				itemSummary = item.GetItemSummary()
				attrSlot = 0
				self.__AdjustMaxWidth(attrSlot, itemDesc)
				itemName = item.GetItemName()
				realName = itemName[:itemName.find("+")]
				self.SetTitle(realName + " +0 - +4")

				## Description ###
				self.AppendDescription(itemDesc, 26)
				self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

				if item.ITEM_TYPE_METIN == itemType:
					self.AppendMetinInformation()
					self.AppendMetinWearInformation()

				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
						self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)

					elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						self.AppendTimerBasedOnWearLastTime(metinSlot)

				
				
				self.ShowToolTip()

		extern_wa_shopitem.FuncCheckPrice(self,slotIndex,price)

	def SetShopItemBySecondaryCoin(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = []
			for i in xrange(item.GLOVE_ATTR_MAX_NUM):
				attrRandomSlot.append(shop.GetItemRandomAttribute(slotIndex, i))
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0,0, attrRandomSlot)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

		self.AppendPriceBySecondaryCoin(price)

	def SetExchangeOwnerItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromSelf(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromSelf(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromSelf(slotIndex, i))
		apply_random_list = []
		if app.ENABLE_APPLY_RANDOM:
			for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(exchange.GetItemApplyRandomFromSelf(slotIndex, i))

		if app.ELEMENT_SPELL_WORLDARD:
			grade_element = exchange.GetItemElementGradeFromSelf(slotIndex)
			if grade_element > 0:
				attack_element = exchange.GetItemElementAttackFromSelf(slotIndex,grade_element-1)
				type_element = exchange.GetItemElementTypeFromSelf(slotIndex)
				value_element = exchange.GetItemElementValueFromSelf(slotIndex,grade_element-1)
				self.ElementSpellItemDateDirect(grade_element,attack_element,type_element,value_element)

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = []
			for i in xrange(item.GLOVE_ATTR_MAX_NUM):
				attrRandomSlot.append(shop.GetItemRandomAttribute(slotIndex, i))
			
			if app.ENABLE_NEW_NAME_ITEM:
				newname = exchange.GetItemNewName(slotIndex,True)
				if not newname:
					newname = "^"
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0,0, attrRandomSlot, newname, applyRandomList = apply_random_list)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0,0, attrRandomSlot, applyRandomList = apply_random_list)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetExchangeTargetItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromTarget(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromTarget(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromTarget(slotIndex, i))
		apply_random_list = []
		if app.ENABLE_APPLY_RANDOM:
			for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(exchange.GetItemApplyRandomFromTarget(slotIndex, i))

		if app.ELEMENT_SPELL_WORLDARD:
			grade_element = exchange.GetItemElementGradeFromTarget(slotIndex)
			if grade_element > 0:
				attack_element = exchange.GetItemElementAttackFromTarget(slotIndex,grade_element-1)
				type_element = exchange.GetItemElementTypeFromTarget(slotIndex)
				value_element = exchange.GetItemElementValueFromTarget(slotIndex,grade_element-1)
				self.ElementSpellItemDateDirect(grade_element,attack_element,type_element,value_element)

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = []
			for i in xrange(item.GLOVE_ATTR_MAX_NUM):
				attrRandomSlot.append(shop.GetItemRandomAttribute(slotIndex, i))
			
			if app.ENABLE_NEW_NAME_ITEM:
				newname = exchange.GetItemNewName(slotIndex,False)
				if not newname:
					newname = "^"
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0,0, attrRandomSlot, newname, applyRandomList = apply_random_list)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0,0, attrRandomSlot, applyRandomList = apply_random_list)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)
		
	def SetEditPrivateShopItem(self, invenType, invenPos, price):
		itemVnum = player.GetItemIndex(invenType, invenPos)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		self.ClearToolTip()
		self.AppendSellingPrice(price)

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(invenPos, i))

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = []
			for i in xrange(item.GLOVE_ATTR_MAX_NUM):
				attrRandomSlot.append(shop.GetItemRandomAttribute(slotIndex, i))
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0,0, attrRandomSlot)		
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)
		
	def SetPrivateShopBuilderItem(self, invenType, invenPos, privateShopSlotIndex):
		itemVnum = player.GetItemIndex(invenType, invenPos)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		self.ClearToolTip()
		self.AppendSellingPrice(shop.GetPrivateShopItemPrice(invenType, invenPos))

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(invenPos, i))
		apply_random_list = []
		if app.ENABLE_APPLY_RANDOM:
			for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(player.GetItemApplyRandom(invenPos, i))

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = []
			for i in xrange(item.GLOVE_ATTR_MAX_NUM):
				attrRandomSlot.append(shop.GetItemRandomAttribute(slotIndex, i))
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0,0, attrRandomSlot, applyRandomList = apply_random_list)		
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetSafeBoxItem(self, slotIndex):
		itemVnum = safebox.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetItemAttribute(slotIndex, i))
		apply_random_list = []
		if app.ENABLE_APPLY_RANDOM:
			for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(safebox.GetItemApplyRandom(slotIndex, i))


		self.ShowSafeboxEmoji(2)

		if app.ELEMENT_SPELL_WORLDARD:
			(grade_element,attack_element,type_element,value_element) = safebox.GetElements(slotIndex)
			self.ElementSpellItemDateDirect(grade_element,attack_element,type_element,value_element)

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = []
			for i in xrange(item.GLOVE_ATTR_MAX_NUM):
				attrRandomSlot.append(safebox.GetMallItemRandomAttribute(slotIndex, i))
			
			if app.ENABLE_NEW_NAME_ITEM:
				newname = safebox.GetItemNewName(slotIndex)
				if not newname:
					newname = "^"

			if app.ENABLE_NEW_NAME_ITEM:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0, safebox.GetItemFlags(slotIndex),-1,0,0, attrRandomSlot, newname, applyRandomList = apply_random_list)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0, safebox.GetItemFlags(slotIndex),-1,0,0, attrRandomSlot, applyRandomList = apply_random_list)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot, safebox.GetItemFlags(slotIndex))

	def SetMallItem(self, slotIndex):
		itemVnum = safebox.GetMallItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetMallItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetMallItemAttribute(slotIndex, i))
		apply_random_list = []
		if app.ENABLE_APPLY_RANDOM:
			for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM):
				apply_random_list.append(safebox.GetMallItemApplyRandom(slotIndex, i))
		
		if app.ENABLE_ITEMSHOP:
			item.SelectItem(itemVnum)
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					metinSlot[0] = limitValue
				elif item.LIMIT_REAL_TIME == limitType or item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					metinSlot[0] = app.GetGlobalTimeStamp()+limitValue

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = []
			for i in xrange(item.GLOVE_ATTR_MAX_NUM):
				attrRandomSlot.append(safebox.GetMallItemRandomAttribute(slotIndex, i))
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0,0, attrRandomSlot, applyRandomList = apply_random_list)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

	if app.ENABLE_WIKI:
		def SetItemToolTipWiki(self, itemVnum):
			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)
			metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [(0,0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					metinSlot[0] = limitValue
				elif item.LIMIT_REAL_TIME == limitType or item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					metinSlot[0] = app.GetGlobalTimeStamp()+limitValue
			self.SetTitle(item.GetItemName())
			self.AppendDescription(item.GetItemDescription(), 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			self.AppendWearableInformation()
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					if metinSlot[0] > 0:
						self.AppendMallItemLastTime(metinSlot[0])
					break
			self.ShowToolTip()

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def GetBuffSkillLevelGrade(self, skillLevel):
			skillLevel = int(skillLevel)
			if skillLevel >= 0 and skillLevel < 20:
				return ("%d" % int(skillLevel))
			if skillLevel >= 20 and skillLevel < 30:
				return ("M%d" % int(skillLevel-19))
			if skillLevel >= 30 and skillLevel < 40: 
				return ("G%d" % int(skillLevel-29))
			if skillLevel == 40: 
				return "P"

		def AppendEXPGauge(self, exp_perc):
			IMG_PATH = "d:/ymir work/ui/aslan/buffnpc/"
			gauge_empty_list = []
			gauge_full_list = []
			x_pos = [35, 17, 1, 19]
			for i in xrange(4):
				gauge_empty = ui.ExpandedImageBox()
				gauge_empty.SetParent(self)
				gauge_empty.LoadImage(IMG_PATH + "exp_empty.sub")
				if i <= 1:
					gauge_empty.SetPosition(self.toolTipWidth/2 - x_pos[i], self.toolTipHeight)
				else:
					gauge_empty.SetPosition(self.toolTipWidth/2 + x_pos[i], self.toolTipHeight)
				gauge_empty.Show()

				gauge_full = ui.ExpandedImageBox()
				gauge_full.SetParent(self)
				gauge_full.LoadImage(IMG_PATH + "exp_full.sub")
				if i <= 1:
					gauge_full.SetPosition(self.toolTipWidth/2 - x_pos[i], self.toolTipHeight)
				else:
					gauge_full.SetPosition(self.toolTipWidth/2 + x_pos[i], self.toolTipHeight)
					
				gauge_empty_list.append(gauge_empty)
				gauge_full_list.append(gauge_full)
		
			exp_perc = float(exp_perc / 100.0)
			exp_bubble_perc = 25.0

			for i in xrange(4):
				if exp_perc > exp_bubble_perc:
					exp_bubble_perc += 25.0
					gauge_full_list[i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
					gauge_full_list[i].Show()
				else:
					exp_perc = float((exp_perc - exp_bubble_perc) * 4 / 100) 
					gauge_full_list[i].SetRenderingRect(0.0, exp_perc, 0.0, 0.0)
					gauge_full_list[i].Show()
					break

			self.childrenList.append(gauge_empty_list)
			self.childrenList.append(gauge_full_list)
			
			self.toolTipHeight += 18
			self.ResizeToolTip()

	def SetItemToolTip(self, itemVnum):
		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))

		if app.ENABLE_ITEMSHOP:
			item.SelectItem(itemVnum)
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
					metinSlot[0] = limitValue
				elif item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
					metinSlot[0] = limitValue
				elif item.LIMIT_REAL_TIME == limitType:
					metinSlot[0] = app.GetGlobalTimeStamp()+limitValue

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = []
			for i in xrange(item.GLOVE_ATTR_MAX_NUM):
				attrRandomSlot.append((0, 0))
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,0,0, attrRandomSlot)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetItemBuff(self, itemVnum, time, permanente):
		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))

		if app.ENABLE_GLOVE_SYSTEM:
			attrRandomSlot = []
			for i in xrange(item.GLOVE_ATTR_MAX_NUM):
				attrRandomSlot.append(safebox.GetMallItemRandomAttribute(slotIndex, i))
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0,0,player.INVENTORY,-1,1,0, attrRandomSlot)			
		else:
			self.AddItemData(itemVnum,metinSlot,attrSlot,0, 0, player.INVENTORY, -1, 1)


		if permanente == 0:
			self.AppendMallItemLastTime(time)
		else:
			self.AppendSpace(5)
			self.AppendTextLine("Permanente")

	def __AppendAttackSpeedInfo(self, item):
		atkSpd = item.GetValue(0)

		if atkSpd < 80:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_FAST
		elif atkSpd <= 95:
			stSpd = localeInfo.TOOLTIP_ITEM_FAST
		elif atkSpd <= 105:
			stSpd = localeInfo.TOOLTIP_ITEM_NORMAL
		elif atkSpd <= 120:
			stSpd = localeInfo.TOOLTIP_ITEM_SLOW
		else:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_SLOW

		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_SPEED % stSpd, self.NORMAL_COLOR)

	def __AppendAttackGradeInfo(self):
		atkGrade = item.GetValue(1)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_GRADE % atkGrade, self.GetChangeTextLineColor(atkGrade))
	
	if app.ENABLE_SASH_SYSTEM:
		def CalcSashValue(self, value, abs):

			if not value:
				return 0
			
			valueCalc 	= round(value * abs) / 100
			valueCalc 	+= 0.5 #changed the -0.5 which + 0.5 (rounding bug)
			valueCalc 	= int(valueCalc) +1 if valueCalc > 0 else int(valueCalc)
			value 		= 1 if (valueCalc <= 0 and value > 0) else valueCalc
			return value

	if app.ENABLE_RARITY:
		def __AppendAttackPowerInfo(self, itemAbsChance = 0, metinSlot = []):
			minPower = item.GetValue(3)
			maxPower = item.GetValue(4)
			addPower = item.GetValue(5)
			
			if app.ENABLE_SASH_SYSTEM:
				if itemAbsChance:
					minPower = self.CalcSashValue(minPower, itemAbsChance)
					maxPower = self.CalcSashValue(maxPower, itemAbsChance)
					addPower = self.CalcSashValue(addPower, itemAbsChance)

			text = ""
			if maxPower > minPower:
				if app.ELEMENT_SPELL_WORLDARD:
					if self.GetItemElementGrade >= 0:
						if self.GetAddElementSpellOpen and self.GetFuncElementSpell:
							self.GetItemElementAttack += 2
							text = localeInfo.TOOLTIP_APPLY_ITEM_ATT_POWER_REFINE % (minPower+addPower, maxPower+addPower, self.GetItemElementAttack ,self.GetItemElementAttack+10)
						else:
							if self.GetItemElementGrade > 0:
								text = localeInfo.TOOLTIP_ITEM_ATT_POWER_REFINE % (minPower+addPower, maxPower+addPower, self.GetItemElementAttack )
							else:
								text = localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower)
					else:
						text = localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower)
				else:
					text = localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower)
			else:
				if self.GetItemElementGrade > 0:
					if itemAbsChance:
						text = localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG_ELEMENT % (minPower+addPower, self.CalcSashValue(self.GetItemElementAttack, itemAbsChance))
				else:
					text = localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % (minPower+addPower)

			if item.RARITY_TYPE_INDEX < len(metinSlot):
				rarityValue = item.GetRarityPoint(-2,metinSlot[item.RARITY_TYPE_INDEX])
				if rarityValue > 0:
					text+=" |cffFFFF95(+%d%%)"%rarityValue

			self.AppendTextLine(text, self.POSITIVE_COLOR)
		
		def __AppendMagicAttackInfo(self, itemAbsChance = 0, metinSlot = []):
			minMagicAttackPower = item.GetValue(1)
			maxMagicAttackPower = item.GetValue(2)
			addPower = item.GetValue(5)
			if app.ENABLE_SASH_SYSTEM:
				if itemAbsChance:
					minMagicAttackPower = self.CalcSashValue(minMagicAttackPower, itemAbsChance)
					maxMagicAttackPower = self.CalcSashValue(maxMagicAttackPower, itemAbsChance)
					addPower = self.CalcSashValue(addPower, itemAbsChance)

			if minMagicAttackPower > 0 or maxMagicAttackPower > 0:
				text = ""
				if maxMagicAttackPower > minMagicAttackPower:
					text = localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (minMagicAttackPower + addPower, maxMagicAttackPower + addPower)
				else:
					text = localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % (minMagicAttackPower + addPower)

				if item.RARITY_TYPE_INDEX < len(metinSlot):
					rarityValue = item.GetRarityPoint(-1,metinSlot[item.RARITY_TYPE_INDEX])
					if rarityValue > 0:
						text+=" |cffFFFF95(+%d%%)"%rarityValue
				self.AppendTextLine(text, self.POSITIVE_COLOR)
		def __AppendMagicDefenceInfo(self, itemAbsChance = 0, metinSlot = []):
			magicDefencePower = item.GetValue(0)
			if app.ENABLE_SASH_SYSTEM:
				if itemAbsChance:
					magicDefencePower = self.CalcSashValue(magicDefencePower, itemAbsChance)

			if magicDefencePower > 0:
				text = localeInfo.TOOLTIP_ITEM_MAGIC_DEF_POWER % magicDefencePower
				if item.RARITY_TYPE_INDEX < len(metinSlot):
					rarityValue = item.GetRarityPoint(-3,metinSlot[item.RARITY_TYPE_INDEX])
					if rarityValue > 0:
						text+=" |cffFFFF95(+%d%%)"%rarityValue
				self.AppendTextLine(text, self.GetChangeTextLineColor(magicDefencePower))
	else:
		def __AppendAttackPowerInfo(self, itemAbsChance = 0):
			minPower = item.GetValue(3)
			maxPower = item.GetValue(4)
			addPower = item.GetValue(5)
			
			if app.ENABLE_SASH_SYSTEM:
				if itemAbsChance:
					minPower = self.CalcSashValue(minPower, itemAbsChance)
					maxPower = self.CalcSashValue(maxPower, itemAbsChance)
					addPower = self.CalcSashValue(addPower, itemAbsChance)
			
			if maxPower > minPower:
				if app.ELEMENT_SPELL_WORLDARD:
					if self.GetItemElementGrade >= 0:
						if self.GetAddElementSpellOpen and self.GetFuncElementSpell:
							self.GetItemElementAttack += 2
							self.AppendTextLine(localeInfo.TOOLTIP_APPLY_ITEM_ATT_POWER_REFINE % (minPower+addPower, maxPower+addPower, self.GetItemElementAttack ,self.GetItemElementAttack+10), self.POSITIVE_COLOR)
						else:
							if self.GetItemElementGrade > 0:
								self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER_REFINE % (minPower+addPower, maxPower+addPower, self.GetItemElementAttack ), self.POSITIVE_COLOR)
							else:
								self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower), self.POSITIVE_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower), self.POSITIVE_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER % (minPower+addPower, maxPower+addPower), self.POSITIVE_COLOR)
			else:
				if self.GetItemElementGrade > 0:
					if itemAbsChance:
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG_ELEMENT % (minPower+addPower, self.CalcSashValue(self.GetItemElementAttack, itemAbsChance)), self.POSITIVE_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % (minPower+addPower), self.POSITIVE_COLOR)

		def __AppendMagicAttackInfo(self, itemAbsChance = 0):
			minMagicAttackPower = item.GetValue(1)
			maxMagicAttackPower = item.GetValue(2)
			addPower = item.GetValue(5)
			
			if app.ENABLE_SASH_SYSTEM:
				if itemAbsChance:
					minMagicAttackPower = self.CalcSashValue(minMagicAttackPower, itemAbsChance)
					maxMagicAttackPower = self.CalcSashValue(maxMagicAttackPower, itemAbsChance)
					addPower = self.CalcSashValue(addPower, itemAbsChance)
			
			if minMagicAttackPower > 0 or maxMagicAttackPower > 0:
				if maxMagicAttackPower > minMagicAttackPower:
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (minMagicAttackPower + addPower, maxMagicAttackPower + addPower), self.POSITIVE_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % (minMagicAttackPower + addPower), self.POSITIVE_COLOR)

		def __AppendMagicDefenceInfo(self, itemAbsChance = 0):
			magicDefencePower = item.GetValue(0)
			
			if app.ENABLE_SASH_SYSTEM:
				if itemAbsChance:
					magicDefencePower = self.CalcSashValue(magicDefencePower, itemAbsChance)
			
			if magicDefencePower > 0:
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_MAGIC_DEF_POWER % magicDefencePower, self.GetChangeTextLineColor(magicDefencePower))

	def __AppendBonusElementSash(self, itemAbsChance = 0):
		if self.GetItemElementGrade >= 0:
			if self.GetAddElementSpellOpen and self.GetFuncElementSpell:
				self.GetItemElementValue += 1
				self.AppendTextLine(self.AFFECT_DICT_ELEMENT[self.GetItemElementType][1]%(self.GetItemElementValue,self.GetItemElementValue+7), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])
			else:
				if self.GetItemElementGrade > 0:
					if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_SASH and itemAbsChance:
						value = self.CalcSashValue(self.GetItemElementValue, itemAbsChance)

						self.AppendTextLine(self.AFFECT_DICT[self.GetItemElementType](value), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])

	if app.ENABLE_SPECIAL_COSTUME_ATTR:
		def __AppendAttributeInformation(self, attrSlot, itemAbsChance = 0, itemVnum = 0):
			if 0 != attrSlot:
				if app.ENABLE_LOCK_ATTR:
					lockIndex=[]
					isAddonItem = False
					for j in xrange(5):
						if attrSlot[j][0] == item.APPLY_NORMAL_HIT_DAMAGE_BONUS or attrSlot[j][0] == item.APPLY_SKILL_DAMAGE_BONUS:
							isAddonItem = True
							break
					for j in xrange(2):
						if attrSlot[7+j][1] != 0:
							if isAddonItem:
								if attrSlot[7+j][1] == 1 or attrSlot[7+j][1] == 2:
									lockIndex.append(0)
									lockIndex.append(1)
									continue
							lockIndex.append(attrSlot[7+j][1]-1)

				needInfo = False
				attrLimit = -1
				if itemVnum != 0:
					item.SelectItem(itemVnum)
					__CanAttrNewAttr = {
						item.ITEM_TYPE_COSTUME: {
							item.COSTUME_TYPE_BODY : item.SPECIAL_ATTR_COSTUME_BODY_LIMIT,
							item.COSTUME_TYPE_HAIR : item.SPECIAL_ATTR_COSTUME_HAIR_LIMIT,
							item.COSTUME_TYPE_WEAPON : item.SPECIAL_ATTR_COSTUME_WEAPON_LIMIT,
							item.COSTUME_TYPE_MOUNT_SKIN : item.SPECIAL_ATTR_COSTUME_MOUNT_SKIN_LIMIT,
							item.COSTUME_TYPE_SKIN_SASH : item.SPECIAL_ATTR_COSTUME_SASH_SKIN_LIMIT,
						},
						item.ITEM_TYPE_SHINING : {
							item.SHINING_WEAPON : item.SPECIAL_ATTR_COSTUME_SHINING_LIMIT,
							item.SHINING_ARMOR : item.SPECIAL_ATTR_COSTUME_SHINING_LIMIT,
							item.SHINING_SPECIAL : item.SPECIAL_ATTR_COSTUME_SHINING_LIMIT,
						},
					}
					if __CanAttrNewAttr.has_key(item.GetItemType()):
						if __CanAttrNewAttr[item.GetItemType()].has_key(item.GetItemSubType()):
							needInfo = True
							attrLimit = __CanAttrNewAttr[item.GetItemType()][item.GetItemSubType()]

				for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					type = attrSlot[i][0]
					value = attrSlot[i][1]
					if 0 == value:
						if needInfo == True and i <= attrLimit-1:
							self.AppendTextLine(localeInfo.NOBONUS, self.NORMAL_COLOR)
						if app.ENABLE_LOCK_ATTR:
							if type == 0 or 0 == value:
								continue
						continue

					affectString = self.__GetAffectString(type, value)
					if app.ENABLE_SASH_SYSTEM:
						if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_SASH and itemAbsChance:
							value = self.CalcSashValue(value, itemAbsChance)
							affectString = self.__GetAffectString(type, value)

					if affectString:
						affectColor = self.__GetAttributeColor(i, value)
						if app.ENABLE_LOCK_ATTR:
							if i in lockIndex:
								self.AppendTextLine("<<"+affectString+">>", self.SPECIAL_TITLE_COLOR)
								continue
						self.AppendTextLine(affectString, affectColor)
	else:
		def __AppendAttributeInformation(self, attrSlot, itemAbsChance = 0):
			if 0 != attrSlot:
				for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					type = attrSlot[i][0]
					value = attrSlot[i][1]
					if 0 == value:
						continue
					affectString = self.__GetAffectString(type, value)
					if app.ENABLE_SASH_SYSTEM:
						if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_SASH and itemAbsChance:
							value = self.CalcSashValue(value, itemAbsChance)
							affectString = self.__GetAffectString(type, value)
					
					if affectString:
						affectColor = self.__GetAttributeColor(i, value)
						self.AppendTextLine(affectString, affectColor)

	def __GetAttributeColor(self, index, value):
		if value > 0:
			if index >= player.ATTRIBUTE_SLOT_RARE_START and index < player.ATTRIBUTE_SLOT_RARE_END:
				return self.ATTR_6TH_7TH_COLOR
			else:
				return self.SPECIAL_POSITIVE_COLOR
		elif value == 0:
			return self.NORMAL_COLOR
		else:
			return self.NEGATIVE_COLOR

	if app.ENABLE_APPLY_RANDOM:
		def __AppendDefaultItemApplyInformation(self, apply_random_list):
			if apply_random_list != None:
				for i in xrange(player.APPLY_RANDOM_SLOT_MAX_NUM):
					type = apply_random_list[i][0]
					value = apply_random_list[i][1]

					if 0 == value:
						continue

					affectString = self.__GetAffectString(type, value)
					if affectString:
						self.AppendTextLine(affectString, self.APPLY_RANDOM_TEXT_COLOR)

	if app.BL_67_ATTR:
		def AppendAttribute6th7thPossibility(self, attrSlot):
			if attrSlot == 0:
				return

			count = 0
			for i in range(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]

				if 0 == type or 0 == value:
					continue

				count += 1

			if (5 <= count <= 6):
				self.AppendTextLine(localeInfo.ATTR_6TH_7TH_POSSIBILITY, self.ATTR_6TH_7TH_COLOR)

	def __IsPolymorphItem(self, itemVnum):
		if itemVnum >= 70103 and itemVnum <= 70106:
			return 1
		return 0

	def __SetPolymorphItemTitle(self, monsterVnum):
		if localeInfo.IsVIETNAM():
			itemName =item.GetItemName()
			itemName+=" "
			itemName+=nonplayer.GetMonsterName(monsterVnum)
		else:
			itemName =nonplayer.GetMonsterName(monsterVnum)
			itemName+=" "
			itemName+=item.GetItemName()
		self.SetTitle(itemName)

	if app.ENABLE_RARITY:
		def __SetRarityBar(self, itemVnum, metinSlot):
			if app.CLOSE_ATTACK_DEFENSE_DECREASE_VALUE:
				return

			if item.RARITY_TYPE_INDEX >= len(metinSlot):
				return
			elif item.IsRarityItem(itemVnum) == 0:
				return
			gaugeNames = ["normal","uncommun","rare","epic","relic","legendary"]

			rarityType = metinSlot[item.RARITY_TYPE_INDEX]
			if rarityType >= len(gaugeNames):
				return
			rarityValue = metinSlot[item.RARITY_VALUE_INDEX]
			rarityMaxValue = item.GetRarityMaxValue(itemVnum, rarityType)

			self.toolTipHeight += self.TEXT_LINE_HEIGHT

			rarityBar = ui.RarityGauge()
			rarityBar.SetParent(self)
			rarityBar.MakeGauge(160,gaugeNames[rarityType])
			rarityBar.SetPercentage(rarityValue,rarityMaxValue)
			rarityBar.SetPosition((self.toolTipWidth/2)-(rarityBar.GetWidth()/2),self.toolTipHeight)
			rarityBar.Show()
			self.childrenList.append(rarityBar)
			self.toolTipHeight += self.TEXT_LINE_HEIGHT-5
			self.ResizeToolTip()

			if player.IsGameMaster():
				self.AppendTextLine("type: %d value: %d"%(rarityType,rarityValue))

			if rarityValue == 0:
				self.AppendTextLine("(0%) - Repair for use this item",self.NEGATIVE_COLOR)
			else:
				percentBar = int((float(rarityValue)/float(rarityMaxValue))*100)
				self.AppendTextLine("("+str(percentBar)+"%)",0xffD1D1D1)

		def __SetRarityType(self, itemVnum, metinSlot):
			if item.RARITY_TYPE_INDEX >= len(metinSlot):
				return
			elif item.IsRarityItem(itemVnum) == 0:
				return
			rarityType = metinSlot[item.RARITY_TYPE_INDEX]
			rarityNames = [["(Normal)",0xff8E8E8E],["(Uncommun)",0xffD1D1D1],["(Rare)",0xff7CA1FF],["(Epic)",0xffFF3252],["(Relic)",0xff34FF30],["(Legendary)",0xffFA30FF]]
			if rarityType >= len(rarityNames):
				return
			self.AppendTextLine(rarityNames[rarityType][0],rarityNames[rarityType][1])

	if app.ENABLE_NEW_NAME_ITEM:
		def __SetItemTitle(self, itemVnum, metinSlot, attrSlot, window_type = player.INVENTORY, slotIndex = -1, newname = "^"):
			newname = item.GetItemName()
			if self.__IsPolymorphItem(itemVnum):
				self.__SetPolymorphItemTitle(metinSlot[0])
			else:
				if newname == "^" and slotIndex >= 0:
					if window_type == player.INVENTORY:
						newname = player.GetItemNewName(window_type, slotIndex)
					elif window_type == player.SAFEBOX:
						newname = safebox.GetItemNewName(slotIndex)
					elif window_type == player.MALL:
						newname = safebox.GetItemNewName(slotIndex)
				if self.__IsAttr(attrSlot):
					self.__SetSpecialItemTitle(newname)
					return
				self.__SetNormalItemTitle(newname)
		def __SetNormalItemTitle(self, newname):
			if app.ENABLE_SEND_TARGET_INFO:
				if self.isStone:
					itemName = item.GetItemName()
					realName = itemName[:itemName.find("+")]
					self.SetTitle(realName + " +0 - +4")
				else:
					if newname != "^":
						self.SetTitle(newname)
					else:
						self.SetTitle(item.GetItemName())
			else:
				self.SetTitle(item.GetItemName())
		def __SetSpecialItemTitle(self, newname):
			if newname != "^":
				self.AppendTextLine(newname, self.SPECIAL_TITLE_COLOR)
			else:
				self.AppendTextLine(item.GetItemName(), self.SPECIAL_TITLE_COLOR)
	else:
		def __SetNormalItemTitle(self):
			if app.ENABLE_SEND_TARGET_INFO:
				if self.isStone:
					itemName = item.GetItemName()
					realName = itemName[:itemName.find("+")]
					self.SetTitle(realName + " +0/+4")
				else:
					self.SetTitle(item.GetItemName())
			else:
				self.SetTitle(item.GetItemName())

		def __SetSpecialItemTitle(self):
			self.AppendTextLine(item.GetItemName(), self.SPECIAL_TITLE_COLOR)


		def __SetItemTitle(self, itemVnum, metinSlot, attrSlot):
			if localeInfo.IsCANADA():
				if 72726 == itemVnum or 72730 == itemVnum:
					self.AppendTextLine(item.GetItemName(), grp.GenerateColor(1.0, 0.7843, 0.0, 1.0))
					return

			if self.__IsPolymorphItem(itemVnum):
				self.__SetPolymorphItemTitle(metinSlot[0])
			else:
				if self.__IsAttr(attrSlot):
					self.__SetSpecialItemTitle()
					return

				self.__SetNormalItemTitle()

	if app.ENABLE_RENDER_TARGET:
		def __AppendRenderTarget(self, itemVnum):
			if uiRenderTarget.IsCanShowItems(itemVnum):
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_RENDER_TARGET, self.POSITIVE_COLOR)

	def __IsAttr(self, attrSlot):
		if not attrSlot:
			return False

		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			if 0 != type:
				return True

		return False

	if app.ENABLE_RARITY_REFINE:
		def AddRefineRarityItemData(self, itemVnum, metinSlot, attrSlot, apply_random_list):
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlotData = metinSlot[i]

				if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
					metinSlot[i] = player.METIN_SOCKET_TYPE_SILVER

			self.show_render = False

			REFINE_MODE = {
				0 : 50000,
				1 : 75000,
				2 : 100000,
				3 : 150000,
				4 : 200000,
				5 : 300000,
			}

			metinSlot[6] = metinSlot[6] + 1
			metinSlot[7] = REFINE_MODE[metinSlot[6]]

			self.AddItemData(itemVnum, metinSlot, attrSlot, applyRandomList = apply_random_list)

	if app.__RENEWAL_CRYSTAL__:
		def CrystalTimeCalculate(self, time):
			if time <= 0:
				return "0 " + localeInfo.SECOND
			second = int(time % 60)
			minute = int((time / 60) % 60)
			hour = int((time / 60) / 60) % 24
			day = int(int((time / 60) / 60) / 24)
			text = ""
			if day > 0:
				text += str(day) + localeInfo.DAY
				text += " "
			if hour > 0:
				text += str(hour) + " " + localeInfo.HOUR
				text += " "
			if minute > 0:
				text += str(minute) + " " + localeInfo.MINUTE
				text += " "
			if second > 0:
				text += str(second) + " " + localeInfo.SECOND
			return text
		def AppendCrystalLastTime(self, endTime):
			leftSec = max(0, endTime - app.GetGlobalTimeStamp())
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.LEFT_TIME + " : " + self.CrystalTimeCalculate(leftSec), self.NORMAL_COLOR)
		def CheckCrystalAttr(self, itemIdx, attrSlot):
			isCrystal = True if itemIdx >= 51010 and itemIdx <= 51035 else False
			if isCrystal:
				LEVEL_RANGE = 5
				attrSlot = [(0, 0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
				refineLevel = itemIdx - 51010
				m_AffectList = [[item.APPLY_ATTBONUS_MONSTER, 10], [item.APPLY_MAX_HP, 2000], [item.APPLY_ATTBONUS_HUMAN, 10], [item.APPLY_ATTBONUS_STONE, 10], [item.APPLY_ATTBONUS_ANIMAL, 10]]
				for i in xrange(len(m_AffectList)):
					bonusStartLevel = 1 + (i * LEVEL_RANGE);
					if refineLevel >= bonusStartLevel:
						bonusLevel = LEVEL_RANGE if refineLevel >= bonusStartLevel + (LEVEL_RANGE-1) else LEVEL_RANGE - ((bonusStartLevel + (LEVEL_RANGE-1)) - refineLevel);
						attrSlot[i] = (m_AffectList[i][0], bonusLevel * (m_AffectList[i][1]/LEVEL_RANGE))
			return attrSlot

	def AddRefineItemData(self, itemVnum, metinSlot, attrSlot = 0, apply_random_list = None):
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
				metinSlot[i]=player.METIN_SOCKET_TYPE_SILVER

		self.show_render = False

		if app.__RENEWAL_CRYSTAL__:
			attrSlot = self.CheckCrystalAttr(itemVnum, attrSlot)

		self.AddItemData(itemVnum, metinSlot, attrSlot, applyRandomList = apply_random_list)

	def AddItemData_Offline(self, itemVnum, itemDesc, itemSummary, metinSlot, attrSlot):
		self.__AdjustMaxWidth(attrSlot, itemDesc)
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

	def check_sigillo(self, item_vnum):
		for x in range(55701,55705):
			if x == item_vnum:
				return TRUE	
		if item_vnum == 55801:
			return TRUE
		return FALSE

	def AddSearchItemData(self, itemVnum, gold, attrSlot = 0):
		self.__AppendSearchIcon(itemVnum)

		self.show_render = False
		
		self.AddItemData(itemVnum,0,attrSlot,0,0,0)

		if gold != -1:
			self.AppendTextLine(localeInfo.PRICE01+localeInfo.NumberToMoneyString(gold), self.GetPriceColor(gold))

	if app.ELEMENT_SPELL_WORLDARD:
		def ElementSpellItemDate(self,slotIndex,grade_add=0):
			if slotIndex >= 0:
				if self.GetFuncElementSpell:
					if grade_add != 0:
						self.GetItemElementGrade = 0
						self.GetItemElementType = grade_add
						self.GetItemElementValue = 0
						self.GetItemElementAttack = 0
					else:
						if player.GetItemElementGrade(slotIndex) > 0:
							self.GetItemElementGrade = player.GetItemElementGrade(slotIndex)
							self.GetItemElementAttack = player.GetItemElementAttack(slotIndex,(self.GetItemElementGrade-1))
							self.GetItemElementType = player.GetItemElementType(slotIndex)
							self.GetItemElementValue = player.GetItemElementValue(slotIndex,(self.GetItemElementGrade-1))
				else:
					if player.GetItemElementGrade(slotIndex)-1 > 0:
						self.GetItemElementGrade = player.GetItemElementGrade(slotIndex)-1
						self.GetItemElementAttack = player.GetItemElementAttack(slotIndex,(self.GetItemElementGrade-1))
						self.GetItemElementType = player.GetItemElementType(slotIndex)
						self.GetItemElementValue = player.GetItemElementValue(slotIndex,(self.GetItemElementGrade-1))

		def ElementSpellItemDateDirect(self,grade,attack,type,value):
			self.GetItemElementGrade = grade
			self.GetItemElementType = type
			self.GetItemElementValue = value
			self.GetItemElementAttack = attack

		def ClearElementsSpellItemDate(self):
			self.GetAddElementSpellOpen = False
			self.GetFuncElementSpell = True
			self.GetItemElementGrade = 0
			self.GetItemElementType = 0
			self.GetItemElementValue = 0
			self.GetItemElementAttack = 0

		def FuncElementSpellItemDate(self,slotIndex):
			self.ClearElementsSpellItemDate()
			self.ElementSpellItemDate(slotIndex)


		def AddElementsSpellItemData(self, itemVnum, func, grade_add ,slotIndex, metinSlot, attrSlot = 0):
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlotData=metinSlot[i]
				if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
					metinSlot[i]=player.METIN_SOCKET_TYPE_SILVER

			
			self.ClearElementsSpellItemDate()

			self.GetFuncElementSpell = func
			self.ElementSpellItemDate(slotIndex,grade_add)
			self.GetAddElementSpellOpen = True
			self.show_render = False
			self.AddItemData(itemVnum, metinSlot, attrSlot)

		def ElementSpellItem(self):
			if self.GetItemElementGrade >= 0:
				if self.GetAddElementSpellOpen and self.GetFuncElementSpell:
					self.GetItemElementGrade += 1
					self.AppendTextLine(self.AFFECT_DICT_ELEMENT[self.GetItemElementType][0]%(self.GetItemElementGrade), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])
				else:
					if self.GetItemElementGrade > 0:
						self.AppendTextLine(self.AFFECT_DICT_ELEMENT[self.GetItemElementType][0]%(self.GetItemElementGrade), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])


		def __AppendBonusElement(self):
			if self.GetItemElementGrade >= 0:
				if self.GetAddElementSpellOpen and self.GetFuncElementSpell:
					self.GetItemElementValue += 1
					self.AppendTextLine(self.AFFECT_DICT_ELEMENT[self.GetItemElementType][1]%(self.GetItemElementValue,self.GetItemElementValue+7), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])
				else:
					if self.GetItemElementGrade > 0:
						self.AppendTextLine(self.AFFECT_DICT[self.GetItemElementType](self.GetItemElementValue), self.AFFECT_DICT_ELEMENT[self.GetItemElementType][2])

	if app.ENABLE_GLOVE_SYSTEM:
		def __AppendGlobveAttributeInformation(self, attrSlot, itemAbsChance = 0):
			if 0 != attrSlot:
				for i in xrange(item.GLOVE_ATTR_MAX_NUM):
					type = attrSlot[i][0]
					value = attrSlot[i][1]
					if 0 == value:
						continue
					
					affectString = self.__GetAffectString(type, value)
					if app.ENABLE_SASH_SYSTEM:
						if item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_SASH and itemAbsChance:
							value = self.CalcSashValue(value, itemAbsChance)
							affectString = self.__GetAffectString(type, value)
					
					if affectString:
						affectColor = self.__GetAttributeColor(i, value)
						self.AppendTextLine(affectString, affectColor)
					
		def AddRandomItemData(self, itemVnum, attrRandomSlot):
			self.itemVnum = itemVnum
			item.SelectItem(itemVnum)
			self.__AppendGlobveAttributeInformation(attrRandomSlot)

	def IsCanSeeRender(self, itemType, itemSubType):
		if item.ITEM_TYPE_COSTUME == itemType:
			if item.COSTUME_TYPE_HAIR == itemSubType\
				or item.COSTUME_TYPE_BODY == itemSubType\
				or item.COSTUME_TYPE_MOUNT == itemSubType\
				or item.COSTUME_TYPE_PET == itemSubType\
				or item.COSTUME_TYPE_SASH == itemSubType\
				or item.COSTUME_TYPE_WEAPON == itemSubType:
					return True
		elif item.ITEM_TYPE_ARMOR == itemType and itemSubType == item.ARMOR_BODY:
			return True
		elif item.ITEM_TYPE_WEAPON == itemType and itemSubType != item.WEAPON_ARROW:
			return True
		elif item.ITEM_TYPE_PET == itemType and itemSubType == item.PET_LEVELABLE:
			return True
		elif item.ITEM_TYPE_SHINING == itemType and (itemSubType == item.SHINING_WEAPON or itemSubType == item.SHINING_ARMOR):
			return True
		return False

	def AddItemData(self, itemVnum, metinSlot, attrSlot = 0, flags = 0, unbindTime = 0, window_type = player.INVENTORY, slotIndex = -1, buff = 0, search = 0, attrRandomSlot = None , newname = "^", applyRandomList = None): # app.ENABLE_GLOVE_SYSTEM
		if itemVnum == 55501:
			self.toolTipWidth = 250
			self.ResizeToolTip()

		self.itemVnum = itemVnum
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()
		self.interface = constInfo.GetInterfaceInstance()

		if 50026 == itemVnum:
			if 0 != metinSlot:
				name = item.GetItemName()
				if metinSlot[0] > 0:
					name += " "
					name += localeInfo.NumberToMoneyString(metinSlot[0])
				self.SetTitle(name)
				self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11
				self.ShowToolTip()
			return

		### Skill Book ###
		if app.ENABLE_SEND_TARGET_INFO:
			if 50300 == itemVnum and not self.isBook:
				if 0 != metinSlot and not self.isBook:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
					self.ShowToolTip()
				elif self.isBook:
					self.SetTitle(item.GetItemName())
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()

				if self.interface:
					if self.emoji_safebox > 0 and self.interface.SafeboxIsShow():
						self.AppendSpace(5)
						self.AppendTextLine("|Eemoji/key_ctrl|e + |Eemoji/key_lclick|e - Inventario")
				return
			elif 70037 == itemVnum:
				if 0 != metinSlot and not self.isBook2:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				elif self.isBook2:
					self.SetTitle(item.GetItemName())
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				
				if self.emoji_safebox > 0 and self.interface.SafeboxIsShow():
					self.AppendSpace(5)
					self.AppendTextLine("|Eemoji/key_ctrl|e + |Eemoji/key_lclick|e - Inventario")
					
				return
			elif 70055 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				
				if self.emoji_safebox > 0 and self.interface.SafeboxIsShow():
					self.AppendSpace(5)
					self.AppendTextLine("|Eemoji/key_ctrl|e + |Eemoji/key_lclick|e - Inventario")
				
				return
		else:
			if 50300 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
					self.ShowToolTip()
				return
			elif 70037 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				return
			elif 70055 == itemVnum:
				if 0 != metinSlot:
					self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
					self.AppendDescription(item.GetItemDescription(), 26)
					self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
					self.ShowToolTip()
				return
		###########################################################################################


		itemDesc = item.GetItemDescription()
		itemSummary = item.GetItemSummary()

		isCostumeItem = 0
		isCostumeHair = 0
		isCostumeBody = 0
		isCostumeSkinSash = 0
		isCostumePet = 0

		# if app.ENABLE_MOUNT_COSTUME_SYSTEM:
		isCostumeMount = 0

		# if app.ENABLE_SASH_SYSTEM:
		isCostumeSash = 0

		# if app.ENABLE_WEAPON_COSTUME_SYSTEM:
		isCostumeWeapon = 0

		# if app.ENABLE_AURA_SYSTEM:
		isCostumeAura = 0

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if itemVnum == 71998 or itemVnum == 71999:
				self.__AdjustMaxWidth(attrSlot, itemDesc)
				self.__SetItemTitle(itemVnum, 0, 0)
				self.AppendDescription(itemDesc, 26)
				self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)
				# self.AppendSpace(5)
				self.AppendTextLine("_________________", self.TITLE_COLOR)
				
				if metinSlot[0] == 0:
					self.AppendDescription(uiScriptLocale.ASLAN_BUFF_TOOLTIP_WITH_SOCKET_ZERO, 26)
				else:
					sexDesc = [uiScriptLocale.ASLAN_BUFF_TOOLTIP_MALE, uiScriptLocale.ASLAN_BUFF_TOOLTIP_FEMALE]
					self.AppendTextLine(sexDesc[metinSlot[1]], self.NORMAL_COLOR)
					self.AppendTextLine(uiScriptLocale.ASLAN_BUFF_TOOLTIP_LEVEL % str(metinSlot[2]), self.NORMAL_COLOR)
					exp_perc = float(metinSlot[3] / 100.0)
					self.AppendTextLine("%.2f%%" % exp_perc, self.TITLE_COLOR)
					self.AppendEXPGauge(metinSlot[3])
					self.AppendTextLine("_________________", self.TITLE_COLOR)
					self.AppendTextLine(uiScriptLocale.ASLAN_BUFF_TOOLTIP_SKILLPOINTS % str(metinSlot[4]), self.NORMAL_COLOR)
					self.AppendTextLine(uiScriptLocale.ASLAN_BUFF_TOOLTIP_INTELLIGENCE % str(metinSlot[5]), self.NORMAL_COLOR)
					self.AppendTextLine("_________________", self.TITLE_COLOR)
					
					self.AppendTextLine(skill.GetSkillName(94, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[0][0]), self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(skill.GetSkillName(95, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[0][1]), self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(skill.GetSkillName(96, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[1][0]), self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(skill.GetSkillName(109, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[1][1]), self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(skill.GetSkillName(110, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[2][0]), self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(skill.GetSkillName(111, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[2][1]), self.SPECIAL_POSITIVE_COLOR)
					
				self.ShowToolTip()
				return

		if app.ENABLE_COSTUME_SYSTEM:
			if item.ITEM_TYPE_COSTUME == itemType:
				isCostumeItem = 1
				isCostumeHair = item.COSTUME_TYPE_HAIR == itemSubType
				isCostumeBody = item.COSTUME_TYPE_BODY == itemSubType
				if app.ENABLE_MOUNT_COSTUME_SYSTEM:
					isCostumeMount = item.COSTUME_TYPE_MOUNT == itemSubType
				
				if app.ENABLE_MOUNT_SKIN and isCostumeMount == False:
					isCostumeMount = item.COSTUME_TYPE_MOUNT_SKIN == itemSubType

				isCostumePet = item.COSTUME_TYPE_PET == itemSubType

				if app.ENABLE_SASH_SYSTEM:
					isCostumeSash = itemSubType == item.COSTUME_TYPE_SASH

				if app.ENABLE_WEAPON_COSTUME_SYSTEM:
					isCostumeWeapon = item.COSTUME_TYPE_WEAPON == itemSubType

				isCostumeSkinSash = itemSubType == item.COSTUME_TYPE_SKIN_SASH

				if app.ENABLE_AURA_SYSTEM:
					isCostumeAura = item.COSTUME_TYPE_AURA == itemSubType

				#dbg.TraceError("IS_COSTUME_ITEM! body(%d) hair(%d)" % (isCostumeBody, isCostumeHair))

		self.__AdjustMaxWidth(attrSlot, itemDesc)
		if app.ENABLE_NEW_NAME_ITEM:
			self.__SetItemTitle(itemVnum, metinSlot, attrSlot, window_type, slotIndex, newname)
		else:
			self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		if player.IsGameMaster():
			self.AppendSpace(5)
			self.AppendTextLine("%d - %d/%d"%(itemVnum, itemType, itemSubType),self.SPECIAL_TITLE_COLOR)
			self.AppendSpace(5)

		if app.ELEMENT_SPELL_WORLDARD:
			self.ElementSpellItem()

		#if self.show_render == True:
		#	self.interface.CloseRenderTooltip()
		#	self.interface.RenderClearDates()
	
		if self.show_render == False or self.IsCanSeeRender(itemType, itemSubType) == False:
			interface = constInfo.GetInterfaceInstance()
			if interface != None:
				interface.CloseRenderTooltip()
				interface.RenderClearDates()

		### Hair Preview Image ###
		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

		if self.check_sigillo(itemVnum) or itemVnum == 55002:
			if attrSlot[0][1] != 0:
				self.AppendSpace(5)
				self.AppendTextLine("Livello: "+str(metinSlot[1]), self.NORMAL_COLOR)
				self.AppendTextLine("Hp: +"+pointop(str(attrSlot[0][1]))+"%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine("Dif: +"+pointop(str(attrSlot[1][1]))+"%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendTextLine("Mp: +"+pointop(str(attrSlot[2][1]))+"%", self.SPECIAL_POSITIVE_COLOR)
				self.AppendSpace(5)
				if itemVnum != 55002:
					days = (int(attrSlot[3][1])/60)/24
					hours = (int(attrSlot[3][1]) - (days*60*24)) / 60
					mins = int(attrSlot[3][1]) - (days*60*24) - (hours*60)
					self.AppendTextLine("Durata: %d giorni %d Ore %d Minuti" % (days, hours, mins), self.SPECIAL_POSITIVE_COLOR)

		if app.ENABLE_NEW_PET_SYSTEM:
			if item.ITEM_TYPE_PET == itemType:
				if itemSubType == item.PET_LEVELABLE:
					level = metinSlot[1]
					if level > 0:
						curPoint = metinSlot[2]
						if level >= 120:
							maxPoint = 2500000000
						else:
							maxPoint = constInfo.exp_table[level]
						curPoint = min(curPoint, maxPoint)
						curPoint = max(curPoint, 0)
						maxPoint = max(maxPoint, 0)

						self.AppendTextLine("Lv. %d"%level,self.SPECIAL_POSITIVE_COLOR)
						age_text = [localeInfo.PET_GUI_YOUNG, localeInfo.PET_GUI_WILD, localeInfo.PET_GUI_BRAVE, localeInfo.PET_GUI_HERO]
						self.AppendTextLine("%s : %s"%(localeInfo.PET_GUI_AGE,age_text[metinSlot[3]]),self.SPECIAL_POSITIVE_COLOR)
						self.AppendTextLine("%s : %.2f%%" % (localeInfo.TASKBAR_EXP, float(curPoint) / max(1, float(maxPoint)) * 100),self.SPECIAL_POSITIVE_COLOR)

						self.AppendSpace(5)

						#pet_bonus_types=[item.APPLY_MAX_HP,item.APPLY_ATTBONUS_MONSTER,item.APPLY_CRITICAL_PCT]
						#pet_bonus_value=[4000,20,10]
						for j in xrange(3):
							ptr = metinSlot[5+j]
							if ptr == 20:
								bonus_value = constInfo.pet_bonus_value[j]
							else:
								bonus_value = float(float(constInfo.pet_bonus_value[j])/constInfo.PET_BONUS_MAX_LEVEL) * ptr

							text = self.__GetAffectString(constInfo.pet_bonus_types[j],int(bonus_value))
							if text != None:
								text = text.replace(":","")
								index = text.find("+")
								if index == -1:
									index = text.find("%")
									if index == -1:
										index =0
								if not index  <= 0:
									new_text = text[:index]
									new_text += " (Lv %d  -  %s)"%(ptr,text[index:])
									self.AppendTextLine(new_text,self.TYRANIS_TOOLTIP_COLOR)
								else:
									new_text = text
									new_text += " (Lv %d  -  +%d)"%(ptr,int(bonus_value))
									self.AppendTextLine(new_text,self.TYRANIS_TOOLTIP_COLOR)

						self.AppendSpace(5)
						for j in xrange(len(attrSlot)):
							if attrSlot[j][0] == 0 or attrSlot[j][0] == 99:
								continue
							self.AppendTextLine(constInfo.pet_skill_data[attrSlot[j][0]][0]+"(Lv"+str(attrSlot[j][1])+")",self.SPECIAL_TITLE_COLOR)

						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.LEFT_TIME+ ": "+localeInfo.SecondToDHM(metinSlot[0]-app.GetGlobalTimeStamp()),self.SPECIAL_POSITIVE_COLOR)

						if self.show_render == True:
							item.SelectItem(itemVnum)
							if metinSlot[3] >= 3:
								self.interface.SetRenderDates(item.GetValue(1),5)
							else:
								self.interface.SetRenderDates(item.GetValue(0),5)

						## if have transmutation !!!!!!!!!!!!!!!!!
						#self.AppendSpace(5)
						#self.AppendTransmutationEx(window_type, slotIndex, transmutation) #if have transmutation...

		if app.ENABLE_GLOVE_SYSTEM:
			if attrRandomSlot:
				self.AddRandomItemData(itemVnum, attrRandomSlot)				
		if item.ITEM_TYPE_SHINING == itemType:
			if self.show_render == True:
				if itemSubType == item.SHINING_WEAPON:
					self.interface.SetRenderDates(itemVnum,6)
				elif itemSubType == item.SHINING_ARMOR:
					self.interface.SetRenderDates(itemVnum,7)

			self.__AppendAffectInformation()
			if app.ENABLE_SPECIAL_COSTUME_ATTR:
				self.__AppendAttributeInformation(attrSlot, 0, itemVnum)
			else:
				self.__AppendAttributeInformation(attrSlot)

			bHasRealtimeFlag = 0
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1
			if bHasRealtimeFlag == 1:
				self.AppendMallItemLastTime(metinSlot[0])

		elif item.ITEM_TYPE_RINGS == itemType:
			self.__AppendLimitInformation()
			if app.ENABLE_RARITY:
				self.__SetRarityType(itemVnum, metinSlot)
				self.__AppendAffectInformation(itemVnum, metinSlot)
			else:
				self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			if app.BL_67_ATTR:
				self.AppendAttribute6th7thPossibility(attrSlot)
			self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_ACCESSORY_MATERIAL_VNUM(itemVnum, itemType))

			if app.ENABLE_RARITY:
				self.__SetRarityBar(itemVnum, metinSlot)
			self.AppendWearableInformation()

		### Weapon ###
		elif item.ITEM_TYPE_WEAPON == itemType:
			self.__AppendLimitInformation()
			if app.ENABLE_RARITY:
				self.__SetRarityType(itemVnum, metinSlot)

			if self.show_render == True:
				arrow_render = False
				if itemSubType == item.WEAPON_ARROW:
					arrow_render = True

				if arrow_render == False:
					interface = constInfo.GetInterfaceInstance()
					if interface != None:
						interface.SetRenderDates(itemVnum,1)


			self.AppendSpace(5)

			if app.ENABLE_RARITY:
				if item.WEAPON_FAN == itemSubType:
					self.__AppendMagicAttackInfo(0,metinSlot)
					self.__AppendAttackPowerInfo(0,metinSlot)
				else:
					self.__AppendAttackPowerInfo(0,metinSlot)
					self.__AppendMagicAttackInfo(0,metinSlot)
				if app.ENABLE_APPLY_RANDOM:
					self.__AppendDefaultItemApplyInformation(applyRandomList)
				self.__AppendAffectInformation(itemVnum,metinSlot)
			else:
				## 부채일 경우 마공을 먼저 표시한다.
				if item.WEAPON_FAN == itemSubType:
					self.__AppendMagicAttackInfo()
					self.__AppendAttackPowerInfo()

				else:
					self.__AppendAttackPowerInfo()
					self.__AppendMagicAttackInfo()
				if app.ENABLE_APPLY_RANDOM:
					self.__AppendDefaultItemApplyInformation(applyRandomList)
				self.__AppendAffectInformation()

			if app.ELEMENT_SPELL_WORLDARD:
				self.__AppendBonusElement()

			self.__AppendAttributeInformation(attrSlot)

			if app.BL_67_ATTR:
				self.AppendAttribute6th7thPossibility(attrSlot)

			if app.ENABLE_RARITY:
				self.__SetRarityBar(itemVnum, metinSlot)

			self.AppendWearableInformation()

			if itemSubType != item.WEAPON_QUIVER:
				self.__AppendMetinSlotInfo(metinSlot)
			else:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
					
				if bHasRealtimeFlag == 1:
					self.AppendMallItemLastTime(metinSlot[0])

			#self.__AppendMetinSlotInfo(metinSlot)

		### Armor ###
		elif item.ITEM_TYPE_ARMOR == itemType:
			self.__AppendLimitInformation()
			if app.ENABLE_RARITY:
				self.__SetRarityType(itemVnum, metinSlot)

			## 방어력
			defGrade = item.GetValue(1)
			defBonus = item.GetValue(5)*2 ## 방어력 표시 잘못 되는 문제를 수정
			if defGrade > 0:
				self.AppendSpace(5)
				if app.ENABLE_RARITY:
					text = localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade+defBonus)
					if item.RARITY_TYPE_INDEX < len(metinSlot):
						rarityValue = item.GetRarityPoint(-4,metinSlot[item.RARITY_TYPE_INDEX])
						if rarityValue > 0:
							text+=" |cffFFFF95(+%d%%)"%rarityValue
					self.AppendTextLine(text, self.GetChangeTextLineColor(defGrade))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade+defBonus), self.GetChangeTextLineColor(defGrade))

			if app.ENABLE_RARITY:
				self.__AppendMagicDefenceInfo(0,metinSlot)
				self.__AppendAffectInformation(itemVnum,metinSlot)
			else:
				self.__AppendMagicDefenceInfo()
				self.__AppendAffectInformation()
			if app.ENABLE_APPLY_RANDOM:
				self.__AppendDefaultItemApplyInformation(applyRandomList)
			self.__AppendAttributeInformation(attrSlot)

			if app.BL_67_ATTR and itemSubType != item.ARMOR_PENDANT:
				self.AppendAttribute6th7thPossibility(attrSlot)

			if app.ENABLE_RARITY:
				self.__SetRarityBar(itemVnum, metinSlot)

			self.AppendWearableInformation()
			if search == 0:
				if itemSubType in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):				
					self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_ACCESSORY_MATERIAL_VNUM(itemVnum, itemSubType))
				else:
					self.__AppendMetinSlotInfo(metinSlot)

			if self.show_render == True:
				if itemSubType == item.ARMOR_BODY:
					self.interface.SetRenderDates(itemVnum,2)


		### Ring Slot Item (Not UNIQUE) ###
		elif item.ITEM_TYPE_RING == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			if app.ENABLE_APPLY_RANDOM:
				self.__AppendDefaultItemApplyInformation(applyRandomList)
			self.__AppendAttributeInformation(attrSlot)

			#반지 소켓 시스템 관련해선 아직 기획 미정
			#self.__AppendAccessoryMetinSlotInfo(metinSlot, 99001)


		### Belt Item ###
		elif item.ITEM_TYPE_BELT == itemType:
			
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			if app.ENABLE_APPLY_RANDOM:
				self.__AppendDefaultItemApplyInformation(applyRandomList)
			self.__AppendAttributeInformation(attrSlot)
			if search == 0:
				self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_BELT_MATERIAL_VNUM(itemVnum))

		## 코스츔 아이템 ##
		elif 0 != isCostumeItem:
			self.__AppendLimitInformation()

			if isCostumeAura:
				if app.ENABLE_AURA_SYSTEM:
					self.__AppendAffectInformationAura(window_type, slotIndex, metinSlot)
					self.__AppendAuraItemAffectInformation(itemVnum, window_type, slotIndex, metinSlot)
					self.__AppendAttributeInformationAura(window_type, slotIndex, attrSlot, metinSlot)
					self.__AppendAuraBoostMetinSlotInfo(itemVnum, window_type, slotIndex, metinSlot)
			elif isCostumeSash:
				if app.ENABLE_SASH_SYSTEM:
					self.__AppendAffectInformation()
					absChance = int(metinSlot[sash.ABSORPTION_SOCKET])
					self.AppendTextLine(localeInfo.SASH_ABSORB_CHANCE % (absChance), self.CONDITION_COLOR)
					if self.show_render == True:
						self.interface.SetRenderDates(itemVnum,4)

					itemAbsorbedVnum = int(metinSlot[sash.ABSORBED_SOCKET])
					if itemAbsorbedVnum:
						item.SelectItem(itemAbsorbedVnum)
						if item.GetItemType() == item.ITEM_TYPE_WEAPON:
							if item.GetItemSubType() == item.WEAPON_FAN:
								self.__AppendMagicAttackInfo(metinSlot[sash.ABSORPTION_SOCKET])
								item.SelectItem(itemAbsorbedVnum)
								self.__AppendAttackPowerInfo(metinSlot[sash.ABSORPTION_SOCKET])
							else:
								self.__AppendAttackPowerInfo(metinSlot[sash.ABSORPTION_SOCKET])
								item.SelectItem(itemAbsorbedVnum)
								self.__AppendMagicAttackInfo(metinSlot[sash.ABSORPTION_SOCKET])
						elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
							defGrade = item.GetValue(1)
							defBonus = item.GetValue(5) * 2
							defGrade = self.CalcSashValue(defGrade, metinSlot[sash.ABSORPTION_SOCKET])
							defBonus = self.CalcSashValue(defBonus, metinSlot[sash.ABSORPTION_SOCKET])

							if defGrade > 0:
								self.AppendSpace(5)
								self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))

							item.SelectItem(itemAbsorbedVnum)
							self.__AppendMagicDefenceInfo(metinSlot[sash.ABSORPTION_SOCKET])

						item.SelectItem(itemAbsorbedVnum)
						for i in xrange(item.ITEM_APPLY_MAX_NUM):
							(affectType, affectValue) = item.GetAffect(i)
							affectValue = self.CalcSashValue(affectValue, metinSlot[sash.ABSORPTION_SOCKET])
							affectString = self.__GetAffectString(affectType, affectValue)
							if affectString and affectValue > 0:
								self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

							item.SelectItem(itemAbsorbedVnum)
						# END EFFECT

						item.SelectItem(itemVnum)

						if app.ELEMENT_SPELL_WORLDARD:
							self.__AppendBonusElementSash(metinSlot[sash.ABSORPTION_SOCKET])

						## ATTR
						self.__AppendAttributeInformation(attrSlot, metinSlot[sash.ABSORPTION_SOCKET])
						# END ATTR

						if app.BL_67_ATTR:
							self.AppendAttribute6th7thPossibility(attrSlot)
					else:
						# ATTR
						self.__AppendAttributeInformation(attrSlot)
						if app.BL_67_ATTR:
							self.AppendAttribute6th7thPossibility(attrSlot)
						# END ATTR
			else:
				# self.__AppendAffectInformation()
				# self.__AppendAttributeInformation(attrSlot)

				self.__AppendAffectInformation()

				if app.ELEMENT_SPELL_WORLDARD:
					self.__AppendBonusElement()

				if app.ENABLE_SPECIAL_COSTUME_ATTR:
					self.__AppendAttributeInformation(attrSlot, 0, itemVnum)
				else:
					self.__AppendAttributeInformation(attrSlot)

				if self.show_render == True:
					if isCostumeHair != 0:
						self.interface.SetRenderDates(itemVnum, 3 ,item.GetValue(3))

					if isCostumeBody != 0:
						self.interface.SetRenderDates(itemVnum, 2)

					if isCostumeWeapon != 0:
						self.interface.SetRenderDates(itemVnum, 1)

					if isCostumeSkinSash != 0:
						self.interface.SetRenderDates(itemVnum, 4)

					if isCostumePet != 0 or isCostumeMount != 0:
						item.SelectItem(itemVnum)
						self.interface.SetRenderDates(item.GetValue(0), 5)

			self.AppendWearableInformation()
			bHasRealtimeFlag = 0
			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = 1

			if bHasRealtimeFlag == 1 and buff == 0:
				self.AppendMallItemLastTime(metinSlot[0])

		## Rod ##
		elif item.ITEM_TYPE_ROD == itemType:

			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendRodInformation(curLevel, curEXP, maxEXP)

		## Pick ##
		elif item.ITEM_TYPE_PICK == itemType:

			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendPickInformation(curLevel, curEXP, maxEXP)

		## Lottery ##
		elif item.ITEM_TYPE_LOTTERY == itemType:
			if 0 != metinSlot:

				ticketNumber = int(metinSlot[0])
				stepNumber = int(metinSlot[1])

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_LOTTERY_STEP_NUMBER % (stepNumber), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_LOTTO_NUMBER % (ticketNumber), self.NORMAL_COLOR);

		### Metin ###
		elif item.ITEM_TYPE_METIN == itemType:
			self.AppendMetinInformation()
			self.AppendMetinWearInformation()

		### Fish ###
		elif item.ITEM_TYPE_FISH == itemType:
			if 0 != metinSlot:
				self.__AppendFishInfo(metinSlot[0])

		## item.ITEM_TYPE_BLEND
		elif item.ITEM_TYPE_BLEND == itemType:
			self.__AppendLimitInformation()

			if metinSlot:
				affectType = metinSlot[0]
				affectValue = metinSlot[1]
				time = metinSlot[2]

				self.AppendSpace(5)
				affectText = self.__GetAffectString(affectType, affectValue)

				self.AppendTextLine(affectText, self.NORMAL_COLOR)

				if time > 0:
					minute = (time / 60)
					second = (time % 60)
					timeString = localeInfo.TOOLTIP_POTION_TIME

					if minute > 0:
						timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
					if second > 0:
						timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

					self.AppendTextLine(timeString)
			# 	else:
			# 		self.AppendTextLine(localeInfo.BLEND_POTION_NO_TIME)
			else:
				self.AppendTextLine(localeInfo.BLEND_POTION_NO_TIME)

		elif item.ITEM_TYPE_UNIQUE == itemType:

			if app.THANOS_GLOVE:
				if itemVnum >= 500001 and itemVnum <= 500006:
					self.__AppendLimitInformation()
					self.__AppendAffectInformation()
					self.__AppendAttributeInformation(attrSlot)

			if app.ENABLE_MULTI_FARM_BLOCK:
				if itemVnum>=55610 and itemVnum<=55615:
					self.AppendTextLine("Adding Time: (%s)"% localeInfo.SecondToDHM(item.GetValue(0)),self.SPECIAL_TITLE_COLOR)
					self.AppendTextLine("Increase Count: (+%d)" % item.GetValue(1), self.SPECIAL_TITLE_COLOR)
			if 0 != metinSlot:
				bHasRealtimeFlag = 0

				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if buff == 0:
					if 1 == bHasRealtimeFlag:
						self.AppendMallItemLastTime(metinSlot[0])
					else:
						time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

						if 1 == item.GetValue(2): ## 실시간 이용 Flag / 장착 안해도 준다
							self.AppendMallItemLastTime(time)
						else:
							self.AppendUniqueItemLastTime(time)

			if 71136 == itemVnum or 71143 == itemVnum or 71145 == itemVnum or 71146 == itemVnum or 71147 == itemVnum or 71169 == itemVnum or 71170 == itemVnum or 71173 == itemVnum:
				self.__AppendAffectInformation()

		### Use ###
		elif item.ITEM_TYPE_USE == itemType:
			self.__AppendLimitInformation()

			if app.ENABLE_LOCK_ATTR:
				if itemVnum == 50348 or itemVnum == 50349:
					attrIndex = 0
					try:
						attrIndex = int(metinSlot[0])
					except:
						attrIndex = 0
					self.AppendSpace(5)
					if 0 != attrIndex:
						self.AppendTextLine(localeInfo.LOCK_BONUS %attrIndex, self.SPECIAL_TITLE_COLOR)
					else:
						self.AppendTextLine(localeInfo.LOCK_BONUS2, self.SPECIAL_TITLE_COLOR)

			if app.ENABLE_COPY_ATTR_ITEM:
				if itemVnum == 77927:
					hasAttr = False
					for attr in attrSlot:
						if attr[0] > 0:
							hasAttr = True
							break
					if hasAttr:
						itemNames = {
							item.ITEM_TYPE_WEAPON : ["Weapon", [localeInfo.COPY_ITEM3,localeInfo.COPY_ITEM4,localeInfo.COPY_ITEM5,localeInfo.COPY_ITEM6,localeInfo.COPY_ITEM7,localeInfo.COPY_ITEM8]],
							item.ITEM_TYPE_ARMOR : ["Armor", [localeInfo.COPY_ITEM9,localeInfo.COPY_ITEM10,localeInfo.COPY_ITEM11,localeInfo.COPY_ITEM12,localeInfo.COPY_ITEM13,localeInfo.COPY_ITEM14,localeInfo.COPY_ITEM15]],
							item.ITEM_TYPE_COSTUME : ["Costume", [localeInfo.COPY_ITEM16,localeInfo.COPY_ITEM17,localeInfo.COPY_ITEM18,localeInfo.COPY_ITEM19,localeInfo.COPY_ITEM20,localeInfo.COPY_ITEM21,localeInfo.COPY_ITEM22,localeInfo.COPY_ITEM23,localeInfo.COPY_ITEM24]],
						}

						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.COPY_ITEM)
						self.AppendSpace(5)
						self.__AppendAttributeInformation(attrSlot)
						self.AppendSpace(5)
						
						try:
							self.AppendTextLine("[{}:{}]".format(itemNames[int(metinSlot[0])][0], itemNames[int(metinSlot[0])][1][int(metinSlot[1])]))
							self.AppendSpace(5)
						except:
							pass
						self.AppendTextLine(localeInfo.COPY_ITEM1)
					else:
						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.COPY_ITEM2)

			if app.ENABLE_SPECIAL_COSTUME_ATTR:
				if itemVnum >= 53998 and itemVnum <= 54500:
					if item.GetValue(0) != 0:
						self.AppendSpace(5)
						affectString = self.__GetAffectString(item.GetValue(0), item.GetValue(1))
						if affectString:
							affectColor = self.__GetAttributeColor(0, item.GetValue(1))
							self.AppendTextLine(affectString, affectColor)

						if player.IsGameMaster():
							bonusValueFlag = item.GetValue(2)
							bonusFlag = ["Body","Hair","Weapon","MountSkin","SashSkin","Effect"]
							flagText = ""
							for j in xrange(len(bonusFlag)):
								if constInfo.IS_SET(bonusValueFlag, 1 << j+1) or bonusValueFlag == 0:
									flagText+=", "+bonusFlag[j]
							self.AppendSpace(5)
							self.AppendTextLine("Flags: ["+flagText[2:]+"]", self.SPECIAL_TITLE_COLOR)

			if item.USE_POTION == itemSubType or item.USE_POTION_NODELAY == itemSubType:
				self.__AppendPotionInformation()

			elif item.USE_ABILITY_UP == itemSubType:
				self.__AppendAbilityPotionInformation()

			if (app.WJ_COMBAT_ZONE):
				if itemVnum in [50287, 50288, 50290]:
					if 0 != metinSlot:
						useCount = int(metinSlot[0])

						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % ((3 - useCount)), self.CONDITION_COLOR)
			## 영석 감지기
			if 27989 == itemVnum or 76006 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (6 - useCount), self.NORMAL_COLOR)

			## 이벤트 감지기
			elif 50004 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (10 - useCount), self.NORMAL_COLOR)

			## 자동물약
			elif constInfo.IS_AUTO_POTION(itemVnum):
				if 0 != metinSlot:
					## 0: 활성화, 1: 사용량, 2: 총량
					isActivated = int(metinSlot[0])
					usedAmount = float(metinSlot[1])
					totalAmount = float(metinSlot[2])

					if 0 == totalAmount:
						totalAmount = 1

					self.AppendSpace(5)

					if 0 != isActivated:
						self.AppendTextLine("(%s)" % (localeInfo.TOOLTIP_AUTO_POTION_USING), self.SPECIAL_POSITIVE_COLOR)
						self.AppendSpace(5)

					try:
						n = (100.0 - ((usedAmount / totalAmount) * 100.0))
						if app.ENABLE_NEW_AUTOPOTION:
							if constInfo.IS_NEW_AUTO_POTION(itemVnum):
								self.__AppendAffectInformation()
								
								bHasRealtimeFlag = 0
								for i in xrange(item.LIMIT_MAX_NUM):
									(limitType, limitValue) = item.GetLimit(i)
									if item.LIMIT_REAL_TIME == limitType:
										bHasRealtimeFlag = 1
									
								if bHasRealtimeFlag:
									self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(metinSlot[2]))
							else:
								self.AppendTextLine(localeInfo.TOOLTIP_AUTO_POTION_REST % float(n), self.POSITIVE_COLOR)
						else:
							self.AppendTextLine(localeInfo.TOOLTIP_AUTO_POTION_REST % float(n), self.POSITIVE_COLOR)
					except:
						pass

			## 귀환 기억부
			elif itemVnum in WARP_SCROLLS:
				if 0 != metinSlot:
					xPos = int(metinSlot[0])
					yPos = int(metinSlot[1])

					if xPos != 0 and yPos != 0:
						(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(xPos, yPos)

						localeMapName=localeInfo.MINIMAP_ZONE_NAME_DICT.get(mapName, "")

						self.AppendSpace(5)

						if localeMapName!="":
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION % (localeMapName, int(xPos-xBase)/100, int(yPos-yBase)/100), self.NORMAL_COLOR)
						else:
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION_ERROR % (int(xPos)/100, int(yPos)/100), self.NORMAL_COLOR)
							dbg.TraceError("NOT_EXIST_IN_MINIMAP_ZONE_NAME_DICT: %s" % mapName)

			#####
			if item.USE_SPECIAL == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)
					if app.ENABLE_NEW_AUTOPOTION and constInfo.IS_NEW_AUTO_POTION(itemVnum):
						break

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if buff == 0:
					## 있다면 관련 정보를 표시함. ex) 남은 시간 : 6일 6시간 58분
					if 1 == bHasRealtimeFlag:
						self.AppendMallItemLastTime(metinSlot[0])
					else:
						# ... 이거... 서버에는 이런 시간 체크 안되어 있는데...
						# 왜 이런게 있는지 알지는 못하나 그냥 두자...
						if 0 != metinSlot:
							time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

							## 실시간 이용 Flag
							if 1 == item.GetValue(2):
								self.AppendMallItemLastTime(time)

			elif item.USE_TIME_CHARGE_PER == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER(item.GetValue(0)))

				## 있다면 관련 정보를 표시함. ex) 남은 시간 : 6일 6시간 58분
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

			elif item.USE_TIME_CHARGE_FIX == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX(item.GetValue(0)))

				## 있다면 관련 정보를 표시함. ex) 남은 시간 : 6일 6시간 58분
				if 1 == bHasRealtimeFlag:
					self.AppendMallItemLastTime(metinSlot[0])

		elif item.ITEM_TYPE_QUEST == itemType:
			if itemVnum >= 53008 and itemVnum <= 53013 or itemVnum == 53001 or itemVnum == 53003 or itemVnum == 53017 or itemVnum == 53002 or itemVnum == 53007 or itemVnum == 53224 or itemVnum == 53225 or itemVnum == 53226 or itemVnum == 53227 or itemVnum == 53228 or itemVnum == 53229 or itemVnum == 53218 or itemVnum == 53219 or itemVnum == 53220 or itemVnum == 53221 or itemVnum == 53006 or itemVnum == 53030 or itemVnum == 53031 or itemVnum == 53032 or itemVnum == 53033 or itemVnum == 53034 or itemVnum == 53035 or itemVnum == 53036 or itemVnum == 53037 or itemVnum == 53038 or itemVnum == 53039 or itemVnum == 53040 or itemVnum == 53041 or itemVnum == 53042 or itemVnum == 53043 or itemVnum == 53044 or itemVnum == 53045 or itemVnum == 53046 or itemVnum == 53047 or itemVnum == 53048 or itemVnum == 53049 or itemVnum == 53050 or itemVnum == 53051 or itemVnum == 53052 or itemVnum == 53053 or itemVnum == 53054 or itemVnum == 53055 or itemVnum == 53056 or itemVnum == 53057 or itemVnum == 53058 or itemVnum == 53058 or itemVnum == 53060 or itemVnum == 53061 or itemVnum == 53062 or itemVnum == 53063 or itemVnum == 53064 or itemVnum == 53260 or itemVnum == 53261:
				self.__AppendAffectInformation()
			if app.__RENEWAL_CRYSTAL__:
				if itemVnum >= 51010 and itemVnum <= 51035:
					self.__AppendAttributeInformation(attrSlot, 0, itemVnum)
					self.AppendCrystalLastTime(metinSlot[1] if metinSlot[1] > 60 * 60 * 24 * 7 else metinSlot[1] + app.GetGlobalTimeStamp())

			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)
				if search == 0 or buff == 0:
					if item.LIMIT_REAL_TIME == limitType:
						self.AppendMallItemLastTime(metinSlot[0])

			if itemVnum >= 71124 and itemVnum <= 71128 or itemVnum >= 71131 and itemVnum <= 71134 or itemVnum >= 71171 and itemVnum <= 71172 or itemVnum >= 71176 and itemVnum <= 71177 or itemVnum >= 71166 and itemVnum <= 71192 or itemVnum >= 71193 or itemVnum >= 71114 or itemVnum >= 71115 or itemVnum >= 71116 or itemVnum >= 71117 or itemVnum >= 71222 or itemVnum >= 71223 or itemVnum >= 71224 or itemVnum >= 71225 or itemVnum >= 71226 or itemVnum >= 71227 or itemVnum >= 71228 or itemVnum >= 71229 or itemVnum >= 71231 or itemVnum >= 71232 or itemVnum >= 71233 or itemVnum >= 71234 or itemVnum >= 71235 or itemVnum >= 71236 or itemVnum >= 71242 or itemVnum >= 71243 or itemVnum >= 71244 or itemVnum >= 71245 or itemVnum >= 71246 or itemVnum >= 71247 or itemVnum >= 71248 or itemVnum >= 71249 or itemVnum >= 71250 or itemVnum >= 71251 or itemVnum >= 71252:
				self.__AppendAffectInformation()
			
		
		elif item.ITEM_TYPE_GIFTBOX == itemType and app.ENABLE_SHOW_CHEST_DROP:
			self.AppendChestDropInfo(itemVnum, player.GetItemCount(window_type, slotIndex))

		elif item.ITEM_TYPE_DS == itemType:
			self.AppendTextLine(self.__DragonSoulInfoString(itemVnum))
			self.__AppendAttributeInformation(attrSlot)
		else:
			self.__AppendLimitInformation()
		
		
		
		# if app.ENABLE_FEATURES_REFINE_SYSTEM:
			# if itemVnum in (player.REFINE_VNUM_POTION_LOW, player.REFINE_VNUM_POTION_MEDIUM, player.REFINE_VNUM_POTION_EXTRA):

				# self.DESCRIPTION_VNUMS = [
					# localeInfo.REFINE_TOOLTIP_ITEM_DESCRIPTION_1,
					# localeInfo.REFINE_TOOLTIP_ITEM_DESCRIPTION_2,
					# localeInfo.REFINE_TOOLTIP_ITEM_DESCRIPTION_3,
					# localeInfo.REFINE_TOOLTIP_ITEM_DESCRIPTION_4
				# ]
				
				# self.PERCENTAGE_VNUMS = {
					# player.REFINE_VNUM_POTION_LOW : player.REFINE_PERCENTAGE_LOW,
					# player.REFINE_VNUM_POTION_MEDIUM : player.REFINE_PERCENTAGE_MEDIUM,
					# player.REFINE_VNUM_POTION_EXTRA : player.REFINE_PERCENTAGE_EXTRA
				# }
				
				# self.COLORS = [
					# self.NORMAL_COLOR, self.SPECIAL_POSITIVE_COLOR, self.DISABLE_COLOR, self.HIGH_PRICE_COLOR
				# ]
					
				# self.AppendSpace(5)

				# for it in xrange(len(self.DESCRIPTION_VNUMS) - 1):
					# self.AppendDescription(self.DESCRIPTION_VNUMS[it], None, self.COLORS[it])
				# self.AppendDescription(self.DESCRIPTION_VNUMS[3] % (self.PERCENTAGE_VNUMS[itemVnum]), None, self.COLORS[3])

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)
			#dbg.TraceError("LimitType : %d, limitValue : %d" % (limitType, limitValue))

			if item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
				self.AppendRealTimeStartFirstUseLastTime(item, metinSlot, i)
				#dbg.TraceError("2) REAL_TIME_START_FIRST_USE flag On ")

			elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
				self.AppendTimerBasedOnWearLastTime(metinSlot)
				#dbg.TraceError("1) REAL_TIME flag On ")

		self.__AppendSealInformation(window_type, slotIndex) ## cyh itemseal 2013 11 11
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if self.show_render == True:
				if interface.IsRenderTooltip():
					self.AppendSpace(5)
					self.AppendTextLine("|Eemoji/key_alt|e - Visualizar")
			# 1 = inventory
			if self.emoji_safebox == 1 and interface.SafeboxIsShow():
				self.AppendSpace(5)
				self.AppendTextLine("|Eemoji/key_ctrl|e + |Eemoji/key_lclick|e - Almacen")
			# 2 = safebox
			if self.emoji_safebox == 2 and interface.SafeboxIsShow():
				self.AppendSpace(5)
				self.AppendTextLine("|Eemoji/key_ctrl|e + |Eemoji/key_lclick|e - Inventario")

		self.ShowSafeboxEmoji(0)


		AFDict = {
				"|Eemoji/anti_drop|e": item.IsAntiFlag(item.ITEM_ANTIFLAG_DROP),
				"|Eemoji/anti_sell|e": item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL),
				"|Eemoji/anti_give|e": item.IsAntiFlag(item.ITEM_ANTIFLAG_GIVE),
				"|Eemoji/anti_stack|e": item.IsAntiFlag(item.ITEM_ANTIFLAG_STACK),
				"|Eemoji/anti_shop|e": item.IsAntiFlag(item.ITEM_ANTIFLAG_MYSHOP),
				"|Eemoji/anti_safebox|e": item.IsAntiFlag(item.ITEM_ANTIFLAG_SAFEBOX),
			}

		AFNames = [name for name, flag in AFDict.iteritems() if flag]

		if AFNames:

			self.AppendSpace(5)
			# AFTitle = self.AppendTextLine("[ " + localeInfo.NOT_POSSIBLE + " ]", self.DISABLE_COLOR)
			AFLine = self.AppendTextLine('{}'.format(' '.join(AFNames)), self.DISABLE_COLOR)

			# AFTitle.SetFeather()
			AFLine.SetFeather()

		#self.show_render = True
		if app.ENABLE_MINI_GAME_CATCH_KING:
			if self.itemVnum in [79603, 79604]:
				if 0 != metinSlot[0]:
					self.AppendMallItemLastTime(metinSlot[0])

		self.ShowToolTip()
		
		if app.ENABLE_RENDER_TARGET:
			self.__AppendRenderTarget(itemVnum)

	def FuncListBlend(self):
		info = [
		#Vnum - IdBonus -ValuesBonus
		[51003,1,5,2],
		[51004,1,5,2],
		[51005,1,5,2],
		[51006,1,5,3],
		[51007,1,5,3],

		]

		return info

	if app.ENABLE_SHOW_CHEST_DROP:
		def AppendChestDropInfo(self, itemVnum, itemCount = 0):
			if itemCount <= 1:
				self.AppendSpace(5)
				self.AppendTextLine("|Eemoji/key_ctrl|e + |Eemoji/key_rclick|e - "+localeInfo.CHEST_TOOLTIP_TEXT, self.NORMAL_COLOR)
				return
			self.AppendSpace(5)
			self.AppendTextLine("|Eemoji/key_ctrl|e + |Eemoji/key_rclick|e - "+localeInfo.CHEST_TOOLTIP_TEXT, self.NORMAL_COLOR)
			self.AppendSpace(5)
			self.AppendTextLine("|Eemoji/key_ctrl|e + |Eemoji/key_z|e + |Eemoji/key_rclick|e - "+localeInfo.CHEST_TOOLTIP_TEXT_OPEN, self.NORMAL_COLOR)

	def FuncBlendGet(self,vnum):
		list_get = self.FuncListBlend()

		for i in xrange(0,len(list_get)):
			if vnum == list_get[i][0]:
				return True

		return False

	def FuncBlendGetIDBonus(self,vnum):
		list_get = self.FuncListBlend()

		for i in xrange(0,len(list_get)):
			if vnum == list_get[i][1]:
				return list_get[i][1]

	def FuncBlendGetValueBonus(self,vnum):
		list_get = self.FuncListBlend()

		for i in xrange(0,len(list_get)):
			if vnum == list_get[i][2]:
				return list_get[i][2]

	def FuncBlendGetTime(self,vnum):
		list_get = self.FuncListBlend()

		for i in xrange(0,len(list_get)):
			if vnum == list_get[i][3]:
				return list_get[i][3]

	def __DragonSoulInfoString (self, dwVnum):
		step = (dwVnum / 100) % 10
		refine = (dwVnum / 10) % 10
		if 0 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL1 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 1 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL2 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 2 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL3 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 3 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL4 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		elif 4 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL5 + " " + localeInfo.DRAGON_SOUL_STRENGTH(refine)
		else:
			return ""


	## 헤어인가?
	def __IsHair(self, itemVnum):
		return (self.__IsOldHair(itemVnum) or
			self.__IsNewHair(itemVnum) or
			self.__IsNewHair2(itemVnum) or
			self.__IsNewHair3(itemVnum) or
			self.__IsCostumeHair(itemVnum)
			)

	def __IsOldHair(self, itemVnum):
		return itemVnum > 73000 and itemVnum < 74000

	def __IsNewHair(self, itemVnum):
		return itemVnum > 74000 and itemVnum < 75000

	def __IsNewHair2(self, itemVnum):
		return itemVnum > 75000 and itemVnum < 76000

	def __IsNewHair3(self, itemVnum):
		return ((74012 < itemVnum and itemVnum < 74022) or
			(74262 < itemVnum and itemVnum < 74272) or
			(74512 < itemVnum and itemVnum < 74522) or
			(74544 < itemVnum and itemVnum < 74560) or
			(74762 < itemVnum and itemVnum < 74772) or
			(45000 < itemVnum and itemVnum < 47000))

	def __IsCostumeHair(self, itemVnum):
		return app.ENABLE_COSTUME_SYSTEM and self.__IsNewHair3(itemVnum - 100000)

	def __AppendSearchIcon(self, itemVnum):
		item.SelectItem(itemVnum)

		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()

		itemImage.LoadImage(item.GetIconImageFileName())

		itemImage.SetPosition(itemImage.GetWidth()/2+60, self.toolTipHeight)
		self.toolTipHeight += itemImage.GetHeight()
		self.childrenList.append(itemImage)
		self.ResizeToolTip()

	def __AppendHairIcon(self, itemVnum):
		if itemVnum >=46001 and itemVnum <= 46014:
			return

		imageFolder = ""
		if self.__IsOldHair(itemVnum):
			imageFolder = "d:/ymir work/item/quest/"+str(itemVnum)+".tga"
		elif self.__IsNewHair3(itemVnum):
			imageFolder = "icon/hair/%d.sub" % (itemVnum)
		elif self.__IsNewHair(itemVnum): # 기존 헤어 번호를 연결시켜서 사용한다. 새로운 아이템은 1000만큼 번호가 늘었다.
			imageFolder = "d:/ymir work/item/quest/"+str(itemVnum-1000)+".tga"
		elif self.__IsNewHair2(itemVnum):
			imageFolder = "icon/hair/%d.sub" % (itemVnum)
		elif self.__IsCostumeHair(itemVnum):
			imageFolder = "icon/hair/%d.sub" % (itemVnum - 100000)

		if not pack.Exist(imageFolder) or imageFolder == "":
			return

		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.LoadImage(imageFolder)
		itemImage.Show()

		itemImage.SetPosition(itemImage.GetWidth()/2, self.toolTipHeight)
		self.toolTipHeight += itemImage.GetHeight()
		#self.toolTipWidth += itemImage.GetWidth()/2
		self.childrenList.append(itemImage)
		self.ResizeToolTip()

	## 사이즈가 큰 Description 일 경우 툴팁 사이즈를 조정한다
	def __AdjustMaxWidth(self, attrSlot, desc):
		newToolTipWidth = self.toolTipWidth
		newToolTipWidth = max(self.__AdjustAttrMaxWidth(attrSlot), newToolTipWidth)
		newToolTipWidth = max(self.__AdjustDescMaxWidth(desc), newToolTipWidth)
		if newToolTipWidth > self.toolTipWidth:
			self.toolTipWidth = newToolTipWidth
			self.ResizeToolTip()

	def __AdjustAttrMaxWidth(self, attrSlot):
		if 0 == attrSlot:
			return self.toolTipWidth

		maxWidth = self.toolTipWidth
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			value = attrSlot[i][1]
			if self.ATTRIBUTE_NEED_WIDTH.has_key(type):
				if value > 0:
					maxWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], maxWidth)

					# ATTR_CHANGE_TOOLTIP_WIDTH
					#self.toolTipWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], self.toolTipWidth)
					#self.ResizeToolTip()
					# END_OF_ATTR_CHANGE_TOOLTIP_WIDTH

		return maxWidth

	def __AdjustDescMaxWidth(self, desc):
		if len(desc) < DESC_DEFAULT_MAX_COLS:
			return self.toolTipWidth

		return DESC_WESTERN_MAX_WIDTH

	def __SetSkillBookToolTip(self, skillIndex, bookName, skillGrade):
		skillName = skill.GetSkillName(skillIndex)

		if not skillName:
			return

		if localeInfo.IsVIETNAM():
			itemName = bookName + " " + skillName
		else:
			itemName = skillName + " " + bookName
		self.SetTitle(itemName)

	def __AppendPickInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE3, self.NORMAL_COLOR)


	def __AppendRodInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE3, self.NORMAL_COLOR)

	def __AppendLimitInformation(self):

		appendSpace = False

		for i in xrange(item.LIMIT_MAX_NUM):

			(limitType, limitValue) = item.GetLimit(i)

			if limitValue > 0:
				if False == appendSpace:
					self.AppendSpace(5)
					appendSpace = True

			else:
				continue

			if item.LIMIT_LEVEL == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.LEVEL), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (limitValue), color)
			"""
			elif item.LIMIT_STR == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.ST), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_STR % (limitValue), color)
			elif item.LIMIT_DEX == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.DX), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_DEX % (limitValue), color)
			elif item.LIMIT_INT == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.IQ), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_INT % (limitValue), color)
			elif item.LIMIT_CON == limitType:
				color = self.GetLimitTextLineColor(player.GetStatus(player.HT), limitValue)
				self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_CON % (limitValue), color)
			"""

	## cyh itemseal 2013 11 11
	def __AppendSealInformation(self, window_type, slotIndex):
		if not app.ENABLE_SOULBIND_SYSTEM:
			return

		itemSealDate = player.GetItemSealDate(window_type, slotIndex)
		if itemSealDate == item.GetDefaultSealDate():
			return

		if itemSealDate == item.GetUnlimitedSealDate():
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_SEALED, self.NEGATIVE_COLOR)

		elif itemSealDate > 0:
			self.AppendSpace(5)
			hours, minutes = player.GetItemUnSealLeftTime(window_type, slotIndex)
			self.AppendTextLine(localeInfo.TOOLTIP_UNSEAL_LEFT_TIME % (hours, minutes), self.NEGATIVE_COLOR)

	def __GetAffectString(self, affectType, affectValue):
		if 0 == affectType:
			return None

		if 0 == affectValue:
			return None

		if app.ENABLE_APPLY_RANDOM:
			if affectType == item.APPLY_RANDOM_NEW:
				return None

		if affectType == item.APPLY_RANDOM:
			return None

		try:
			return self.AFFECT_DICT[affectType](affectValue)
		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)


	if app.ENABLE_RARITY:
		def __AppendAffectInformation(self, itemVnum = 0, metinSlot = []):
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					if item.IsRarityItem(itemVnum) and len(metinSlot) > 0:
						if item.RARITY_TYPE_INDEX < len(metinSlot):
							rarityValue = item.GetRarityPoint(affectType,metinSlot[item.RARITY_TYPE_INDEX])
							if rarityValue > 0:
								affectString+=" |cffFFFF95(+%d%%)"%rarityValue

					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
	else:
		def __AppendAffectInformation(self):
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendWearableInformation(self):

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)

		flagList = (
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
			not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN))
		if app.ENABLE_WOLFMAN_CHARACTER:
			flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)
		characterNames = ""
		for i in xrange(self.CHARACTER_COUNT):

			name = self.CHARACTER_NAMES[i]
			flag = flagList[i]

			if flag:
				characterNames += " "
				characterNames += name

		textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
		textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
			textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
			textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
			textLine.SetFeather()

	def __AppendPotionInformation(self):
		self.AppendSpace(5)

		healHP = item.GetValue(0)
		healSP = item.GetValue(1)
		healStatus = item.GetValue(2)
		healPercentageHP = item.GetValue(3)
		healPercentageSP = item.GetValue(4)

		if healHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_POINT % healHP, self.GetChangeTextLineColor(healHP))
		if healSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_POINT % healSP, self.GetChangeTextLineColor(healSP))
		if healStatus != 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_CURE)
		if healPercentageHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_PERCENT % healPercentageHP, self.GetChangeTextLineColor(healPercentageHP))
		if healPercentageSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_PERCENT % healPercentageSP, self.GetChangeTextLineColor(healPercentageSP))

	def __AppendAbilityPotionInformation(self):

		self.AppendSpace(5)

		abilityType = item.GetValue(0)
		time = item.GetValue(1)
		point = item.GetValue(2)

		if abilityType == item.APPLY_ATT_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_ATTACK_SPEED % point, self.GetChangeTextLineColor(point))
		elif abilityType == item.APPLY_MOV_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_MOVING_SPEED % point, self.GetChangeTextLineColor(point))

		if time > 0:
			minute = (time / 60)
			second = (time % 60)
			timeString = localeInfo.TOOLTIP_POTION_TIME

			if minute > 0:
				timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
			if second > 0:
				timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

			self.AppendTextLine(timeString)

	def GetPriceColor(self, price):
		if price>=constInfo.HIGH_PRICE:
			return self.HIGH_PRICE_COLOR
		if price>=constInfo.MIDDLE_PRICE:
			return self.MIDDLE_PRICE_COLOR
		else:
			return self.LOW_PRICE_COLOR

	def AppendPrice(self, price):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))

	def AppendPriceBySecondaryCoin(self, price):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToSecondaryCoinString(price)), self.GetPriceColor(price))

	def AppendSellingPrice(self, price):
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL):
			self.AppendTextLine(localeInfo.TOOLTIP_ANTI_SELL, self.DISABLE_COLOR)
			self.AppendSpace(5)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_SELLPRICE % (localeInfo.NumberToMoneyString(price)), self.GetPriceColor(price))
			self.AppendSpace(5)

	def AppendMetinInformation(self):
		if constInfo.ENABLE_FULLSTONE_DETAILS:
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					self.AppendSpace(5)
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendMetinWearInformation(self):

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SOCKET_REFINABLE_ITEM, self.NORMAL_COLOR)

		flagList = (item.IsWearableFlag(item.WEARABLE_BODY),
					item.IsWearableFlag(item.WEARABLE_HEAD),
					item.IsWearableFlag(item.WEARABLE_FOOTS),
					item.IsWearableFlag(item.WEARABLE_WRIST),
					item.IsWearableFlag(item.WEARABLE_WEAPON),
					item.IsWearableFlag(item.WEARABLE_NECK),
					item.IsWearableFlag(item.WEARABLE_EAR),
					item.IsWearableFlag(item.WEARABLE_UNIQUE),
					item.IsWearableFlag(item.WEARABLE_SHIELD),
					item.IsWearableFlag(item.WEARABLE_ARROW))

		wearNames = ""
		for i in xrange(self.WEAR_COUNT):

			name = self.WEAR_NAMES[i]
			flag = flagList[i]

			if flag:
				wearNames += "  "
				wearNames += name

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
		textLine.SetHorizontalAlignCenter()
		textLine.SetPackedFontColor(self.NORMAL_COLOR)
		textLine.SetText(wearNames)
		textLine.Show()
		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

	def GetMetinSocketType(self, number):
		if player.METIN_SOCKET_TYPE_NONE == number:
			return player.METIN_SOCKET_TYPE_NONE
		elif player.METIN_SOCKET_TYPE_SILVER == number:
			return player.METIN_SOCKET_TYPE_SILVER
		elif player.METIN_SOCKET_TYPE_GOLD == number:
			return player.METIN_SOCKET_TYPE_GOLD
		else:
			item.SelectItem(number)
			if item.METIN_NORMAL == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_SILVER
			elif item.METIN_GOLD == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_GOLD
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_RING_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_BELT_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER

		return player.METIN_SOCKET_TYPE_NONE

	def GetMetinItemIndex(self, number):
		if player.METIN_SOCKET_TYPE_SILVER == number:
			return 0
		if player.METIN_SOCKET_TYPE_GOLD == number:
			return 0

		return number

	def __AppendAccessoryMetinSlotInfo(self, metinSlot, mtrlVnum):
		ACCESSORY_SOCKET_MAX_SIZE = 3

		cur=min(metinSlot[0], ACCESSORY_SOCKET_MAX_SIZE)
		end=min(metinSlot[1], ACCESSORY_SOCKET_MAX_SIZE)

		affectType1, affectValue1 = item.GetAffect(0)
		affectList1=[0, max(1, affectValue1*10/100), max(2, affectValue1*20/100), max(3, affectValue1*40/100)]

		affectType2, affectValue2 = item.GetAffect(1)
		affectList2=[0, max(1, affectValue2*10/100), max(2, affectValue2*20/100), max(3, affectValue2*40/100)]

		affectType3, affectValue3 = item.GetAffect(2)
		affectList3=[0, max(1, affectValue3*10/100), max(2, affectValue3*20/100), max(3, affectValue3*40/100)]

		mtrlPos=0
		mtrlList=[mtrlVnum]*cur+[player.METIN_SOCKET_TYPE_SILVER]*(end-cur)
		for mtrl in mtrlList:
			affectString1 = self.__GetAffectString(affectType1, affectList1[mtrlPos+1]-affectList1[mtrlPos])
			affectString2 = self.__GetAffectString(affectType2, affectList2[mtrlPos+1]-affectList2[mtrlPos])
			affectString3 = self.__GetAffectString(affectType3, affectList3[mtrlPos+1]-affectList3[mtrlPos])

			leftTime = 0
			if cur == mtrlPos+1:
				leftTime=metinSlot[2]

			self.__AppendMetinSlotInfo_AppendMetinSocketData(mtrlPos, mtrl, affectString1, affectString2, affectString3, leftTime)
			mtrlPos+=1

	def __AppendMetinSlotInfo(self, metinSlot):
		if self.__AppendMetinSlotInfo_IsEmptySlotList(metinSlot):
			return

		if app.ENABLE_RARITY:
			for i in xrange(player.METIN_SOCKET_MAX_NUM_EX):
				self.__AppendMetinSlotInfo_AppendMetinSocketData(i, metinSlot[i])
		else:
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				self.__AppendMetinSlotInfo_AppendMetinSocketData(i, metinSlot[i])

	def __AppendMetinSlotInfo_IsEmptySlotList(self, metinSlot):
		if 0 == metinSlot:
			return 1

		if app.ENABLE_RARITY:
			for i in xrange(player.METIN_SOCKET_MAX_NUM_EX):
				metinSlotData=metinSlot[i]
				if 0 != self.GetMetinSocketType(metinSlotData):
					if 0 != self.GetMetinItemIndex(metinSlotData):
						return 0
		else:
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlotData=metinSlot[i]
				if 0 != self.GetMetinSocketType(metinSlotData):
					if 0 != self.GetMetinItemIndex(metinSlotData):
						return 0
		return 1

	def __AppendMetinSlotInfo_AppendMetinSocketData(self, index, metinSlotData, custumAffectString="", custumAffectString2="", custumAffectString3="", leftTime=0):

		slotType = self.GetMetinSocketType(metinSlotData)
		itemIndex = self.GetMetinItemIndex(metinSlotData)

		if 0 == slotType:
			return

		self.AppendSpace(5)

		slotImage = ui.ImageBox()
		slotImage.SetParent(self)
		slotImage.Show()

		## Name
		nameTextLine = ui.TextLine()
		nameTextLine.SetParent(self)
		nameTextLine.SetFontName(self.defFontName)
		nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
		nameTextLine.SetOutline()
		nameTextLine.SetFeather()
		nameTextLine.Show()

		self.childrenList.append(nameTextLine)

		if player.METIN_SOCKET_TYPE_SILVER == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
		elif player.METIN_SOCKET_TYPE_GOLD == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")

		self.childrenList.append(slotImage)

		if localeInfo.IsARABIC():
			slotImage.SetPosition(self.toolTipWidth - slotImage.GetWidth() - 9, self.toolTipHeight-1)
			nameTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 2)
		else:
			slotImage.SetPosition(9, self.toolTipHeight-1)
			nameTextLine.SetPosition(50, self.toolTipHeight + 2)

		metinImage = ui.ImageBox()
		metinImage.SetParent(self)
		metinImage.Show()
		self.childrenList.append(metinImage)

		if itemIndex:

			item.SelectItem(itemIndex)

			## Image
			try:
				metinImage.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" %
					(itemIndex, item.GetIconImageFileName())
				)

			nameTextLine.SetText(item.GetItemName())

			## Affect
			affectTextLine = ui.TextLine()
			affectTextLine.SetParent(self)
			affectTextLine.SetFontName(self.defFontName)
			affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
			affectTextLine.SetOutline()
			affectTextLine.SetFeather()
			affectTextLine.Show()

			if localeInfo.IsARABIC():
				metinImage.SetPosition(self.toolTipWidth - metinImage.GetWidth() - 10, self.toolTipHeight)
				affectTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2)
			else:
				metinImage.SetPosition(10, self.toolTipHeight)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

			if custumAffectString:
				affectTextLine.SetText(custumAffectString)
			elif itemIndex!=constInfo.ERROR_METIN_STONE:
				affectType, affectValue = item.GetAffect(0)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					affectTextLine.SetText(affectString)
			else:
				affectTextLine.SetText(localeInfo.TOOLTIP_APPLY_NOAFFECT)

			self.childrenList.append(affectTextLine)

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString2) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString2 = self.__GetAffectString(*item.GetAffect(1))

			if custumAffectString2:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString2)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString3) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString3 = self.__GetAffectString(*item.GetAffect(2))

			if custumAffectString3:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString3)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

			if 0 != leftTime:
				timeText = (localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftTime))

				timeTextLine = ui.TextLine()
				timeTextLine.SetParent(self)
				timeTextLine.SetFontName(self.defFontName)
				timeTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				timeTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				timeTextLine.SetOutline()
				timeTextLine.SetFeather()
				timeTextLine.Show()
				timeTextLine.SetText(timeText)
				self.childrenList.append(timeTextLine)
				self.toolTipHeight += 16 + 2

		else:
			nameTextLine.SetText(localeInfo.TOOLTIP_SOCKET_EMPTY)

		self.toolTipHeight += 35
		self.ResizeToolTip()

	def __AppendFishInfo(self, size):
		try:
			size = int(size)
			if size > 0:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_FISH_LEN % (float(size) / 100.0), self.NORMAL_COLOR)
		except:
			pass

	def AppendUniqueItemLastTime(self, restMin):
		restSecond = restMin*60
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(restSecond), self.NORMAL_COLOR)

	def AppendMallItemLastTime(self, endTime):
		leftSec = max(0, endTime - app.GetGlobalTimeStamp())
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(leftSec), self.NORMAL_COLOR)

	def AppendTimerBasedOnWearLastTime(self, metinSlot):
		if 0 == metinSlot[0]:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.CANNOT_USE, self.DISABLE_COLOR)
		else:
			endTime = app.GetGlobalTimeStamp() + metinSlot[0]
			self.AppendMallItemLastTime(endTime)

	def AppendRealTimeStartFirstUseLastTime(self, item, metinSlot, limitIndex):
		useCount = metinSlot[1]
		endTime = metinSlot[0]

		# 한 번이라도 사용했다면 Socket0에 종료 시간(2012년 3월 1일 13시 01분 같은..) 이 박혀있음.
		# 사용하지 않았다면 Socket0에 이용가능시간(이를테면 600 같은 값. 초단위)이 들어있을 수 있고, 0이라면 Limit Value에 있는 이용가능시간을 사용한다.
		if 0 == useCount:
			if 0 == endTime:
				(limitType, limitValue) = item.GetLimit(limitIndex)
				endTime = limitValue

			endTime += app.GetGlobalTimeStamp()

		self.AppendMallItemLastTime(endTime)
	if app.ENABLE_SASH_SYSTEM:
		def SetSashResultItem(self, slotIndex, window_type = player.INVENTORY):
			(itemVnum, MinAbs, MaxAbs) = sash.GetResultItem()
			if not itemVnum:
				return
			
			self.ClearToolTip()
			
			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			
			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_SASH:
				return
			
			absChance = MaxAbs
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnum, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			self.__AppendLimitInformation()
			
			## ABSORPTION RATE
			if MinAbs == MaxAbs:
				self.AppendTextLine(localeInfo.SASH_ABSORB_CHANCE % (MinAbs), self.CONDITION_COLOR)
			else:
				self.AppendTextLine(localeInfo.SASH_ABSORB_CHANCE2 % (MinAbs, MaxAbs), self.CONDITION_COLOR)
			## END ABSOPRTION RATE
			
			itemAbsorbedVnum = int(metinSlot[sash.ABSORBED_SOCKET])
			if itemAbsorbedVnum:
				## ATTACK / DEFENCE
				item.SelectItem(itemAbsorbedVnum)
				if item.GetItemType() == item.ITEM_TYPE_WEAPON:
					if item.GetItemSubType() == item.WEAPON_FAN:
						self.__AppendMagicAttackInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendAttackPowerInfo(absChance)
					else:
						self.__AppendAttackPowerInfo(absChance)
						item.SelectItem(itemAbsorbedVnum)
						self.__AppendMagicAttackInfo(absChance)
				elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
					defGrade = item.GetValue(1)
					defBonus = item.GetValue(5) * 2
					defGrade = self.CalcSashValue(defGrade, absChance)
					defBonus = self.CalcSashValue(defBonus, absChance)
					
					if defGrade > 0:
						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
					
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicDefenceInfo(absChance)
				## END ATTACK / DEFENCE
				
				## EFFECT
				item.SelectItem(itemAbsorbedVnum)
				for i in xrange(item.ITEM_APPLY_MAX_NUM):
					(affectType, affectValue) = item.GetAffect(i)
					affectValue = self.CalcSashValue(affectValue, absChance)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString and affectValue > 0:
						self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
					
					item.SelectItem(itemAbsorbedVnum)
				# END EFFECT
				
			item.SelectItem(itemVnum)
			## ATTR
			self.__AppendAttributeInformation(attrSlot, MaxAbs)
			# END ATTR
			
			self.AppendWearableInformation()
			self.ShowToolTip()

		def SetSashResultAbsItem(self, slotIndex1, slotIndex2, window_type = player.INVENTORY):
			itemVnumSash = player.GetItemIndex(window_type, slotIndex1)
			itemVnumTarget = player.GetItemIndex(window_type, slotIndex2)
			if not itemVnumSash or not itemVnumTarget:
				return
			
			self.ClearToolTip()
			
			item.SelectItem(itemVnumSash)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()
			if itemType != item.ITEM_TYPE_COSTUME and itemSubType != item.COSTUME_TYPE_SASH:
				return
			
			metinSlot = [player.GetItemMetinSocket(window_type, slotIndex1, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(window_type, slotIndex2, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			
			itemDesc = item.GetItemDescription()
			self.__AdjustMaxWidth(attrSlot, itemDesc)
			self.__SetItemTitle(itemVnumSash, metinSlot, attrSlot)
			self.AppendDescription(itemDesc, 26)
			self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
			item.SelectItem(itemVnumSash)
			self.__AppendLimitInformation()
			
			## ABSORPTION RATE
			self.AppendTextLine(localeInfo.SASH_ABSORB_CHANCE % (metinSlot[sash.ABSORPTION_SOCKET]), self.CONDITION_COLOR)
			## END ABSOPRTION RATE
			
			## ATTACK / DEFENCE
			itemAbsorbedVnum = itemVnumTarget
			item.SelectItem(itemAbsorbedVnum)
			if item.GetItemType() == item.ITEM_TYPE_WEAPON:
				if item.GetItemSubType() == item.WEAPON_FAN:
					self.__AppendMagicAttackInfo(metinSlot[sash.ABSORPTION_SOCKET])
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendAttackPowerInfo(metinSlot[sash.ABSORPTION_SOCKET])
				else:
					self.__AppendAttackPowerInfo(metinSlot[sash.ABSORPTION_SOCKET])
					item.SelectItem(itemAbsorbedVnum)
					self.__AppendMagicAttackInfo(metinSlot[sash.ABSORPTION_SOCKET])
			elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
				defGrade = item.GetValue(1)
				defBonus = item.GetValue(5) * 2
				defGrade = self.CalcSashValue(defGrade, metinSlot[sash.ABSORPTION_SOCKET])
				defBonus = self.CalcSashValue(defBonus, metinSlot[sash.ABSORPTION_SOCKET])
				
				if defGrade > 0:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade + defBonus), self.GetChangeTextLineColor(defGrade))
				
				item.SelectItem(itemAbsorbedVnum)
				self.__AppendMagicDefenceInfo(metinSlot[sash.ABSORPTION_SOCKET])
			## END ATTACK / DEFENCE
			
			## EFFECT
			item.SelectItem(itemAbsorbedVnum)
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				affectValue = self.CalcSashValue(affectValue, metinSlot[sash.ABSORPTION_SOCKET])
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString and affectValue > 0:
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))
				
				item.SelectItem(itemAbsorbedVnum)
			## END EFFECT
			
			## ATTR
			item.SelectItem(itemAbsorbedVnum)
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				type = attrSlot[i][0]
				value = attrSlot[i][1]
				if not value:
					continue
				
				value = self.CalcSashValue(value, metinSlot[sash.ABSORPTION_SOCKET])
				affectString = self.__GetAffectString(type, value)
				if affectString and value > 0:
					affectColor = self.__GetAttributeColor(i, value)
					self.AppendTextLine(affectString, affectColor)
				
				item.SelectItem(itemAbsorbedVnum)
			## END ATTR
			
			## WEARABLE
			item.SelectItem(itemVnumSash)
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)
			
			item.SelectItem(itemVnumSash)
			flagList = (
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_WARRIOR),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_ASSASSIN),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SURA),
						not item.IsAntiFlag(item.ITEM_ANTIFLAG_SHAMAN)
			)
			
			if app.ENABLE_WOLFMAN_CHARACTER:
				flagList += (not item.IsAntiFlag(item.ITEM_ANTIFLAG_WOLFMAN),)
			
			characterNames = ""
			for i in xrange(self.CHARACTER_COUNT):
				name = self.CHARACTER_NAMES[i]
				flag = flagList[i]
				if flag:
					characterNames += " "
					characterNames += name
			
			textLine = self.AppendTextLine(characterNames, self.NORMAL_COLOR, True)
			textLine.SetFeather()
			
			item.SelectItem(itemVnumSash)
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE):
				textLine = self.AppendTextLine(localeInfo.FOR_FEMALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
			
			if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE):
				textLine = self.AppendTextLine(localeInfo.FOR_MALE, self.NORMAL_COLOR, True)
				textLine.SetFeather()
			## END WEARABLE
			
			self.ShowToolTip()

	if app.ENABLE_AURA_SYSTEM:
		def SetAuraWindowItem(self, slotIndex):
			itemVnum = player.GetAuraItemID(slotIndex)
			if 0 == itemVnum: return

			self.ClearToolTip()
			if shop.IsOpen() and not shop.IsPrivateShop():
				self.AppendSellingPrice(item.GetISellItemPrice(item.SelectItem(itemVnum)))

			metinSlot = [player.GetAuraItemMetinSocket(slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetAuraItemAttribute(slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

			self.AddItemData(itemVnum, metinSlot, attrSlot, player.AURA_REFINE, slotIndex)

		def __AppendAffectInformationAura(self, window_type, slotIndex, metinSlot):
			socketLevelValue = 0
			socketBoostValue = 0
			if window_type == player.INVENTORY:
				socketLevelValue = player.GetItemMetinSocket(window_type, slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
				if metinSlot[player.ITEM_SOCKET_AURA_CURRENT_LEVEL] != 0 and socketLevelValue == 0:
					socketLevelValue = metinSlot[player.ITEM_SOCKET_AURA_CURRENT_LEVEL]
				socketBoostValue = player.GetItemMetinSocket(window_type, slotIndex, player.ITEM_SOCKET_AURA_BOOST)
				if metinSlot[player.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
					socketBoostValue = metinSlot[player.ITEM_SOCKET_AURA_BOOST]
			elif window_type == player.AURA_REFINE:
				socketLevelValue = player.GetAuraItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
				socketBoostValue = player.GetAuraItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_BOOST)
			elif window_type == player.SAFEBOX:
				socketLevelValue = safebox.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
				socketBoostValue = safebox.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_BOOST)

			if socketLevelValue == 0:
				return

			curLevel = (socketLevelValue / 100000) - 1000
			curStep = player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_STEP)
			if curStep < item.AURA_GRADE_RADIANT:
				curExpPer = 100.0 * (socketLevelValue % 100000) / player.GetAuraRefineInfo(curLevel, player.AURA_REFINE_INFO_NEED_EXP)

			self.AppendTextLine(localeInfo.AURA_LEVEL_STEP % (curLevel, curStep), self.CONDITION_COLOR)
			if curStep < item.AURA_GRADE_RADIANT:
				self.AppendTextLine(localeInfo.AURA_TOOLTIP_EXP % (curExpPer), self.CONDITION_COLOR)

			boostPercent = 0
			if socketBoostValue != 0:
				curBoostIndex = socketBoostValue / 100000000
				boostItemVnum = curBoostIndex + item.AURA_BOOST_ITEM_VNUM_BASE
				if boostItemVnum:
					item.SelectItem(boostItemVnum)
					boostPercent = item.GetValue(player.ITEM_VALUE_AURA_BOOST_PERCENT)

			if boostPercent > 0:
				self.AppendTextLine(localeInfo.AURA_DRAIN_BOOST_PER % (1.0 * curLevel / 10, boostPercent), self.CONDITION_COLOR)
			else:
				self.AppendTextLine(localeInfo.AURA_DRAIN_PER % (1.0 * curLevel / 10), self.CONDITION_COLOR)

		def __AppendAuraItemAffectInformation(self, oriItemVnum, window_type, slotIndex, metinSlot):
			socketLevelValue = 0
			socketBoostValue = 0
			if window_type == player.INVENTORY:
				socketLevelValue = player.GetItemMetinSocket(window_type, slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
				if metinSlot[player.ITEM_SOCKET_AURA_CURRENT_LEVEL] != 0 and socketLevelValue == 0:
					socketLevelValue = metinSlot[player.ITEM_SOCKET_AURA_CURRENT_LEVEL]
				socketBoostValue = player.GetItemMetinSocket(window_type, slotIndex, player.ITEM_SOCKET_AURA_BOOST)
				if metinSlot[player.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
					socketBoostValue = metinSlot[player.ITEM_SOCKET_AURA_BOOST]
			elif window_type == player.AURA_REFINE:
				socketLevelValue = player.GetAuraItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
				socketBoostValue = player.GetAuraItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_BOOST)
			elif window_type == player.SAFEBOX:
				socketLevelValue = safebox.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
				socketBoostValue = safebox.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_BOOST)

			if socketLevelValue == 0:
				return

			curLevel = (socketLevelValue / 100000) - 1000
			boostPercent = 0.0
			if socketBoostValue != 0:
				curBoostIndex = socketBoostValue / 100000000
				boostItemVnum = curBoostIndex + item.AURA_BOOST_ITEM_VNUM_BASE
				if boostItemVnum:
					item.SelectItem(boostItemVnum)
					boostPercent = item.GetValue(player.ITEM_VALUE_AURA_BOOST_PERCENT) / 100.0

			drainlate = curLevel / 10. / 100. + boostPercent

			socketInDrainItemVnum = 0
			if window_type == player.INVENTORY:
				socketInDrainItemVnum = player.GetItemMetinSocket(window_type, slotIndex, player.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM)
				if not metinSlot[player.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM] == 0 and socketInDrainItemVnum == 0:
					socketInDrainItemVnum = metinSlot[player.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM]
			elif window_type == player.AURA_REFINE:
				socketInDrainItemVnum = player.GetAuraItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM)
			elif window_type == player.SAFEBOX:
				socketInDrainItemVnum = safebox.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_DRAIN_ITEM_VNUM)

			if socketInDrainItemVnum == 0:
				return

			item.SelectItem(socketInDrainItemVnum)
			itemType = item.GetItemType()
			if itemType == item.ITEM_TYPE_ARMOR:
				defBonus = item.GetValue(5)*2
				if item.GetValue(1) >= 1:
					defGrade = max(((item.GetValue(1) + defBonus) * drainlate) , 1)
					if defGrade > 0:
						self.AppendSpace(5)
						self.AppendTextLineAbsorb(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade), self.GetChangeTextLineColor(defGrade))

			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)
				if affectValue > 0:
					affectValue = max((affectValue * drainlate), 1)
					affectString = self.__GetAffectString(affectType, affectValue)
					if affectString:
						self.AppendTextLineAbsorb(affectString, self.GetChangeTextLineColor(affectValue))

			item.SelectItem(oriItemVnum)

		def __AppendAttributeInformationAura(self, window_type, slotIndex, attrSlot, metinSlot):
			if 0 != attrSlot:
				socketLevelValue = 0
				socketBoostValue = 0
				if window_type == player.INVENTORY:
					socketLevelValue = player.GetItemMetinSocket(window_type, slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
					socketBoostValue = player.GetItemMetinSocket(window_type, slotIndex, player.ITEM_SOCKET_AURA_BOOST)
					if metinSlot[player.ITEM_SOCKET_AURA_CURRENT_LEVEL] != 0 and socketLevelValue == 0:
						socketLevelValue = metinSlot[player.ITEM_SOCKET_AURA_CURRENT_LEVEL]
					if metinSlot[player.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
						socketBoostValue = metinSlot[player.ITEM_SOCKET_AURA_BOOST]
				elif window_type == player.AURA_REFINE:
					socketLevelValue = player.GetAuraItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
					socketBoostValue = player.GetAuraItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_BOOST)
				elif window_type == player.SAFEBOX:
					socketLevelValue = safebox.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_CURRENT_LEVEL)
					socketBoostValue = safebox.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_BOOST)

				if socketLevelValue == 0:
					return

				curLevel = (socketLevelValue / 100000) - 1000
				boostPercent = 0.0
				if socketBoostValue != 0:
					curBoostIndex = socketBoostValue / 100000000
					boostItemVnum = curBoostIndex + item.AURA_BOOST_ITEM_VNUM_BASE
					if boostItemVnum:
						item.SelectItem(boostItemVnum)
						boostPercent = item.GetValue(player.ITEM_VALUE_AURA_BOOST_PERCENT) / 100.0

				drainlate = curLevel / 10. / 100. + boostPercent

				for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					type = attrSlot[i][0]
					value = attrSlot[i][1]
					if 0 >= value:
						continue

					value = max(((value) * drainlate) , 1)
					affectString = self.__GetAffectString(type, value)

					if affectString:
						affectColor = self.__GetAttributeColor(i, value)
						self.AppendTextLine(affectString, affectColor)

		def __AppendAuraBoostMetinSlotInfo(self, oriItemVnum, window_type, slotIndex, metinSlot):
			socketBoostValue = 0
			if window_type == player.INVENTORY:
				socketBoostValue = player.GetItemMetinSocket(window_type, slotIndex, player.ITEM_SOCKET_AURA_BOOST)
				if metinSlot[player.ITEM_SOCKET_AURA_BOOST] != 0 and socketBoostValue == 0:
					socketBoostValue = metinSlot[player.ITEM_SOCKET_AURA_BOOST]
			elif window_type == player.AURA_REFINE:
				socketBoostValue = player.GetAuraItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_BOOST)
			elif window_type == player.SAFEBOX:
				socketBoostValue = safebox.GetItemMetinSocket(slotIndex, player.ITEM_SOCKET_AURA_BOOST)

			if socketBoostValue == 0:
				return

			curBoostIndex = socketBoostValue / 100000000

			socketImageDict = {
				player.METIN_SOCKET_TYPE_SILVER : "d:/ymir work/ui/game/windows/metin_slot_silver.sub",
				player.METIN_SOCKET_TYPE_GOLD : "d:/ymir work/ui/game/windows/metin_slot_gold.sub",
			}
			socketType = player.METIN_SOCKET_TYPE_NONE
			if item.ITEM_AURA_BOOST_ERASER < curBoostIndex < item.ITEM_AURA_BOOST_ULTIMATE:
				socketType = player.METIN_SOCKET_TYPE_SILVER
			elif curBoostIndex == item.ITEM_AURA_BOOST_ULTIMATE:
				socketType = player.METIN_SOCKET_TYPE_GOLD

			if player.METIN_SOCKET_TYPE_NONE == socketType:
				return

			boostRemainTime = socketBoostValue % 100000000
			boostItemVnum = curBoostIndex + item.AURA_BOOST_ITEM_VNUM_BASE

			self.AppendSpace(5)

			slotImage = ui.ImageBox()
			slotImage.SetParent(self)
			slotImage.LoadImage(socketImageDict[socketType])
			slotImage.Show()
			self.childrenList.append(slotImage)

			## Name
			nameTextLine = ui.TextLine()
			nameTextLine.SetParent(self)
			nameTextLine.SetFontName(self.defFontName)
			nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
			nameTextLine.SetOutline()
			nameTextLine.SetFeather()
			nameTextLine.Show()
			self.childrenList.append(nameTextLine)

			if localeInfo.IsARABIC():
				slotImage.SetPosition(self.toolTipWidth - slotImage.GetWidth() - 9, self.toolTipHeight-1)
				nameTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 2)
			else:
				slotImage.SetPosition(9, self.toolTipHeight-1)
				nameTextLine.SetPosition(50, self.toolTipHeight + 2)

			boostItemImage = ui.ImageBox()
			boostItemImage.SetParent(self)
			boostItemImage.Show()
			self.childrenList.append(boostItemImage)

			if boostItemVnum:
				item.SelectItem(boostItemVnum)
				try:
					boostItemImage.LoadImage(item.GetIconImageFileName())
				except:
					dbg.TraceError("ItemToolTip.__AppendAuraBoostMetinSlotInfo() - Failed to find image file %d:%s" % (boostItemVnum, item.GetIconImageFileName()))

				nameTextLine.SetText(item.GetItemName())

				boostDrainTextLine = ui.TextLine()
				boostDrainTextLine.SetParent(self)
				boostDrainTextLine.SetFontName(self.defFontName)
				boostDrainTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				boostDrainTextLine.SetOutline()
				boostDrainTextLine.SetFeather()
				boostDrainTextLine.SetText(localeInfo.AURA_BOOST_DRAIN_PER % (item.GetValue(player.ITEM_VALUE_AURA_BOOST_PERCENT)))
				boostDrainTextLine.Show()
				self.childrenList.append(boostDrainTextLine)

				if localeInfo.IsARABIC():
					boostItemImage.SetPosition(self.toolTipWidth - boostItemImage.GetWidth() - 10, self.toolTipHeight)
					boostDrainTextLine.SetPosition(self.toolTipWidth - 50, self.toolTipHeight + 16 + 2)
				else:
					boostItemImage.SetPosition(10, self.toolTipHeight)
					boostDrainTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

				if 1 == item.GetValue(player.ITEM_VALUE_AURA_BOOST_UNLIMITED):
					boostRemainTime = 0

				if 0 != boostRemainTime:
					timeText = (localeInfo.LEFT_TIME + " : " + localeInfo.SecondToDHM(boostRemainTime))

					timeTextLine = ui.TextLine()
					timeTextLine.SetParent(self)
					timeTextLine.SetFontName(self.defFontName)
					timeTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
					timeTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
					timeTextLine.SetOutline()
					timeTextLine.SetFeather()
					timeTextLine.Show()
					timeTextLine.SetText(timeText)
					self.childrenList.append(timeTextLine)
					self.toolTipHeight += 16 + 2

			self.toolTipHeight += 35
			self.ResizeToolTip()

class HyperlinkItemToolTip(ItemToolTip):
	def __init__(self):
		ItemToolTip.__init__(self, isPickable=True)


	def SetHyperlinkItem(self, tokens):
		minTokenCount = 3

		head, vnum, flag = tokens[:minTokenCount]
		itemVnum = int(vnum, 16)

		metinSlot = [int(metin, 16) for metin in tokens[minTokenCount:minTokenCount+player.METIN_SOCKET_MAX_NUM]]

		minTokenCount+=player.METIN_SOCKET_MAX_NUM

		attrSlot = []
		rests = tokens[minTokenCount:minTokenCount+(player.ATTRIBUTE_SLOT_MAX_NUM*2)]
		if rests:
			rests.reverse()
			while rests:
				key = int(rests.pop(), 16)
				if rests:
					val = int(rests.pop())
					attrSlot.append((key, val))
				else:
					attrSlot.append((0, 0))

		minTokenCount+=(player.ATTRIBUTE_SLOT_MAX_NUM*2)

		attrRandomSlot = []
		if app.ENABLE_GLOVE_SYSTEM:
			rests = tokens[minTokenCount:minTokenCount+(item.GLOVE_ATTR_MAX_NUM*2)]
			if rests:
				rests.reverse()
				while rests:
					key = int(rests.pop(), 16)
					if rests:
						val = int(rests.pop())
						attrRandomSlot.append((key, val))
					else:
						attrRandomSlot.append((0, 0))

			minTokenCount+=(item.GLOVE_ATTR_MAX_NUM*2)

		apply_random_list = []
		if app.ENABLE_APPLY_RANDOM:
			rests = tokens[minTokenCount:minTokenCount+(player.APPLY_RANDOM_SLOT_MAX_NUM * 2)]
			if rests:
				rests.reverse()
				while rests:
					key = int(rests.pop(), 16)
					if rests:
						val = int(rests.pop())
						apply_random_list.append((key, val))
					else:
						apply_random_list.append((0, 0))

			minTokenCount += (player.APPLY_RANDOM_SLOT_MAX_NUM * 2)

		if app.ELEMENT_SPELL_WORLDARD:
			grade_element		= tokens[minTokenCount]
			minTokenCount+=1
			element_type_bonus		= tokens[minTokenCount]
			minTokenCount+=1
			attack_element		= tokens[minTokenCount]
			minTokenCount+=1
			value_element		= tokens[minTokenCount]
			self.ElementSpellItemDateDirect(int(grade_element,16),int(attack_element,16),int(element_type_bonus,16),int(value_element,16))
		self.ShowRender(False)
		self.ClearToolTip()

		if app.ENABLE_GLOVE_SYSTEM:
			self.AddItemData(itemVnum, metinSlot, attrSlot, 0, 0, player.INVENTORY, -1, 0, 0, attrRandomSlot, applyRandomList = apply_random_list)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

		ItemToolTip.OnUpdate(self)

		#minTokenCount = 3 + player.METIN_SOCKET_MAX_NUM
		#maxTokenCount = minTokenCount + 2 * player.ATTRIBUTE_SLOT_MAX_NUM
		#
		#if app.ELEMENT_SPELL_WORLDARD:
		#	maxTokenCount += 2+ (2*player.MAX_ELEMENTS_SPELL)
		#if app.ENABLE_GLOVE_SYSTEM:
		#	maxTokenCount += 2 * player.ATTRIBUTE_SLOT_MAX_NUM
		#if tokens and len(tokens) >= minTokenCount and len(tokens) <= maxTokenCount:
		#	head, vnum, flag = tokens[:3]
		#	itemVnum = int(vnum, 16)
		#	metinSlot = [int(metin, 16) for metin in tokens[3:6]]
		#
		#	if app.ELEMENT_SPELL_WORLDARD:
		#		rests = tokens[6:6+(2*player.ATTRIBUTE_SLOT_MAX_NUM)]
		#	else:
		#		rests = tokens[6:]
		#
		#	if rests:
		#		attrSlot = []
		#
		#		rests.reverse()
		#		while rests:
		#			key = int(rests.pop(), 16)
		#			if rests:
		#				val = int(rests.pop())
		#				attrSlot.append((key, val))
		#
		#		attrSlot += [(0, 0)] * (player.ATTRIBUTE_SLOT_MAX_NUM - len(attrSlot))
		#	else:
		#		attrSlot = [(0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM
		#
		#	self.ShowRender(False)
		#	self.ClearToolTip()
		#
		#	if app.ELEMENT_SPELL_WORLDARD:
		#		grade_element		= tokens[6+(2*player.ATTRIBUTE_SLOT_MAX_NUM)]
		#		element_type_bonus 	= tokens[7+(2*player.ATTRIBUTE_SLOT_MAX_NUM)]
		#		attack_element 		= tokens[8+(2*player.ATTRIBUTE_SLOT_MAX_NUM)]
		#		value_element 		= tokens[9+(2*player.ATTRIBUTE_SLOT_MAX_NUM)]
		#		self.ElementSpellItemDateDirect(int(grade_element,16),int(attack_element,16),int(element_type_bonus,16),int(value_element,16))
		#		
		#	self.AddItemData(itemVnum, metinSlot, attrSlot)
		#
		#	ItemToolTip.OnUpdate(self)

	def OnUpdate(self):
		pass

	def OnMouseLeftButtonDown(self):
		self.Hide()

class SkillToolTip(ToolTip):

	POINT_NAME_DICT = {
		player.LEVEL : localeInfo.SKILL_TOOLTIP_LEVEL,
		player.IQ : localeInfo.SKILL_TOOLTIP_INT,
	}

	SKILL_TOOL_TIP_WIDTH = 200
	PARTY_SKILL_TOOL_TIP_WIDTH = 340

	PARTY_SKILL_EXPERIENCE_AFFECT_LIST = (	( 2, 2,  10,),
											( 8, 3,  20,),
											(14, 4,  30,),
											(22, 5,  45,),
											(28, 6,  60,),
											(34, 7,  80,),
											(38, 8, 100,), )

	PARTY_SKILL_PLUS_GRADE_AFFECT_LIST = (	( 4, 2, 1, 0,),
											(10, 3, 2, 0,),
											(16, 4, 2, 1,),
											(24, 5, 2, 2,), )

	PARTY_SKILL_ATTACKER_AFFECT_LIST = (	( 36, 3, ),
											( 26, 1, ),
											( 32, 2, ), )

	SKILL_GRADE_NAME = {	player.SKILL_GRADE_MASTER : localeInfo.SKILL_GRADE_NAME_MASTER,
							player.SKILL_GRADE_GRAND_MASTER : localeInfo.SKILL_GRADE_NAME_GRAND_MASTER,
							player.SKILL_GRADE_PERFECT_MASTER : localeInfo.SKILL_GRADE_NAME_PERFECT_MASTER, }

	AFFECT_NAME_DICT =	{
							"HP" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_POWER,
							"ATT_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_GRADE,
							"DEF_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_DEF_GRADE,
							"ATT_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_SPEED,
							"MOV_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_MOV_SPEED,
							"DODGE" : localeInfo.TOOLTIP_SKILL_AFFECT_DODGE,
							"RESIST_NORMAL" : localeInfo.TOOLTIP_SKILL_AFFECT_RESIST_NORMAL,
							"REFLECT_MELEE" : localeInfo.TOOLTIP_SKILL_AFFECT_REFLECT_MELEE,
						}
	AFFECT_APPEND_TEXT_DICT =	{
									"DODGE" : "%",
									"RESIST_NORMAL" : "%",
									"REFLECT_MELEE" : "%",
								}

	def __init__(self):
		ToolTip.__init__(self, self.SKILL_TOOL_TIP_WIDTH)
	def __del__(self):
		ToolTip.__del__(self)

	def SetSkill(self, skillIndex, skillLevel = -1):

		if 0 == skillIndex:
			return

		if skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillGrade = player.GetSkillGrade(slotIndex)
			skillLevel = player.GetSkillLevel(slotIndex)
			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def SetSkillNew(self, slotIndex, skillIndex, skillGrade, skillLevel):

		if 0 == skillIndex:
			return

		if player.SKILL_INDEX_TONGSOL == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillLevel = player.GetSkillLevel(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendPartySkillData(skillGrade, skillLevel)

		elif player.SKILL_INDEX_RIDING == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			self.AppendSupportSkillDefaultData(skillIndex, skillGrade, skillLevel, 30)

		elif player.SKILL_INDEX_SUMMON == skillIndex:

			maxLevel = 10

			self.ClearToolTip()
			self.__SetSkillTitle(skillIndex, skillGrade)

			## Description
			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)

			if skillLevel == 10:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel*10), self.NORMAL_COLOR)

			else:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.__AppendSummonDescription(skillLevel, self.NORMAL_COLOR)

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel+1), self.NEGATIVE_COLOR)
				self.__AppendSummonDescription(skillLevel+1, self.NEGATIVE_COLOR)

		elif skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)

			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex, skillGrade)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def __SetSkillTitle(self, skillIndex, skillGrade):
		self.SetTitle(skill.GetSkillName(skillIndex, skillGrade))
		self.__AppendSkillGradeName(skillIndex, skillGrade)

	def __AppendSkillGradeName(self, skillIndex, skillGrade):
		if self.SKILL_GRADE_NAME.has_key(skillGrade):
			self.AppendSpace(5)
			self.AppendTextLine(self.SKILL_GRADE_NAME[skillGrade] % (skill.GetSkillName(skillIndex, 0)), self.CAN_LEVEL_UP_COLOR)

	def SetSkillOnlyName(self, slotIndex, skillIndex, skillGrade):
		if 0 == skillIndex:
			return

		slotIndex = player.GetSkillSlotIndex(skillIndex)

		self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
		self.ResizeToolTip()

		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)
		self.AppendDefaultData(skillIndex, skillGrade)
		self.AppendSkillConditionData(skillIndex)
		self.ShowToolTip()

	def AppendDefaultData(self, skillIndex, skillGrade = 0):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Level Limit
		levelLimit = skill.GetSkillLevelLimit(skillIndex)
		if levelLimit > 0:

			color = self.NORMAL_COLOR
			if player.GetStatus(player.LEVEL) < levelLimit:
				color = self.NEGATIVE_COLOR

			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (levelLimit), color)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

	def AppendSupportSkillDefaultData(self, skillIndex, skillGrade, skillLevel, maxLevel):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel = 40

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_WITH_MAX % (skillLevel, maxLevel), self.NORMAL_COLOR)

	def AppendSkillConditionData(self, skillIndex):
		conditionDataCount = skill.GetSkillConditionDescriptionCount(skillIndex)
		if conditionDataCount > 0:
			self.AppendSpace(5)
			for i in xrange(conditionDataCount):
				self.AppendTextLine(skill.GetSkillConditionDescription(skillIndex, i), self.CONDITION_COLOR)

	def AppendGuildSkillData(self, skillIndex, skillLevel):
		skillMaxLevel = 7
		skillCurrentPercentage = float(skillLevel) / float(skillMaxLevel)
		skillNextPercentage = float(skillLevel+1) / float(skillMaxLevel)
		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillLevel == skillMaxLevel:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)

				#####

				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillCurrentPercentage), self.ENABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillCurrentPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.ENABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillCurrentPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.ENABLE_COLOR)

		## Next Level
		if skillLevel < skillMaxLevel:
			if self.HasSkillLevelDescription(skillIndex, skillLevel+1):
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevel), self.DISABLE_COLOR)

				#####

				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillNextPercentage), self.DISABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillNextPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.DISABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillNextPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.DISABLE_COLOR)

	def AppendSkillDataNew(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage):

		self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
		self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

		skillLevelUpPoint = 1
		realSkillGrade = player.GetSkillGrade(slotIndex)
		skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
		skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillGrade == skill.SKILL_GRADE_COUNT:
					pass
				elif skillLevel == skillMaxLevelEnd:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.AppendSkillLevelDescriptionNew(skillIndex, skillCurrentPercentage, self.ENABLE_COLOR)

		## Next Level
		if skillGrade != skill.SKILL_GRADE_COUNT:
			if skillLevel < skillMaxLevelEnd:
				if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
					self.AppendSpace(5)
					## HP보강, 관통회피 보조스킬의 경우
					if skillIndex == 141 or skillIndex == 142:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_3 % (skillLevel+1), self.DISABLE_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)
					self.AppendSkillLevelDescriptionNew(skillIndex, skillNextPercentage, self.DISABLE_COLOR)

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def SetSkillBuffNPC(self, slotIndex, skillIndex, skillGrade, skillLevel, curSkillPower, nextSkillPower, intPoints):

			if 0 == skillIndex:
				return

			self.AppendDefaultData(skillIndex, skillGrade)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataBuffNPC(slotIndex, skillIndex, skillGrade, skillLevel, curSkillPower, nextSkillPower, intPoints)
			self.AppendSkillRequirement(skillIndex, skillLevel)

			self.ShowToolTip()
			
		def AppendSkillDataBuffNPC(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage, intPoints):
			self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
			self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

			skillLevelUpPoint = 1
			realSkillGrade = player.GetSkillGrade(slotIndex)
			skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
			skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

			## Current Level
			if skillLevel > 0:
				if self.HasSkillLevelDescription(skillIndex, skillLevel):
					self.AppendSpace(5)
					if skillGrade == skill.SKILL_GRADE_COUNT:
						pass
					elif skillLevel == skillMaxLevelEnd:
						self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
					self.AppendSkillLevelDescriptionBuffNPC(skillIndex, skillCurrentPercentage, self.ENABLE_COLOR, intPoints)

			## Next Level
			if skillGrade != skill.SKILL_GRADE_COUNT:
				if skillLevel < skillMaxLevelEnd:
					if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
						self.AppendSpace(5)
						if skillIndex == 141 or skillIndex == 142:
							self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_3 % (skillLevel+1), self.DISABLE_COLOR)
						else:
							self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)
						self.AppendSkillLevelDescriptionBuffNPC(skillIndex, skillNextPercentage, self.DISABLE_COLOR, intPoints)
					
		def AppendSkillLevelDescriptionBuffNPC(self, skillIndex, skillPercentage, color, intPoints):

			affectDataCount = skill.GetNewAffectDataCount(skillIndex)
			
			for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
				self.AppendTextLine(skill.GetBuffNPCSkillAffectDescription(skillIndex, i, skillPercentage, intPoints), color)

			duration = skill.GetDuration(skillIndex, skillPercentage)
			if duration > 0:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)

			coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
			if coolTime > 0:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)

	def AppendSkillLevelDescriptionNew(self, skillIndex, skillPercentage, color):

		affectDataCount = skill.GetNewAffectDataCount(skillIndex)
		if affectDataCount > 0:
			for i in xrange(affectDataCount):
				type, minValue, maxValue = skill.GetNewAffectData(skillIndex, i, skillPercentage)

				if not self.AFFECT_NAME_DICT.has_key(type):
					continue

				minValue = int(minValue)
				maxValue = int(maxValue)
				affectText = self.AFFECT_NAME_DICT[type]

				if "HP" == type:
					if minValue < 0 and maxValue < 0:
						minValue *= -1
						maxValue *= -1

					else:
						affectText = localeInfo.TOOLTIP_SKILL_AFFECT_HEAL

				affectText += str(minValue)
				if minValue != maxValue:
					affectText += " - " + str(maxValue)
				affectText += self.AFFECT_APPEND_TEXT_DICT.get(type, "")

				#import debugInfo
				#if debugInfo.IsDebugMode():
				#	affectText = "!!" + affectText

				self.AppendTextLine(affectText, color)

		else:
			for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
				self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillPercentage), color)


		## Duration
		duration = skill.GetDuration(skillIndex, skillPercentage)
		if duration > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)

		## Cooltime
		coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
		if coolTime > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)

		## SP
		needSP = skill.GetSkillNeedSP(skillIndex, skillPercentage)
		if needSP != 0:
			continuationSP = skill.GetSkillContinuationSP(skillIndex, skillPercentage)

			if skill.IsUseHPSkill(skillIndex):
				self.AppendNeedHP(needSP, continuationSP, color)
			else:
				self.AppendNeedSP(needSP, continuationSP, color)

	def AppendSkillRequirement(self, skillIndex, skillLevel):

		skillMaxLevel = skill.GetSkillMaxLevel(skillIndex)

		if skillLevel >= skillMaxLevel:
			return

		isAppendHorizontalLine = False

		## Requirement
		if skill.IsSkillRequirement(skillIndex):

			if not isAppendHorizontalLine:
				isAppendHorizontalLine = True
				self.AppendHorizontalLine()

			requireSkillName, requireSkillLevel = skill.GetSkillRequirementData(skillIndex)

			color = self.CANNOT_LEVEL_UP_COLOR
			if skill.CheckRequirementSueccess(skillIndex):
				color = self.CAN_LEVEL_UP_COLOR
			self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_SKILL_LEVEL % (requireSkillName, requireSkillLevel), color)

		## Require Stat
		requireStatCount = skill.GetSkillRequireStatCount(skillIndex)
		if requireStatCount > 0:

			for i in xrange(requireStatCount):
				type, level = skill.GetSkillRequireStatData(skillIndex, i)
				if self.POINT_NAME_DICT.has_key(type):

					if not isAppendHorizontalLine:
						isAppendHorizontalLine = True
						self.AppendHorizontalLine()

					name = self.POINT_NAME_DICT[type]
					color = self.CANNOT_LEVEL_UP_COLOR
					if player.GetStatus(type) >= level:
						color = self.CAN_LEVEL_UP_COLOR
					self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_STAT_LEVEL % (name, level), color)

	def HasSkillLevelDescription(self, skillIndex, skillLevel):
		if skill.GetSkillAffectDescriptionCount(skillIndex) > 0:
			return True
		if skill.GetSkillCoolTime(skillIndex, skillLevel) > 0:
			return True
		if skill.GetSkillNeedSP(skillIndex, skillLevel) > 0:
			return True

		return False

	def AppendMasterAffectDescription(self, index, desc, color):
		self.AppendTextLine(desc, color)

	def AppendNextAffectDescription(self, index, desc):
		self.AppendTextLine(desc, self.DISABLE_COLOR)

	def AppendNeedHP(self, needSP, continuationSP, color):

		self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP_PER_SEC % (continuationSP), color)

	def AppendNeedSP(self, needSP, continuationSP, color):

		if -1 == needSP:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_ALL_SP, color)

		else:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP_PER_SEC % (continuationSP), color)

	def AppendPartySkillData(self, skillGrade, skillLevel):
		def fix001(vl):
			return vl.replace("%,0f", "%.0f")

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel =  40

		if skillLevel <= 0:
			return

		skillIndex = player.SKILL_INDEX_TONGSOL
		slotIndex = player.GetSkillSlotIndex(skillIndex)
		skillPower = player.GetSkillCurrentEfficientPercentage(slotIndex)
		if localeInfo.IsBRAZIL():
			k = skillPower
		else:
			k = player.GetSkillLevel(skillIndex) / 100.0
		self.AppendSpace(5)
		self.AutoAppendTextLine(localeInfo.TOOLTIP_PARTY_SKILL_LEVEL % skillLevel, self.NORMAL_COLOR)

		if skillLevel>=10:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_ATTACKER) % chop( 10 + 60 * k ))

		if skillLevel>=20:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_BERSERKER) 	% chop(1 + 5 * k))
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_TANKER) 	% chop(50 + 1450 * k))

		if skillLevel>=25:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_BUFFER) % chop(5 + 45 * k ))

		if skillLevel>=35:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_SKILL_MASTER) % chop(25 + 600 * k ))

		if skillLevel>=40:
			self.AutoAppendTextLine(fix001(localeInfo.PARTY_SKILL_DEFENDER) % chop( 5 + 30 * k ))

		self.AlignHorizonalCenter()

	def __AppendSummonDescription(self, skillLevel, color):
		if skillLevel > 1:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel * 10), color)
		elif 1 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (15), color)
		elif 0 == skillLevel:
			self.AppendTextLine(localeInfo.SKILL_SUMMON_DESCRIPTION % (10), color)


if __name__ == "__main__":
	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui

	#wndMgr.SetOutlineFlag(True)

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create("METIN2 CLOSED BETA", systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	toolTip = ItemToolTip()
	toolTip.ClearToolTip()
	#toolTip.AppendTextLine("Test")
	desc = "Item descriptions:|increase of width of display to 35 digits per row AND installation of function that the displayed words are not broken up in two parts, but instead if one word is too long to be displayed in this row, this word will start in the next row."
	summ = ""

	toolTip.AddItemData_Offline(10, desc, summ, 0, 0)
	toolTip.Show()

	app.Loop()
