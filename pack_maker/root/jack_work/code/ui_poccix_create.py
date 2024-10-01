BASE_PATH = "jack_work/images/create/"
BTN_PATH = BASE_PATH + "btn/"

height = 0
if SCREEN_HEIGHT <= 1000:
	height = -120

window = {
	"name" : "CreateCharacterWindow",
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
			"name" : "character_render_window", "type" : "window",
			"x" : SCREEN_WIDTH / 2, "y" : 0,
			"width" : SCREEN_WIDTH / 2, "height" : SCREEN_HEIGHT,
			"children" : (
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
			),
		},
		{
			"name" : "content_create", "type" : "image",
			"x" : SCREEN_WIDTH / 4 - 360 / 2, "y" : SCREEN_HEIGHT / 2 - 520 / 2,
			"image" : BASE_PATH + "content.tga",
			"children" :
			(
				{
					"name" : "btn_shape_01", "type" : "radio_button",
					"x" : 107, "y" : 397,
					"default_image" : BTN_PATH + "btn_shape_01_normal.tga",
					"over_image" : BTN_PATH + "btn_shape_01_hover.tga",
					"down_image" : BTN_PATH + "btn_shape_01_active.tga",
				},
				{
					"name" : "btn_shape_02", "type" : "radio_button",
					"x" : 107+49, "y" : 397,
					"default_image" : BTN_PATH + "btn_shape_02_normal.tga",
					"over_image" : BTN_PATH + "btn_shape_02_hover.tga",
					"down_image" : BTN_PATH + "btn_shape_02_active.tga",
				},
				{
					"name" : "btn_gender_01", "type" : "radio_button",
					"x" : 224, "y" : 397,
					"default_image" : BTN_PATH + "btn_female_normal.tga",
					"over_image" : BTN_PATH + "btn_female_hover.tga",
					"down_image" : BTN_PATH + "btn_female_active.tga",
				},
				{
					"name" : "btn_gender_02", "type" : "radio_button",
					"x" : 224+49, "y" : 397,
					"default_image" : BTN_PATH + "btn_male_normal.tga",
					"over_image" : BTN_PATH + "btn_male_hover.tga",
					"down_image" : BTN_PATH + "btn_male_active.tga",
				},
				# NAME - Field
				{
					"name" : "edit_name", "type" : "editline",
					"x" : 116, "y" : 461, "width" : 200, "height" : 16,
					"input_limit" : 24,
					"text" : "",
				},
				{
					"name" : "text_desc_01", "type" : "text",
					"x" : 208, "y" : 218,
					"text_horizontal_align" : "center",
					"fontname" : "Tahoma:14",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
				{
					"name" : "text_desc_02", "type" : "text",
					"x" : 208, "y" : 218+18*1,
					"text_horizontal_align" : "center",
					"fontname" : "Tahoma:14",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
				{
					"name" : "text_desc_03", "type" : "text",
					"x" : 208, "y" : 218+18*2,
					"text_horizontal_align" : "center",
					"fontname" : "Tahoma:14",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
				{
					"name" : "text_desc_04", "type" : "text",
					"x" : 208, "y" : 218+18*3,
					"text_horizontal_align" : "center",
					"fontname" : "Tahoma:14",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
				{
					"name" : "text_desc_05", "type" : "text",
					"x" : 208, "y" : 218+18*4,
					"text_horizontal_align" : "center",
					"fontname" : "Tahoma:14",
					"color" : 0xffCECECE,
					"text" : "DEFAULT_TEXT",
				},
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
	),
}
