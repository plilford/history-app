"""
Phase I2 — Ottoman timeline content + under-served umbrella deep-fill.

Sections:
  - Ottoman Empire: ~30 entries
  - Black Death depth: ~5
  - Spanish Civil War: a few more
  - Baroque music + early classical: ~10
  - Genpei / Russo-Japanese / Peninsular War children: ~10
  - Misc: medieval pandemics, more music + literature, science gaps
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_EU = {"europe": 10, "americas": 3, "asia": 3, "australasia": 1, "africa": 3}
RW_OTTOMAN = {"europe": 9, "americas": 1, "asia": 10, "australasia": 1, "africa": 6}
RW_JAPAN = {"europe": 4, "americas": 6, "asia": 10, "australasia": 4, "africa": 1}
RW_GLOBAL = {"europe": 8, "americas": 7, "asia": 5, "australasia": 3, "africa": 4}


def pri(master: int, **extras) -> dict:
    return {"master": master, **extras}


ENTRIES = [
    # =================================================================
    # OTTOMAN EMPIRE
    # =================================================================
    {"type": "event", "title": "Ottoman Empire",
     "description": "Turkic Sunni Muslim empire founded by Osman I; spanned three continents; capital Constantinople from 1453; dissolved 1922.",
     "start_year": 1299, "end_year": 1922,
     "wikipedia": "https://en.wikipedia.org/wiki/Ottoman_Empire",
     "priorities": pri(980_000, ottoman=999_000, **{"major-religions": 950_000, "islam": 970_000}),
     "region_weights": RW_OTTOMAN},

    {"type": "person", "title": "Osman I",
     "description": "Founder of the Ottoman dynasty; small Bey of Söğüt in northwestern Anatolia; expanded against weakened Byzantine empire.",
     "start_year": 1258, "end_year": 1326, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Osman_I",
     "priorities": pri(870_000, ottoman=920_000, people=890_000),
     "region_weights": RW_OTTOMAN},

    {"type": "person", "title": "Mehmed II (the Conqueror)",
     "description": "Ottoman sultan; conqueror of Constantinople; consolidated Ottoman rule across Anatolia and the Balkans.",
     "start_year": 1432, "end_year": 1481, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mehmed_II",
     "priorities": pri(930_000, ottoman=950_000, people=940_000),
     "region_weights": RW_OTTOMAN},

    {"type": "person", "title": "Suleiman the Magnificent",
     "description": "Tenth and longest-reigning Ottoman sultan; empire at its territorial and cultural peak; codified Ottoman law (Kanun).",
     "start_year": 1494, "end_year": 1566, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Suleiman_the_Magnificent",
     "priorities": pri(950_000, ottoman=970_000, people=950_000),
     "region_weights": RW_OTTOMAN},

    {"type": "event", "title": "Reign of Suleiman the Magnificent",
     "description": "Ottoman empire at its height; conquests in Hungary, North Africa, Mesopotamia; Topkapı reformed; Mimar Sinan's mosques.",
     "start_year": 1520, "end_year": 1566, "start_month": 9, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Reign_of_Suleiman_the_Magnificent",
     "priorities": pri(920_000, ottoman=950_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Battle of Mohács",
     "description": "Suleiman crushes the Hungarian army in two hours; King Louis II killed; opens conquest of Hungary; sets stage for Vienna 1529.",
     "start_year": 1526, "start_month": 8, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Moh%C3%A1cs",
     "priorities": pri(890_000, ottoman=920_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Ottoman conquest of Egypt",
     "description": "Selim I defeats Mamluks at Ridanieh; Egypt absorbed into Ottoman Empire; Ottomans become protectors of the Holy Cities.",
     "start_year": 1517, "start_month": 1, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Ottoman%E2%80%93Mamluk_War_(1516%E2%80%931517)",
     "priorities": pri(890_000, ottoman=920_000, islam=890_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "person", "title": "Mimar Sinan",
     "description": "Chief Ottoman architect under Suleiman, Selim II, Murad III; designed ~300 buildings including Süleymaniye and Selimiye mosques.",
     "start_year": 1489, "end_year": 1588, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mimar_Sinan",
     "priorities": pri(890_000, ottoman=920_000, people=910_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_OTTOMAN},

    {"type": "event", "title": "Selimiye Mosque completed",
     "description": "Mimar Sinan's masterpiece in Edirne; one of the great architectural achievements of Islamic civilisation.",
     "start_year": 1574, "start_month": 3, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Selimiye_Mosque",
     "priorities": pri(870_000, ottoman=910_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Topkapı Palace built",
     "description": "Mehmed II builds his new palace on the acropolis of old Constantinople; principal Ottoman residence for nearly 400 years.",
     "start_year": 1465, "end_year": 1478,
     "wikipedia": "https://en.wikipedia.org/wiki/Topkap%C4%B1_Palace",
     "priorities": pri(860_000, ottoman=910_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Treaty of Karlowitz",
     "description": "Ottoman defeat at Vienna 1683 leads to Habsburg-led coalition victory; Ottomans cede Hungary and Transylvania; first major territorial loss.",
     "start_year": 1699, "start_month": 1, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Karlowitz",
     "priorities": pri(850_000, ottoman=890_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Tulip era",
     "description": "Early-18th-century Ottoman cultural flowering under Ahmed III; embassies to Europe; printing press introduced; ended by Patrona Halil revolt.",
     "start_year": 1718, "end_year": 1730,
     "wikipedia": "https://en.wikipedia.org/wiki/Tulip_period",
     "priorities": pri(830_000, ottoman=880_000, **{"arts-and-thoughts": 850_000}),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Tanzimat reforms",
     "description": "Major Ottoman modernisation programme; legal equality regardless of religion, secular schools, conscription; transformed the empire's institutions.",
     "start_year": 1839, "end_year": 1876,
     "wikipedia": "https://en.wikipedia.org/wiki/Tanzimat",
     "priorities": pri(890_000, ottoman=940_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Crimean War (Ottoman view)",
     "description": "Ottoman empire allied with Britain and France against Russia; victory preserves the empire but at heavy cost.",
     "start_year": 1853, "end_year": 1856,
     "wikipedia": "https://en.wikipedia.org/wiki/Crimean_War",
     "priorities": pri(860_000, ottoman=900_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Greek War of Independence",
     "description": "Eight-year revolt establishes modern Greek state from Ottoman rule; British/French/Russian intervention at Navarino 1827.",
     "start_year": 1821, "end_year": 1832,
     "wikipedia": "https://en.wikipedia.org/wiki/Greek_War_of_Independence",
     "priorities": pri(900_000, ottoman=910_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Russo-Turkish War (1877-1878)",
     "description": "Russia defeats Ottomans; Treaty of San Stefano then Berlin Congress creates independent Romania, Serbia, Montenegro, autonomous Bulgaria.",
     "start_year": 1877, "start_month": 4, "start_day": 24, "end_year": 1878, "end_month": 3, "end_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Russo-Turkish_War_(1877%E2%80%931878)",
     "priorities": pri(860_000, ottoman=900_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Hamidian massacres",
     "description": "Sultan Abdul Hamid II orchestrates mass killings of Armenians across eastern Anatolia; precursor to the genocide of 1915.",
     "start_year": 1894, "end_year": 1896,
     "wikipedia": "https://en.wikipedia.org/wiki/Hamidian_massacres",
     "priorities": pri(820_000, ottoman=880_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Young Turk Revolution",
     "description": "Committee of Union and Progress forces restoration of the 1876 constitution; reshapes Ottoman politics in the empire's last years.",
     "start_year": 1908, "start_month": 7, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Young_Turk_Revolution",
     "priorities": pri(870_000, ottoman=910_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Italo-Turkish War",
     "description": "Italy seizes Libya and the Dodecanese from Ottomans; first use of aircraft in war; weakens Ottoman position before the Balkan Wars.",
     "start_year": 1911, "start_month": 9, "start_day": 29, "end_year": 1912, "end_month": 10, "end_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Italo-Turkish_War",
     "priorities": pri(820_000, ottoman=870_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Gallipoli campaign",
     "description": "Allied attempt to force the Dardanelles fails after eight months of fighting; ~115,000 Allied and ~85,000 Ottoman casualties.",
     "start_year": 1915, "start_month": 2, "start_day": 19, "end_year": 1916, "end_month": 1, "end_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Gallipoli_campaign",
     "priorities": pri(910_000, ottoman=940_000, **{"ww1": 940_000}, england=900_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Armenian genocide",
     "description": "Ottoman government's systematic killing and deportation of Armenian Christians; estimated 1 million dead.",
     "start_year": 1915, "start_month": 4, "start_day": 24, "end_year": 1923,
     "wikipedia": "https://en.wikipedia.org/wiki/Armenian_genocide",
     "priorities": pri(950_000, ottoman=940_000, **{"ww1": 920_000}),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Sykes-Picot Agreement",
     "description": "Secret Anglo-French treaty partitioning Ottoman Arab provinces; reshapes the Middle East after WWI.",
     "start_year": 1916, "start_month": 5, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Sykes%E2%80%93Picot_Agreement",
     "priorities": pri(900_000, ottoman=910_000, england=890_000, france=870_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Treaty of Sèvres",
     "description": "WWI peace treaty partitions Ottoman empire; rejected by Turkish nationalists under Mustafa Kemal; superseded by Lausanne 1923.",
     "start_year": 1920, "start_month": 8, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_S%C3%A8vres",
     "priorities": pri(880_000, ottoman=920_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Turkish War of Independence",
     "description": "Mustafa Kemal leads nationalist forces against Greek, French, British, Armenian, and remaining Ottoman opposition; founds modern Turkey.",
     "start_year": 1919, "end_year": 1923,
     "wikipedia": "https://en.wikipedia.org/wiki/Turkish_War_of_Independence",
     "priorities": pri(910_000, ottoman=920_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "person", "title": "Mustafa Kemal Atatürk",
     "description": "Founding father of the Republic of Turkey; led Turkish War of Independence; sweeping westernising reforms.",
     "start_year": 1881, "end_year": 1938, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mustafa_Kemal_Atat%C3%BCrk",
     "priorities": pri(950_000, ottoman=920_000, people=950_000),
     "region_weights": RW_OTTOMAN},

    {"type": "event", "title": "Abolition of the Ottoman Sultanate",
     "description": "Grand National Assembly abolishes the sultanate; Mehmed VI exiled; ends the 600-year Ottoman dynasty.",
     "start_year": 1922, "start_month": 11, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Abolition_of_the_Ottoman_sultanate",
     "priorities": pri(910_000, ottoman=950_000),
     "region_weights": RW_OTTOMAN,
     "first_zoom_out": "Ottoman Empire"},

    {"type": "event", "title": "Republic of Turkey proclaimed",
     "description": "Atatürk proclaims the Republic of Turkey; secular nation-state replaces multi-ethnic Ottoman empire.",
     "start_year": 1923, "start_month": 10, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Republic_Day_(Turkey)",
     "priorities": pri(930_000, ottoman=940_000),
     "region_weights": RW_OTTOMAN},

    {"type": "event", "title": "Abolition of the Caliphate",
     "description": "Turkish Grand National Assembly abolishes the Sunni caliphate; institutional end of a 1,300-year office; shock across Muslim world.",
     "start_year": 1924, "start_month": 3, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Abolition_of_the_Caliphate",
     "priorities": pri(910_000, ottoman=930_000, islam=940_000),
     "region_weights": RW_OTTOMAN},

    {"type": "event", "title": "Turkish alphabet reform",
     "description": "Atatürk's government replaces Arabic-script Ottoman Turkish with a Latin alphabet; reshapes literacy and culture in a year.",
     "start_year": 1928, "start_month": 11, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Turkish_alphabet",
     "priorities": pri(840_000, ottoman=890_000, **{"arts-and-thoughts": 860_000}),
     "region_weights": RW_OTTOMAN},

    # =================================================================
    # BLACK DEATH (umbrella exists; add depth)
    # =================================================================
    {"type": "event", "title": "Plague arrives at Caffa",
     "description": "Mongol siege of the Genoese port of Caffa in Crimea; plague-infected corpses catapulted over walls; spreads to Europe via Italian ships.",
     "start_year": 1346, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Caffa",
     "priorities": pri(840_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Black Death"},

    {"type": "event", "title": "Black Death reaches Italy",
     "description": "Plague arrives at Sicilian and Italian ports; spreads up the Italian peninsula; Boccaccio sets the Decameron in plague-stricken Florence.",
     "start_year": 1347, "start_month": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Black_Death",
     "priorities": pri(880_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Black Death"},

    {"type": "event", "title": "Pogroms during the Black Death",
     "description": "Jewish communities falsely blamed for poisoning wells; thousands killed in pogroms across the Rhineland and beyond.",
     "start_year": 1348, "end_year": 1351,
     "wikipedia": "https://en.wikipedia.org/wiki/Black_Death_Jewish_persecutions",
     "priorities": pri(840_000, judaism=890_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Black Death"},

    {"type": "art", "title": "Boccaccio's Decameron",
     "description": "Hundred-tale frame story set among Florentines fleeing the Black Death; landmark of early Italian prose.",
     "start_year": 1353, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Decameron",
     "priorities": pri(900_000, **{"arts-and-thoughts": 930_000, "renaissance": 900_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Black Death"},

    {"type": "event", "title": "Plague returns: Second Pandemic",
     "description": "Plague recurs in waves for centuries after the Black Death — London 1665, Marseille 1720, Vienna 1679 — each killing tens of thousands.",
     "start_year": 1361, "end_year": 1720, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_plague_pandemic",
     "priorities": pri(860_000),
     "region_weights": RW_EU},

    # =================================================================
    # SPANISH CIVIL WAR — more depth
    # =================================================================
    {"type": "event", "title": "Falangist movement founded",
     "description": "José Antonio Primo de Rivera founds the Falange; Spanish fascist movement that backs the Nationalist cause in the Civil War.",
     "start_year": 1933, "start_month": 10, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/FE_de_las_JONS",
     "priorities": pri(810_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Spanish Civil War"},

    {"type": "event", "title": "Nationalist coup d'état",
     "description": "Military officers in Spanish Morocco rise against the Republic; partial success splits Spain and triggers civil war.",
     "start_year": 1936, "start_month": 7, "start_day": 17, "end_month": 7, "end_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/July_1936_coup_in_Spain",
     "priorities": pri(870_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Spanish Civil War"},

    {"type": "event", "title": "Death of Federico García Lorca",
     "description": "Poet and playwright executed by Nationalist forces at Víznar; symbol of cultural cost of the Civil War.",
     "start_year": 1936, "start_month": 8, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Federico_Garc%C3%ADa_Lorca",
     "priorities": pri(880_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Spanish Civil War"},

    {"type": "person", "title": "Federico García Lorca",
     "description": "Spanish poet and playwright; Blood Wedding, The House of Bernarda Alba, Poet in New York; killed at the start of the Civil War.",
     "start_year": 1898, "end_year": 1936, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Federico_Garc%C3%ADa_Lorca",
     "priorities": pri(900_000, people=910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_EU},

    # =================================================================
    # BAROQUE + EARLY MUSIC
    # =================================================================
    {"type": "person", "title": "Claudio Monteverdi",
     "description": "Italian composer who bridged Renaissance and Baroque; L'Orfeo is one of the earliest extant operas.",
     "start_year": 1567, "end_year": 1643, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Claudio_Monteverdi",
     "priorities": pri(900_000, people=920_000, **{"arts-and-thoughts": 930_000, "renaissance": 900_000}),
     "region_weights": RW_EU},

    {"type": "art", "title": "Monteverdi's L'Orfeo",
     "description": "Court opera premiered at Mantua; one of the earliest works of the Baroque opera tradition; reshapes Western music.",
     "start_year": 1607, "start_month": 2, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/L%27Orfeo",
     "priorities": pri(870_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Baroque art and architecture"},

    {"type": "person", "title": "Antonio Vivaldi",
     "description": "Venetian priest and Baroque composer; The Four Seasons; nearly forgotten until 20th-century revival.",
     "start_year": 1678, "end_year": 1741, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Antonio_Vivaldi",
     "priorities": pri(920_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU},

    {"type": "art", "title": "Vivaldi's The Four Seasons",
     "description": "Set of four violin concertos; among the most popular pieces in the Baroque repertoire.",
     "start_year": 1725, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Four_Seasons_(Vivaldi)",
     "priorities": pri(900_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "George Frideric Handel",
     "description": "German-British Baroque composer; Messiah, Water Music, Music for the Royal Fireworks; dominated English musical life.",
     "start_year": 1685, "end_year": 1759, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/George_Frideric_Handel",
     "priorities": pri(930_000, england=920_000, germany=900_000, people=930_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_EU},

    {"type": "art", "title": "Handel's Messiah",
     "description": "English-language oratorio; standing audience tradition for the Hallelujah chorus reportedly started by George II.",
     "start_year": 1742, "start_month": 4, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Messiah_(Handel)",
     "priorities": pri(920_000, england=910_000, **{"arts-and-thoughts": 940_000, "christianity": 900_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Joseph Haydn",
     "description": "Austrian composer; \"Father of the Symphony\" and string quartet; taught Beethoven, friends with Mozart.",
     "start_year": 1732, "end_year": 1809, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Joseph_Haydn",
     "priorities": pri(910_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU},

    {"type": "art", "title": "Bach's St Matthew Passion",
     "description": "Bach's three-hour Passion oratorio; one of the great works of sacred music.",
     "start_year": 1727, "start_month": 4, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/St_Matthew_Passion",
     "priorities": pri(890_000, germany=900_000, christianity=890_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU},

    {"type": "art", "title": "Bach's Mass in B minor",
     "description": "Bach's late-career Mass setting; pinnacle of his sacred composition; never performed in full in his lifetime.",
     "start_year": 1749, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mass_in_B_minor",
     "priorities": pri(880_000, **{"arts-and-thoughts": 920_000, "christianity": 880_000}),
     "region_weights": RW_EU},

    # =================================================================
    # GENPEI / RUSSO-JAPANESE / PENINSULAR WAR CHILDREN
    # =================================================================
    {"type": "event", "title": "Taira-Minamoto conflict begins",
     "description": "Heiji rebellion; Taira clan eliminates Minamoto rivals at court; sets stage for the Genpei War 20 years later.",
     "start_year": 1159, "start_month": 12, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Heiji_Rebellion",
     "priorities": pri(810_000, japan=850_000),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Genpei War"},

    {"type": "event", "title": "Battle of Ichi-no-Tani",
     "description": "Minamoto Yoshitsune's surprise downhill cavalry attack breaks the Taira positions; turning point in the Genpei War.",
     "start_year": 1184, "start_month": 3, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Ichi-no-Tani",
     "priorities": pri(790_000, japan=820_000),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Genpei War"},

    {"type": "event", "title": "Battle of Yashima",
     "description": "Yoshitsune's daring assault destroys the last Taira land base on Shikoku; sets up the final naval battle at Dan-no-ura.",
     "start_year": 1185, "start_month": 3, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Yashima",
     "priorities": pri(780_000, japan=820_000),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Genpei War"},

    {"type": "event", "title": "Siege of Port Arthur",
     "description": "Five-month Japanese siege of the Russian-leased fortress; combination of trenches, mines, machine guns foreshadows WWI.",
     "start_year": 1904, "start_month": 8, "start_day": 1, "end_year": 1905, "end_month": 1, "end_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Port_Arthur",
     "priorities": pri(840_000, japan=870_000),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Russo-Japanese War"},

    {"type": "event", "title": "Battle of Mukden",
     "description": "Largest land battle of the Russo-Japanese War; Japanese decisively defeat Russians; ~600,000 troops engaged.",
     "start_year": 1905, "start_month": 2, "start_day": 20, "end_month": 3, "end_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Mukden",
     "priorities": pri(840_000, japan=870_000),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Russo-Japanese War"},

    {"type": "event", "title": "Battle of Bailén",
     "description": "Spanish army forces French corps to surrender in Andalusia; first major defeat of Napoleon's land army; lights up Spanish resistance.",
     "start_year": 1808, "start_month": 7, "start_day": 16, "end_month": 7, "end_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Bail%C3%A9n",
     "priorities": pri(810_000, **{"napoleonic": 870_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Peninsular War"},

    {"type": "event", "title": "Battle of Talavera",
     "description": "Wellesley defeats French at Talavera in Spain; opens Anglo-Spanish-Portuguese offensive in the Peninsular War.",
     "start_year": 1809, "start_month": 7, "start_day": 27, "end_month": 7, "end_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Talavera",
     "priorities": pri(800_000, england=830_000, **{"napoleonic": 850_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Peninsular War"},

    {"type": "event", "title": "Battle of Salamanca",
     "description": "Wellington crushes Marmont in a brilliant Spanish summer manoeuvre; turns the Peninsular War in the Allies' favour.",
     "start_year": 1812, "start_month": 7, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Salamanca",
     "priorities": pri(820_000, england=860_000, **{"napoleonic": 880_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Peninsular War"},

    {"type": "event", "title": "Siege of Badajoz",
     "description": "Wellington's army storms the Spanish fortress; one of the bloodiest assaults of the Napoleonic Wars; troops sack the town for two days afterward.",
     "start_year": 1812, "start_month": 3, "start_day": 16, "end_month": 4, "end_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Badajoz_(1812)",
     "priorities": pri(800_000, england=830_000, **{"napoleonic": 850_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Peninsular War"},

    {"type": "event", "title": "Spanish Constitution of 1812",
     "description": "Cortes of Cádiz adopts a liberal constitution during the Peninsular War; influence on subsequent constitutional thought in Spanish America.",
     "start_year": 1812, "start_month": 3, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Spanish_Constitution_of_1812",
     "priorities": pri(810_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Peninsular War"},
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
