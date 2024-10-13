import uiScriptLocale
import localeInfo
import nano_interface


## PATCHS
ROOT = "nano_interface/animations/ring/"
MALE_EFFECT = "nano_interface/faces/effect_male/"
FIMALE_EFFECT = "nano_interface/faces/effect_fimale/"
BASE_PATH = "nano_interface/"
CHAR_CREATE = "nano_interface/character_create/"

window = {
	"name" : "CreateCharacterWindow",

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
			"name" : "slot_indicator",
			"type" : "window",

			"x" : (SCREEN_WIDTH/2)-300,
			"y" : (SCREEN_HEIGHT/2)- 320,
			
			"width" : 30,
			"height" : 30,
			
			"children" :
			(	
				{
					"name" : "sep_btn_right",
					"type" : "expanded_image",
					
					"x" : -175,
					"y" : 106,
					
					"image": CHAR_CREATE + "button_separators_right.png",
				},
				{
					"name" : "sep_btn_left",
					"type" : "expanded_image",
					
					"x" : 520,
					"y" : 106,
					
					"image": CHAR_CREATE + "button_separators_left.png",
				},
				{
					"name" : "ani_cicle",
					"type" : "ani_image",

					"x" : 35,
					"y" : 15,

					"delay" : 6,

					"images" :
					(
						ROOT + "ring-splash-dashed1_01.png",
						ROOT + "ring-splash-dashed1_02.png",
						ROOT + "ring-splash-dashed1_03.png",
						ROOT + "ring-splash-dashed1_04.png",
						ROOT + "ring-splash-dashed1_05.png",
						ROOT + "ring-splash-dashed1_06.png",
						ROOT + "ring-splash-dashed1_07.png",
						ROOT + "ring-splash-dashed1_08.png",
						ROOT + "ring-splash-dashed1_09.png",
						ROOT + "ring-splash-dashed1_10.png",
					)
				},
				{
					"name" : "mid_cicle",
					"type" : "expanded_image",
					
					"x" : 50,
					"y" : 30,
					
					"image": CHAR_CREATE + "mid_cicle.png",
				},
			),
		},
		
		## Left Side
		{
			"name" : "left_side",
			"type" : "window",

			"x" : (SCREEN_WIDTH/2)-480,
			"y" : (SCREEN_HEIGHT/2)- 220,
			
			"width" : 275,
			"height" : 395,
			
			"children" :
			(
				{
					"name" : "male_1_btn",
					"type" : "radio_button",

					"x" : 35,
					"y" : 8,

					"default_image" : CHAR_CREATE + "select_male_btn/slot_normal.png", 
					"over_image" : CHAR_CREATE + "select_male_btn/slot_1.png", 
					"down_image" : CHAR_CREATE + "select_male_btn/slot_1.png", 
					"disable_image" : CHAR_CREATE + "select_male_btn/slot_1_disable.png", 
					
					"children" :
					(
						{
							"name" : "male_1_txt",
							"type" : "text",

							"x" : 77,
							"y" : 18,


							"fontname" : "Tahoma Bold:16",
							"color" : 0xffCECECE,
							"text" : localeInfo.WARRIOR_M,
						},
					
						{
							"name" : "ico",
							"type" : "image",

							"x" : -13,
							"y" : 5,

							"image" : BASE_PATH + "faces/shape_icon.png",
							"children" :
							(
								{
									"name" : "icon_0",
									"type" : "image",

									"x" : -2,
									"y" : -10,

									"image" : BASE_PATH + "faces/icon_mwarrior.png",
								},
							),
						},	
					),
				},
				
				{
					"name" : "male_2_btn",
					"type" : "radio_button",

					"x" : 35,
					"y" : 85,

					"default_image" : CHAR_CREATE + "select_male_btn/slot_normal.png", 
					"over_image" : CHAR_CREATE + "select_male_btn/slot_2.png", 
					"down_image" : CHAR_CREATE + "select_male_btn/slot_2.png", 
					"disable_image" : CHAR_CREATE + "select_male_btn/slot_2_disable.png", 
					
					"children" :
					(
						{
							"name" : "male_2_txt",
							"type" : "text",

							"x" : 80,
							"y" : 24,


							"fontname" : "Tahoma Bold:16",
							"color" : 0xffCECECE,
							"text" : localeInfo.NINJA_M,
						},
						
						{
							"name" : "ico",
							"type" : "image",

							"x" : -13,
							"y" : 5,

							"image" : BASE_PATH + "faces/shape_icon.png",
							"children" :
							(
								{
									"name" : "icon_1",
									"type" : "image",

									"x" : -2,
									"y" : -10,

									"image" : BASE_PATH + "faces/icon_mninja.png",
								},
							),
						},	
					),
				},
				
				{
					"name" : "male_3_btn",
					"type" : "radio_button",

					"x" : 35,
					"y" : 85+85-8,

					"default_image" : CHAR_CREATE + "select_male_btn/slot_normal.png", 
					"over_image" : CHAR_CREATE + "select_male_btn/slot_3.png", 
					"down_image" : CHAR_CREATE + "select_male_btn/slot_3.png", 
					"disable_image" : CHAR_CREATE + "select_male_btn/slot_3_disable.png", 
					
					"children" :
					(
						{
							"name" : "male_3_txt",
							"type" : "text",

							"x" : 80,
							"y" : 24,


							"fontname" : "Tahoma Bold:16",
							"color" : 0xffCECECE,
							"text" : localeInfo.SURA_M,
						},
					
						{
							"name" : "ico",
							"type" : "image",

							"x" : -13,
							"y" : 5,

							"image" : BASE_PATH + "faces/shape_icon.png",
							"children" :
							(
								{
									"name" : "icon_2",
									"type" : "image",

									"x" : -2,
									"y" : -5,

									"image" : BASE_PATH + "faces/icon_msura.png",
								},
							),
						},	
					),
				},
				
				{
					"name" : "male_4_btn",
					"type" : "radio_button",

					"x" : 35,
					"y" : 85+85*2-16,

					"default_image" : CHAR_CREATE + "select_male_btn/slot_normal.png", 
					"over_image" : CHAR_CREATE + "select_male_btn/slot_4.png", 
					"down_image" : CHAR_CREATE + "select_male_btn/slot_4.png", 
					"disable_image" : CHAR_CREATE + "select_male_btn/slot_4_disable.png", 
					
					"children" :
					(
						{
							"name" : "male_4_txt",
							"type" : "text",

							"x" : 70,
							"y" : 24,


							"fontname" : "Tahoma Bold:16",
							"color" : 0xffCECECE,
							"text" : localeInfo.SHAMAN_M,
						},
						{
							"name" : "ico",
							"type" : "image",

							"x" : -13,
							"y" : 5,

							"image" : BASE_PATH + "faces/shape_icon.png",
							"children" :
							(
								{
									"name" : "icon_3",
									"type" : "image",

									"x" : -2,
									"y" : 0,

									"image" : BASE_PATH + "faces/icon_mshaman.png",
								},
							),
						},	
					),
				},
				# Male Effect
				{
					"name" : "on_effect_male",
					"type" : "ani_image",

					"x" : 18,
					"y" : 13,

					"delay" : 6,

					"images" :
					(
						MALE_EFFECT + "effect_male_01.png",
						MALE_EFFECT + "effect_male_02.png",
						MALE_EFFECT + "effect_male_03.png",
						MALE_EFFECT + "effect_male_04.png",
						MALE_EFFECT + "effect_male_05.png",
						MALE_EFFECT + "effect_male_06.png",
						MALE_EFFECT + "effect_male_07.png",
						MALE_EFFECT + "effect_male_08.png",
						MALE_EFFECT + "effect_male_09.png",
						MALE_EFFECT + "effect_male_10.png",
					)
				},
			),
		},
		
		## Right Side
		{
			"name" : "left_side",
			"type" : "window",

			"x" : (SCREEN_WIDTH/2)+230,
			"y" : (SCREEN_HEIGHT/2)- 220,
			
			"width" : 275,
			"height" : 395,
			
			"children" :
			(
				{
					"name" : "female_1_btn",
					"type" : "radio_button",

					"x" : 5,
					"y" : 8,

					"default_image" : CHAR_CREATE + "select_fimale_btn/slot_normal.png", 
					"over_image" : CHAR_CREATE + "select_fimale_btn/slot_1.png", 
					"down_image" : CHAR_CREATE + "select_fimale_btn/slot_1.png", 
					"disable_image" : CHAR_CREATE + "select_fimale_btn/slot_1_disable.png",
					"children" :
					(
						{
							"name" : "female_1_txt",
							"type" : "text",

							"x" : 100,
							"y" : 24,


							"fontname" : "Tahoma Bold:16",
							"color" : 0xffCECECE,
							"text" : localeInfo.WARRIOR_W,
						},
						{
							"name" : "ico",
							"type" : "image",

							"x" : 190,
							"y" : 5,

							"image" : BASE_PATH + "faces/shape_icon.png",
							"children" :
							(
								{
									"name" : "icon_4",
									"type" : "image",

									"x" : -2,
									"y" : -10,

									"image" : BASE_PATH + "faces/icon_wwarrior.png",
								},
							),
						},	
					),
				},
				{
					"name" : "female_2_btn",
					"type" : "radio_button",

					"x" : 51,
					"y" : 85,

					"default_image" : CHAR_CREATE + "select_fimale_btn/slot_normal.png", 
					"over_image" : CHAR_CREATE + "select_fimale_btn/slot_2.png", 
					"down_image" : CHAR_CREATE + "select_fimale_btn/slot_2.png", 
					"disable_image" : CHAR_CREATE + "select_fimale_btn/slot_2_disable.png",
					"children" :
					(
						{
							"name" : "female_2_txt",
							"type" : "text",

							"x" : 65,
							"y" : 24,


							"fontname" : "Tahoma Bold:16",
							"color" : 0xffCECECE,
							"text" : localeInfo.NINJA_W,
						},
						{
							"name" : "ico",
							"type" : "image",

							"x" : 145,
							"y" : 5,

							"image" : BASE_PATH + "faces/shape_icon.png",
							"children" :
							(
								{
									"name" : "icon_5",
									"type" : "image",

									"x" : -2,
									"y" : -10,

									"image" : BASE_PATH + "faces/icon_wninja.png",
								},
							),
						},	
					),
				},
				{
					"name" : "female_3_btn",
					"type" : "radio_button",

					"x" : 71,
					"y" : 85*2-8,

					"default_image" : CHAR_CREATE + "select_fimale_btn/slot_normal.png", 
					"over_image" : CHAR_CREATE + "select_fimale_btn/slot_3.png", 
					"down_image" : CHAR_CREATE + "select_fimale_btn/slot_3.png", 
					"disable_image" : CHAR_CREATE + "select_fimale_btn/slot_3_disable.png",
					"children" :
					(
						{
							"name" : "female_3_txt",
							"type" : "text",

							"x" : 45,
							"y" : 24,


							"fontname" : "Tahoma Bold:16",
							"color" : 0xffCECECE,
							"text" : localeInfo.SURA_W,
						},
						{
							"name" : "ico",
							"type" : "image",

							"x" : 125,
							"y" : 5,

							"image" : BASE_PATH + "faces/shape_icon.png",
							"children" :
							(
								{
									"name" : "icon_6",
									"type" : "image",

									"x" : -2,
									"y" : -10,

									"image" : BASE_PATH + "faces/icon_wsura.png",
								},
							),
						},	
					),
				},
				{
					"name" : "female_4_btn",
					"type" : "radio_button",

					"x" : 49,
					"y" : 85*3-16,

					"default_image" : CHAR_CREATE + "select_fimale_btn/slot_normal.png", 
					"over_image" : CHAR_CREATE + "select_fimale_btn/slot_4.png", 
					"down_image" : CHAR_CREATE + "select_fimale_btn/slot_4.png", 
					"disable_image" : CHAR_CREATE + "select_fimale_btn/slot_4_disable.png",
					"children" :
					(
						{
							"name" : "female_4_txt",
							"type" : "text",

							"x" : 60,
							"y" : 24,


							"fontname" : "Tahoma Bold:16",
							"color" : 0xffCECECE,
							"text" : localeInfo.SHAMAN_W,
						},
						{
							"name" : "ico",
							"type" : "image",

							"x" : 147,
							"y" : 5,

							"image" : BASE_PATH + "faces/shape_icon.png",
							"children" :
							(
								{
									"name" : "icon_7",
									"type" : "image",

									"x" : -2,
									"y" : -10,

									"image" : BASE_PATH + "faces/icon_wshaman.png",
								},
							),
						},	
					),
				},
				# SOLARI
				#{
				#	"name" : "female_5_btn",
				#	"type" : "radio_button",

				#	"x" : 5,
				#	"y" : 85+85*3-24,

				#	"default_image" : CHAR_CREATE + "select_fimale_btn/slot_normal.png",
				#	"over_image" : CHAR_CREATE + "select_fimale_btn/slot_5.png",
				#	"down_image" : CHAR_CREATE + "select_fimale_btn/slot_5.png",

				#	"children" :
				#	(

				#		{
				#			"name" : "female_5_txt",
				#			"type" : "text",

				#			"x" : 100,
				#			"y" : 24,


				#			"fontname" : "Tahoma Bold:16",
				#			"color" : 0xffCECECE,
				#			"text" : "Solari",
				#		},

				#		{
				#			"name" : "ico",
				#			"type" : "image",

				#			"x" : 190,
				#			"y" : 5,

				#			"image" : BASE_PATH + "faces/shape_icon.png",
				#			"children" :
				#			(
				#				{
				#					"name" : "icon",
				#					"type" : "image",

				#					"x" : -2,
				#					"y" : -10,

				#					"image" : BASE_PATH + "faces/icon_mlykaner.png",
				#				},
				#			),
				#		},
				#	),
				#},
				## Fmale Effect
				{
					"name" : "on_effect_female",
					"type" : "ani_image",

					"x" : 193,
					"y" : 13,

					"delay" : 6,

					"images" :
					(
						FIMALE_EFFECT + "effect_fimale_01.png",
						FIMALE_EFFECT + "effect_fimale_02.png",
						FIMALE_EFFECT + "effect_fimale_03.png",
						FIMALE_EFFECT + "effect_fimale_04.png",
						FIMALE_EFFECT + "effect_fimale_05.png",
						FIMALE_EFFECT + "effect_fimale_06.png",
						FIMALE_EFFECT + "effect_fimale_07.png",
						FIMALE_EFFECT + "effect_fimale_08.png",
						FIMALE_EFFECT + "effect_fimale_09.png",
						FIMALE_EFFECT + "effect_fimale_10.png",
					)
				},
			),
		},
		
		{
			"name" : "indicators",
			"type" : "window",

			"x" : (SCREEN_WIDTH/2)-300,
			"y" : (SCREEN_HEIGHT/2)- 320,
			
			"width" : 30,
			"height" : 30,
			
			"children" :
			(	
				
				{
					"name" : "indicate_0",
					"type" : "expanded_image",
					
					"x" : 20,
					"y" : -3,
					
					"image": CHAR_CREATE + "select_male_btn/slot_1_indicator.png",
				},
				{
					"name" : "indicate_1",
					"type" : "expanded_image",
					
					"x" : 9,
					"y" : -2,
					
					"image": CHAR_CREATE + "select_male_btn/slot_2_indicator.png",
				},
				{
					"name" : "indicate_2",
					"type" : "expanded_image",
					
					"x" : 0,
					"y" : 0,
					
					"image": CHAR_CREATE + "select_male_btn/slot_3_indicator.png",
				},
				{
					"name" : "indicate_3",
					"type" : "expanded_image",
					
					"x" : 9,
					"y" : 0,
					
					"image": CHAR_CREATE + "select_male_btn/slot_4_indicator.png",
				},
				# {
					# "name" : "indicate_4",
					# "type" : "expanded_image",
					
					# "x" : 17,
					# "y" : -1,
					
					# "image": CHAR_CREATE + "select_male_btn/slot_5_indicator.png",
				# },
				
				## FEMALE
				
				{
					"name" : "indicate_4",
					"type" : "expanded_image",
					
					"x" : 24,
					"y" : 3,
					
					"image": CHAR_CREATE + "select_fimale_btn/slot_1_indicator.png",
				},
				{
					"name" : "indicate_5",
					"type" : "expanded_image",
					
					"x" : 24,
					"y" : 3,
					
					"image": CHAR_CREATE + "select_fimale_btn/slot_2_indicator.png",
				},
				{
					"name" : "indicate_6",
					"type" : "expanded_image",
					
					"x" : 25,
					"y" : 6,
					
					"image": CHAR_CREATE + "select_fimale_btn/slot_3_indicator.png",
				},
				{
					"name" : "indicate_7",
					"type" : "expanded_image",
					
					"x" : 23,
					"y" : 5,
					
					"image": CHAR_CREATE + "select_fimale_btn/slot_4_indicator.png",
				},
				{
					"name" : "indicate_8",
					"type" : "expanded_image",
					
					"x" : 21,
					"y" : 5,
					
					"image": CHAR_CREATE + "select_fimale_btn/slot_5_indicator.png",
				},
			),
		},
		
		{
			"name" : "action_buttons",
			"type" : "window",

			"x" : (SCREEN_WIDTH/2)-120,
			"y" : (SCREEN_HEIGHT/2)+ 180,
			
			"width" : 280,
			"height" : 110,
			
			"children" :
			(
				{
					"name" : "shape_board",
					"type" : "expanded_image",

					"x" : 3,
					"y" : 40,

					"image": CHAR_CREATE + "action_buttons/shape_board.png",
					"children" :
					(
						{
							"name" : "chenar",
							"type" : "expanded_image",

							"x" : 52,
							"y" : -40,

							"image": CHAR_CREATE + "action_buttons/name_chenar.png",
							"children" :
							(
								{
									"name" : "character_name_txt",
									"type" : "text",

									"x" : 12,
									"y" : 5,

									"text" : localeInfo.NAME,
									"fontname" : "Tahoma Bold:16.5",
									"color" : 0xffffd286,
									"text_horizontal_align" : "left",
								},
								{
									"name" : "character_name_value",
									"type" : "editline",

									"x" : 43+18,
									"y" : 6,

									"input_limit" : 12,

									"width" : 90,
									"height" : 20,
									"color" : 0xffffd286,
									"fontname" : "Tahoma Bold:14",
								},
							),
							
						},
						{
							"name" : "shape_board",
							"type" : "expanded_image",

							"x" : -53,
							"y" : -27,

							"image": CHAR_CREATE + "action_buttons/decoration_2.png",
						},
						{
							"name" : "shape_board",
							"type" : "expanded_image",

							"x" : 223,
							"y" : -27,

							"image": CHAR_CREATE + "action_buttons/decoration_1.png",
						},
						{
							"name" : "exit_button",
							"type" : "button",

							"x" : 8,
							"y" : 5,

							"default_image" : CHAR_CREATE + "action_buttons/exit_button_normal.png",
							"over_image" : CHAR_CREATE + "action_buttons/exit_button_hover.png",
							"down_image" : CHAR_CREATE + "action_buttons/exit_button_active.png",
							"disable_image" : CHAR_CREATE + "action_buttons/exit_button_disabled.png",
						
						},
						{
							"name" : "create_button",
							"type" : "button",

							"x" : 44,
							"y" : 5,

							"default_image" : CHAR_CREATE + "action_buttons/create_button_normal.png",
							"over_image" : CHAR_CREATE + "action_buttons/create_button_hover.png",
							"down_image" : CHAR_CREATE + "action_buttons/create_button_active.png",
							"disable_image" : CHAR_CREATE + "action_buttons/create_button_disabled.png",
							"children" :
							(
								{
									"name" : "text",
									"type" : "text",

									"x" : 52,
									"y" : 12,

									"text" : localeInfo.CONFIRM,
									"fontname" : "Tahoma Bold:17",
									"color" : 0xffa2c6c6,
									"text_horizontal_align" : "left",
								},
							),
						},
						{
							"name" : "shape_button",
							"type" : "button",

							"x" : 221,
							"y" : 5,

							"default_image" : CHAR_CREATE + "action_buttons/shape_button_normal.png",
							"over_image" : CHAR_CREATE + "action_buttons/shape_button_hover.png",
							"down_image" : CHAR_CREATE + "action_buttons/shape_button_active.png",
							"disable_image" : CHAR_CREATE + "action_buttons/shape_button_disabled.png",
						
						},
					),
				},
			
			),
		},
	),
}
