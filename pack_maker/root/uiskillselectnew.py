import ui
import chat
import localeInfo
import uiCommon
import net

job_dict = {
	'JOB_WARRIOR': {
		'position': {
			'thinboard_image_index': 0,
			'slot_count': 5,
			'slot_skill_first_index': [1, 16]
		},
		'desc': {
			'header_title': ['Váleèník Tìlo', 'Váleèník Mental'],
			'footer_title': ['Váleèník Tìlo', 'Váleèník Mental'],
			'footer_desc': [localeInfo.ADVANCE_SKILL_SELECT_WARRIOR_SKILL_IMG_DESC_LEFT, localeInfo.ADVANCE_SKILL_SELECT_WARRIOR_SKILL_IMG_DESC_RIGHT]
		}
	},
	'JOB_ASSASSIN': {
		'position': {
			'thinboard_image_index': 1,
			'slot_count': 5,
			'slot_skill_first_index': [31, 46],
		},
		'desc': {
			'header_title': ['Ninja Boj zblízka', 'Ninja Boj na dálku'],
			'footer_title': ['Ninja Boj zblízka', 'Ninja Boj na dálku'],
			'footer_desc': [localeInfo.ADVANCE_SKILL_SELECT_ASSASSIN_SKILL_IMG_DESC_LEFT, localeInfo.ADVANCE_SKILL_SELECT_ASSASSIN_SKILL_IMG_DESC_RIGHT]
		}
	},
	'JOB_SURA': {
		'position': {
			'thinboard_image_index': 2,
			'slot_count': 6,
			'slot_skill_first_index': [61, 76],
		},
		'desc': {
			'header_title': ['Sura Magické zbranì', 'Sura Èerná magie'],
			'footer_title': ['Sura Magické zbranì', 'Sura Èerná magie'],
			'footer_desc': [localeInfo.ADVANCE_SKILL_SELECT_SURA_SKILL_IMG_DESC_LEFT, localeInfo.ADVANCE_SKILL_SELECT_SURA_SKILL_IMG_DESC_RIGHT]
		}
	},
	'JOB_SHAMAN': {
		'position': {
			'thinboard_image_index': 3,
			'slot_count': 6,
			'slot_skill_first_index': [91, 106],
		},
		'desc': {
			'header_title': ['Šaman Draèí moc', 'Šaman Léèení'],
			'footer_title': ['Šaman Draèí moc', 'Šaman Léèení'],
			'footer_desc': [localeInfo.ADVANCE_SKILL_SELECT_SHAMAN_SKILL_IMG_DESC_LEFT, localeInfo.ADVANCE_SKILL_SELECT_SHAMAN_SKILL_IMG_DESC_RIGHT]
		}
	},
}

class SkillSelectWindowNew(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.thinboard_0_image = []
		self.thinboard_1_image = []
		self.job = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.thinboard_0_image = []
		self.thinboard_1_image = []
		self.job = None
		
	def LoadWindow(self):
		try:
			python_script_loader = ui.PythonScriptLoader()
			python_script_loader.LoadScriptFile(self, "UIScript/SkillSelectWindowNew.py")

			for i in xrange(4):
				self.thinboard_0_image.append(self.GetChild('thinboard_0_image%d' % i))
				self.thinboard_0_image[i].Hide()
				self.thinboard_1_image.append(self.GetChild('thinboard_1_image%d' % i))
				self.thinboard_1_image[i].Hide()

			for i in xrange(2):
				self.GetChild('slot_%d_bg_6' % i).Hide()
				self.GetChild('slot_%d_6' % i).Hide()
				self.GetChild('slot_%d_bg_5' % i).Hide()
				self.GetChild('slot_%d_5' % i).Hide()
				self.GetChild('confirm_%d' % i).SAFE_SetEvent(self.OnClickConfirmButton, i)

		except:
			import exception
			exception.Abort("<SkillSelectWindowNew> failed to inialize!")

		#self.Open("JOB_SHAMAN")

	def OnClickConfirmButton(self, index):
		skill_group_confirm = uiCommon.QuestionDialog("thin")
		skill_group_confirm.SetText(localeInfo.ADVANCE_SKILL_SELECT_FINAL_ANSWER)
		skill_group_confirm.SetAcceptEvent(lambda arg=True: self.RequestConfirmButtonFinaly(arg, index))
		skill_group_confirm.SetCancelEvent(lambda arg=False: self.RequestConfirmButtonFinaly(arg, index))
		skill_group_confirm.Open()
		self.skill_group_confirm = skill_group_confirm

	def RequestConfirmButtonFinaly(self, answer, index):
		if not self.skill_group_confirm:
			return
		if answer:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Zvolená Schopnost: %s" % job_dict[self.job]['desc']['header_title'][index])
			net.SendChatPacket("/advance_skill_select %s" % str(index+1))
			self.Close()
			
		self.skill_group_confirm.Close()
		self.skill_group_confirm = None

	def Open(self, job):
		self.job = job
		thinboard_image_index = job_dict[job]['position']['thinboard_image_index']
		slot_count = job_dict[job]['position']['slot_count']
		slot_skill_first_index_job0 = job_dict[job]['position']['slot_skill_first_index'][0]
		slot_skill_first_index_job1 = job_dict[job]['position']['slot_skill_first_index'][1]

		self.thinboard_0_image[thinboard_image_index].Show()
		self.thinboard_1_image[thinboard_image_index].Show()
		self.GetChild('slot_0_bg_%d' % slot_count).Show()
		self.GetChild('slot_0_%d' % slot_count).Show()
		self.GetChild('slot_1_bg_%d' % slot_count).Show()
		self.GetChild('slot_1_%d' % slot_count).Show()

		for i in xrange(slot_count):
			self.GetChild('slot_0_%d' % slot_count).SetSkillSlotNew(i, i+slot_skill_first_index_job0, 3, 40)
			self.GetChild('slot_0_%d' % slot_count).SetCoverButton(i)
			self.GetChild('slot_0_%d' % slot_count).DisableCoverButton(i)

			self.GetChild('slot_1_%d' % slot_count).SetSkillSlotNew(i, i+slot_skill_first_index_job1, 3, 40)
			self.GetChild('slot_1_%d' % slot_count).SetCoverButton(i)
			self.GetChild('slot_1_%d' % slot_count).DisableCoverButton(i)

		for i in xrange(2):
			self.GetChild('title_%d_value' % i).SetText(job_dict[job]['desc']['header_title'][i])
			self.GetChild('thinboard_circle%d_desc0' % i).SetText(job_dict[job]['desc']['footer_title'][i])
			self.GetChild('thinboard_circle%d_desc1' % i).SetText(job_dict[job]['desc']['footer_desc'][i])
		
		self.Show()
		self.SetTop()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

