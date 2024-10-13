import app
import uiScriptLocale

window = {
	"name" : "LoginWindow",
	"sytle" : ("movable",),

	"x" : 0, 
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" : 
	(
		# pozadí
		{
			"name" : "background", 
			"type" : "expanded_image",

			"x" : 0, 
			"y" : 0,

			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,

			"image" : "twix_work/loginwindow/background.tga",
		},
		# pozadí_login
		{
			"name" : "board_main",
			"type" : "window",
					
			"x" : -200, 
			"y" : 0,
					
			"width" : 1920, 
			"height" : 1080,
					
			"vertical_align" : "center",
			"horizontal_align" : "center",
					
			"children" :
			(
				{
					"name" : "board",
					"type" : "image",
							
					"x" : 0, 
					"y" : 50,
					
					"vertical_align" : "center",
					"horizontal_align" : "center",
							
					"image" : "twix_work/loginwindow/board.tga",
							
					"children" : 
					(
						{
							"name" : "id_slotbar",
							"type" : "image",
									
							"x" : 0, 
							"y" : -39,
									
							"horizontal_align" : "center",
							"vertical_align" : "center",
									
							"image" : "twix_work/loginwindow/slotbar.tga",
									
							"children" : 
							(
								{
									"name" : "id",
									"type" : "editline",
											
									"x" : 12, 
									"y" : 10,
											
									"width" : 200, 
									"height" : 16,
											
									"color" : 0xffd80000,
									"input_limit": 16,
								},
							),
						},
						{
							"name" : "pwd_slotbar",
							"type" : "image",
									
							"x" : 0, 
							"y" : 7,
							
							"horizontal_align" : "center",
							"vertical_align" : "center",
									
							"image" : "twix_work/loginwindow/slotbar.tga",
									
							"children" : 
							(
								{
									"name" : "pwd",
									"type" : "editline",
											
									"x" : 12, 
									"y" : 10,
											
									"width" : 200, 
									"height" : 16,
											
									"color" : 0xffd80000,
									"input_limit": 16,
									"secret_flag": 1,
								},
							),
						},
						{
							"name" : "login_button",
							"type" : "button",

							"x" : -10, 
							"y" : 83+35,

							"horizontal_align" : "center",
							"vertical_align" : "center",

							"default_image" : "twix_work/loginwindow/prihlasit.tga", 
							"over_image" : "twix_work/loginwindow/prihlasit_1.tga",
							"down_image" : "twix_work/loginwindow/prihlasit_2.tga",

							"children" : 
							(
								{
									"name" : "login_text",
									"type" : "text",
											
									"x" : 38, 
									"y" : 7,
								},
							),
						},
					),
				},
			),
		},
		{
			"name" : "changechannel",
			"type" : "image",
			
			"x" : -15,
			"y" : -200,

			"image": "twix_work/loginwindow/channel/board.tga",
			
			"horizontal_align" : "center",
			"vertical_align" : "center",

			"children" :
			(
				{
					"name" : "ch1",
					"type" : "radio_button",
					
					"x" : -160, 
					"y" : 40,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					"default_image" : "twix_work/loginwindow/channel/button_ch1_0.tga",
					"over_image" : "twix_work/loginwindow/channel/button_ch1_1.tga",
					"down_image" : "twix_work/loginwindow/channel/button_ch1_2.tga",
					
					"children" : 
					(
						{
							"name" : "ch1_text",
							"type" : "text",
									
							"x" : 0, 
							"y" : 0,
									
							"text" : "",
							"color" : 0xffffffff,
						},
					),
				},
				{
					"name" : "ch2",
					"type" : "radio_button",
					
					"x" : -90, 
					"y" : 40,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					"default_image" : "twix_work/loginwindow/channel/button_ch2_0.tga",
					"over_image" : "twix_work/loginwindow/channel/button_ch2_1.tga",
					"down_image" : "twix_work/loginwindow/channel/button_ch2_2.tga",

					"children" : 
					(
						{
							"name" : "ch2_text",
							"type" : "text",
									
							"x" : 0, 
							"y" : 6,
									
							"text" : "",
							"color" : 0xffffffff,
						},
					),
				},
				{
					"name" : "ch3",
					"type" : "radio_button",
					
					"x" : -20, 
					"y" : 40,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					"default_image" : "twix_work/loginwindow/channel/button_ch3_0.tga",
					"over_image" : "twix_work/loginwindow/channel/button_ch3_1.tga",
					"down_image" : "twix_work/loginwindow/channel/button_ch3_2.tga",
					
					"children" : 
					(
						{
							"name" : "ch3_text",
							"type" : "text",
									
							"x" : 0, 
							"y" : 6,
									
							"text" : "",
							"color" : 0xffffffff,
						},
					),
				},
				{
					"name" : "ch4",
					"type" : "radio_button",
					
					"x" : 50, 
					"y" : 40,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					"default_image" : "twix_work/loginwindow/channel/button_ch4_0.tga",
					"over_image" : "twix_work/loginwindow/channel/button_ch4_1.tga",
					"down_image" : "twix_work/loginwindow/channel/button_ch4_2.tga",
					
					"children" : 
					(
						{
							"name" : "ch4_text",
							"type" : "text",
									
							"x" : 0, 
							"y" : 6,
									
							"text" : "",
							"color" : 0xffffffff,
						},
					),
				},
				{
					"name" : "ch5",
					"type" : "radio_button",
					
					"x" : 120, 
					"y" : 40,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					#"default_image" : "twix_work/loginwindow/channel/button_ch5_0.tga",
					#"over_image" : "twix_work/loginwindow/channel/button_ch5_1.tga",
					#"down_image" : "twix_work/loginwindow/channel/button_ch5_2.tga",
					
					"children" : 
					(
						{
							"name" : "ch5_text",
							"type" : "text",
									
							"x" : 0, 
							"y" : 6,
									
							"text" : "",
							"color" : 0xffffffff,
						},
					),
				},
				{
					"name" : "ch6",
					"type" : "radio_button",
					
					"x" : 190, 
					"y" : 50,
					
					"horizontal_align" : "center",
					"vertical_align" : "center",
					
					#"default_image" : "twix_work/loginwindow/channel/button_ch6_0.tga",
					#"over_image" : "twix_work/loginwindow/channel/button_ch6_1.tga",
					#"down_image" : "twix_work/loginwindow/channel/button_ch6_2.tga",
					
					"children" : 
					(
						{
							"name" : "ch6_text",
							"type" : "text",
									
							"x" : 0, 
							"y" : 6,
									
							"text" : "",
							"color" : 0xffffffff,
						},
					),
				},
			),
		},	
		{
			"name" : "account_board",
			"type" : "image",
			
			"x" : 500,
			"y" : 50,

			"horizontal_align" : "right",
			"vertical_align" : "center",

			"image" : "twix_work/loginwindow/account/board.tga",

			"children" :
			(
				{
					"name" : "account_0_image",
					"type" : "image",
					
					"x" : 28, 
					"y" : 24,
					
					"image" : "twix_work/loginwindow/slotbar.tga",
					
					"children" : 
					(
						{
							"name" : "account_0_text",
							"type" : "text",

							"x" : 0, 
							"y" : -1,

							"color" : 0xffffffff,
							"all_align" : True,
						},
					),
				},
				{
					"name" : "delete_button_0",
					"type" : "button",
					
					"x" : 260, 
					"y" : 27,
					
					"default_image" : "twix_work/loginwindow/account/delete_0.tga",
					"over_image" :  "twix_work/loginwindow/account/delete_1.tga",
					"down_image" : "twix_work/loginwindow/account/delete_2.tga",
				},
				{
					"name" : "save_button_0",
					"type" : "button",
					
					"x" : 260, 
					"y" : 27,
					
					"default_image" : "twix_work/loginwindow/account/save_0.tga",
					"over_image" :  "twix_work/loginwindow/account/save_1.tga",
					"down_image" : "twix_work/loginwindow/account/save_2.tga",
				},
				{
					"name" : "load_button_0",
					"type" : "button",
					
					"x" : 150, 
					"y" : 26,
					
					"default_image" : "twix_work/loginwindow/button_0.tga",
					"over_image" :  "twix_work/loginwindow/button_1.tga",
					"down_image" : "twix_work/loginwindow/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "load_text",
							"type" : "text",

							"x" : 40, 
							"y" : 7,

							"text" : "Naèíst",
							"color" : 0xffe8b478,
						},
					),
				},
				{
					"name" : "account_1_image",
					"type" : "image",
					"x" : 28, "y" : 74,
					"image" : "twix_work/loginwindow/slotbar.tga",
					"children" : 
					(
						{
							"name" : "account_1_text",
							"type" : "text",
							
							"x" : 0, 
							"y" : -1,
							
							"color" : 0xffffffff,
							"all_align" : True,
						},
					),
				},
				{
					"name" : "delete_button_1",
					"type" : "button",
					
					"x" : 260, 
					"y" : 77,
					
					"default_image" : "twix_work/loginwindow/account/delete_0.tga",
					"over_image" :  "twix_work/loginwindow/account/delete_1.tga",
					"down_image" : "twix_work/loginwindow/account/delete_2.tga",
				},
				{
					"name" : "save_button_1",
					"type" : "button",
					
					"x" : 260, 
					"y" : 77,
					
					"default_image" : "twix_work/loginwindow/account/save_0.tga",
					"over_image" :  "twix_work/loginwindow/account/save_1.tga",
					"down_image" : "twix_work/loginwindow/account/save_2.tga",
				},
				{
					"name" : "load_button_1",
					"type" : "button",
					
					"x" : 150, 
					"y" : 76,
					
					"default_image" : "twix_work/loginwindow/button_0.tga",
					"over_image" :  "twix_work/loginwindow/button_1.tga",
					"down_image" : "twix_work/loginwindow/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "load_text",
							"type" : "text",

							"x" : 40, 
							"y" : 7,

							"text" : "Naèíst",
							"color" : 0xffe8b478,
						},
					),
				},
				{
					"name" : "background", 
					"type" : "expanded_image",

					"x" : -35, 
					"y" : 58,

					"image" : "twix_work/loginwindow/mezera.tga",
				},
				{
					"name" : "background", 
					"type" : "expanded_image",

					"x" : -35, 
					"y" : 108,

					"image" : "twix_work/loginwindow/mezera.tga",
				},
				{
					"name" : "background", 
					"type" : "expanded_image",

					"x" : -35, 
					"y" : 158,

					"image" : "twix_work/loginwindow/mezera.tga",
				},
				{
					"name" : "account_2_image",
					"type" : "image",
					"x" : 28, "y" : 124,
					"image" : "twix_work/loginwindow/slotbar.tga",
					"children" : 
					(
						{
							"name" : "account_2_text",
							"type" : "text",
							
							"x" : 0, 
							"y" : -1,
							
							"color" : 0xffffffff,
							"all_align" : True,
						},
					),
				},
				{
					"name" : "delete_button_2",
					"type" : "button",
					
					"x" : 260, 
					"y" : 126,
					
					"default_image" : "twix_work/loginwindow/account/delete_0.tga",
					"over_image" :  "twix_work/loginwindow/account/delete_1.tga",
					"down_image" : "twix_work/loginwindow/account/delete_2.tga",
				},
				{
					"name" : "save_button_2",
					"type" : "button",
					
					"x" : 260, 
					"y" : 126,
					
					"default_image" : "twix_work/loginwindow/account/save_0.tga",
					"over_image" :  "twix_work/loginwindow/account/save_1.tga",
					"down_image" : "twix_work/loginwindow/account/save_2.tga",
				},
				{
					"name" : "load_button_2",
					"type" : "button",
					
					"x" : 150, 
					"y" : 125,
					
					"default_image" : "twix_work/loginwindow/button_0.tga",
					"over_image" :  "twix_work/loginwindow/button_1.tga",
					"down_image" : "twix_work/loginwindow/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "load_text",
							"type" : "text",

							"x" : 40, 
							"y" : 7,

							"text" : "Naèíst",
							"color" : 0xffe8b478,
						},
					),
				},
				{
					"name" : "account_3_image",
					"type" : "image",
					"x" : 28, "y" : 174,
					"image" : "twix_work/loginwindow/slotbar.tga",
					"children" : 
					(
						{
							"name" : "account_3_text",
							"type" : "text",
							
							"x" : 0, 
							"y" : -1,
							
							"color" : 0xffffffff,
							"all_align" : True,
						},
					),
				},
				{
					"name" : "delete_button_3",
					"type" : "button",
					
					"x" : 260, 
					"y" : 177,
					
					"default_image" : "twix_work/loginwindow/account/delete_0.tga",
					"over_image" :  "twix_work/loginwindow/account/delete_1.tga",
					"down_image" : "twix_work/loginwindow/account/delete_2.tga",
				},
				{
					"name" : "save_button_3",
					"type" : "button",
					
					"x" : 260, 
					"y" : 177,
					
					"default_image" : "twix_work/loginwindow/account/save_0.tga",
					"over_image" :  "twix_work/loginwindow/account/save_1.tga",
					"down_image" : "twix_work/loginwindow/account/save_2.tga",
				},
				{
					"name" : "load_button_3",
					"type" : "button",
					
					"x" : 150, 
					"y" : 176,
					
					"default_image" : "twix_work/loginwindow/button_0.tga",
					"over_image" :  "twix_work/loginwindow/button_1.tga",
					"down_image" : "twix_work/loginwindow/button_2.tga",
					
					"children" : 
					(
						{
							"name" : "load_text",
							"type" : "text",

							"x" : 40, 
							"y" : 7,

							"text" : "Naèíst",
							"color" : 0xffe8b478,
						},
					),
				},
			),
		},
		{
			"name" : "exit_button",
			"type" : "button",
				
			"x" : SCREEN_WIDTH - 190, 
			"y" : 10,
					
			"default_image" : "twix_work/loginwindow/ukoncit.tga",
			"over_image" :  "twix_work/loginwindow/ukoncit_1.tga",
			"down_image" : "twix_work/loginwindow/ukoncit_2.tga",

			"children" : 
			(
				{
					"name" : "exit_text",
					"type" : "text",

					"x" : 36, 
					"y" : 7,

				},
			),
		},
	),
}