"""
Phase H2 — Deep-fill of high-priority existing umbrellas + a few topical
gaps that didn't get an umbrella scaffold in H1.

Targets:
  - Spanish Civil War depth (~8)
  - French Wars of Religion (~6)
  - Eastern Front WW2 (~8)
  - North Africa WW2 (~6)
  - Italian Renaissance art masters (~10)
  - Persian / Achaemenid empire (~8)
  - Pharaonic Egypt (~10)
  - Roman emperors gaps + early Christianity (~6)
  - Pre-Columbian deeper (~5)
  - More Tang/Song/Ming detail (~8)
  - Various modern (~10)
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_EU = {"europe": 10, "americas": 3, "asia": 3, "australasia": 1, "africa": 3}
RW_AMER = {"europe": 4, "americas": 10, "asia": 1, "australasia": 1, "africa": 3}
RW_RUSSIA = {"europe": 9, "americas": 4, "asia": 5, "australasia": 1, "africa": 1}
RW_AFRICA = {"europe": 5, "americas": 1, "asia": 3, "australasia": 1, "africa": 10}
RW_PERSIA = {"europe": 4, "americas": 1, "asia": 10, "australasia": 1, "africa": 4}
RW_EGYPT = {"europe": 5, "americas": 1, "asia": 5, "australasia": 1, "africa": 10}
RW_CHINA = {"europe": 2, "americas": 1, "asia": 10, "australasia": 2, "africa": 1}
RW_GLOBAL = {"europe": 8, "americas": 7, "asia": 5, "australasia": 3, "africa": 4}


def pri(master: int, **extras) -> dict:
    return {"master": master, **extras}


ENTRIES = [
    # =================================================================
    # SPANISH CIVIL WAR
    # =================================================================
    {"type": "person", "title": "Francisco Franco",
     "description": "Spanish general; led Nationalist forces in the Civil War; dictator of Spain 1939-75; cultivated international ambiguity during WWII.",
     "start_year": 1892, "end_year": 1975, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Francisco_Franco",
     "priorities": pri(910_000, people=920_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Siege of Madrid",
     "description": "Three-year Republican defence of Madrid against Nationalist forces; emblem of the Republic's resistance.",
     "start_year": 1936, "start_month": 11, "start_day": 8, "end_year": 1939, "end_month": 3, "end_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Madrid",
     "priorities": pri(840_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Spanish Civil War"},

    {"type": "event", "title": "Bombing of Guernica",
     "description": "Nazi Condor Legion bombs Basque town of Guernica; subject of Picasso's famous painting; symbol of total war on civilians.",
     "start_year": 1937, "start_month": 4, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Bombing_of_Guernica",
     "priorities": pri(900_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Spanish Civil War"},

    {"type": "art", "title": "Picasso's Guernica",
     "description": "Pablo Picasso's monumental anti-war painting commissioned for the 1937 Paris Exposition; defining work of 20th-century political art.",
     "start_year": 1937, "start_month": 6, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Guernica_(Picasso)",
     "priorities": pri(930_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Bombing of Guernica"},

    {"type": "event", "title": "International Brigades",
     "description": "Foreign volunteer brigades (35,000+ from 50+ countries) fight for Spanish Republic; communist-led; lost most of their effectiveness by mid-1937.",
     "start_year": 1936, "end_year": 1938,
     "wikipedia": "https://en.wikipedia.org/wiki/International_Brigades",
     "priorities": pri(860_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Spanish Civil War"},

    {"type": "event", "title": "Battle of the Ebro",
     "description": "Largest battle of the Spanish Civil War; Republican offensive becomes a Nationalist defensive victory; effectively decides the war.",
     "start_year": 1938, "start_month": 7, "start_day": 25, "end_month": 11, "end_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Ebro",
     "priorities": pri(820_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Spanish Civil War"},

    {"type": "event", "title": "Nationalist victory in Spain",
     "description": "Madrid falls; Franco declares victory; opens 36-year fascist-leaning dictatorship.",
     "start_year": 1939, "start_month": 4, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Spanish_Civil_War",
     "priorities": pri(890_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Spanish Civil War"},

    # =================================================================
    # FRENCH WARS OF RELIGION
    # =================================================================
    {"type": "event", "title": "St Bartholomew's Day Massacre",
     "description": "Targeted killing of French Huguenot leaders in Paris triggers nationwide massacre; ~10,000 killed; intensifies the Wars of Religion.",
     "start_year": 1572, "start_month": 8, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/St._Bartholomew%27s_Day_massacre",
     "priorities": pri(910_000, france=940_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Wars of Religion"},

    {"type": "person", "title": "Henry IV of France",
     "description": "First Bourbon king; converted to Catholicism (\"Paris is worth a Mass\") to end the Wars of Religion; issued the Edict of Nantes; assassinated 1610.",
     "start_year": 1553, "end_year": 1610, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Henry_IV_of_France",
     "priorities": pri(910_000, france=930_000, people=920_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Edict of Nantes",
     "description": "Henry IV grants Huguenots substantial rights of worship; ends French Wars of Religion; revoked 1685 by Louis XIV.",
     "start_year": 1598, "start_month": 4, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Edict_of_Nantes",
     "priorities": pri(900_000, france=920_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Wars of Religion"},

    {"type": "event", "title": "Revocation of the Edict of Nantes",
     "description": "Louis XIV revokes Henry IV's edict; Huguenots emigrate en masse; significant economic and demographic damage to France.",
     "start_year": 1685, "start_month": 10, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Edict_of_Fontainebleau",
     "priorities": pri(870_000, france=900_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Siege of La Rochelle (1627-1628)",
     "description": "Richelieu's royal forces crush the last great Huguenot stronghold; effective end of Huguenot political-military power.",
     "start_year": 1627, "start_month": 9, "start_day": 10, "end_year": 1628, "end_month": 10, "end_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_La_Rochelle",
     "priorities": pri(820_000, france=860_000),
     "region_weights": RW_EU},

    # =================================================================
    # EASTERN FRONT WW2
    # =================================================================
    {"type": "event", "title": "Operation Barbarossa",
     "description": "Hitler's invasion of the Soviet Union opens the Eastern Front; ~3 million Axis troops attack across 1,800-mile front.",
     "start_year": 1941, "start_month": 6, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Operation_Barbarossa",
     "priorities": pri(980_000, **{"ww2": 970_000}, germany=950_000),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Siege of Leningrad",
     "description": "Germans besiege Leningrad for 872 days; ~1 million civilians starve to death; longest siege of any modern major city.",
     "start_year": 1941, "start_month": 9, "start_day": 8, "end_year": 1944, "end_month": 1, "end_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Leningrad",
     "priorities": pri(940_000, **{"ww2": 950_000}),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Battle of Moscow",
     "description": "Soviets stop the Wehrmacht at the gates of Moscow in December 1941; first major German defeat; Blitzkrieg myth shattered.",
     "start_year": 1941, "start_month": 10, "start_day": 2, "end_year": 1942, "end_month": 1, "end_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Moscow",
     "priorities": pri(900_000, **{"ww2": 920_000}),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Battle of Stalingrad",
     "description": "Five-month battle for the Volga city; entire German Sixth Army surrenders; turning point of the war in Europe.",
     "start_year": 1942, "start_month": 8, "start_day": 23, "end_year": 1943, "end_month": 2, "end_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Stalingrad",
     "priorities": pri(990_000, **{"ww2": 980_000}, germany=950_000),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Battle of Kursk",
     "description": "Largest tank battle in history; Soviets blunt Hitler's last great Eastern offensive; ends German strategic initiative.",
     "start_year": 1943, "start_month": 7, "start_day": 5, "end_month": 8, "end_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Kursk",
     "priorities": pri(930_000, **{"ww2": 940_000}),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Operation Bagration",
     "description": "Soviet summer offensive destroys German Army Group Centre; Red Army drives from Belarus to the Vistula in six weeks.",
     "start_year": 1944, "start_month": 6, "start_day": 22, "end_month": 8, "end_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Operation_Bagration",
     "priorities": pri(870_000, **{"ww2": 900_000}),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Warsaw Uprising",
     "description": "Polish Home Army rises against Nazi occupation; Soviets halt across the Vistula; 200,000 Poles killed; Warsaw flattened.",
     "start_year": 1944, "start_month": 8, "start_day": 1, "end_month": 10, "end_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Warsaw_Uprising",
     "priorities": pri(890_000, **{"ww2": 910_000}),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "World War II"},

    # =================================================================
    # NORTH AFRICA WW2
    # =================================================================
    {"type": "event", "title": "North African campaign",
     "description": "British Commonwealth, Free French and American forces battle Italians and Germans across the desert of Libya, Egypt, Tunisia.",
     "start_year": 1940, "end_year": 1943,
     "wikipedia": "https://en.wikipedia.org/wiki/North_African_campaign",
     "priorities": pri(890_000, **{"ww2": 910_000}, england=900_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "World War II"},

    {"type": "person", "title": "Erwin Rommel",
     "description": "German general; \"Desert Fox\" of the Afrika Korps; later in Normandy; implicated in 20 July plot, forced to commit suicide.",
     "start_year": 1891, "end_year": 1944, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Erwin_Rommel",
     "priorities": pri(900_000, **{"ww2": 920_000}, germany=910_000, people=910_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Second Battle of El Alamein",
     "description": "Montgomery's British Eighth Army defeats Rommel's Panzerarmee Afrika; turning point of the desert war.",
     "start_year": 1942, "start_month": 10, "start_day": 23, "end_month": 11, "end_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Battle_of_El_Alamein",
     "priorities": pri(910_000, **{"ww2": 930_000}, england=910_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "North African campaign"},

    {"type": "event", "title": "Operation Torch",
     "description": "Allied amphibious landings in Vichy-controlled Morocco and Algeria; Eisenhower's first major Allied command.",
     "start_year": 1942, "start_month": 11, "start_day": 8, "end_month": 11, "end_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Operation_Torch",
     "priorities": pri(870_000, **{"ww2": 900_000}, usa=870_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "North African campaign"},

    {"type": "event", "title": "Tunisia campaign",
     "description": "Final Axis defeat in Africa; ~270,000 Italian and German soldiers surrender; Axis presence in North Africa ends.",
     "start_year": 1942, "start_month": 11, "start_day": 17, "end_year": 1943, "end_month": 5, "end_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Tunisia_campaign",
     "priorities": pri(830_000, **{"ww2": 870_000}),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "North African campaign"},

    {"type": "person", "title": "Bernard Montgomery",
     "description": "British field marshal; victor at El Alamein; led 21st Army Group from Normandy to Germany; theatrical commander.",
     "start_year": 1887, "end_year": 1976, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Bernard_Montgomery",
     "priorities": pri(890_000, england=910_000, **{"ww2": 910_000}, people=900_000),
     "region_weights": RW_EU},

    # =================================================================
    # ITALIAN RENAISSANCE ART MASTERS
    # =================================================================
    {"type": "person", "title": "Sandro Botticelli",
     "description": "Florentine Renaissance painter; The Birth of Venus, Primavera; later influenced by Savonarola and abandoned mythological subjects.",
     "start_year": 1445, "end_year": 1510, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Sandro_Botticelli",
     "priorities": pri(910_000, renaissance=940_000, people=920_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_EU},

    {"type": "art", "title": "Botticelli's Primavera",
     "description": "Florentine Renaissance allegory of Spring; Venus, Mercury, the Three Graces, Flora; commissioned for the Medici.",
     "start_year": 1482, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Primavera_(Botticelli)",
     "priorities": pri(890_000, renaissance=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Renaissance"},

    {"type": "art", "title": "Botticelli's The Birth of Venus",
     "description": "Iconic painting of Venus emerging from the sea on a scallop shell; one of the defining images of the Italian Renaissance.",
     "start_year": 1486, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Birth_of_Venus",
     "priorities": pri(940_000, renaissance=950_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Renaissance"},

    {"type": "person", "title": "Donatello",
     "description": "Florentine sculptor; bronze David first free-standing nude since antiquity; statues of Gattamelata; defined Renaissance sculpture.",
     "start_year": 1386, "end_year": 1466, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Donatello",
     "priorities": pri(890_000, renaissance=920_000, people=900_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Filippo Brunelleschi",
     "description": "Florentine architect; designed the dome of Florence Cathedral; pioneered linear perspective in painting.",
     "start_year": 1377, "end_year": 1446, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Filippo_Brunelleschi",
     "priorities": pri(910_000, renaissance=940_000, people=920_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_EU},

    {"type": "event", "title": "Dome of Florence Cathedral completed",
     "description": "Brunelleschi's masterpiece; largest masonry dome in the world; engineering breakthrough that defined the Italian Renaissance.",
     "start_year": 1436, "start_month": 8, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Florence_Cathedral",
     "priorities": pri(910_000, renaissance=940_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Renaissance"},

    {"type": "person", "title": "Titian",
     "description": "Venetian Renaissance painter; greatest colourist of his generation; portraits of emperors and popes; long career into late style.",
     "start_year": 1488, "end_year": 1576, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Titian",
     "priorities": pri(900_000, renaissance=930_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Lorenzo de' Medici",
     "description": "Banker and de-facto ruler of Florence; \"il Magnifico\"; patron of Botticelli, Michelangelo, the Platonic Academy.",
     "start_year": 1449, "end_year": 1492, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Lorenzo_de%27_Medici",
     "priorities": pri(910_000, renaissance=940_000, people=920_000),
     "region_weights": RW_EU},

    {"type": "person", "title": "Girolamo Savonarola",
     "description": "Dominican friar; preached apocalyptic reform in 1490s Florence; \"Bonfire of the Vanities\"; excommunicated and burned in 1498.",
     "start_year": 1452, "end_year": 1498, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Girolamo_Savonarola",
     "priorities": pri(870_000, renaissance=900_000, people=890_000),
     "region_weights": RW_EU},

    # =================================================================
    # ACHAEMENID PERSIAN EMPIRE
    # =================================================================
    {"type": "event", "title": "Achaemenid Persian Empire",
     "description": "Greatest empire of antiquity by population; from the Aegean to the Indus; founded by Cyrus the Great; ended by Alexander.",
     "start_year": -550, "end_year": -330,
     "wikipedia": "https://en.wikipedia.org/wiki/Achaemenid_Empire",
     "priorities": pri(950_000),
     "region_weights": RW_PERSIA},

    {"type": "person", "title": "Cyrus the Great",
     "description": "Founder of the Persian Achaemenid Empire; tolerant of subject peoples; freed Jews from Babylonian captivity; biblical 'anointed one'.",
     "start_year": -600, "end_year": -530, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Cyrus_the_Great",
     "priorities": pri(950_000, people=950_000),
     "region_weights": RW_PERSIA},

    {"type": "person", "title": "Darius the Great",
     "description": "Achaemenid king; organised the empire into satrapies; built Persepolis; defeated at Marathon by Athenians.",
     "start_year": -550, "end_year": -486, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Darius_the_Great",
     "priorities": pri(910_000, people=920_000),
     "region_weights": RW_PERSIA},

    {"type": "person", "title": "Xerxes I",
     "description": "Achaemenid king; led second Persian invasion of Greece; defeated at Salamis and Plataea.",
     "start_year": -519, "end_year": -465, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Xerxes_I",
     "priorities": pri(900_000, people=910_000),
     "region_weights": RW_PERSIA},

    {"type": "event", "title": "Cyrus conquers Babylon",
     "description": "Persian capture of Babylon ends the Neo-Babylonian empire; Cyrus permits return of the Jewish exiles.",
     "start_year": -539, "start_month": 10, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Fall_of_Babylon",
     "priorities": pri(900_000),
     "region_weights": RW_PERSIA,
     "first_zoom_out": "Achaemenid Persian Empire"},

    {"type": "event", "title": "Persepolis built",
     "description": "Darius the Great founds the ceremonial capital of the Persian Empire; vast palace complex; burned by Alexander in 330 BCE.",
     "start_year": -518, "end_year": -330,
     "wikipedia": "https://en.wikipedia.org/wiki/Persepolis",
     "priorities": pri(890_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_PERSIA,
     "first_zoom_out": "Achaemenid Persian Empire"},

    {"type": "person", "title": "Zoroaster",
     "description": "Persian prophet; founded Zoroastrianism; emphasised cosmic struggle between good (Ahura Mazda) and evil; influenced Judaism and Christianity.",
     "start_year": -1200, "end_year": -1100, "is_full_life": True, "date_uncertain": True,
     "display_date": "exact dates disputed; c. 1500-1000 BCE",
     "wikipedia": "https://en.wikipedia.org/wiki/Zoroaster",
     "priorities": pri(880_000, people=900_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_PERSIA},

    # =================================================================
    # PHARAONIC EGYPT
    # =================================================================
    {"type": "event", "title": "Old Kingdom of Egypt",
     "description": "Egyptian dynasties 3-6; age of pyramid-building; centralised divine kingship; ends in regional fragmentation (First Intermediate Period).",
     "start_year": -2686, "end_year": -2181,
     "wikipedia": "https://en.wikipedia.org/wiki/Old_Kingdom_of_Egypt",
     "priorities": pri(910_000),
     "region_weights": RW_EGYPT},

    {"type": "event", "title": "Great Pyramid of Giza built",
     "description": "Khufu's tomb; tallest human-made structure for 3,800 years; only one of the Seven Wonders of the Ancient World still standing.",
     "start_year": -2580, "end_year": -2560, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Great_Pyramid_of_Giza",
     "priorities": pri(960_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_EGYPT,
     "first_zoom_out": "Old Kingdom of Egypt"},

    {"type": "event", "title": "Middle Kingdom of Egypt",
     "description": "Dynasties 11-12; reunification under Mentuhotep II; literary classics composed; ends with Hyksos invasions.",
     "start_year": -2055, "end_year": -1650,
     "wikipedia": "https://en.wikipedia.org/wiki/Middle_Kingdom_of_Egypt",
     "priorities": pri(840_000),
     "region_weights": RW_EGYPT},

    {"type": "event", "title": "New Kingdom of Egypt",
     "description": "Dynasties 18-20; imperial age of Egypt; great pharaohs Hatshepsut, Thutmose III, Akhenaten, Tutankhamun, Ramesses II; Battle of Kadesh.",
     "start_year": -1550, "end_year": -1077,
     "wikipedia": "https://en.wikipedia.org/wiki/New_Kingdom_of_Egypt",
     "priorities": pri(900_000),
     "region_weights": RW_EGYPT},

    {"type": "person", "title": "Hatshepsut",
     "description": "Female pharaoh of the 18th Dynasty; long, prosperous reign; trade expeditions to Punt; monumental temple at Deir el-Bahari.",
     "start_year": -1507, "end_year": -1458, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hatshepsut",
     "priorities": pri(890_000, people=910_000),
     "region_weights": RW_EGYPT,
     "first_zoom_out": "New Kingdom of Egypt"},

    {"type": "person", "title": "Akhenaten",
     "description": "18th-Dynasty pharaoh; abandoned traditional polytheism for the sun-god Aten; built new capital at Amarna; reforms reversed after his death.",
     "start_year": -1380, "end_year": -1336, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Akhenaten",
     "priorities": pri(910_000, people=920_000),
     "region_weights": RW_EGYPT,
     "first_zoom_out": "New Kingdom of Egypt"},

    {"type": "person", "title": "Tutankhamun",
     "description": "18th-Dynasty boy-pharaoh; reversed Akhenaten's reforms; tomb discovered intact by Howard Carter in 1922.",
     "start_year": -1341, "end_year": -1323, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tutankhamun",
     "priorities": pri(940_000, people=940_000),
     "region_weights": RW_EGYPT},

    {"type": "person", "title": "Ramesses II (the Great)",
     "description": "19th-Dynasty pharaoh; one of Egypt's most celebrated rulers; 66-year reign; Battle of Kadesh against the Hittites; monumental building.",
     "start_year": -1303, "end_year": -1213, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ramesses_II",
     "priorities": pri(930_000, people=940_000),
     "region_weights": RW_EGYPT,
     "first_zoom_out": "New Kingdom of Egypt"},

    {"type": "event", "title": "Battle of Kadesh",
     "description": "Pharaoh Ramesses II vs Hittite Muwatalli II in modern Syria; first battle in history with detailed tactical records; ends in stalemate.",
     "start_year": -1274, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Kadesh",
     "priorities": pri(870_000),
     "region_weights": RW_EGYPT,
     "first_zoom_out": "New Kingdom of Egypt"},

    {"type": "event", "title": "Discovery of Tutankhamun's tomb",
     "description": "Howard Carter and Lord Carnarvon open the tomb of Tutankhamun in the Valley of the Kings; greatest archaeological find of the 20th century.",
     "start_year": 1922, "start_month": 11, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Tutankhamun",
     "priorities": pri(920_000, england=860_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Rosetta Stone discovered",
     "description": "French soldiers in Napoleon's Egyptian expedition find the trilingual stone; Champollion deciphers hieroglyphics in 1822.",
     "start_year": 1799, "start_month": 7, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Rosetta_Stone",
     "priorities": pri(910_000, france=860_000),
     "region_weights": RW_GLOBAL},

    # =================================================================
    # ROMAN EMPERORS + EARLY CHRISTIANITY
    # =================================================================
    {"type": "person", "title": "Saint Paul",
     "description": "Jewish Pharisee turned Christian apostle; brought Christianity to gentiles; epistles foundational to Christian theology.",
     "start_year": 5, "end_year": 67, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Paul_the_Apostle",
     "priorities": pri(940_000, people=940_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_EU},

    {"type": "event", "title": "Council of Nicaea (325) — christological",
     "description": "First ecumenical council; condemned Arianism; defined Christ as 'consubstantial' with the Father; produced Nicene Creed.",
     "start_year": 325, "start_month": 5, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Council_of_Nicaea",
     "priorities": pri(900_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Augustine of Hippo",
     "description": "North African bishop; Confessions, City of God; defining theologian of Latin Christianity for a millennium.",
     "start_year": 354, "end_year": 430, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Augustine_of_Hippo",
     "priorities": pri(950_000, people=950_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Saint Benedict of Nursia",
     "description": "Founder of Western monasticism; his Rule shaped European religious life for over a millennium.",
     "start_year": 480, "end_year": 547, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Benedict_of_Nursia",
     "priorities": pri(870_000, people=890_000, **{"arts-and-thoughts": 890_000}),
     "region_weights": RW_EU},

    {"type": "event", "title": "Conversion of Constantine",
     "description": "Constantine's vision before Milvian Bridge marks his turn to Christianity; legalised by Edict of Milan; transforms the religion's status.",
     "start_year": 312, "start_month": 10, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Constantine_the_Great_and_Christianity",
     "priorities": pri(930_000),
     "region_weights": RW_EU},

    # =================================================================
    # TANG / SONG / MING DETAIL
    # =================================================================
    {"type": "event", "title": "Tang reopens the Silk Road",
     "description": "Tang dynasty extends control across Central Asia; cosmopolitan capital at Chang'an attracts Persian, Sogdian, Korean, Japanese visitors.",
     "start_year": 640, "end_year": 750, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tang_dynasty",
     "priorities": pri(870_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Tang dynasty"},

    {"type": "event", "title": "Battle of Talas",
     "description": "Abbasid army defeats Tang force at the edge of Central Asia; Chinese papermaking technology captured and spreads to the Islamic world.",
     "start_year": 751, "start_month": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Talas",
     "priorities": pri(870_000, china=900_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Tang dynasty"},

    {"type": "event", "title": "Five Dynasties and Ten Kingdoms period",
     "description": "Half-century of fragmentation between Tang and Song; rapid succession of short-lived north Chinese dynasties.",
     "start_year": 907, "end_year": 960,
     "wikipedia": "https://en.wikipedia.org/wiki/Five_Dynasties_and_Ten_Kingdoms_period",
     "priorities": pri(820_000),
     "region_weights": RW_CHINA},

    {"type": "event", "title": "Wang Anshi reforms",
     "description": "Song chancellor Wang Anshi launches sweeping New Policies — state credit, agriculture reform, conscription; bitterly opposed and reversed.",
     "start_year": 1069, "end_year": 1076,
     "wikipedia": "https://en.wikipedia.org/wiki/Wang_Anshi",
     "priorities": pri(830_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Song dynasty"},

    {"type": "event", "title": "Yongle Emperor moves capital to Beijing",
     "description": "Ming Yongle moves capital from Nanjing; builds the Forbidden City; commissions Zheng He's voyages and the Yongle Encyclopedia.",
     "start_year": 1421, "start_month": 2, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Yongle_Emperor",
     "priorities": pri(900_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Ming dynasty"},

    {"type": "event", "title": "Imjin War (Korean view)",
     "description": "Korea under Yi dynasty defends against Japanese invasions; Admiral Yi Sun-sin's turtle ships defeat the Japanese navy.",
     "start_year": 1592, "end_year": 1598,
     "wikipedia": "https://en.wikipedia.org/wiki/Japanese_invasions_of_Korea_(1592%E2%80%931598)",
     "priorities": pri(870_000),
     "region_weights": RW_CHINA},

    {"type": "person", "title": "Yi Sun-sin",
     "description": "Korean admiral; turtle-ship fleet defeated Japanese navy in 23 engagements during the Imjin War; killed at Battle of Noryang Point.",
     "start_year": 1545, "end_year": 1598, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Yi_Sun-sin",
     "priorities": pri(870_000, people=890_000),
     "region_weights": RW_CHINA},

    # =================================================================
    # MISC MODERN
    # =================================================================
    {"type": "event", "title": "9/11 attacks",
     "description": "Al-Qaeda hijackers crash four airliners into the World Trade Center, Pentagon, and a Pennsylvania field; ~2,977 killed; triggers War on Terror.",
     "start_year": 2001, "start_month": 9, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/September_11_attacks",
     "priorities": pri(990_000, usa=990_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Global financial crisis",
     "description": "Subprime mortgage collapse becomes a worldwide banking and recession crisis; Lehman Brothers fails; trillion-dollar bailouts.",
     "start_year": 2007, "start_month": 8, "end_year": 2009, "end_month": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Financial_crisis_of_2007%E2%80%932008",
     "priorities": pri(960_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Lehman Brothers collapse",
     "description": "150-year-old investment bank files for bankruptcy; cascading global financial panic; triggers massive central bank interventions.",
     "start_year": 2008, "start_month": 9, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Bankruptcy_of_Lehman_Brothers",
     "priorities": pri(920_000, usa=910_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Global financial crisis"},

    {"type": "event", "title": "Eurozone debt crisis",
     "description": "Greek default fears spread to Ireland, Portugal, Spain, Italy; ECB and IMF impose austerity-conditioned bailouts; tests the Euro.",
     "start_year": 2010, "end_year": 2015,
     "wikipedia": "https://en.wikipedia.org/wiki/European_debt_crisis",
     "priorities": pri(910_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Same-sex marriage US Supreme Court ruling",
     "description": "Obergefell v. Hodges legalises same-sex marriage in all 50 US states; landmark civil-rights decision.",
     "start_year": 2015, "start_month": 6, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Obergefell_v._Hodges",
     "priorities": pri(910_000, usa=940_000),
     "region_weights": RW_AMER},

    {"type": "event", "title": "MeToo movement",
     "description": "Allegations against Hollywood producer Harvey Weinstein launch global #MeToo movement against sexual harassment.",
     "start_year": 2017, "start_month": 10, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Me_Too_movement",
     "priorities": pri(910_000, usa=910_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Storming of the US Capitol",
     "description": "Trump supporters storm the US Capitol to stop certification of the 2020 election; five killed; lasting effects on US democracy.",
     "start_year": 2021, "start_month": 1, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/January_6_United_States_Capitol_attack",
     "priorities": pri(940_000, usa=970_000),
     "region_weights": RW_AMER},
]


def main() -> int:
    base = next_available_id()
    for i, en in enumerate(ENTRIES):
        en["id"] = base + i
    n = append_entries(ENTRIES)
    print(f"Appended {n} entries (IDs {base}..{base+n-1}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
