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
	["#95c4ff", [	["La joie", "la_joie"],
					["L'amusement", "amusement"],
					["La colère", "la_colere"],
					["La motivation", "la_motivation"],
					["La fatigue", "la_fatigue"],
					["La tristesse", "la_tristesse"],
					["La fierté", "la_fierte"],
					["L'etonnement", "etonnement"]	]	],	
	["#3dffff", [	["L'adulte est d'accord?", "adulte_accord"],
					["Demandons à l'adulte", "demande_adulte"],
					["Que pense l'adulte?", "que_pense"],
					["Monsieur!", "monsieur"],
					["Madame!", "madame"] ]       ],
	["#b1c5fe", [	["C'est bien ?", "bien"],
					["C'est mieux ?", "cest_mieux"],
					["Tu m'expliques ?", "tu_mexplique"],
					["Le plus important ?", "important"],
					["Que fait-on ensuite ?", "ensuite"],
					["Pourquoi ce n'est pas bien ?", "pk_pas_bien"],
					["Tu es sur(e) ?", "tu_es_sur"],
					["Je ne trouve pas", "je_trouve_pas"],
					["Le plus simple?","plus_simple"],
					["Le plus difficile?","plus_difficile"]]	],
	["",		[	["",""] ]		],
	["#8791a2",	[	["QT écrire","ecrit"] ]		],
	["#ebecfb", [	["Tu triches", "triche"],
					["C'est trop facile ?", "facile"],
					["C'est trop difficile ?", "difficile"],
					["Pas trop vite", "pas_trop_vite"],
					["Et boum", "boum"]	]	],
	["#a8ebbf", [	["Tu relances ?", "tu_relances"],
					["Je bugue", "je_bugue"],
					["Je fatigue", "fatigue"],
					["Je rouille", "je_rouille"],
					["Attends", "attends"],
					["Je suis malade", "malade"]	]	],
	["#f7b0b6", [	["Et alors ?", "et_alors"],
					["J'ai progressé", "jai_progresse"],
					["C'est difficile", "cest_difficile"],
					["Je fais des efforts", "fais_mon_mieux"],
					["Tu as gagné", "tas_gagne"],
					["Ma tablette ?", "ma_tablette"],
					["C'est pas mal", "pas_mal"]	]	],
	["#d7fba5", [	["Respire et recommence", "respire"],
					["J'ecris mal", "ecris_mal"],
					["C'est pas grave", "cest_pas_grave"],
					["Réessayons", "reessayons"],
					["On fera mieux", "fera_mieux"],
					["Courage", "courage"],
					["Nous avons raté", "rate"],
					["Je ne suis pas content de moi","pas_content_moi"]	]	],
	["#fff68a", [	["Bravo", "bravo"],
					["Je suis fort", "je_suis_fort"],
					["C'est bien", "cest_bien"],
					["Tu as bien fait", "tu_es_fort"],
					["On est fort", "nous_sommes_fort"]	]	],
	["#fcbc98", [	["Aie", "aie"],
					["Ahahah", "ahahah"],
					["J'ai des muscles en plastique", "muscle"]	]	],
	["#f9e3c0", [	["Ca va ?", "ca_va"],
					["Bonjour", "bonjour"],
					["Au revoir", "au_revoir"],
					["Merci", "merci"],
					["Comment ?", "repete"],
					["Oui", "oui"],
					["Non", "non"]	]	]
	
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
