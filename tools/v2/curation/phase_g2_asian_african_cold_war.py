"""
Phase G2 — Children for Asian, African, and late-Cold-War umbrellas.

Targets:
  Mongol Empire children (~10)
  Taiping Rebellion (~6)
  Sengoku additional (~5)
  Mughal expansion (~4)
  Sub-Saharan African civilisations (~15) — Mali, Songhai, Ethiopia/Aksum,
      Great Zimbabwe, Benin, Kongo
  Decolonisation of Africa (~12)
  Late Cold War: Solidarity, Glasnost/Perestroika, Soviet collapse (~12)
  Vietnam War depth (~8)
  Korean War depth (~6)
  Pacific WW2 depth (~10)
  Recent conflicts: Afghanistan/Iraq detail (~10)
  Pacific exploration / Polynesia (~5)
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_CHINA = {"europe": 2, "americas": 1, "asia": 10, "australasia": 2, "africa": 1}
RW_JAPAN = {"europe": 2, "americas": 3, "asia": 10, "australasia": 3, "africa": 1}
RW_AFRICA = {"europe": 3, "americas": 2, "asia": 2, "australasia": 1, "africa": 10}
RW_VIETNAM = {"europe": 4, "americas": 6, "asia": 10, "australasia": 4, "africa": 1}
RW_COLD = {"europe": 9, "americas": 8, "asia": 6, "australasia": 4, "africa": 4}


def pri(master: int, **extras) -> dict:
    return {"master": master, **extras}


ENTRIES = [
    # ----- Mongol Empire children (~10) -----
    {"type": "person", "title": "Subutai",
     "description": "Genghis Khan's greatest general; orchestrated campaigns from Russia to Hungary; never lost a battle.",
     "start_year": 1175, "end_year": 1248, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Subutai",
     "priorities": pri(840_000, people=870_000),
     "region_weights": RW_CHINA},

    {"type": "event", "title": "Mongol invasion of Khwarazm",
     "description": "Genghis Khan destroys the Khwarazmian Empire across modern Iran and Central Asia; cities like Samarkand and Merv razed.",
     "start_year": 1219, "end_year": 1221,
     "wikipedia": "https://en.wikipedia.org/wiki/Mongol_conquest_of_Khwarazmia",
     "priorities": pri(880_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Genghis Khan"},

    {"type": "event", "title": "Mongol invasion of Rus' (1237-1240)",
     "description": "Batu Khan's army devastates Kievan Rus'; Kiev sacked 1240; principalities become tributaries of the Golden Horde for ~240 years.",
     "start_year": 1237, "end_year": 1240,
     "wikipedia": "https://en.wikipedia.org/wiki/Mongol_invasion_of_Kievan_Rus%27",
     "priorities": pri(910_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Kievan Rus'"},

    {"type": "event", "title": "Mongol invasion of Europe",
     "description": "Mongols smash Polish-Hungarian armies at Liegnitz and Mohi; Europe spared further devastation by Ögedei Khan's death.",
     "start_year": 1241, "start_month": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Mongol_invasion_of_Europe",
     "priorities": pri(900_000),
     "region_weights": RW_CHINA},

    {"type": "event", "title": "Sack of Baghdad (1258)",
     "description": "Mongol prince Hulagu sacks Baghdad; last Abbasid Caliph executed; ends the Islamic Golden Age centred on the city.",
     "start_year": 1258, "start_month": 2, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Baghdad_(1258)",
     "priorities": pri(940_000),
     "region_weights": RW_CHINA},

    {"type": "event", "title": "Ilkhanate established",
     "description": "Hulagu founds the Mongol Ilkhanate in Persia and Mesopotamia; persists for nearly a century before fragmenting.",
     "start_year": 1256, "end_year": 1335,
     "wikipedia": "https://en.wikipedia.org/wiki/Ilkhanate",
     "priorities": pri(840_000),
     "region_weights": RW_CHINA},

    {"type": "event", "title": "Golden Horde",
     "description": "Mongol successor state ruling the Pontic-Caspian steppe and tributary Russian principalities; lasts into the 16th century.",
     "start_year": 1242, "end_year": 1502,
     "wikipedia": "https://en.wikipedia.org/wiki/Golden_Horde",
     "priorities": pri(870_000),
     "region_weights": RW_CHINA},

    {"type": "event", "title": "Pax Mongolica",
     "description": "Mid-13th to mid-14th century period of relative peace and trade across Mongol-controlled Eurasia; Marco Polo and ibn Battuta travel.",
     "start_year": 1260, "end_year": 1360, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pax_Mongolica",
     "priorities": pri(870_000),
     "region_weights": RW_CHINA},

    {"type": "event", "title": "Timur's conquests",
     "description": "Turco-Mongol warlord Timur (Tamerlane) builds vast empire from Anatolia to Delhi; legendary cruelty; founds the Timurid dynasty.",
     "start_year": 1370, "end_year": 1405,
     "wikipedia": "https://en.wikipedia.org/wiki/Timur",
     "priorities": pri(910_000),
     "region_weights": RW_CHINA},

    {"type": "event", "title": "Battle of Ankara (1402)",
     "description": "Timur crushes Ottoman sultan Bayezid I; captures him; delays Ottoman expansion by a generation.",
     "start_year": 1402, "start_month": 7, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Ankara",
     "priorities": pri(830_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Timur's conquests"},

    # ----- Taiping Rebellion (~6) -----
    {"type": "person", "title": "Hong Xiuquan",
     "description": "Failed civil-service candidate who proclaimed himself brother of Jesus; founded the Taiping Heavenly Kingdom; suicide on Nanjing's fall.",
     "start_year": 1814, "end_year": 1864, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hong_Xiuquan",
     "priorities": pri(870_000, china=890_000, people=890_000),
     "region_weights": RW_CHINA},

    {"type": "event", "title": "Taiping Heavenly Kingdom",
     "description": "Anti-Qing theocratic state established by Hong Xiuquan, ruling much of southern China from Nanjing.",
     "start_year": 1851, "end_year": 1864,
     "wikipedia": "https://en.wikipedia.org/wiki/Taiping_Heavenly_Kingdom",
     "priorities": pri(880_000, china=900_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Taiping Rebellion"},

    {"type": "event", "title": "Taiping capture of Nanjing",
     "description": "Taiping forces seize Nanjing; renamed Tianjing ('Heavenly Capital'); their capital for the rest of the rebellion.",
     "start_year": 1853, "start_month": 3, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Nanjing_(1853)",
     "priorities": pri(820_000, china=860_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Taiping Rebellion"},

    {"type": "event", "title": "Battle of Anqing",
     "description": "Long Qing siege of the Taiping stronghold of Anqing ends in starvation surrender; opens path to Nanjing.",
     "start_year": 1861, "start_month": 9, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Anqing",
     "priorities": pri(780_000, china=830_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Taiping Rebellion"},

    {"type": "event", "title": "Fall of Nanjing (1864)",
     "description": "Qing forces under Zeng Guofan retake Nanjing; Hong Xiuquan dead; ~100,000 killed in the city; effective end of the Taiping.",
     "start_year": 1864, "start_month": 7, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Nanjing_(1864)",
     "priorities": pri(850_000, china=890_000),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Taiping Rebellion"},

    # ----- Sub-Saharan African civilisations (~14) -----
    {"type": "event", "title": "Kingdom of Aksum",
     "description": "Powerful trading kingdom of northeast Africa (modern Eritrea/Ethiopia); minted coins; early adopter of Christianity.",
     "start_year": 100, "end_year": 940, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Kingdom_of_Aksum",
     "priorities": pri(870_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Aksum converts to Christianity",
     "description": "King Ezana converts under influence of Frumentius; Aksum becomes one of the first Christian kingdoms.",
     "start_year": 340, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ezana_of_Axum",
     "priorities": pri(820_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "Kingdom of Aksum"},

    {"type": "event", "title": "Ghana Empire",
     "description": "First major West African empire; controlled trans-Saharan gold-salt trade; collapsed under Almoravid pressure.",
     "start_year": 700, "end_year": 1240, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ghana_Empire",
     "priorities": pri(860_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Mali Empire",
     "description": "West African empire; vast wealth from gold; capitals at Niani; trans-Saharan trade with North Africa.",
     "start_year": 1235, "end_year": 1670, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mali_Empire",
     "priorities": pri(900_000),
     "region_weights": RW_AFRICA},

    {"type": "person", "title": "Mansa Musa",
     "description": "Ruler of Mali at its peak; his 1324 hajj to Mecca with so much gold that he depressed prices in Egypt is the stuff of legend.",
     "start_year": 1280, "end_year": 1337, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mansa_Musa",
     "priorities": pri(920_000, people=930_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Mansa Musa's hajj to Mecca",
     "description": "Mansa Musa travels to Mecca via Cairo with vast retinue and gold; introduces Mali to the Mediterranean world.",
     "start_year": 1324,
     "wikipedia": "https://en.wikipedia.org/wiki/Mansa_Musa",
     "priorities": pri(900_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "Mali Empire"},

    {"type": "event", "title": "Timbuktu as centre of Islamic learning",
     "description": "Sankoré madrasah and Djinguereber Mosque make Timbuktu a major scholarly centre; libraries hold tens of thousands of manuscripts.",
     "start_year": 1100, "end_year": 1600, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Timbuktu",
     "priorities": pri(870_000, **{"arts-and-thoughts": 870_000}),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Songhai Empire",
     "description": "Succeeded Mali as the dominant West African power; capital at Gao; conquered by Moroccan forces with firearms in 1591.",
     "start_year": 1464, "end_year": 1591,
     "wikipedia": "https://en.wikipedia.org/wiki/Songhai_Empire",
     "priorities": pri(880_000),
     "region_weights": RW_AFRICA},

    {"type": "person", "title": "Sunni Ali",
     "description": "Founder of the Songhai Empire; brilliant military strategist who conquered Timbuktu and Djenné.",
     "start_year": 1464, "end_year": 1492, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Sonni_Ali",
     "priorities": pri(800_000, people=830_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Battle of Tondibi",
     "description": "Moroccan forces with firearms destroy the Songhai army; ends West Africa's classical great power era.",
     "start_year": 1591, "start_month": 3, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Tondibi",
     "priorities": pri(800_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "Songhai Empire"},

    {"type": "event", "title": "Kingdom of Kongo",
     "description": "Central African kingdom in modern Angola/DRC; converted to Christianity early; intricate diplomatic relations with Portugal.",
     "start_year": 1390, "end_year": 1914, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Kingdom_of_Kongo",
     "priorities": pri(830_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Kingdom of Benin",
     "description": "West African kingdom (modern Edo State, Nigeria) famed for bronze plaques and ivory carvings; sacked by Britain in 1897.",
     "start_year": 1180, "end_year": 1897, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Kingdom_of_Benin",
     "priorities": pri(840_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Sokoto Caliphate founded",
     "description": "Fulani-led jihadist state in northern Nigeria under Usman dan Fodio; one of the largest pre-colonial African empires.",
     "start_year": 1804,
     "wikipedia": "https://en.wikipedia.org/wiki/Sokoto_Caliphate",
     "priorities": pri(830_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Zulu Kingdom under Shaka",
     "description": "Shaka transforms the small Zulu chiefdom into a militarised regional power; impi tactics and short stabbing assegai.",
     "start_year": 1816, "end_year": 1828,
     "wikipedia": "https://en.wikipedia.org/wiki/Shaka",
     "priorities": pri(880_000),
     "region_weights": RW_AFRICA},

    # ----- Decolonisation of Africa (~12) -----
    {"type": "event", "title": "Independence of Ghana",
     "description": "Gold Coast becomes Ghana under Kwame Nkrumah; first sub-Saharan African colony to gain independence from European rule.",
     "start_year": 1957, "start_month": 3, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Independence_of_Ghana",
     "priorities": pri(890_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "Decolonisation of Africa"},

    {"type": "person", "title": "Kwame Nkrumah",
     "description": "Founding president of Ghana; pan-Africanist; overthrown in 1966 coup.",
     "start_year": 1909, "end_year": 1972, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Kwame_Nkrumah",
     "priorities": pri(880_000, people=900_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Mau Mau uprising",
     "description": "Kenyan insurgency against British colonial rule; brutally suppressed; leads to Kenyan independence in 1963.",
     "start_year": 1952, "end_year": 1960,
     "wikipedia": "https://en.wikipedia.org/wiki/Mau_Mau_rebellion",
     "priorities": pri(870_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "Decolonisation of Africa"},

    {"type": "event", "title": "Algerian War of Independence",
     "description": "FLN-led war against French rule; brutal on both sides; ends with Algerian independence; defeats the Fourth Republic.",
     "start_year": 1954, "end_year": 1962,
     "wikipedia": "https://en.wikipedia.org/wiki/Algerian_War",
     "priorities": pri(900_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Congo Crisis",
     "description": "Newly independent Congo descends into secessionism, mercenary war, UN intervention; Patrice Lumumba assassinated.",
     "start_year": 1960, "end_year": 1965,
     "wikipedia": "https://en.wikipedia.org/wiki/Congo_Crisis",
     "priorities": pri(880_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "Decolonisation of Africa"},

    {"type": "event", "title": "Sharpeville massacre",
     "description": "South African police kill 69 unarmed protesters in Sharpeville; turning point in the international anti-apartheid movement.",
     "start_year": 1960, "start_month": 3, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Sharpeville_massacre",
     "priorities": pri(880_000),
     "region_weights": RW_AFRICA},

    {"type": "person", "title": "Nelson Mandela",
     "description": "South African anti-apartheid revolutionary and statesman; imprisoned 27 years; first president of democratic South Africa.",
     "start_year": 1918, "end_year": 2013, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Nelson_Mandela",
     "priorities": pri(970_000, people=970_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Mandela imprisoned (Rivonia Trial)",
     "description": "Nelson Mandela and other ANC leaders sentenced to life imprisonment at the Rivonia Trial.",
     "start_year": 1964, "start_month": 6, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Rivonia_Trial",
     "priorities": pri(890_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Nigerian Civil War (Biafra)",
     "description": "Eastern Region secedes as Biafra; three-year war; 1-3 million civilians die, mostly from starvation; secessionist state crushed.",
     "start_year": 1967, "end_year": 1970,
     "wikipedia": "https://en.wikipedia.org/wiki/Nigerian_Civil_War",
     "priorities": pri(880_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Rwandan genocide",
     "description": "Hutu extremists murder ~800,000 Tutsis and moderate Hutus in 100 days; international community fails to intervene.",
     "start_year": 1994, "start_month": 4, "start_day": 7, "end_month": 7, "end_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Rwandan_genocide",
     "priorities": pri(940_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "End of apartheid",
     "description": "F. W. de Klerk legalises the ANC and releases Mandela; negotiations lead to multiracial elections in 1994.",
     "start_year": 1990, "start_month": 2, "start_day": 2, "end_year": 1994, "end_month": 4, "end_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Apartheid",
     "priorities": pri(950_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "First multiracial South African election",
     "description": "Mandela wins the presidency of a democratic South Africa; ends 46 years of apartheid rule and centuries of white minority dominance.",
     "start_year": 1994, "start_month": 4, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/1994_South_African_general_election",
     "priorities": pri(950_000),
     "region_weights": RW_AFRICA},

    # ----- Late Cold War / Soviet collapse (~12) -----
    {"type": "event", "title": "Solidarity strike at Lenin Shipyard",
     "description": "Lech Wałęsa leads strike at Gdańsk; founding of Solidarity, first independent trade union in the Soviet bloc.",
     "start_year": 1980, "start_month": 8, "start_day": 14, "end_month": 8, "end_day": 31,
     "wikipedia": "https://en.wikipedia.org/wiki/Gda%C5%84sk_Agreement",
     "priorities": pri(900_000, **{"cold-war": 920_000}),
     "region_weights": RW_COLD,
     "first_zoom_out": "Cold War"},

    {"type": "person", "title": "Lech Wałęsa",
     "description": "Polish trade unionist; led Solidarity; first democratically elected president of Poland after the Cold War.",
     "start_year": 1943, "is_full_life": False,
     "wikipedia": "https://en.wikipedia.org/wiki/Lech_Wa%C5%82%C4%99sa",
     "priorities": pri(900_000, **{"cold-war": 910_000}, people=910_000),
     "region_weights": RW_COLD},

    {"type": "event", "title": "Martial law in Poland",
     "description": "General Jaruzelski declares martial law to crush Solidarity; thousands interned; Solidarity goes underground.",
     "start_year": 1981, "start_month": 12, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Martial_law_in_Poland",
     "priorities": pri(840_000, **{"cold-war": 870_000}),
     "region_weights": RW_COLD},

    {"type": "person", "title": "Mikhail Gorbachev",
     "description": "Last leader of the Soviet Union; introduced glasnost and perestroika; allowed Eastern Europe to break free; resigned 25 December 1991.",
     "start_year": 1931, "end_year": 2022, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mikhail_Gorbachev",
     "priorities": pri(970_000, **{"cold-war": 970_000}, people=970_000),
     "region_weights": RW_COLD},

    {"type": "event", "title": "Glasnost and perestroika",
     "description": "Gorbachev's twin reform programmes — openness and restructuring — unintentionally accelerate Soviet collapse.",
     "start_year": 1985, "end_year": 1991,
     "wikipedia": "https://en.wikipedia.org/wiki/Glasnost",
     "priorities": pri(940_000, **{"cold-war": 950_000}),
     "region_weights": RW_COLD},

    {"type": "event", "title": "Chernobyl disaster",
     "description": "Reactor 4 explodes at Chernobyl; worst civilian nuclear accident in history; corrodes Soviet legitimacy.",
     "start_year": 1986, "start_month": 4, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Chernobyl_disaster",
     "priorities": pri(950_000, **{"cold-war": 920_000}),
     "region_weights": RW_COLD},

    {"type": "event", "title": "INF Treaty signed",
     "description": "Reagan and Gorbachev agree to eliminate intermediate-range nuclear missiles; first treaty to reduce nuclear arsenals.",
     "start_year": 1987, "start_month": 12, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Intermediate-Range_Nuclear_Forces_Treaty",
     "priorities": pri(890_000, **{"cold-war": 910_000}, usa=860_000),
     "region_weights": RW_COLD},

    {"type": "event", "title": "Revolutions of 1989",
     "description": "Wave of revolutions across Eastern Europe; Hungary, Poland, East Germany, Czechoslovakia, Bulgaria, Romania end communist rule.",
     "start_year": 1989,
     "wikipedia": "https://en.wikipedia.org/wiki/Revolutions_of_1989",
     "priorities": pri(960_000, **{"cold-war": 970_000}),
     "region_weights": RW_COLD},

    {"type": "event", "title": "Velvet Revolution",
     "description": "Peaceful overthrow of communism in Czechoslovakia; Václav Havel becomes president; Slovak-Czech split follows in 1993.",
     "start_year": 1989, "start_month": 11, "start_day": 17, "end_month": 12, "end_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Velvet_Revolution",
     "priorities": pri(910_000, **{"cold-war": 930_000}),
     "region_weights": RW_COLD,
     "first_zoom_out": "Revolutions of 1989"},

    {"type": "event", "title": "Romanian Revolution of 1989",
     "description": "Violent overthrow and execution of Nicolae Ceaușescu; bloodiest of the 1989 revolutions; 1,100+ killed.",
     "start_year": 1989, "start_month": 12, "start_day": 16, "end_month": 12, "end_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Romanian_Revolution",
     "priorities": pri(880_000, **{"cold-war": 900_000}),
     "region_weights": RW_COLD,
     "first_zoom_out": "Revolutions of 1989"},

    {"type": "event", "title": "Soviet coup attempt (August Putsch)",
     "description": "Hardliners try to depose Gorbachev; resisted by Boris Yeltsin atop a tank in Moscow; coup collapses in three days.",
     "start_year": 1991, "start_month": 8, "start_day": 19, "end_month": 8, "end_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/1991_Soviet_coup_attempt",
     "priorities": pri(900_000, **{"cold-war": 930_000}),
     "region_weights": RW_COLD},

    {"type": "event", "title": "Dissolution of the Soviet Union",
     "description": "Belavezha Accords (December 8) end the USSR; Gorbachev resigns on 25 December; the red flag is lowered over the Kremlin.",
     "start_year": 1991, "start_month": 12, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Dissolution_of_the_Soviet_Union",
     "priorities": pri(990_000, **{"cold-war": 970_000}),
     "region_weights": RW_COLD},

    # ----- Vietnam War (~8) -----
    {"type": "event", "title": "Battle of Dien Bien Phu",
     "description": "Vietnamese forces under General Giáp defeat French at Dien Bien Phu; ends French Indochina, opens Vietnam War.",
     "start_year": 1954, "start_month": 3, "start_day": 13, "end_month": 5, "end_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Dien_Bien_Phu",
     "priorities": pri(910_000, **{"cold-war": 890_000}),
     "region_weights": RW_VIETNAM},

    {"type": "event", "title": "Gulf of Tonkin incident",
     "description": "Reported attacks on US destroyers provide pretext for the Gulf of Tonkin Resolution and dramatic US escalation in Vietnam.",
     "start_year": 1964, "start_month": 8, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Gulf_of_Tonkin_incident",
     "priorities": pri(890_000, **{"cold-war": 880_000}, usa=870_000),
     "region_weights": RW_VIETNAM},

    {"type": "event", "title": "Tet Offensive",
     "description": "Coordinated North Vietnamese and Viet Cong surprise attack across South Vietnam during Tet; militarily defeated but politically devastating.",
     "start_year": 1968, "start_month": 1, "start_day": 30, "end_month": 9, "end_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Tet_Offensive",
     "priorities": pri(940_000, **{"cold-war": 920_000}, usa=900_000),
     "region_weights": RW_VIETNAM},

    {"type": "event", "title": "My Lai massacre",
     "description": "US soldiers kill 504 unarmed Vietnamese villagers; coverup unraveled by journalist Seymour Hersh; intense political fallout.",
     "start_year": 1968, "start_month": 3, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/My_Lai_massacre",
     "priorities": pri(900_000, **{"cold-war": 880_000}, usa=890_000),
     "region_weights": RW_VIETNAM},

    {"type": "event", "title": "Cambodian Campaign / Kent State shootings",
     "description": "Nixon orders invasion of Cambodia; protests erupt across US universities; National Guard kills four at Kent State.",
     "start_year": 1970, "start_month": 5, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Kent_State_shootings",
     "priorities": pri(880_000, **{"cold-war": 860_000}, usa=890_000),
     "region_weights": RW_VIETNAM,
     "first_zoom_out": "Vietnam War"},

    {"type": "event", "title": "Paris Peace Accords",
     "description": "US-North Vietnam treaty ostensibly ends US involvement; North Vietnam continues war against the South.",
     "start_year": 1973, "start_month": 1, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Paris_Peace_Accords",
     "priorities": pri(870_000, **{"cold-war": 870_000}, usa=880_000),
     "region_weights": RW_VIETNAM,
     "first_zoom_out": "Vietnam War"},

    {"type": "event", "title": "Fall of Saigon",
     "description": "North Vietnamese tanks crash through the gates of the Presidential Palace; iconic helicopter evacuations from the US embassy roof.",
     "start_year": 1975, "start_month": 4, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Fall_of_Saigon",
     "priorities": pri(940_000, **{"cold-war": 930_000}),
     "region_weights": RW_VIETNAM,
     "first_zoom_out": "Vietnam War"},

    {"type": "event", "title": "Khmer Rouge takes Phnom Penh",
     "description": "Pol Pot's Khmer Rouge enters Phnom Penh; empties cities; begins genocide that kills 1.5-2 million Cambodians.",
     "start_year": 1975, "start_month": 4, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Khmer_Rouge",
     "priorities": pri(920_000, **{"cold-war": 900_000}),
     "region_weights": RW_VIETNAM},

    # ----- Korean War (~6) -----
    {"type": "event", "title": "North Korea invades South",
     "description": "Kim Il-sung's forces cross the 38th parallel; UN troops arrive within weeks; opens Korean War.",
     "start_year": 1950, "start_month": 6, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Korean_War",
     "priorities": pri(940_000, **{"cold-war": 940_000}),
     "region_weights": RW_VIETNAM},

    {"type": "event", "title": "Battle of Inchon",
     "description": "MacArthur's amphibious landing in the rear of North Korean forces; collapses the invasion of the south.",
     "start_year": 1950, "start_month": 9, "start_day": 15, "end_month": 9, "end_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Inchon",
     "priorities": pri(880_000, **{"cold-war": 880_000}),
     "region_weights": RW_VIETNAM,
     "first_zoom_out": "North Korea invades South"},

    {"type": "event", "title": "Chinese intervention in Korea",
     "description": "300,000 Chinese 'volunteers' cross the Yalu River; drive UN forces south; war becomes a stalemate.",
     "start_year": 1950, "start_month": 10, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Chinese_People%27s_Volunteer_Army",
     "priorities": pri(890_000, **{"cold-war": 890_000}, china=890_000),
     "region_weights": RW_VIETNAM},

    {"type": "event", "title": "Truman dismisses MacArthur",
     "description": "President Truman fires General Douglas MacArthur over his public demand to expand the Korean War to China.",
     "start_year": 1951, "start_month": 4, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Relief_of_Douglas_MacArthur",
     "priorities": pri(840_000, usa=880_000),
     "region_weights": RW_VIETNAM,
     "first_zoom_out": "North Korea invades South"},

    {"type": "event", "title": "Korean War armistice signed",
     "description": "Panmunjom armistice halts fighting along a line close to the original 38th parallel; no peace treaty has ever been signed.",
     "start_year": 1953, "start_month": 7, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Korean_Armistice_Agreement",
     "priorities": pri(910_000, **{"cold-war": 910_000}),
     "region_weights": RW_VIETNAM,
     "first_zoom_out": "North Korea invades South"},

    # ----- Pacific WW2 (~10) -----
    {"type": "event", "title": "Bataan Death March",
     "description": "Japanese force-march 75,000 American and Filipino prisoners; thousands die from exhaustion, disease, summary execution.",
     "start_year": 1942, "start_month": 4, "start_day": 9, "end_month": 4, "end_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Bataan_Death_March",
     "priorities": pri(870_000, **{"ww2": 890_000}, usa=870_000),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Doolittle Raid",
     "description": "American B-25s launched from a carrier bomb Tokyo and other cities; first US attack on the Japanese home islands.",
     "start_year": 1942, "start_month": 4, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Doolittle_Raid",
     "priorities": pri(860_000, **{"ww2": 880_000}, usa=860_000),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Battle of the Coral Sea",
     "description": "First naval battle fought entirely between aircraft from carriers; checks Japanese advance toward Australia.",
     "start_year": 1942, "start_month": 5, "start_day": 4, "end_month": 5, "end_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Coral_Sea",
     "priorities": pri(870_000, **{"ww2": 890_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Battle of Guadalcanal",
     "description": "Six-month US-Japanese campaign; first major Allied land offensive in the Pacific; ends in US victory.",
     "start_year": 1942, "start_month": 8, "start_day": 7, "end_year": 1943, "end_month": 2, "end_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Guadalcanal_campaign",
     "priorities": pri(890_000, **{"ww2": 920_000}, usa=890_000),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Battle of the Philippine Sea",
     "description": "'Great Marianas Turkey Shoot'; US naval aviators destroy Japanese carrier air power.",
     "start_year": 1944, "start_month": 6, "start_day": 19, "end_month": 6, "end_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Philippine_Sea",
     "priorities": pri(850_000, **{"ww2": 880_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Battle of Leyte Gulf",
     "description": "Largest naval battle in history; first appearance of kamikaze attacks; effective destruction of Japanese fleet.",
     "start_year": 1944, "start_month": 10, "start_day": 23, "end_month": 10, "end_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Leyte_Gulf",
     "priorities": pri(890_000, **{"ww2": 910_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Firebombing of Tokyo",
     "description": "US bombers under Curtis LeMay drop incendiaries on Tokyo; ~100,000 dead in a single night; most destructive non-nuclear air raid.",
     "start_year": 1945, "start_month": 3, "start_day": 9, "end_month": 3, "end_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Bombing_of_Tokyo",
     "priorities": pri(900_000, **{"ww2": 910_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Soviet invasion of Manchuria",
     "description": "Soviet army overruns Japanese-held Manchuria in three weeks; major factor in Japan's decision to surrender.",
     "start_year": 1945, "start_month": 8, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Soviet%E2%80%93Japanese_War",
     "priorities": pri(890_000, **{"ww2": 900_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "World War II"},

    # ----- Recent conflicts (~6) -----
    {"type": "event", "title": "Tora Bora battle",
     "description": "US and Afghan forces assault al-Qaeda's mountain refuge in eastern Afghanistan; bin Laden escapes into Pakistan.",
     "start_year": 2001, "start_month": 12, "start_day": 6, "end_month": 12, "end_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Tora_Bora",
     "priorities": pri(870_000, usa=860_000),
     "region_weights": RW_VIETNAM,
     "first_zoom_out": "War in Afghanistan begins"},

    {"type": "event", "title": "Killing of Osama bin Laden",
     "description": "US Navy SEAL Team Six raids his compound in Abbottabad, Pakistan; bin Laden killed; body buried at sea.",
     "start_year": 2011, "start_month": 5, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Killing_of_Osama_bin_Laden",
     "priorities": pri(950_000, usa=950_000),
     "region_weights": RW_VIETNAM},

    {"type": "event", "title": "Fall of Mosul to ISIS",
     "description": "Islamic State captures Iraq's second city; Iraqi army collapses; ISIS declares a caliphate days later.",
     "start_year": 2014, "start_month": 6, "start_day": 4, "end_month": 6, "end_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Fall_of_Mosul",
     "priorities": pri(890_000),
     "region_weights": RW_VIETNAM},

    {"type": "event", "title": "Arab Spring begins",
     "description": "Tunisian street vendor Mohamed Bouazizi sets himself on fire; sparks wave of protests across the Arab world.",
     "start_year": 2010, "start_month": 12, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Arab_Spring",
     "priorities": pri(930_000),
     "region_weights": RW_AFRICA},

    {"type": "event", "title": "Egyptian Revolution of 2011",
     "description": "Eighteen days of Cairo protests force Hosni Mubarak's resignation after 30 years; brief democratic opening before counter-coup.",
     "start_year": 2011, "start_month": 1, "start_day": 25, "end_month": 2, "end_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Egyptian_revolution_of_2011",
     "priorities": pri(900_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "Arab Spring begins"},

    {"type": "event", "title": "Libyan Civil War (2011)",
     "description": "NATO-backed rebellion overthrows Muammar Gaddafi; he is killed in Sirte; Libya descends into ongoing factional war.",
     "start_year": 2011, "start_month": 2, "start_day": 15, "end_month": 10, "end_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Libyan_civil_war_(2011)",
     "priorities": pri(890_000),
     "region_weights": RW_AFRICA,
     "first_zoom_out": "Arab Spring begins"},

    {"type": "event", "title": "Russia annexes Crimea",
     "description": "Russian forces occupy Crimea; sham referendum delivers union with Russia; first redrawing of European borders by force since WWII.",
     "start_year": 2014, "start_month": 2, "start_day": 20, "end_month": 3, "end_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Russian_annexation_of_Crimea",
     "priorities": pri(940_000),
     "region_weights": RW_COLD},

    {"type": "event", "title": "Russian invasion of Ukraine 2022",
     "description": "Full-scale Russian invasion of Ukraine; largest land war in Europe since WWII; Western sanctions and weapons supply transform NATO.",
     "start_year": 2022, "start_month": 2, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Russian_invasion_of_Ukraine",
     "priorities": pri(980_000),
     "region_weights": RW_COLD},
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
