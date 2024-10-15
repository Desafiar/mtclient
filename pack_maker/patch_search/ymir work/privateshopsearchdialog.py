import uiScriptLocale
import item
import app
import localeInfo

LOCALE_PATH = "d:/ymir work/ui/privatesearch/"
GOLD_COLOR	= 0xFFFEE3AE
WIDTH=590
HEIGHT=350
window = {
	"name" : "PrivateShopSearchDialog",

	"x" : 650,
	"y" : 0,

	"style" : ("movable", "float", "animate",),

	"width" : WIDTH,
	"height" : HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),
			"x" : 0,
			"y" : 0,

			"width" : WIDTH,
			"height" : HEIGHT,
							
			"children" :
			(
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 5,
					"y" : 5,

					"width" : WIDTH-10,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":10, "y":1, "text":"Buscador de items en tienda", "all_align":"center" },
					),
				},
					## ItemName
				{
					"name" : "ItemNameImg",
					"type" : "image",
					"x" : 10,
					"y" : 275-238,
					"image" : LOCALE_PATH+"private_leftNameImg.sub",
					"children" :
					(
						{ "name" : "ItemNameText", "type" : "text", "text_horizontal_align":"center", "x" : 60, "y" : 5, "text" : "Nombre:", "color":GOLD_COLOR },
					),
				},
					## ItemNameEditLine
				{
					"name" : "ItemNameSlot",
					"type" : "image",
					"x" : 12,
					"y" : 295-238,
					"image" : LOCALE_PATH+"private_leftSlotImg.sub",
					"children" :
					(
						{
							"name" : "ItemNameValue",
							"type" : "editline",
							"x" : 2,
							"y" : 3,
							"width" : 136,
							"height" : 15,
							"input_limit" : 20,
							"text" : "",
						},
					),
				},
					## GoldText
				{
					"name" : "GoldImg",
					"type" : "image",
					"x" : 10,
					"y" : 215-138,
					"image" : LOCALE_PATH+"private_leftNameImg.sub",
					"children" :
					(
						{ "name" : "GoldText", "type" : "text", "text_horizontal_align":"center", "x" : 60, "y" : 5, "text" : "Precio:", "color":GOLD_COLOR },
					),
				},
					## GoldminEditLine
				{
					"name" : "GoldSlot",
					"type" : "image",
					"x" : 12,
					"y" : 235-138,
					"image" : LOCALE_PATH+"private_leftSlotImg.sub",

					"children" :
					(
						{
							"name" : "ItemGoldValue",
							"type" : "editline",
							"x" : 2,
							"y" : 3,
							"width" : 115,
							"height" : 15,
							"input_limit" : 10,
							"only_number" : 1,
							"text" : "0",
						},
					),
				},

				#All Function
				{
					"name" : "AllFunctionItems",
					"type" : "button",

					"x" : 10,
					"y" : 315-25,

					"text" : "Todos",

					"default_image" : LOCALE_PATH + "private_findbuttonImg01.sub",
					"over_image" : LOCALE_PATH + "private_findbuttonImg02.sub",
					"down_image" : LOCALE_PATH + "private_findbuttonImg03.sub",
				},
					## FindButton
				{
					"name" : "SearchButton",
					"type" : "button",

					"x" : 10,
					"y" : 315,

					"text" : "Buscar",

					"default_image" : LOCALE_PATH + "private_findbuttonImg01.sub",
					"over_image" : LOCALE_PATH + "private_findbuttonImg02.sub",
					"down_image" : LOCALE_PATH + "private_findbuttonImg03.sub",
				},

						
					## LeftTop
				{
					"name" : "LeftTop",
					"type" : "image",
					"x" : 133,
					"y" : 36,
					"image" : LOCALE_PATH+"private_mainboxlefttop.sub",
				},
					## RightTop
				{
					"name" : "RightTop",
					"type" : "image",
					"x" : 561,
					"y" : 36,
					"image" : LOCALE_PATH+"private_mainboxrighttop.sub",
				},
					## LeftBottom
				{
					"name" : "LeftBottom",
					"type" : "image",
					"x" : 133,
					"y" : 320,
					"image" : LOCALE_PATH+"private_mainboxleftbottom.sub",
				},
					## RightBottom
				{
					"name" : "RightBottom",
					"type" : "image",
					"x" : 561,
					"y" : 320,
					"image" : LOCALE_PATH+"private_mainboxrightbottom.sub",
				},
					## leftcenterImg
				{
					"name" : "leftcenterImg",
					"type" : "expanded_image",
					"x" : 133,
					"y" : 52,
					"image" : LOCALE_PATH+"private_leftcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 15),
				},
					## rightcenterImg
				{
					"name" : "rightcenterImg",
					"type" : "expanded_image",
					"x" : 560,
					"y" : 52,
					"image" : LOCALE_PATH+"private_rightcenterImg.tga",
					"rect" : (0.0, 0.0, 0, 15),
				},
					## topcenterImg
				{
					"name" : "topcenterImg",
					"type" : "expanded_image",
					"x" : 149,
					"y" : 36,
					"image" : LOCALE_PATH+"private_topcenterImg.tga",
					"rect" : (0.0, 0.0, 24, 0),
				},
					## bottomcenterImg
				{
					"name" : "bottomcenterImg",
					"type" : "expanded_image",
					"x" : 149,
					"y" : 320,
					"image" : LOCALE_PATH+"private_bottomcenterImg.tga",
					"rect" : (0.0, 0.0, 24, 0),
				},
					## centerImg
				{
					"name" : "centerImg",
					"type" : "expanded_image",
					"x" : 149,
					"y" : 52,
					"image" : LOCALE_PATH+"private_centerImg.tga",
					"rect" : (0.0, 0.0, 24, 15),
				},
					
					## tab_menu_01
				{
					"name" : "ItemTypeImg",
					"type" : "image",
					"x" : 136,
					"y" : 39,
					"width" : 10,
					"image" : "d:/ymir work/ui/tab_menu_01.tga",
					"children" :
					(
							## Text
						{ "name" : "ResultNameText1", "type" : "text", "x" : 0, "y" : 0,  "text" : "Items Relacionados", "all_align":"center",},
					),
				},		
				{
					"name" : "next_button", 
					"type" : "button",

					"x" : 453-100, "y" : 313,


					"default_image" : LOCALE_PATH + "private_next_btn_01.sub",
					"over_image" : LOCALE_PATH + "private_next_btn_02.sub",
					"down_image" : LOCALE_PATH + "private_next_btn_01.sub",
				},
				{
					"name" : "last_next_button", "type" : "button",
					"x" : 483-100, "y" : 313,

					"default_image" : LOCALE_PATH + "private_last_next_btn_01.sub",
					"over_image" : LOCALE_PATH + "private_last_next_btn_02.sub",
					"down_image" : LOCALE_PATH + "private_last_next_btn_01.sub",
				},	
				{
					"name" : "prev_button", "type" : "button",
					"x" : 260-20-40, "y" : 313,

					"default_image" : LOCALE_PATH + "private_prev_btn_01.sub",
					"over_image" : LOCALE_PATH + "private_prev_btn_02.sub",
					"down_image" : LOCALE_PATH + "private_prev_btn_01.sub",
				},
				{
					"name" : "last_prev_button", "type" : "button",
					"x" : 230-20-40, "y" : 313,

					"default_image" : LOCALE_PATH + "private_first_prev_btn_01.sub",
					"over_image" : LOCALE_PATH + "private_first_prev_btn_02.sub",
					"down_image" : LOCALE_PATH + "private_first_prev_btn_01.sub",
				},
				{
					"name" : "AceptButton",
					"type" : "button",

					"x" : 430,
					"y" : 307,

					"text" : "Localizar",

					"default_image" : "d:/ymir work/ui/privatesearch/private_findbuttonImg01.sub",
					"over_image" : "d:/ymir work/ui/privatesearch/private_findbuttonImg02.sub",
					"down_image" : "d:/ymir work/ui/privatesearch/private_findbuttonImg03.sub",
				},
			),
		},
	),
}
