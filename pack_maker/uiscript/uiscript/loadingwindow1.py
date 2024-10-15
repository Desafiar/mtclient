import uiScriptLocale
import app

INTERFACE_PATH = "d:/ymir work/ui/gui_interface/"

window = {
	"name" : "LoadingWindow",
	"sytle" : ("movable","ltr",),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		{
			"name":"ErrorMessage", 
			"type":"text", "x":10, "y":10, 
			"text": uiScriptLocale.LOAD_ERROR, 
		},
		
		{
			"name" : "GageBoard",
			"type" : "window",
			"x" : float(SCREEN_WIDTH) / 2  - 268/2,
			"y" : float(SCREEN_HEIGHT) / 2 - 50,
			"width" : 268, 
			"height": 268,

			"children" :
			(
				{
					"name" : "BackGage",
					"type" : "ani_image",


					"x" : -15,
					"y" : -100,

					"delay" : 1,

					"images" :
					(
						"locale/en/ui/loading/load/x1.png",
						"locale/en/ui/loading/load/x2.png",
						"locale/en/ui/loading/load/x3.png",
						"locale/en/ui/loading/load/x4.png",
						"locale/en/ui/loading/load/x5.png",
						"locale/en/ui/loading/load/x6.png",
						"locale/en/ui/loading/load/x7.png",
						"locale/en/ui/loading/load/x8.png",
						"locale/en/ui/loading/load/x9.png",
						"locale/en/ui/loading/load/x10.png",
						"locale/en/ui/loading/load/x11.png",
						"locale/en/ui/loading/load/x12.png",
						"locale/en/ui/loading/load/x13.png",
						"locale/en/ui/loading/load/x14.png",
						"locale/en/ui/loading/load/x15.png",
						"locale/en/ui/loading/load/x16.png",
						"locale/en/ui/loading/load/x17.png",
						"locale/en/ui/loading/load/x18.png",
						"locale/en/ui/loading/load/x19.png",
						"locale/en/ui/loading/load/x20.png",
						"locale/en/ui/loading/load/x21.png",
						"locale/en/ui/loading/load/x22.png",
						"locale/en/ui/loading/load/x23.png",
						"locale/en/ui/loading/load/x1.png",
						"locale/en/ui/loading/load/x2.png",
						"locale/en/ui/loading/load/x3.png",
					)
				},
			),
		},
	),
}
