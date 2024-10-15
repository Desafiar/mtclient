import uiScriptLocale
import item
import app
import localeInfo

LOCALE_PATH = "d:/ymir work/ui/privatesearch/"
GOLD_COLOR = 0xFFFEE3AE

window = {
	"name" : "PrivateShopSearchDialog",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float",),
	"width" : 590,
	"height" : 370,
	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"x" : 0,
			"y" : 0,
			"width" : 590,
			"height" : 370,
			"title" : uiScriptLocale.PRIVATESHOPSEARCH_SEARCH_BAR,
			"children" :
			(
				## ItemName
				{
					"name" : "ItemNameImg",
					"type" : "image",
					"x" : 10,
					"y" : 275,
					"image" : LOCALE_PATH+"private_leftNameImg.sub",
					"children" :
					(
						{ "name" : "ItemNameText", "type" : "text", "text_horizontal_align":"center", "x" : 60, "y" : 5, "text" : uiScriptLocale.PRIVATESHOPSEARCH_ITEMNAME, "color":GOLD_COLOR },
					),
				},
				## ItemNameEditLine
				{
					"name" : "ItemNameSlot",
					"type" : "image",
					"x" : 12,
					"y" : 295,
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
				## FindButton
				{
					"name" : "SearchButton",
					"type" : "button",
					"x" : 10,
					"y" : 328,
					"text" : uiScriptLocale.PRIVATESHOPSEARCH_SEARCH,
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
						{ "name" : "ResultNameText1", "type" : "text", "x" : 67, "y" : 4,  "text" : uiScriptLocale.PRIVATESHOPSEARCH_ITEMNAME, },
						{ "name" : "ResultNameText2", "type" : "text", "x" : 207, "y" : 4, "text" : uiScriptLocale.PRIVATESHOPSEARCH_SELLER, },
						{ "name" : "ResultNameText3", "type" : "text", "x" : 303, "y" : 4, "text" : uiScriptLocale.PRIVATESHOPSEARCH_COUNT, },
						{ "name" : "ResultNameText4", "type" : "text", "x" : 377, "y" : 4, "text" : uiScriptLocale.PRIVATESHOPSEARCH_PRICE, },
					),
				},
				{
					"name" : "first_prev_button", "type" : "button",
					"x" : 230-20, "y" : 315,
					"default_image" : LOCALE_PATH + "private_first_prev_btn_01.sub",
					"over_image" 	: LOCALE_PATH + "private_first_prev_btn_02.sub",
					"down_image" 	: LOCALE_PATH + "private_first_prev_btn_01.sub",
				},
				{
					"name" : "prev_button", "type" : "button",
					"x" : 260-20, "y" : 315,
					"default_image" : LOCALE_PATH + "private_prev_btn_01.sub",
					"over_image" 	: LOCALE_PATH + "private_prev_btn_02.sub",
					"down_image" 	: LOCALE_PATH + "private_prev_btn_01.sub",
				},
				{
					"name" : "page1_button", "type" : "button",
					"x" : 275-10, "y" : 313,
					"text" : "1",
					"default_image" : LOCALE_PATH + "private_pagenumber_00.sub",
					"over_image" 	: LOCALE_PATH + "private_pagenumber_01.sub",
					"down_image" 	: LOCALE_PATH + "private_pagenumber_02.sub",
				},
				{
					"name" : "page2_button", "type" : "button",
					"x" : 310-10, "y" : 313,
					"text" : "2",
					"default_image" : LOCALE_PATH + "private_pagenumber_00.sub",
					"over_image" 	: LOCALE_PATH + "private_pagenumber_01.sub",
					"down_image" 	: LOCALE_PATH + "private_pagenumber_02.sub",
				},
				{
					"name" : "page3_button", "type" : "button",
					"x" : 345-10, "y" : 313,
					
					"text" : "3",
					"default_image" : LOCALE_PATH + "private_pagenumber_00.sub",
					"over_image" 	: LOCALE_PATH + "private_pagenumber_01.sub",
					"down_image" 	: LOCALE_PATH + "private_pagenumber_02.sub",
				},
				{
					"name" : "page4_button", "type" : "button",
					"x" : 380-10, "y" : 313,
					"text" : "4",
					"default_image" : LOCALE_PATH + "private_pagenumber_00.sub",
					"over_image" 	: LOCALE_PATH + "private_pagenumber_01.sub",
					"down_image" 	: LOCALE_PATH + "private_pagenumber_02.sub",
				},
				{
					"name" : "page5_button", "type" : "button",
					"x" : 415-10, "y" : 313,
					"text" : "5",
					"default_image" : LOCALE_PATH + "private_pagenumber_00.sub",
					"over_image" 	: LOCALE_PATH + "private_pagenumber_01.sub",
					"down_image" 	: LOCALE_PATH + "private_pagenumber_02.sub",
				},
				{
					"name" : "next_button", "type" : "button",
					"x" : 453, "y" : 315,
					"default_image" : LOCALE_PATH + "private_next_btn_01.sub",
					"over_image" 	: LOCALE_PATH + "private_next_btn_02.sub",
					"down_image" 	: LOCALE_PATH + "private_next_btn_01.sub",
				},
				{
					"name" : "last_next_button", "type" : "button",
					"x" : 483, "y" : 315,
					"default_image" : LOCALE_PATH + "private_last_next_btn_01.sub",
					"over_image" 	: LOCALE_PATH + "private_last_next_btn_02.sub",
					"down_image" 	: LOCALE_PATH + "private_last_next_btn_01.sub",
				},
			),
		},
	),
}