"""
Phase C3 — High Empire (Trajan→Severans) + Crisis of the 3rd century +
Late Empire (Diocletian→Theodosius) + Byzantine empire through 1453.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_ROMAN = {"europe": 10, "americas": 1, "asia": 3, "australasia": 1, "africa": 4}
RW_EURO_ASIA = {"europe": 10, "americas": 1, "asia": 8, "australasia": 1, "africa": 3}
RW_BYZ = {"europe": 9, "americas": 1, "asia": 9, "australasia": 1, "africa": 4}


def m(master_pri: int, rh_pri: int, **extra) -> dict:
    out = {"master": master_pri, "roman-history": rh_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- High Empire -----
    {"type": "event", "title": "Reign of Trajan",
     "description": "Optimus Princeps; expands the empire to its greatest territorial extent with conquest of Dacia and Mesopotamia.",
     "start_year": 98, "end_year": 117, "start_month": 1, "start_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Trajan",
     "priorities": m(860_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Dacian Wars",
     "description": "Trajan's two campaigns subjugate the kingdom of Decebalus; Dacia becomes a Roman province and a gold-rich frontier.",
     "start_year": 101, "end_year": 106,
     "wikipedia": "https://en.wikipedia.org/wiki/Trajan%27s_Dacian_Wars",
     "priorities": m(820_000, 880_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Trajan's Column erected",
     "description": "Marble column in Trajan's Forum carved with a continuous spiral relief of the Dacian Wars; ~190 ft tall.",
     "start_year": 113, "start_month": 5, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Trajan%27s_Column",
     "priorities": m(810_000, 850_000, **{"arts-and-thoughts": 860_000}),
     "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Hadrian",
     "description": "Adoptive successor of Trajan; consolidates frontiers, builds Hadrian's Wall, travels the entire empire.",
     "start_year": 117, "end_year": 138, "start_month": 8, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Hadrian",
     "priorities": m(860_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Hadrian's Wall begun",
     "description": "Construction of the 73-mile fortified frontier across northern Britannia, manned for nearly three centuries.",
     "start_year": 122, "end_year": 128,
     "wikipedia": "https://en.wikipedia.org/wiki/Hadrian%27s_Wall",
     "priorities": m(850_000, 880_000, england=900_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Bar Kokhba revolt",
     "description": "Last great Jewish revolt against Rome under Hadrian; ends in devastation of Judea and renaming to Syria Palaestina.",
     "start_year": 132, "end_year": 136,
     "wikipedia": "https://en.wikipedia.org/wiki/Bar_Kokhba_revolt",
     "priorities": m(820_000, 870_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Pantheon (Hadrian) completed",
     "description": "Concrete-domed temple-to-all-gods in Rome, completed under Hadrian; world's largest unreinforced concrete dome.",
     "start_year": 128, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pantheon,_Rome",
     "priorities": m(880_000, 900_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Antoninus Pius",
     "description": "Quiet, prosperous 23-year reign at the empire's apogee; namesake of the Antonine dynasty.",
     "start_year": 138, "end_year": 161, "start_month": 7, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Antoninus_Pius",
     "priorities": m(810_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "person", "title": "Marcus Aurelius",
     "description": "Stoic philosopher-emperor; co-emperor with Lucius Verus; spent most of his reign fighting Marcomanni on the Danube.",
     "start_year": 121, "end_year": 180, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Marcus_Aurelius",
     "priorities": m(900_000, 940_000, people=950_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Marcus Aurelius",
     "description": "Philosopher-emperor; defends the Danube against Marcomanni and Sarmatians; writes the Meditations.",
     "start_year": 161, "end_year": 180, "start_month": 3, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Marcus_Aurelius",
     "priorities": m(860_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Antonine Plague",
     "description": "Smallpox pandemic carried back by Roman armies from the east; kills millions and weakens the high imperial economy.",
     "start_year": 165, "end_year": 180, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Antonine_Plague",
     "priorities": m(830_000, 880_000), "region_weights": RW_ROMAN},

    {"type": "art", "title": "Meditations of Marcus Aurelius",
     "description": "Personal Stoic notebooks written by Marcus Aurelius during the Marcomannic Wars; classic of philosophy.",
     "start_year": 175, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Meditations",
     "priorities": m(850_000, 890_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Commodus",
     "description": "Marcus Aurelius's son ends the Five Good Emperors; capricious gladiator-emperor strangled by his wrestling partner.",
     "start_year": 180, "end_year": 192, "start_month": 3, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Commodus",
     "priorities": m(820_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Year of the Five Emperors",
     "description": "Year of civil war between Pertinax, Didius Julianus, Pescennius Niger, Clodius Albinus, and Septimius Severus.",
     "start_year": 193,
     "wikipedia": "https://en.wikipedia.org/wiki/Year_of_the_Five_Emperors",
     "priorities": m(810_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Septimius Severus",
     "description": "African-born general who founds the Severan dynasty; militarises the empire and dies in Britain at Eboracum.",
     "start_year": 193, "end_year": 211, "start_month": 4, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Septimius_Severus",
     "priorities": m(820_000, 870_000, england=830_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Constitutio Antoniniana",
     "description": "Edict of Caracalla extends Roman citizenship to every free inhabitant of the empire; transforms identity and law.",
     "start_year": 212,
     "wikipedia": "https://en.wikipedia.org/wiki/Constitutio_Antoniniana",
     "priorities": m(860_000, 910_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "End of the Severan dynasty",
     "description": "Murder of Severus Alexander on the Rhine plunges the empire into 50 years of crisis.",
     "start_year": 235, "start_month": 3, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Severus_Alexander",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    # ----- Crisis of the Third Century -----
    {"type": "event", "title": "Crisis of the Third Century",
     "description": "Fifty-year stretch of usurpations, plague, invasion, and breakaway states; nearly destroys the empire.",
     "start_year": 235, "end_year": 284,
     "wikipedia": "https://en.wikipedia.org/wiki/Crisis_of_the_Third_Century",
     "priorities": m(880_000, 940_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Abritus",
     "description": "Goths under Cniva defeat and kill Emperor Decius; first Roman emperor to die in battle against barbarians.",
     "start_year": 251,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Abritus",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Capture of Valerian",
     "description": "Sasanian king Shapur I captures Emperor Valerian at Edessa; he dies in Persian captivity.",
     "start_year": 260,
     "wikipedia": "https://en.wikipedia.org/wiki/Valerian_(emperor)",
     "priorities": m(810_000, 870_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Gallic Empire breakaway",
     "description": "Postumus and successors rule Gaul, Britain and Hispania independently of Rome for over a decade during the Crisis.",
     "start_year": 260, "end_year": 274,
     "wikipedia": "https://en.wikipedia.org/wiki/Gallic_Empire",
     "priorities": m(800_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Palmyrene Empire under Zenobia",
     "description": "Queen Zenobia of Palmyra seizes Roman east from Egypt to Anatolia; crushed by Aurelian.",
     "start_year": 270, "end_year": 273,
     "wikipedia": "https://en.wikipedia.org/wiki/Palmyrene_Empire",
     "priorities": m(820_000, 880_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Aurelian Walls of Rome",
     "description": "Emperor Aurelian builds 19-km wall around Rome; symbolic and practical recognition that the capital itself is now vulnerable.",
     "start_year": 271, "end_year": 275,
     "wikipedia": "https://en.wikipedia.org/wiki/Aurelian_Walls",
     "priorities": m(820_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Aurelian reunites the empire",
     "description": "'Restitutor Orbis' Aurelian crushes the breakaway Gallic and Palmyrene empires in two campaigns, restoring imperial unity.",
     "start_year": 274,
     "wikipedia": "https://en.wikipedia.org/wiki/Aurelian",
     "priorities": m(830_000, 890_000), "region_weights": RW_ROMAN},

    # ----- Diocletian and the Tetrarchy -----
    {"type": "event", "title": "Reign of Diocletian",
     "description": "Soldier-emperor who ends the Crisis; reorganises empire into Tetrarchy with two senior Augusti and two junior Caesars.",
     "start_year": 284, "end_year": 305, "start_month": 11, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Diocletian",
     "priorities": m(870_000, 930_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Tetrarchy established",
     "description": "Diocletian formalises rule by four emperors; doubles the army, partitions provinces, and creates the late Roman bureaucracy.",
     "start_year": 293, "start_month": 3, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Tetrarchy",
     "priorities": m(840_000, 900_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Edict on Maximum Prices",
     "description": "Diocletian fixes price ceilings across the empire to fight inflation; widely ignored.",
     "start_year": 301,
     "wikipedia": "https://en.wikipedia.org/wiki/Edict_on_Maximum_Prices",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Diocletianic Persecution",
     "description": "Last and largest Roman persecution of Christians; thousands killed before Edict of Milan reverses policy.",
     "start_year": 303, "end_year": 311,
     "wikipedia": "https://en.wikipedia.org/wiki/Diocletianic_Persecution",
     "priorities": m(840_000, 890_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Diocletian abdicates",
     "description": "Unique abdication of a Roman emperor; Diocletian retires to his palace at Spalatum (Split) to grow cabbages.",
     "start_year": 305, "start_month": 5, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Diocletian",
     "priorities": m(810_000, 870_000), "region_weights": RW_ROMAN},

    # ----- Constantine and the Christian Empire -----
    {"type": "event", "title": "Battle of the Milvian Bridge",
     "description": "Constantine defeats Maxentius outside Rome under the labarum; turning point in the Christianisation of the empire.",
     "start_year": 312, "start_month": 10, "start_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Milvian_Bridge",
     "priorities": m(890_000, 930_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Constantine the Great",
     "description": "First Christian emperor; founds Constantinople; reunites empire after defeating Licinius in 324.",
     "start_year": 306, "end_year": 337, "start_month": 7, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Constantine_the_Great",
     "priorities": m(900_000, 950_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "First Council of Nicaea",
     "description": "Constantine convenes the first ecumenical council; defines Trinity, condemns Arianism, sets date of Easter.",
     "start_year": 325, "start_month": 5, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Council_of_Nicaea",
     "priorities": m(890_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Julian the Apostate",
     "description": "Last pagan emperor; tries to reverse Christianisation; killed campaigning against the Sasanians in Mesopotamia.",
     "start_year": 361, "end_year": 363, "start_month": 11, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Julian_(emperor)",
     "priorities": m(830_000, 890_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Adrianople",
     "description": "Goths under Fritigern annihilate Eastern army; Emperor Valens killed; ushers in waves of barbarian settlement inside the empire.",
     "start_year": 378, "start_month": 8, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Adrianople",
     "priorities": m(880_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Theodosius I",
     "description": "Last emperor to rule both halves of the empire; makes Nicene Christianity the state religion; bans paganism.",
     "start_year": 379, "end_year": 395, "start_month": 1, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Theodosius_I",
     "priorities": m(860_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Edict of Thessalonica",
     "description": "Theodosius makes Nicene Christianity the official religion of the Roman empire; other Christianities branded heretical.",
     "start_year": 380, "start_month": 2, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Edict_of_Thessalonica",
     "priorities": m(870_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Empire permanently divided",
     "description": "Theodosius dies; empire passed permanently to two sons — Honorius (West) and Arcadius (East). They never reunite.",
     "start_year": 395, "start_month": 1, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Theodosius_I",
     "priorities": m(880_000, 930_000), "region_weights": RW_ROMAN},

    # ----- Western collapse -----
    {"type": "event", "title": "Sack of Rome by Alaric",
     "description": "Visigoths under Alaric storm the city of Rome — first sack in 800 years; shock across the Mediterranean world.",
     "start_year": 410, "start_month": 8, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Sack_of_Rome_(410)",
     "priorities": m(910_000, 950_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of the Catalaunian Plains",
     "description": "Coalition under Aetius defeats Attila the Hun in Gaul; one of the last great Western Roman field victories.",
     "start_year": 451, "start_month": 6, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Catalaunian_Plains",
     "priorities": m(850_000, 900_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Vandal sack of Rome",
     "description": "Vandals under Geiseric loot Rome for two weeks; word 'vandalism' descends from the event.",
     "start_year": 455, "start_month": 6, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Sack_of_Rome_(455)",
     "priorities": m(840_000, 890_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Odoacer deposes Romulus Augustulus",
     "description": "Germanic general Odoacer deposes the last Western Roman emperor; sends imperial regalia to Constantinople.",
     "start_year": 476, "start_month": 9, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Odoacer",
     "priorities": m(880_000, 920_000), "region_weights": RW_ROMAN},

    # ----- Early Byzantine -----
    {"type": "event", "title": "Reign of Justinian I",
     "description": "Eastern emperor who codifies Roman law, reconquers Italy and Africa, and builds Hagia Sophia.",
     "start_year": 527, "end_year": 565, "start_month": 8, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Justinian_I",
     "priorities": m(910_000, 950_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Corpus Juris Civilis",
     "description": "Justinian's commission codifies a millennium of Roman law into the Codex, Digest, and Institutes; basis of European civil law.",
     "start_year": 529, "end_year": 534,
     "wikipedia": "https://en.wikipedia.org/wiki/Corpus_Juris_Civilis",
     "priorities": m(900_000, 950_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Nika riots",
     "description": "Chariot-faction riots erupt into a near-revolution in Constantinople; Justinian crushes them with thousands dead in the Hippodrome.",
     "start_year": 532, "start_month": 1, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Nika_riots",
     "priorities": m(830_000, 890_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Hagia Sophia completed",
     "description": "Justinian's domed basilica in Constantinople; the largest interior space in the world for nearly a thousand years.",
     "start_year": 537, "start_month": 12, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Hagia_Sophia",
     "priorities": m(920_000, 950_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_BYZ},

    {"type": "event", "title": "Plague of Justinian",
     "description": "First recorded pandemic of bubonic plague; sweeps the Mediterranean and shatters the demographic base of Justinian's reconquests.",
     "start_year": 541, "end_year": 549,
     "wikipedia": "https://en.wikipedia.org/wiki/Plague_of_Justinian",
     "priorities": m(870_000, 920_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Byzantine reconquest of Italy",
     "description": "Belisarius and Narses recover Italy from the Ostrogoths in a 20-year war that ruins the peninsula.",
     "start_year": 535, "end_year": 554,
     "wikipedia": "https://en.wikipedia.org/wiki/Gothic_War_(535%E2%80%93554)",
     "priorities": m(840_000, 900_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Reign of Heraclius",
     "description": "Eastern emperor who crushes Sasanian Persia, recovers the True Cross, then loses Syria, Egypt and North Africa to early Islam.",
     "start_year": 610, "end_year": 641, "start_month": 10, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Heraclius",
     "priorities": m(870_000, 920_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Byzantine-Sasanian War (602-628)",
     "description": "Last great war of antiquity; Heraclius's victory exhausts both empires and opens the way for Islamic conquests.",
     "start_year": 602, "end_year": 628,
     "wikipedia": "https://en.wikipedia.org/wiki/Byzantine%E2%80%93Sasanian_War_of_602%E2%80%93628",
     "priorities": m(830_000, 890_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Arab siege of Constantinople (674-678)",
     "description": "First Arab attempt to take Constantinople; broken by Byzantine fleet using newly invented Greek fire.",
     "start_year": 674, "end_year": 678,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Constantinople_(674%E2%80%93678)",
     "priorities": m(820_000, 880_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Arab siege of Constantinople (717-718)",
     "description": "Second Arab attempt repulsed by Leo III the Isaurian; one of the most consequential battles in European history.",
     "start_year": 717, "end_year": 718,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Constantinople_(717%E2%80%93718)",
     "priorities": m(860_000, 910_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "First Iconoclasm",
     "description": "Leo III bans veneration of religious images in the Eastern empire; opens a century of bitter ecclesiastical conflict.",
     "start_year": 726, "end_year": 787,
     "wikipedia": "https://en.wikipedia.org/wiki/Byzantine_Iconoclasm",
     "priorities": m(820_000, 880_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Second Council of Nicaea",
     "description": "Empress Irene convenes seventh ecumenical council; restores icon veneration and ends first iconoclasm.",
     "start_year": 787, "start_month": 9, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Council_of_Nicaea",
     "priorities": m(800_000, 870_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Reign of Basil I (Macedonian dynasty)",
     "description": "Founder of the Macedonian dynasty; ushers in two centuries of Byzantine cultural and military renaissance.",
     "start_year": 867, "end_year": 886, "start_month": 9, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Basil_I",
     "priorities": m(820_000, 880_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Conversion of the Rus' to Orthodoxy",
     "description": "Vladimir of Kiev adopts Byzantine Christianity; permanently aligns eastern Slavs with Constantinople.",
     "start_year": 988, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Christianization_of_Kievan_Rus%27",
     "priorities": m(870_000, 900_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Reign of Basil II 'Bulgar-Slayer'",
     "description": "Macedonian emperor at the empire's medieval peak; destroys the First Bulgarian Empire after a 30-year campaign.",
     "start_year": 976, "end_year": 1025, "start_month": 1, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Basil_II",
     "priorities": m(850_000, 910_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Battle of Kleidion",
     "description": "Basil II crushes Tsar Samuel of Bulgaria; blinds 14,000 prisoners, earning the sobriquet 'Bulgar-Slayer'.",
     "start_year": 1014, "start_month": 7, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Kleidion",
     "priorities": m(800_000, 860_000), "region_weights": RW_BYZ},

    # ----- Komnenian and decline -----
    {"type": "event", "title": "Reign of Alexios I Komnenos",
     "description": "Founder of the Komnenian restoration; requests Western aid that becomes the First Crusade.",
     "start_year": 1081, "end_year": 1118, "start_month": 4, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Alexios_I_Komnenos",
     "priorities": m(820_000, 880_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Comnenian restoration",
     "description": "Komnenoi dynasty rebuilds Byzantine power in 12th-century Anatolia and Balkans; cultural high point of medieval Constantinople.",
     "start_year": 1081, "end_year": 1185,
     "wikipedia": "https://en.wikipedia.org/wiki/Komnenian_restoration",
     "priorities": m(810_000, 880_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Latin Empire of Constantinople",
     "description": "Crusader state set up after Fourth Crusade sack of 1204; Byzantine government-in-exile at Nicaea recovers the city in 1261.",
     "start_year": 1204, "end_year": 1261,
     "wikipedia": "https://en.wikipedia.org/wiki/Latin_Empire",
     "priorities": m(830_000, 890_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Byzantine recovery of Constantinople",
     "description": "Michael VIII Palaiologos retakes the city from the Latins; restores Byzantine empire as a Palaiologan rump state.",
     "start_year": 1261, "start_month": 7, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Recapture_of_Constantinople",
     "priorities": m(830_000, 880_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Battle of Pelekanon",
     "description": "Ottoman victory over Andronikos III destroys Byzantine military presence in Bithynia; opens Anatolia to Ottoman conquest.",
     "start_year": 1329, "start_month": 6, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Pelekanon",
     "priorities": m(790_000, 850_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Council of Florence",
     "description": "Late attempt at union between Roman and Greek churches in exchange for crusade aid; repudiated by Orthodox laity.",
     "start_year": 1438, "end_year": 1439,
     "wikipedia": "https://en.wikipedia.org/wiki/Council_of_Florence",
     "priorities": m(810_000, 870_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Reign of Constantine XI Palaiologos",
     "description": "Last Roman emperor; killed defending the walls of Constantinople against Mehmed II's army.",
     "start_year": 1449, "end_year": 1453, "start_month": 1, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Constantine_XI_Palaiologos",
     "priorities": m(830_000, 890_000), "region_weights": RW_BYZ},

    {"type": "event", "title": "Siege of Constantinople (1453)",
     "description": "Mehmed II's seven-week siege ends with the storming of the Theodosian walls; 1100-year Eastern Roman empire ends.",
     "start_year": 1453, "start_month": 4, "start_day": 6, "end_month": 5, "end_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Fall_of_Constantinople",
     "priorities": m(880_000, 940_000), "region_weights": RW_BYZ},
]


def main() -> int:
    base = next_available_id()
    for i, e in enumerate(ENTRIES):
        e["id"] = base + i
    n = append_entries(ENTRIES)
    print(f"Appended {n} entries (IDs {base}..{base+n-1}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
