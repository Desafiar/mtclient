import uiScriptLocale
import item
import app
import player

COSTUME_START_INDEX = item.COSTUME_SLOT_START
SHINING_START_INDEX = item.SHINING_SLOT_START
SKIN_SASH_START_INDEX = item.SKIN_SASH_SLOT_START

IMG_WIDTH = 177
IMG_HEIGHT = 200
Y_EXTRA = 30
X_EXTRA = 7

if app.ENABLE_WEAPON_COSTUME_SYSTEM:
	window = {
		"name" : "CostumeWindow",

		"x" : SCREEN_WIDTH - 175 - (IMG_WIDTH+(X_EXTRA*2)) - 33,
		"y" : SCREEN_HEIGHT - 37 - 565 + 5,

		"style" : ("movable", "float", "animate",),

		"width" : IMG_WIDTH+(X_EXTRA*2),
		"height" : Y_EXTRA+IMG_HEIGHT+X_EXTRA,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),

				"x" : 0,
				"y" : 0,

				"width" : IMG_WIDTH+(X_EXTRA*2),
				"height" : Y_EXTRA+IMG_HEIGHT+X_EXTRA,
			
				"children" :
				(
					## Title
					{
						"name" : "TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),
						"x" : 6,
						"y" : 6,

						"width" :  IMG_WIDTH+(X_EXTRA*2) - 10,
						"color" : "yellow",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":((IMG_WIDTH+(X_EXTRA*2)) - 15) / 2, "y":3, "text":uiScriptLocale.COSTUME_WINDOW_TITLE, "text_horizontal_align":"center" },
						),
					},

					## Costume Slot
					{
						"name" : "Costume_Base",
						"type" : "image",
						"x" : X_EXTRA,
						"y" : Y_EXTRA,
						"image" : "d:/ymir work/ui/game/costume/new_costume_window2.tga",
					},
				),
			},
		),
	}