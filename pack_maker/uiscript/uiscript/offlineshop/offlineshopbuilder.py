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
				"image" : "d:/ymir work/ui/game/365_offlineshop/bg_create.tga",
				"children" :
				(
					{
							"name" : "NameSlot",
							# "type" : "slotbar",
							"x" : 125, # HOR
							"y" : 5,# VERT
							"width" : 250,
							"height" : 25,
							"children" :
							(
								{
									"name" : "NameLine", # NOMBRE DE SHOP
									"type" : "editline",
									"x" : 3,
									"y" : 5,
									"width" : 250,
									"height" : 20,
									"input_limit" : 20,
									"text" : "....",
								},
							),
						},
						
						{
							"name" : "Money_Slot",
							"x" : 17+20,
							"y" : 333,
							"width" : 90 + 75,
							"height" : 25,
							"children" :
							(
								{
									"name" : "Money", # YANG
									"type" : "text",
									"x" : 90,
									"y" : -24,
									"horizontal_align" : "right",
									"text_horizontal_align" : "center",
									"text" : "0",
									"fontname" : "Tahoma:12",
								},
							),
						},
						{
							"name" : "FirstButton", # BOTON CREATE
							"type" : "button",
							"x" : 205,
							"y": 304,
							"width" : 61,
							"height" : 21,
							"default_image" : NEW+"open_shop_0.tga",
							"over_image" : NEW+"open_shop_1.tga",
							"down_image" : NEW+"open_shop_2.tga",
							"text" : localeInfo.OFFLINESHOP_CREATE,
							"fontname" : "Tahoma:12",
						},
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
					),
				},
			),
		},
	),
}

