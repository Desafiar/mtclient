
import localeInfo

ROOT = "d:/ymir work/ui/game/12zi/bead/"

window = {
	"name" : "BeadWindow",

	"x" : SCREEN_WIDTH - 134,
	"y" : 0,

	"width" : 30,
	"height" : 30,

	"children" :
	(
		{
			"name" : "Bead_image",
			"type" : "button",

			"x" : 0,
			"y" : 0,

			"default_image" : ROOT + "bead_default.sub",
			"over_image" : ROOT + "bead_over.sub",
			"down_image" : ROOT + "bead_down.sub",
		},
		{
			"name" : "beadInfo",
			"type" : "text",
			"x" : 15,
			"y" : 15,
			"text" : "0"
		},
		
	),
}
