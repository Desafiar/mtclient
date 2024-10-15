import localeInfo

WINDOW_WIDTH = 405
WINDOW_HEIGHT = 114

IMG_DIR_AVATAR = "d:/ymir work/ui/game/track/avatar/"
IMG_DIR = "d:/ymir work/ui/game/track/ymirdesign/"

window = {
	"name" : "TrackWindow",
	"x" : 0,
	"y" : 0,
	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,
	"children" :
	(
		{
			"name" : "board",
			"type" : "expanded_image",
			"x" : 0,
			"y" : 0,
			"image" : IMG_DIR+"dungeon_closed.tga",
			"children" :
			(
				{"name" : "avatar","type" : "expanded_image","x" : 5,"y" : 5,"image":IMG_DIR_AVATAR+"alastor.tga",},
				{"name" : "name_field","type" : "text","x" : 123,"y" : 19,"text":"","color":0xFFFFAF00,},
				{"name" : "level_field","type" : "text","x" : 123,"y" : 19 + (1*18) ,"text":"",},
				{"name" : "group_field","type" : "text","x" : 123,"y" : 19 + (2*18) ,"text":"",},
				{"name" : "cooldown_field","type" : "text","x" : 123,"y" : 19 + (3*18) ,"text":"",},
				{"name" : "status_field","type" : "text","x" : 123,"y" : 19 + (4*18) ,"text":"",},
				{
					"name" : "teleport_button",
					"type" : "button",
					"x" : WINDOW_WIDTH-114,
					"y" : WINDOW_HEIGHT-35,
					"default_image" : IMG_DIR+"button_0.tga",
					"over_image" : IMG_DIR+"button_1.tga",
					"down_image" : IMG_DIR+"button_2.tga",
					"children" :
					(
						{"name" : "dungeon_key","type" : "text","x" : 49,"y" : -60,"text_horizontal_align": "center","text":localeInfo.TRACK_DUNGEON_KEY,},
						{"name" : "teleport_button_text","type" : "text","x" : 0,"y" : 0,"all_align": 1,"text": localeInfo.TRACK_TELEPORT,},
					),
				},

				{
					"name" :"itemwall0",
					"type" : "expanded_image",
					"x" : (WINDOW_WIDTH-114)+49,
					"y" : 40,
					"image":IMG_DIR+"item_slot.tga",
					"children":(
						{
							"name" :"item0","type" : "expanded_image","x" : 0,"y" : 0,"image":"icon/item/70068.tga",
							"children" :({ "name" : "itemcount0","type" : "text","x" : 10,"y" : 10,"all_align": 1,"text":"1","style" : ("not_pick",),},),
						},
					),
				},
				{
					"name" :"itemwall1",
					"type" : "expanded_image",
					"x" : (WINDOW_WIDTH-114)+49,
					"y" : 40,
					"image":IMG_DIR+"item_slot.tga",
					"children":(
						{
							"name" :"item1","type" : "expanded_image","x" : 0,"y" : 0,"image":"icon/item/70068.tga",
							"children" :({ "name" : "itemcount1","type" : "text","x" : 10,"y" : 10,"all_align": 1,"text":"1","style" : ("not_pick",),},),
						},
					),
				},
				{
					"name" :"itemwall2",
					"type" : "expanded_image",
					"x" : (WINDOW_WIDTH-114)+49,
					"y" : 40,
					"image":IMG_DIR+"item_slot.tga",
					"children":(
						{
							"name" :"item2","type" : "expanded_image","x" : 0,"y" : 0,"image":"icon/item/70068.tga",
							"children" :({ "name" : "itemcount2","type" : "text","x" : 10,"y" : 10,"all_align": 1,"text":"1","style" : ("not_pick",),},),
						},
					),
				}
			),
		},
	),
}
