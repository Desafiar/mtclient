import ui
import dbg
import app
import constInfo
import player
import chat
import net
import event
import playerSettingModule

FACE_IMAGE_DICT = {
	playerSettingModule.RACE_WARRIOR_M	: "arayuz/icon_mwarrior.tga",
	playerSettingModule.RACE_WARRIOR_W	: "arayuz/icon_wwarrior.tga",
	playerSettingModule.RACE_ASSASSIN_M	: "arayuz/icon_mninja.tga",
	playerSettingModule.RACE_ASSASSIN_W	: "arayuz/icon_wninja.tga",
	playerSettingModule.RACE_SURA_M		: "arayuz/icon_msura.tga",
	playerSettingModule.RACE_SURA_W		: "arayuz/icon_wsura.tga",
	playerSettingModule.RACE_SHAMAN_M	: "arayuz/icon_mshaman.tga",
	playerSettingModule.RACE_SHAMAN_W	: "arayuz/icon_wshaman.tga",
}

class arayuzdialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded=0
		self.arayuz = constInfo.GUI_ARAYUZ
		self.GUI = constInfo.GUI_ARAYUZ_ICERIK
		self.level_yazi = None
		self.isim_yazi = None
		self.karakter_resim = None
		self.exp_bar = None
		self.exp_yazi = None
		self.hp_bar = None
		self.hp_yazi = None
		self.sp_bar = None
		self.sp_yazi = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Load(self):
		if constInfo.arayuz_mod == 0:
			##arayüz sistemi
			arayuz = ui.AniImageBox()
			arayuz.AppendImage("arayuz/yeni_arayuz.tga")
			constInfo.GUI_ARAYUZ = arayuz
			self.arayuz = constInfo.GUI_ARAYUZ
			self.arayuz.SetPosition(0,55)
			self.arayuz.SetSize(275, 104)
			self.arayuz.Show()

			self.level_yazi = ui.TextLine()
			self.level_yazi.SetParent(self.arayuz)
			self.level_yazi.SetFontName("Tahoma:12")

			if int(player.GetStatus(player.LEVEL)) < 15:
				self.level_yazi.SetPosition(135,91)
			else:
				self.level_yazi.SetPosition(132,91)

			self.level_yazi.SetText(str(player.GetStatus(player.LEVEL)))
			self.level_yazi.Show()

			self.GUI[0].append(self.level_yazi)
			self.isim_yazi = ui.TextLine()
			self.isim_yazi.SetParent(self.arayuz)
			self.isim_yazi.SetFontName("Tahoma:12")
			self.isim_yazi.SetText(str(player.GetName()))
			kacharfvarki = len(str(player.GetName()))

			if kacharfvarki < 15:
				self.isim_yazi.SetPosition(195,102)
			else:
				self.isim_yazi.SetPosition(195,126)

			self.isim_yazi.Show()
			self.GUI[1].append(self.isim_yazi)
			self.GUI[1].append(self.isim_yazi)

			karakter_resim = ui.AniImageBox()
			race = net.GetMainActorRace()
			karakter_resim.AppendImage(FACE_IMAGE_DICT[race])
			self.karakter_resim = karakter_resim
			self.karakter_resim.SetParent(self.arayuz)
			self.karakter_resim.SetPosition(34,23)
			self.karakter_resim.Show()
			self.GUI[2].append(self.karakter_resim)

			exp_bar = ui.AniImageBox()
			exp_bar.AddFlag("not_pick")
			exp_bar.AppendImage("arayuz/uf_runes_fill_full.tga")
			self.exp_bar = exp_bar
			self.exp_bar.SetParent(self.arayuz)
			self.exp_bar.SetPosition(18, 90)
			self.exp_bar.SetPercentage(0,100)
			self.exp_bar.Show()

			self.exp_yazi = ui.TextLine()
			self.exp_yazi.SetParent(exp_bar)
			self.exp_yazi.SetFontName("Tahoma:12")
			self.exp_yazi.SetText("%d" % (constInfo.arayuz_max))
			self.exp_yazi.SetPosition(2,54)
			self.exp_yazi.Show()

			hp_bar = ui.AniImageBox()
			hp_bar.AddFlag("not_pick")
			hp_bar.AppendImage("arayuz/uf_fill_green.tga")
			hp_bar.AppendImage("arayuz/uf_fill_green.tga")

			self.hp_bar = hp_bar
			self.hp_bar.SetParent(self.arayuz)
			self.hp_bar.SetPosition(123, 32)
			self.hp_bar.SetPercentage(0,100)
			self.hp_bar.Show()
			self.GUI[5].append(self.hp_bar)

			self.hp_yazi = ui.TextLine()
			self.hp_yazi.SetParent(hp_bar)
			self.hp_yazi.SetFontName("Tahoma:12")
			self.hp_yazi.SetText("%d / %d" % (constInfo.arayuz_hp_cur, constInfo.arayuz_hp_max))
			self.hp_yazi.SetPosition(70,3)
			self.hp_yazi.Show()
			self.GUI[6].append(self.hp_yazi)

			self.hp_bar.SetPercentage((float(constInfo.arayuz_hp_cur) / max(1, float(constInfo.arayuz_hp_max)) * 100),100)

			sp_bar = ui.AniImageBox()
			sp_bar.AddFlag("not_pick")
			hp_bar.SetDelay(25)
			sp_bar.SetDelay(25)
			sp_bar.AppendImage("arayuz/uf_fill_orange.tga")
			sp_bar.AppendImage("arayuz/uf_fill_orange.tga")

			self.sp_bar = sp_bar
			self.sp_bar.SetParent(self.arayuz)
			self.sp_bar.SetPosition(131, 59)
			self.sp_bar.SetPercentage(0,100)
			self.sp_bar.Show()
			self.GUI[7].append(self.sp_bar)

			self.sp_yazi = ui.TextLine()
			self.sp_yazi.SetParent(sp_bar)
			self.sp_yazi.SetFontName("Tahoma:12")
			self.sp_yazi.SetText("%d / %d" % (constInfo.arayuz_mp_cur, constInfo.arayuz_mp_max))
			self.sp_yazi.SetPosition(70,2)
			self.sp_yazi.Show()
			self.GUI[8].append(self.sp_yazi)

			self.sp_bar.SetPercentage((float(constInfo.arayuz_mp_cur) / max(1, float(constInfo.arayuz_mp_max)) * 100),100)

	def OnUpdate(self):
		if constInfo.arayuz_mod == 0:
			self.arayuz.Show()
			if int(player.GetStatus(player.LEVEL)) < 10:
				self.GUI[0][0].SetPosition(135,91)
			else:
				self.GUI[0][0].SetPosition(132,91)
			if self.level_yazi:
				self.level_yazi.SetText(str(player.GetStatus(player.LEVEL)))
			else:
				self.GUI[0][0].SetText(str(player.GetStatus(player.LEVEL)))

			if self.exp_bar:
				self.exp_bar.SetPercentage((float(constInfo.arayuz_cur) / max(1, float(constInfo.arayuz_max)) * 100),100)

			if self.exp_yazi:
				self.exp_yazi.SetText("%.2f%%" % (float(constInfo.arayuz_cur) / max(1, float(constInfo.arayuz_max)) * 100))

			if self.hp_bar:
				self.hp_bar.SetPercentage((float(constInfo.arayuz_hp_cur) / max(1, float(constInfo.arayuz_hp_max)) * 100),100)
			else:
				self.GUI[5][0].SetPercentage((float(constInfo.arayuz_hp_cur) / max(1, float(constInfo.arayuz_hp_max)) * 100),100)

			if self.hp_yazi:
				self.hp_yazi.SetText("%d / %d" % (constInfo.arayuz_hp_cur, constInfo.arayuz_hp_max))
			else:
				self.GUI[6][0].SetText("%d / %d" % (constInfo.arayuz_hp_cur, constInfo.arayuz_hp_max))

			if self.sp_bar:
				self.sp_bar.SetPercentage((float(constInfo.arayuz_mp_cur) / max(1, float(constInfo.arayuz_mp_max)) * 100),100)
			else:
				self.GUI[7][0].SetPercentage((float(constInfo.arayuz_mp_cur) / max(1, float(constInfo.arayuz_mp_max)) * 100),100)

			if self.sp_yazi:
				self.sp_yazi.SetText("%d / %d" % (constInfo.arayuz_mp_cur, constInfo.arayuz_mp_max))
			else:
				self.GUI[8][0].SetText("%d / %d" % (constInfo.arayuz_mp_cur, constInfo.arayuz_mp_max))
		else:
			self.arayuz.Hide()

	def Show(self):
		if self.isLoaded==0:
			self.isLoaded=1
			self.__Load()

		ui.ScriptWindow.Show(self)

	def Open(self):
		self.Show()

	def Close(self):
		self.arayuz.Hide()

