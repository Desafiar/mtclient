import ui, grp, wndMgr, item, player, nonplayer, datetime, app, net, constInfo, chat, localeInfo

IMG_DIR = "d:/ymir work/ui/game/battle_pass/"

battlepass_mission_data = {
	player.MISSION_NONE:{
		"name":localeInfo.MISSION_NONE,
		"description":localeInfo.MISSION_NONE,
		"subtext":"",
		"image":"none",
	},
	player.MISSION_BOSS:{
		"name":localeInfo.MISSION_BOSS,
		"description":localeInfo.MISSION_BOSS_DESC,
		"subtext":localeInfo.MISSION_BOSS_SUB,
		"image":"boss",
	},
	player.MISSION_CATCH_FISH:{
		"name":localeInfo.MISSION_CATCH_FISH,
		"description":localeInfo.MISSION_CATCH_FISH_DESC,
		"subtext":localeInfo.MISSION_CATCH_FISH_SUB,
		"image":"catch_fish",
	},
	player.MISSION_CRAFT_ITEM:{
		"name":localeInfo.MISSION_CRAFT_ITEM,
		"description":localeInfo.MISSION_CRAFT_ITEM_DESC,
		"subtext":localeInfo.MISSION_CRAFT_ITEM_SUB,
		"image":"craft",
	},
	player.MISSION_CRAFT_GAYA:{
		"name":localeInfo.MISSION_CRAFT_GAYA,
		"description":localeInfo.MISSION_CRAFT_GAYA_DESC,
		"subtext":"",
		"image":"craft_gaya",
	},
	player.MISSION_DESTROY_ITEM:{
		"name":localeInfo.MISSION_DESTROY_ITEM,
		"description":localeInfo.MISSION_DESTROY_ITEM_DESC,
		"subtext":localeInfo.MISSION_CRAFT_ITEM_SUB,
		"image":"destroy_item",
	},
	player.MISSION_DUNGEON:{
		"name":localeInfo.MISSION_DUNGEON,
		"description":localeInfo.MISSION_DUNGEON_DESC,
		"subtext":localeInfo.MISSION_DUNGEON_SUB,
		"image":"dungeon",
	},
	player.MISSION_EARN_MONEY:{
		"name":localeInfo.MISSION_EARN_MONEY,
		"description":localeInfo.MISSION_EARN_MONEY_DESC,
		"subtext":"",
		"image":"earn_money",
	},
	player.MISSION_FEED_PET:{
		"name":localeInfo.MISSION_FEED_PET,
		"description":localeInfo.MISSION_FEED_PET_DESC,
		"subtext":"",
		"image":"clean",
	},
	player.MISSION_LEVEL_UP:{
		"name":localeInfo.MISSION_LEVEL_UP,
		"description":localeInfo.MISSION_LEVEL_UP_DESC,
		"subtext":"",
		"image":"levelup",
	},
	player.MISSION_MONSTER:{
		"name":localeInfo.MISSION_MONSTER,
		"description":localeInfo.MISSION_MONSTER_DESC,
		"subtext":localeInfo.MISSION_MONSTER_SUB,
		"image":"monster",
	},
	player.MISSION_MOUNT_TIME:{
		"name":localeInfo.MISSION_MOUNT_TIME,
		"description":localeInfo.MISSION_MOUNT_TIME_DESC,
		"subtext":"",
		"image":"mount",
	},
	player.MISSION_OPEN_OFFLINESHOP:{
		"name":localeInfo.MISSION_OPEN_OFFLINESHOP,
		"description":localeInfo.MISSION_OPEN_OFFLINESHOP_DESC,
		"subtext":"",
		"image":"open_offlineshop",
	},
	player.MISSION_PLAYTIME:{
		"name":localeInfo.MISSION_PLAYTIME,
		"description":localeInfo.MISSION_PLAYTIME_DESC,
		"subtext":"",
		"image":"playtime",
	},
	player.MISSION_REFINE_ITEM:{
		"name":localeInfo.MISSION_REFINE_ITEM,
		"description":localeInfo.MISSION_REFINE_ITEM_DESC,
		"subtext":localeInfo.MISSION_REFINE_ITEM_SUB,
		"image":"refine",
	},
	player.MISSION_REFINE_ALCHEMY:{
		"name":localeInfo.MISSION_REFINE_ALCHEMY,
		"description":localeInfo.MISSION_REFINE_ALCHEMY_DESC,
		"subtext":"",
		"image":"refine_alchemy",
	},
	player.MISSION_SASH:{
		"name":localeInfo.MISSION_SASH,
		"description":localeInfo.MISSION_SASH_DESC,
		"subtext":"",
		"image":"sash",
	},
	player.MISSION_SELL_ITEM:{
		"name":localeInfo.MISSION_SELL_ITEM,
		"description":localeInfo.MISSION_SELL_ITEM_DESC,
		"subtext":localeInfo.MISSION_REFINE_ITEM_SUB,
		"image":"sell_item",
	},
	player.MISSION_SPEND_MONEY:{
		"name":localeInfo.MISSION_SPEND_MONEY,
		"description":localeInfo.MISSION_SPEND_MONEY_DESC,
		"subtext":"",
		"image":"spend_money",
	},
	player.MISSION_SPRITE_STONE:{
		"name":localeInfo.MISSION_SPRITE_STONE,
		"description":localeInfo.MISSION_SPRITE_STONE_DESC,
		"subtext":localeInfo.MISSION_REFINE_ITEM_SUB,
		"image":"sprite_stone",
	},
	player.MISSION_STONE:{
		"name":localeInfo.MISSION_STONE,
		"description":localeInfo.MISSION_STONE_DESC,
		"subtext":localeInfo.MISSION_MONSTER_SUB,
		"image":"stone",
	},
	player.MISSION_USE_EMOTICON:{
		"name":localeInfo.MISSION_USE_EMOTICON,
		"description":localeInfo.MISSION_USE_EMOTICON_DESC,
		"subtext":"",
		"image":"use_emoticon",
	},
	player.MISSION_WHISPER:{
		"name":localeInfo.MISSION_WHISPER,
		"description":localeInfo.MISSION_WHISPER_DESC,
		"subtext":"",
		"image":"whisper",
	},
	player.MISSION_SHOUT_CHAT:{
		"name":localeInfo.MISSION_SHOUT_CHAT,
		"description":localeInfo.MISSION_SHOUT_CHAT_DESC,
		"subtext":"",
		"image":"whisper",
	},
	player.MISSION_KILLPLAYER:{
		"name":localeInfo.MISSION_KILLPLAYER,
		"description":localeInfo.MISSION_KILLPLAYER_DESC,
		"subtext":"",
		"image":"clean",
	},
}
class BattlePassGauge(ui.Window):
	SLOT_WIDTH = 16
	SLOT_HEIGHT = 7
	GAUGE_TEMPORARY_PLACE = 9
	GAUGE_WIDTH = 16
	def __init__(self):
		ui.Window.__init__(self)
		self.width = 0
	def Destroy(self):
		self.width = 0
		self.SLOT_WIDTH = 0
		self.SLOT_HEIGHT = 0
		self.GAUGE_TEMPORARY_PLACE = 0
		self.GAUGE_WIDTH = 0
		self.imgLeft = 0
		self.imgCenter = 0
		self.imgRight = 0
		self.imgGauge = 0
	def __del__(self):
		ui.Window.__del__(self)
	def MakeGauge(self, width):
		self.width = max(48, width)
		imgSlotLeft = ui.ImageBox()
		imgSlotLeft.SetParent(self)
		imgSlotLeft.LoadImage(IMG_DIR+"gauge/gauge_slot_left.tga")
		imgSlotLeft.Show()
		imgSlotRight = ui.ImageBox()
		imgSlotRight.SetParent(self)
		imgSlotRight.LoadImage(IMG_DIR+"gauge/gauge_slot_right.tga")
		imgSlotRight.Show()
		imgSlotRight.SetPosition(width - self.SLOT_WIDTH, 0)
		imgSlotCenter = ui.ExpandedImageBox()
		imgSlotCenter.SetParent(self)
		imgSlotCenter.LoadImage(IMG_DIR+"gauge/gauge_slot_center.tga")
		imgSlotCenter.Show()
		imgSlotCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
		imgSlotCenter.SetPosition(self.SLOT_WIDTH, 0)
		imgGauge = ui.ExpandedImageBox()
		imgGauge.SetParent(self)
		imgGauge.LoadImage(IMG_DIR+"gauge/gauge_bpass.tga")
		imgGauge.Show()
		imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)
		imgSlotLeft.AddFlag("attach")
		imgSlotCenter.AddFlag("attach")
		imgSlotRight.AddFlag("attach")
		self.imgLeft = imgSlotLeft
		self.imgCenter = imgSlotCenter
		self.imgRight = imgSlotRight
		self.imgGauge = imgGauge
		self.SetSize(width, self.SLOT_HEIGHT)
	def SetPercentage(self, curValue, maxValue):
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0
		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGauge.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)
