import uiScriptLocale

ROOT = "WorldArd/"

window = {
	"name" : "DiscordWindows",
	
	"x" : SCREEN_WIDTH - 136 - 140,
	"y" : 15,
	
	"width" : 59,
	"height" : 32,
	
	"children" :
	(
		{
			"name" : "discord_window",
			"type" : "window",
			
			"x" : 0,
			"y" : 0,
			
			"width" : 59,
			"height" : 32,
			
			"children" :
			(
				{
					"name" : "discord_button",
					"type" : "button",
					
					"x" : 0,
					"y" : 0,
					
					"default_image" : ROOT + "discord_1.tga",
					"over_image" : ROOT + "discord_2.tga",
					"down_image" : ROOT + "discord_3.tga",
				},
			),
		},		
	),	
}
