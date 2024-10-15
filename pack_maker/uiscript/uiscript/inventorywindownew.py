import uiScriptLocale

WINDOW_WIDTH = 176
WINDOW_HEIGHT = 434


RUTA_IMG_SPECIAL_INV = "buttons_inv/"
RUTA_IMG_NEW_INV = "rework_inv/"
NEW_INV_DESIGN = "d:/ymir work/ui/game/special_inventory/"

window = {
	"name" : "InventoryWindow",

	"x" : SCREEN_WIDTH - 176 - 287 - 10,
	"y" : SCREEN_HEIGHT - 37 - 525,

	"style" : ("movable", "float", "animate",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,
			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,
			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 161,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":77, "y":3, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center" },
					),
				},
				{
					"name" : "loadingImage",
					"type" : "expanded_image",
					"x" : 8+((32*5)/2),
					"y" : 33+((32*9)/2),
					"image" : "d:/ymir work/ui/load_.tga"
				},

				{
					"name" : "ItemSlot",
					"type" : "grid_table",
					"x" : 8,
					"y" : 33,
					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 9,
					"x_step" : 32,
					"y_step" : 32,
					"image" : "d:/ymir work/ui/public/Slot_Base.sub"
				},


				{
					"name" : "Inventory_Tab_01",
					"type" : "radio_button",
					"x" : 10,
					"y" : 33 + ( 9 * 32) + 5,
					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_1,
					"children" :
					(
						{
							"name" : "Inventory_Tab_01_Print",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : "I",
						},
					),
				},
				{
					"name" : "Inventory_Tab_02",
					"type" : "radio_button",
					"x" : 10 + 39,
					"y" : 33 + ( 9 * 32) + 5,
					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_2,
					"children" :
					(
						{
							"name" : "Inventory_Tab_02_Print",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : "II",
						},
					),
				},
				
				{
					"name" : "Inventory_Tab_03",
					"type" : "radio_button",
					"x" : 10 + 39 + 39,
					"y" : 33 + ( 9 * 32) + 5,
					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_3,
					"children" :
					(
						{
							"name" : "Inventory_Tab_03_Print",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : "III",
						},
					),
				},
				
				{
					"name" : "Inventory_Tab_04",
					"type" : "radio_button",
					"x" : 10 + 39 + 39 + 39,
					"y" : 33 + ( 9 * 32) + 5,
					"default_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_01.sub",
					"over_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_02.sub",
					"down_image" : "d:/ymir work/ui/game/windows/tab_button_large_half_03.sub",
					"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP_4,
					"children" :
					(
						{
							"name" : "Inventory_Tab_04_Print",
							"type" : "text",
							"x" : 0,
							"y" : 0,
							"all_align" : "center",
							"text" : "IV",
						},
					),
				},
				
				{
					"name" : "inventory_type_background", # SEPERATE IMG !
					"type" : "image",
					"x" : 10,
					"y" : 33 +(9*32)+5+20,
					"image" : NEW_INV_DESIGN+"bg_buttons.tga",
					"children" :
					(
						{
							"name" : "Inventory_Special_1",
							"type" : "radio_button",
							"x" : 5,
							"y" : 5,
							"default_image" : NEW_INV_DESIGN+"upp_storage_0.tga",
							"over_image" : NEW_INV_DESIGN+"upp_storage_1.tga",
							"down_image" : NEW_INV_DESIGN+"upp_storage_2.tga",
						},

						{
							"name" : "Inventory_Special_2",
							"type" : "radio_button",
							"x" : 2+(36*1)+(5*1),
							"y" : 5,
							"default_image" : NEW_INV_DESIGN+"book_storage_0.tga",
							"over_image" : NEW_INV_DESIGN+"book_storage_1.tga",
							"down_image" : NEW_INV_DESIGN+"book_storage_2.tga",
						},

						{
							"name" : "Inventory_Special_3",
							"type" : "radio_button",
							"x" : 2+(35*2)+(5*2),
							"y" : 5,
							"default_image" : NEW_INV_DESIGN+"stone_storage_0.tga",
							"over_image" : NEW_INV_DESIGN+"stone_storage_1.tga",
							"down_image" : NEW_INV_DESIGN+"stone_storage_2.tga",
						},

						{
							"name" : "Inventory_Special_4",
							"type" : "radio_button",
							"x" : 2+(34*3)+(5*3),
							"y" : 5,
							"default_image" : NEW_INV_DESIGN+"change_storage_0.tga",
							"over_image" : NEW_INV_DESIGN+"change_storage_1.tga",
							"down_image" : NEW_INV_DESIGN+"change_storage_2.tga",
						},
						
						{
							"name" : "Inventory_Special_5", # costme
							"type" : "radio_button",
							"x" : 5,
							"y" : 3+ 32 + 5,
							"default_image" : NEW_INV_DESIGN+"costume_storage_0.tga",
							"over_image" : NEW_INV_DESIGN+"costume_storage_1.tga",
							"down_image" : NEW_INV_DESIGN+"costume_storage_2.tga",
						},
						
						{
							"name" : "Inventory_Special_6", # safebox
							"type" : "radio_button",
							"x" : 1+(36*1)+(5*1),
							"y" : 3 + 32 + 5,
							"default_image" : NEW_INV_DESIGN+"normal_storage_0.tga",
							"over_image" : NEW_INV_DESIGN+"normal_storage_1.tga",
							"down_image" : NEW_INV_DESIGN+"normal_storage_2.tga",
						},
						
						{
							"name" : "Inventory_Special_7", # mall
							"type" : "radio_button",
							"x" : 1+(35*2)+(5*2),
							"y" : 3 + 32 + 5,
							"default_image" : NEW_INV_DESIGN+"ishop_storage_0.tga",
							"over_image" : NEW_INV_DESIGN+"ishop_storage_1.tga",
							"down_image" : NEW_INV_DESIGN+"ishop_storage_2.tga",
						},
					),
				},
			),
		},
	),
}

