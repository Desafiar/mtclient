import app
import uiScriptLocale

LOCALE_PATH = uiScriptLocale.LOGIN_PATH
MAIN_LOCALE_PATH = "locale/en/ui/"

SERVER_BOARD_HEIGHT = 220 + 180
SERVER_LIST_HEIGHT = 171 + 180
SERVER_BOARD_WEIGHT = 375

ID_LIMIT_COUNT = 19
PW_LIMIT_COUNT = 16

## Size of login.sub
BACKGROUND_IMAGE_WIDTH = 1920.0
BACKGROUND_IMAGE_HEIGHT = 1080.0

## Language flag size.
FLAG_SIZE = 45
ROOT = "d:/ymir work/ui/game/"

window = {
	"name" : "LoginWindow",
	"sytle" : ("movable",),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	[


		## Board Window - Old
		# {
			# "name" : "bg1", "type" : "expanded_image", "x" : 0, "y" : 0,
			# "x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			# "image" : MAIN_LOCALE_PATH + "serverlist.sub",
		# },
		# {
			# "name" : "bg2", "type" : "expanded_image", "x" : 0, "y" : 0,
			# "x_scale" : float(SCREEN_WIDTH) / 1024.0, "y_scale" : float(SCREEN_HEIGHT) / 768.0,
			# "image" : MAIN_LOCALE_PATH + "login.sub",
		# },

		## Board Window - New

		{
		"name" : "background", "type" : "expanded_image", "x" : 0, "y" : 0,
		"x_scale" : float(SCREEN_WIDTH) / BACKGROUND_IMAGE_WIDTH, "y_scale" : float(SCREEN_HEIGHT) / BACKGROUND_IMAGE_HEIGHT,
		"image" : MAIN_LOCALE_PATH + "login.sub", ## Size replacement is needed here.
		},

		## ConnectBoard
		{
			"name" : "ConnectBoard",
			"type" : "thinboard",

			"x" : (SCREEN_WIDTH - 208) / 2,
			"y" : (SCREEN_HEIGHT - 410 - 40),
			"width" : 208,
			"height" : 30,

			"children" :
			(
				{
					"name" : "ConnectName",
					"type" : "text",

					"x" : 15,
					"y" : 0,
					"vertical_align" : "center",
					"text_vertical_align" : "center",

					"text" : uiScriptLocale.LOGIN_DEFAULT_SERVERADDR,
				},
				{
					"name" : "SelectConnectButton",
					"type" : "button",

					"x" : 150,
					"y" : 0,
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/small_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/small_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/small_button_03.sub",

					"text" : uiScriptLocale.LOGIN_SELECT_BUTTON,
				},
			),
		},

		## LoginBoard
		{
			"name" : "LoginBoard",
			"type" : "image",

			"x" : (SCREEN_WIDTH - 208) / 2,
			"y" : (SCREEN_HEIGHT - 415),

			"image" : LOCALE_PATH + "loginwindow.sub",

			"children" :
			(
				{ 
					"name" : "ID_Text_window", "type" : "window", "x" : 45, "y" : 4, "width" : 120, "height" : 18,
					"children" :
					(
						{"name":"ID_Text", "type":"text", "x":0, "y":0, "text":uiScriptLocale.LOGIN_ID, "all_align" : "center"},
					),
				},
				
				{ 
					"name" : "Password_Text_window", "type" : "window", "x" : 45, "y" : 41, "width" : 120, "height" : 18,
					"children" :
					(
						{"name":"Password_Text", "type":"text", "x":0, "y":0, "text":uiScriptLocale.LOGIN_PASSWORD, "all_align" : "center"},
					),
				},
				
				{
					"name" : "ID_EditLine",
					"type" : "editline",

					"x" : 48,
					"y" : 23,

					"width" : 120,
					"height" : 18,

					"input_limit" : ID_LIMIT_COUNT,
					"enable_codepage" : 0,

					"r" : 1.0,
					"g" : 1.0,
					"b" : 1.0,
					"a" : 1.0,
				},
				{
					"name" : "Password_EditLine",
					"type" : "editline",

					"x" : 48,
					"y" : 60,

					"width" : 120,
					"height" : 18,

					"input_limit" : PW_LIMIT_COUNT,
					"secret_flag" : 1,
					"enable_codepage" : 0,

					"r" : 1.0,
					"g" : 1.0,
					"b" : 1.0,
					"a" : 1.0,
				},
				{
					"name" : "LoginButton",
					"type" : "button",

					"x" : 15,
					"y" : 79,

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.LOGIN_CONNECT,
				},
				{
					"name" : "LoginExitButton",
					"type" : "button",

					"x" : 105,
					"y" : 79,

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.LOGIN_EXIT,
				},
			),
		},

		# Language
		{
			"name" : "LanguageBoard",
			"type" : "window",
			"x" : (SCREEN_WIDTH - 390) / 2,
			"y" : (SCREEN_HEIGHT - 520),
			"width" : 360,
			"height" : 60,

			"text_horizontal_align" : "center",

			"children" :
			(
				## Board
				{
					"name" : "FlagBoard",
					"type" : "thinboard",
					"x" : 8,
					"y" : -20,
					"width" : 375,
					"height" : 62,
				},

				## English
				{
					"name" : "ChangeLanguageEn",
					"type" : "radio_button",

					"x": 20,
					"y": -12,
					"tooltip_text": uiScriptLocale.LANGUAGE_EN,

					"default_image": ROOT + "language/flag_en_norm.tga",
					"over_image": ROOT + "language/flag_en_over.tga",
					"down_image": ROOT + "language/flag_en_down.tga",
				},
				## Arab
				{
					"name" : "ChangeLanguageAe",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE,
					"y": -12,
					"tooltip_text": uiScriptLocale.LANGUAGE_AE,

					"default_image": ROOT + "language/flag_ae_norm.tga",
					"over_image": ROOT + "language/flag_ae_over.tga",
					"down_image": ROOT + "language/flag_ae_down.tga",
				},

				## Czech
				{
					"name" : "ChangeLanguageCz",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*2,
					"y": -12,
					"tooltip_text": uiScriptLocale.LANGUAGE_CZ,

					"default_image": ROOT + "language/flag_cz_norm.tga",
					"over_image": ROOT + "language/flag_cz_over.tga",
					"down_image": ROOT + "language/flag_cz_down.tga",
				},
				## Denmark
				{
					"name" : "ChangeLanguageDk",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*3,
					"y": -12,
					"tooltip_text": uiScriptLocale.LANGUAGE_DK,

					"default_image": ROOT + "language/flag_dk_norm.tga",
					"over_image": ROOT + "language/flag_dk_over.tga",
					"down_image": ROOT + "language/flag_dk_down.tga",
				},
				## France
				{
					"name" : "ChangeLanguageFr",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*4,
					"y": -12,
					"tooltip_text": uiScriptLocale.LANGUAGE_FR,

					"default_image": ROOT + "language/flag_fr_norm.tga",
					"over_image": ROOT + "language/flag_fr_over.tga",
					"down_image": ROOT + "language/flag_fr_down.tga",
				},
				## Greek
				{
					"name" : "ChangeLanguageGr",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*5,
					"y": -12,
					"tooltip_text": uiScriptLocale.LANGUAGE_GR,

					"default_image": ROOT + "language/flag_gr_norm.tga",
					"over_image": ROOT + "language/flag_gr_over.tga",
					"down_image": ROOT + "language/flag_gr_down.tga",
				},
				## Netherland
				{
					"name" : "ChangeLanguageNl",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*6,
					"y": -12,
					"tooltip_text": uiScriptLocale.LANGUAGE_NL,

					"default_image": ROOT + "language/flag_nl_norm.tga",
					"over_image": ROOT + "language/flag_nl_over.tga",
					"down_image": ROOT + "language/flag_nl_down.tga",
				},
				## Polish
				{
					"name" : "ChangeLanguagePl",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*7,
					"y": -12,
					"tooltip_text": uiScriptLocale.LANGUAGE_PL,

					"default_image": ROOT + "language/flag_pl_norm.tga",
					"over_image": ROOT + "language/flag_pl_over.tga",
					"down_image": ROOT + "language/flag_pl_down.tga",
				},
				## Hungarian
				{
					"name" : "ChangeLanguageHu",
					"type" : "radio_button",

					"x": 20,
					"y": 15,
					"tooltip_text": uiScriptLocale.LANGUAGE_HU,

					"default_image": ROOT + "language/flag_hu_norm.tga",
					"over_image": ROOT + "language/flag_hu_over.tga",
					"down_image": ROOT + "language/flag_hu_down.tga",
				},

				## German
				{
					"name" : "ChangeLanguageDe",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE,
					"y": 15,
					"tooltip_text": uiScriptLocale.LANGUAGE_DE,

					"default_image": ROOT + "language/flag_de_norm.tga",
					"over_image": ROOT + "language/flag_de_over.tga",
					"down_image": ROOT + "language/flag_de_down.tga",
				},
				## Italian
				{
					"name" : "ChangeLanguageIt",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*2,
					"y": 15,
					"tooltip_text": uiScriptLocale.LANGUAGE_IT,

					"default_image": ROOT + "language/flag_it_norm.tga",
					"over_image": ROOT + "language/flag_it_over.tga",
					"down_image": ROOT + "language/flag_it_down.tga",
				},
				## Russia
				{
					"name" : "ChangeLanguageRu",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*3,
					"y": 15,
					"tooltip_text": uiScriptLocale.LANGUAGE_RU,

					"default_image": ROOT + "language/flag_ru_norm.tga",
					"over_image": ROOT + "language/flag_ru_over.tga",
					"down_image": ROOT + "language/flag_ru_down.tga",
				},
				## Portoguese
				{
					"name" : "ChangeLanguagePt",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*4,
					"y": 15,
					"tooltip_text": uiScriptLocale.LANGUAGE_PT,

					"default_image": ROOT + "language/flag_pt_norm.tga",
					"over_image": ROOT + "language/flag_pt_over.tga",
					"down_image": ROOT + "language/flag_pt_down.tga",
				},
				## Rumania
				{
					"name" : "ChangeLanguageRo",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*5,
					"y": 15,
					"tooltip_text": uiScriptLocale.LANGUAGE_RO,

					"default_image": ROOT + "language/flag_ro_norm.tga",
					"over_image": ROOT + "language/flag_ro_over.tga",
					"down_image": ROOT + "language/flag_ro_down.tga",
				},
				## Español
				{
					"name" : "ChangeLanguageEs",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*6,
					"y": 15,
					"tooltip_text": uiScriptLocale.LANGUAGE_ES,

					"default_image": ROOT + "language/flag_es_norm.tga",
					"over_image": ROOT + "language/flag_es_over.tga",
					"down_image": ROOT + "language/flag_es_down.tga",
				},
				## Turk
				{
					"name" : "ChangeLanguageTr",
					"type" : "radio_button",

					"x": 20 + FLAG_SIZE*7,
					"y": 15,
					"tooltip_text": uiScriptLocale.LANGUAGE_TR,

					"default_image": ROOT + "language/flag_tr_norm.tga",
					"over_image": ROOT + "language/flag_tr_over.tga",
					"down_image": ROOT + "language/flag_tr_down.tga",
				},
			),
		},

		## Autosave account
		{
			"name" : "SaveBoard",
			"type" : "thinboard",

			'x' : (SCREEN_WIDTH - 352) / 2,
			'y' : SCREEN_HEIGHT - 303,
			'width' : 352,
			'height' : 170,
			"children" :
			(
				# {"name" : "SaveTitle_Thin","type" : "thinboard","x" : 0,"y" : 0,'width' : 352,'height' : 0,},
				{
					"name" : "SaveTitle",
					"type" : "text",

					"x" : (352/2),
					"y" : 7,
					"text_horizontal_align" : "center",

					"text" : uiScriptLocale.LOGIN_AUTOSAVE_TITLE,
				},
				{"name" : "SaveSlot_1_Thin","type" : "thinboard","x" : 0,"y" : 30,'width' : 176,'height' : 50,},
				{"name" : "NameSave_1","type" : "text","x" : 88,"y" : 42,"text_vertical_align" : "center", "text_horizontal_align" : "center", "text" : uiScriptLocale.LOGIN_AUTOSAVE_NONE,},
				{"name" : "LoginButton_1","type" : "button","x" : 23,"y" : 55,"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub","over_image" : "d:/ymir work/ui/public/acceptbutton01.sub","down_image" : "d:/ymir work/ui/public/acceptbutton02.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_LOGIN,},
				{"name" : "SaveButton_1","type" : "button","x" : 23 + 34,"y" : 55,"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub","over_image" : "d:/ymir work/ui/public/acceptbutton01.sub","down_image" : "d:/ymir work/ui/public/acceptbutton02.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_SAVE,},
				{"name" : "DeleteButton_1","type" : "button","x" : 23+70,"y" : 55,"default_image" : "d:/ymir work/ui/public/canclebutton00.sub","over_image" : "d:/ymir work/ui/public/canclebutton01.sub","down_image" : "d:/ymir work/ui/public/canclebutton02.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_DELETE,},

				{"name" : "SaveSlot_2_Thin","type" : "thinboard","x" : 176, "y" : 30,'width' : 176,'height' : 50,},
				{"name" : "NameSave_2","type" : "text","x" : 88 + 175,"y" : 42,"text_vertical_align" : "center", "text_horizontal_align" : "center", "text" : uiScriptLocale.LOGIN_AUTOSAVE_NONE,},
				{"name" : "LoginButton_2","type" : "button","x" : 23 + 175,"y" : 55,"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub","over_image" : "d:/ymir work/ui/public/acceptbutton01.sub","down_image" : "d:/ymir work/ui/public/acceptbutton02.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_LOGIN,},
				{"name" : "SaveButton_2","type" : "button","x" : 23 + 175 + 34,"y" : 55,"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub","over_image" : "d:/ymir work/ui/public/acceptbutton01.sub","down_image" : "d:/ymir work/ui/public/acceptbutton02.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_SAVE,},
				{"name" : "DeleteButton_2","type" : "button","x" : 23 +70 + 175,"y" : 55,"default_image" : "d:/ymir work/ui/public/canclebutton00.sub","over_image" : "d:/ymir work/ui/public/canclebutton00.sub","down_image" : "d:/ymir work/ui/public/canclebutton00.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_DELETE,},

				{"name" : "SaveSlot_3_Thin","type" : "thinboard","x" : 0,"y" : 30 + 30 + 20,'width' : 176,'height' : 50,},
				{"name" : "NameSave_3","type" : "text","x" : 88,"y" : 42 + 30 + 20,"text_vertical_align" : "center", "text_horizontal_align" : "center" ,"text" : uiScriptLocale.LOGIN_AUTOSAVE_NONE,},
				{"name" : "LoginButton_3","type" : "button","x" : 23,"y" : 55 + 30 + 20,"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub","over_image" : "d:/ymir work/ui/public/acceptbutton01.sub","down_image" : "d:/ymir work/ui/public/acceptbutton02.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_LOGIN,},
				{"name" : "SaveButton_3","type" : "button","x" : 23 + 34,"y" : 55 + 30 + 20,"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub","over_image" : "d:/ymir work/ui/public/acceptbutton01.sub","down_image" : "d:/ymir work/ui/public/acceptbutton02.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_SAVE,},
				{"name" : "DeleteButton_3","type" : "button","x" : 23+70,"y" : 55 + 30 + 20,"default_image" : "d:/ymir work/ui/public/canclebutton00.sub","over_image" : "d:/ymir work/ui/public/canclebutton00.sub","down_image" : "d:/ymir work/ui/public/canclebutton00.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_DELETE,},

				{"name" : "SaveSlot_4_Thin","type" : "thinboard","x" : 176, "y" : 30 + 30 + 20,'width' : 176,'height' : 50,},
				{"name" : "NameSave_4","type" : "text","x" : 88 + 175,"y" : 42 + 30 + 20,"text_vertical_align" : "center", "text_horizontal_align" : "center","text" : uiScriptLocale.LOGIN_AUTOSAVE_NONE,},
				{"name" : "LoginButton_4","type" : "button","x" : 23 + 175, "y" : 55 + 30 + 20, "default_image" : "d:/ymir work/ui/public/acceptbutton00.sub","over_image" : "d:/ymir work/ui/public/acceptbutton01.sub","down_image" : "d:/ymir work/ui/public/acceptbutton02.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_LOGIN,},
				{"name" : "SaveButton_4","type" : "button","x" : 23 + 175 + 34, "y" : 55 + 30 + 20, "default_image" : "d:/ymir work/ui/public/acceptbutton00.sub","over_image" : "d:/ymir work/ui/public/acceptbutton01.sub","down_image" : "d:/ymir work/ui/public/acceptbutton02.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_SAVE,},
				{"name" : "DeleteButton_4","type" : "button","x" : 23 +70 + 175, "y" : 55 + 30 + 20,"default_image" : "d:/ymir work/ui/public/canclebutton00.sub","over_image" : "d:/ymir work/ui/public/canclebutton01.sub","down_image" : "d:/ymir work/ui/public/canclebutton02.sub","tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_DELETE,},

				{"name" : "SaveAccAdviceIcon", "type" : "button", "x" : 10, "y" : 0 + 01 + 15 + 30 + 20 + 30 + 20 + 28, "default_image": "d:/ymir work/ui/pattern/q_mark_01.tga", "over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga", "down_image" : "d:/ymir work/ui/pattern/q_mark_02.tga", "tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_HELP,},
				{"name" : "SaveAccAdvice","type" : "text", "x" : (352/2), "y" : 0 + 01 + 15 + 30 + 20 + 30 + 20 + 35,"text_vertical_align" : "center", "text_horizontal_align" : "center", "text" : uiScriptLocale.LOGIN_AUTOSAVE_ADVICE,},
				{"name" : "SaveAccAdviceIcon2", "type" : "button", "x" : 352 - 27, "y" : 0 + 01 + 15 + 30 + 20 + 30 + 20 + 28, "default_image": "d:/ymir work/ui/pattern/q_mark_01.tga", "over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga", "down_image" : "d:/ymir work/ui/pattern/q_mark_02.tga", "tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_HELP,},					{"name" : "SaveAccAdviceIcon2", "type" : "button", "x" : 352 - 27, "y" : 0 + 01 + 15 + 30 + 20 + 30 + 20 + 28, "default_image": "d:/ymir work/ui/pattern/q_mark_01.tga", "over_image" : "d:/ymir work/ui/pattern/q_mark_02.tga", "down_image" : "d:/ymir work/ui/pattern/q_mark_02.tga", "tooltip_text" : uiScriptLocale.LOGIN_AUTOSAVE_HELP,},
			),
		},
		{
			"name" : "ServerBoard",
			"type" : "thinboard",

			"x" : 0,
			"y" : SCREEN_HEIGHT - SERVER_BOARD_HEIGHT - 72,
			"width" : 405,
			"height" : SERVER_BOARD_HEIGHT,
			"horizontal_align" : "center",

			"children" :
			[
				## Title
				{
					"name" : "Title",
					"type" : "text",

					"x" : 0,
					"y" : 12,
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text" : uiScriptLocale.LOGIN_SELECT_TITLE,
				},

				## Horizontal
				{
					"name" : "HorizontalLine1",
					"type" : "line",

					"x" : 10,
					"y" : 34,
					"width" : 385,
					"height" : 0,
					"color" : 0xff777777,
				},
				{
					"name" : "HorizontalLine2",
					"type" : "line",

					"x" : 10,
					"y" : 35,
					"width" : 355,
					"height" : 0,
					"color" : 0xff111111,
				},

				## Vertical
				{
					"name" : "VerticalLine1",
					"type" : "line",

					"x" : 246,
					"y" : 38,
					"width" : 0,
					"height" : SERVER_LIST_HEIGHT + 4,
					"color" : 0xff777777,
				},
				{
					"name" : "VerticalLine2",
					"type" : "line",

					"x" : 247,
					"y" : 38,
					"width" : 0,
					"height" : SERVER_LIST_HEIGHT + 4,
					"color" : 0xff111111,
				},

				## Buttons
				{
					"name" : "ServerSelectButton",
					"type" : "button",

					"x" : 267,
					"y" : SERVER_LIST_HEIGHT,

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.OK,
				},
				{
					"name" : "ServerExitButton",
					"type" : "button",

					"x" : 267,
					"y" : SERVER_LIST_HEIGHT + 22,

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.LOGIN_SELECT_EXIT,
				},

			],

		},

	],
}

if not app.ENABLE_SERVER_SELECT_RENEWAL:
	window["children"][5]["children"] = window["children"][5]["children"] + [
				## ListBox
				{
					"name" : "ServerList",
					"type" : "listbox2",

					"x" : 10,
					"y" : 40,
					"width" : 232,
					"height" : SERVER_LIST_HEIGHT,
					"row_count" : 15,
					"item_align" : 0,
				},
				{
					"name" : "ChannelList",
					"type" : "listbox",
					"x" : 255,
					"y" : 40,
					"width" : 109,
					"height" : SERVER_LIST_HEIGHT-40,

					"item_align" : 0,
				},]