class BattlePassScrollbar(ui.Window):
	SCROLLBAR_WIDTH = 13
	SCROLLBAR_MIDDLE_HEIGHT = 1
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	SCROLL_BTN_XDIST = 2
	SCROLL_BTN_YDIST = 2
	class MiddleBar(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")
			self.SetWindowName("scrollbar_middlebar")
		def MakeImage(self):
			top = ui.ExpandedImageBox()
			top.SetParent(self)
			top.LoadImage(IMG_DIR+"scrollbar/scroll_top.tga")
			top.AddFlag("not_pick")
			top.Show()
			bottom = ui.ExpandedImageBox()
			bottom.SetParent(self)
			bottom.LoadImage(IMG_DIR+"scrollbar/scroll_buttom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()
			middle = ui.ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage(IMG_DIR+"scrollbar/scroll_mid.tga")
			middle.AddFlag("not_pick")
			middle.Show()
			self.top = top
			self.bottom = bottom
			self.middle = middle
		def SetSize(self, height):
			minHeight = self.top.GetHeight() + self.bottom.GetHeight() + self.middle.GetHeight()
			height = max(minHeight, height)
			ui.DragButton.SetSize(self, 10, height)
			scale = (height - minHeight) / 2 
			extraScale = 0
			if (height - minHeight) % 2 == 1:
				extraScale = 1
			self.middle.SetPosition(0, self.top.GetHeight() + scale)
			self.bottom.SetPosition(0, height - self.bottom.GetHeight())
	def __init__(self):
		ui.Window.__init__(self)
		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.eventArgs = None
		self.lockFlag = False
		self.CreateScrollBar()
		self.SetScrollBarSize(0)
		self.scrollStep = 0.09
		self.SetWindowName("NONAME_ScrollBar")
	def __del__(self):
		ui.Window.__del__(self)
	def CreateScrollBar(self):
		topImage = ui.ExpandedImageBox()
		topImage.SetParent(self)
		topImage.AddFlag("not_pick")
		topImage.LoadImage(IMG_DIR+"scrollbar/scrollbar_top.tga")
		topImage.Show()
		bottomImage = ui.ExpandedImageBox()
		bottomImage.SetParent(self)
		bottomImage.AddFlag("not_pick")
		bottomImage.LoadImage(IMG_DIR+"scrollbar/scrollbar_bottom.tga")
		bottomImage.Show()
		middleImage = ui.ExpandedImageBox()
		middleImage.SetParent(self)
		middleImage.AddFlag("not_pick")
		middleImage.SetPosition(0, topImage.GetHeight())
		middleImage.LoadImage(IMG_DIR+"scrollbar/scrollbar_middle.tga")
		middleImage.Show()
		self.topImage = topImage
		self.bottomImage = bottomImage
		self.middleImage = middleImage
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(0) # set min height
		self.middleBar = middleBar
	def Destroy(self):
		self.eventScroll = None
		self.eventArgs = None
	def SetScrollEvent(self, event, *args):
		self.eventScroll = event
		self.eventArgs = args
	def SetMiddleBarSize(self, pageScale):
		self.middleBar.SetSize(int(pageScale * float(self.GetHeight() - self.SCROLL_BTN_YDIST*2)))
		realHeight = self.GetHeight() - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()
		self.pageSize = realHeight
	def SetScrollBarSize(self, height):
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.pageSize = height - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()
		middleImageScale = float((height - self.SCROLL_BTN_YDIST*2) - self.middleImage.GetHeight()) / float(self.middleImage.GetHeight())
		self.middleImage.SetRenderingRect(0, 0, 0, middleImageScale)
		self.bottomImage.SetPosition(0, height - self.bottomImage.GetHeight())
		self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, self.middleBar.GetWidth(), height - self.SCROLL_BTN_YDIST * 2)
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)
	def SetScrollStep(self, step):
		self.scrollStep = step
	def GetScrollStep(self):
		return self.scrollStep
	def GetPos(self):
		return self.curPos
	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)
	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)
	def SetPos(self, pos, moveEvent = True):
		pos = max(0.0, pos)
		pos = min(1.0, pos)
		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, int(newPos) + self.SCROLL_BTN_YDIST)
		if moveEvent == True:
			self.OnMove()
	def OnMove(self):
		if self.lockFlag:
			return
		if 0 == self.pageSize:
			return
		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLL_BTN_YDIST) / float(self.pageSize)
		if self.eventScroll:
			apply(self.eventScroll, self.eventArgs)
	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		newPos = float(yMouseLocalPosition) / float(self.GetHeight())
		self.SetPos(newPos)
	def LockScroll(self):
		self.lockFlag = True
	def UnlockScroll(self):
		self.lockFlag = False

