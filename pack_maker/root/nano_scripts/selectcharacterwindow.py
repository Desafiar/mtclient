import uiScriptLocale
import nano_interface
import localeInfo

ROOT_PATH = "d:/ymir work/ui/public/"
LOCALE_PATH = uiScriptLocale.SELECT_PATH
BASE_PATH = "nano_interface/"
CHAR_SELECT = "nano_interface/select_character/"

BOARD_X = SCREEN_WIDTH * (65) / 800
BOARD_Y = SCREEN_HEIGHT * (220) / 600

BOARD_ITEM_ADD_POSITION = -40

AJUST = 50
EMPTY_FLAG = "nano_interface/animations/empty_flag/"
EMPTY_FLAG_BIG = "nano_interface/animations/big_empty_flag/"

window = {
	"name" : "SelectCharacterWindow",

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		## Board
		{
			"name" : "BackGround",
			"type" : "expanded_image",
			"x" : 0,
			"y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image": BASE_PATH + "background_shd.png",
		},

		{
			"name" : "proviewBoard",
			"type" : "window",

			"x" : (SCREEN_WIDTH/2) - 500,
			"y" : (SCREEN_HEIGHT/2) - 300,

			"width" : 1000,
			"height" : 600,
			"children" :
			(
				{
					"name" : "effect_0",
					"type" : "ani_image",

					"x" : 340+AJUST,
					"y" : 90,

					"delay" : 6,

					"images" :
					(
						EMPTY_FLAG_BIG + "big_empty_flag_00.png",
						EMPTY_FLAG_BIG + "big_empty_flag_01.png",
						EMPTY_FLAG_BIG + "big_empty_flag_02.png",
						EMPTY_FLAG_BIG + "big_empty_flag_03.png",
						EMPTY_FLAG_BIG + "big_empty_flag_04.png",
						EMPTY_FLAG_BIG + "big_empty_flag_05.png",
						EMPTY_FLAG_BIG + "big_empty_flag_06.png",
						EMPTY_FLAG_BIG + "big_empty_flag_07.png",
						EMPTY_FLAG_BIG + "big_empty_flag_08.png",
						EMPTY_FLAG_BIG + "big_empty_flag_09.png",
						EMPTY_FLAG_BIG + "big_empty_flag_10.png",
						EMPTY_FLAG_BIG + "big_empty_flag_11.png",
						EMPTY_FLAG_BIG + "big_empty_flag_12.png",
						EMPTY_FLAG_BIG + "big_empty_flag_13.png",
						EMPTY_FLAG_BIG + "big_empty_flag_14.png",
						EMPTY_FLAG_BIG + "big_empty_flag_15.png",
						EMPTY_FLAG_BIG + "big_empty_flag_16.png",
						EMPTY_FLAG_BIG + "big_empty_flag_17.png",
						EMPTY_FLAG_BIG + "big_empty_flag_18.png",
						EMPTY_FLAG_BIG + "big_empty_flag_19.png",
						EMPTY_FLAG_BIG + "big_empty_flag_20.png",
						EMPTY_FLAG_BIG + "big_empty_flag_21.png",
						EMPTY_FLAG_BIG + "big_empty_flag_22.png",
						EMPTY_FLAG_BIG + "big_empty_flag_23.png",
						EMPTY_FLAG_BIG + "big_empty_flag_24.png",
						EMPTY_FLAG_BIG + "big_empty_flag_25.png",
						EMPTY_FLAG_BIG + "big_empty_flag_26.png",
						EMPTY_FLAG_BIG + "big_empty_flag_27.png",

					)
				},
				{
					"name" : "effect_1",
					"type" : "ani_image",

					"x" : 540+AJUST,
					"y" : 100,

					"delay" : 6,

					"images" :
					(
						EMPTY_FLAG + "empty_flag_00.png",
						EMPTY_FLAG + "empty_flag_01.png",
						EMPTY_FLAG + "empty_flag_02.png",
						EMPTY_FLAG + "empty_flag_03.png",
						EMPTY_FLAG + "empty_flag_04.png",
						EMPTY_FLAG + "empty_flag_05.png",
						EMPTY_FLAG + "empty_flag_06.png",
						EMPTY_FLAG + "empty_flag_07.png",
						EMPTY_FLAG + "empty_flag_08.png",
						EMPTY_FLAG + "empty_flag_09.png",
						EMPTY_FLAG + "empty_flag_10.png",
						EMPTY_FLAG + "empty_flag_11.png",
						EMPTY_FLAG + "empty_flag_12.png",
						EMPTY_FLAG + "empty_flag_13.png",
						EMPTY_FLAG + "empty_flag_14.png",
						EMPTY_FLAG + "empty_flag_15.png",
						EMPTY_FLAG + "empty_flag_16.png",
						EMPTY_FLAG + "empty_flag_17.png",
						EMPTY_FLAG + "empty_flag_18.png",
						EMPTY_FLAG + "empty_flag_19.png",
						EMPTY_FLAG + "empty_flag_20.png",
						EMPTY_FLAG + "empty_flag_21.png",
						EMPTY_FLAG + "empty_flag_22.png",
						EMPTY_FLAG + "empty_flag_23.png",
						EMPTY_FLAG + "empty_flag_24.png",
						EMPTY_FLAG + "empty_flag_25.png",
						EMPTY_FLAG + "empty_flag_26.png",
						EMPTY_FLAG + "empty_flag_27.png",
						EMPTY_FLAG + "empty_flag_28.png",
						EMPTY_FLAG + "empty_flag_29.png",
						EMPTY_FLAG + "empty_flag_30.png",
						EMPTY_FLAG + "empty_flag_31.png",

					)
				},
				{
					"name" : "effect_2",
					"type" : "ani_image",

					"x" : 140+AJUST,
					"y" : 100,

					"delay" : 6,

					"images" :
					(
						EMPTY_FLAG + "empty_flag_00.png",
						EMPTY_FLAG + "empty_flag_01.png",
						EMPTY_FLAG + "empty_flag_02.png",
						EMPTY_FLAG + "empty_flag_03.png",
						EMPTY_FLAG + "empty_flag_04.png",
						EMPTY_FLAG + "empty_flag_05.png",
						EMPTY_FLAG + "empty_flag_06.png",
						EMPTY_FLAG + "empty_flag_07.png",
						EMPTY_FLAG + "empty_flag_08.png",
						EMPTY_FLAG + "empty_flag_09.png",
						EMPTY_FLAG + "empty_flag_10.png",
						EMPTY_FLAG + "empty_flag_11.png",
						EMPTY_FLAG + "empty_flag_12.png",
						EMPTY_FLAG + "empty_flag_13.png",
						EMPTY_FLAG + "empty_flag_14.png",
						EMPTY_FLAG + "empty_flag_15.png",
						EMPTY_FLAG + "empty_flag_16.png",
						EMPTY_FLAG + "empty_flag_17.png",
						EMPTY_FLAG + "empty_flag_18.png",
						EMPTY_FLAG + "empty_flag_19.png",
						EMPTY_FLAG + "empty_flag_20.png",
						EMPTY_FLAG + "empty_flag_21.png",
						EMPTY_FLAG + "empty_flag_22.png",
						EMPTY_FLAG + "empty_flag_23.png",
						EMPTY_FLAG + "empty_flag_24.png",
						EMPTY_FLAG + "empty_flag_25.png",
						EMPTY_FLAG + "empty_flag_26.png",
						EMPTY_FLAG + "empty_flag_27.png",
						EMPTY_FLAG + "empty_flag_28.png",
						EMPTY_FLAG + "empty_flag_29.png",
						EMPTY_FLAG + "empty_flag_30.png",
						EMPTY_FLAG + "empty_flag_31.png",

					)
				},
				{
					"name" : "effect_3",
					"type" : "ani_image",

					"x" : 20,
					"y" : 100,

					"delay" : 6,

					"images" :
					(
						EMPTY_FLAG + "empty_flag_00.png",
						EMPTY_FLAG + "empty_flag_01.png",
						EMPTY_FLAG + "empty_flag_02.png",
						EMPTY_FLAG + "empty_flag_03.png",
						EMPTY_FLAG + "empty_flag_04.png",
						EMPTY_FLAG + "empty_flag_05.png",
						EMPTY_FLAG + "empty_flag_06.png",
						EMPTY_FLAG + "empty_flag_07.png",
						EMPTY_FLAG + "empty_flag_08.png",
						EMPTY_FLAG + "empty_flag_09.png",
						EMPTY_FLAG + "empty_flag_10.png",
						EMPTY_FLAG + "empty_flag_11.png",
						EMPTY_FLAG + "empty_flag_12.png",
						EMPTY_FLAG + "empty_flag_13.png",
						EMPTY_FLAG + "empty_flag_14.png",
						EMPTY_FLAG + "empty_flag_15.png",
						EMPTY_FLAG + "empty_flag_16.png",
						EMPTY_FLAG + "empty_flag_17.png",
						EMPTY_FLAG + "empty_flag_18.png",
						EMPTY_FLAG + "empty_flag_19.png",
						EMPTY_FLAG + "empty_flag_20.png",
						EMPTY_FLAG + "empty_flag_21.png",
						EMPTY_FLAG + "empty_flag_22.png",
						EMPTY_FLAG + "empty_flag_23.png",
						EMPTY_FLAG + "empty_flag_24.png",
						EMPTY_FLAG + "empty_flag_25.png",
						EMPTY_FLAG + "empty_flag_26.png",
						EMPTY_FLAG + "empty_flag_27.png",
						EMPTY_FLAG + "empty_flag_28.png",
						EMPTY_FLAG + "empty_flag_29.png",
						EMPTY_FLAG + "empty_flag_30.png",
						EMPTY_FLAG + "empty_flag_31.png",

					)
				},
				{
					"name" : "effect_4",
					"type" : "ani_image",

					"x" : 710+AJUST,
					"y" : 100,

					"delay" : 6,

					"images" :
					(
						EMPTY_FLAG + "empty_flag_00.png",
						EMPTY_FLAG + "empty_flag_01.png",
						EMPTY_FLAG + "empty_flag_02.png",
						EMPTY_FLAG + "empty_flag_03.png",
						EMPTY_FLAG + "empty_flag_04.png",
						EMPTY_FLAG + "empty_flag_05.png",
						EMPTY_FLAG + "empty_flag_06.png",
						EMPTY_FLAG + "empty_flag_07.png",
						EMPTY_FLAG + "empty_flag_08.png",
						EMPTY_FLAG + "empty_flag_09.png",
						EMPTY_FLAG + "empty_flag_10.png",
						EMPTY_FLAG + "empty_flag_11.png",
						EMPTY_FLAG + "empty_flag_12.png",
						EMPTY_FLAG + "empty_flag_13.png",
						EMPTY_FLAG + "empty_flag_14.png",
						EMPTY_FLAG + "empty_flag_15.png",
						EMPTY_FLAG + "empty_flag_16.png",
						EMPTY_FLAG + "empty_flag_17.png",
						EMPTY_FLAG + "empty_flag_18.png",
						EMPTY_FLAG + "empty_flag_19.png",
						EMPTY_FLAG + "empty_flag_20.png",
						EMPTY_FLAG + "empty_flag_21.png",
						EMPTY_FLAG + "empty_flag_22.png",
						EMPTY_FLAG + "empty_flag_23.png",
						EMPTY_FLAG + "empty_flag_24.png",
						EMPTY_FLAG + "empty_flag_25.png",
						EMPTY_FLAG + "empty_flag_26.png",
						EMPTY_FLAG + "empty_flag_27.png",
						EMPTY_FLAG + "empty_flag_28.png",
						EMPTY_FLAG + "empty_flag_29.png",
						EMPTY_FLAG + "empty_flag_30.png",
						EMPTY_FLAG + "empty_flag_31.png",

					)
				},
				{
					"name" : "Slot_0",
					"type" : "image",

					"x" : 359+AJUST,
					"y" : 100,

					"image": CHAR_SELECT + "big_slot_unknown.png",
					"children" :
					(

						{
							"name" : "face_small_0",
							"type" : "image",

							"x" : 55,
							"y" : -12,

							"image": BASE_PATH + "faces/select_faces/icon_mwarrior.png",
						},

						{
							"name" : "name_small_0",
							"type" : "text",

							"x" : 0,
							"y" : -50,

							"all_align" : "center",
							"fontname" : "Tahoma:18",
							"text" : "Apollo",
							"color" : 0xffCECECE,
						},

						{
							"name" : "guild_symbol_small_0",
							"type" : "image",

							"x" : 69,
							"y" : 180,

							"image": CHAR_SELECT + "guild_symbol.png",
							"children" :
							(
								{
									"name" : "guild_text_small_0",
									"type" : "text",

									"x" : 0,
									"y" : -20,

									"all_align" : "center",
									"fontname" : "Tahoma:16",
									"text" : "UltraS",
									"color" : 0xffCECECE,
								},
							),
						},

						{
							"name" : "Select_slot_0",
							"type" : "radio_button",

							"x" : -16,
							"y" : -30,

							"default_image": CHAR_SELECT + "on_hover.png",
							"over_image": CHAR_SELECT + "on_select_slot.png",
							"down_image":  CHAR_SELECT + "on_select_slot.png",

						},

						{
							"name" : "delete_slot_0",
							"type" : "button",

							"x" : 34,
							"y" : 240,

							"default_image": CHAR_SELECT + "delete_normal_button.png",
							"over_image": CHAR_SELECT + "delete_hover_button.png",
							"down_image":  CHAR_SELECT + "delete_active_button.png",
						},

						{
							"name" : "switch_main_0",
							"type" : "button",

							"x" : 124,
							"y" : 240,

							"default_image": CHAR_SELECT + "swith_slots_normal.png",
							"over_image": CHAR_SELECT + "swith_slots_hover.png",
							"down_image":  CHAR_SELECT + "swith_slots_active.png",
						},
						{
							"name" : "level_decoration_0",
							"type" : "image",

							"x" : 110,
							"y" : 68,

							"image": CHAR_SELECT + "level_decoration.png",
							"children" :
							(
								{
									"name" : "level_value_0",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",
									"fontname" : "Tahoma:12",
									"text" : "123",
									"color" : 0xffCECECE,
								},

							),
						},

					),
				},

				{
					"name" : "create_slot_0",
					"type" : "button",

					"x" : 359+AJUST+75,
					"y" : 100+280,

					"default_image": CHAR_SELECT + "create_btn_normal.png",
					"over_image": CHAR_SELECT + "create_btn_hover.png",
					"down_image":  CHAR_SELECT + "create_btn_active.png",

				},

				{
					"name" : "Slot_1",
					"type" : "image",

					"x" : 570+AJUST,
					"y" : 170,

					"image": CHAR_SELECT + "back_slot.png",
					"children" :
					(

						{
							"name" : "face_small_1",
							"type" : "image",

							"x" : 46,
							"y" : -2,

							"image": BASE_PATH + "faces/icon_mwarrior.png",
						},

						{
							"name" : "name_small_1",
							"type" : "text",

							"x" : 0,
							"y" : -50,

							"all_align" : "center",
							"fontname" : "Tahoma:18",
							"text" : "Apollo1",
							"color" : 0xffCECECE,
						},
						{
							"name" : "guild_symbol_small_1",
							"type" : "image",

							"x" : 48,
							"y" : 140,

							"image": CHAR_SELECT + "guild_symbol.png",
							"children" :
							(
								{
									"name" : "guild_text_small_1",
									"type" : "text",

									"x" : 0,
									"y" : -20,

									"all_align" : "center",
									"fontname" : "Tahoma:16",
									"text" : "UltraS",
									"color" : 0xffCECECE,
								},
							),
						},
						{
							"name" : "Select_slot_1",
							"type" : "radio_button",

							"x" : 0,
							"y" : -22,

							"default_image": CHAR_SELECT + "on_hover_2.png",
							"over_image": CHAR_SELECT + "on_select_slot_2.png",
							"down_image":  CHAR_SELECT + "on_select_slot_2.png",

						},

						{
							"name" : "switch_main_1",
							"type" : "button",

							"x" : 90,
							"y" : 165,

							"default_image": CHAR_SELECT + "swith_slots_normal.png",
							"over_image": CHAR_SELECT + "swith_slots_hover.png",
							"down_image":  CHAR_SELECT + "swith_slots_active.png",
						},
						
						{
							"name" : "delete_slot_1",
							"type" : "button",

							"x" : 30,
							"y" : 170,

							"default_image": CHAR_SELECT + "delete_normal_button_small.png",
							"over_image": CHAR_SELECT + "delete_hover_button_small.png",
							"down_image":  CHAR_SELECT + "delete_active_button_small.png",

						},
						{
							"name" : "level_decoration_1",
							"type" : "image",

							"x" : 80,
							"y" : 45,

							"image": CHAR_SELECT + "level_decoration.png",
							"children" :
							(
								{
									"name" : "level_value_1",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",
									"fontname" : "Tahoma:12",
									"text" : "120",
									"color" : 0xffCECECE,
								},
							),
						},

					),
				},
				{
					"name" : "create_slot_1",
					"type" : "button",

					"x" : 570+AJUST+60,
					"y" : 170+170,

					"default_image": CHAR_SELECT + "create_btn_normal_small.png",
					"over_image": CHAR_SELECT + "create_btn_hover_small.png",
					"down_image":  CHAR_SELECT + "create_btn_active_small.png",

				},
				{
					"name" : "Slot_2",
					"type" : "image",

					"x" : 170+AJUST,
					"y" : 170,

					"image": CHAR_SELECT + "back_slot.png",
					"children" :
					(
						{
							"name" : "face_small_2",
							"type" : "image",

							"x" : 46,
							"y" : -2,

							"image": BASE_PATH + "faces/icon_mwarrior.png",
						},

						{
							"name" : "name_small_2",
							"type" : "text",

							"x" : 0,
							"y" : -50,

							"all_align" : "center",
							"fontname" : "Tahoma:18",
							"text" : "Apollo2",
							"color" : 0xffCECECE,
						},
						{
							"name" : "guild_symbol_small_2",
							"type" : "image",

							"x" : 48,
							"y" : 140,

							"image": CHAR_SELECT + "guild_symbol.png",
							"children" :
							(
								{
									"name" : "guild_text_small_2",
									"type" : "text",

									"x" : 0,
									"y" : -20,

									"all_align" : "center",
									"fontname" : "Tahoma:16",
									"text" : "UltraS",
									"color" : 0xffCECECE,
								},
							),
						},
						{
							"name" : "Select_slot_2",
							"type" : "radio_button",

							"x" : 0,
							"y" : -22,

							"default_image": CHAR_SELECT + "on_hover_2.png",
							"over_image": CHAR_SELECT + "on_select_slot_2.png",
							"down_image":  CHAR_SELECT + "on_select_slot_2.png",

						},
						
						{
							"name" : "switch_main_2",
							"type" : "button",

							"x" : 90,
							"y" : 165,

							"default_image": CHAR_SELECT + "swith_slots_normal.png",
							"over_image": CHAR_SELECT + "swith_slots_hover.png",
							"down_image":  CHAR_SELECT + "swith_slots_active.png",
						},
						
						{
							"name" : "delete_slot_2",
							"type" : "button",

							"x" : 30,
							"y" : 170,

							"default_image": CHAR_SELECT + "delete_normal_button_small.png",
							"over_image": CHAR_SELECT + "delete_hover_button_small.png",
							"down_image":  CHAR_SELECT + "delete_active_button_small.png",

						},

						{
							"name" : "level_decoration_2",
							"type" : "image",

							"x" : 80,
							"y" : 45,

							"image": CHAR_SELECT + "level_decoration.png",
							"children" :
							(
								{
									"name" : "level_value_2",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",
									"fontname" : "Tahoma:12",
									"text" : "120",
									"color" : 0xffCECECE,
								},
							),
						},

					),
				},
				{
					"name" : "create_slot_2",
					"type" : "button",

					"x" : 170+AJUST+60,
					"y" : 170+170,

					"default_image": CHAR_SELECT + "create_btn_normal_small.png",
					"over_image": CHAR_SELECT + "create_btn_hover_small.png",
					"down_image":  CHAR_SELECT + "create_btn_active_small.png",

				},
				##
				{
					"name" : "Slot_3",
					"type" : "image",

					"x" : 0+AJUST,
					"y" : 170,

					"image": CHAR_SELECT + "back_slot.png",
					"children" :
					(
						{
							"name" : "face_small_3",
							"type" : "image",

							"x" : 46,
							"y" : -2,

							"image": BASE_PATH + "faces/icon_mwarrior.png",
						},

						{
							"name" : "name_small_3",
							"type" : "text",

							"x" : 0,
							"y" : -50,

							"all_align" : "center",
							"fontname" : "Tahoma:18",
							"text" : "Apollo3",
							"color" : 0xffCECECE,
						},
						{
							"name" : "guild_symbol_small_3",
							"type" : "image",

							"x" : 48,
							"y" : 140,

							"image": CHAR_SELECT + "guild_symbol.png",
							"children" :
							(
								{
									"name" : "guild_text_small_3",
									"type" : "text",

									"x" : 0,
									"y" : -20,

									"all_align" : "center",
									"fontname" : "Tahoma:16",
									"text" : "UltraS",
									"color" : 0xffCECECE,
								},
							),
						},
						{
							"name" : "Select_slot_3",
							"type" : "radio_button",

							"x" : 0,
							"y" : -22,

							"default_image": CHAR_SELECT + "on_hover_2.png",
							"over_image": CHAR_SELECT + "on_select_slot_2.png",
							"down_image":  CHAR_SELECT + "on_select_slot_2.png",

						},
						{
							"name" : "switch_main_3",
							"type" : "button",

							"x" : 90,
							"y" : 165,

							"default_image": CHAR_SELECT + "swith_slots_normal.png",
							"over_image": CHAR_SELECT + "swith_slots_hover.png",
							"down_image":  CHAR_SELECT + "swith_slots_active.png",
						},
						
						{
							"name" : "delete_slot_3",
							"type" : "button",

							"x" : 30,
							"y" : 170,

							"default_image": CHAR_SELECT + "delete_normal_button_small.png",
							"over_image": CHAR_SELECT + "delete_hover_button_small.png",
							"down_image":  CHAR_SELECT + "delete_active_button_small.png",

						},
						{
							"name" : "level_decoration_3",
							"type" : "image",

							"x" : 80,
							"y" : 45,

							"image": CHAR_SELECT + "level_decoration.png",
							"children" :
							(
								{
									"name" : "level_value_3",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",
									"fontname" : "Tahoma:12",
									"text" : "120",
									"color" : 0xffCECECE,
								},
							),
						},
					),
				},

				{
					"name" : "create_slot_3",
					"type" : "button",

					"x" : 0+AJUST+60,
					"y" : 170+170,

					"default_image": CHAR_SELECT + "create_btn_normal_small.png",
					"over_image": CHAR_SELECT + "create_btn_hover_small.png",
					"down_image":  CHAR_SELECT + "create_btn_active_small.png",

				},

				{
					"name" : "Slot_4",
					"type" : "image",

					"x" : 570+170+AJUST,
					"y" : 170,

					"image": CHAR_SELECT + "back_slot.png",
					"children" :
					(

						{
							"name" : "face_small_4",
							"type" : "image",

							"x" : 46,
							"y" : -2,

							"image": BASE_PATH + "faces/icon_mwarrior.png",
						},

						{
							"name" : "name_small_4",
							"type" : "text",

							"x" : 0,
							"y" : -50,

							"all_align" : "center",
							"fontname" : "Tahoma:18",
							"text" : "Apollo4",
							"color" : 0xffCECECE,
						},
						{
							"name" : "guild_symbol_small_4",
							"type" : "image",

							"x" : 48,
							"y" : 140,

							"image": CHAR_SELECT + "guild_symbol.png",
							"children" :
							(
								{
									"name" : "guild_text_small_4",
									"type" : "text",

									"x" : 0,
									"y" : -20,

									"all_align" : "center",
									"fontname" : "Tahoma:16",
									"text" : "UltraS",
									"color" : 0xffCECECE,
								},
							),
						},
						{
							"name" : "Select_slot_4",
							"type" : "radio_button",

							"x" : 0,
							"y" : -22,

							"default_image": CHAR_SELECT + "on_hover_2.png",
							"over_image": CHAR_SELECT + "on_select_slot_2.png",
							"down_image":  CHAR_SELECT + "on_select_slot_2.png",

						},
						{
							"name" : "switch_main_4",
							"type" : "button",

							"x" : 90,
							"y" : 165,

							"default_image": CHAR_SELECT + "swith_slots_normal.png",
							"over_image": CHAR_SELECT + "swith_slots_hover.png",
							"down_image":  CHAR_SELECT + "swith_slots_active.png",
						},
						
						{
							"name" : "delete_slot_4",
							"type" : "button",

							"x" : 30,
							"y" : 170,

							"default_image": CHAR_SELECT + "delete_normal_button_small.png",
							"over_image": CHAR_SELECT + "delete_hover_button_small.png",
							"down_image":  CHAR_SELECT + "delete_active_button_small.png",

						},
						{
							"name" : "level_decoration_4",
							"type" : "image",

							"x" : 80,
							"y" : 45,

							"image": CHAR_SELECT + "level_decoration.png",
							"children" :
							(
								{
									"name" : "level_value_4",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",
									"fontname" : "Tahoma:12",
									"text" : "0",
									"color" : 0xffCECECE,
								},
							),
						},
					),
				},

				{
					"name" : "create_slot_4",
					"type" : "button",

					"x" : 570+170+AJUST+60,
					"y" : 170+170,

					"default_image": CHAR_SELECT + "create_btn_normal_small.png",
					"over_image": CHAR_SELECT + "create_btn_hover_small.png",
					"down_image":  CHAR_SELECT + "create_btn_active_small.png",

				},
			),
		},
		## Main_Actor
		{
			"name" : "Shad_BackGround",
			"type" : "image",
			"x" : 0,
			"y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image": BASE_PATH + "background_shd.png",
		},
		{
			"name" : "Main_Actor",
			"type" : "window",

			"x" : (SCREEN_WIDTH/2) - 400,
			"y" : (SCREEN_HEIGHT/2) - 200,

			"width" : 205,
			"height" : 370,
			"children" :
			(
				{
					"name" : "flag_main_actor",
					"type" : "image",

					"x" : 0,
					"y" : 0,

					"image": CHAR_SELECT + "blue_slot.png",
					"children" :
					(

						{
							"name" : "face_race_mainActor",
							"type" : "image",

							"x" : 55,
							"y" : -10,

							"image": BASE_PATH + "faces/select_faces/icon_mwarrior.png",
						},

						{
							"name" : "name_mainActor",
							"type" : "text",

							"x" : 0,
							"y" : -50,

							"all_align" : "center",
							"fontname" : "Tahoma:18",
							"text" : "Apollo",
							"color" : 0xffCECECE,
						},

						{
							"name" : "guild_symbol_mainActor",
							"type" : "image",

							"x" : 69,
							"y" : 180,

							"image": CHAR_SELECT + "guild_symbol.png",
							"children" :
							(
								{
									"name" : "guild_name_mainActor",
									"type" : "text",

									"x" : 0,
									"y" : -20,

									"all_align" : "center",
									"fontname" : "Tahoma:16",
									"text" : "UltraS",
									"color" : 0xffCECECE,
								},
							),
						},

						{
							"name" : "deleteSlot_fromMainActor",
							"type" : "button",

							"x" : 34,
							"y" : 240,

							"default_image": CHAR_SELECT + "delete_normal_button.png",
							"over_image": CHAR_SELECT + "delete_hover_button.png",
							"down_image":  CHAR_SELECT + "delete_active_button.png",
						},

						{
							"name" : "switch_MainSlots",
							"type" : "button",

							"x" : 124,
							"y" : 240,

							"default_image": CHAR_SELECT + "switch_btn_normal.png",
							"over_image": CHAR_SELECT + "switch_btn_hover.png",
							"down_image":  CHAR_SELECT + "switch_btn_active.png",
						},
						{
							"name" : "level_symbol_fromMainActor",
							"type" : "image",

							"x" : 110,
							"y" : 68,

							"image": CHAR_SELECT + "level_decoration.png",
							"children" :
							(
								{
									"name" : "level_name_fromMainActor",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",
									"fontname" : "Tahoma:12",
									"text" : "Level",
									"color" : 0xffCECECE,
								},
							),
						},
						{
							"name" : "createSlot_fromMainActor",
							"type" : "button",

							"x" : 34,
							"y" : 240,

							"default_image": CHAR_SELECT + "create_btn_normal.png",
							"over_image": CHAR_SELECT + "create_btn_hover.png",
							"down_image":  CHAR_SELECT + "create_btn_active.png",

						},

						## Stats
						{
							"name" : "Status_parent",
							"type" : "window",

							"x" : 580,
							"y" : 80,

							"width" : 200,
							"height" : 200,

							"children" :
							(
								{
									"name" : "aspect",
									"type" : "image",

									"x" : -30,
									"y" : 0,

									"image" : CHAR_SELECT + "decoration.png",
									"children" :
									(
										{
											"name" : "text",
											"type" : "text",

											"x" : 93,
											"y" : -25,

											"fontname" : "Tahoma:18",
											"text" : localeInfo.STATUS,
											"color" : 0xffCECECE,
										},
									),
								},
								{
									"name" : "character_hth",
									"type" : "text",

									"x" : 30,
									"y" : 35,

									"fontname" : "Tahoma:12",
									# "text" : apollo_interface.VIT,
									"color" : 0xffCECECE,

									"text_horizontal_align" : "right",

									"children" :
									(
										{
											"name" : "gauge_back1",
											"type" : "expanded_image",

											"x" : 0,
											"y" : 2,

											"image" : CHAR_SELECT + "vertmeter-container.png",
										},
										{
											"name" : "icon",
											"type" : "expanded_image",

											"x" : -5,
											"y" : 100,

											"image" : CHAR_SELECT + "roleicon-support.png",
										},
										{
											"name" : "gauge_hth",
											"type" : "nano_expanded_image",

											"x" : 2,
											"y" : 4,

											"image" : CHAR_SELECT + "vertmeter-fill.png",
										},
									),
								},
								{
									"name" : "character_int",
									"type" : "text",
									"x" : 70,
									"y" : 35,

									"fontname" : "Tahoma:12",
									# "text" : apollo_interface.INT,
									"color" : 0xffCECECE,

									"text_horizontal_align" : "right",

									"children" :
									(
										{
											"name" : "gauge_back1",
											"type" : "expanded_image",

											"x" : 0,
											"y" : 2,

											"image" : CHAR_SELECT + "vertmeter-container.png",
										},
										{
											"name" : "icon",
											"type" : "expanded_image",

											"x" : -5,
											"y" : 100,

											"image" : CHAR_SELECT + "roleicon-mage.png",
										},
										{
											"name" : "gauge_int",
											"type" : "nano_expanded_image",

											"x" : 2,
											"y" : 4,

											"image" : CHAR_SELECT + "vertmeter-fill.png",
										},
									),
								},
								{
									"name" : "character_str",
									"type" : "text",
									"x" : 110,
									"y" : 35,

									"fontname" : "Tahoma:12",
									# "text" : apollo_interface.STR,
									"color" : 0xffCECECE,

									"text_horizontal_align" : "right",

									"children" :
									(
										{
											"name" : "gauge_back1",
											"type" : "expanded_image",

											"x" : 0,
											"y" : 2,

											"image" : CHAR_SELECT + "vertmeter-container.png",
										},
										{
											"name" : "icon",
											"type" : "expanded_image",

											"x" : -5,
											"y" : 100,

											"image" : CHAR_SELECT + "roleicon-marksman.png",
										},
										{
											"name" : "gauge_str",
											"type" : "nano_expanded_image",

											"x" : 2,
											"y" : 4,

											"image" : CHAR_SELECT + "vertmeter-fill.png",
										},
									),
								},
								{
									"name" : "character_dex",
									"type" : "text",
									"x" : 150,
									"y" : 35,

									"fontname" : "Tahoma:12",
									# "text" : apollo_interface.DEX,
									"color" : 0xffCECECE,

									"text_horizontal_align" : "right",

									"children" :
									(
										{
											"name" : "icon",
											"type" : "expanded_image",

											"x" : -5,
											"y" : 100,

											"image" : CHAR_SELECT + "roleicon-tank.png",
										},
										{
											"name" : "gauge_back1",
											"type" : "expanded_image",

											"x" : 0,
											"y" : 2,

											"image" : CHAR_SELECT + "vertmeter-container.png",
										},
										{
											"name" : "gauge_dex",
											"type" : "nano_expanded_image",

											"x" : 2,
											"y" : 4,

											"image" : CHAR_SELECT + "vertmeter-fill.png",
										},
									),
								},
							),
						},
					),
				},
			),
		},
		{
			"name" : "Exit_MainActor_Board",
			"type" : "window",

			"x" : (SCREEN_WIDTH-250)/2,
			"y" : SCREEN_HEIGHT - 55,

			"width" : 230,
			"height" : 80,
			"children" :
			(
				{
					"name" : "decoration_1",
					"type" : "image",

					"x" : 180,
					"y" : 0,

					"image": CHAR_SELECT + "decoration_1.png",
				},
				{
					"name" : "decoration_2",
					"type" : "image",

					"x" : -35,
					"y" : 0,

					"image": CHAR_SELECT + "decoration_2.png",
				},
				{
					"name" : "button_backgr",
					"type" : "image",

					"x" : 40,
					"y" : 15,

					"image": CHAR_SELECT + "backgr_buttons.png",
					"children" :
					(
						{
							"name" : "confirm_button_mainActor",
							"type" : "button",

							"x" : 30,
							"y" : -1,

							"default_image": CHAR_SELECT + "button_create_normal.png",
							"over_image": CHAR_SELECT + "button_create_hover.png",
							"down_image":  CHAR_SELECT + "button_create_active.png",
							"disable_image":  CHAR_SELECT + "button_create_disable.png",
							"children" :
							(
								{
									"name" : "confirm",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"all_align" : "center",
									"fontname" : "Tahoma:15",
									"text" : localeInfo.CONFIRM,
									"color" : 0xffCECECE,
								},
								{
									"name" : "Seconds",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"all_align" : "center",
									"fontname" : "Tahoma:15",
									"text" : localeInfo.CONFIRM,
									"color" : 0xffCECECE,
								},
							),
						},
						{
							"name" : "exit_button_mainActor",
							"type" : "button",

							"x" : 3,
							"y" : 3,

							"default_image": CHAR_SELECT + "exit_button_normal.png",
							"over_image": CHAR_SELECT + "exit_button_hover.png",
							"down_image":  CHAR_SELECT + "exit_button_active.png",
						},

					),
				},
			),
		},

		{
			"name" : "Exit_Board",
			"type" : "window",

			"x" : (SCREEN_WIDTH-250)/2,
			"y" : SCREEN_HEIGHT - 55,

			"width" : 230,
			"height" : 80,
			"children" :
			(
				{
					"name" : "decoration_1",
					"type" : "image",

					"x" : 180,
					"y" : 0,

					"image": CHAR_SELECT + "decoration_1.png",
				},
				{
					"name" : "decoration_2",
					"type" : "image",

					"x" : -35,
					"y" : 0,

					"image": CHAR_SELECT + "decoration_2.png",
				},
				{
					"name" : "button_backgr",
					"type" : "image",

					"x" : 40,
					"y" : 15,

					"image": CHAR_SELECT + "backgr_buttons.png",
					"children" :
					(
						{
							"name" : "confirm_button",
							"type" : "button",

							"x" : 30,
							"y" : -1,

							"default_image": CHAR_SELECT + "button_create_normal.png",
							"over_image": CHAR_SELECT + "button_create_hover.png",
							"down_image":  CHAR_SELECT + "button_create_active.png",
							"disable_image":  CHAR_SELECT + "button_create_disable.png",
							"children" :
							(
								{
									"name" : "confirm",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"all_align" : "center",
									"fontname" : "Tahoma:15",
									"text" : localeInfo.CONFIRM,
									"color" : 0xffCECECE,
								},
								{
									"name" : "Seconds",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"all_align" : "center",
									"fontname" : "Tahoma:15",
									"text" : localeInfo.CONFIRM,
									"color" : 0xffCECECE,
								},
							),
						},
						{
							"name" : "exit_button",
							"type" : "button",

							"x" : 3,
							"y" : 3,

							"default_image": CHAR_SELECT + "exit_button_normal.png",
							"over_image": CHAR_SELECT + "exit_button_hover.png",
							"down_image":  CHAR_SELECT + "exit_button_active.png",
						},
					),
				},
			),
		},
	),
}
