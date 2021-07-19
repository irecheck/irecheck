var groupsList = [
	["static/images/scenario/end.png", "QT conclue la séance"],
	["static/images/scenario/explain.png", "QT explique son scénario"],
	["static/images/scenario/start.png", "QT lance la séance"],
	["static/images/scenario/analyse.png","Analyse"],
	["static/images/scenario/tilt.png", "Jeu \"Hélicoptère\""],
	["static/images/scenario/chase.png", "Jeu \"Poursuite\""],
	["static/images/scenario/pressure.png", "Jeu \"Sous-marin\""],
	["static/images/scenario/twister.png", "Jeu \"Twister\""],
	["static/images/scenario/cowritter.png","Jeu \"Apprenti\""]
]

var infoList = [
	["static/images/arrow/startarrow.png", ""],
	["static/images/arrow/scenarioarrow.png", ""],
	["static/images/arrow/vert2.png", ""],
	["static/images/arrow/twisterarrow.png", ""],
	["static/images/arrow/pressurearrow.png", ""],
	["static/images/arrow/hautplein.png", ""], // a changer
	["static/images/arrow/hautgaucheboucle.png", ""], //a changer
	["static/images/arrow/poursuitearrow.png", ""],
	["static/images/arrow/tiltarrow.png", ""]	
]

var textList = [
	["", "QT conclue la séance"],
	["", "QT explique son scénario"],
	["", "QT lance la séance"],
	["","Analyse"],
	["", "Jeu \"Hélicoptère\""],
	["", "Jeu \"Poursuite\""],
	["", "Jeu \"Sous-marin\""],
	["", "Jeu \"Twister\""],
	["","Jeu \"Apprenti\""]
]

var commandsList = [
	["#ffc3c4", [	["Dernier jeu","dernier_jeu",5],
					["C'était bien", "cetait_bien",12],
					["Tu m'aides", "tu_maide",8],
					["Tu vois mes progrès ?", "mes_progres",11],
					["On essaye après", "on_essaye",8],
					["Nous avons beaucoup travaillé", "bcp_travaille",10],
					["Il est l'heure", "il_est_lheure",10],
					["On arrête", "arrete",10],
					["Au revoir", "au_revoir",8]	]	],
	["#f5e0c4", [	["Je m'appelle QT", "je_mappelle_qt",11],
					["Tu veux m'aider ?", "tu_veux_maider",22],
					["Tu m'aides encore ?", "tu_maides_encore",15]	]	],
	["#baffd2", [	["Tu viens ?", "tu_viens",10],
					["Clique sur ton nom", "ton_nom",8],
					["Ca va ?", "ca_va",4],
					["Bonjour", "bonjour",11]	]	],
	["#fdeaaf", [	["Lancement", "analyse_lance",10]	]	],
	["#f1b3b2", [	["Lancement", "tilt_lance",10],
					["Explication des règles", "tilt_expli",12]	]	],	
	["#c1dbff", [	["Lancement", "poursuite_lance",10],
					["Explication des règles", "poursuite_expli",12]	]	],
	["#fdf3cc", [	["Lancement", "pression_lance",10],
					["Explication des règles", "pression_expli",12]	]	],
	["#fccbad", [	]	],
	["#f8fdf9", [	["Lancement", "cowritter_lance",10],
					["Explication des règles","cowritter_expli_class",13]	]	]
]

// icon position
var ellipseGroupList = [
	[9.9,	-7],
	[0, -8.5],	
	[-9.9,	-7],
	[-16.5,	2.8],
	[-10.2,	6.4],
	[-3.6,	8],
	[3.6,	8],
	[10.2,	6.4],
	[16.5,	2.8]
]

// arrow position
var ellipseInfoList = [
	[12.0, -11.5],
	[-0.2, -13.2],
	[-14.5, -8.3],
	[-19.9, 7.0],
	[-10.0, 10.6],
	[-3.0, 12.6],
	[7.5, 10.5],
	[14.5, 8.5],
	[21.2, 2.6]	
]

//	text position 
var ellipseTextList = [
	[17.0, -7.5],
	[4.3, -13],
	[-13.5, -12.3],
	[-21.5, 5.0],
	[-12.0, 13.3],
	[-4.0, 14.8],
	[7.5, 14.5],
	[15.5, 12.5],
	[22.2, 6.6]	
]

// button position
var ellipseCommandList = [
	[17.4,	-7.9],
	[0,	-11.2],
	[-17.4,	-7.8],
	[-24,	3.7],
	[-17.5,	8.5],
	[-5.2,	12.5],
	[5.2,	12.5],
	[15.5,	11],
	[23.5,	3.5]
]
