var groupsList = [
	["static/images/scenario/g2465.png","Jeux \"Sous-marin\" et \"Archéologue\""],//à modifier
	["static/images/scenario/drapeau.png","Jeux \"Drapeaux\" et \"Alphabet\""],//à modifier
	["static/images/scenario/zoo.png","Jeu \"Zoo\""],
	["static/images/scenario/chim3.png","Jeu \"Chimiste\""],
	["static/images/scenario/copter.png", "Jeu \"Hélicoptère\""],
	["static/images/scenario/apprenti.png","Jeu \"Apprenti\""],
	["static/images/scenario/g2270.png", "Jeu \"Jus\""],//à modifier
	["static/images/scenario/mongolf.png", "Jeu \"Poursuite\""],
	["static/images/scenario/start.png", "QT lance la séance"],
	["static/images/scenario/explain.png", "QT explique son scénario"],
	["static/images/scenario/rythme3.png", "QT gère le rythme au sein de la séance"],
	["static/images/scenario/end.png","QT conclue la séance"]
]

var infoList = [
	["static/images/arrow/startarrow.png", ""],	
	["static/images/arrow/tiltarrow.png", ""],
	["static/images/arrow/hautgaucheboucle.png", ""],
	["static/images/arrow/hautplein.png", ""],
	["static/images/arrow/pressurearrow.png", ""],
	["static/images/arrow/ghghgh.png", ""],
	["static/images/arrow/twisterarrow.png", ""],
	["static/images/arrow/vert1.png", ""],
	["static/images/arrow/scribble-1.png", ""],
	["static/images/arrow/rouge.png", ""],
	["static/images/arrow/basgauche.png", ""],
	["static/images/arrow/jaune.png", ""]
]

var textList = [
	["","Jeux \"Sous-marin\" et \"Archéologue\""],
	["","Jeux \"Drapeaux\" et \"Alphabet\""],
	["", "Jeu \"Zoo\""],
	["", "Jeu \"Chimiste\""],
	["", "Jeu \"Hélicoptère\""],
	["","Jeu \"Apprenti\""],
	["", "Jeu \"Jus\""],
	["","Jeu \"Poursuite\""],
	["", "QT lance la séance"],
	["", "QT explique son scénario"],
	["", "QT gère le rythme au sein de la séance"],
	["","QT conclue la séance"]
]

var commandsList = [
	["#3AB8DD", [	["Sous-marin: Lancement", "pression_lance",10],
					["Sous-marin: Explication des règles", "pression_expli",12],
					["Sous-marin: Complément des règles","pression_complet",13],
					["Archéologue: Lancement", "archeo_lance",10],
					["Archéologue: Explication des règles","archeo_expli",13],
					["Archéologue: Complément des règles","archeo_complet",12]	]	],
	["#F2838C", [	["Drapeaux: Lancement", "drapeau_lance",10],
					["Drapeaux: Explication des règles","drapeau_expli",13],
					["Drapeaux: Complément des règles","drapeau_complet",12],
					["Alphabet: Lancement", "alpha_lance",10],
					["Alphabet: Explication des règles", "alpha_expli",12],
					["Alphabet: Complément des règles","alpha_complet",13]]	],
	["#C7AAFE", [	["Lancement", "zoo_lance",10],
					["Explication des règles","zoo_expli",13],
					["Complément des règles","zoo_complet",12]	]	],
	["#C4FB6F", [	["Lancement","chimi_lance",10],
					["Explication","chimi_expli",12]	]	],
	["#FCB4DA", [	["Lancement", "tilt_lance",10],
					["Explication des règles", "tilt_expli",12],
					["Complément des règles","tilt_complet",12]	]	],
	["#FEE977", [	["Lancement", "cowritter_lance",10],
					["Explication des règles","cowritter_expli_class",13],
					["Complément des règles","cowritter_complet",12]	]	],
	["#ABEDFD", [	["Lancement", "jus_lance",10],//à modifier
					["Explication des règles", "jus_expli",12], //à modifier
					["Complément des règles","jus_complet",15]	]	],//à modifier
	["#FEC772", [	["Lancement", "poursuite_lance",10],
					["Explication des règles", "poursuite_expli",12],
					["Complément des règles","poursuite_complet",12]	]	],
	["#74FFA4", [	["Tu viens ?", "tu_viens",10],
					["Clique sur ton nom", "ton_nom",8],
					["Ca va ?", "ca_va",4],
					["Bonjour", "bonjour",11]	]	],
	["#F0CFA6", [	["Première rencontre", "je_mappelle_qt",11],
					["Tu veux m'aider ?", "tu_veux_maider",22],
					["Tu m'aides encore ?", "tu_maides_encore",15],
					["Prépation dernier adieu","adieu",20],
					["Dernier adieu","adieu2",10]	]	],
	["#DEC7FF",	[	["Courte pause après un niveau?","pause",10],
					["On change de jeu?","change_jeu",8],
					["Tu choisis le jeu?","choisis_jeu",8] ]		],
	["#FF9FA0", [	["Dernier jeu","dernier_jeu",5],
					["C'était bien", "cetait_bien",12],
					["Tu m'aides", "tu_maide",8],
					["Tu vois mes progrès ?", "mes_progres",11],
					["Bisou","bisou",8],
					["Nous avons beaucoup travaillé", "bcp_travaille",10],
					["Il est l'heure", "il_est_lheure",10],
					["On arrête", "arrete",10],
					["Au revoir", "au_revoir",8]	]	]
]

// icon position
var ellipseGroupList = [
	[15.5,	-4.2],
	[17,	2.3],
	[11,	6],
	[4, 8],
	[-3.5, 8],
	[-10.5,	6],
	[-16.5,	2.5],
	[-15,-4],
	[-8.2,	-7.8],
	[-2.6, -8.55],	
	[3.5,	-8.55],
	[9.2,-7.8]
]

// arrow position
var ellipseInfoList = [
	[17.5,	-8.5],
	[21.5,	2.3],
	[12,10],
	[4.4, 12.6],
	[-3, 12.5],
	[-13, 10.6],	
	[-19.5, 6.6],
	[-19.9, -3.0],
	[-12.8, -9.3],
	[-5, -13.5],
	[5, -13.5],
	[11.5,-12.5]
]

//	text position 
var ellipseTextList = [
	[23.5,-4.5],	
	[22.2, 7],
	[16.5, 13],
	[4.5, 15.3],
	[-7.5, 15.3],
	[-18.5, 12.3],
	[-25,4.5],
	[-26.5, -3.0],
	[-19.5, -10.5],
	[-11, -15.5],
	[8, -15.5],
	[18.5,-11.5]
]

// button position
var ellipseCommandList = [
	[25.16,-3.54],
	[25.16,3.54],
	[17.73,10.24],
	[6.33,13.57],
	[-6.33,13.57],
	[-17.73,11.24],
	[-25.16,3.54],
	[-25.16,-3.54],
	[-17.73,-10.24],
	[-6.33,-13.57],	
	[6.33,-13.57],
	[17.73,-10.24]
]
