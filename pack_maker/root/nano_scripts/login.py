import nano_interface
import localeInfo

AJUST_HEIGHT = 7
ROOT = "nano_interface/animations/cicle/"
BASE_PATH = "nano_interface/"

window = {
	"name" : "LoginWindow",
	"sytle" : ("movable",),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		# Board
		{
			"name" : "background_el",
			"type" : "image",
			"x" : 0,
			"y" : 0,
			"x_scale" : float(SCREEN_WIDTH) / 1920.0,
			"y_scale" : float(SCREEN_HEIGHT) / 1080.0,
			"image": BASE_PATH + "login.jpg",
		},
		
		{
			"name" : "board",
			"type" : "nano_login_board",
			"x" : (SCREEN_WIDTH-230),
			"y" : -35,

			"width" : 290,
			"height" : SCREEN_HEIGHT+200,
			"children" :
			(

				{
					"name" : "Logo",
					"type" : "expanded_image",

					"x": 30,
					"y": 45+AJUST_HEIGHT,
					
					"image": BASE_PATH + "logo.png",

				},
				
				#{
				#	"name" : "logText",
				#	"type" : "text",

				#	"x": 32,
				#	"y": 130+AJUST_HEIGHT,
					
				#	"text": localeInfo.SIGN_IN,
				#	"fontname" : "Tahoma Bold:17",
				#	"color" : nano_interface.SING_IN_COLOR,
	
				#},
				# {
					# "name" : "bo2ard",
					# "type" : "board_nano",
					# "x": -532,
					# "y": 112,

					# "width" : 290,
					# "height" : 360,
	
				# },
				# Remember Me
				#{
				#	"name" : "remeberBtn",
				#	"type" : "toggle_button",

				#	"x": 32,
				#	"y": 302,

				#	"default_image": BASE_PATH+"buttons/remember_me_normal.png",
				#	"over_image": BASE_PATH+"buttons/remember_me_active.png",
				#	"down_image": BASE_PATH+"buttons/remember_me_active.png",
				#},
				#{
				#	"name" : "remeberTxt",
				#	"type" : "text",

				#	"x": 32+50,
				#	"y": 302,

				#	"fontname" : "Tahoma Bold:13",
				#	"outline" : 1,
					
					
				#	"color" : 0xff969184,
				#	"text" : localeInfo.REMEMBER_ME,
				#},
				#{
				#	"name" : "remebermeInf",
				#	"type" : "text",

				#	"x": 50,
				#	"y": 300,

				#	"fontname" : "Tahoma Bold:13",
				#	"outline" : 1,
					
					
				#	"color" : 0xff969184,
				#	"text" : localeInfo.REMEMBER_ME,
				#},
				# Save account
				{
					"name" : "saveBtn",
					"type" : "toggle_button",

					"x": 32,
					"y": 302,

					"default_image": BASE_PATH+"buttons/remember_me_normal.png",
					"over_image": BASE_PATH+"buttons/remember_me_active.png",
					"down_image": BASE_PATH+"buttons/remember_me_active.png",
				},
				{
					"name" : "saveInf",
					"type" : "text",

					"x": 50,
					"y": 300,

					"fontname" : "Tahoma Bold:13",
					"outline" : 1,
					
					
					"color" : 0xff969184,
					"text" : localeInfo.SAVE_ME,
				},
				# Modo Perros
				## Server Channel
				#{
				#	"name" : "serverClient",
				#	"type" : "text",

				#	"x": 32,
				#	"y": 332,

				#	"fontname" : "Tahoma Bold:13",
				#	"outline" : 1,
					
					
				#	"color" : 0xff969184,
				#	"text" : localeInfo.SERVERORCHANNEL,
				#},
				
				#{
				#	"name": "showServerList",
				#	"type": "nano_text_link",

				#	"x": 33,
				#	"y": 385+AJUST_HEIGHT,
					
				#	"text" : "Server/Channel",

				#},
				
				#Holders
				{
					"name" : "placeHolderId",
					"type" : "special_editline",

					"x" : 32,
					"y" : 190+AJUST_HEIGHT,
					
					"width" : 121,
					"height" : 25,

					"input_limit" : 35,
					"enable_ime" : 0,
					
					"color" : 0xff969184,
					"children" :
					(
						{
							"name": "text",
							"type": "text",

							"x": -10,
							"y": -30,
							
							"fontname" : "Tahoma Bold:13",
							"outline" : 1,
							
							"color" : 0xff969184,
							"text" : localeInfo.ID_HOLD,

						},
					),
				},
				
				{
					"name" : "placeHolderPw",
					"type" : "special_editline",

					"x" : 32,
					"y" : 248+AJUST_HEIGHT,
					
					"width" : 121,
					"height" : 25,

					"input_limit" : 35,
					"enable_ime" : 0,
					
					"color" : 0xff969184,
					"children" :
					(
						{
							"name": "text",
							"type": "text",

							"x": -10,
							"y": -30,
							
							"fontname" : "Tahoma Bold:13",
							"outline" : 1,
							
							
							"color" : 0xff969184,
							"text" : localeInfo.PW_HOLD,

						},
					),
				},

				#Server link
				
				#Channels
				{
					"name" : "channel_1",
					"type" : "radio_button",

					"x": 23,
					"y": 350,

					"default_image": BASE_PATH+"server_buttons/btn_ch_normal.png",
					"over_image": BASE_PATH+"server_buttons/btn_ch_active.png",
					"down_image": BASE_PATH+"server_buttons/btn_ch_hover.png",
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
					"name" : "channel_2",
					"type" : "radio_button",

					"x": 23,
					"y": 350+38,

					"default_image": BASE_PATH+"server_buttons/btn_ch_normal.png",
					"over_image": BASE_PATH+"server_buttons/btn_ch_active.png",
					"down_image": BASE_PATH+"server_buttons/btn_ch_hover.png",
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
					"name" : "channel_3",
					"type" : "radio_button",

					"x": 23,
					"y": 350+38+38,

					"default_image": BASE_PATH+"server_buttons/btn_ch_normal.png",
					"over_image": BASE_PATH+"server_buttons/btn_ch_active.png",
					"down_image": BASE_PATH+"server_buttons/btn_ch_hover.png",
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
					"name" : "channel_4",
					"type" : "radio_button",

					"x": 23,
					"y": 350+38+38+38,

					"default_image": BASE_PATH+"server_buttons/btn_ch_normal.png",
					"over_image": BASE_PATH+"server_buttons/btn_ch_active.png",
					"down_image": BASE_PATH+"server_buttons/btn_ch_hover.png",
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
				
				{
					"name" : "account_1",
					"type" : "radio_button",

					"x": 110,
					"y": 350,

					"default_image": BASE_PATH+"server_buttons/btn_account_normal.png",
					"over_image": BASE_PATH+"server_buttons/btn_account_active.png",
					"down_image": BASE_PATH+"server_buttons/btn_account_hover.png",
					"children" :
					(
						{
							"name": "account_1_txt",
							"type": "text",

							"x": 9,
							"y": 9,

							"text" : localeInfo.ACCOUNT_1,

						},
					),
				},
				{
					"name" : "account_1_delete",
					"type" : "button",

					"x": 206,
					"y": 355,

					"default_image": BASE_PATH+"server_buttons/eliminar.png",
					"over_image": BASE_PATH+"server_buttons/eliminar_pulsado.png",
					"down_image": BASE_PATH+"server_buttons/eliminar.png",
				},
				{
					"name" : "account_2",
					"type" : "radio_button",

					"x": 110,
					"y": 350+38,

					"default_image": BASE_PATH+"server_buttons/btn_account_normal.png",
					"over_image": BASE_PATH+"server_buttons/btn_account_active.png",
					"down_image": BASE_PATH+"server_buttons/btn_account_hover.png",
					"children" :
					(
						{
							"name": "account_2_txt",
							"type": "text",

							"x": 9,
							"y": 9,

							"text" : localeInfo.ACCOUNT_2,
						},

					),
				},
				{
					"name" : "account_2_delete",
					"type" : "radio_button",
					
					"x": 206,
					"y": 355+38,

					"default_image": BASE_PATH+"server_buttons/eliminar.png",
					"over_image": BASE_PATH+"server_buttons/eliminar_pulsado.png",
					"down_image": BASE_PATH+"server_buttons/eliminar.png",
				},
				{
					"name" : "account_3",
					"type" : "radio_button",

					"x": 110,
					"y": 350+38+38,

					"default_image": BASE_PATH+"server_buttons/btn_account_normal.png",
					"over_image": BASE_PATH+"server_buttons/btn_account_active.png",
					"down_image": BASE_PATH+"server_buttons/btn_account_hover.png",
					"children" :
					(
						{
							"name": "account_3_txt",
							"type": "text",

							"x": 9,
							"y": 9,

							"text" : localeInfo.ACCOUNT_3,
						},
					),
				},
				{
					"name" : "account_3_delete",
					"type" : "radio_button",

					"x": 206,
					"y": 355+38+38,

					"default_image": BASE_PATH+"server_buttons/eliminar.png",
					"over_image": BASE_PATH+"server_buttons/eliminar_pulsado.png",
					"down_image": BASE_PATH+"server_buttons/eliminar.png",
				},
				{
					"name" : "account_4",
					"type" : "radio_button",

					"x": 110,
					"y": 350+38+38+38,

					"default_image": BASE_PATH+"server_buttons/btn_account_normal.png",
					"over_image": BASE_PATH+"server_buttons/btn_account_active.png",
					"down_image": BASE_PATH+"server_buttons/btn_account_hover.png",
					"children" :
					(
						{
							"name": "account_4_txt",
							"type": "text",

							"x": 9,
							"y": 9,

							"text" : localeInfo.ACCOUNT_4,
						},
					),
				},
				{
					"name" : "account_4_delete",
					"type" : "radio_button",

					"x": 206,
					"y": 355+38+38+38,

					"default_image": BASE_PATH+"server_buttons/eliminar.png",
					"over_image": BASE_PATH+"server_buttons/eliminar_pulsado.png",
					"down_image": BASE_PATH+"server_buttons/eliminar.png",
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
				
				{
					"name": "loginInfor",
					"type": "text",

					"x": 40,
					"y": 160,

					"text" : "TextTextTextTextTextText",

				},
				{
					"name" : "loginBtn",
					"type" : "button",

					"x": 27,
					"y": SCREEN_HEIGHT-90,

					"default_image": BASE_PATH + "buttons/btn_normal.png",
					"over_image": BASE_PATH + "buttons/btn_active.png",
					"down_image": BASE_PATH + "buttons/btn_hover.png",
					"disable_image": BASE_PATH + "buttons/btn_disabled.png",
					"children" :
					(
						{
							"name": "fontButton",
							"type": "text",

							"x": -25,
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

					"x": 33,
					"y": SCREEN_HEIGHT-50,
					
					"text" : localeInfo.FORGOT_PASSWORD,

				},
				{
					"name": "link_acc",
					"type": "nano_text_link_login",

					"x": 33,
					"y": SCREEN_HEIGHT-35,
					
					"text" : localeInfo.CREATE_ACCOUNT,

				},
				
				{
					"name": "bar",
					"type": "nano_horizontal",

					"x": 15,
					"y": SCREEN_HEIGHT-10,

					"width" : 160,
					"children" :
					(
						{
							"name": "versionAndCreator",
							"type": "text",

							"x": -30,
							"y": 9,
							
							#
							"horizontal_align": "center",
							# "vertical_align": "center",
							#
					
							"fontname" : "Tahoma Bold:16.5",
							"text" : localeInfo.VERSION + localeInfo.CREATOR,
							"color" : 0xff3c3c41,

						},
					),
				},
			)
		},
		#{
		#	"name" : "reBackgr",
		#	"type" : "toggle_button",

		#	"x": 132,
		#	"y": SCREEN_HEIGHT-40,

		#	"default_image": BASE_PATH+"buttons/remember_me_normal.png",
		#	"over_image": BASE_PATH+"buttons/remember_me_active.png",
		#	"down_image": BASE_PATH+"buttons/remember_me_active.png",
		#},
		# Remember Me
		#{
		#	"name" : "reback",
		#	"type" : "text",

		#	"x": 153,
		#	"y": SCREEN_HEIGHT-42,

		#	"fontname" : "Tahoma Bold:13",
		#	"outline" : 1,
			
			
		#	"color" : 0xff969184,
		#	"text" : localeInfo.BACKGROUND,
		#},
		{
			"name" : "change_es",
			"type" : "radio_button",

			"x": 10,
			"y": 10,

			"default_image": "d:/ymir work/ui/language/es.png",
			"over_image": "d:/ymir work/ui/language/es_hover.png",
			"down_image": "d:/ymir work/ui/language/es_hover.png",
		},
		{
			"name" : "change_en",
			"type" : "radio_button",

			"x": 10+40,
			"y": 10,

			"default_image": "d:/ymir work/ui/language/en.png",
			"over_image": "d:/ymir work/ui/language/en_hover.png",
			"down_image": "d:/ymir work/ui/language/en_hover.png",
		},
		{
			"name" : "change_pt",
			"type" : "radio_button",

			"x": 10+40+40,
			"y": 10,

			"default_image": "d:/ymir work/ui/language/pt.png",
			"over_image": "d:/ymir work/ui/language/pt_hover.png",
			"down_image": "d:/ymir work/ui/language/pt_hover.png",
		},
		{
			"name" : "change_de",
			"type" : "radio_button",

			"x": 10+40+40+40,
			"y": 10,

			"default_image": "d:/ymir work/ui/language/de.png",
			"over_image": "d:/ymir work/ui/language/de_hover.png",
			"down_image": "d:/ymir work/ui/language/de_hover.png",
		},
		{
			"name" : "change_ru",
			"type" : "radio_button",

			"x": 10+40+40+40+40,
			"y": 10,

			"default_image": "d:/ymir work/ui/language/ru.png",
			"over_image": "d:/ymir work/ui/language/ru_hover.png",
			"down_image": "d:/ymir work/ui/language/ru_hover.png",
		},
		{
			"name" : "change_pl",
			"type" : "radio_button",

			"x": 10+40+40+40+40+40,
			"y": 10,

			"default_image": "d:/ymir work/ui/language/pl.png",
			"over_image": "d:/ymir work/ui/language/pl_hover.png",
			"down_image": "d:/ymir work/ui/language/pl_hover.png",
		},
	),
}
