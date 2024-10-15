import uiScriptLocale

BOARD_WIDTH = 239
BOARD_HEIGHT = 64 + (32 * 5)

TITLE_MS = 13

window = {
	"name" : "QuestionDialog",
	"style" : ("movable", "float",),
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
							"text":uiScriptLocale.NEW_DROP_ITEM_TITLE,
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
					"height" : BOARD_HEIGHT - 42,
				},
				{
					"name" : "ItemSlot",
					"type" : "grid_table",
					"x" : 25,
					# "y" : 43,
					"y" : 15 + 29 + (((32 * 5) / 2) - ((32 * 3) / 2)),
					"start_index" : 0,
					"x_count" : 1,
					"y_count" : 3,
					"x_step" : 32,
					"y_step" : 32,
					"image" : "d:/ymir work/ui/public/Slot_Base.sub"
				},
				{
					"name" : "accept",
					"type" : "button",
					"x" : 70,
					"y" : 15 + (32 * 1),
					"text" : uiScriptLocale.NEW_DROP_ITEM_LARGAR,
					"default_image" : "d:/ymir work/ui/public/select_btn_01.sub",
					"over_image" : "d:/ymir work/ui/public/select_btn_02.sub",
					"down_image" : "d:/ymir work/ui/public/select_btn_03.sub",
				},
				{
					"name" : "destroy",
					"type" : "button",
					"x" : 70,
					"y" : 15 + (32 * 2),
					# "text_color" : 0xFFe3af66,
					"text" : uiScriptLocale.DESTROY,
					"default_image" : "d:/ymir work/ui/public/select_btn_01.sub",
					"over_image" : "d:/ymir work/ui/public/select_btn_02.sub",
					"down_image" : "d:/ymir work/ui/public/select_btn_03.sub",
				},
				{
					"name" : "energy",
					"type" : "button",
					"x" : 70,
					"y" : 15 + (32 * 3),
					# "text_color" : 0xff34FF30,
					"text" : uiScriptLocale.EXTRACT_ENERGY_SHARD,
					"default_image" : "d:/ymir work/ui/public/select_btn_01.sub",
					"over_image" : "d:/ymir work/ui/public/select_btn_02.sub",
					"down_image" : "d:/ymir work/ui/public/select_btn_03.sub",
				},
				{
					"name" : "runas",
					"type" : "button",
					"x" : 70,
					"y" : 15 + (32 * 4),
					# "text_color" : 0xff7CA1FF,
					"text" : uiScriptLocale.EXTRACT_AURA_FROST_RUNE,
					"default_image" : "d:/ymir work/ui/public/select_btn_01.sub",
					"over_image" : "d:/ymir work/ui/public/select_btn_02.sub",
					"down_image" : "d:/ymir work/ui/public/select_btn_03.sub",
				},
				{
					"name" : "cancel",
					"type" : "button",
					"x" : 70,
					"y" : 15 + (32 * 5),
					"text" : uiScriptLocale.CANCEL,
					"default_image" : "d:/ymir work/ui/public/select_btn_01.sub",
					"over_image" : "d:/ymir work/ui/public/select_btn_02.sub",
					"down_image" : "d:/ymir work/ui/public/select_btn_03.sub",
				},
			),
		},
	),
}