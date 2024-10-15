import localeInfo

NEW = "d:/ymir work/ui/game/365_offlineshop/"

window = {
	"name" : "OfflineShopBuilder", # VENTANA
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float", "animate",),
	"width" : 184*2-15,
	"height" : 280+26+20+60,
	"children" :
	(
		{
			"name" : "Board", # TITULO
			"type" : "board_with_titlebar",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : 184*2-11,
			"height" : 275+26+20+60,
			"title" : localeInfo.OFFLINE_SHOP_TITLE,
			"children" :
			(
			{
				"name" : "MainWindow", # BG 
				"type" : "image",
				"x" : 10,
				"y" : 33,
				"width" : 184*2-15,
				"height" : 295+26+20+20,
				"image" : "d:/ymir work/ui/game/365_offlineshop/bg.tga",
				"children" :
				(
					{
						"name" : "ItemSlot", # RANURAS SLOT #1
						"type" : "grid_table",
						"x" : 7,
						"y" : 27 + 30-19,
						"start_index" : 0,
						"x_count" : 5,
						"y_count" : 8,
						"x_step" : 32,
						"y_step" : 32,
						"image" : "d:/ymir work/ui/public/Slot_Base.sub",
					},
					{
						"name" : "ItemSlot2", # RANURAS SLOT #1
						"type" : "grid_table",
						"x" : 167+0,
						"y" : 27 + 30-19,
						"start_index" : 0,
						"x_count" : 5,
						"y_count" : 8,
						"x_step" : 32,
						"y_step" : 32,
						"image" : "d:/ymir work/ui/public/Slot_Base.sub",
					},
					{
						"name" : "time_slot",
						"x" : 200,
						"y" : 3,
						"width" : 200,
						"height" : 25,
						"children" :
						(
							{
								"name" : "time_btn", # AUMENTAR TIEMPO
								"type" : "button",
								"x" : 110,
								"y": -2,
								"default_image" : NEW+"time_0.tga",
								"over_image" : NEW+"time_1.tga",
								"down_image" : NEW+"time_2.tga",
							},
							{
								"name" : "time",
								"type" : "text",
								"x" : -50,
								"y" : 3,
								"horizontal_align" : "center",
								"text_horizontal_align" : "center",
								"text" : "0",
								"fontname" : "Tahoma:12",
							},
						),
					},
				),
			},
			{
				"name" : "LogsWindow",
				"type" : "window",
				"x" : 5,
				"y" : 40,
				"width" : 545,
				"height" : 295+26+20+50,
				"children" :
				(
					{
						"name" : "ListBox",
						"type" : "listboxex",
						"x" : 5,
						"y" : 43,
						"width" : 184*2-15,
						"height" : 38*40,
						"viewcount" : 10,
					},
					{
						"name" : "ScrollBar",
						"type" : "scrollbar_new",
						"x" : 12+520,
						"y" : 35,
						"size" : 315,
					},
				),
			},
			{
				"name" : "NameSlot",
				"x" : 50,
				"y" :33,
				"width" : 280,
				"height" : 25,
				"children" :
				(
					{
						"name" : "NameLine",
						"type" : "editline",
						"x" : -4,
						"y" : 6,
						"width" : 280,
						"height" : 20,
						"input_limit" :20,
						"text" : "NULL",
					},

					{
						"name" : "refresh_title",
						"type" : "button",
						"x" : 101,
						"y": 1,
						"default_image" : NEW+"set_ok_0.tga",
						"over_image" : NEW+"set_ok_1.tga",
						"down_image" : NEW+"set_ok_2.tga",
					},
				),
			},
			{
				"name" : "Money_Slot", # YANG RETIRAR
				"x" : 17+20,
				"y" : 333,
				"width" : 90 + 75,
				"height" : 25,
				"children" :
				(
					{
						"name" : "refresh_yang",
						"type" : "button",
						"x" : 142,
						"y": 5,
						"default_image" : NEW+"retirar_yang_0.tga",
						"over_image" : NEW+"retirar_yang_1.tga",
						"down_image" : NEW+"retirar_yang_2.tga",
					},
					{
						"name" : "Money",
						"type" : "text",
						"x" : 90,
						"y" : 11,
						"horizontal_align" : "right",
						"text_horizontal_align" : "center",
						"text" : "0",
						"fontname" : "Tahoma:12",
					},
				),
			},
			{
				"name" : "FirstButton",
				"type" : "button",
				"x" : 217,
				"y": 337,
				"width" : 61,
				"height" : 21,
				"default_image" : NEW+"close_shop_0.tga",
				"over_image" : NEW+"close_shop_1.tga",
				"down_image" : NEW+"close_shop_2.tga",
				"text" : localeInfo.OFFLINESHOP_CLOSE,
				"fontname" : "Tahoma:12",
			},
			),
		},
	),
}

