
import uiScriptLocale
import localeInfo

BASE_PATH = "nano_interface/images/login/"
BASE_PATH2 = "nano_interface/"
BTN_PATH = BASE_PATH + "btn/"
CHANNEL_PATH = BTN_PATH + "ch/"
ROOT = "nano_interface/animations/cicle/"

height = 0
if SCREEN_HEIGHT <= 1000:
	height = -120

window = {
	"name" : "LoginWindow",
	"x" : 0, "y" : 0, "width" : SCREEN_WIDTH, "height" : SCREEN_HEIGHT,
	"style" : ("float",),
	"children" :
	(
		{
			"name" : "background", "type" : "image",
			"x" : SCREEN_WIDTH / 2 - 1920 / 2, "y" : 0 + height,
			"image" : BASE_PATH + "background.png",
			"children" :
			(
				# ID
				{
					"name": "placeHolderId", "type": "special_editline",
					"x": (SCREEN_WIDTH / 2 - 166 / 2) - 5,
					"y": (SCREEN_HEIGHT / 2 - 20 - 10),
					"width": 166, "height": 30,
					"input_limit": 24,
				},
				# PWD
				{
					"name": "placeHolderPw", "type": "special_editline",
					"x": (SCREEN_WIDTH / 2 - 166 / 2) - 5,
					"y": (SCREEN_HEIGHT / 2) + 5,
					"width": 166, "height": 30,
					"secret_flag": 1,
					"input_limit": 24,
				},				
				{
					"name": "loginInfor",
					"type": "text",
					"x": SCREEN_WIDTH / 2 - (len("TextTextTextTextTextText") * 6) / 2,
					"y": 650,
					"text": "TextTextTextTextTextText",
				},
				{
					"name" : "saveBtn",
					"type" : "toggle_button",

					"x": (SCREEN_WIDTH / 2 - 166 / 2) - 5,
					"y": 547,

					"default_image": BASE_PATH2+"buttons/remember_me_normal.png",
					"over_image": BASE_PATH2+"buttons/remember_me_active.png",
					"down_image": BASE_PATH2+"buttons/remember_me_active.png",
				},
				{
					"name" : "saveInf",
					"type" : "text",

					"x": (SCREEN_WIDTH / 2 - 166 / 2)+10,
					"y": 545,

					"fontname" : "Tahoma Bold:13",
					"outline" : 1,
					
					
					"color" : 0xff969184,
					"text" : localeInfo.SAVE_ME,
				},
				# LOGINBTN
				{
					"name" : "loginBtn",
					"type" : "button",
					"x": (SCREEN_WIDTH / 2 - 166 / 2) - 10,
					"y" : 569,
					"default_image": BASE_PATH2 + "buttons/btn_normal.png",
					"over_image": BASE_PATH2 + "buttons/btn_active.png",
					"down_image": BASE_PATH2 + "buttons/btn_hover.png",
					"disable_image": BASE_PATH2 + "buttons/btn_disabled.png",
					"children" :
					(
						{
							"name": "fontButton",
							"type": "text",

							"x": -35,
							"y": 7,
					
							"fontname" : "Tahoma Bold:16.5",
							"horizontal_align": "center",
							"text" : localeInfo.SIGN_IN,
							"color" : 0xffa3c7c1,

						},
					),
				},				
				{
					"name": "link_user",
					"type": "nano_text_link_login",

					"x": (SCREEN_WIDTH / 2 - 166 / 2) - 10,
					"y": 602,
					
					"text" : localeInfo.FORGOT_PASSWORD,

				},
				{
					"name": "link_acc",
					"type": "nano_text_link_login",

					"x": (SCREEN_WIDTH / 2 - 166 / 2) - 10,
					"y": 615,
					
					"text" : localeInfo.CREATE_ACCOUNT,

				},
				# CHANNEL
				{
					"name" : "channel_1", "type" : "radio_button",
					"x" : 669, "y" : 442,

					"default_image": BASE_PATH2+"server_buttons/btn_ch_normal.png",
					"over_image": BASE_PATH2+"server_buttons/btn_ch_active.png",
					"down_image": BASE_PATH2+"server_buttons/btn_ch_hover.png",
					"children" :
					(
						{
							"name": "chText_1",
							"type": "text",

							"x": 7,
							"y": 9,

							"text" : localeInfo.ACCOUNT_1,

						},
					),
				},
				{
					"name" : "channel_2", "type" : "radio_button",
					"x" : 669, "y" : 477,

					"default_image": BASE_PATH2+"server_buttons/btn_ch_normal.png",
					"over_image": BASE_PATH2+"server_buttons/btn_ch_active.png",
					"down_image": BASE_PATH2+"server_buttons/btn_ch_hover.png",
					"children" :
					(
						{
							"name": "chText_2",
							"type": "text",

							"x": 7,
							"y": 9,

							"text" : localeInfo.ACCOUNT_2,

						},
					),
				},
				{
					"name" : "channel_3", "type" : "radio_button",
					"x" : 669, "y" : 512,

					"default_image": BASE_PATH2+"server_buttons/btn_ch_normal.png",
					"over_image": BASE_PATH2+"server_buttons/btn_ch_active.png",
					"down_image": BASE_PATH2+"server_buttons/btn_ch_hover.png",
					"children" :
					(
						{
							"name": "chText_3",
							"type": "text",

							"x": 7,
							"y": 9,

							"text" : localeInfo.ACCOUNT_3,

						},
					),
				},
				{
					"name" : "channel_4", "type" : "radio_button",
					"x" : 669, "y" : 547,

					"default_image": BASE_PATH2+"server_buttons/btn_ch_normal.png",
					"over_image": BASE_PATH2+"server_buttons/btn_ch_active.png",
					"down_image": BASE_PATH2+"server_buttons/btn_ch_hover.png",
					"children" :
					(
						{
							"name": "chText_4",
							"type": "text",

							"x": 7,
							"y": 9,

							"text" : localeInfo.ACCOUNT_4,

						},
					),
				},
				# ACCOUNTDELETE
				{
					"name" : "account_1_delete", "type" : "button",
					"default_image" : BTN_PATH + "btn_delete_normal.png",
					"x" : 1274, "y" : 456+32*0,
					"over_image" : BTN_PATH + "btn_delete_hover.png",
					"down_image" : BTN_PATH + "btn_delete_active.png",
				},
				{
					"name" : "account_2_delete", "type" : "button",
					"x" : 1274, "y" : 456+32*1,
					"default_image" : BTN_PATH + "btn_delete_normal.png",
					"over_image" : BTN_PATH + "btn_delete_hover.png",
					"down_image" : BTN_PATH + "btn_delete_active.png",
				},
				{
					"name" : "account_3_delete", "type" : "button",
					"x" : 1274, "y" : 456+32*2,
					"default_image" : BTN_PATH + "btn_delete_normal.png",
					"over_image" : BTN_PATH + "btn_delete_hover.png",
					"down_image" : BTN_PATH + "btn_delete_active.png",
				},
				{
					"name" : "account_4_delete", "type" : "button",
					"x" : 1274, "y" : 456+32*3,
					"default_image" : BTN_PATH + "btn_delete_normal.png",
					"over_image" : BTN_PATH + "btn_delete_hover.png",
					"down_image" : BTN_PATH + "btn_delete_active.png",
				},
				{
					"name" : "account_5_delete", "type" : "button",
					"x" : 1274, "y" : 456+32*4,
					"default_image" : BTN_PATH + "btn_delete_normal.png",
					"over_image" : BTN_PATH + "btn_delete_hover.png",
					"down_image" : BTN_PATH + "btn_delete_active.png",
				},
				{
					"name" : "account_6_delete", "type" : "button",
					"x" : 1274, "y" : 456+32*5,
					"default_image" : BTN_PATH + "btn_delete_normal.png",
					"over_image" : BTN_PATH + "btn_delete_hover.png",
					"down_image" : BTN_PATH + "btn_delete_active.png",
				},
				# ACCOUNTSELECT
				{
					"name" : "account_1_txt", "type" : "text",
					"x" : 1150, "y" : 454+32*0,
					"text" : "#01 - " + "Freier Slot",
				},
				{
					"name" : "account_1", "type" : "button",
					"x" : 1145, "y" : 452+32*0,
					"default_image" : BTN_PATH + "btn_select_blank.png",
					"over_image" : BTN_PATH + "btn_select.png",
					"down_image" : BTN_PATH + "btn_select.png",
				},
				{
					"name" : "account_2_txt", "type" : "text",
					"x" : 1150, "y" : 456+32*1,
					"text" : "#02 - " + "Freier Slot",
				},
				{
					"name" : "account_2", "type" : "button",
					"x" : 1145, "y" : 454+32*1,
					"default_image" : BTN_PATH + "btn_select_blank.png",
					"over_image" : BTN_PATH + "btn_select.png",
					"down_image" : BTN_PATH + "btn_select.png",
				},
				{
					"name" : "account_3_txt", "type" : "text",
					"x" : 1150, "y" : 456+32*2,
					"text" : "#03 - " + "Freier Slot",
				},
				{
					"name" : "account_3", "type" : "button",
					"x" : 1145, "y" : 454+32*2,
					"default_image" : BTN_PATH + "btn_select_blank.png",
					"over_image" : BTN_PATH + "btn_select.png",
					"down_image" : BTN_PATH + "btn_select.png",
				},
				{
					"name" : "account_4_txt", "type" : "text",
					"x" : 1150, "y" : 456+32*3,
					"text" : "#04 - " + "Freier Slot",
				},
				{
					"name" : "account_4", "type" : "button",
					"x" : 1145, "y" : 454+32*3,
					"default_image" : BTN_PATH + "btn_select_blank.png",
					"over_image" : BTN_PATH + "btn_select.png",
					"down_image" : BTN_PATH + "btn_select.png",
				},
				{
					"name" : "account_5_txt", "type" : "text",
					"x" : 1150, "y" : 456+32*4,
					"text" : "#05 - " + "Freier Slot",
				},
				{
					"name" : "account_5", "type" : "button",
					"x" : 1145, "y" : 454+32*4,
					"default_image" : BTN_PATH + "btn_select_blank.png",
					"over_image" : BTN_PATH + "btn_select.png",
					"down_image" : BTN_PATH + "btn_select.png",
				},
				{
					"name" : "account_6_txt", "type" : "text",
					"x" : 1150, "y" : 456+32*5,
					"text" : "#06 - " + "Freier Slot",
				},
				{
					"name" : "account_6", "type" : "button",
					"x" : 1145, "y" : 454+32*5,
					"default_image" : BTN_PATH + "btn_select_blank.png",
					"over_image" : BTN_PATH + "btn_select.png",
					"down_image" : BTN_PATH + "btn_select.png",
				},
				{
					"name" : "logo", "type" : "button",
					"x" : 815, "y" : 165,
					"default_image" : BTN_PATH + "logo.png",
					"over_image" : BTN_PATH + "logo.png",
					"down_image" : BTN_PATH + "logo.png",
				},				
				{
					"name" : "loadAnim",
					"type" : "ani_image",

					"x" : 80,
					"y" : 384,

					"delay" : 2,

					"images" :
					(
						ROOT + "img0001.png",
						ROOT + "img0002.png",
						ROOT + "img0003.png",
						ROOT + "img0004.png",
						ROOT + "img0005.png",
						ROOT + "img0006.png",
						ROOT + "img0007.png",
						ROOT + "img0008.png",
						ROOT + "img0009.png",
						ROOT + "img0010.png",
						ROOT + "img0011.png",
						ROOT + "img0012.png",
						ROOT + "img0013.png",
						ROOT + "img0014.png",
						ROOT + "img0015.png",
						ROOT + "img0016.png",
						ROOT + "img0017.png",
						ROOT + "img0018.png",
						ROOT + "img0019.png",
						ROOT + "img0020.png",
						ROOT + "img0021.png",
						ROOT + "img0022.png",
						ROOT + "img0023.png",
						ROOT + "img0024.png",
						ROOT + "img0025.png",
						ROOT + "img0026.png",
						ROOT + "img0027.png",
						ROOT + "img0028.png",
						ROOT + "img0029.png",
						ROOT + "img0030.png",
						ROOT + "img0031.png",
						
					
					)
				},
			),
		},
	),
}