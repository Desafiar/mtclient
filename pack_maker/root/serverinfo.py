import app
import localeInfo
app.ServerName = None

SRV1 = {
	"name":localeInfo.SERVERNAME,
	"host":"192.168.191.103",
	"auth1":30001,
	"ch1":30003,
	"ch2":30011,
	"ch3":30019,
	"ch4":30027,
}
SRV2 = {
	"name":localeInfo.SERVERNAMETEST,
	"host":"192.168.191.103",
	"auth1":30001,
	"ch1":30003,
	"ch2":30011,
	"ch3":30019,
	"ch4":30027,
}

STATE_NONE = "..."

STATE_DICT = {
	0 : localeInfo.CHANNEL_STATE_OFF,
	1 : localeInfo.CHANNEL_STATE_NORMAL,
	2 : localeInfo.CHANNEL_STATE_MED,
	3 : localeInfo.CHANNEL_STATE_FULL
}

SERVER1_CHANNEL_DICT = {
	1:{"key":11,"name":"CH1","ip":SRV1["host"],"tcp_port":SRV1["ch1"],"udp_port":SRV1["ch1"],"state":STATE_NONE,},
	2:{"key":12,"name":"CH2","ip":SRV1["host"],"tcp_port":SRV1["ch2"],"udp_port":SRV1["ch2"],"state":STATE_NONE,},
	3:{"key":13,"name":"CH3","ip":SRV1["host"],"tcp_port":SRV1["ch3"],"udp_port":SRV1["ch3"],"state":STATE_NONE,},
	4:{"key":14,"name":"CH4","ip":SRV1["host"],"tcp_port":SRV1["ch4"],"udp_port":SRV1["ch4"],"state":STATE_NONE,},
}

SERVER2_CHANNEL_DICT = {
	1:{"key":21,"name":"CH1","ip":SRV2["host"],"tcp_port":SRV2["ch1"],"udp_port":SRV2["ch1"],"state":STATE_NONE,},
	# 2:{"key":22,"name":"CH2","ip":SRV2["host"],"tcp_port":SRV2["ch2"],"udp_port":SRV2["ch2"],"state":STATE_NONE,},
	# 3:{"key":23,"name":"CH3","ip":SRV2["host"],"tcp_port":SRV2["ch3"],"udp_port":SRV2["ch3"],"state":STATE_NONE,},
	# 4:{"key":24,"name":"CH4 ","ip":SRV2["host"],"tcp_port":SRV2["ch4"],"udp_port":SRV2["ch4"],"state":STATE_NONE,},
}

REGION_NAME_DICT = {
	0 : SRV1["name"],
}

REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : { "ip":SRV1["host"], "port":SRV1["auth1"], },
		2 : { "ip":SRV2["host"], "port":SRV2["auth1"], },
	}
}

REGION_DICT = {
	0 : {
		1 : { "name" :SRV1["name"], "channel" : SERVER1_CHANNEL_DICT, },
		2 : { "name" :SRV2["name"], "channel" : SERVER2_CHANNEL_DICT, },
	},
}

MARKADDR_DICT = {
	10 : { "ip" : SRV1["host"], "tcp_port" : SRV1["ch1"], "mark" : "10.tga", "symbol_path" : "10", },
	20 : { "ip" : SRV2["host"], "tcp_port" : SRV2["ch1"], "mark" : "10.tga", "symbol_path" : "20", },
}

TESTADDR = { "ip" : SRV1["host"], "tcp_port" : SRV1["ch1"], "udp_port" : SRV1["ch1"], }

#DONE


