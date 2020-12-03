var groupsList = [
	["static/images/scenario/tilt.png", "Jeu \"Tilt\""],
	["static/images/scenario/chase.png", "Jeu \"Poursuite\""],
	["static/images/scenario/pressure.png", "Jeu \"Pression\""],
	["static/images/empty.png", "Jeu \"Twister\""],
	["static/images/scenario/comment.png", "QT commente le jeu"],
	["static/images/scenario/end.png", "QT conclue la séance"],
	["static/images/scenario/explain.png", "QT explique son scénario"],
	["static/images/scenario/start.png", "QT lance la séance"]
]

var infoList = [
	["static/images/arrow/tiltarrow.png", ""],
	["static/images/arrow/poursuitearrow.png", ""],
	["static/images/arrow/pressurearrow.png", ""],
	["static/images/arrow/twisterarrow.png", ""],
	["static/images/arrow/scribble-1.png", ""],
	["static/images/arrow/vert2.png", ""],
	["static/images/arrow/scenarioarrow.png", ""],
	["static/images/arrow/startarrow.png", ""]
]

var textList = [
	["", "Jeu \"Tilt\""],
	["", "Jeu \"Poursuite\""],
	["", "Jeu \"Pression\""],
	["", "Jeu \"Twister\""],
	["", "QT commente le jeu"],
	["", "QT conclue la séance"],
	["", "QT explique son scénario"],
	["", "QT lance la séance"]
]

var commandsList = [
	["#f1b3b2", [	["Lancement", "tilt_lance"],
					["Explication des règles", "tilt_expli"]	]	],	
	["#c1dbff", [	["Lancement", "poursuite_lance"],
					["Explication des règles", "poursuite_expli"]	]	],
	["#fdf3cc", [	["Lancement", "pression_lance"],
					["Explication des règles", "pression_expli"]	]	],
	["#dddddd", [	["Lancement", "twister_lance"],
					["Explication des règles", "twister_expli"]	]	],
	["#ebecfb", [	["Tu triches", "triche"],
					["C'est trop facile ?", "facile"],
					["C'est trop difficile ?", "difficile"],
					["Pas trop vite", "pas_trop_vite"],
					["Et boum", "boum"]	]	],
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
					["Clique sur ton nom", "ton_nom"]	]	]
]
