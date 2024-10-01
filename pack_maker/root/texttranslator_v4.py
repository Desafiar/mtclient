# -*- coding: utf-8 -*-
import ui
import grp
import textwrap
import systemSetting
import uiToolTip
from googletrans import Translator
import time
import constInfo
import app
import chat
## Ente ente ente ente
                                          
DEFAULT_LANG_TO_ENCODING = "cp1252"

COLOR_INFO = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
COLOR_TEXT = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)

TEXT_BUTTON_INFO = "Info"
TEXT_BUTTON_TRANSLATE = "Uebersetzen"
TEXT_LEAVE_SHIFT_TO_TRANSLATE = "[Lass SHIFT los um den Text zu uebersetzen]"
TEXT_BOARD_WHISPER_TITLE_NAME = "Whisper [%s] Translator"
TEXT_BOARD_CHAT_TITLE_NAME = "Chat Translator"

SHOW_INFO_BUTTON_ON_BOARD = False
TEXT_INFO_TRANSLATOR = "[Translator Infos]"
TEXT_INFO_TRANSLATOR_USAGE = "Gehe mit der Maus ueber einen Text und halte die Taste [linkes STRG] gedrueckt um ihn zu uebersetzen. Halte die beiden Tasten [linkes STRG] + [linkes SHIFT] gedrueckt um mehr Text auszuwaehlen und lasse [linkes SHIFT] wieder los um ihn zu uebersetzen."

TOOLTIP_INFO_SHOW_TIME = 10.0
TOOLTIP_MULTI_TEXT_SHOW_TIME = 5.0
TOOLTIP_SHOW_TIME = 0.1

KEY_TO_TRANSLATE = app.DIK_LCONTROL

class TextTranslator(object):
	def __init__(self):
		self.isMultiText = False
		self.textToTranslate = ""
		self.translatedTextDict = {}
		self.lastTranslatedText = ""
		self.wrapper = textwrap.TextWrapper(width=50) 
	
		toolTipTranslation = uiToolTip.ToolTip(230)
		toolTipTranslation.HideToolTip()
		self.toolTipTranslation = toolTipTranslation

		self.waitingDialog = WaitingDialog()
		
		self.translator = Translator()

	def TranslateTextAvailable(self):
		if self.textToTranslate != "":
			return True
		else:
			return False
		
	def SetTranslateText(self, text):
		if text:
			pos = text.find(' : ') ## filter chat names
			if pos != -1:
				text = text[pos+3:]
			
			self.isMultiText = False
			self.textToTranslate = text
				
	def TranslateText(self):
		toolTipShowTime = TOOLTIP_SHOW_TIME
		if self.isMultiText:
			toolTipShowTime = TOOLTIP_MULTI_TEXT_SHOW_TIME

		self.isMultiText = False

		if self.lastTranslatedText != self.textToTranslate:
			if self.textToTranslate:
				textToTranslate = self.textToTranslate
				self.textToTranslate = ""
				langTo = systemSetting.GetTransLangKey()
				if langTo not in self.translatedTextDict.keys():
					self.translatedTextDict[langTo] = {}
			
				if textToTranslate not in self.translatedTextDict[langTo].keys():
					self.translatedTextDict[langTo][textToTranslate] = {'translation':"...", 'srcLang':"...", 'destLang':"..."}
					self.Translate(textToTranslate)

				self.toolTipTranslation.ClearToolTip()

				wordListTextToTranslate = self.wrapper.wrap(text=textToTranslate)
				for word in wordListTextToTranslate:
					self.toolTipTranslation.AppendTextLine(word, COLOR_TEXT)

				wordListTranslation = self.wrapper.wrap(text=self.translatedTextDict[langTo][textToTranslate]['translation'])
				self.toolTipTranslation.AppendTextLine("[%s -> %s]" % (self.translatedTextDict[langTo][textToTranslate]['srcLang'], self.translatedTextDict[langTo][textToTranslate]['destLang']), COLOR_INFO)
				for word in wordListTranslation:
					self.toolTipTranslation.AppendTextLine(word, COLOR_TEXT)
		self.ShowToolTip(toolTipShowTime)
	
	def AppendTranslateText(self, text):
		self.isMultiText = True
		if text and not text in self.textToTranslate:
			self.textToTranslate += " "+text
			self.RefreshToolTipMultiTranslateText()

	def RefreshToolTipMultiTranslateText(self):
		self.toolTipTranslation.ClearToolTip()
		wordList = self.wrapper.wrap(text=self.textToTranslate)
		
		for word in wordList:
			self.toolTipTranslation.AppendTextLine(word, COLOR_TEXT)
		self.toolTipTranslation.AppendTextLine(TEXT_LEAVE_SHIFT_TO_TRANSLATE, COLOR_INFO)
		self.ShowToolTip(TOOLTIP_MULTI_TEXT_SHOW_TIME)

	def Translate(self, textToTranslate):
		langTo = systemSetting.GetTransLangKey()
		translated = self.translator.translate(textToTranslate.decode("cp%s" % app.GetDefaultCodePage()).encode('utf-8', errors='replace'), dest=langTo)
		if langTo in constInfo.AVAILABLE_LANGUAGES:
			encoding = constInfo.AVAILABLE_LANGUAGES[langTo]['encoding']
		else:
			encoding = DEFAULT_LANG_TO_ENCODING

		destLang = translated.dest.encode(encoding, errors='replace')
		if destLang in constInfo.AVAILABLE_LANGUAGES:
			destLang = constInfo.AVAILABLE_LANGUAGES[destLang]['name']

		srcLang = translated.src.encode(encoding, errors='replace')
		if srcLang in constInfo.AVAILABLE_LANGUAGES:
			srcLang = constInfo.AVAILABLE_LANGUAGES[srcLang]['name']

		self.translatedTextDict[langTo][textToTranslate] = {
			'translation' : translated.text.encode(encoding, errors='replace'), 
			'srcLang' : srcLang,
			'destLang' : destLang
		}

	def ShowToolTip(self, time = 0.0):
		self.toolTipTranslation.Show()
		if time != 0.0:
			self.waitingDialog.Open(time)
			self.waitingDialog.SAFE_SetTimeOverEvent(self.HideToolTip)
		else:
			self.waitingDialog.Stop()

	def HideToolTip(self):
		if self.toolTipTranslation.IsShow():
			self.toolTipTranslation.HideToolTip()
			self.textToTranslate = ""

	def OnKeyDownEvent(self, key):
		if key == KEY_TO_TRANSLATE:
			if app.TRANS != app.GetCursor():
				app.SetCursor(app.TRANS)
			return True
		return False
	
	def OnKeyUpEvent(self, key):
		if key == KEY_TO_TRANSLATE:
			if app.TRANS == app.GetCursor():
				app.SetCursor(app.NORMAL)
				return True
		return False

