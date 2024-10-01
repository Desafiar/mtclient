import uiScriptLocale
import nano_interface
window = {
	"name" : "PopupDialog",
	"style" : ("float",),

	# "x" : SCREEN_WIDTH/2 - 250,
	# "y" : SCREEN_HEIGHT/2 - 40,
	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		{
			"name" : "Shad_BackGround", 
			"type" : "nano_image",
			"x" : 0,
			"y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image": nano_interface.PATCH + "background_shd.png",
		},
		{
			"name" : "board",
			"type" : "board_nano",
			"x" : (SCREEN_WIDTH/2) - 150,
			"y" : (SCREEN_HEIGHT/2) - 50,

			"width" : 280,
			"height" : 105,

			"children" :
			(
				{
					"name" : "message",
					"type" : "text",

					"x" : 0,
					"y" : 38,

					"text" : uiScriptLocale.MESSAGE,
					
					"fontname" : "Tahoma:16",
					"color" : nano_interface.COLOR_HOVER2,
					
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				
				{
					"name" : "accept",
					"type" : "button",

					"x" : 0,
					"y" : 69,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					# "text" : uiScriptLocale.OK,

					"default_image" : nano_interface.COMMON + "dialog/btn_dialog_normal.png",
					"over_image" : nano_interface.COMMON + "dialog/btn_dialog_hover.png",
					"down_image" : nano_interface.COMMON + "dialog/btn_dialog_active.png",
					"children" :
					(
						{
							"name" : "dec", 
							"type" : "image",
							"x" : 68,
							"y" : 17,
							
							"image" : nano_interface.COMMON + "dialog/dec_left.png",
						},
						
						{
							"name" : "dec2", 
							"type" : "image",
							"x" : -4,
							"y" : 17,
							
							"image" : nano_interface.COMMON + "dialog/dec_right.png",
						},
						
						{
							"name" : "text",
							"type" : "text",

							"x" : 0,
							"y" : 0,
							
							"all_align" : "center",
							"fontname" : "Tahoma:16",
							"text" : uiScriptLocale.OK,
							"color" : nano_interface.COLOR_HOVER2,
						},
					),
				},
			),
		},
	),
}