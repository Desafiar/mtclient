ROOT = "d:/ymir work/ui/minimap/"
RUTA_IMGS = "System/Dungeon/design/"
PATCH_IMG = "d_ranking_gremios/"

import localeInfo

window = {
	"name" : "MiniMap",

	"x" : SCREEN_WIDTH - 136,
	"y" : 0,

	"width" : 136,
	"height" : 137,

	"children" :
	(
		## OpenWindow
		{
			"name" : "OpenWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 136,
			"height" : 137,

			"children" :
			(
				{
					"name" : "OpenWindowBGI",
					"type" : "image",
					"x" : 0,
					"y" : 0,
					"image" : ROOT + "minimap.sub",
				},
				## MiniMapWindow
				{
					"name" : "MiniMapWindow",
					"type" : "window",

					"x" : 4,
					"y" : 5,

					"width" : 128,
					"height" : 128,
				},
				## ScaleUpButton
				{
					"name" : "ScaleUpButton",
					"type" : "button",

					"x" : 101,
					"y" : 116,

					"default_image" : ROOT + "minimap_scaleup_default.sub",
					"over_image" : ROOT + "minimap_scaleup_over.sub",
					"down_image" : ROOT + "minimap_scaleup_down.sub",
				},
				## ScaleDownButton
				{
					"name" : "ScaleDownButton",
					"type" : "button",

					"x" : 115,
					"y" : 103,

					"default_image" : ROOT + "minimap_scaledown_default.sub",
					"over_image" : ROOT + "minimap_scaledown_over.sub",
					"down_image" : ROOT + "minimap_scaledown_down.sub",
				},
				## MiniMapHideButton
				{
					"name" : "MiniMapHideButton",
					"type" : "button",

					"x" : 111,
					"y" : 6,

					"default_image" : ROOT + "minimap_close_default.sub",
					"over_image" : ROOT + "minimap_close_over.sub",
					"down_image" : ROOT + "minimap_close_down.sub",
				},
				## AtlasShowButton
				{
					"name" : "AtlasShowButton",
					"type" : "button",

					"x" : 12,
					"y" : 12,

					"default_image" : ROOT + "atlas_open_default.sub",
					"over_image" : ROOT + "atlas_open_over.sub",
					"down_image" : ROOT + "atlas_open_down.sub",
				},
				## Dungeon
				{
					"name" : "DungeonSystemButton",
					"type" : "button",

					"x" : -10,
					"y" : 55-15,

					"default_image" : "d:/ymir work/ui/game/minimapa/btn_timer_normal.png",
					"over_image" : "d:/ymir work/ui/game/minimapa/btn_timer_hover.png",
					"down_image" : "d:/ymir work/ui/game/minimapa/btn_timer_down.png",
				},
				## Biologo
				{
					"name" : "bio",
					"type" : "button",
					"x" : 0,
					"y" : 80,
					"default_image" : "d:/ymir work/ui/game/minimapa/btn_bio_normal.png",
					"over_image" : "d:/ymir work/ui/game/minimapa/btn_bio_hover.png",
					"down_image" : "d:/ymir work/ui/game/minimapa/btn_bio_down.png",
				},
				## Battle Pass
				{
					"name" : "battlepass",
					"type" : "button",
					"x" : 15,
					"y" : 105,
					"default_image" : "d:/ymir work/ui/game/minimapa/btn_battlepass_normal.png",
					"over_image" : "d:/ymir work/ui/game/minimapa/btn_battlepass_hover.png",
					"down_image" : "d:/ymir work/ui/game/minimapa/btn_battlepass_down.png",
				},
				## Ranking Guild
				# {
					# "name" : "RankingButton",
					# "type" : "button",
					# "x" : 0,
					# "y" : 80,
					# "default_image" : "d:/ymir work/ui/game/minimapa/rank_guild_0.tga",
					# "over_image" : "d:/ymir work/ui/game/minimapa/rank_guild_1.tga",
					# "down_image" : "d:/ymir work/ui/game/minimapa/rank_guild_2.tga",
				# },
				## ServerInfo
				{
					"name" : "ServerInfo",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 140,

					"text" : "",
				},
				## PositionInfo
				{
					"name" : "Title_New",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 160,

					"text" : localeInfo.SERVER_TIME,
				},

				## ObserverCount
				{
					"name" : "Hora",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 180,

					"text" : "",
				},

				## ObserverCount
				{
					"name" : "ObserverCount",
					"type" : "text",
					
					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 200,

					"text" : "",
				},
			),
		},
		{
			"name" : "CloseWindow",
			"type" : "window",
			"x" : 0,
			"y" : 0,
			"width" : 132,
			"height" : 48,
			"children" :
			(
				## ShowButton
				{
					"name" : "MiniMapShowButton",
					"type" : "button",
					"x" : 100,
					"y" : 4,
					"default_image" : ROOT + "minimap_open_default.sub",
					"over_image" : ROOT + "minimap_open_default.sub",
					"down_image" : ROOT + "minimap_open_default.sub",
				},
			),
		},
	),
}
