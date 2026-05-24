"""
Phase C2 — Punic Wars detail + Macedonian wars + Late Republic.
Focused on filling gaps the existing data doesn't cover.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_ROMAN = {"europe": 10, "americas": 1, "asia": 3, "australasia": 1, "africa": 4}
RW_EURO_AFRICA = {"europe": 10, "americas": 1, "asia": 2, "australasia": 1, "africa": 8}
RW_EURO_ASIA = {"europe": 10, "americas": 1, "asia": 8, "australasia": 1, "africa": 3}


def m(master_pri: int, rh_pri: int, **extra) -> dict:
    out = {"master": master_pri, "roman-history": rh_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- First Punic War detail -----
    {"type": "event", "title": "Battle of Mylae",
     "description": "Roman fleet under Duilius wins its first naval victory over Carthage; corvus boarding ramp neutralises Punic seamanship.",
     "start_year": -260,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Mylae",
     "priorities": m(800_000, 860_000), "region_weights": RW_EURO_AFRICA},

    {"type": "event", "title": "Regulus invades Africa",
     "description": "Consul Regulus lands in Africa during First Punic War; initial success ends in capture at the Battle of Tunis.",
     "start_year": -256, "end_year": -255,
     "wikipedia": "https://en.wikipedia.org/wiki/Marcus_Atilius_Regulus",
     "priorities": m(790_000, 850_000), "region_weights": RW_EURO_AFRICA},

    {"type": "event", "title": "Battle of the Aegates Islands",
     "description": "Decisive Roman naval victory off western Sicily ends the First Punic War in Rome's favour.",
     "start_year": -241, "start_month": 3, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Aegates",
     "priorities": m(810_000, 870_000), "region_weights": RW_EURO_AFRICA},

    {"type": "event", "title": "Mercenary War (Carthage)",
     "description": "Carthage's unpaid mercenaries revolt after First Punic War; Hamilcar Barca crushes them and forges Barcid power.",
     "start_year": -241, "end_year": -238,
     "wikipedia": "https://en.wikipedia.org/wiki/Mercenary_War",
     "priorities": m(780_000, 840_000), "region_weights": RW_EURO_AFRICA},

    {"type": "event", "title": "Hamilcar Barca conquers Hispania",
     "description": "Carthaginian general Hamilcar Barca builds a Punic empire in Iberia, financing later war on Rome.",
     "start_year": -237, "end_year": -228,
     "wikipedia": "https://en.wikipedia.org/wiki/Hamilcar_Barca",
     "priorities": m(800_000, 860_000), "region_weights": RW_EURO_AFRICA},

    {"type": "event", "title": "Siege of Saguntum",
     "description": "Hannibal storms the Roman-allied Iberian city, triggering the Second Punic War.",
     "start_year": -219,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Saguntum",
     "priorities": m(800_000, 860_000), "region_weights": RW_EURO_AFRICA},

    {"type": "event", "title": "Hannibal crosses the Alps",
     "description": "Hannibal leads his army and war elephants over the Alps into Italy, opening the Second Punic War in the Po Valley.",
     "start_year": -218,
     "wikipedia": "https://en.wikipedia.org/wiki/Hannibal%27s_crossing_of_the_Alps",
     "priorities": m(910_000, 950_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of the Trebia",
     "description": "Hannibal's first major Italian victory; consul Sempronius's army shattered on the Trebia in winter.",
     "start_year": -218, "start_month": 12, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Trebia",
     "priorities": m(810_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Lake Trasimene",
     "description": "Hannibal ambushes consul Flaminius in fog along Lake Trasimene; one of the largest ambushes in military history.",
     "start_year": -217, "start_month": 6, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Lake_Trasimene",
     "priorities": m(830_000, 890_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Fabian strategy adopted",
     "description": "Dictator Quintus Fabius Maximus 'Cunctator' wears Hannibal down by avoiding pitched battle; origin of the Fabian doctrine.",
     "start_year": -217,
     "wikipedia": "https://en.wikipedia.org/wiki/Fabian_strategy",
     "priorities": m(810_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Siege of Syracuse (Archimedes)",
     "description": "Roman siege of Syracuse, defended by engineering devices of Archimedes; ends with the city's sack and the scientist's death.",
     "start_year": -214, "end_year": -212,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Syracuse_(213%E2%80%93212_BC)",
     "priorities": m(840_000, 880_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of the Metaurus",
     "description": "Roman armies destroy Hasdrubal's relief force, killing him and ending Punic hopes of reinforcing Hannibal in Italy.",
     "start_year": -207,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Metaurus",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Scipio's conquest of Hispania",
     "description": "Publius Cornelius Scipio (Africanus) drives Carthage from Iberia in a campaign culminating at Ilipa.",
     "start_year": -210, "end_year": -206,
     "wikipedia": "https://en.wikipedia.org/wiki/Roman_conquest_of_Hispania",
     "priorities": m(800_000, 860_000), "region_weights": RW_EURO_AFRICA},

    {"type": "event", "title": "Battle of Ilipa",
     "description": "Scipio Africanus decisively defeats the last major Punic army in Iberia.",
     "start_year": -206,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Ilipa",
     "priorities": m(790_000, 850_000), "region_weights": RW_EURO_AFRICA},

    {"type": "person", "title": "Scipio Africanus",
     "description": "Roman general who defeated Hannibal at Zama; political star of the early 2nd century BCE.",
     "start_year": -236, "end_year": -183, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Scipio_Africanus",
     "priorities": m(880_000, 930_000, people=940_000), "region_weights": RW_ROMAN},

    # ----- Macedonian and Seleucid wars -----
    {"type": "event", "title": "First Macedonian War",
     "description": "Roman intervention in Greece against Philip V of Macedon, allied with Hannibal during the Second Punic War.",
     "start_year": -214, "end_year": -205,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Macedonian_War",
     "priorities": m(790_000, 850_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Second Macedonian War",
     "description": "Rome defeats Philip V of Macedon at Cynoscephalae; Flamininus proclaims 'freedom of the Greeks' at the Isthmian Games.",
     "start_year": -200, "end_year": -197,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Macedonian_War",
     "priorities": m(810_000, 870_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Battle of Cynoscephalae",
     "description": "Roman legions defeat the Macedonian phalanx of Philip V; ends Antigonid hegemony in Greece.",
     "start_year": -197,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Cynoscephalae",
     "priorities": m(790_000, 850_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Roman-Seleucid War",
     "description": "Rome and the Seleucid king Antiochus III clash over Greece; Roman victories culminate at Magnesia.",
     "start_year": -192, "end_year": -188,
     "wikipedia": "https://en.wikipedia.org/wiki/Roman%E2%80%93Seleucid_War",
     "priorities": m(810_000, 870_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Battle of Magnesia",
     "description": "Scipios crush Antiochus III's Seleucid army in Asia Minor; Rome becomes the dominant power east of the Aegean.",
     "start_year": -190,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Magnesia",
     "priorities": m(800_000, 860_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Third Macedonian War",
     "description": "Rome ends the Antigonid kingdom of Perseus at Pydna; Macedonia broken into four client republics.",
     "start_year": -171, "end_year": -168,
     "wikipedia": "https://en.wikipedia.org/wiki/Third_Macedonian_War",
     "priorities": m(800_000, 860_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Battle of Pydna",
     "description": "Aemilius Paullus crushes Perseus of Macedon; legion proves superior to phalanx in close terrain.",
     "start_year": -168, "start_month": 6, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Pydna",
     "priorities": m(800_000, 860_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Sack of Corinth",
     "description": "Roman general Lucius Mummius destroys Corinth, ending the Achaean War and making mainland Greece a Roman province.",
     "start_year": -146,
     "wikipedia": "https://en.wikipedia.org/wiki/Sack_of_Corinth_(146_BC)",
     "priorities": m(820_000, 870_000), "region_weights": RW_EURO_ASIA},

    # ----- Reform era / Gracchi / Marius / Sulla -----
    {"type": "event", "title": "Tribunate of Tiberius Gracchus",
     "description": "Land-reform tribune Tiberius Sempronius Gracchus is killed by senators; opens century of political violence in Rome.",
     "start_year": -133,
     "wikipedia": "https://en.wikipedia.org/wiki/Tiberius_Gracchus",
     "priorities": m(860_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Tribunate of Gaius Gracchus",
     "description": "Younger Gracchus brother's broader reform programme also ends in his death; pattern of popularis-optimate conflict set.",
     "start_year": -123, "end_year": -121,
     "wikipedia": "https://en.wikipedia.org/wiki/Gaius_Gracchus",
     "priorities": m(840_000, 900_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Jugurthine War",
     "description": "Rome defeats Numidian king Jugurtha after years of struggle; war exposes Senate corruption and elevates Marius.",
     "start_year": -112, "end_year": -106,
     "wikipedia": "https://en.wikipedia.org/wiki/Jugurthine_War",
     "priorities": m(800_000, 860_000), "region_weights": RW_EURO_AFRICA},

    {"type": "event", "title": "Cimbrian War",
     "description": "Migrating Germanic Cimbri and Teutones threaten Italy; Marius destroys them at Aquae Sextiae and Vercellae.",
     "start_year": -113, "end_year": -101,
     "wikipedia": "https://en.wikipedia.org/wiki/Cimbrian_War",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "person", "title": "Gaius Marius",
     "description": "Seven-times consul; reformer of the Roman army into a professional force; rival of Sulla in the first civil war.",
     "start_year": -157, "end_year": -86, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Gaius_Marius",
     "priorities": m(880_000, 940_000, people=930_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Social War (Rome and Italian allies)",
     "description": "Italian allies revolt to demand Roman citizenship; ends with mass enfranchisement of free Italians.",
     "start_year": -91, "end_year": -87,
     "wikipedia": "https://en.wikipedia.org/wiki/Social_War_(91%E2%80%9387_BC)",
     "priorities": m(830_000, 890_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Sulla's first march on Rome",
     "description": "Consul Sulla marches his legions on Rome to overturn an assembly law; first general to do so, breaking a deep taboo.",
     "start_year": -88,
     "wikipedia": "https://en.wikipedia.org/wiki/Sulla%27s_first_civil_war",
     "priorities": m(820_000, 880_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "First Mithridatic War",
     "description": "Sulla campaigns in Greece against Mithridates VI of Pontus; sacks Athens; ends in compromise peace.",
     "start_year": -89, "end_year": -85,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Mithridatic_War",
     "priorities": m(800_000, 860_000), "region_weights": RW_EURO_ASIA},

    {"type": "person", "title": "Sulla (Lucius Cornelius Sulla)",
     "description": "Roman general and dictator; victor of the first civil war; constitutional reformer who restored Senate power before retiring.",
     "start_year": -138, "end_year": -78, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Sulla",
     "priorities": m(880_000, 940_000, people=920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Sulla's proscriptions",
     "description": "Sulla posts lists of enemies marked for legal killing and confiscation; thousands die, the practice enters Roman politics.",
     "start_year": -82, "end_year": -81,
     "wikipedia": "https://en.wikipedia.org/wiki/Proscription",
     "priorities": m(830_000, 880_000), "region_weights": RW_ROMAN},

    # ----- Late Republic crisis and Caesar -----
    {"type": "event", "title": "Third Mithridatic War",
     "description": "Lucullus and then Pompey defeat Mithridates VI, annexing Pontus and reorganising the eastern provinces.",
     "start_year": -73, "end_year": -63,
     "wikipedia": "https://en.wikipedia.org/wiki/Third_Mithridatic_War",
     "priorities": m(800_000, 860_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Pompey clears the Mediterranean of pirates",
     "description": "In just three months Pompey, with extraordinary command, eliminates Cilician piracy that had crippled Rome's grain supply.",
     "start_year": -67,
     "wikipedia": "https://en.wikipedia.org/wiki/Pompey",
     "priorities": m(810_000, 870_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Catilinarian conspiracy",
     "description": "Cicero as consul exposes Catiline's coup plot; delivers the four Catilinarian orations and executes conspirators.",
     "start_year": -63,
     "wikipedia": "https://en.wikipedia.org/wiki/Catilinarian_conspiracy",
     "priorities": m(830_000, 890_000), "region_weights": RW_ROMAN},

    {"type": "person", "title": "Cicero",
     "description": "Greatest orator of the Late Republic; consul, prolific philosopher and letter-writer; killed in the Triumvirs' proscriptions.",
     "start_year": -106, "end_year": -43, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Cicero",
     "priorities": m(910_000, 950_000, people=960_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_ROMAN},

    {"type": "person", "title": "Pompey the Great",
     "description": "Roman general and statesman; ally then rival of Caesar; killed in Egypt after defeat at Pharsalus.",
     "start_year": -106, "end_year": -48, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pompey",
     "priorities": m(890_000, 940_000, people=940_000), "region_weights": RW_ROMAN},

    {"type": "person", "title": "Crassus (Marcus Licinius Crassus)",
     "description": "Wealthiest Roman of the Late Republic; suppressed Spartacus; member of the First Triumvirate; killed at Carrhae.",
     "start_year": -115, "end_year": -53, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Marcus_Licinius_Crassus",
     "priorities": m(840_000, 900_000, people=900_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Carrhae",
     "description": "Parthian horse-archers under Surena annihilate Crassus's army; Crassus killed; legionary standards lost for decades.",
     "start_year": -53,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Carrhae",
     "priorities": m(820_000, 880_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Battle of Alesia",
     "description": "Caesar besieges Vercingetorix at Alesia behind double walls and crushes the Gallic relief army; effectively ends the Gallic Wars.",
     "start_year": -52, "start_month": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Alesia",
     "priorities": m(870_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Caesar's invasions of Britain",
     "description": "Julius Caesar mounts two expeditions across the Channel; Britain is brought into Rome's geographical horizon for the first time.",
     "start_year": -55, "end_year": -54,
     "wikipedia": "https://en.wikipedia.org/wiki/Caesar%27s_invasions_of_Britain",
     "priorities": m(830_000, 880_000, england=850_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Caesar's civil war",
     "description": "Caesar crosses the Rubicon and defeats Pompey and the optimate Senate in Spain, Greece, Africa, and Hispania.",
     "start_year": -49, "end_year": -45,
     "wikipedia": "https://en.wikipedia.org/wiki/Caesar%27s_civil_war",
     "priorities": m(880_000, 930_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Pharsalus",
     "description": "Caesar decisively defeats Pompey in Thessaly; Pompey flees to Egypt where he is murdered.",
     "start_year": -48, "start_month": 8, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Pharsalus",
     "priorities": m(850_000, 910_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Thapsus",
     "description": "Caesar defeats the optimate army of Metellus Scipio in north Africa; Cato the Younger commits suicide at Utica.",
     "start_year": -46, "start_month": 4, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Thapsus",
     "priorities": m(790_000, 860_000), "region_weights": RW_EURO_AFRICA},

    {"type": "event", "title": "Battle of Munda",
     "description": "Caesar's last battle; defeats the sons of Pompey in Spain, ending the civil war.",
     "start_year": -45, "start_month": 3, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Munda",
     "priorities": m(790_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Julian calendar introduced",
     "description": "Caesar's reform replaces the irregular Roman calendar with a 365.25-day solar year; used until the Gregorian reform.",
     "start_year": -45, "start_month": 1, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Julian_calendar",
     "priorities": m(870_000, 910_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Philippi",
     "description": "Antony and Octavian defeat Brutus and Cassius in Macedonia; the Republican cause dies on the field.",
     "start_year": -42, "start_month": 10, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Philippi",
     "priorities": m(840_000, 900_000), "region_weights": RW_ROMAN},

    {"type": "person", "title": "Mark Antony",
     "description": "Caesar's lieutenant, triumvir, and lover of Cleopatra; defeated by Octavian at Actium.",
     "start_year": -83, "end_year": -30, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mark_Antony",
     "priorities": m(870_000, 920_000, people=930_000), "region_weights": RW_ROMAN},

    # ----- Augustus and the early Principate -----
    {"type": "event", "title": "Augustan settlement",
     "description": "Octavian formalises his rule as 'princeps'; the Senate confers the title Augustus; constitutional fiction of restored Republic begins the Principate.",
     "start_year": -27, "start_month": 1, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/First_settlement",
     "priorities": m(890_000, 950_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Ara Pacis Augustae consecrated",
     "description": "Senate-commissioned marble altar in Rome celebrating Augustus's peace after Gallic and Hispanic campaigns.",
     "start_year": -9, "start_month": 1, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Ara_Pacis",
     "priorities": m(800_000, 850_000, **{"arts-and-thoughts": 850_000}), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Teutoburg Forest",
     "description": "German chief Arminius destroys three Roman legions in the Teutoburg Wald; halts Roman expansion at the Rhine.",
     "start_year": 9, "start_month": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Teutoburg_Forest",
     "priorities": m(880_000, 930_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Death of Augustus",
     "description": "Founder of the Principate dies at Nola; his stepson Tiberius succeeds, demonstrating the dynastic logic of the new system.",
     "start_year": 14, "start_month": 8, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Augustus",
     "priorities": m(870_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Praetorian Guard concentrated in Rome",
     "description": "Tiberius's prefect Sejanus quarters the Praetorian cohorts in a single barracks in Rome; magnifies their political weight.",
     "start_year": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Praetorian_Guard",
     "priorities": m(790_000, 850_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Conquest of Britain begins (Claudius)",
     "description": "Emperor Claudius lands four legions under Aulus Plautius in Kent; beginning of a 400-year Roman province of Britannia.",
     "start_year": 43, "end_year": 43, "start_month": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Roman_conquest_of_Britain",
     "priorities": m(860_000, 910_000, england=920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "First Jewish-Roman War",
     "description": "Jewish revolt in Judea against Roman rule ends with Titus's sack of Jerusalem and destruction of the Second Temple.",
     "start_year": 66, "end_year": 73,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Jewish%E2%80%93Roman_War",
     "priorities": m(870_000, 910_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Destruction of the Second Temple",
     "description": "Titus's legions storm Jerusalem and burn the Temple in 70 CE; transforms Judaism and Christian self-definition.",
     "start_year": 70, "start_month": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Jerusalem_(70_CE)",
     "priorities": m(890_000, 920_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Siege of Masada",
     "description": "Jewish Sicarii rebels hold the desert fortress against Roman siegeworks until mass suicide on the brink of capture.",
     "start_year": 73, "start_month": 4, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Masada",
     "priorities": m(820_000, 870_000), "region_weights": RW_EURO_ASIA},

    {"type": "event", "title": "Year of the Four Emperors",
     "description": "After Nero's suicide, Galba, Otho, Vitellius and Vespasian successively claim the throne; Vespasian's Flavian dynasty wins.",
     "start_year": 69,
     "wikipedia": "https://en.wikipedia.org/wiki/Year_of_the_Four_Emperors",
     "priorities": m(840_000, 900_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Vespasian",
     "description": "Founder of the Flavian dynasty; stabilises the empire after civil war; begins the Colosseum.",
     "start_year": 69, "end_year": 79, "start_month": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Vespasian",
     "priorities": m(820_000, 880_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Titus",
     "description": "Flavian emperor who completed the Colosseum; reign marked by Vesuvius eruption and fire and plague at Rome.",
     "start_year": 79, "end_year": 81, "start_month": 6, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Titus",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Domitian",
     "description": "Last Flavian emperor; effective administrator and tyrant; assassinated in palace conspiracy after 15 years.",
     "start_year": 81, "end_year": 96, "start_month": 9, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Domitian",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Nerva",
     "description": "Senator chosen as emperor after Domitian's murder; adopts Trajan as heir, initiating the 'Five Good Emperors' succession.",
     "start_year": 96, "end_year": 98, "start_month": 9, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Nerva",
     "priorities": m(790_000, 850_000), "region_weights": RW_ROMAN},
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
