import uiScriptLocale
import nano_interface
import localeInfo

ROOT_PATH = "d:/ymir work/ui/public/"
LOCALE_PATH = uiScriptLocale.EMPIRE_PATH
BLUE_FLAG = "nano_interface/animations/flag_blue/"
GREEN_FLAG = "nano_interface/animations/flag_green/"
MOUVE_FLAG = "nano_interface/animations/flag_mouve/"
BASE_PATH = "nano_interface/"
CHAR_SELECT = "nano_interface/select_character/"

ATALS_X = SCREEN_WIDTH * (282) / 800
ATALS_Y = SCREEN_HEIGHT * (170) / 600
AJUST = 50
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
			"name" : "bg",
			"type" : "expanded_image",
			"x" : 0,
			"y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image": BASE_PATH + "background_select.png",
		},
		
		
		{
			"name" : "Center",
			"type" : "window",

			"x" : (SCREEN_WIDTH/2) - 500,
			"y" : (SCREEN_HEIGHT/2) - 300,

			"width" : 1000,
			"height" : 600,
			"children" :
			(
				# Main Slot
				{
					"name" : "back_flags_0", # 1. sarı bayrak
					"type" : "image",

					"x" : 120-AJUST+12,
					"y" : 25,

					"image": BLUE_FLAG + "flag_blue.png",
					"children" :
					(	
						{
							"name" : "effect_0",
							"type" : "ani_image",

							"x" : 0,
							"y" : 0,

							"delay" : 6,

							"images" :
							(
								BLUE_FLAG + "flag_blue_00.png",
								BLUE_FLAG + "flag_blue_01.png",
								BLUE_FLAG + "flag_blue_02.png",
								BLUE_FLAG + "flag_blue_03.png",
								BLUE_FLAG + "flag_blue_04.png",
								BLUE_FLAG + "flag_blue_05.png",
								BLUE_FLAG + "flag_blue_06.png",
								BLUE_FLAG + "flag_blue_07.png",
								BLUE_FLAG + "flag_blue_08.png",
								BLUE_FLAG + "flag_blue_09.png",
								BLUE_FLAG + "flag_blue_10.png",
								BLUE_FLAG + "flag_blue_11.png",
								BLUE_FLAG + "flag_blue_12.png",
								BLUE_FLAG + "flag_blue_13.png",
								BLUE_FLAG + "flag_blue_14.png",
								BLUE_FLAG + "flag_blue_15.png",
								BLUE_FLAG + "flag_blue_16.png",
								BLUE_FLAG + "flag_blue_17.png",
								BLUE_FLAG + "flag_blue_18.png",
								BLUE_FLAG + "flag_blue_19.png",
								BLUE_FLAG + "flag_blue_20.png",
								BLUE_FLAG + "flag_blue_21.png",
								BLUE_FLAG + "flag_blue_22.png",
								BLUE_FLAG + "flag_blue_23.png",
								BLUE_FLAG + "flag_blue_24.png",
								BLUE_FLAG + "flag_blue_25.png",
								BLUE_FLAG + "flag_blue_26.png",
								BLUE_FLAG + "flag_blue_27.png",
								BLUE_FLAG + "flag_blue_28.png",
								# BLUE_FLAG + "flag_blue_29.png",
								
							)
						},
						{
							"name" : "rubin",
							"type" : "image",

							"x" : 38,
							"y" : 0,

							"image": BASE_PATH + "select_empire/karmizibayrak.png",
						},
						{
							"name" : "start_slot_0",
							"type" : "radio_button",

							"x" : 50,
							"y" : 25,

							"default_image": BASE_PATH + "select_empire/on_hover.png",
							"over_image": BASE_PATH + "select_empire/on_select_slot.png",
							"down_image":  BASE_PATH + "select_empire/on_select_slot.png",

						},
					),
				},
				{
					"name" : "back_flags_1", # Mor bayrak
					"type" : "image",

					"x" : 510+AJUST-5,
					"y" : 25,

					"image": BLUE_FLAG + "flag_blue.png",
					"children" :
					(	
						{
							"name" : "effect_1",
							"type" : "ani_image",

							"x" : 0,
							"y" : 0,

							"delay" : 6,

							"images" :
							(
								BLUE_FLAG + "flag_blue_00.png",
								BLUE_FLAG + "flag_blue_01.png",
								BLUE_FLAG + "flag_blue_02.png",
								BLUE_FLAG + "flag_blue_03.png",
								BLUE_FLAG + "flag_blue_04.png",
								BLUE_FLAG + "flag_blue_05.png",
								BLUE_FLAG + "flag_blue_06.png",
								BLUE_FLAG + "flag_blue_07.png",
								BLUE_FLAG + "flag_blue_08.png",
								BLUE_FLAG + "flag_blue_09.png",
								BLUE_FLAG + "flag_blue_10.png",
								BLUE_FLAG + "flag_blue_11.png",
								BLUE_FLAG + "flag_blue_12.png",
								BLUE_FLAG + "flag_blue_13.png",
								BLUE_FLAG + "flag_blue_14.png",
								BLUE_FLAG + "flag_blue_15.png",
								BLUE_FLAG + "flag_blue_16.png",
								BLUE_FLAG + "flag_blue_17.png",
								BLUE_FLAG + "flag_blue_18.png",
								BLUE_FLAG + "flag_blue_19.png",
								BLUE_FLAG + "flag_blue_20.png",
								BLUE_FLAG + "flag_blue_21.png",
								BLUE_FLAG + "flag_blue_22.png",
								BLUE_FLAG + "flag_blue_23.png",
								BLUE_FLAG + "flag_blue_24.png",
								BLUE_FLAG + "flag_blue_25.png",
								BLUE_FLAG + "flag_blue_26.png",
								BLUE_FLAG + "flag_blue_27.png",
								BLUE_FLAG + "flag_blue_28.png",
								# BLUE_FLAG + "flag_blue_29.png",
								
							)
						},
						{
							"name" : "rubin",
							"type" : "image",

							"x" : 38,
							"y" : 0,

							"image": BASE_PATH + "select_empire/celeste_rubin.png",
						},
						{
							"name" : "start_slot_1",
							"type" : "radio_button",

							"x" : 50,
							"y" : 25,

							"default_image": BASE_PATH + "select_empire/on_hover.png",
							"over_image": BASE_PATH + "select_empire/on_select_slot.png",
							"down_image":  BASE_PATH + "select_empire/on_select_slot.png",

						},
					),
				},
				{
					"name" : "back_flags_2", # 2. sarı bayrak
					"type" : "image",

					"x" : 220-AJUST+148,
					"y" : 25,

					"image": BLUE_FLAG + "flag_blue.png",
					"children" :
					(	
						{
							"name" : "effect_2",
							"type" : "ani_image",

							"x" : 0,
							"y" : 0,

							"delay" : 6,

							"images" :
							(
								BLUE_FLAG + "flag_blue_00.png",
								BLUE_FLAG + "flag_blue_01.png",
								BLUE_FLAG + "flag_blue_02.png",
								BLUE_FLAG + "flag_blue_03.png",
								BLUE_FLAG + "flag_blue_04.png",
								BLUE_FLAG + "flag_blue_05.png",
								BLUE_FLAG + "flag_blue_06.png",
								BLUE_FLAG + "flag_blue_07.png",
								BLUE_FLAG + "flag_blue_08.png",
								BLUE_FLAG + "flag_blue_09.png",
								BLUE_FLAG + "flag_blue_10.png",
								BLUE_FLAG + "flag_blue_11.png",
								BLUE_FLAG + "flag_blue_12.png",
								BLUE_FLAG + "flag_blue_13.png",
								BLUE_FLAG + "flag_blue_14.png",
								BLUE_FLAG + "flag_blue_15.png",
								BLUE_FLAG + "flag_blue_16.png",
								BLUE_FLAG + "flag_blue_17.png",
								BLUE_FLAG + "flag_blue_18.png",
								BLUE_FLAG + "flag_blue_19.png",
								BLUE_FLAG + "flag_blue_20.png",
								BLUE_FLAG + "flag_blue_21.png",
								BLUE_FLAG + "flag_blue_22.png",
								BLUE_FLAG + "flag_blue_23.png",
								BLUE_FLAG + "flag_blue_24.png",
								BLUE_FLAG + "flag_blue_25.png",
								BLUE_FLAG + "flag_blue_26.png",
								BLUE_FLAG + "flag_blue_27.png",
								BLUE_FLAG + "flag_blue_28.png",
								# BLUE_FLAG + "flag_blue_29.png",
								
							)
						},
						{
							"name" : "rubin",
							"type" : "image",

							"x" : 38,
							"y" : 0,

							"image": BASE_PATH + "select_empire/mavibayrak.png",
						},
						{
							"name" : "start_slot_2",
							"type" : "radio_button",

							"x" : 50,
							"y" : 25,

							"default_image": BASE_PATH + "select_empire/on_hover.png",
							"over_image": BASE_PATH + "select_empire/on_select_slot.png",
							"down_image":  BASE_PATH + "select_empire/on_select_slot.png",

						},
					),
				},
			),
		},
		
		{
			"name" : "Center_bttom_window",
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
								# {
									# "name" : "Seconds",
									# "type" : "text",

									# "x" : 0,
									# "y" : -1,
									
									# "all_align" : "center",
									# "fontname" : "Tahoma:15",
									# "text" : localeInfo.CONFIRM,
									# "color" : 0xffCECECE,
								# },
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
		{
			"name" : "aspect",
			"type" : "image",

			"x" : (SCREEN_WIDTH/2) - 210,
			"y" : (SCREEN_HEIGHT/2) + 165,

			"image" : BASE_PATH + "select_empire/decoration.png",
			"children":
			(
				{
					"name" : "description_text",
					"type" : "text",
				
					"x" : -20, 
					"y" : 0,

					"fontname" : "Tahoma Bold:18",
					
					"r" : 1,
					"g" : 1,
					"b" : 1,
					
					"all_align" : "center",
					"text" : localeInfo.SELECT_EMPIRE,
				},			
			),
		},
	),
}