class MultiTextLine(ui.Window):
	def __del__(self):
		ui.Window.__del__(self)
	def Destroy(self):
		self.children = []
		self.rangeText = 0
	def __init__(self):
		ui.Window.__init__(self)
		self.children = []
		self.rangeText = 15
		self.textType = ""
		self.rgb = [0,0,0]
		self.outlineStatus =False
	def SetFontColor(self, r, g, b):
		self.rgb = [r, g, b]
		for text in self.children:
			text.SetFontColor(r, g, b)
	def SetOutline(self):
		for text in self.children:
			text.SetOutline()
		self.outlineStatus = True
	def SetTextType(self, textType):
		self.textType = textType
		for text in self.children:
			self.AddTextType(self.textType.split("#"),text)
	def SetTextRange(self, range):
		self.rangeText = range
		yPosition = 0
		for text in self.children:
			text.SetPosition(0,yPosition)
			yPosition+=self.rangeText
	def AddTextType(self, typeArg, text):
		if len(typeArg) > 1:
			if typeArg[0] == "vertical":
				if typeArg[1] == "top":
					text.SetVerticalAlignTop()
				elif typeArg[1] == "bottom":
					text.SetVerticalAlignBottom()
				elif typeArg[1] == "center":
					text.SetVerticalAlignCenter()
			elif typeArg[0] == "horizontal":
				if typeArg[1] == "left":
					text.SetHorizontalAlignLeft()
				elif typeArg[1] == "right":
					text.SetHorizontalAlignRight()
				elif typeArg[1] == "center":
					text.SetHorizontalAlignCenter()
	def SetText(self, cmd):
		for oldText in self.children:
			oldText.Hide()
			oldText.Destroy()
		self.children=[]
		multi_arg = cmd.split("\n")
		yPosition = 0
		for text in multi_arg:
			childText = ui.TextLine()
			childText.SetParent(self)
			childText.SetPosition(0,yPosition)
			if self.textType != "":
				self.AddTextType(self.textType.split("#"),childText)
			childText.SetText(str(text))
			if self.outlineStatus:
				childText.SetOutline()
			if self.rgb[0] != 0:
				childText.SetFontColor(self.rgb[0], self.rgb[1], self.rgb[2])
			childText.Show()
			self.children.append(childText)
			yPosition+=self.rangeText

