import uiscriptlocale

window = {
	"name" : "CreateCharacterWindow",
	"x" : 0, 
	"y" : 0,
	
	"width" : SCREEN_WIDTH,	
	"height" : SCREEN_HEIGHT,
	
	"children" : 
	(
		{
			"name" : "BackGround",
			"type" : "expanded_image",
			
			"x" : 0, 
			"y" : 0,
			
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			
			"image" : "twix_work/characterwindow/background_vytvorit.tga",
			
			"children" : 
			(
				{
					"name" : "board_main",
					"type" : "window",
					
					"x" : 0, 
					"y" : 0,
					
					"width" : 352, 
					"height" : 457,
					
					"vertical_align" : "center",
					"horizontal_align" : "left",
					
					"children" :
					(
						{
							"name" : "board",
							"type" : "image",
							
							"x" : 100, 
							"y" : 0,
							
							"vertical_align" : "center",
							"horizontal_align" : "left",
							
							"image" : "twix_work/characterwindow/create/board.tga",
							
							"children" : 
							(
								{
									"name" : "name_slotbar",
									"type" : "image",
									
									"x" : 0, 
									"y" : -118,
									
									"horizontal_align" : "center",
									"vertical_align" : "center",
									
									"image" : "twix_work/characterwindow/create/slotbar.tga",
									
									"children" : 
									(
										{
											"name" : "name",
											"type" : "editline",
											
											"x" : 17, 
											"y" : 30,
											
											"width" : 200, 
											"height" : 16,
											
											"color" : 0xffc8aa80,
											"input_limit": 16,
											
											"enable_codepage": 0,
										},
									),
								},
								{
									"name" : "name_warrior",
									"type" : "image",

									"x" : 88,
									"y" : 110,
								},
								{
									"name" : "name_assassin",
									"type" : "image",

									"x" : 88,
									"y" : 110,
								},
								{
									"name" : "name_sura",
									"type" : "image",

									"x" : 88,
									"y" : 110,
								},
								{
									"name" : "name_shaman",
									"type" : "image",

									"x" : 88,
									"y" : 110,
								},
								{
									"name" : "name_wolfman",
									"type" : "image",

									"x" : 88,
									"y" : 110,
								},
								{
									"name" : "name_elfe",
									"type" : "image",

									"x" : 88,
									"y" : 110,
								},
								{
									"name" : "shape1",
									"type" : "radio_button",
									
									"x" : -45, 
									"y" : -90,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/create/vzhled.tga",
									"over_image" : "twix_work/characterwindow/create/vzhled_1.tga",
									"down_image" : "twix_work/characterwindow/create/vzhled_2.tga",
									
									"children" : 
									(
										{
											"name" : "shape1_text",
											"type" : "text",

											"x" : 23, 
											"y" : 7,

										},
									),
								},
								{
									"name" : "shape2",
									"type" : "radio_button",
									
									"x" : 45, 
									"y" : -90,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/create/vzhled_3.tga",
									"over_image" : "twix_work/characterwindow/create/vzhled_4.tga",
									"down_image" : "twix_work/characterwindow/create/vzhled_5.tga",
									
									"children" : 
									(
										{
											"name" : "shape2_text",
											"type" : "text",

											"x" : 23, 
											"y" : 7,
										},
									),
								},
								{
									"name" : "gender_man",
									"type" : "radio_button",
									
									"x" : -45, 
									"y" : 20,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/create/muz.tga",
									"over_image" : "twix_work/characterwindow/create/muz_1.tga",
									"down_image" : "twix_work/characterwindow/create/muz_2.tga",
									
									"children" : 
									(
										{
											"name" : "man_text",
											"type" : "text",

											"x" : 31, 
											"y" : 7,
										},
									),
								},
								{
									"name" : "gender_woman",
									"type" : "radio_button",
									
									"x" : 45, 
									"y" : 20,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/create/zena.tga",
									"over_image" : "twix_work/characterwindow/create/zena_1.tga",
									"down_image" : "twix_work/characterwindow/create/zena_2.tga",
									
									"children" : 
									(
										{
											"name" : "woman_text",
											"type" : "text",

											"x" : 31, 
											"y" : 7,
										},
									),
								},
								{
									"name" : "create_button",
									"type" : "button",
									
									"x" : 0, 
									"y" : 156,
									
									"vertical_align" : "center",
									"horizontal_align" : "left",
									
									"default_image" : "twix_work/characterwindow/create/vytvorit.tga",
									"over_image" : "twix_work/characterwindow/create/vytvorit_1.tga",
									"down_image" : "twix_work/characterwindow/create/vytvorit_2.tga",
									
									"children" : 
									(
										{
											"name" : "create_text",
											"type" : "text",

											"x" : 24, 
											"y" : 7,
										},
									),
								},
							),
						},
					),
				},
				{
					"name" : "left_button",
					"type" : "button",
					
					"x" : -180, 
					"y" : 20,
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"default_image" : "twix_work/characterwindow/select/left_0.tga",
					"over_image" : "twix_work/characterwindow/select/left_1.tga",
					"down_image" : "twix_work/characterwindow/select/left_2.tga",
				},
				{
					"name" : "right_button",
					"type" : "button",
					
					"x" : 240, 
					"y" : 20,
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
					
					"default_image" : "twix_work/characterwindow/select/right_0.tga",
					"over_image" : "twix_work/characterwindow/select/right_1.tga",
					"down_image" : "twix_work/characterwindow/select/right_2.tga",
				},
				{
					"name" : "exit_button",
					"type" : "button",
						
					"x" : SCREEN_WIDTH - 110, 
					"y" : 10,
							
					"default_image" : "twix_work/loginwindow/button_0.tga",
					"over_image" :  "twix_work/loginwindow/button_1.tga",
					"down_image" : "twix_work/loginwindow/button_2.tga",

					"children" : 
					(
						{
							"name" : "exit_text",
							"type" : "text",

							"x" : 36, 
							"y" : 7,

							"text" : uiscriptlocale.LOGIN_EXIT,
							"color" : 0xffe8b478,
						},
					),
				},
			),
		},
	),
}
