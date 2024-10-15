import uiScriptLocale

BOARD_WIDTH = 200
BOARD_HEIGHT = 100
TITLE_MS = 13

window = {
	"name" : "QuestionDialog_ConfirmDestroy",
	"style" : ("attach", "float",),

	"x" : SCREEN_WIDTH/2 - 125,
	"y" : SCREEN_HEIGHT/2 - 52,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar_without_button",
					"style" : ("attach",),
					"x" : 6,
					"y" : 6,
					"width" : BOARD_WIDTH - TITLE_MS,
					"color" : "yellow",
					"children" :
					(
						{
							"name":"TitleName",
							"type":"text",
							"x":BOARD_WIDTH/2-10,
							"y":3,
							"text":uiScriptLocale.NEW_DROP_ITEM_TITLE_DESTROY,
							"text_horizontal_align":"center"
						},
					),
				},
				{
					"name" : "base_thinboard",
					"type" : "thinboard",

					"x" : 10,
					"y" : 32,

					"width" : BOARD_WIDTH - 20,
					"height" : BOARD_HEIGHT-42,
				},
				{
					"name" : "message",
					"type" : "text",

					"x" : 0,
					"y" : 45,

					"horizontal_align" : "center",
					"text" : uiScriptLocale.NEW_DROP_ITEM_MES_DESTROY,

					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "accept",
					"type" : "button",

					"x" : -40,
					"y" : 62,
					"horizontal_align" : "center",
					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				{
					"name" : "cancel",
					"type" : "button",

					"x" : 40,
					"y" : 62,
					"horizontal_align" : "center",
					"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
					"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
					"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
				},
			),
		},
	),
}