var groupsList = [
	["static/images/face/identemotion2.png", "QT identifie les sentiments"],	
	["static/images/face/parleadulte.png", "QT interagit avec l'adulte"],
	["static/images/face/questionne.png", "QT questionne et fait reflechir"],
	["",""],
	["static/images/face/ecrit.png", "QT écrit"],
	["static/images/face/reacjeux2.png", "QT commente les jeux"],
	["static/images/face/ouch.png", "QT bugue et est malade"],
	["static/images/face/defend2.png", "QT se défend"],
	["static/images/face/ghghgh.png", "QT encourage et réagit à un échec"],
	["static/images/face/stars.png", "QT félicite et applaudit"],
	["static/images/face/wink.png", "QT taquine et plaisante"],
	["static/images/face/happy.png", "QT papote"]
]

var infoList = [
	["static/images/arrow/bleu1.png", ""],
	["static/images/arrow/bleu2.png", ""],
	["static/images/arrow/orange.png", ""],
	["", ""], 
	["static/images/arrow/ah.png", ""],
	["static/images/arrow/vert1.png", ""],
	["static/images/arrow/rouge.png", ""],
	["static/images/arrow/vert2.png", ""],
	["static/images/arrow/peau.png", ""],
	["static/images/arrow/basgauche.png", ""], //change
	["static/images/arrow/jaune.png", ""], 
	["static/images/arrow/gaucheplume.png", ""] //change
]

var textList = [
	["", "QT identifie les sentiments"],
	["", "QT interagit avec l'adulte"],
	["", "QT questionne et fait reflechir"],
	["",""],
	["", "QT écrit"],
	["", "QT commente les jeux"],
	["", "QT bugue et est malade"],
	["", "QT se défend"],
	["", "QT encourage et réagit à un échec"],
	["", "QT félicite et applaudit"],
	["", "QT taquine et plaisante"],
	["", "QT papote"]
]

var commandsList = [
	["#95c4ff", [	["La joie", "la_joie",11],
					["L'amusement", "amusement",10],
					["La colère", "la_colere",11],
					["La motivation", "la_motivation",12],
					["La fatigue", "la_fatigue",11],
					["La tristesse", "la_tristesse",6],
					["La fierté", "la_fierte",8],
					["L'etonnement", "etonnement",11]	]	],	
	["#3dffff", [	["L'adulte est d'accord?", "adulte_accord",9],
					["Demandons à l'adulte", "demande_adulte",10],
					["Que pense l'adulte?", "que_pense",9],
					["Monsieur!", "monsieur",3],
					["Madame!", "madame",3] ]       ],
	["#b1c5fe", [	["C'est bien ?", "bien",5],
					["C'est mieux ?", "cest_mieux",10],
					["Tu m'expliques ?", "tu_mexplique",11],
					["Le plus important ?", "important",9],
					["Que fait-on ensuite ?", "ensuite",10],
					["Pourquoi ce n'est pas bien ?", "pk_pas_bien",11],
					["Tu es sur(e) ?", "tu_es_sur",11],
					["Je ne trouve pas", "je_trouve_pas",7],
					["Le plus simple pour toi?","plus_simple",5],
					["Le plus difficile pour toi?","plus_difficile",5],
					["Qu'est-ce que je fais bien et mal","bien_mal",5],
					["Pourquoi ça n'a pas marché","pas_marche",6]]	],
	["",		[	["","",0] ]		],
	["#8791a2",	[	["QT écrit","ecrit",13] ]		],
	["#ebecfb", [	["Tu triches", "triche",10],
					["C'est trop facile ?", "facile",10],
					["Pas trop vite", "pas_trop_vite",5],
					["Et boum", "boum",10]	]	],
	["#a8ebbf", [	["Tu relances ?", "tu_relances",9],
					["Je bugue", "je_bugue",6],
					["Je fatigue", "fatigue",10],
					["Je rouille", "je_rouille",10],
					["Attends", "attends",5],
					["Je suis malade", "malade",13]	]	],
	["#f7b0b6", [	["Et alors ?", "et_alors",6],
					["J'ai progressé", "jai_progresse",10],
					["C'est difficile", "cest_difficile",10],
					["Je fais des efforts", "fais_mon_mieux",10],
					["C'est bon, t'as gagné", "tas_gagne",11],
					["Ma tablette ?", "ma_tablette",10],
					["C'est pas mal", "pas_mal",10]	]	],
	["#d7fba5", [	["Respire et recommence", "respire",15],
					["J'ecris mal", "ecris_mal",6],
					["C'est pas grave", "cest_pas_grave",6],
					["Réessayons", "reessayons",9],
					["On fera mieux", "fera_mieux",7],
					["Courage", "courage",10],
					["Nous avons raté", "rate",10],
					["C'est trop difficile ?", "difficile",10],
					["Je ne suis pas content de moi","pas_content_moi",6],
					["Tu m'écoutes?","tu_mecoute",4]	]	],
	["#fff68a", [	["Bravo", "bravo",10],
					["Je suis fort", "je_suis_fort",11],
					["C'est bien", "cest_bien",10],
					["Tu as bien fait", "tu_es_fort",12],
					["On est fort", "nous_sommes_fort",10],
					["Je suis fier de toi","fier_de_toi",6]	]	],
	["#fcbc98", [	["Aie", "aie",11],
					["Ahahah", "ahahah",9],
					["J'ai des muscles en plastique", "muscle",10]	]	],
	["#f9e3c0", [	["Merci", "merci",6],
					["Comment ?", "repete",5],
					["Oui", "oui",6],
					["Non", "non",7],
					["Je sais pas, et toi?","sais_pas_toi",6],
					["Et toi?","et_toi",3]	]	]
	
]

// icon position
var ellipseGroupList = [
	[14.9, 4.2],
	[10.2, 6.5],
	[5.2, 7.6],
	[-5.2, 7.6],
	[-10.2, 6.5],
	[-14.9, 4.2],
	[-14.9,	-4.2],
	[-10.2,	-6.5],
	[-5.2, -7.6],
	[5.2, -7.6],
	[10.2, -6.5],
	[14.9, -4.2]
]

// arrow position
var ellipseInfoList = [
	[18.8, 5],
	[14, 9.5],
	[7.2, 12],
	[-7.2, 12],
	[-13, 10],
	[-19.2, 6],
	[-19.8, -6],
	[-14.8, -9.5],
	[-6.3, -12.2],
	[7.2, -11.8],
	[13.3, -10.5],
	[19.8, -6],
]

// text position
var ellipseTextList = [
	[22.3, 9.0],
	[15.3, 12.8],
	[2.4, 14.3],
	[-7.7, 11.5],
	[-15.8, 10.7],
	[-22.3, 4.3],
	[-22.5, -8.8],
	[-15.3, -11.7],
	[-0.1, -14.5],
	[8.7, -13],
	[16.6, -10.7],
	[22.3, -6.3]
]

// button position
var ellipseCommandList = [
	[22.28, 6.35],
	[15.32, 10.8],
	[6.82, 14.2],
	[-7.82, 14.2],
	[-15.32, 10.8],
	[-22.28, 6.35],
	[-22.28, -5.35],
	[-15.32, -9.8],
	[-7.82, -13.2],
	[7.82, -13.2],
	[15.32, -9.8],
	[22.28, -5.35]
]
