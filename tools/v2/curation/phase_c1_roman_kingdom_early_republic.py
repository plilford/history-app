"""
Phase C1 — Roman Kingdom (753-509 BCE) + Early Republic (509-264 BCE).
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

# Default region weights for Roman entries: Europe-heavy.
RW_ROMAN = {"europe": 10, "americas": 1, "asia": 3, "australasia": 1, "africa": 4}
RW_EURO_AFRICA = {"europe": 10, "americas": 1, "asia": 2, "australasia": 1, "africa": 8}

P_R_HIGH = {"master": 920_000, "roman-history": 950_000}
P_R_MID = {"master": 880_000, "roman-history": 900_000}
P_R_LOW = {"master": 850_000, "roman-history": 860_000}
P_R_BG = {"master": 830_000, "roman-history": 840_000}


def m(master_pri: int, rh_pri: int, **extra) -> dict:
    out = {"master": master_pri, "roman-history": rh_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- Etruscan + pre-Roman context -----
    {"type": "event", "title": "Etruscan civilization peak",
     "description": "Etruscan league dominates central Italy, deeply influencing nascent Rome's religion, kingship, and engineering.",
     "start_year": -700, "end_year": -500, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Etruscan_civilization",
     "priorities": m(870_000, 900_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Aeneas legend (Trojan origin myth)",
     "description": "Mythic genealogy linking Rome's founders to refugees from fallen Troy via Aeneas, later canonised by Virgil.",
     "start_year": -1184, "date_uncertain": True,
     "display_date": "legendary, c. 1184 BCE",
     "wikipedia": "https://en.wikipedia.org/wiki/Aeneas",
     "priorities": m(800_000, 830_000), "region_weights": RW_ROMAN},

    # ----- Kingdom of Rome -----
    {"type": "event", "title": "Reign of Romulus",
     "description": "Traditional first king of Rome; founds the city, organises Senate of 100 elders, fights Sabines.",
     "start_year": -753, "end_year": -716, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Romulus",
     "priorities": m(870_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Rape of the Sabine Women",
     "description": "Legendary abduction of Sabine women by early Romans; ends in alliance and merger of the two peoples.",
     "start_year": -750, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Rape_of_the_Sabine_Women",
     "priorities": m(800_000, 850_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Numa Pompilius",
     "description": "Second king of Rome; credited with founding Roman religious institutions, college of pontiffs, and the calendar.",
     "start_year": -715, "end_year": -673, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Numa_Pompilius",
     "priorities": m(830_000, 880_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Tullus Hostilius",
     "description": "Third king of Rome; warlike successor who destroys Alba Longa and absorbs its population.",
     "start_year": -673, "end_year": -642, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tullus_Hostilius",
     "priorities": m(810_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Ancus Marcius",
     "description": "Fourth king of Rome; expands the city to the Aventine, builds the first bridge over the Tiber and the port of Ostia.",
     "start_year": -642, "end_year": -617, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ancus_Marcius",
     "priorities": m(810_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Tarquinius Priscus",
     "description": "Fifth king, first of Etruscan dynasty; builds Cloaca Maxima, Circus Maximus and the Temple of Jupiter on the Capitoline.",
     "start_year": -616, "end_year": -579, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Lucius_Tarquinius_Priscus",
     "priorities": m(830_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Servius Tullius",
     "description": "Sixth king of Rome; reorganises the citizen body into centuries and classes, lays out the Servian Wall.",
     "start_year": -578, "end_year": -535, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Servius_Tullius",
     "priorities": m(840_000, 880_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Reign of Tarquinius Superbus",
     "description": "Seventh and last king of Rome; tyrannical Etruscan ruler whose overthrow founds the Republic.",
     "start_year": -534, "end_year": -509, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Lucius_Tarquinius_Superbus",
     "priorities": m(840_000, 880_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Rape of Lucretia",
     "description": "Assault of Lucretia by the king's son sparks the revolt that ends the monarchy at Rome.",
     "start_year": -509, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Lucretia",
     "priorities": m(810_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Roman Republic founded",
     "description": "Expulsion of Tarquinius Superbus; Rome adopts two annual consuls and the institutions of the Senate-driven Republic.",
     "start_year": -509,
     "wikipedia": "https://en.wikipedia.org/wiki/Roman_Republic",
     "priorities": m(960_000, 990_000), "region_weights": RW_ROMAN},

    # ----- Early Republic -----
    {"type": "event", "title": "Battle of Lake Regillus",
     "description": "Roman victory over the Latin League secures the young Republic against Etruscan-backed restoration of the Tarquins.",
     "start_year": -496, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Lake_Regillus",
     "priorities": m(800_000, 850_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "First secession of the plebs",
     "description": "Plebeians withdraw from Rome to the Mons Sacer; concessions create the tribunate of the plebs and aedileship.",
     "start_year": -494, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Secessio_plebis",
     "priorities": m(840_000, 910_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Cincinnatus called from the plough",
     "description": "Roman senator twice given dictatorial powers and twice retires after victory; archetype of civic restraint.",
     "start_year": -458, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Lucius_Quinctius_Cincinnatus",
     "priorities": m(820_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Law of the Twelve Tables",
     "description": "Rome's first codified law, posted in the Forum; foundation of Roman legal tradition.",
     "start_year": -451, "end_year": -449, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Twelve_Tables",
     "priorities": m(870_000, 940_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Lex Canuleia",
     "description": "Tribune Canuleius secures legalisation of marriage between patricians and plebeians at Rome.",
     "start_year": -445, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Lex_Canuleia",
     "priorities": m(790_000, 840_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Siege of Veii",
     "description": "Ten-year Roman siege of the Etruscan city of Veii ends in capture and doubles Roman territory.",
     "start_year": -406, "end_year": -396, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Veii",
     "priorities": m(820_000, 880_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of the Allia",
     "description": "Senones Gauls under Brennus crush a Roman army on the Allia, opening Rome to sack.",
     "start_year": -390, "start_month": 7, "start_day": 18, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Allia",
     "priorities": m(840_000, 890_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Gallic sack of Rome",
     "description": "Senones Gauls under Brennus capture and burn Rome; the Capitol holds out. \"Vae victis.\"",
     "start_year": -390, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Allia",
     "priorities": m(880_000, 930_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Camillus rebuilds Rome",
     "description": "After the Gallic sack, Marcus Furius Camillus refounds the city's defences and constitution; styled second founder of Rome.",
     "start_year": -390, "end_year": -365, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Marcus_Furius_Camillus",
     "priorities": m(810_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Servian Wall completed",
     "description": "Eleven-kilometre defensive wall enclosing Rome's seven hills, built in tufa blocks after the Gallic sack.",
     "start_year": -378, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Servian_Wall",
     "priorities": m(800_000, 850_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Licinian-Sextian laws",
     "description": "Tribunes Licinius and Sextius open the consulship to plebeians and cap individual landholding on public land.",
     "start_year": -367, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Leges_Liciniae_Sextiae",
     "priorities": m(820_000, 880_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "First Samnite War",
     "description": "Rome's first major war south of Latium, intervening in Campania against the Samnite confederation.",
     "start_year": -343, "end_year": -341,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Samnite_War",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Latin War",
     "description": "Latin allies revolt against Roman dominance; Rome wins and dissolves the Latin League, absorbing its cities individually.",
     "start_year": -340, "end_year": -338,
     "wikipedia": "https://en.wikipedia.org/wiki/Latin_War",
     "priorities": m(810_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Second Samnite War",
     "description": "Long struggle for central Italy; includes Roman disaster at the Caudine Forks and eventual Roman dominance.",
     "start_year": -326, "end_year": -304,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Samnite_War",
     "priorities": m(830_000, 890_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of the Caudine Forks",
     "description": "Samnites trap and humiliate a Roman army in a mountain defile; survivors pass beneath the yoke.",
     "start_year": -321,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Caudine_Forks",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Appius Claudius begins Via Appia",
     "description": "Censor Appius Claudius Caecus starts construction of the Via Appia from Rome to Capua; first great Roman road.",
     "start_year": -312,
     "wikipedia": "https://en.wikipedia.org/wiki/Appian_Way",
     "priorities": m(810_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Aqua Appia (first Roman aqueduct)",
     "description": "Appius Claudius Caecus also commissions Rome's first aqueduct; ~16 km mostly underground supply to the city.",
     "start_year": -312,
     "wikipedia": "https://en.wikipedia.org/wiki/Aqua_Appia",
     "priorities": m(790_000, 850_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Third Samnite War",
     "description": "Final Samnite coalition with Etruscans, Umbrians, and Gauls crushed by Rome; consolidates Roman control of Italy.",
     "start_year": -298, "end_year": -290,
     "wikipedia": "https://en.wikipedia.org/wiki/Third_Samnite_War",
     "priorities": m(810_000, 870_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Sentinum",
     "description": "Decisive Roman victory over Samnite-Gallic-Etruscan coalition; consul Decius Mus performs devotio.",
     "start_year": -295,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Sentinum",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Lex Hortensia",
     "description": "Plebiscites of the plebeian assembly become binding on all Romans; effective end of the Conflict of the Orders.",
     "start_year": -287,
     "wikipedia": "https://en.wikipedia.org/wiki/Lex_Hortensia",
     "priorities": m(820_000, 890_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Pyrrhic War",
     "description": "Pyrrhus of Epirus crosses to Italy at Tarentum's request; defeats Rome at Heraclea and Asculum but at ruinous cost.",
     "start_year": -280, "end_year": -275,
     "wikipedia": "https://en.wikipedia.org/wiki/Pyrrhic_War",
     "priorities": m(830_000, 890_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Heraclea",
     "description": "Pyrrhus wins his first 'Pyrrhic victory' over Rome using war elephants new to Italian warfare.",
     "start_year": -280,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Heraclea",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Asculum (279 BCE)",
     "description": "Second 'Pyrrhic victory' — Pyrrhus defeats Rome but loses irreplaceable veterans.",
     "start_year": -279,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Asculum",
     "priorities": m(790_000, 850_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Battle of Beneventum (275 BCE)",
     "description": "Romans under Manius Curius Dentatus defeat Pyrrhus, ending his Italian adventure; Rome dominant in peninsula.",
     "start_year": -275,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Beneventum_(275_BC)",
     "priorities": m(800_000, 860_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Rome controls all peninsular Italy",
     "description": "With Tarentum's surrender, Rome consolidates control of the Italian peninsula south of the Po.",
     "start_year": -272,
     "wikipedia": "https://en.wikipedia.org/wiki/Roman_expansion_in_Italy",
     "priorities": m(880_000, 920_000), "region_weights": RW_ROMAN},

    {"type": "event", "title": "Punic Carthage at peak",
     "description": "By the mid-3rd century BCE the Punic city-state dominates the western Mediterranean trade routes, setting up collision with Rome.",
     "start_year": -300, "end_year": -264, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Carthage",
     "priorities": m(840_000, 890_000), "region_weights": RW_EURO_AFRICA},

    {"type": "event", "title": "First Roman coinage (silver didrachms)",
     "description": "Rome strikes its first silver didrachms, originally for trade with Greek south Italy.",
     "start_year": -280, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Roman_currency",
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
