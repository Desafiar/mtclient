##################### AICI INCEPE MUNCA ##################### ORA: 21:47

## LOCATII PENTRU IMAGINI ##
LOCATIE_FISIERE = "loginwindow_new/"
LOCATIE_FISIERE_BUTOANE = "loginwindow_new/butoane/" 
LOCATIE_FISIERE_CANAL = "loginwindow_new/channel/" 
## LOCATII PENTRU IMAGINI ##

window = {
		"sytle" : ("movable",),
		"x" : 0, "y" : 0,
		"width" : SCREEN_WIDTH,
		"height" : SCREEN_HEIGHT,
		"children" : (
				{
					"name" : "background", 
					"type" : "expanded_image",
					"x" : 0, "y" : 0,
					"x_scale" : float(SCREEN_WIDTH) / 1366.0,
					"y_scale" : float(SCREEN_HEIGHT) / 768.0,
					"image" : LOCATIE_FISIERE + "background.tga",
					"children" : (
							{
									"name" : "board_main",
									"type" : "window",
									"x" : 0, "y" : 0,
									"width" : 352, "height" : 290,
									"vertical_align" : "center",
									"horizontal_align" : "center",
									"children" :(
											{
													"name" : "board",
													"type" : "image",
													"x" : 0, "y" : 0,
													"image" : LOCATIE_FISIERE + "board.tga",
													"children" : (
															{
																	"name" : "id_slotbar",
																	"type" : "image",
																	"x" : 0, "y" : -70,
																	"horizontal_align" : "center",
																	"vertical_align" : "center",
																	"image" : LOCATIE_FISIERE + "bar.tga",
																	"children" : (
																			{
																					"name" : "id",
																					"type" : "editline",
																					"x" : 12, "y" : 10,
																					"width" : 200, "height" : 16,
																					"color" : 0xffc8aa80,
																					"input_limit": 16,
																			},
																	),
															},
															{

																	"name" : "pwd_slotbar",
																	"type" : "image",
																	"x" : 0, "y" : -5,
																	"horizontal_align" : "center",
																	"vertical_align" : "center",
																	"image" : LOCATIE_FISIERE + "bar.tga",
																	"children" : (
																			{
																					"name" : "pwd",
																					"type" : "editline",
																					"x" : 12, "y" : 10,
																					"width" : 200, "height" : 16,
																					"color" : 0xffc8aa80,
																					"input_limit": 16,
																					"secret_flag": 1,
																			},
																	),
															},
													),
											},
## TEXT ID SI PAROLA ##
		{
			"name" : "pwd_image",
			"type" : "image",
			"x" : -120, "y" : -20,
			"horizontal_align" : "center",
			"vertical_align" : "center",
			"image" : LOCATIE_FISIERE + "password.tga",
		},
		{
			"name" : "id_image",
			"type" : "image",
			"x" : -120, "y" : -85,
			"horizontal_align" : "center",
			"vertical_align" : "center",
			"image" : LOCATIE_FISIERE + "username.tga",
		},
## BUTONUL DE LOGIN ##
		{
			"name" : "login_button",
			"type" : "button",
			"x" : -15, "y" : 78,
			"horizontal_align" : "center",
			"vertical_align" : "center",
			"default_image" : LOCATIE_FISIERE_BUTOANE + "login_0.tga", 
			"over_image" : LOCATIE_FISIERE_BUTOANE + "login_1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "login_2.tga",
		},
## BUTONUL PENTRU PAROLA UITATA ##
		{
			"name" : "parolauitata_button",
			"type" : "button",
			"x" : 48, "y" : 252,
			"default_image" : LOCATIE_FISIERE_BUTOANE + "parolauitata_0.tga",
			"over_image" :  LOCATIE_FISIERE_BUTOANE + "parolauitata_1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "parolauitata_2.tga",
		},
## BUTONUL PENTRU REGISTER ##
		{
			"name" : "register_button",
			"type" : "button",
			"x" : 3*48+21, "y" : 252,
			"default_image" : LOCATIE_FISIERE_BUTOANE + "inregistrare_0.tga",
			"over_image" : LOCATIE_FISIERE_BUTOANE + "inregistrare_1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "inregistrare_2.tga",
		},
										),
								},

## CANALE ##
		{
			"name" : "ch1",
			"type" : "radio_button",
			"x" : 175, "y" : -75,
			"horizontal_align" : "center",
			"vertical_align" : "center",
			"default_image" : LOCATIE_FISIERE_CANAL + "ch1_0.tga",
			"over_image" : LOCATIE_FISIERE_CANAL + "ch1_1.tga",
			"down_image" : LOCATIE_FISIERE_CANAL + "ch1_2.tga",
		},
		{
			"name" : "ch2",
			"type" : "radio_button",
			"x" : 175, "y" : -55,
			"horizontal_align" : "center",
			"vertical_align" : "center",
			"default_image" : LOCATIE_FISIERE_CANAL + "ch2_0.tga",
			"over_image" : LOCATIE_FISIERE_CANAL + "ch2_1.tga",
			"down_image" : LOCATIE_FISIERE_CANAL + "ch2_2.tga",
		},
		{
			"name" : "ch3",
			"type" : "radio_button",
			"x" : 175, "y" : -35,
			"horizontal_align" : "center",
			"vertical_align" : "center",
			"default_image" : LOCATIE_FISIERE_CANAL + "ch3_0.tga",
			"over_image" : LOCATIE_FISIERE_CANAL + "ch3_1.tga",
			"down_image" : LOCATIE_FISIERE_CANAL + "ch3_2.tga",
		},
		{
			"name" : "ch4",
			"type" : "radio_button",
			"x" : 175, "y" : -15,
			"horizontal_align" : "center",
			"vertical_align" : "center",
			"default_image" : LOCATIE_FISIERE_CANAL + "ch4_0.tga",
			"over_image" : LOCATIE_FISIERE_CANAL + "ch4_1.tga",
			"down_image" : LOCATIE_FISIERE_CANAL + "ch4_2.tga",
		},
####################
## BUTONUL DE IESIRE ##
		{
			"name" : "exit_button",
			"type" : "button",
			"x" : SCREEN_WIDTH - 115, "y" : 980,
			"default_image" : LOCATIE_FISIERE_BUTOANE + "exit_0.tga",
			"over_image" :  LOCATIE_FISIERE_BUTOANE + "exit_1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "exit_2.tga",
		},
## BUTONUL PENTRU WEBSITE ##
		{
			"name" : "website_button",
			"type" : "button",
			"x" : SCREEN_WIDTH - 1910, "y" : 980,
			"default_image" : LOCATIE_FISIERE_BUTOANE + "website_0.tga",
			"over_image" :  LOCATIE_FISIERE_BUTOANE + "website_1.tga",
			"down_image" : LOCATIE_FISIERE_BUTOANE + "website_2.tga",
		},
						),
				},
		),
}
##################### INSFARSIT AM GATAT ##################### ORA: 02:03