class BattlePassWindow(ui.BoardWithTitleBar):
	class BattlePassItem(ui.RadioButton):
		def __del__(self):
			ui.RadioButton.__del__(self)
		def __init__(self):
			ui.RadioButton.__init__(self)
			self.Destroy()
		def Destroy(self):
			self.children = {}
			self.rewardItemList = []
			self.missionIndex = 0
			self.missionReward = ""
			self.missionValue = 0
			self.missionMaxValue = 0
			self.missionSubValue = 0
			self.missinVecIndex = 0
		def __lt__(self, other):
			return (self.missinVecIndex < other.missinVecIndex)
		def LoadMission(self, missionIndex, missionReward, missionValue, missionMaxValue, missionSubValue, missinVecIndex):
			self.missionIndex = missionIndex
			self.missionReward = missionReward
			self.missionValue = missionValue
			self.missionMaxValue = missionMaxValue
			self.missionSubValue = missionSubValue
			self.missinVecIndex = missinVecIndex

			if not battlepass_mission_data.has_key(missionIndex):
				self.LoadMission(0,"",0,0,0)
				return

			missionData = battlepass_mission_data[missionIndex]

			self.SetUpVisual(IMG_DIR+"list_item_0.tga")
			self.SetOverVisual(IMG_DIR+"list_item_0.tga")
			self.SetDownVisual(IMG_DIR+"list_item_1.tga")

			battlePassImage = ui.ImageBox()
			battlePassImage.SetParent(self)
			battlePassImage.AddFlag("not_pick")
			battlePassImage.LoadImage(IMG_DIR+"mission/"+missionData["image"]+".tga")
			battlePassImage.SetPosition(1,1)
			battlePassImage.Show()
			self.children["battlePassImage"] = battlePassImage

			battlePassText = ui.TextLine()
			battlePassText.SetParent(self)
			battlePassText.AddFlag("not_pick")
			battlePassText.SetHorizontalAlignLeft()
			battlePassText.SetText(missionData["name"])
			battlePassText.SetPosition(1+battlePassImage.GetWidth()+10,5)
			battlePassText.SetOutline()
			battlePassText.Show()
			self.children["battlePassText"] = battlePassText

			battlePassGauge = BattlePassGauge()
			battlePassGauge.SetParent(self)
			battlePassGauge.AddFlag("not_pick")
			battlePassGauge.MakeGauge(132)
			battlePassGauge.SetPosition(1+battlePassImage.GetWidth()+5,5+22)
			battlePassGauge.SetPercentage(missionValue,missionMaxValue)
			battlePassGauge.Show()
			self.children["battlePassGauge"] = battlePassGauge

			self.rewardItemList = []
			#missionReward = "50300|5#51501|10##"
			if len(missionReward) > 0:
				itemsSplit = missionReward.split("#")
				for rewardList in itemsSplit:
					rewardItem = rewardList.split("|")
					if len(rewardItem) != 2:
						continue
					if rewardItem[0].isdigit() == False or rewardItem[1].isdigit() == False:
						continue
					self.rewardItemList.append([int(rewardItem[0]),int(rewardItem[1])])

			for j in xrange(len(self.rewardItemList)):
				(itemVnum,itemCount) = (self.rewardItemList[j][0],self.rewardItemList[j][1])
				item.SelectItem(itemVnum)
				rewardItem = ui.ImageBox()
				rewardItem.SetParent(self)
				rewardItem.AddFlag("attach")
				rewardItem.LoadImage(item.GetIconImageFileName())
				rewardItem.SAFE_SetStringEvent("MOUSE_OVER_IN",self.OverInItem,itemVnum)
				rewardItem.SAFE_SetStringEvent("MOUSE_OVER_OUT",self.OverOutItem)
				rewardItem.SetPosition(187+(j*32),7)
				rewardItem.Show()
				self.children["rewardItem%d"%j] = rewardItem

				rewardItemCount = ui.NumberLine()
				rewardItemCount.SetParent(self)
				rewardItemCount.AddFlag("attach")
				rewardItemCount.SetNumber(str(itemCount))
				rewardItemCount.SetPosition(187+(j*32)+15,7+20)
				rewardItemCount.Show()
				self.children["rewardItemCount%d"%j] = rewardItemCount

		def SetMission(self, missionValue):
			self.missionValue = missionValue
			self.children["battlePassGauge"].SetPercentage(self.missionValue,self.missionMaxValue)

		def OverOutItem(self):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipItem:
					interface.tooltipItem.HideToolTip()

		def OverInItem(self, itemVnum):
			interface = constInfo.GetInterfaceInstance()
			if interface:
				if interface.tooltipItem:
					interface.tooltipItem.SetItemToolTip(itemVnum)

	def Destroy(self):
		self.children = {}
		self.missionIndex = 0
		self.pageIndex = 0
		self.battlePassStatus = 0
		self.isSendPacket = False
		self.battlePassleftTime = 0
		self.battlePassRewardList = []
		self.clickIndex = 0
		self.effectStatus = False
		self.effectTime = 0
	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.Destroy()
		self.LoadWindow()
	def LoadWindow(self):
		self.AddFlag("movable")
		self.AddFlag("attach")
		self.AddFlag("float")
		self.SetSize(540,302)
		self.SetCenterPosition()
		self.SetTitleName(localeInfo.BATTLEPASS_TITLE)
		self.SetCloseEvent(self.Close)

		listBoxWall = ui.ImageBox()
		listBoxWall.SetParent(self)
		listBoxWall.AddFlag("attach")
		listBoxWall.LoadImage(IMG_DIR+"wall.tga")
		listBoxWall.SetPosition(8,30)
		listBoxWall.Show()
		self.children["listBoxWall"] = listBoxWall

		listBox = ui.ListBoxEx()
		listBox.SetParent(listBoxWall)
		listBox.AddFlag("attach")
		listBox.SetSize(listBoxWall.GetWidth(),listBoxWall.GetHeight())
		listBox.SetPosition(3,5)
		listBox.SetItemSize(290,46)
		listBox.SetItemStep(46+5)
		listBox.SetViewItemCount(5)
		listBox.Show()
		self.children["listBox"] = listBox

		scrollBar = BattlePassScrollbar()
		scrollBar.SetParent(listBoxWall)
		scrollBar.SetPosition(listBoxWall.GetWidth()-11,0)
		scrollBar.SetScrollBarSize(listBoxWall.GetHeight())
		#scrollBar.Show()
		listBox.SetScrollBar(scrollBar)
		self.children["scrollBar"] = scrollBar

		listBoxScroll = ui.ListBoxEx()
		listBoxScroll.SetParent(listBoxWall)
		listBox.AddFlag("attach")
		listBox.SetSize(listBoxWall.GetWidth(),listBoxWall.GetHeight())
		listBox.SetPosition(3,5)
		listBox.SetItemSize(290,46)
		listBox.SetItemStep(46+5)
		listBox.SetViewItemCount(5)
		listBox.Show()
		self.children["listBox"] = listBox

		rightWall = ui.ImageBox()
		rightWall.SetParent(self)
		rightWall.AddFlag("attach")
		rightWall.SetPosition(8+listBoxWall.GetWidth()+5,30)
		rightWall.Show()
		self.children["rightWall"] = rightWall

		rightBtn0 = ui.RadioButton()
		rightBtn0.SetParent(rightWall)
		rightBtn0.SetUpVisual(IMG_DIR+"right_table_button.tga")
		rightBtn0.SetOverVisual(IMG_DIR+"right_table_button.tga")
		rightBtn0.SetDownVisual(IMG_DIR+"right_table_button.tga")
		rightBtn0.SetPosition(20,5)
		rightBtn0.SetEvent(self.SetRightTable, 0)
		rightBtn0.Show()
		self.children["rightBtn0"] = rightBtn0

		rightWall0 = ui.ImageBox()
		rightWall0.SetParent(rightWall)
		rightWall0.SetPosition(2,51)
		self.children["rightWall0"] = rightWall0

		wall0BarList = [\
			[0,2,[0.1, 0.0, 0.0, 0.5]],\
			[0,38,[1.0, 1.0, 1.0, 0.2]],\
			[0,86,[0.1, 0.0, 0.0, 0.5]],\
			[0,122,[1.0, 1.0, 1.0, 0.2]]
		]

		for j in xrange(len(wall0BarList)):
			barData = wall0BarList[j]
			rightWall0Bar = ui.ImageBox()
			rightWall0Bar.SetParent(rightWall0)
			rightWall0Bar.SetSize(rightWall0.GetWidth(),21)
			rightWall0Bar.SetPosition(barData[0],barData[1])
			rightWall0Bar.LoadImage(IMG_DIR+"bar.tga")
			rightWall0Bar.SetDiffuseColor(barData[2][0],barData[2][1],barData[2][2],barData[2][3])
			rightWall0Bar.Show()
			self.children["rightWall0Bar%d"%j] = rightWall0Bar

		wall0TextList = [\
			[100,-18,"center","Title",[1.0,1.0,1.0],""],\
			[100, 4,"center","Info",[1.0,1.0,1.0],localeInfo.BATTLEPASS_INFORMATION],\
			[5, 20,"left","Type",[1.0,1.0,1.0],""],
			[5, 40,"left","Remaining",[1.0,1.0,1.0],""],
			[5, 58,"left","Completed",[1.0,1.0,1.0],""],
			[100, 88,"center","DescriptionTitle",[1.0,1.0,1.0],localeInfo.BATTLEPASS_DESCRIPTION],
			[5, 105,"left","Description",[0.9490, 0.9058, 0.7568],""],
		]

		for j in xrange(len(wall0TextList)):
			textData = wall0TextList[j]
			if textData[3] == "Description":
				rightWall0Text = MultiTextLine()
				rightWall0Text.SetTextType("horizontal#%s"%textData[2])
			else:
				rightWall0Text = ui.TextLine()
				if textData[2] == "center":
					rightWall0Text.SetHorizontalAlignCenter()
				elif textData[2] == "right":
					rightWall0Text.SetHorizontalAlignRight()
				elif textData[2] == "left":
					rightWall0Text.SetHorizontalAlignLeft()
			rightWall0Text.SetParent(rightWall0)
			if textData[5] != "":
				rightWall0Text.SetText(textData[5])
			rightWall0Text.SetPosition(textData[0], textData[1])
			if textData[4][0] != 1.0 and textData[4][1] != 1.0 and textData[4][2] != 1.0:
				rightWall0Text.SetFontColor(textData[4][0],textData[4][1],textData[4][2])
			rightWall0Text.SetOutline()
			rightWall0Text.Show()
			self.children["rightWall0%s"%textData[3]] = rightWall0Text

		rightWall1 = ui.ImageBox()
		rightWall1.SetParent(rightWall)
		rightWall1.SetPosition(2,51)
		self.children["rightWall1"] = rightWall1

		wall1BarList = [\
			[0,21,[0.1, 0.0, 0.0, 0.5]],\
			[0,57,[0.1, 0.0, 0.0, 0.5]],\
		]

		for j in xrange(len(wall1BarList)):
			barData = wall1BarList[j]
			rightWall1Bar = ui.ImageBox()
			rightWall1Bar.SetParent(rightWall1)
			rightWall1Bar.SetSize(rightWall1.GetWidth(),21)
			rightWall1Bar.SetPosition(barData[0],barData[1])
			rightWall1Bar.LoadImage(IMG_DIR+"bar.tga")
			rightWall1Bar.SetDiffuseColor(barData[2][0],barData[2][1],barData[2][2],barData[2][3])
			rightWall1Bar.Show()
			self.children["rightWall1Bar%d"%j] = rightWall1Bar

		wall1TextList = [\
			[100,-18,"center","Title",[1.0,1.0,1.0],localeInfo.BATTLEPASS_INFORMATION_EX],\
			[5,5,"left","Name",[1.0,1.0,1.0],""],\
			[5,23,"left","Status",[1.0,1.0,1.0],""],\
			[5,41,"left","Task",[1.0,1.0,1.0],""],\
			[5,59,"left","Completed",[1.0,1.0,1.0],""],\
			[5,77,"left","Time",[1.0,1.0,1.0],""],\
			[100,100,"center","GaugeTitle",[1.0,1.0,1.0],localeInfo.BATTLEPASS_TOTAL_PROGRESS],\
		]

		for j in xrange(len(wall1TextList)):
			textData = wall1TextList[j]

			rightWall1Text = ui.TextLine()
			rightWall1Text.SetParent(rightWall1)
			if textData[2] == "center":
				rightWall1Text.SetHorizontalAlignCenter()
			elif textData[2] == "right":
				rightWall1Text.SetHorizontalAlignRight()
			elif textData[2] == "left":
				rightWall1Text.SetHorizontalAlignLeft()
			if textData[5] != "":
				rightWall1Text.SetText(textData[5])
			rightWall1Text.SetPosition(textData[0], textData[1])
			if textData[4][0] != 1.0 and textData[4][1] != 1.0 and textData[4][2] != 1.0:
				rightWall1Text.SetFontColor(textData[4][0],textData[4][1],textData[4][2])
			rightWall1Text.SetOutline()
			rightWall1Text.Show()
			self.children["rightWall1%s"%textData[3]] = rightWall1Text

		rightWall1Gauge = BattlePassGauge()
		rightWall1Gauge.SetParent(rightWall1)
		rightWall1Gauge.MakeGauge(192)
		rightWall1Gauge.SetPercentage(0,100)
		rightWall1Gauge.SetPosition(5,115)
		rightWall1Gauge.Show()
		self.children["rightWall1Gauge"] = rightWall1Gauge

		shopBtn = ui.Button()
		shopBtn.SetParent(rightWall1)
		shopBtn.SetUpVisual(IMG_DIR+"shop_0.tga")
		shopBtn.SetOverVisual(IMG_DIR+"shop_1.tga")
		shopBtn.SetDownVisual(IMG_DIR+"shop_2.tga")
		shopBtn.SetPosition(10,145)
		shopBtn.SetEvent(self.ClickShop)
		shopBtn.Show()
		self.children["shopBtn"] = shopBtn

		checkBtn = ui.Button()
		checkBtn.SetParent(rightWall1)
		checkBtn.SetUpVisual(IMG_DIR+"reward_0.tga")
		checkBtn.SetOverVisual(IMG_DIR+"reward_1.tga")
		checkBtn.SetDownVisual(IMG_DIR+"reward_2.tga")
		checkBtn.SetPosition(10,145+shopBtn.GetHeight()+5)
		checkBtn.SetEvent(self.CheckBtn)
		checkBtn.Show()
		self.children["checkBtn"] = checkBtn

		rewardItems = ui.GridSlotWindow()
		rewardItems.SetParent(rightWall1)
		rewardItems.SetPosition(10+shopBtn.GetWidth()+5, 135)
		rewardItems.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		rewardItems.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		rewardItems.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		rewardItems.ArrangeSlot(0, 3, 2, 32, 32, 0, 0)
		rewardItems.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		rewardItems.RefreshSlot()
		rewardItems.Show()
		self.children["rewardItems"] = rewardItems


		rightBtn1 = ui.RadioButton()
		rightBtn1.SetParent(rightWall)
		rightBtn1.SetUpVisual(IMG_DIR+"right_table_button.tga")
		rightBtn1.SetOverVisual(IMG_DIR+"right_table_button.tga")
		rightBtn1.SetDownVisual(IMG_DIR+"right_table_button.tga")
		rightBtn1.SetPosition(101,5)
		rightBtn1.SetEvent(self.SetRightTable, 1)
		rightBtn1.Show()
		self.children["rightBtn1"] = rightBtn1

		deactiveWindow = ui.ThinBoardCircle()
		deactiveWindow.SetParent(self)
		deactiveWindow.SetSize(self.GetWidth()-11, self.GetHeight()-38)
		deactiveWindow.SetPosition(5,30)
		deactiveWindow.SetAlpha(0.8)
		#deactiveWindow.Show()
		self.children["deactiveWindow"] = deactiveWindow

		deactiveWindowText = MultiTextLine()
		deactiveWindowText.SetParent(deactiveWindow)
		deactiveWindowText.SetTextType("horizontal#left")
		deactiveWindowText.SetTextRange(20)
		deactiveWindowText.SetPosition(30,40)
		deactiveWindowText.SetText(localeInfo.BATTLEPASS_DEACTIVE_TEXT_1+"\n"+localeInfo.BATTLEPASS_DEACTIVE_TEXT_2)
		deactiveWindowText.Show()
		self.children["deactiveWindowText"] = deactiveWindowText

		deactiveWindowBtn = ui.Button()
		deactiveWindowBtn.SetParent(deactiveWindow)
		deactiveWindowBtn.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		deactiveWindowBtn.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		deactiveWindowBtn.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		deactiveWindowBtn.SetEvent(self.ClickDeactiveBtn)
		deactiveWindowBtn.SetText(localeInfo.UI_OK)
		deactiveWindowBtn.SetPosition(30, 90)
		deactiveWindowBtn.Show()
		self.children["deactiveWindowBtn"] = deactiveWindowBtn

		effectPtrList = []
		for j in xrange(3):
			effectAniImage = ui.AniImageBox()
			effectAniImage.SetParent(self)
			effectAniImage.SetDelay(6)
			for x in range(1,9):
				effectAniImage.AppendImage("d:/ymir work/ui/minigame/rumi/card_completion_effect/card_completion_eff%d.sub"%x)
			effectAniImage.SetPosition(50+(j*43), 100)
			#effectAniImage.Show()
			effectPtrList.append(effectAniImage)
		
		effectText = ui.AniImageBox()
		effectText.SetParent(self)
		effectText.SetDelay(6)
		for x in range(1,10):
			effectText.AppendImage("d:/ymir work/ui/minigame/rumi/card_completion_effect/card_completion_text_effect%d.sub"%x)
		effectText.SetPosition(80, 170)
		#effectText.Show()
		effectPtrList.append(effectText)

		self.children["effectList"] = effectPtrList

		self.SetRightTable(0)

	def ClickDeactiveBtn(self):
		self.children["deactiveWindow"].Hide()

	def HideSuccesAffect(self):
		self.effectStatus = False
		self.effectTime = 0
		for effect in self.children["effectList"]:
			effect.Hide()

	def ShowSuccesAffect(self):
		self.effectStatus = True
		self.effectTime = app.GetGlobalTimeStamp()+2
		for effect in self.children["effectList"]:
			effect.Show()

	def OverOutItem(self):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.HideToolTip()

	def OverInItem(self, slotIndex):
		interface = constInfo.GetInterfaceInstance()
		if interface:
			if interface.tooltipItem:
				interface.tooltipItem.SetItemToolTip(self.battlePassRewardList[slotIndex][0])

	def GetDungeonName(self, mapIndex):
		if mapIndex == 66:
			return "Devil Tower"
		return "None"

	def GetSubText(self, missionIndex, subValue):
		if not battlepass_mission_data.has_key(missionIndex):
			return ""
		missionData = battlepass_mission_data[missionIndex]
		if missionData["subtext"] == "":
			return ""
		if subValue == 0:
			return missionData["subtext"]+": "+"|cffea150a"+localeInfo.MISSION_SUB_ALL
		elif player.MISSION_BOSS==missionIndex or player.MISSION_MONSTER==missionIndex or player.MISSION_STONE==missionIndex:
			return missionData["subtext"]+": "+"|cffea150a"+nonplayer.GetMonsterName(subValue)
		elif player.MISSION_CATCH_FISH==missionIndex or player.MISSION_CRAFT_ITEM==missionIndex or player.MISSION_DESTROY_ITEM==missionIndex or player.MISSION_REFINE_ITEM==missionIndex or player.MISSION_SELL_ITEM==missionIndex:
			item.SelectItem(subValue)
			return missionData["subtext"]+": "+"|cffea150a"+item.GetItemName()
		elif missionIndex == player.MISSION_DUNGEON:
			return missionData["subtext"]+": "+"|cffea150a"+self.GetDungeonName(subValue)
		elif missionIndex == player.MISSION_KILLPLAYER:
			return missionData["subtext"]+": "+"|cffea150a"+str(subValue)

	def GetRemaining(self, missionIndex, missionMaxValue):
		if player.MISSION_PLAYTIME == missionIndex or player.MISSION_MOUNT_TIME == missionIndex:
			return localeInfo.MISSION_REMAINING+self.FormatTime(missionMaxValue)
		else:
			return localeInfo.MISSION_REMAINING+localeInfo.NumberToMoneyStringNEW(missionMaxValue)

	def GetCompleted(self, missionIndex, missionValue):
		if player.MISSION_PLAYTIME == missionIndex or player.MISSION_MOUNT_TIME == missionIndex:
			return localeInfo.MISSION_COMPLETED+self.FormatTime(missionValue)
		else:
			return localeInfo.MISSION_COMPLETED+localeInfo.NumberToMoneyStringNEW(missionValue)
	def GetMonthName(self, monthIndex):
		monthName = {
			1:localeInfo.EVENT_MONTH_1,
			2:localeInfo.EVENT_MONTH_2,
			3:localeInfo.EVENT_MONTH_3,
			4:localeInfo.EVENT_MONTH_4,
			5:localeInfo.EVENT_MONTH_5,
			6:localeInfo.EVENT_MONTH_6,
			7:localeInfo.EVENT_MONTH_7,
			8:localeInfo.EVENT_MONTH_8,
			9:localeInfo.EVENT_MONTH_9,
			10:localeInfo.EVENT_MONTH_10,
			11:localeInfo.EVENT_MONTH_11,
			12:localeInfo.EVENT_MONTH_12
		}
		if monthName.has_key(monthIndex):
			return monthName[monthIndex]
		return "None"

	def CalculateCompleteMission(self, listBoxListPointer):
		xCount = 0
		for mission in listBoxListPointer:
			if mission.missionValue >= mission.missionMaxValue:
				xCount+=1
		return xCount

	def RefreshFirstPage(self, listboxIndex):
		listBoxList = self.children["listBox"].itemList
		if len(listBoxList) == 0:
			return

		selectedMission = listBoxList[listboxIndex]
		subText = self.GetSubText(selectedMission.missionIndex,selectedMission.missionSubValue)
		if subText != "":
			self.children["rightWall0Type"].SetText(subText)
			self.children["rightWall0Type"].Show()
		else:
			self.children["rightWall0Type"].Hide()

		remainingText = self.GetRemaining(selectedMission.missionIndex,selectedMission.missionMaxValue)
		self.children["rightWall0Remaining"].SetText(remainingText)

		completedText = self.GetCompleted(selectedMission.missionIndex,selectedMission.missionValue)
		self.children["rightWall0Completed"].SetText(completedText)

		if battlepass_mission_data.has_key(selectedMission.missionIndex):
			dungeonData = battlepass_mission_data[selectedMission.missionIndex]

			self.children["rightWall0Title"].SetText(dungeonData["name"])

			self.children["rightWall0Description"].SetText(dungeonData["description"])

			if self.pageIndex == 0:
				self.children["rightWall0"].LoadImage(IMG_DIR+"mission_right/"+dungeonData["image"]+".tga")

	def RefreshSecondPage(self, listboxIndex):
		listBoxList = self.children["listBox"].itemList
		if len(listBoxList) == 0:
			return

		dt = datetime.datetime.today()
		self.children["rightWall1Name"].SetText(localeInfo.MISSION_DATE_TEXT % (self.GetMonthName(dt.month),dt.year))
		if self.battlePassStatus==1:
			self.children["rightWall1Status"].SetText(localeInfo.MISSION_STATUS_ACTIVE)
		elif self.battlePassStatus==2:
			self.children["rightWall1Status"].SetText(localeInfo.MISSION_STATUS_DONE)
		else:
			self.children["rightWall1Status"].SetText(localeInfo.MISSION_STATUS_NOT_ACTIVE)
		self.children["rightWall1Task"].SetText(localeInfo.MISSION_TASK_COUNT % len(listBoxList))
		totalComplete = self.CalculateCompleteMission(listBoxList)
		self.children["rightWall1Completed"].SetText(localeInfo.MISSION_COMPLETED_COUNT % totalComplete)
		self.children["rightWall1Gauge"].SetPercentage(totalComplete,len(listBoxList))
		rewardSlots = self.children["rewardItems"]
		for i in xrange(3 * 2):
			rewardSlots.ClearSlot(i)
		index = 0
		for reward in self.battlePassRewardList:
			rewardSlots.SetItemSlot(index, reward[0], reward[1])
			index+=1
		rewardSlots.RefreshSlot()

		checkBtn = self.children["checkBtn"]
		if len(listBoxList) == totalComplete and self.battlePassStatus == 1:
			checkBtn.SetUpVisual(IMG_DIR+"reward_0.tga")
			checkBtn.SetOverVisual(IMG_DIR+"reward_1.tga")
			checkBtn.SetDownVisual(IMG_DIR+"reward_2.tga")
		else:
			checkBtn.SetUpVisual(IMG_DIR+"reward_0.tga")
			checkBtn.SetOverVisual(IMG_DIR+"reward_0.tga")
			checkBtn.SetDownVisual(IMG_DIR+"reward_0.tga")

	def ClickMission(self, listboxIndex):
		listBoxList = self.children["listBox"].itemList
		if len(listBoxList) == 0:
			return
		self.clickIndex = listboxIndex
		self.__ClickRadioButton(listBoxList,listboxIndex)
		self.RefreshFirstPage(listboxIndex)
		self.RefreshSecondPage(listboxIndex)
	def OnUpdate(self):
		if self.pageIndex == 1 and len(self.children["listBox"].itemList) > 0:
			leftTime = self.battlePassleftTime-app.GetGlobalTimeStamp()
			if leftTime <= 0:
				leftTime = 0
			self.children["rightWall1Time"].SetText(localeInfo.MISSION_LEFT_TIME % self.FormatTime(leftTime))

		if self.effectStatus:
			if app.GetGlobalTimeStamp() > self.effectTime:
				self.HideSuccesAffect()

	def SetRightTable(self, btnIndex):
		self.__ClickRadioButton([self.children["rightBtn0"],self.children["rightBtn1"]],btnIndex)
		self.children["rightWall"].LoadImage(IMG_DIR+"right_table_%d.tga"%btnIndex)
		self.pageIndex = btnIndex
		if self.pageIndex == 0:
			self.children["rightWall1"].Hide()
			wallStatistics = self.children["rightWall0"]
			if wallStatistics.GetWidth() == 0:
				wallStatistics.LoadImage(IMG_DIR+"mission_right/none.tga")
			wallStatistics.Show()
		elif self.pageIndex == 1:
			self.children["rightWall0"].Hide()
			wallInfo = self.children["rightWall1"]
			if wallInfo.GetWidth() == 0:
				wallInfo.LoadImage(IMG_DIR+"mission_right/special.tga")
			wallInfo.Show()
	def Open(self):
		if self.isSendPacket == False:
			net.SendChatPacket("/battle_pass info")
			self.isSendPacket = True
		else:
			if self.battlePassStatus == 0:
				self.children["deactiveWindow"].Show()
		self.Show()

		self.RefreshSecondPage(self.clickIndex)
		try:
			itemData = self.children["listBox"].itemList
			if itemData[self.clickIndex].missionIndex == missionIndex:
				self.RefreshFirstPage(self.clickIndex)
		except:
			pass

	def Close(self):
		self.Hide()
	def OnPressEscapeKey(self):
		self.Close()
		return True
	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			btn=buttonList[buttonIndex]
		except IndexError:
			return
		for eachButton in buttonList:
			eachButton.SetUp()
		btn.Down()

	def SetBattlePassStatusEx(self, status):
		self.battlePassStatus = status
		self.RefreshSecondPage(self.clickIndex)

		if self.battlePassStatus == 2:
			checkBtn = self.children["checkBtn"]
			checkBtn.SetUpVisual(IMG_DIR+"reward_0.tga")
			checkBtn.SetOverVisual(IMG_DIR+"reward_0.tga")
			checkBtn.SetDownVisual(IMG_DIR+"reward_0.tga")

	def SetBattlePassStatus(self, status, leftTime, reward):
		self.battlePassStatus = status
		self.battlePassleftTime = leftTime+app.GetGlobalTimeStamp()
		self.battlePassRewardList = []
		if len(reward) > 0:
			itemsSplit = reward.split("#")
			for rewardList in itemsSplit:
				rewardItem = rewardList.split("|")
				if len(rewardItem) != 2:
					continue
				if rewardItem[0].isdigit() == False or rewardItem[1].isdigit() == False:
					continue
				self.battlePassRewardList.append([int(rewardItem[0]),int(rewardItem[1])])

		if self.battlePassStatus == 2:
			itemData = self.children["listBox"].itemList
			for missionData in itemData:
				missionData.SetMission(missionData.missionMaxValue)

		if self.battlePassStatus == 0:
			self.children["deactiveWindow"].Show()

		self.ClickMission(0)
	def BattlePassClear(self):
		self.children["listBox"].RemoveAllItems()
	def SetMission(self, missionIndex, missionValue):
		itemData = self.children["listBox"].itemList
		for rewardItem in itemData:
			if rewardItem.missionIndex == missionIndex:
				rewardItem.SetMission(missionValue)
				if rewardItem.missionValue == rewardItem.missionMaxValue:
					self.ShowSuccesAffect()
				break
		if self.IsShow():
			self.RefreshSecondPage(self.clickIndex)
			try:
				if itemData[self.clickIndex].missionIndex == missionIndex:
					self.RefreshFirstPage(self.clickIndex)
			except:
				pass

	def FormatTime(self, seconds):
		second = int(seconds % 60)
		minute = int((seconds / 60) % 60)
		hour = int((seconds / 60) / 60) % 24
		day = int(int((seconds / 60) / 60) / 24)
		return localeInfo.BATTLEPASS_TIME_FORMAT % (day, hour, minute, second)

	def AppendMission(self, missionIndex, missionReward, missionValue, missionMaxValue, missionSubValue, missionVecIndex):
		if missionReward =="Empty":
			missionReward = ""
		listboxPtr = self.children["listBox"]
		listboxItem = self.BattlePassItem()
		listboxItem.LoadMission(missionIndex, missionReward, missionValue, missionMaxValue, missionSubValue, missionVecIndex)
		listboxPtr.AppendItem(listboxItem)
		listboxPtr.itemList.sort()
		listboxPtr.SetBasePos(0)
		for missionItem in listboxPtr.itemList:
			missionItem.SetEvent(self.ClickMission, listboxPtr.itemList.index(missionItem))
		if len(listboxPtr.itemList) > 5:
			self.children["scrollBar"].Show()

	def CheckBtn(self):
		listBoxList = self.children["listBox"].itemList
		if self.CalculateCompleteMission(listBoxList) != len(listBoxList):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.BATTLEPASS_REWARD_INFO)
			return
		if self.battlePassStatus == 2:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.BATTLEPASS_ALREADY_GET_REWARD)
			return
		net.SendChatPacket("/battle_pass reward")
	def ClickShop(self):
		net.SendChatPacket("/open_shop 15")

