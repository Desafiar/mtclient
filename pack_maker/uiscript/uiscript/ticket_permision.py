import localeInfo

BOARD_HEIGHT = 16
CHECKBOX_SIZE = 52
BOARD_WIDTH = 100+50+((75-CHECKBOX_SIZE)+CHECKBOX_SIZE)*3
TICKET_PATH = "d:/ymir work/ui/tickets/"

window = {
	"name" : "TicketPriority",
	
	"x" : 0,
	"y" : 0,
	
	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,
	
	"children" :
	(
		{
			"name" : "name_slot",
			"type" : "slotbar",
			
			"x" : 0,
			"y" : 0,
			
			"width" : 100,
			"height" : BOARD_HEIGHT,
			
			"children" :
			(
				{
					"name" : "name_value",
					"type" : "text",
					"all_align" : 1,
					
					"x" : 0,
					"y" : 0,
					
					"text" : localeInfo.TICKET_NAME_MEMBER,
				},
			),
		},
		{
			"name" : "delete_member",
			"type" : "button",
			"horizontal_align" : "right",
			
			"x" : 16,
			"y" : 1,
			
			"tooltip_text" : localeInfo.TICKET_DELETE_MEMBER,
			
			"default_image" : TICKET_PATH + "delete_1.tga",
			"over_image" : TICKET_PATH + "delete_2.tga",
			"down_image" : TICKET_PATH + "delete_3.tga",
		},
	),
}