import localeInfo
import uiScriptLocale

IMG_DIR = "d:/ymir work/ui/login_new/"

IMG_EXTENSION = ".png"

window = {
	"name": "LoginWindow",
	"sytle": ("movable","attach","float",),
	"x": 0,
	"y": 0,
	"width": SCREEN_WIDTH,
	"height": SCREEN_HEIGHT,
	"children": 
	(
		{
			"name": "BackGround",
			"type": "expanded_image",
			"x": 0,
			"y": 0,
			"image": IMG_DIR+"login_bg"+IMG_EXTENSION,
			"x_scale": float(SCREEN_WIDTH) / 1920.0,
			"y_scale": float(SCREEN_HEIGHT) / 1080.0,
		},
		{
			"name": "BackGround_ANI",
			"type": "ani_image",
			"x": 0,
			"y": 0,
			"x_scale": float(SCREEN_WIDTH) / 1920.0,
			"y_scale": float(SCREEN_HEIGHT) / 1080.0,
		},
		{
			"name": "Logo",
			"type": "image",
			"x": (float(SCREEN_WIDTH)/3.2),
			"y": (float(SCREEN_HEIGHT)/9.5),
			"x_scale": float(SCREEN_WIDTH) / 1920.0,
			"y_scale": float(SCREEN_HEIGHT) / 1080.0,
			"image": IMG_DIR+"logo"+IMG_EXTENSION,
		},

		{
			"name": "AccountImage",
			"type": "image",
			"x": (float(SCREEN_WIDTH)/2.0)-(320.0/2.0)+320-14-12-10,
			"y": (float(SCREEN_HEIGHT)/2.0)-(307.0/2.0)+40+37,
			"image": IMG_DIR+"saved_acc/right_box"+IMG_EXTENSION,
			"children": 
			(
				{"name": "saved_accounts","type": "image","x": 48 + 14,"y": 12,"image": IMG_DIR+"saved_acc/saved_account"+IMG_EXTENSION,},
				{
					"name": "back_page",
					"type": "button",
					"x": 3 + 14,
					"y": 8,
					"default_image" : IMG_DIR+"saved_acc/arrow_left"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"saved_acc/arrow_left_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"saved_acc/arrow_left_down"+IMG_EXTENSION,
				},
				{
					"name": "next_page",
					"type": "button",
					"x": 194 + 14,
					"y": 8,
					"default_image" : IMG_DIR+"saved_acc/arrow_right"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"saved_acc/arrow_right_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"saved_acc/arrow_right_down"+IMG_EXTENSION,
				},
				# {
					# "name": "page_image",
					# "type": "image",
					# "x": 15 + 14,
					# "y": 12,
					# "image" : IMG_DIR+"saved_acc/page_image"+IMG_EXTENSION,
					# "children": 
					# (
						# {"name" : "page_text", "type" : "text", "x" : 0, "y" : 0, "fontname":"Tahoma:11","all_align":1 , "color":0xFF948D87, "text":"1 of 2",},
					# ),
				# },

				{
					"name": "Account0Window",
					"type": "image",
					"x": 9,
					"y": 25 + (34 * 0),
					"image" : IMG_DIR+"saved_acc/ebene"+IMG_EXTENSION,
					"children": 
					(
						{"name" : "account0text", "sytle": ("not_pick",), "type" : "text", "x" : 40, "y" : 8, "text_horizontal_align":"left" , "color":0xFFD6C8BB, "text":"Free Slot",},
						{
							"name": "account0start",
							"type": "button",
							"x": 158-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/arrow"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/arrow_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/arrow_down"+IMG_EXTENSION,
						},

						{
							"name": "account0delete",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/delete"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/delete_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/delete_down"+IMG_EXTENSION,
						},

						{
							"name": "account0save",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/shape"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/shape_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/shape_down"+IMG_EXTENSION,
						},
					),
				},
				{
					"name": "Account1Window",
					"type": "image",
					"x": 9,
					"y": 25 + (34 * 1),
					"image" : IMG_DIR+"saved_acc/ebene"+IMG_EXTENSION,
					"children": 
					(
						{"name" : "account1text", "sytle": ("not_pick",), "type" : "text", "x" : 40, "y" : 8, "text_horizontal_align":"left" , "color":0xFFD6C8BB, "text":"Free Slot",},
						{
							"name": "account1start",
							"type": "button",
							"x": 158-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/arrow"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/arrow_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/arrow_down"+IMG_EXTENSION,
						},

						{
							"name": "account1delete",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/delete"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/delete_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/delete_down"+IMG_EXTENSION,
						},

						{
							"name": "account1save",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/shape"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/shape_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/shape_down"+IMG_EXTENSION,
						},
					),
				},
				{
					"name": "Account2Window",
					"type": "image",
					"x": 9,
					"y": 25 + (34 * 2),
					"image" : IMG_DIR+"saved_acc/ebene"+IMG_EXTENSION,
					"children": 
					(
						{"name" : "account2text", "sytle": ("not_pick",), "type" : "text", "x" : 40, "y" : 8, "text_horizontal_align":"left" , "color":0xFFD6C8BB, "text":"Free Slot",},
						{
							"name": "account2start",
							"type": "button",
							"x": 158-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/arrow"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/arrow_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/arrow_down"+IMG_EXTENSION,
						},

						{
							"name": "account2delete",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/delete"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/delete_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/delete_down"+IMG_EXTENSION,
						},

						{
							"name": "account2save",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/shape"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/shape_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/shape_down"+IMG_EXTENSION,
						},
					),
				},
				{
					"name": "Account3Window",
					"type": "image",
					"x": 9,
					"y": 25 + (34 * 3),
					"image" : IMG_DIR+"saved_acc/ebene"+IMG_EXTENSION,
					"children": 
					(
						{"name" : "account3text", "sytle": ("not_pick",), "type" : "text", "x" : 40, "y" : 8, "text_horizontal_align":"left" , "color":0xFFD6C8BB, "text":"Free Slot",},
						{
							"name": "account3start",
							"type": "button",
							"x": 158-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/arrow"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/arrow_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/arrow_down"+IMG_EXTENSION,
						},

						{
							"name": "account3delete",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/delete"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/delete_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/delete_down"+IMG_EXTENSION,
						},

						{
							"name": "account3save",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/shape"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/shape_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/shape_down"+IMG_EXTENSION,
						},
					),
				},
				{
					"name": "Account4Window",
					"type": "image",
					"x": 9,
					"y": 25 + (34 * 4),
					"image" : IMG_DIR+"saved_acc/ebene"+IMG_EXTENSION,
					"children": 
					(
						{"name" : "account4text", "sytle": ("not_pick",), "type" : "text", "x" : 40, "y" : 8, "text_horizontal_align":"left" , "color":0xFFD6C8BB, "text":"Free Slot",},
						{
							"name": "account4start",
							"type": "button",
							"x": 158-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/arrow"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/arrow_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/arrow_down"+IMG_EXTENSION,
						},

						{
							"name": "account4delete",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/delete"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/delete_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/delete_down"+IMG_EXTENSION,
						},

						{
							"name": "account4save",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/shape"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/shape_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/shape_down"+IMG_EXTENSION,
						},
					),
				},
				{
					"name": "Account5Window",
					"type": "image",
					"x": 9,
					"y": 25 + (34 * 5),
					"image" : IMG_DIR+"saved_acc/ebene"+IMG_EXTENSION,
					"children": 
					(
						{"name" : "account5text", "sytle": ("not_pick",), "type" : "text", "x" : 40, "y" : 8, "text_horizontal_align":"left" , "color":0xFFD6C8BB, "text":"Free Slot",},
						{
							"name": "account5start",
							"type": "button",
							"x": 158-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/arrow"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/arrow_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/arrow_down"+IMG_EXTENSION,
						},

						{
							"name": "account5delete",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/delete"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/delete_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/delete_down"+IMG_EXTENSION,
						},

						{
							"name": "account5save",
							"type": "button",
							"x": 173-10,
							"y": 12-3,
							"default_image" : IMG_DIR+"saved_acc/shape"+IMG_EXTENSION,
							"over_image" : IMG_DIR+"saved_acc/shape_hover"+IMG_EXTENSION,
							"down_image" : IMG_DIR+"saved_acc/shape_down"+IMG_EXTENSION,
						},
					),
				},
			),
		},

		{
			"name": "ChannelImage",
			"type": "image",
			"x": (float(SCREEN_WIDTH)/2.0)-(320.0/2.0)-231+13+12+10,
			"y": (float(SCREEN_HEIGHT)/2.0)-(307.0/2.0)+40+37,
			"image": IMG_DIR+"channels/left_box"+IMG_EXTENSION,
			"children": 
			(
				{"name": "select_channel","type": "image","x": 48,"y": 12,"image": IMG_DIR+"channels/select_channel"+IMG_EXTENSION,},
				{
					"name": "Channel0",
					"type": "radio_button",
					"x": 25,
					"y": 25 + (34 * 0),
					"default_image" : IMG_DIR+"channels/ch1"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"channels/ch1_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"channels/ch1_down"+IMG_EXTENSION,
					"children": 
					(
						{"name": "stat_0","type": "image","x": 24,"y": 9,"image": IMG_DIR+"channels/offline"+IMG_EXTENSION,},
					),
				},
				{
					"name": "Channel1",
					"type": "radio_button",
					"x": 25,
					"y": 25 + (34 * 1),
					"default_image" : IMG_DIR+"channels/ch2"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"channels/ch2_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"channels/ch2_down"+IMG_EXTENSION,
					"children": 
					(
						{"name": "stat_1","type": "image","x": 24,"y": 9,"image": IMG_DIR+"channels/offline"+IMG_EXTENSION,},
					),
				},
				{
					"name": "Channel2",
					"type": "radio_button",
					"x": 25,
					"y": 25 + (34 * 2),
					"default_image" : IMG_DIR+"channels/ch3"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"channels/ch3_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"channels/ch3_down"+IMG_EXTENSION,
					"children": 
					(
						{"name": "stat_2","type": "image","x": 24,"y": 9,"image": IMG_DIR+"channels/offline"+IMG_EXTENSION,},
					),
				},
				{
					"name": "Channel3",
					"type": "radio_button",
					"x": 25,
					"y": 25 + (34 * 3),
					"default_image" : IMG_DIR+"channels/ch4"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"channels/ch4_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"channels/ch4_down"+IMG_EXTENSION,
					"children": 
					(
						{"name": "stat_3","type": "image","x": 24,"y": 9,"image": IMG_DIR+"channels/offline"+IMG_EXTENSION,},
					),
				},
				{
					"name": "Channel4",
					"type": "radio_button",
					"x": 25,
					"y": 25 + (34 * 4),
					"default_image" : IMG_DIR+"channels/ch5"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"channels/ch5_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"channels/ch5_down"+IMG_EXTENSION,
					"children": 
					(
						{"name": "stat_4","type": "image","x": 24,"y": 9,"image": IMG_DIR+"channels/offline"+IMG_EXTENSION,},
					),
				},
				{
					"name": "Channel5",
					"type": "radio_button",
					"x": 25,
					"y": 25 + (34 * 5),
					"default_image" : IMG_DIR+"channels/ch6"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"channels/ch6_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"channels/ch6_down"+IMG_EXTENSION,
					"children": 
					(
						{"name": "stat_5","type": "image","x": 24,"y": 9,"image": IMG_DIR+"channels/offline"+IMG_EXTENSION,},
					),
				},
			),
		},
		
		{
			"name": "LangImage",
			"type": "image",
			"x": (float(SCREEN_WIDTH)/2.0)-(259.0/2.0),
			"y": (float(SCREEN_HEIGHT)/2.0)+40+(307/2)+26,
			"image": IMG_DIR+"language/bg"+IMG_EXTENSION,
			"children": 
			(
				{"name": "left_wing","type": "image","x": -17,"y": -7,"image": IMG_DIR+"language/left"+IMG_EXTENSION,},
				{"name": "right_wing","type": "image","x": 242,"y": -7,"image": IMG_DIR+"language/right"+IMG_EXTENSION,},
				{
					"name": "lang_0",
					"type": "radio_button",
					"x": 35+(0*31),
					"y": 14,
					"default_image" : IMG_DIR+"language/eng"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"language/eng_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"language/eng_down"+IMG_EXTENSION,
				},
				{
					"name": "lang_1",
					"type": "radio_button",
					"x": 45+(1 * 31),
					"y": 14,
					"default_image" : IMG_DIR+"language/turk"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"language/turk_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"language/turk_down"+IMG_EXTENSION,
				},
				{
					"name": "lang_2",
					"type": "radio_button",
					"x": 55+(2 * 31),
					"y": 14,
					"default_image" : IMG_DIR+"language/ger"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"language/ger_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"language/ger_down"+IMG_EXTENSION,
				},

				{
					"name": "lang_3",
					"type": "radio_button",
					"x": 65+(3 * 31),
					"y": 14,
					"default_image" : IMG_DIR+"language/pol"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"language/pol_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"language/pol_down"+IMG_EXTENSION,
				},
				{
					"name": "lang_4",
					"type": "radio_button",
					"x": 75+(4 * 31),
					"y": 14,
					"default_image" : IMG_DIR+"language/ru"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"language/ru_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"language/ru_down"+IMG_EXTENSION,
				},

			),
		},


		{
			"name": "MainImage",
			"type": "image",
			"x": (float(SCREEN_WIDTH)/2.0)-(320.0/2.0),
			"y": (float(SCREEN_HEIGHT)/2.0)-(307.0/2.0)+40,
			"image": IMG_DIR+"login/main_box"+IMG_EXTENSION,
			"children": 
			(
				{"name": "login_details","type": "image","x": 83,"y": 45,"image": IMG_DIR+"login/login_details"+IMG_EXTENSION,},
				{
					"name": "username_image",
					"type": "image",
					"x": 42,
					"y": 70 + (44 * 0),
					"image" : IMG_DIR+"login/button"+IMG_EXTENSION,
					"children": 
					(
						{"name": "username_icon","type": "image","x": 18,"y": 10,"image": IMG_DIR+"login/user"+IMG_EXTENSION,},
						{
							"name": "id_editline",
							"type": "editline",
							"info_msg": "ID",
							"x": 39,
							"y": 10,
							"width": 187,
							"height": 32,
							"input_limit": 16,
							"enable_codepage": 0,
							"color":0xFFBBB4AE,
						},
					),
				},
				{
					"name": "password_image",
					"type": "image",
					"x": 42,
					"y": 70 + (44 * 1),
					"image" : IMG_DIR+"login/button"+IMG_EXTENSION,
					"children": 
					(
						{"name": "password_icon","type": "image","x": 18,"y": 10,"image": IMG_DIR+"login/lock"+IMG_EXTENSION,},
						{
							"name": "pwd_editline",
							"type": "editline",
							"info_msg":"Password",
							"x": 39,
							"y": 10,
							"width": 187,
							"height": 32,
							"input_limit": 16,
							"secret_flag": 1,
							"enable_codepage": 0,
							"color":0xFFBBB4AE,
							"children":
							(
								{
									"name": "hide_text",
									"type": "toggle_button",
									"x": 187-5-24,
									"y": -1,
									"default_image": IMG_DIR+"login/show_eye"+IMG_EXTENSION,
									"over_image": IMG_DIR+"login/hide_eye"+IMG_EXTENSION,
									"down_image": IMG_DIR+"login/hide_eye"+IMG_EXTENSION,
								},
							),
						},
					),
				},
				{
					"name": "ForgetPassswordWnd",
					"type": "window",
					"x": 200,
					"y": 195,
					"width":75,
					"height":20,
					"children":(
						{"name" : "forget_password", "type" : "text", "x" : 0, "y" : 0, "text_horizontal_align":"left" , "color" : 0xFFD6C8BB, "text": uiScriptLocale.FORGET_PASS,},
					),
				},

				{
					"name": "login_button",
					"type": "button",
					"x": 79,
					"y": 232,
					"default_image" : IMG_DIR+"login/button_main"+IMG_EXTENSION,
					"over_image" : IMG_DIR+"login/button_hover"+IMG_EXTENSION,
					"down_image" : IMG_DIR+"login/button_down"+IMG_EXTENSION,
					# "children": 
					# (
						# {"name": "pin_icon","type": "image","x": 63,"y": 16,"image": IMG_DIR+"login/login"+IMG_EXTENSION,"sytle": ("not_pick",),},
					# ),
				},

				
			),
		},
	),
}
