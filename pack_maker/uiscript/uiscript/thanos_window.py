import localeInfo, uiScriptLocale, item
WIDTH = 575
HEIGHT = 415
WIDTH_GAP = 5
HEIGHT_GAP = 4

SLOT1_POS_X = 41
SLOT2_POS_X = 41
SLOT3_POS_X = 41
SLOT4_POS_X = 503
SLOT5_POS_X = 503
SLOT6_POS_X = 503

SLOT1_POS_Y = 98
SLOT2_POS_Y = 188
SLOT3_POS_Y = 279
SLOT4_POS_Y = 98
SLOT5_POS_Y = 188
SLOT6_POS_Y = 279

TEXT1_POS_X = 88
TEXT2_POS_X = 88
TEXT3_POS_X = 88
TEXT4_POS_X = 422
TEXT5_POS_X = 422
TEXT6_POS_X = 422

TEXT1_POS_Y = 104
TEXT2_POS_Y = 196
TEXT3_POS_Y = 285
TEXT4_POS_Y = 104
TEXT5_POS_Y = 196
TEXT6_POS_Y = 285

SLOT_START = item.GLOVE_SLOT_START

WIDTH_FP = WIDTH - WIDTH_GAP # width For Pos
HEIGHT_FP = HEIGHT - HEIGHT_GAP # height For Pos
window = {
	"name" : "ThanosMain","x" : SCREEN_WIDTH / 2,"y" : SCREEN_HEIGHT / 2,"width" : WIDTH,"height" : HEIGHT,
	"style" : ("movable", "float","limit",),
	"children" :[
		{
			"name" : "ThanosBoard","type" : "image","x" : 0,"y" : 0,"width" : WIDTH,"height" : HEIGHT,
			"image" : "d:/ymir work/thanos/thanos_bg.tga",
			"style" : ("attach",),
			"children" :[
				{ "name" : "itemSlotLeft", "type" : "slot", "x" : SLOT1_POS_X, "y" : SLOT1_POS_Y, #"style" : ("float",),
					"width" : 32,
					"height" : (SLOT3_POS_Y - SLOT1_POS_Y) + 32,
					"slot" :(
						{"index": SLOT_START+0, "x": 0,"y": SLOT1_POS_Y - SLOT1_POS_Y, "width":32, "height":32,},
						{"index": SLOT_START+1, "x": 0,"y": SLOT2_POS_Y - SLOT1_POS_Y, "width":32, "height":32,},
						{"index": SLOT_START+2, "x": 0,"y": SLOT3_POS_Y - SLOT1_POS_Y, "width":32, "height":32,},
					),
				},
				{ "name" : "itemSlotRight", "type" : "slot", "x" : SLOT4_POS_X, "y" : SLOT4_POS_Y, #"style" : ("float",),
					"width" : 32,
					"height" : (SLOT6_POS_Y - SLOT4_POS_Y) + 32,
					"slot" :(
						{"index": SLOT_START+3, "x": 0,"y": SLOT4_POS_Y - SLOT4_POS_Y, "width":32, "height":32,},
						{"index": SLOT_START+4, "x": 0,"y": SLOT5_POS_Y - SLOT4_POS_Y, "width":32, "height":32,},
						{"index": SLOT_START+5, "x": 0,"y": SLOT6_POS_Y - SLOT4_POS_Y, "width":32, "height":32,},
					),
				},

				{"name" : "itemName_1","type" : "text", "y" : TEXT1_POS_Y,"x" : TEXT1_POS_X, "text" : "" },
				{"name" : "itemName_2","type" : "text", "y" : TEXT2_POS_Y,"x" : TEXT2_POS_X, "text" : "" },
				{"name" : "itemName_3","type" : "text", "y" : TEXT3_POS_Y,"x" : TEXT3_POS_X, "text" : "" },
				{"name" : "itemName_4","type" : "text", "y" : TEXT4_POS_Y,"x" : TEXT4_POS_X, "text" : "" },
				{"name" : "itemName_5","type" : "text", "y" : TEXT5_POS_Y,"x" : TEXT5_POS_X, "text" : "" },
				{"name" : "itemName_6","type" : "text", "y" : TEXT6_POS_Y,"x" : TEXT6_POS_X, "text" : "" },
				{
					"name" : "CloseButton", "type" : "button",
					"x" : WIDTH_FP - 52, # 52 is close button image's width
					"y" : 30,
					"default_image" : "d:/ymir work/thanos/close_norm.tga",
					"over_image" : "d:/ymir work/thanos/close_over.tga",
					"down_image" : "d:/ymir work/thanos/close_press.tga",
				},
			],
		},
	],
}