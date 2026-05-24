"""
Phase C4 — Prehistoric / Roman / Sub-Roman / Anglo-Saxon / Viking Britain.
Fills gaps the existing data doesn't cover.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_BRIT = {"europe": 10, "americas": 2, "asia": 2, "australasia": 2, "africa": 2}


def e(master_pri: int, eng_pri: int, **extra) -> dict:
    out = {"master": master_pri, "england": eng_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- Prehistoric / Iron Age Britain -----
    {"type": "event", "title": "Stonehenge sarsen circle erected",
     "description": "Massive sarsen and bluestone monument in Wiltshire reaches its iconic form; major ceremonial site of late Neolithic Britain.",
     "start_year": -2500, "date_uncertain": True,
     "display_date": "c. 2500 BCE",
     "wikipedia": "https://en.wikipedia.org/wiki/Stonehenge",
     "priorities": e(890_000, 940_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_BRIT},

    {"type": "event", "title": "Pytheas of Massalia visits Britain",
     "description": "Greek navigator from Marseille sails round Britain; first written Mediterranean account of the islands and tin trade.",
     "start_year": -320, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pytheas",
     "priorities": e(790_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Celtic Iron Age in Britain",
     "description": "Late La Tène culture flourishes across Britain; tribal kingdoms, hillforts, and coinage.",
     "start_year": -800, "end_year": 43, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Iron_Age_Britain",
     "priorities": e(820_000, 890_000), "region_weights": RW_BRIT},

    # ----- Roman Britain detail -----
    {"type": "event", "title": "Cunobeline of Catuvellauni",
     "description": "British king ruling much of southeast England before Roman conquest; Shakespeare's Cymbeline.",
     "start_year": -9, "end_year": 40, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Cunobeline",
     "priorities": e(780_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Roman Britain (Britannia)",
     "description": "Roman province from Claudius's invasion in 43 CE to the army's withdrawal in 410; ~365 years of Roman rule.",
     "start_year": 43, "end_year": 410,
     "wikipedia": "https://en.wikipedia.org/wiki/Roman_Britain",
     "priorities": e(900_000, 950_000, **{"roman-history": 920_000}), "region_weights": RW_BRIT},

    {"type": "event", "title": "Roman Londinium founded",
     "description": "Roman trading settlement established on the Thames; grows into the provincial capital after Boudica's revolt.",
     "start_year": 47, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Londinium",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Agricola governor of Britannia",
     "description": "Cornelius Tacitus's father-in-law campaigns into Caledonia, fights at Mons Graupius, circumnavigates Britain.",
     "start_year": 78, "end_year": 84,
     "wikipedia": "https://en.wikipedia.org/wiki/Gnaeus_Julius_Agricola",
     "priorities": e(810_000, 870_000, **{"roman-history": 850_000}), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Mons Graupius",
     "description": "Agricola defeats Caledonian leader Calgacus in northern Britain; the high-water mark of Roman expansion in the island.",
     "start_year": 83, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Mons_Graupius",
     "priorities": e(790_000, 850_000, **{"roman-history": 830_000}), "region_weights": RW_BRIT},

    {"type": "event", "title": "Antonine Wall built",
     "description": "Turf rampart 100 km north of Hadrian's Wall, between the Forth and Clyde; held for about 20 years before retreat.",
     "start_year": 142, "end_year": 154,
     "wikipedia": "https://en.wikipedia.org/wiki/Antonine_Wall",
     "priorities": e(800_000, 860_000, **{"roman-history": 830_000}), "region_weights": RW_BRIT},

    {"type": "event", "title": "Carausian Revolt",
     "description": "Roman naval commander Carausius declares himself emperor in Britain and northern Gaul; killed by his finance minister Allectus.",
     "start_year": 286, "end_year": 296,
     "wikipedia": "https://en.wikipedia.org/wiki/Carausius",
     "priorities": e(790_000, 850_000, **{"roman-history": 830_000}), "region_weights": RW_BRIT},

    {"type": "event", "title": "Constantine acclaimed at York",
     "description": "Constantine the Great proclaimed emperor by his army at Eboracum (York) after his father Constantius dies there.",
     "start_year": 306, "start_month": 7, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Constantine_the_Great",
     "priorities": e(820_000, 880_000, **{"roman-history": 870_000}), "region_weights": RW_BRIT},

    {"type": "event", "title": "Great Conspiracy",
     "description": "Coordinated attacks on Roman Britain by Picts, Scoti, Saxons and Attacotti; Theodosius the Elder restores order.",
     "start_year": 367, "end_year": 368,
     "wikipedia": "https://en.wikipedia.org/wiki/Great_Conspiracy",
     "priorities": e(780_000, 840_000, **{"roman-history": 830_000}), "region_weights": RW_BRIT},

    {"type": "event", "title": "Magnus Maximus stripped Britain of legions",
     "description": "Western usurper drains the British garrison for his Gallic campaign; weakens the province permanently.",
     "start_year": 383, "end_year": 388,
     "wikipedia": "https://en.wikipedia.org/wiki/Magnus_Maximus",
     "priorities": e(790_000, 850_000, **{"roman-history": 830_000}), "region_weights": RW_BRIT},

    {"type": "event", "title": "Rescript of Honorius",
     "description": "Western emperor tells the cities of Britannia to look to their own defence; effective end of Roman administration.",
     "start_year": 410,
     "wikipedia": "https://en.wikipedia.org/wiki/End_of_Roman_rule_in_Britain",
     "priorities": e(870_000, 920_000, **{"roman-history": 900_000}), "region_weights": RW_BRIT},

    # ----- Sub-Roman / Early Anglo-Saxon -----
    {"type": "event", "title": "Adventus Saxonum (legendary)",
     "description": "Traditional date of Hengist and Horsa's invitation by Vortigern to defend Kent against Picts; opens Anglo-Saxon settlement.",
     "start_year": 449, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Adventus_Saxonum",
     "priorities": e(820_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Brittonic kingdoms emerge",
     "description": "Post-Roman British kingdoms (Dumnonia, Gwynedd, Strathclyde, Rheged) establish themselves west and north of Saxon expansion.",
     "start_year": 450, "end_year": 700, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Sub-Roman_Britain",
     "priorities": e(800_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Heptarchy of Anglo-Saxon England",
     "description": "Seven major kingdoms (Wessex, Mercia, Northumbria, East Anglia, Essex, Sussex, Kent) divide what becomes England.",
     "start_year": 600, "end_year": 900, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Heptarchy",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Sutton Hoo ship burial",
     "description": "Spectacular East Anglian royal burial under a mound near Woodbridge; treasure-laden iron-bound ship and ornate helmet.",
     "start_year": 625, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Sutton_Hoo",
     "priorities": e(850_000, 900_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_BRIT},

    {"type": "event", "title": "Lindisfarne Gospels",
     "description": "Illuminated Insular manuscript of the four Gospels produced at Lindisfarne; one of the masterpieces of Anglo-Saxon art.",
     "start_year": 715, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Lindisfarne_Gospels",
     "priorities": e(830_000, 880_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_BRIT},

    {"type": "event", "title": "Offa's Dyke built",
     "description": "Earthen rampart and ditch ~150 miles long along the Welsh border, marking Mercian expansion under Offa.",
     "start_year": 785, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Offa%27s_Dyke",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    # ----- Viking Age -----
    {"type": "event", "title": "Lindisfarne raid",
     "description": "Vikings attack the monastery on Holy Island in Northumbria; conventional start of the Viking Age in Britain.",
     "start_year": 793, "start_month": 6, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Lindisfarne",
     "priorities": e(870_000, 920_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Great Heathen Army lands",
     "description": "Vast Danish Viking host lands in East Anglia; over the next 14 years it conquers Northumbria, Mercia and East Anglia.",
     "start_year": 865,
     "wikipedia": "https://en.wikipedia.org/wiki/Great_Heathen_Army",
     "priorities": e(850_000, 910_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Edington",
     "description": "Alfred the Great's victory over the Danish Great Heathen Army; secures Wessex and forces conversion of Guthrum.",
     "start_year": 878, "start_month": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Edington",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Danelaw established",
     "description": "Treaty between Alfred and Guthrum partitions England; Danish law and settlement dominate north and east.",
     "start_year": 886, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Danelaw",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Anglo-Saxon Chronicle begun",
     "description": "Annual chronicle of English history, started in Alfred's reign; continues in some manuscripts until 1154.",
     "start_year": 890, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Anglo-Saxon_Chronicle",
     "priorities": e(810_000, 880_000, **{"arts-and-thoughts": 850_000}),
     "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Brunanburh",
     "description": "Æthelstan defeats a Norse-Scottish-Strathclyde coalition; consolidates a unified English kingdom.",
     "start_year": 937,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Brunanburh",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Maldon",
     "description": "English ealdorman Byrhtnoth killed by raiding Vikings on the Essex coast; subject of the Old English poem.",
     "start_year": 991, "start_month": 8, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Maldon",
     "priorities": e(790_000, 850_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "St Brice's Day Massacre",
     "description": "Æthelred orders the killing of Danes living in England; provokes vengeful invasions by Sweyn Forkbeard.",
     "start_year": 1002, "start_month": 11, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/St._Brice%27s_Day_massacre",
     "priorities": e(790_000, 850_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Danegeld payments",
     "description": "Anglo-Saxon kings buy off Viking raiders with massive silver payments; ultimately exceed 250,000 lb of silver.",
     "start_year": 991, "end_year": 1014, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Danegeld",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    # ----- 1066 -----
    {"type": "event", "title": "Battle of Fulford",
     "description": "Harald Hardrada and Tostig defeat the northern English earls; opens the way to York shortly before Hastings.",
     "start_year": 1066, "start_month": 9, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Fulford",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Stamford Bridge",
     "description": "Harold Godwinson crushes Harald Hardrada's Norwegian invasion in Yorkshire, days before the Norman landing in Sussex.",
     "start_year": 1066, "start_month": 9, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Stamford_Bridge",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Hastings",
     "description": "William of Normandy defeats Harold Godwinson on Senlac Hill; Harold killed and the throne falls to William.",
     "start_year": 1066, "start_month": 10, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Hastings",
     "priorities": e(920_000, 960_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Harrying of the North",
     "description": "William's brutal winter campaign devastates Yorkshire and Durham; population displaced for generations.",
     "start_year": 1069, "end_year": 1070,
     "wikipedia": "https://en.wikipedia.org/wiki/Harrying_of_the_North",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},
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
