import uiScriptLocale
import grp
import localeInfo

BOARD_X = 263
BOARD_Y = 352

COLOR_LINE = 0xff5b5e5e
COLOR_PERCENTAGE = 0xffaaf698
LARGE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_05.sub"

window = {
	"name" : "RefineRarityDialog",
	"style" : ("movable", "float",),
	"x" : SCREEN_WIDTH - 400,
	"y" : 70 * 800 / SCREEN_HEIGHT,
	"width" : 0,
	"height" : 0,
	"children" :
	(
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : 0,
			"height" : 0,
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),
					"x" : 8,
					"y" : 8,
					"width" : 0,
					"color" : "red",
					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",
							"text" : uiScriptLocale.REFINE_TTILE,
							"horizontal_align" : "center",
							"text_horizontal_align" : "center",
							"x" : 0,
							"y" : 3,
						},
					),
				},
				{
					"name" : "Background",
					"type" : "bar",
					"x" : 7,
					"y" : 32,
					"width" : BOARD_X - 14,
					"height" : BOARD_Y - 40,
					"color" : grp.GenerateColor(0.0, 0.0, 0.0, 0.5),
				},
				{
					"name" : "AttachNextItem",
					"type" : "image",
					"x" : 123,
					"y" : 95,
					"image" : "d:/ymir work/ui/game/windows/attach_metin_arrow.sub",
				},
				{
					"name": "ContentDesign",
					"type":"horizontalbar",
					"x": 14,
					"y": 35,
					"width": 235,
					"children" :
					(
						{
							"name": "curItem",
							"type":  "text",
							"x": 5,
							"y": 2,
							"text": localeInfo.REFINE_CURRENT_ITEM,
						},
						{
							"name": "nextItem",
							"type":  "text",
							"x": 160,
							"y": 2,
							"text": localeInfo.REFINE_NEXT_ITEM,
						},
					),
				},
				{
					"name": "DesignNeedItens",
					"type":"horizontalbar",
					"x": 14,
					"y": 172,
					"width": 235,
					"children" :
					(
						{
							"name": "needItems",
							"type":  "text",
							"x": 5,
							"y": 2,
							"text": localeInfo.REFINE_NEED_ITEMS,
						},
					),
				},
				{
					"name": "DesignIncrease",
					"type":"horizontalbar",
					"x": 14,
					"y": 211,
					"width": 235,
					"children" :
					(
						{
							"name": "SuccessPercentage",
							"type":  "text",
							"x": 5,
							"y": 2,
							"text": "",
						},
						{
							"name": "SuccessPercentageIncreased",
							"type":  "text",
							"x": 165,
							"y": 2,
							"color" : 0xffe2ff75,
							"text": "",
						},
					),
				},
				{
					"name": "DesignCost",
					"type":"horizontalbar",
					"x": 14,
					"y": 241,
					"width": 235,
					"children" :
					(
						{
							"name": "textLine",
							"type": "text",
							"x": 5,
							"y": 2,
							"text": localeInfo.REFINE_COST_UPGRADE,
						},
					),
				},
				{
					"name" : "SlotCost",
					"type" : "button",
					"x" : 74,
					"y" : 272,
					"default_image" : LARGE_VALUE_FILE,
					"over_image" : LARGE_VALUE_FILE,
					"down_image" : LARGE_VALUE_FILE,
					"children" :
					(
						{
							"name":"Money_Icon",
							"type": "image",
							"x": -18,
							"y": 2,
							"image": "d:/ymir work/ui/game/windows/money_icon.sub",
						},
						{
							"name" : "Cost",
							"type" : "text",
							"x" : 3,
							"y" : 3,
							"horizontal_align" : "right",
							"text_horizontal_align" : "right",
							"text" : "",
						},
					),
				},
				{
					"name" : "AcceptButton",
					"type" : "button",
					"x" : 30,
					"y" : 311,
					"text" : uiScriptLocale.OK,
					"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",
				},
				{
					"name" : "CancelButton",
					"type" : "button",
					"x" : 150,
					"y" : 311,
					"text" : uiScriptLocale.CANCEL,
					"default_image" : "d:/ymir work/ui/public/Large_Button_01.sub",
					"over_image" : "d:/ymir work/ui/public/Large_Button_02.sub",
					"down_image" : "d:/ymir work/ui/public/Large_Button_03.sub",
				},
			),
		},
	),
}