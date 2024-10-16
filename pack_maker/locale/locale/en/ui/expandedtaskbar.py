import uiScriptLocale
import localeInfo
import app

ROOT = "d:/ymir work/ui/game/"
NEW_DESIGN_FOLDER = "d:/ymir work/ui/game/new_inventory/"

Y_ADD_POSITION = 0
window = {
	"name" : "ExpandTaskBar",
	"style" : ("ltr", ),

	"x" : SCREEN_WIDTH/2 - 5,
	"y" : SCREEN_HEIGHT - 74,

	"width" : 37,
	"height" : 37,

	"children" :
	[
		{
			"name" : "ExpanedTaskBar_Board",
			"type" : "window",
			"style" : ("ltr", ),

			"x" : 0,
			"y" : 0,

			"width" : 37,
			"height" : 37,

			"children" :
			[
				{
					"name" : "DragonSoulButton",
					"type" : "button",
					"style" : ("ltr", ),

					"x" : 0,
					"y" : 0,

					"width" : 37,
					"height" : 37,

					"tooltip_text" : uiScriptLocale.TASKBAR_DRAGON_SOUL,

					"default_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_01.tga",
					"over_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_02.tga",
					"down_image" : "d:/ymir work/ui/dragonsoul/DragonSoul_Button_03.tga",
				},
			],
		},
	],
}

if app.ENABLE_IMPROVED_AUTOMATIC_HUNTING_SYSTEM:
	window["width"] = 37 * 2
	window["children"][0]["width"] = window["children"][0]["width"] + 37
	window["children"][0]["children"] = window["children"][0]["children"] + [
		{
			"name" : "AutoButton",
			"type" : "button",
			# "style" : ("ltr", ),

			"x" : 38,
			"y" : 0,

			"width" : 37,
			"height" : 37,

			"tooltip_text" : uiScriptLocale.KEYCHANGE_AUTO_WINDOW,

			"default_image" : "icon/item/TaskBar_Auto_Button_01.tga",
			"over_image" : "icon/item/TaskBar_Auto_Button_02.tga",
			"down_image" : "icon/item/TaskBar_Auto_Button_03.tga",
		},
	]

if app.ENABLE_SWITCHBOT:
	window["width"] = 37 * 3
	window["children"][0]["width"] = window["children"][0]["width"] + 37
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "SwitchbotButton",
						"type" : "button",

						"x" : 74,
						"y" : 0,

						"width" : 37,
						"height" : 37,

						"tooltip_text" : uiScriptLocale.SWITCHBOT_TITLE,

						"tooltip_text" : uiScriptLocale.SWITCHBOT_TITLE,
						"default_image" : NEW_DESIGN_FOLDER+"switch_0.tga",
						"over_image" : NEW_DESIGN_FOLDER+"switch_1.tga",
						"down_image" : NEW_DESIGN_FOLDER+"switch_2.tga",
					},]

# if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
	# window["width"] = 37*4
	# window["children"][0]["width"] = window["children"][0]["width"] + 37
	# window["children"][0]["children"] = window["children"][0]["children"] + [
					# {
						# "name" : "ShopSearchButton",
						# "type" : "button",
						# "style" : ("ltr", ),

						# "x" : 111,
						# "y" : 0,

						# "width" : 37,
						# "height" : 37,

						# "tooltip_text" : uiScriptLocale.SHOP_SEARCH_TITLE,
								
						# "default_image" : NEW_DESIGN_FOLDER+"search_0.tga",
						# "over_image" : NEW_DESIGN_FOLDER+"search_1.tga",
						# "down_image" : NEW_DESIGN_FOLDER+"search_2.tga",
					# },]

if app.ENABLE_WIKI:
	window["width"] = 37*5
	window["children"][0]["width"] = window["children"][0]["width"] + 37
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "WikiButton",
						"type" : "button",
						"style" : ("ltr", ),

						"x" : 148,
						"y" : 0,

						"width" : 37,
						"height" : 37,

						"tooltip_text" : localeInfo.WIKI_TITLE2,
								
						"default_image" : NEW_DESIGN_FOLDER+"wiki_0.tga",
						"over_image" : NEW_DESIGN_FOLDER+"wiki_1.tga",
						"down_image" : NEW_DESIGN_FOLDER+"wiki_2.tga",
					},]

if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
	window["width"] = 37*6
	window["children"][0]["width"] = window["children"][0]["width"] + 37
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name" : "BuffNPCButton",
						"type" : "button",
						"style" : ("ltr", ),

						"x" : 185,
						"y" : 0,

						"width" : 37,
						"height" : 37,

						"tooltip_text" : uiScriptLocale.KEYCHANGE_BUFF_NPC,
								
						"default_image" : "icon/item/buff_0.tga",
						"over_image" : "icon/item/buff_1.tga",
						"down_image" : "icon/item/buff_2.tga",
					},]

# if app.ENABLE_DRAGON_GATE:
	# window["width"] = 37 * 6
	# window["children"][0]["width"] = window["children"][0]["width"] + 37
	# window["children"][0]["children"] = window["children"][0]["children"] + [
	# {
		# "name" : "DragonGateButton",
		# "type" : "button",
		# "style" : ("ltr", ),

		# "x" : 182,
		# "y" : 0,

		# "width" : 37,
		# "height" : 37,

		# "tooltip_text" : uiScriptLocale.KEYCHANGE_DRAGON_GATE,
				
		# "default_image" : "icon/item/dragondoor_01.tga",
		# "over_image" : "icon/item/dragondoor_02.tga",
		# "down_image" : "icon/item/dragondoor_03.tga",
	# },]

# if app.ENABLE_MERCENARY_SYSTEM:
	# window["width"] = 37 * 7
	# window["children"][0]["width"] = window["children"][0]["width"] + 37
	# window["children"][0]["children"] = window["children"][0]["children"] + [
	# {
		# "name" : "MercenaryButton",
		# "type" : "button",
		# "style" : ("ltr", ),

		# "x" : 218,
		# "y" : 0,

		# "width" : 37,
		# "height" : 37,

		# "tooltip_text" : uiScriptLocale.KEYCHANGE_MERCENARY,
				
		# "default_image" : "icon/item/mercenary_01.tga",
		# "over_image" : "icon/item/mercenary_02.tga",
		# "down_image" : "icon/item/mercenary_03.tga",
	# },]

# if app.ENABLE_SUNGMAHEE_GATE:
	# window["width"] = 37 * 8
	# window["children"][0]["width"] = window["children"][0]["width"] + 37
	# window["children"][0]["children"] = window["children"][0]["children"] + [
	# {
		# "name" : "SungmaheeGateAchievButton",
		# "type" : "button",
		# "style" : ("ltr", ),

		# "x" : 254,
		# "y" : 0,

		# "width" : 37,
		# "height" : 37,

		# "tooltip_text" : uiScriptLocale.KEYCHANGE_SUNGMAHEE_GATE_ACHIEV,
				
		# "default_image" : "icon/item/smhgate_01.tga",
		# "over_image" : "icon/item/smhgate_02.tga",
		# "down_image" : "icon/item/smhgate_03.tga",
	# },]