class TranslatorBoard(ui.BoardWithTitleBar):
	def __init__(self, editLine):
		ui.BoardWithTitleBar.__init__(self)
		self.SetSize(200+30, 90)
		self.AddFlag('float')
		self.SetTitleName("Translator by Ente")
		self.SetCloseEvent(self.Close)
		self.SetCenterPosition()
		self.Hide()

		self.editLine = editLine

		comboBoxLanguageFrom = ui.ComboBox()
		comboBoxLanguageFrom.SetParent(self)
		comboBoxLanguageFrom.SetPosition(15,30+25)
		comboBoxLanguageFrom.SetSize(50, 20)
		comboBoxLanguageFrom.ClearItem()

		comboBoxLanguageTo = ui.ComboBox()
		comboBoxLanguageTo.SetParent(self)
		comboBoxLanguageTo.SetPosition(15+60,30+25)
		comboBoxLanguageTo.SetSize(50, 20)
		comboBoxLanguageTo.ClearItem()

		comboBoxLanguageFrom.InsertItem('auto', 'auto')
		for langKey, lang in constInfo.AVAILABLE_LANGUAGES.iteritems():
			comboBoxLanguageFrom.InsertItem(langKey, lang['name'])
			comboBoxLanguageTo.InsertItem(langKey, lang['name'])

		self.languageFrom = 'auto' 
		comboBoxLanguageFrom.SetCurrentItem("auto")

		self.languageTo = list(constInfo.AVAILABLE_LANGUAGES)[0]
		comboBoxLanguageTo.SetCurrentItem(constInfo.AVAILABLE_LANGUAGES[self.languageTo]['name'])
		
		self.comboBoxLanguageFrom = comboBoxLanguageFrom
		self.comboBoxLanguageFrom.SetEvent(self._OnSelectItemComboBoxLanguageFrom)

		self.comboBoxLanguageTo = comboBoxLanguageTo
		self.comboBoxLanguageTo.SetEvent(self._OnSelectItemComboBoxLanguageTo)

		self.comboBoxLanguageFrom.Show()
		self.comboBoxLanguageTo.Show()

		buttonTranslate = ui.Button()
		buttonTranslate.SetParent(self)
		buttonTranslate.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		buttonTranslate.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		buttonTranslate.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		buttonTranslate.SetText(TEXT_BUTTON_TRANSLATE)
		buttonTranslate.SetPosition(260-88-42,30+25)
		buttonTranslate.SetEvent(self._OnClickButtonTranslate)
		buttonTranslate.Show()
		self.buttonTranslate = buttonTranslate

		buttonInfo = ui.Button()
		buttonInfo.SetParent(self)
		buttonInfo.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
		buttonInfo.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
		buttonInfo.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
		buttonInfo.SetText(TEXT_BUTTON_INFO)
		buttonInfo.SetPosition(260-43-42,30)
		buttonInfo.SetEvent(self._OnClickButtonInfo)
		if SHOW_INFO_BUTTON_ON_BOARD:
			buttonInfo.Show()
		self.buttonInfo = buttonInfo

		checkBox = ui.CheckBox()
		checkBox.SetParent(self)
		checkBox.SetPosition(15,30+5)
		checkBox.SetCheckStatus(False)
		checkBox.SetTextInfo("Instant Translate")
		checkBox.Show()
		self.checkBox = checkBox

		toolTipInfo = uiToolTip.ToolTip(230)
		toolTipInfo.HideToolTip()
		self.toolTipInfo = toolTipInfo

		self.wrapper = textwrap.TextWrapper(width=50)
		self.wordListInfoTranslatorUsage = self.wrapper.wrap(text=TEXT_INFO_TRANSLATOR_USAGE)
		self.waitingDialog = WaitingDialog()

		self.translator = Translator()

	def _OnClickButtonInfo(self):
		self.toolTipInfo.ClearToolTip()
		self.toolTipInfo.AppendTextLine(TEXT_INFO_TRANSLATOR, COLOR_INFO)
		for word in self.wordListInfoTranslatorUsage:
			self.toolTipInfo.AppendTextLine(word, COLOR_TEXT)

		self.ShowToolTip(TOOLTIP_INFO_SHOW_TIME)

	def ShowToolTip(self, time = 0.0):
		self.toolTipInfo.Show()
		if time != 0.0:
			self.waitingDialog.Open(time)
			self.waitingDialog.SAFE_SetTimeOverEvent(self.HideToolTip)
		else:
			self.waitingDialog.Stop()

	def HideToolTip(self):
		if self.toolTipInfo.IsShow():
			self.toolTipInfo.HideToolTip()

	def __del__(self):
		self.Close()
		ui.BoardWithTitleBar.__del__(self)

	def Close(self):
		self.Hide()

	def SetWhisperTitleName(self, targetName):
		self.SetTitleName(TEXT_BOARD_WHISPER_TITLE_NAME % targetName)

	def SetChatTitleName(self):
		self.SetTitleName(TEXT_BOARD_CHAT_TITLE_NAME)

	def _OnSelectItemComboBoxLanguageFrom(self, id):
		if id == 'auto':
			self.comboBoxLanguageFrom.SetCurrentItem("auto")
		else:
			self.comboBoxLanguageFrom.SetCurrentItem(constInfo.AVAILABLE_LANGUAGES[id]['name'])
		self.languageFrom = id

	def _OnSelectItemComboBoxLanguageTo(self, id):
		self.comboBoxLanguageTo.SetCurrentItem(constInfo.AVAILABLE_LANGUAGES[id]['name'])
		self.languageTo = id

	def InitiateTranslation(self):
		if self.checkBox.GetCheckStatus() == True:
			self.__Translate()

	def _OnClickButtonTranslate(self):
		self.__Translate()
		self.Close()

	def __Translate(self):
		textToTranslate = self.editLine.GetText()
		if textToTranslate:
			chatMark = ""
			for c in ['!','#','%']:
				if textToTranslate[0] == c:
					chatMark = c
					textToTranslate = textToTranslate[1:]
					break
			
			if self.languageFrom == 'auto':
				translated = self.translator.translate(textToTranslate.decode("cp%s" % app.GetDefaultCodePage()).encode('utf-8', errors='replace'), dest=self.languageTo)
			else:
				translated = self.translator.translate(textToTranslate.decode("cp%s" % app.GetDefaultCodePage()).encode('utf-8', errors='replace'), src=self.languageFrom, dest=self.languageTo)
			
			if self.languageTo in constInfo.AVAILABLE_LANGUAGES:
				encoding = constInfo.AVAILABLE_LANGUAGES[self.languageTo]['encoding']
			else:
				encoding = DEFAULT_LANG_TO_ENCODING

			translatedText = translated.text.encode(encoding, errors='replace')
			self.editLine.SetText(chatMark + translatedText)
	
	def OpenTranslator(self):
		self.SetTop()
		self.Show()

class WaitingDialog(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)
		self.eventTimeOver = lambda *arg: None
		self.eventExit = lambda *arg: None
		self.run = False

	def Open(self, waitTime):
		curTime = time.clock()
		self.endTime = curTime + waitTime
		self.run = True
		self.Show()	

	def Stop(self):
		self.run = False

	def Close(self):
		self.Hide()

	def Destroy(self):
		self.Hide()

	def SAFE_SetTimeOverEvent(self, event):
		self.eventTimeOver = ui.__mem_func__(event)

	def SAFE_SetExitEvent(self, event):
		self.eventExit = ui.__mem_func__(event)
		
	def OnUpdate(self):
		if self.run:
			lastTime = max(0, self.endTime - time.clock())
			if 0 == lastTime:
				self.Close()
				self.eventTimeOver()

wnd = TextTranslator()