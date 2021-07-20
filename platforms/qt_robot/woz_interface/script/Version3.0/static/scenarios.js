var groupsList = [
	["static/images/scenario/end.png","QT conclue la séance"],
	["static/images/scenario/rythme3.png", "QT gère le rythme au sein de la séance"],
	["static/images/scenario/explain.png", "QT explique son scénario"],
	["static/images/scenario/start.png", "QT lance la séance"],
	["static/images/scenario/analyse.png","Analyse"],
	["static/images/scenario/helicop.png", "Jeu \"Hélicoptère\""],
	["static/images/scenario/poursuite.png", "Jeu \"Poursuite\""],
	["static/images/scenario/sousmarin.png", "Jeu \"Sous-marin\""],
	["static/images/scenario/apprenti.png","Jeu \"Apprenti\""]
]

var infoList = [
	["static/images/arrow/startarrow.png", ""],
	["static/images/arrow/jaune.png", ""],
	["static/images/arrow/scenarioarrow.png", ""],
	["static/images/arrow/vert2.png", ""],
	["static/images/arrow/twisterarrow.png", ""],
	["static/images/arrow/pressurearrow.png", ""],
	["static/images/arrow/hautplein.png", ""], // a changer
	["static/images/arrow/hautgaucheboucle.png", ""], //a changer
	["static/images/arrow/tiltarrow.png", ""]	
]

var textList = [
	["","QT conclue la séance"],
	["", "QT gère le rythme au sein de la séance"],
	["", "QT explique son scénario"],
	["", "QT lance la séance"],
	["","Analyse"],
	["", "Jeu \"Hélicoptère\""],
	["", "Jeu \"Poursuite\""],
	["", "Jeu \"Sous-marin\""],
	["","Jeu \"Apprenti\""]
]

var commandsList = [
	["#ffc3c4", [	["Dernier jeu","dernier_jeu",5],
					["C'était bien", "cetait_bien",12],
					["Tu m'aides", "tu_maide",8],
					["Tu vois mes progrès ?", "mes_progres",11],
					["Bisou","bisou",8],
					["Nous avons beaucoup travaillé", "bcp_travaille",10],
					["Il est l'heure", "il_est_lheure",10],
					["On arrête", "arrete",10],
					["Au revoir", "au_revoir",8]	]	],
	["#e0b1f9",	[	["Courte pause après un niveau?","pause",10],
					["On change de jeu?","change_jeu",8],
					["Tu choisis le jeu?","choisis_jeu",8] ]		],
	["#f5e0c4", [	["Première rencontre", "je_mappelle_qt",11],
					["Tu veux m'aider ?", "tu_veux_maider",22],
					["Tu m'aides encore ?", "tu_maides_encore",15],
					["Prépation dernier adieu","adieu",20],
					["Dernier adieu","adieu2",10]	]	],
	["#baffd2", [	["Tu viens ?", "tu_viens",10],
					["Clique sur ton nom", "ton_nom",8],
					["Ca va ?", "ca_va",4],
					["Bonjour", "bonjour",11]	]	],
	["#fdf3cc", [	["Lancement", "analyse_lance",10]	]	],
	["#f1b3b2", [	["Lancement", "tilt_lance",10],
					["Explication des règles", "tilt_expli",12],
					["Complément des règles","tilt_complet",12] 	]	],	
	["#fdeaaf", [	["Lancement", "poursuite_lance",10],
					["Explication des règles", "poursuite_expli",12],
					["Complément des règles","poursuite_complet",12]	]	],
	["#c1dbff", [	["Lancement", "pression_lance",10],
					["Explication des règles", "pression_expli",12],
					["Complément des règles","pression_complet",13]	]	],
	["#f8fdf9", [	["Lancement", "cowritter_lance",10],
					["Explication des règles","cowritter_expli_class",13],
					["Complément des règles","cowritter_complet",12]	]	]
]

// icon position
var ellipseGroupList = [
	[13.2,-5.55],
	[5,	-8.55],
	[-5, -8.25],	
	[-13.2,	-5.55],
	[-16.5,	2.8],
	[-9.9,	6.5],
	[0,	8],
	[9.9,	6.5],
	[16.5,	2.8]
]

// arrow position
var ellipseInfoList = [
	[15,-10.5],
	[7.25, -13.5],
	[-5, -13.5],
	[-17.8, -7.3],
	[-19.9, 7.0],
	[-10.0, 11.6],
	[0, 12.6],
	[12.5, 10.5],
	[21.2, 2.6]	
]

//	text position 
var ellipseTextList = [
	[19.35,-6],
	[12, -14.8],
	[-1, -12.5],
	[-15.5, -10.3],
	[-21.5, 5.0],
	[-12.0, 14.3],
	[0, 15.3],
	[18.5, 13],
	[22.2, 7]	
]

// button position
var ellipseCommandList = [
	[19.5,-8.2],
	[7.5,	-12.5],
	[-7.5,	-12.5],
	[-21,	-8.2],
	[-24,	4.7],
	[-15.5,	11],
	[0,	13],
	[15.5,	11],
	[23.5,	4.5]
]
