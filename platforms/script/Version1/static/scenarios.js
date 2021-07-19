var groupsList = [
	["static/images/scenario/end.png", "QT conclue la séance"],
	["static/images/scenario/explain.png", "QT explique son scénario"],
	["static/images/scenario/start.png", "QT lance la séance"],
	["static/images/scenario/analyse.png","Analyse"],
	["static/images/scenario/tilt.png", "Jeu \"Tilt\""],
	["static/images/scenario/chase.png", "Jeu \"Poursuite\""],
	["static/images/scenario/pressure.png", "Jeu \"Pression\""],
	["static/images/scenario/twister.png", "Jeu \"Twister\""],
	["static/images/scenario/cowritter.png","Jeu \"Cowritter\""]
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
	["", "Jeu \"Tilt\""],
	["", "Jeu \"Poursuite\""],
	["", "Jeu \"Pression\""],
	["", "Jeu \"Twister\""],
	["","Jeu \"Cowritter\""]
]

var commandsList = [
	["#ffc3c4", [	["C'était bien", "cetait_bien"],
					["Tu m'aides", "tu_maide"],
					["Tu vois mes progrès ?", "mes_progres"],
					["On essaye après", "on_essaye"],
					["Nous avons beaucoup travaillé", "bcp_travaille"],
					["Il est l'heure", "il_est_lheure"],
					["On arrête", "arrete"]	]	],
	["#f5e0c4", [	["Je m'appelle QT", "je_mappelle_qt"],
					["Tu veux m'aider ?", "tu_veux_maider"],
					["Tu m'aides encore ?", "tu_maides_encore"]	]	],
	["#baffd2", [	["Tu viens ?", "tu_viens"],
					["Clique sur ton nom", "ton_nom"]	]	],
	["#fdeaaf", [	["Lancement", "analyse_lance"]	]	],
	["#f1b3b2", [	["Lancement", "tilt_lance"],
					["Explication des règles", "tilt_expli"]	]	],	
	["#c1dbff", [	["Lancement", "poursuite_lance"],
					["Explication des règles", "poursuite_expli"]	]	],
	["#fdf3cc", [	["Lancement", "pression_lance"],
					["Explication des règles", "pression_expli"]	]	],
	["#fccbad", [	["Lancement", "twister_lance"],
					["Explication des règles", "twister_expli"]	]	],
	["#f8fdf9", [	["Lancement", "cowritter_lance"],
					["Explication des règles", "cowritter_expli"]	]	]
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
