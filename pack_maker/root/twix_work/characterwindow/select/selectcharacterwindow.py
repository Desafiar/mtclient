import uiscriptlocale

window = {
	"name" : "selectcharacterwindow",
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
			
			"image" : "twix_work/characterwindow/background_vyber.tga",
			
			"children" : 
			(
				{
					"name" : "board_main",
					"type" : "window",
					
					"x" : 0, 
					"y" : 0,
					
					"width" : 480, 
					"height" : 600,
					
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
							
							"image" : "twix_work/characterwindow/select/board.tga",
							
							"children" : 
							(
								{
									"name" : "name_slotbar",
									"type" : "image",
									
									"x" : -200, 
									"y" : -97,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"image" : "twix_work/characterwindow/select/slotbar0.tga",
									
									"children" : 
									(
										{
											"name" : "name",
											"type" : "text",
											
											"x" : 0, 
											"y" : -5,
											
											"color" : 0xffc8aa80,
											"all_align" : True,
										},
									),
								},
								{
									"name" : "guild_slotbar",
									"type" : "image",
									
									"x" : -200, 
									"y" : -47,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"image" : "twix_work/characterwindow/select/slotbar1.tga",
									
									"children" : 
									(
										{
											"name" : "guild",
											"type" : "text",
											
											"x" : 0, 
											"y" : -5,
											
											"color" : 0xffc8aa80,
											"all_align" : True,
										},
									),
								},
								{
									"name" : "level_slotbar",
									"type" : "image",
									
									"x" : -200, 
									"y" : 2,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"image" : "twix_work/characterwindow/select/slotbar2.tga",
									
									"children" : 
									(
										{
											"name" : "level",
											"type" : "text",
											
											"x" : 0, 
											"y" : -5,
											
											"color" : 0xffc8aa80,
											"all_align" : True,
										},
									),
								},
								{
									"name" : "playtime_slotbar",
									"type" : "image",
									
									"x" : -200, 
									"y" : 53,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"image" : "twix_work/characterwindow/select/slotbar3.tga",
									
									"children" : 
									(
										{
											"name" : "playtime",
											"type" : "text",
											
											"x" : 0, 
											"y" : -5,
											
											"color" : 0xffc8aa80,
											"all_align" : True,
										},
									),
								},
								{
									"name" : "empire_slotbar",
									"type" : "image",
									
									"x" : -200, 
									"y" : 103,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"image" : "twix_work/characterwindow/select/slotbar4.tga",
									
									"children" : 
									(
										{
											"name" : "empire",
											"type" : "text",
											
											"x" : 0, 
											"y" : -5,
											
											"color" : 0xffc8aa80,
											"all_align" : True,
										},
									),
								},
								{
									"name" : "delete_button",
									"type" : "button",
									
									"x" : -200, 
									"y" : 230,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/select/smazat.tga",
									"over_image" : "twix_work/characterwindow/select/smazat_1.tga",
									"down_image" : "twix_work/characterwindow/select/smazat_2.tga",
									
									"children" : 
									(
										{
											"name" : "delete_text",
											"type" : "text",

											"x" : 27, 
											"y" : 7,

										},
									),
								},
								{
									"name" : "select_button",
									"type" : "button",
									
									"x" : -200, 
									"y" : 170,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/select/button_0.tga",
									"over_image" : "twix_work/characterwindow/select/button_1.tga",
									"down_image" : "twix_work/characterwindow/select/button_2.tga",
									
									"children" : 
									(
										{
											"name" : "select_text",
											"type" : "text",

											"x" : 30, 
											"y" : 7,

										},
									),
								},
								{
									"name" : "create_button",
									"type" : "button",
									
									"x" : -200, 
									"y" : 170,
									
									"vertical_align" : "center",
									"horizontal_align" : "center",
									
									"default_image" : "twix_work/characterwindow/create/vytvorit.tga",
									"over_image" : "twix_work/characterwindow/create/vytvorit_1.tga",
									"down_image" : "twix_work/characterwindow/create/vytvorit_2.tga",
									
									"children" : 
									(
										{
											"name" : "create_text",
											"type" : "text",

											"x" : 25, 
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
					
					"x" : -193, 
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
					
					"x" : 220, 
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