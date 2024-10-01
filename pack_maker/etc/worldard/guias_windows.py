import uiScriptLocale

ROOT = "WorldArd/"

window = {
	"name" : "GuiasWindows",
	
	"x" : SCREEN_WIDTH - 136 - 140,
	"y" : 15,
	
	"width" : 59,
	"height" : 32,
	
	"children" :
	(
		{
			"name" : "guias_window",
			"type" : "window",
			
			"x" : 0,
			"y" : 0,
			
			"width" : 59,
			"height" : 32,
			
			"children" :
			(
				{
					"name" : "guias_button",
					"type" : "button",
					
					"x" : 0,
					"y" : 0,
					
					"default_image" : ROOT + "guias_1.tga",
					"over_image" : ROOT + "guias_2.tga",
					"down_image" : ROOT + "guias_3.tga",
				},
			),
		},		
	),	
}
