import uiScriptLocale

PATCH_IMG = "battlepass/"

window = {
	"name" : "BattlePassWindows",
	"style" : ("movable", "float", "animate",),

	"x" : (SCREEN_WIDTH / 2) -250,
	"y" : (SCREEN_HEIGHT / 2) - 200,

	"width" : 424,
	"height" : 390,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 424,
			"height" : 390,

			"children" :
			(
				## Title
				{
					"name" : "titlebar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 8,

					"width" : 424-15,

					"children" :
					(
						{ "name":"titlename", "type":"text", "x":0, "y":3, "text" : "Battle Pass", "horizontal_align":"center", "text_horizontal_align":"center" },
					),
				},

				{
					"name" : "marco_img",
					"type" : "image",
					"x"	   : 10,
					"y"	   : 35,
					"image" : PATCH_IMG +"marco_bp.tga",
					"children":
					(
						{
							"name" : "banner",
							"type" : "image",
							"x"	   : 4,
							"y"	   : 4,
							"image" : PATCH_IMG +"banner1.tga",
						},
					),
				},
				{
					"name" : "slot_base_img",
					"type" : "image",
					"x"	   : 215,
					"y"	   : 50,
					"image" : PATCH_IMG +"slot_item.tga",
					"children":
					(
						{
							"name" : "slot",
							"type" : "slot",

							"x"	:	8,
							"y"	:	7,

							"width" : 120+30,
							"height" : 32,

							"slot": (
								{"index": 0, "x":0, "y":0, "width":32, "height":32},
								{"index": 1, "x":0+40, "y":0, "width":32, "height":32},
								{"index": 2, "x":0+(40*2), "y":0, "width":32, "height":32},
								{"index": 3, "x":0+(40*3), "y":0, "width":32, "height":32},

							),
						},
					),
				},
				{
					"name" : "recibir_recompensa_button",
					"type" : "button",

					"x" : 230,
					"y" : 103,

					"text" : "Recibir Recompensa",

					"default_image" : PATCH_IMG + "no_reward.tga",
					"over_image" : PATCH_IMG + "no_reward.tga",
					"down_image" : PATCH_IMG + "no_reward.tga",
				},

				{
					"name" : "barra_titulos",
					"type" : "image",
					"x"	   : 13,
					"y"	   : 138,
					"image" : PATCH_IMG +"barra_titulos.tga",
					"children":
					(
						{ "name":"tittle_titulos", "type":"text", "x":195, "y":3, "text":"Informacion General", "text_horizontal_align":"center" },
					),
				},

				{
					"name" : "marco_info",
					"type" : "image",
					"x"	   : 13,
					"y"	   : 158,
					"image" : PATCH_IMG +"marco_info.tga",

					"children":
					(
						{
							"name" : "barra_fondo_info",
							"type" : "image",
							"x"	   : 4,
							"y"	   : 25,
							"image" : PATCH_IMG +"barra_fondo_info.tga",
						},


						{ "name":"state", "type":"text", "x":100, "y":5, "text":"Estado: Activo", "text_horizontal_align":"center" },
						{ "name":"time_r", "type":"text", "x":100+195, "y":5, "text":"Tiempo Restante: 30d 3h 22min", "text_horizontal_align":"center" },
						{ "name":"mounth", "type":"text", "x":98, "y":5+23, "text":"Pase de Batalla: Agosto 2021", "text_horizontal_align":"center" },
						{ "name":"mision_complete_total", "type":"text", "x":100+195, "y":5+23, "text":"Misiones completadas: 5 / 10", "text_horizontal_align":"center" },

					),
				},

				



				{
					"name" : "barra_misiones",
					"type" : "image",
					"x"	   : 13,
					"y"	   : 138+74,
					"image" : PATCH_IMG +"barra_titulos.tga",
					"children":
					(

						{
							"name" : "corona_oro_1",
							"type" : "image",
							"x"	   : 115,
							"y"	   : 2,
							"image" : PATCH_IMG +"corona_oro.tga",
						},

						{ "name":"tittle_titulos", "type":"text", "x":196, "y":3, "text":"Misiones Disponibles", "text_horizontal_align":"center" },

						{
							"name" : "corona_oro_2",
							"type" : "image",
							"x"	   : 115+137,
							"y"	   : 2,
							"image" : PATCH_IMG +"corona_oro.tga",
						},

					),
				},


			),
		},
	),
}