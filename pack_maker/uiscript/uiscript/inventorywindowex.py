import uiScriptLocale
import item
import app
import player

HEIGHT_W = 570
RUTA_IMG_SPECIAL_INV = "buttons_inv/"
RUTA_IMG_NEW_INV = "rework_inv/"
BUTTONS_COUNT = 9
BOARD_WIDTH = 37
BOARD_HEIGHT = (60 * BUTTONS_COUNT)

NEW_INV_DESIGN = "d:/ymir work/ui/game/new_inventory/"

EQUIPMENT_START_INDEX = player.EQUIPMENT_SLOT_START
# CHANGE_EQUIP_START_INDEX = player.CHANGE_EQUIP_SLOT_START

window = {
	"name" : "InventoryWindow",

	## 600 - (width + ????? ?? ??? 24 px)
	"x" : SCREEN_WIDTH - 210,
	"y" : SCREEN_HEIGHT - 600,

	"style" : ("movable", "float",),

	"width" : 199,
	"height" : 566,

	"children" :
	(
		{
			"name" : "board",
			"type" : "bar",
			"x" : 0,
			"y" : 0,
			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,
			"color" : 0x00000000,
			"children" : 
			(

				## Button1
				{
					"name" : "Button1",
					"type" : "button",

					"x" : 0,
					"y" : 80,

					"tooltip_text" : "Switchbot",
					
					"tooltip_x" : -70,
					"tooltip_y" : 10,
					
					"default_image" : "inventory/switchbot_1.tga",
					"over_image" : "inventory/switchbot_2.tga",
					"down_image" : "inventory/switchbot_3.tga",
				},
				## Button2
				{
					"name" : "Button2",
					"type" : "button",

					"x" : 0,
					"y" : 120,

					"tooltip_text" : "Panel Dungeon",
					
					"tooltip_x" : -70,
					"tooltip_y" : 10,
					
					"default_image" : "inventory/dunges_1.tga",
					"over_image" : "inventory/dunges_2.tga",
					"down_image" : "inventory/dunges_1.tga",
				},
				## Button3
				{
					"name" : "Button3",
					"type" : "button",

					"x" : 0,
					"y" : 160,

					"tooltip_text" : "Biolog",
					
					"tooltip_x" : -70,
					"tooltip_y" : 10,
					
					"default_image" : "inventory/zubl_1.tga",
					"over_image" : "inventory/zubl_2.tga",
					"down_image" : "inventory/zubl_1.tga",
				},
				## Button4
				{
					"name" : "Button4",
					"type" : "button",

					"x" : 0,
					"y" : 200,

					"tooltip_text" : "Teleportaèní Panel",
					
					"tooltip_x" : -70,
					"tooltip_y" : 10,
					
					"default_image" : "inventory/teleport_1.tga",
					"over_image" : "inventory/teleport_2.tga",
					"down_image" : "inventory/teleport_3.tga",
				},
				## Button5
				{
					"name" : "Button5",
					"type" : "button",

					"x" : 0,
					"y" : 240,

					"tooltip_text" : "Battle-Pass",
					
					"tooltip_x" : -70,
					"tooltip_y" : 10,
					
					"default_image" : "inventory/batt_1.tga",
					"over_image" : "inventory/batt_2.tga",
					"down_image" : "inventory/batt_1.tga",
				},
				## Button6
				{
					"name" : "Button6",
					"type" : "button",

					"x" : 0,
					"y" : 280,

					"tooltip_text" : "Systém Buff",
					
					"tooltip_x" : -70,
					"tooltip_y" : 10,
					
					"default_image" : "inventory/bufs_1.tga",
					"over_image" : "inventory/bufs_2.tga",
					"down_image" : "inventory/bufs_1.tga",
				},
                ## Button7
				{
					"name" : "Button7",
					"type" : "button",

					"x" : 0,
					"y" : 320,

					"tooltip_text" : "Wikipedie Nethis",
					
					"tooltip_x" : -70,
					"tooltip_y" : 10,
					
					"default_image" : "inventory/wiki_1.tga",
					"over_image" : "inventory/wiki_2.tga",
					"down_image" : "inventory/wiki_3.tga",
				},
                ## Button8
				{
					"name" : "Button8",
					"type" : "button",

					"x" : 0,
					"y" : 360,

					"tooltip_text" : "Hledání OfflineShop",
					
					"tooltip_x" : -70,
					"tooltip_y" : 10,
					
					"default_image" : "inventory/hledan_1.tga",
					"over_image" : "inventory/hledan_2.tga",
					"down_image" : "inventory/hledan_1.tga",
				},
                ## Button9
				{
					"name" : "Button9",
					"type" : "button",

					"x" : 0,
					"y" : 400,

					"tooltip_text" : "Auto-Lov",
					
					"tooltip_x" : -70,
					"tooltip_y" : 10,
					
					"default_image" : "inventory/aecial_1.tga",
					"over_image" : "inventory/aecial_2.tga",
					"down_image" : "inventory/aecial_1.tga",
				},
			),
		},
		## Inventory, Equipment Slots
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 37,
			"y" : 0,

			"width" : 176,
			"height" : 544,

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
				#{
				#	"name" : "Change_Equip_Tab_01",
				#	"type" : "radio_button",
				#
				#	"x" : 10,
				#	"y" : 32,
				#
				#	"default_image" : NEW_INV_DESIGN+"equip_0.tga",
				#	"over_image" : NEW_INV_DESIGN+"equip_1.tga",
				#	"down_image" : NEW_INV_DESIGN+"equip_2.tga",
				#
				#	"tooltip_text" : uiScriptLocale.CHANGE_EQUIP_1,
				#
				#	"children" :
				#	(
				#		{
				#			"name" : "Change_Equip_01_Print",
				#			"type" : "text",
				#
				#			"x" : 0,
				#			"y" : 0,
				#
				#			"all_align" : "center",
				#
				#			"text" : "I",
				#		},
				#	),
				#},
				#
				#{
				#	"name" : "Change_Equip_Tab_02",
				#	"type" : "radio_button",
				#
				#	"x" : 10+30,
				#	"y" : 32,
				#
				#	"default_image" : NEW_INV_DESIGN+"equip_0.tga",
				#	"over_image" : NEW_INV_DESIGN+"equip_1.tga",
				#	"down_image" : NEW_INV_DESIGN+"equip_2.tga",
				#
				#	"tooltip_text" : uiScriptLocale.CHANGE_EQUIP_2,
				#
				#	"children" :
				#	(
				#		{
				#			"name" : "Change_Equip_02_Print",
				#			"type" : "text",
				#
				#			"x" : 0,
				#			"y" : 0,
				#
				#			"all_align" : "center",
				#
				#			"text" : "II",
				#		},
				#	),
				#},
				#
				#{
				#	"name" : "Change_Equip_Tab_03",
				#	"type" : "radio_button",
				#
				#	"x" : 10+(30*2),
				#	"y" : 32,
				#
				#	"default_image" : NEW_INV_DESIGN+"equip_0.tga",
				#	"over_image" : NEW_INV_DESIGN+"equip_1.tga",
				#	"down_image" : NEW_INV_DESIGN+"equip_2.tga",
				#
				#	"tooltip_text" : uiScriptLocale.CHANGE_EQUIP_3,
				#
				#	"children" :
				#	(
				#		{
				#			"name" : "Change_Equip_03_Print",
				#			"type" : "text",
				#
				#			"x" : 0,
				#			"y" : 0,
				#
				#			"all_align" : "center",
				#
				#			"text" : "III",
				#		},
				#	),
				#},
				#
				#{
				#	"name" : "Change_Equip_Tab_04",
				#	"type" : "radio_button",
				#
				#	"x" : 10+(30*3),
				#	"y" : 32,
				#
				#	"default_image" : NEW_INV_DESIGN+"equip_0.tga",
				#	"over_image" : NEW_INV_DESIGN+"equip_1.tga",
				#	"down_image" : NEW_INV_DESIGN+"equip_2.tga",
				#
				#	"tooltip_text" : uiScriptLocale.CHANGE_EQUIP_4,
				#
				#	"children" :
				#	(
				#		{
				#			"name" : "Change_Equip_04_Print",
				#			"type" : "text",
				#
				#			"x" : 0,
				#			"y" : 0,
				#
				#			"all_align" : "center",
				#
				#			"text" : "IV",
				#		},
				#	),
				#},



				#{
				#	"name" : "ChangeEquipButton",
				#	"type" : "button",
				#
				#	"x" : 135,
				#	"y" : 32,
				#
				#	"tooltip_text" : uiScriptLocale.CHANGE_EQUIP,
				#
				#	"default_image" : NEW_INV_DESIGN+"confirm_0.tga",
				#	"over_image" : NEW_INV_DESIGN+"confirm_1.tga",
				#	"down_image" : NEW_INV_DESIGN+"confirm_2.tga",
				#},



				## Equipment Slot
				{
					"name" : "Equipment_Base",
					"type" : "image",

					"x" : 10,
					"y" : 33,

					"image" : RUTA_IMG_NEW_INV+"new_equipment_bg.tga",

					"children" :
					(

						{
							"name" : "EquipmentSlot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 150,
							"height" : 182,

							"slot" : (
								{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
								{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},
								{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":67, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":35, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+7, "x":2, "y":145, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+8, "x":75, "y":145, "width":32, "height":32},
								# {"index":item.COSTUME_SLOT_START + 3, "x":114, "y":2, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+9, "x":114, "y":2, "width":32, "height":32},
								{"index":EQUIPMENT_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},

								# {"index":EQUIPMENT_START_INDEX+11, "x":39, "y":106, "width":32, "height":32},
								# {"index":EQUIPMENT_START_INDEX+12, "x":74, "y":2, "width":32, "height":32},

								## ? ??1
								# {"index":item.EQUIPMENT_RING1, "x":2, "y":116, "width":32, "height":32},
								## ? ??2
								# {"index":item.EQUIPMENT_RING2, "x":75, "y":116, "width":32, "height":32},
								## ? ??
								{"index":item.EQUIPMENT_BELT, "x":39, "y":106, "width":32, "height":32},

								{"index":item.EQUIPMENT_PENDANT, "x":2, "y":106, "width":32, "height":32},
								#{"index":item.EQUIPMENT_GLOVE, "x":2, "y":106, "width":32, "height":32},
							),
						},

						#{
						#	"name" : "ChangeEquipment",
						#	"type" : "slot",
						#
						#	"x" : 3,
						#	"y" : 3,
						#
						#	"width" : 150,
						#	"height" : 182,
						#
						#	"slot" : (
						#				{"index":CHANGE_EQUIP_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
						#				{"index":CHANGE_EQUIP_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
						#				{"index":CHANGE_EQUIP_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},
						#				{"index":CHANGE_EQUIP_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
						#				{"index":CHANGE_EQUIP_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},
						#				{"index":CHANGE_EQUIP_START_INDEX+5, "x":114, "y":67, "width":32, "height":32},
						#				{"index":CHANGE_EQUIP_START_INDEX+6, "x":114, "y":35, "width":32, "height":32},
						#				#{"index":CHANGE_EQUIP_START_INDEX+7, "x":2, "y":145, "width":32, "height":32},
						#				#{"index":CHANGE_EQUIP_START_INDEX+8, "x":75, "y":145, "width":32, "height":32},
						#				{"index":CHANGE_EQUIP_START_INDEX+22, "x":114, "y":2, "width":32, "height":32},
						#				{"index":CHANGE_EQUIP_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},
						#				{"index":CHANGE_EQUIP_START_INDEX+27, "x":74, "y":96, "width":32, "height":32},
						#				{"index":CHANGE_EQUIP_START_INDEX+28, "x":74+40, "y":96, "width":32, "height":32},
						#				{"index":CHANGE_EQUIP_START_INDEX+31, "x":74, "y":2, "width":32, "height":32},
						#				{"index":CHANGE_EQUIP_START_INDEX+30, "x":2, "y":106, "width":32, "height":32},
						#			),
						#},

						{
							"name" : "CostumeButton",
							"type" : "button",
							"x" : 5+74,
							"y" : 3+2,
							"tooltip_text" : uiScriptLocale.COSTUME_TITLE,
							"tooltip_x": -45,
							"tooltip_y": 7,
							"default_image" : NEW_INV_DESIGN+"Costume_0.tga",
							"over_image" : NEW_INV_DESIGN+"Costume_1.tga",
							"down_image" : NEW_INV_DESIGN+"Costume_2.tga",
						},

						{
							"name" : "DSSButton",
							"type" : "button",
							"x" : 113,
							"y" : 107,
							"tooltip_text" : uiScriptLocale.TASKBAR_DRAGON_SOUL,
							"default_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_01.tga",
							"over_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_02.tga",
							"down_image" : "d:/ymir work/ui/dragonsoul/dss_inventory_button_03.tga",
						},
						
						{
							"name" : "NewInvButton",
							"type" : "button",
							"x" : 115,
							"y" : 107+40,
							"tooltip_text" : uiScriptLocale.SPECIAL_STORAGE,
							"tooltip_x": -45,
							"tooltip_y": 7,
							"default_image" : NEW_INV_DESIGN+"storage_0.tga",
							"over_image" : NEW_INV_DESIGN+"storage_1.tga",
							"down_image" : NEW_INV_DESIGN+"storage_2.tga",
						},

						{
							"name" : "OfflineShopButton",
							"type" : "button",
							"x" : 113-35,
							"y" : 107,
							"tooltip_text" : uiScriptLocale.OFFLINE_SHOP_TITLE,
							"tooltip_x": -45,
							"tooltip_y": 7,
							"default_image" : NEW_INV_DESIGN+"shop_0.tga",
							"over_image" : NEW_INV_DESIGN+"shop_1.tga",
							"down_image" : NEW_INV_DESIGN+"shop_2.tga",
						},

						{
							"name" : "Equipment_Tab_01",
							"type" : "radio_button",

							"x" : 86,
							"y" : 161,

							"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
							"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
							"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

							"children" :
							(
								{
									"name" : "Equipment_Tab_01_Print",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "I",
								},
							),
						},
						{
							"name" : "Equipment_Tab_02",
							"type" : "radio_button",

							"x" : 86 + 32,
							"y" : 161,

							"default_image" : "d:/ymir work/ui/game/windows/tab_button_small_01.sub",
							"over_image" : "d:/ymir work/ui/game/windows/tab_button_small_02.sub",
							"down_image" : "d:/ymir work/ui/game/windows/tab_button_small_03.sub",

							"children" :
							(
								{
									"name" : "Equipment_Tab_02_Print",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "II",
								},
							),
						},

					),
				},

				{
					"name" : "Inventory_Tab_01",
					"type" : "radio_button",

					"x" : 10,
					"y" : 33 + 191,

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

					#"x" : 10 + 78,
					"x" : 10 + 39,
					"y" : 33 + 191,

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
					"y" : 33 + 191,

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
					"y" : 33 + 191,

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

				## Item Slot
				{
					"name" : "ItemSlot",
					"type" : "grid_table",

					"x" : 8,
					"y" : 246,

					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 9,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub"
				},

				## Print
				{
					"name":"Money_Slot",
					"type":"button",

					"x":8,
					"y":29,

					"horizontal_align":"center",
					"vertical_align":"bottom",

					"default_image" : "icon_barra/barra_yang.tga",
					"over_image" : "icon_barra/barra_yang.tga",
					"down_image" : "icon_barra/barra_yang.tga",

					"children" :
					(
						{
							"name":"Money_Icon",
							"type":"image",

							"x":-18,
							"y":2,

							"image":"d:/ymir work/ui/game/windows/money_icon.sub",
						},

						{
							"name" : "Money",
							"type" : "text",

							"x" : 3,
							"y" : 2,

							"horizontal_align" : "right",
							"text_horizontal_align" : "right",

							"text" : "123456789",
						},
					),
				},

			),
		},
	),
}