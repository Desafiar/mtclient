import ui
import wndMgr
import chat
import event
import uiScriptLocale
import dbg
import constInfo
import app

class PanelPenceresi(ui.Window):
	#eklenicek1 Değişken tanımlama misali gbi.Her butona 1+ ekle
	TEST_BUTTON = 0
	
	def __init__(self):
		ui.Window.__init__(self)
		self.Apsis = 0
		self.Ordinat = 200
		self.AcKpa = 0
		self.AnaEkran()

	def AnaEkran(self):
		self.PanelEkran = ui.ExpandedImageBox()
		self.KLVZ = []
		self.PanelEkran.LoadImage("panel/anaekran.tga")					#Dosya konumu
		self.PanelEkran.SetPosition(400, 0)
		self.PanelEkran.Show()

		self.PanelEkranButonlar = ui.Button()
		self.PanelEkranButonlar.SetParent(self.PanelEkran)
		self.PanelEkranButonlar.SetEvent(self.__Akbutonlari)
		self.PanelEkranButonlar.SetPosition(150, 123)
		self.PanelEkranButonlar.SetUpVisual("panel/ac.tga")#Dosya konumu
		self.PanelEkranButonlar.SetOverVisual("panel/ac.tga")#Dosya konumu
		self.PanelEkranButonlar.SetDownVisual("panel/ac.tga")#Dosya konumu
		self.PanelEkranButonlar.Show()

		buttonlar = [ #eklenicek2
					{#42 ekle
						"name" : "TestButton",
						"x" : 600,
						"y" : 15,
						"tooltip_text" : "			Test",	#Eğer sol tarafa eklediysen 3 tab koyun başına yoksa yarısı gözükmüyor
						"default_image" : "d:/ymir work/ui/game/taskbar/character_button_01.sub",
						"over_image" : "d:/ymir work/ui/game/taskbar/character_button_02.sub",
						"down_image" : "d:/ymir work/ui/game/taskbar/character_button_03.sub"
					}				#yeni buton ekleyince , ekleyin
				]

		for i in xrange(len(buttonlar)):
			EkleButon = ui.Button()
			EkleButon.SetParent(self.PanelEkran)
			EkleButon.SetPosition(buttonlar[i]["x"], buttonlar[i]["y"])#Kordi
			EkleButon.SetToolTipText(buttonlar[i]["tooltip_text"])#txt
			EkleButon.SetUpVisual(buttonlar[i]["default_image"])#1
			EkleButon.SetOverVisual(buttonlar[i]["over_image"])#2
			EkleButon.SetDownVisual(buttonlar[i]["down_image"])#3
			EkleButon.Show()
			self.KLVZ.append(EkleButon)

		self.ButonGecisYer = {}#++
		self.ButonGecisYer[PanelPenceresi.TEST_BUTTON] = self.KLVZ[PanelPenceresi.TEST_BUTTON]#eklenicek3

		self.Show()

	def SetToggleButtonEvent(self, eButon, kEventFunc):
		self.ButonGecisYer[eButon].SetEvent(kEventFunc)

	def __Akbutonlari(self):
		if self.AcKpa==0:
			self.PanelEkranButonlar.SetUpVisual("panel/kapa.tga")#Dosya konumu
			self.PanelEkranButonlar.SetOverVisual("panel/kapa.tga")#Dosya konumu
			self.PanelEkranButonlar.SetDownVisual("panel/kapa.tga")#Dosya konumu
			self.AcKpa = 1
		elif self.AcKpa==2:
			self.PanelEkranButonlar.SetUpVisual("panel/ac.tga")#Dosya konumu
			self.PanelEkranButonlar.SetOverVisual("panel/ac.tga")#Dosya konumu
			self.PanelEkranButonlar.SetDownVisual("panel/ac.tga")#Dosya konumu
			self.AcKpa=3

	def OnUpdate(self):
		self.Gecisler()

	def Gecisler(self):#Beynimi .... neymisin
		if self.AcKpa==1:#ÇK
			a = self.PanelEkran.GetGlobalPosition()[0]
			if a<=0:
				self.PanelEkran.SetPosition(-95 + self.Apsis , wndMgr.GetScreenHeight()/2-self.Ordinat)
				self.Apsis += 6
			else:
				self.AcKpa = 2
				self.Apsis = 0
		if self.AcKpa==3:
			a = self.PanelEkran.GetGlobalPosition()[0]
			if a>=-228:#GR
				self.PanelEkran.SetPosition(self.Apsis - a, wndMgr.GetScreenHeight()/2-self.Ordinat)
				self.Apsis -= 8
			else:
				self.PanelEkran.SetPosition(-228, wndMgr.GetScreenHeight()/2-self.Ordinat)
				self.AcKpa = 0
				self.Apsis = 0

	def HideBoard(self):
		self.Hide()
		self.PanelEkran.Hide()

