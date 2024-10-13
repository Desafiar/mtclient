BASE_PATH = "jack_work/images/select/"
BTN_PATH = BASE_PATH + "btn/"

height = 0
if SCREEN_HEIGHT <= 1000:
	height = -120


window = {
	"name" : "SelectCharacterWindow",
	"x" : 0, "y" : 0, "width" : SCREEN_WIDTH, "height" : SCREEN_HEIGHT,
	"style" : ("float",),
	"children" :
	(
		{
			"name" : "background", "type" : "image",
			"x" : SCREEN_WIDTH / 2 - 1920 / 2, "y" : 0 + height,
			"image" : BASE_PATH + "background.tga",
		},
		{
			"name" : "content", "type" : "image",
			"x" : SCREEN_WIDTH / 4 - 360 / 2, "y" : SCREEN_HEIGHT / 2 - 520 / 2,
			"image" : BASE_PATH + "content.tga",
			"children" :
			(
				# NAME - Field
				{
					"name" : "text_playername", "type" : "text",
					"x" : 265, "y" : 209+34*2,
					"text_horizontal_align" : "center",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
				# LEVEL - Field
				{
					"name" : "text_level", "type" : "text",
					"x" : 265, "y" : 209+34*3,
					"text_horizontal_align" : "center",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
				# GUILD - Field
				{
					"name" : "text_guildname", "type" : "text",
					"x" : 265, "y" : 209+34*1,
					"text_horizontal_align" : "center",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
				# VIT - Field
				{
					"name" : "gauge_vit", "type" : "gauge",
					"x" : 90, "y" : 390+30*0, "width" : 200,
					"color" : "red",
				},
				{
					"name" : "text_value_vit", "type" : "text",
					"x" : 300, "y" : 386+30*0,
					"color" : 0xffCECECE,
					"text" : "99",
				},
				# INT - Field
				{
					"name" : "gauge_int", "type" : "gauge",
					"x" : 90, "y" : 390+30*1, "width" : 200,
					"color" : "blue",
				},
				{
					"name" : "text_value_int", "type" : "text",
					"x" : 300, "y" : 386+30*1,
					"color" : 0xffCECECE,
					"text" : "99",
				},
				# STR - Field
				{
					"name" : "gauge_str", "type" : "gauge",
					"x" : 90, "y" : 390+30*2, "width" : 200,
					"color" : "purple",
				},
				{
					"name" : "text_value_str", "type" : "text",
					"x" : 300, "y" : 386+30*2,
					"color" : 0xffCECECE,
					"text" : "99",
				},
				# DEX - Field
				{
					"name" : "gauge_dex", "type" : "gauge",
					"x" : 90, "y" : 390+30*3, "width" : 200,
					"color" : "pink",
				},
				{
					"name" : "text_value_dex", "type" : "text",
					"x" : 300, "y" : 386+30*3,
					"color" : 0xffCECECE,
					"text" : "99",
				},
				# PLAYTIME - Field
				{
					"name" : "text_timevalue", "type" : "text",
					"x" : 265, "y" : 209+34*4,
					"text_horizontal_align" : "center",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
				# KINGDOMNAME - Field
				{
					"name" : "text_kingdomvalue", "type" : "text",
					"x" : 265, "y" : 209,
					"text_horizontal_align" : "center",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
				# LOGINBTN - Field
				{
					"name" : "btn_login", "type" : "button",
					"x" : 0, "y" : 165,
					"horizontal_align" : "center",
					"vertical_align" : "bottom",
					"default_image" : BTN_PATH + "btn_select_normal.tga",
					"over_image" : BTN_PATH + "btn_select_hover.tga",
					"down_image" : BTN_PATH + "btn_select_active.tga",
				},
				# CREATEBTN - Field
				{
					"name" : "btn_create", "type" : "button",
					"x" : 0, "y" : 165,
					"horizontal_align" : "center",
					"vertical_align" : "bottom",
					"default_image" : BTN_PATH + "btn_select_normal.tga",
					"over_image" : BTN_PATH + "btn_select_hover.tga",
					"down_image" : BTN_PATH + "btn_select_active.tga",
				},
				# RACEIMG - Field
				{
					"name" : "img_race", "type" : "image",
					"x" : 0, "y" : 130,
					"horizontal_align" : "center",
					"image" : BASE_PATH + "img_race_warrior.tga",
				},
			),
		},
		# CHARACTERRENDER - Field
		{
			"name" : "character_render_window", "type" : "window",
			"x" : SCREEN_WIDTH / 2, "y" : 0,
			"width" : SCREEN_WIDTH / 2, "height" : SCREEN_HEIGHT,
			"children" :
			(
				{
					"name" : "btn_left", "type" : "button",
					"x" : 50, "y" : SCREEN_HEIGHT / 2 - 42 / 2,
					"default_image" : BTN_PATH + "btn_left_normal.tga",
					"over_image" : BTN_PATH + "btn_left_hover.tga",
					"down_image" : BTN_PATH + "btn_left_down.tga",
				},
				{
					"name" : "btn_right", "type" : "button",
					"x" : SCREEN_WIDTH / 2 - 40 - 50, "y" : SCREEN_HEIGHT / 2 - 42 / 2,
					"default_image" : BTN_PATH + "btn_right_normal.tga",
					"over_image" : BTN_PATH + "btn_right_hover.tga",
					"down_image" : BTN_PATH + "btn_right_down.tga",
				},
				{
					"name" : "text_slot", "type" : "text",
					"x" : SCREEN_WIDTH / 4, "y" : SCREEN_HEIGHT - 50,
					"text_horizontal_align" : "center",
					"fontname" : "Tahoma Fett:14",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
				{
					"name" : "btn_delete", "type" : "button",
					"x" : SCREEN_WIDTH / 4 + 30, "y" : SCREEN_HEIGHT - 48,
					"default_image" : BTN_PATH + "btn_delete_normal.tga",
					"over_image" : BTN_PATH + "btn_delete_hover.tga",
					"down_image" : BTN_PATH + "btn_delete_active.tga",
				},
			),
		},
	),
}
