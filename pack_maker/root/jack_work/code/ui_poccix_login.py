BASE_PATH = "jack_work/images/login/"
BTN_PATH = BASE_PATH + "btn/"
CHANNEL_PATH = BTN_PATH + "ch/"

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
			"image" : BASE_PATH + "background.tga",
			"children" :
			(
				# ID - Field
				{
					"name" : "edit_id", "type" : "editline",
					"x" : 885, "y" : 447, "width" : 150, "height" : 16,
					"input_limit" : 24,
				},
				# PWD - Field
				{
					"name" : "edit_pwd", "type" : "editline",
					"x" : 885, "y" : 447+70, "width" : 150, "height" : 16,
					"secret_flag" : 1,
					"input_limit" : 24,
				},
				# LOGINBTN - Field
				{
					"name" : "btn_login", "type" : "button",
					"x" : 10, "y" : 580,
					"horizontal_align" : "center",
					"default_image" : BTN_PATH + "button_main.tga",
					"over_image" : BTN_PATH + "button_hover.tga",
					"down_image" : BTN_PATH + "button_down.tga",
				},
				# CHANNEL - Field
				{
					"name" : "btn_channel_01", "type" : "radio_button",
					"x" : 633, "y" : 430,
					"default_image" : CHANNEL_PATH + "ch1.tga",
					"over_image" : CHANNEL_PATH + "ch1_hover.tga",
					"down_image" : CHANNEL_PATH + "ch1_down.tga",
				},
				{
					"name" : "btn_channel_02", "type" : "radio_button",
					"x" : 633, "y" : 475,
					"default_image" : CHANNEL_PATH + "ch2.tga",
					"over_image" : CHANNEL_PATH + "ch2_hover.tga",
					"down_image" : CHANNEL_PATH + "ch2_down.tga",
				},
				{
					"name" : "btn_channel_03", "type" : "radio_button",
					"x" : 633, "y" : 520,
					"default_image" : CHANNEL_PATH + "ch3.tga",
					"over_image" : CHANNEL_PATH + "ch3_hover.tga",
					"down_image" : CHANNEL_PATH + "ch3_down.tga",
				},
				{
					"name" : "btn_channel_04", "type" : "radio_button",
					"x" : 633, "y" : 565,
					"default_image" : CHANNEL_PATH + "ch4.tga",
					"over_image" : CHANNEL_PATH + "ch4_hover.tga",
					"down_image" : CHANNEL_PATH + "ch4_down.tga",
				},
				# ACCOUNTDELETE - Field
				{
					"name" : "btn_delete_01", "type" : "button",
					"default_image" : BTN_PATH + "delete.tga",
					"x" : 1278, "y" : 424,
					"over_image" : BTN_PATH + "delete.tga",
					"down_image" : BTN_PATH + "delete.tga",
				},
				{
					"name" : "btn_delete_02", "type" : "button",
					"x" : 1278, "y" : 465,
					"default_image" : BTN_PATH + "delete.tga",
					"over_image" : BTN_PATH + "delete.tga",
					"down_image" : BTN_PATH + "delete.tga",
				},
				{
					"name" : "btn_delete_03", "type" : "button",
					"x" : 1278, "y" : 508,
					"default_image" : BTN_PATH + "delete.tga",
					"over_image" : BTN_PATH + "delete.tga",
					"down_image" : BTN_PATH + "delete.tga",
				},
				{
					"name" : "btn_delete_04", "type" : "button",
					"x" : 1278, "y" : 549,
					"default_image" : BTN_PATH + "delete.tga",
					"over_image" : BTN_PATH + "delete.tga",
					"down_image" : BTN_PATH + "delete.tga",
				},
				{
					"name" : "btn_delete_05", "type" : "button",
					"x" : 1278, "y" : 595,
					"default_image" : BTN_PATH + "delete.tga",
					"over_image" : BTN_PATH + "delete.tga",
					"down_image" : BTN_PATH + "delete.tga",
				},
				# ACCOUNTADD - Field
				{
					"name" : "btn_add_01", "type" : "button",
					"x" : 1263, "y" : 424,
					"default_image" : BTN_PATH + "shape.tga",
					"over_image" : BTN_PATH + "shape.tga",
					"down_image" : BTN_PATH + "shape.tga",
				},
				{
					"name" : "btn_add_02", "type" : "button",
					"x" : 1263, "y" : 465,
					"default_image" : BTN_PATH + "shape.tga",
					"over_image" : BTN_PATH + "shape.tga",
					"down_image" : BTN_PATH + "shape.tga",
				},
				{
					"name" : "btn_add_03", "type" : "button",
					"x" : 1263, "y" : 508,
					"default_image" : BTN_PATH + "shape.tga",
					"over_image" : BTN_PATH + "shape.tga",
					"down_image" : BTN_PATH + "shape.tga",
				},
				{
					"name" : "btn_add_04", "type" : "button",
					"x" : 1263, "y" : 549,
					"default_image" : BTN_PATH + "shape.tga",
					"over_image" : BTN_PATH + "shape.tga",
					"down_image" : BTN_PATH + "shape.tga",
				},
				{
					"name" : "btn_add_05", "type" : "button",
					"x" : 1263, "y" : 595,
					"default_image" : BTN_PATH + "shape.tga",
					"over_image" : BTN_PATH + "shape.tga",
					"down_image" : BTN_PATH + "shape.tga",
				},
				# ACCOUNTSELECT - Field
				{
					"name" : "text_account_01", "type" : "text",
					"x" : 1155, "y" : 424,
					"text" : "#01 - " + "Freier Slot",
				},
				{
					"name" : "btn_select_01", "type" : "button",
					"x" : 1115, "y" : 422,
					"default_image" : BTN_PATH + "btn_select_blank.tga",
					"over_image" : BTN_PATH + "btn_select.tga",
					"down_image" : BTN_PATH + "btn_select.tga",
				},
				{
					"name" : "text_account_02", "type" : "text",
					"x" : 1155, "y" : 465,
					"text" : "#02 - " + "Freier Slot",
				},
				{
					"name" : "btn_select_02", "type" : "button",
					"x" : 1115, "y" : 463,
					"default_image" : BTN_PATH + "btn_select_blank.tga",
					"over_image" : BTN_PATH + "btn_select.tga",
					"down_image" : BTN_PATH + "btn_select.tga",
				},
				{
					"name" : "text_account_03", "type" : "text",
					"x" : 1155, "y" : 508,
					"text" : "#03 - " + "Freier Slot",
				},
				{
					"name" : "btn_select_03", "type" : "button",
					"x" : 1115, "y" : 506,
					"default_image" : BTN_PATH + "btn_select_blank.tga",
					"over_image" : BTN_PATH + "btn_select.tga",
					"down_image" : BTN_PATH + "btn_select.tga",
				},
				{
					"name" : "text_account_04", "type" : "text",
					"x" : 1155, "y" : 549,
					"text" : "#04 - " + "Freier Slot",
				},
				{
					"name" : "btn_select_04", "type" : "button",
					"x" : 1115, "y" : 547,
					"default_image" : BTN_PATH + "btn_select_blank.tga",
					"over_image" : BTN_PATH + "btn_select.tga",
					"down_image" : BTN_PATH + "btn_select.tga",
				},
				{
					"name" : "text_account_05", "type" : "text",
					"x" : 1155, "y" : 595,
					"text" : "#05 - " + "Freier Slot",
				},
				{
					"name" : "btn_select_05", "type" : "button",
					"x" : 1115, "y" : 593,
					"default_image" : BTN_PATH + "btn_select_blank.tga",
					"over_image" : BTN_PATH + "btn_select.tga",
					"down_image" : BTN_PATH + "btn_select.tga",
				},
			),
		},
	),
}