import uiScriptLocale
import item
import app
import localeInfo
import oxevent

LOCALE_PATH = "d:/ymir work/ui/shop_search/"
GOLD_COLOR = 0xFFFEE3AE

window = {
	"name" : "PrivateShopSearchDialog",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float",),
	"width" : 356,
	"height" : 174,
	"children" :
	(
		# board
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"x" : 0,
			"y" : 0,
			"width" : 356,
			"height" : 174,
			"title" : uiScriptLocale.PRIVATESHOPSEARCH_SEARCH_BAR,
			"children" :
			(
				# Center
				{
					"name" : "SearchImgCenter",
					"type" : "image",
					"x" : 12,
					"y" : 34,
					"image" : LOCALE_PATH+"bg.tga",
					"children" :
					(
						# ItemName
						{
							"name" : "ItemNameText",
							"type" : "text",
							"text_horizontal_align":"left",
							"x" : 71,
							"y" : 10,
							"text" : uiScriptLocale.PRIVATESHOPSEARCH_ITEMNAME,
							"color":GOLD_COLOR
						},
						# ItemNameEditLine
						{
							"name" : "ItemNameEditLine",
							"type" : "editline",
							"x" : 73,
							"y" : 38,
							"width" : 197,
							"height" : 17,
							"input_limit" : 25,
						},
						# ItemSlotSearch
						{
							"name" : "ItemSlotSearch",
							"type" : "slot",
							"x" : 16,
							"y" : 5,
							"width" : 32,
							"height" : 96,
							"slot" :
							(
								{
									"index": 1,
									"x":1,
									"y":1,
									"width":32 ,
									"height":96
								},
							),
						},
						# ClearButton
						{
							"name" : "ClearButton",
							"type" : "button",
							"x" : 67,
							"y" : 74,
							"text" : uiScriptLocale.PRIVATESHOPSEARCH_CLEAR,
							"default_image" : LOCALE_PATH + "close_shop_0.tga",
							"over_image" : LOCALE_PATH + "close_shop_1.tga",
							"down_image" : LOCALE_PATH + "close_shop_2.tga",
						},
						# FindButton
						{
							"name" : "SearchButton",
							"type" : "button",
							"x" : 195,
							"y" : 74,
							"text" : uiScriptLocale.PRIVATESHOPSEARCH_SEARCH,
							"default_image" : LOCALE_PATH + "open_shop_0.tga",
							"over_image" : LOCALE_PATH + "open_shop_1.tga",
							"down_image" : LOCALE_PATH + "open_shop_2.tga",
						},
					),
				},
				# Help
				{
					"name" : "DesckText",
					"type" : "text",
					"text_horizontal_align":"center",
					"x" : 178,
					"y" : 150,
					"text" : uiScriptLocale.PRIVATESHOPSEARCH_DESC_TEXT,
					"color":GOLD_COLOR
				},
				# ListBoxBarSearch
				{
					"name" : "ListBoxBarSearch",
					"type" : "slotbar",
					"x" : 70 + 8,
					"y" : 58 + 35,
					"width" : 251,
					"height" : 20,
					"children" :
					(
						{
							"name" : "ListBoxSearch",
							"type" : "listbox2",
							"x" : 0,
							"y" : 0,
							"row_count" : 4,
							"width" : 251,
							"height" : 20,
						},
					),
				},
			),
		},
	),
}