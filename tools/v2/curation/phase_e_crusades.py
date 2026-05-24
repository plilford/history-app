"""
Phase E1 — Crusades timeline. New slug 'crusades'.

Scope: from precursors (Reconquista, Norman Sicily) through Council of
Clermont 1095, the Latin East, military orders, individual crusades, the
Mongol/Mamluk interplay, the fall of Acre 1291, and the long Reconquista
tail through 1492.

Priority calibration follows the same convention used for the recent
timelines: master priority calibrated against the existing dataset; per-slug
priority = master + 30k for strong-anchored, master - 90k if multi-regional.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_CRUSADES = {"europe": 10, "americas": 1, "asia": 9, "australasia": 1, "africa": 6}
RW_EU = {"europe": 10, "americas": 2, "asia": 3, "australasia": 1, "africa": 3}


def c(master_pri: int, crusade_pri: int | None = None, **extra) -> dict:
    if crusade_pri is None:
        crusade_pri = min(999_000, master_pri + 30_000)
    out = {"master": master_pri, "crusades": crusade_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- Precursors -----
    {"type": "event", "title": "Reconquista begins (Battle of Covadonga)",
     "description": "Pelayo of Asturias defeats a Moorish raiding force; traditional start of the 700-year Christian reconquest of Iberia.",
     "start_year": 722, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Covadonga",
     "priorities": c(870_000), "region_weights": RW_EU},

    {"type": "event", "title": "Norman conquest of Sicily",
     "description": "Robert Guiscard and Roger I drive Muslim emirs from Sicily over 30 years; sets template for crusader-state administration.",
     "start_year": 1061, "end_year": 1091,
     "wikipedia": "https://en.wikipedia.org/wiki/Norman_conquest_of_southern_Italy",
     "priorities": c(870_000), "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Manzikert",
     "description": "Seljuk Turks crush Byzantine army; Anatolia opens to Turkish settlement; Byzantine appeal for Western aid triggers the First Crusade.",
     "start_year": 1071, "start_month": 8, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Manzikert",
     "priorities": c(890_000, **{"roman-history": 870_000}), "region_weights": RW_CRUSADES},

    # ----- First Crusade -----
    {"type": "event", "title": "Council of Clermont",
     "description": "Pope Urban II preaches the First Crusade at Clermont in southern France; rallying cry 'Deus vult' (God wills it).",
     "start_year": 1095, "start_month": 11, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Council_of_Clermont",
     "priorities": c(950_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Crusades"},

    {"type": "event", "title": "First Crusade",
     "description": "Western army of ~60,000 marches via Constantinople to the Levant; takes Antioch and Jerusalem; sets up four crusader states.",
     "start_year": 1096, "end_year": 1099,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Crusade",
     "priorities": c(940_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "People's Crusade",
     "description": "Pre-army peasant column under Peter the Hermit massacres Rhineland Jews, marches to Constantinople, slaughtered by Turks at Civetot.",
     "start_year": 1096, "start_month": 4, "end_month": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/People%27s_Crusade",
     "priorities": c(800_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "First Crusade"},

    {"type": "event", "title": "Siege of Antioch",
     "description": "Crusaders take Antioch after eight-month siege; the Holy Lance discovered there inspires their breakout victory over Kerbogha's relief army.",
     "start_year": 1097, "start_month": 10, "start_day": 21, "end_year": 1098, "end_month": 6, "end_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Antioch",
     "priorities": c(870_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "First Crusade"},

    {"type": "event", "title": "Siege of Jerusalem (1099)",
     "description": "Crusaders storm Jerusalem after five-week siege; horrific massacre of Muslim and Jewish inhabitants follows.",
     "start_year": 1099, "start_month": 6, "start_day": 7, "end_month": 7, "end_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Jerusalem_(1099)",
     "priorities": c(920_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "First Crusade"},

    {"type": "event", "title": "Kingdom of Jerusalem founded",
     "description": "Godfrey of Bouillon refuses crown but accepts 'Advocate of the Holy Sepulchre'; his brother Baldwin I is crowned king on Christmas Day 1100.",
     "start_year": 1099, "start_month": 7, "start_day": 22, "end_year": 1291,
     "wikipedia": "https://en.wikipedia.org/wiki/Kingdom_of_Jerusalem",
     "priorities": c(900_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "County of Edessa",
     "description": "First Latin state in the east; falls to Zengi in 1144, triggering the Second Crusade.",
     "start_year": 1098, "end_year": 1150,
     "wikipedia": "https://en.wikipedia.org/wiki/County_of_Edessa",
     "priorities": c(810_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Principality of Antioch",
     "description": "Latin state ruled by Bohemond of Taranto and his descendants; survives until Baibars sacks Antioch in 1268.",
     "start_year": 1098, "end_year": 1268,
     "wikipedia": "https://en.wikipedia.org/wiki/Principality_of_Antioch",
     "priorities": c(820_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "County of Tripoli",
     "description": "Fourth crusader state, established by Raymond IV of Toulouse and his descendants; falls to the Mamluks in 1289.",
     "start_year": 1102, "end_year": 1289,
     "wikipedia": "https://en.wikipedia.org/wiki/County_of_Tripoli",
     "priorities": c(810_000), "region_weights": RW_CRUSADES},

    # ----- Military orders -----
    {"type": "event", "title": "Knights Hospitaller founded",
     "description": "Order of St John established in Jerusalem to care for sick pilgrims; militarised in the 1130s; survives today as the Order of Malta.",
     "start_year": 1099, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Knights_Hospitaller",
     "priorities": c(880_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Knights Templar founded",
     "description": "Hugh de Payens founds the Order of the Temple to guard pilgrim routes; becomes a major military and banking institution before its 1312 suppression.",
     "start_year": 1119, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Knights_Templar",
     "priorities": c(900_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Teutonic Order founded",
     "description": "German military-religious order originating in Acre; from 1226 it crusades against the pagan Prussians and shapes Baltic history.",
     "start_year": 1190,
     "wikipedia": "https://en.wikipedia.org/wiki/Teutonic_Order",
     "priorities": c(870_000, **{"germany": 880_000}), "region_weights": RW_CRUSADES},

    # ----- Second Crusade -----
    {"type": "event", "title": "Fall of Edessa to Zengi",
     "description": "Atabeg Zengi captures the County of Edessa, the first crusader state; Bernard of Clairvaux preaches the Second Crusade in response.",
     "start_year": 1144, "start_month": 12, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Edessa",
     "priorities": c(830_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Second Crusade",
     "description": "Conrad III of Germany and Louis VII of France lead disastrous expedition; fails at Damascus, but Lisbon falls to a Reconquista detachment.",
     "start_year": 1147, "end_year": 1149,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Crusade",
     "priorities": c(890_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Wendish Crusade",
     "description": "Saxon and Danish crusaders attack pagan Slavs east of the Elbe; first northern crusade, paralleling the Second Crusade in the Levant.",
     "start_year": 1147,
     "wikipedia": "https://en.wikipedia.org/wiki/Wendish_Crusade",
     "priorities": c(770_000, **{"germany": 800_000}), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Second Crusade"},

    {"type": "event", "title": "Capture of Lisbon",
     "description": "Crusader fleet bound for the Levant detours to help Afonso I of Portugal take Lisbon; a rare Second Crusade success.",
     "start_year": 1147, "start_month": 7, "start_day": 1, "end_month": 10, "end_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Lisbon",
     "priorities": c(800_000), "region_weights": RW_EU,
     "first_zoom_out": "Second Crusade"},

    # ----- Saladin and Third Crusade -----
    {"type": "person", "title": "Saladin",
     "description": "Kurdish sultan; founder of the Ayyubid dynasty; unified Egypt and Syria, recaptured Jerusalem at Hattin in 1187.",
     "start_year": 1137, "end_year": 1193, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Saladin",
     "priorities": c(940_000, people=950_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Battle of Hattin",
     "description": "Saladin annihilates the kingdom of Jerusalem's army at the Horns of Hattin; capture of the True Cross and most of the Latin army.",
     "start_year": 1187, "start_month": 7, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Hattin",
     "priorities": c(920_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Saladin retakes Jerusalem",
     "description": "Three months after Hattin, Saladin's army takes Jerusalem after a brief siege; treats inhabitants far more leniently than the 1099 crusaders did.",
     "start_year": 1187, "start_month": 9, "start_day": 20, "end_month": 10, "end_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Jerusalem_(1187)",
     "priorities": c(920_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Third Crusade",
     "description": "Richard the Lionheart, Philip II of France and Frederick Barbarossa respond to Hattin; recovers coast but not Jerusalem.",
     "start_year": 1189, "end_year": 1192,
     "wikipedia": "https://en.wikipedia.org/wiki/Third_Crusade",
     "priorities": c(930_000, **{"england": 880_000}), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Drowning of Barbarossa",
     "description": "Frederick I Barbarossa drowns crossing the Saleph river in Anatolia; most of his army turns back, crippling the German contribution to the Third Crusade.",
     "start_year": 1190, "start_month": 6, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Frederick_I,_Holy_Roman_Emperor",
     "priorities": c(820_000, **{"germany": 830_000}), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Third Crusade"},

    {"type": "event", "title": "Siege of Acre (1189-1191)",
     "description": "Two-year siege; Acre falls to combined crusader forces under Richard I and Philip II; recovery base for the next century.",
     "start_year": 1189, "start_month": 8, "end_year": 1191, "end_month": 7, "end_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Acre_(1189%E2%80%931191)",
     "priorities": c(840_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Third Crusade"},

    {"type": "event", "title": "Massacre of Ayyadieh",
     "description": "Richard I orders the execution of 2,700 Muslim prisoners outside Acre after Saladin delays the agreed ransom.",
     "start_year": 1191, "start_month": 8, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Massacre_at_Ayyadieh",
     "priorities": c(770_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Third Crusade"},

    {"type": "event", "title": "Battle of Arsuf",
     "description": "Richard I defeats Saladin in a set-piece battle on the coast road from Acre to Jaffa; restores crusader military credibility.",
     "start_year": 1191, "start_month": 9, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Arsuf",
     "priorities": c(820_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Third Crusade"},

    {"type": "event", "title": "Treaty of Jaffa (1192)",
     "description": "Richard and Saladin agree a three-year truce; Christians retain coast from Tyre to Jaffa; pilgrims granted access to Jerusalem.",
     "start_year": 1192, "start_month": 9, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Jaffa_(1192)",
     "priorities": c(800_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Third Crusade"},

    # ----- Fourth Crusade -----
    {"type": "event", "title": "Fourth Crusade",
     "description": "Diverted from Egypt by Venetian finance and Byzantine palace politics; ends with the sack of Constantinople in 1204.",
     "start_year": 1202, "end_year": 1204,
     "wikipedia": "https://en.wikipedia.org/wiki/Fourth_Crusade",
     "priorities": c(910_000, **{"roman-history": 880_000}), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Sack of Zara",
     "description": "Crusaders sack the Christian city of Zara to pay their Venetian debt; Pope Innocent III excommunicates the army.",
     "start_year": 1202, "start_month": 11, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Zara",
     "priorities": c(780_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Fourth Crusade"},

    {"type": "event", "title": "Sack of Constantinople by Fourth Crusade",
     "description": "Three days of looting and slaughter; Byzantine treasures shipped to Venice (the horses of San Marco); Latin Empire installed.",
     "start_year": 1204, "start_month": 4, "start_day": 12, "end_month": 4, "end_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Sack_of_Constantinople",
     "priorities": c(940_000, **{"roman-history": 900_000}), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Fourth Crusade"},

    # ----- 13th-century crusades -----
    {"type": "event", "title": "Albigensian Crusade",
     "description": "Pope Innocent III launches crusade against Cathar heretics in Languedoc; twenty years of brutal warfare ends Occitan independence.",
     "start_year": 1209, "end_year": 1229,
     "wikipedia": "https://en.wikipedia.org/wiki/Albigensian_Crusade",
     "priorities": c(890_000, **{"france": 880_000}), "region_weights": RW_EU},

    {"type": "event", "title": "Children's Crusade",
     "description": "Mass movement of young Europeans bound for the Holy Land; ends in dispersal, sale into slavery, or shipwreck. Largely legendary in detail.",
     "start_year": 1212, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Children%27s_Crusade",
     "priorities": c(800_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Fifth Crusade",
     "description": "Targets Egypt; takes Damietta, then disastrous march on Cairo collapses in the Nile floods.",
     "start_year": 1217, "end_year": 1221,
     "wikipedia": "https://en.wikipedia.org/wiki/Fifth_Crusade",
     "priorities": c(860_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Francis of Assisi meets Sultan al-Kamil",
     "description": "Francis crosses the front lines at Damietta to preach to the Ayyubid sultan; remarkable inter-faith encounter during a brutal war.",
     "start_year": 1219,
     "wikipedia": "https://en.wikipedia.org/wiki/Francis_of_Assisi",
     "priorities": c(820_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Fifth Crusade"},

    {"type": "event", "title": "Sixth Crusade",
     "description": "Excommunicated emperor Frederick II negotiates the return of Jerusalem from Sultan al-Kamil without significant fighting.",
     "start_year": 1228, "end_year": 1229,
     "wikipedia": "https://en.wikipedia.org/wiki/Sixth_Crusade",
     "priorities": c(880_000, **{"germany": 860_000}), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Khwarezmian sack of Jerusalem",
     "description": "Khwarezmian Turks displaced by Mongols sack Jerusalem; the city is permanently lost to the crusaders.",
     "start_year": 1244, "start_month": 7, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Jerusalem_(1244)",
     "priorities": c(830_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Seventh Crusade",
     "description": "Louis IX of France attacks Egypt; defeated at Mansurah, captured at Fariskur, ransomed for a colossal sum.",
     "start_year": 1248, "end_year": 1254,
     "wikipedia": "https://en.wikipedia.org/wiki/Seventh_Crusade",
     "priorities": c(880_000, **{"france": 870_000}), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Battle of Mansurah",
     "description": "Mamluks defeat Louis IX's army in the Nile delta; the king is captured and held for ransom.",
     "start_year": 1250, "start_month": 2, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Mansurah",
     "priorities": c(800_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Seventh Crusade"},

    {"type": "event", "title": "Mamluk Sultanate established",
     "description": "Egyptian slave-soldiers (Mamluks) overthrow the Ayyubids; Sultan Aybak founds the dynasty that will destroy the crusader states.",
     "start_year": 1250,
     "wikipedia": "https://en.wikipedia.org/wiki/Mamluk_Sultanate",
     "priorities": c(880_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Battle of Ain Jalut",
     "description": "Mamluks under Qutuz and Baibars defeat the Mongols in Galilee; first major Mongol defeat and turning point of Mongol expansion westward.",
     "start_year": 1260, "start_month": 9, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Ain_Jalut",
     "priorities": c(900_000), "region_weights": RW_CRUSADES},

    {"type": "person", "title": "Baibars",
     "description": "Mamluk sultan; conqueror of crusader fortresses (Antioch 1268, Krak des Chevaliers 1271); architect of the eradication of the Latin East.",
     "start_year": 1223, "end_year": 1277, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Baibars",
     "priorities": c(880_000, people=890_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Eighth Crusade",
     "description": "Louis IX's second crusade, against Tunis; the king dies of dysentery shortly after landing.",
     "start_year": 1270, "start_month": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Eighth_Crusade",
     "priorities": c(820_000, **{"france": 830_000}), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Ninth Crusade",
     "description": "Prince Edward of England's expedition; relieves Acre briefly but achieves nothing strategic.",
     "start_year": 1271, "end_year": 1272,
     "wikipedia": "https://en.wikipedia.org/wiki/Ninth_Crusade",
     "priorities": c(800_000, **{"england": 820_000}), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Fall of Krak des Chevaliers",
     "description": "Mamluk sultan Baibars takes the Hospitaller stronghold after a month-long siege; one of the great medieval fortresses in Crusader hands.",
     "start_year": 1271, "start_month": 3, "start_day": 3, "end_month": 4, "end_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Krak_des_Chevaliers",
     "priorities": c(820_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Fall of Antioch (1268)",
     "description": "Baibars sacks Antioch; 17,000 killed and 100,000 enslaved; the principality founded by Bohemond in 1098 ceases to exist.",
     "start_year": 1268, "start_month": 5, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Antioch_(1268)",
     "priorities": c(830_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Fall of Tripoli (1289)",
     "description": "Mamluk Sultan Qalawun takes Tripoli; the County of Tripoli, last crusader state on the mainland besides the Kingdom of Jerusalem, is destroyed.",
     "start_year": 1289, "start_month": 4, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Fall_of_Tripoli_(1289)",
     "priorities": c(840_000), "region_weights": RW_CRUSADES},

    {"type": "event", "title": "Fall of Acre",
     "description": "Sultan al-Ashraf Khalil takes the last major crusader city after a six-week siege; conventional end of the crusader states in the Levant.",
     "start_year": 1291, "start_month": 4, "start_day": 4, "end_month": 5, "end_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Fall_of_Acre",
     "priorities": c(910_000), "region_weights": RW_CRUSADES},

    # ----- Templar suppression -----
    {"type": "event", "title": "Arrest of the Knights Templar",
     "description": "Philip IV of France orders the simultaneous arrest of all Templars on Friday 13 October 1307; tortured confessions extracted.",
     "start_year": 1307, "start_month": 10, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Trials_of_the_Knights_Templar",
     "priorities": c(880_000, **{"france": 870_000}), "region_weights": RW_EU},

    {"type": "event", "title": "Suppression of the Templars",
     "description": "Pope Clement V dissolves the Knights Templar at the Council of Vienne; Grand Master Jacques de Molay burned in 1314.",
     "start_year": 1312, "start_month": 4, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Trials_of_the_Knights_Templar",
     "priorities": c(860_000), "region_weights": RW_EU,
     "first_zoom_out": "Arrest of the Knights Templar"},

    # ----- Northern crusades & Reconquista -----
    {"type": "event", "title": "Northern Crusades (Baltic)",
     "description": "Centuries-long campaign to convert and conquer pagan Slavs, Balts and Finns; carried out chiefly by the Teutonic and Sword orders.",
     "start_year": 1147, "end_year": 1410,
     "wikipedia": "https://en.wikipedia.org/wiki/Northern_Crusades",
     "priorities": c(840_000), "region_weights": RW_EU},

    {"type": "event", "title": "Battle on the Ice (Lake Peipus)",
     "description": "Alexander Nevsky defeats the Teutonic Knights on the frozen Lake Peipus; halts German eastward expansion against Novgorod.",
     "start_year": 1242, "start_month": 4, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_on_the_Ice",
     "priorities": c(850_000), "region_weights": RW_EU,
     "first_zoom_out": "Northern Crusades (Baltic)"},

    {"type": "event", "title": "Battle of Grunwald",
     "description": "Polish-Lithuanian army under Władysław II Jagiełło crushes the Teutonic Knights; effectively ends the Order's expansion.",
     "start_year": 1410, "start_month": 7, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Grunwald",
     "priorities": c(880_000), "region_weights": RW_EU,
     "first_zoom_out": "Northern Crusades (Baltic)"},

    {"type": "event", "title": "Battle of Las Navas de Tolosa",
     "description": "Coalition of Iberian Christian kingdoms crushes the Almohad caliphate; turns the Reconquista decisively in Christian favour.",
     "start_year": 1212, "start_month": 7, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Las_Navas_de_Tolosa",
     "priorities": c(890_000), "region_weights": RW_EU,
     "first_zoom_out": "Reconquista begins (Battle of Covadonga)"},

    {"type": "event", "title": "Fall of Granada",
     "description": "Catholic Monarchs Ferdinand and Isabella take Granada; 781-year Reconquista ends, freeing capital for Columbus's voyage.",
     "start_year": 1492, "start_month": 1, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Granada_War",
     "priorities": c(950_000), "region_weights": RW_EU,
     "first_zoom_out": "Reconquista begins (Battle of Covadonga)"},

    {"type": "event", "title": "Alhambra Decree",
     "description": "Ferdinand and Isabella order all Jews to convert or leave Spain; ends seven centuries of Sephardi presence in Iberia.",
     "start_year": 1492, "start_month": 3, "start_day": 31,
     "wikipedia": "https://en.wikipedia.org/wiki/Alhambra_Decree",
     "priorities": c(870_000), "region_weights": RW_EU,
     "first_zoom_out": "Reconquista begins (Battle of Covadonga)"},

    {"type": "event", "title": "Conquest of Constantinople (1453, crusader context)",
     "description": "Ottoman conquest of Constantinople; the last crusading appeal — Pope Pius II's call to crusade in 1463 — gains little traction.",
     "start_year": 1453, "start_month": 5, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Fall_of_Constantinople",
     "priorities": c(900_000), "region_weights": RW_CRUSADES,
     "first_zoom_out": "Crusades"},

    # ----- Late and ideological crusades -----
    {"type": "event", "title": "Hussite Wars",
     "description": "Five crusades launched by Sigismund and the papacy against Bohemian Hussite Protestants; ends in negotiated compromise.",
     "start_year": 1419, "end_year": 1434,
     "wikipedia": "https://en.wikipedia.org/wiki/Hussite_Wars",
     "priorities": c(840_000, **{"germany": 800_000}), "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Nicopolis",
     "description": "Last large international crusade; Ottoman Sultan Bayezid I crushes a Franco-Hungarian army outside Nicopolis on the Danube.",
     "start_year": 1396, "start_month": 9, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Nicopolis",
     "priorities": c(830_000), "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Varna",
     "description": "Polish-Hungarian crusade against the Ottomans destroyed at Varna; King Władysław III killed; effectively ends crusader land campaigns into the Balkans.",
     "start_year": 1444, "start_month": 11, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Varna",
     "priorities": c(820_000), "region_weights": RW_EU},

    {"type": "event", "title": "Siege of Vienna (1529)",
     "description": "Ottoman Suleiman the Magnificent fails to take Vienna; the high-water mark of Ottoman expansion in central Europe.",
     "start_year": 1529, "start_month": 9, "start_day": 27, "end_month": 10, "end_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Vienna",
     "priorities": c(880_000), "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Lepanto",
     "description": "Holy League fleet under Don Juan of Austria destroys the Ottoman navy in the Gulf of Patras; ends Ottoman naval supremacy in the Mediterranean.",
     "start_year": 1571, "start_month": 10, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Lepanto",
     "priorities": c(900_000), "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Vienna (1683)",
     "description": "Polish-Imperial relief force under Jan Sobieski crushes the Ottoman besieging army outside Vienna; conventional end of crusading-era European-Ottoman warfare.",
     "start_year": 1683, "start_month": 9, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Vienna",
     "priorities": c(900_000, **{"germany": 870_000}), "region_weights": RW_EU},

    # ----- People + miscellaneous -----
    {"type": "person", "title": "Godfrey of Bouillon",
     "description": "Duke of Lower Lorraine; foremost leader of the First Crusade; first ruler of the Kingdom of Jerusalem as 'Advocate of the Holy Sepulchre'.",
     "start_year": 1060, "end_year": 1100, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Godfrey_of_Bouillon",
     "priorities": c(850_000, people=860_000), "region_weights": RW_CRUSADES},

    {"type": "person", "title": "Bohemond of Taranto",
     "description": "Norman prince; leader of the First Crusade; founder of the Principality of Antioch.",
     "start_year": 1054, "end_year": 1111, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Bohemond_I_of_Antioch",
     "priorities": c(810_000, people=830_000), "region_weights": RW_CRUSADES},

    {"type": "person", "title": "Tancred of Hauteville (crusader)",
     "description": "Bohemond's nephew; took Bethlehem during the First Crusade; later regent of Antioch.",
     "start_year": 1075, "end_year": 1112, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tancred,_Prince_of_Galilee",
     "priorities": c(760_000, people=790_000), "region_weights": RW_CRUSADES},

    {"type": "person", "title": "Bernard of Clairvaux",
     "description": "Cistercian abbot; preacher of the Second Crusade; mystic and reformer; one of the most influential churchmen of the 12th century.",
     "start_year": 1090, "end_year": 1153, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Bernard_of_Clairvaux",
     "priorities": c(850_000, people=870_000), "region_weights": RW_CRUSADES},

    {"type": "person", "title": "Reynald of Châtillon",
     "description": "Notorious lord of Kerak; serial truce-breaker whose raids gave Saladin pretext for Hattin; personally beheaded by Saladin after capture.",
     "start_year": 1125, "end_year": 1187, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Raynald_of_Ch%C3%A2tillon",
     "priorities": c(770_000, people=800_000), "region_weights": RW_CRUSADES},

    {"type": "person", "title": "Frederick II (crusader emperor)",
     "description": "Hohenstaufen Holy Roman Emperor; led the Sixth Crusade despite excommunication; gained Jerusalem by treaty rather than battle; stupor mundi.",
     "start_year": 1194, "end_year": 1250, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Frederick_II,_Holy_Roman_Emperor",
     "priorities": c(900_000, people=910_000, **{"germany": 880_000}), "region_weights": RW_CRUSADES},

    {"type": "person", "title": "Louis IX of France",
     "description": "King and saint; led the Seventh and Eighth Crusades; reformed French law and administration; canonised in 1297.",
     "start_year": 1214, "end_year": 1270, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Louis_IX_of_France",
     "priorities": c(890_000, people=900_000, **{"france": 900_000}), "region_weights": RW_CRUSADES},
]


def main() -> int:
    base = next_available_id()
    for i, en in enumerate(ENTRIES):
        en["id"] = base + i
    n = append_entries(ENTRIES)
    print(f"Appended {n} Crusades entries (IDs {base}..{base+n-1}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
