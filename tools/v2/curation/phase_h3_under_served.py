"""
Phase H3 — Add Renaissance umbrella + under-served topics:
- Renaissance umbrella + a few more children
- Islamic Golden Age umbrella + children
- Bronze Age + Iron Age civilisational gaps (Indus Valley, Babylon, Assyria)
- More music / literature gaps
- Modern science deep-fill (Curie, Einstein, Watson-Crick, Apollo, etc.)
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_EU = {"europe": 10, "americas": 3, "asia": 3, "australasia": 1, "africa": 3}
RW_AMER = {"europe": 4, "americas": 10, "asia": 1, "australasia": 1, "africa": 3}
RW_ASIA = {"europe": 4, "americas": 1, "asia": 10, "australasia": 2, "africa": 4}
RW_MIDEAST = {"europe": 5, "americas": 1, "asia": 10, "australasia": 1, "africa": 5}
RW_GLOBAL = {"europe": 8, "americas": 7, "asia": 5, "australasia": 3, "africa": 4}


def pri(master: int, **extras) -> dict:
    return {"master": master, **extras}


ENTRIES = [
    # =================================================================
    # RENAISSANCE umbrella row
    # =================================================================
    {"type": "event", "title": "Renaissance",
     "description": "European cultural rebirth from c. 1400 to c. 1600; revival of classical learning; Italian beginnings spread north.",
     "start_year": 1400, "end_year": 1600,
     "wikipedia": "https://en.wikipedia.org/wiki/Renaissance",
     "priorities": pri(990_000, renaissance=990_000, **{"arts-and-thoughts": 990_000}),
     "region_weights": RW_EU},

    # =================================================================
    # ISLAMIC GOLDEN AGE umbrella + children
    # =================================================================
    {"type": "event", "title": "Islamic Golden Age",
     "description": "Centuries-long cultural and scientific flowering across Abbasid Caliphate and beyond; advances in mathematics, medicine, astronomy.",
     "start_year": 750, "end_year": 1258,
     "wikipedia": "https://en.wikipedia.org/wiki/Islamic_Golden_Age",
     "priorities": pri(960_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Abbasid Caliphate founded",
     "description": "Overthrow of the Umayyad Caliphate; capital moves to Baghdad; opens the Islamic Golden Age.",
     "start_year": 750, "start_month": 1, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Abbasid_Caliphate",
     "priorities": pri(910_000),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Islamic Golden Age"},

    {"type": "event", "title": "House of Wisdom (Baghdad)",
     "description": "Abbasid institution translating Greek, Persian, Indian works into Arabic; major centre of scholarship under al-Ma'mun.",
     "start_year": 830, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/House_of_Wisdom",
     "priorities": pri(880_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Islamic Golden Age"},

    {"type": "person", "title": "Al-Khwarizmi",
     "description": "Persian mathematician at the House of Wisdom; foundational works on algebra (al-jabr) and Hindu-Arabic numerals.",
     "start_year": 780, "end_year": 850, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Al-Khwarizmi",
     "priorities": pri(900_000, people=920_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_MIDEAST},

    {"type": "person", "title": "Avicenna (Ibn Sina)",
     "description": "Persian polymath; Canon of Medicine became the standard medical text for centuries; major contributions to philosophy and astronomy.",
     "start_year": 980, "end_year": 1037, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Avicenna",
     "priorities": pri(920_000, people=940_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_MIDEAST},

    {"type": "person", "title": "Averroes (Ibn Rushd)",
     "description": "Andalusi philosopher; commentator on Aristotle whose works re-introduced Greek philosophy to Latin Europe.",
     "start_year": 1126, "end_year": 1198, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Averroes",
     "priorities": pri(890_000, people=910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_MIDEAST},

    {"type": "person", "title": "Al-Ghazali",
     "description": "Persian Sunni theologian; reconciled Sufi mysticism with orthodox Islam; The Incoherence of the Philosophers profoundly influential.",
     "start_year": 1058, "end_year": 1111, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Al-Ghazali",
     "priorities": pri(880_000, people=900_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_MIDEAST},

    {"type": "person", "title": "Ibn Battuta",
     "description": "Moroccan Muslim traveller of the 14th century; covered ~75,000 miles across Africa, Asia, Europe; his Rihla is the great travelogue of medieval Islam.",
     "start_year": 1304, "end_year": 1369, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ibn_Battuta",
     "priorities": pri(900_000, people=920_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_GLOBAL},

    {"type": "person", "title": "Ibn Khaldun",
     "description": "Tunisian Arab historian and sociologist; Muqaddimah analyses the rise and fall of dynasties; a founding text of the social sciences.",
     "start_year": 1332, "end_year": 1406, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ibn_Khaldun",
     "priorities": pri(900_000, people=920_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_MIDEAST},

    # =================================================================
    # BRONZE / IRON AGE CIVILISATIONAL GAPS
    # =================================================================
    {"type": "event", "title": "Indus Valley Civilisation",
     "description": "Bronze Age urban civilisation across modern Pakistan and northwest India; great cities Mohenjo-daro and Harappa; mysterious decline.",
     "start_year": -3300, "end_year": -1300, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Indus_Valley_Civilisation",
     "priorities": pri(910_000, india=940_000),
     "region_weights": RW_ASIA},

    {"type": "event", "title": "Sumerian civilisation",
     "description": "World's first urban civilisation in southern Mesopotamia; invented writing (cuneiform); city-states of Ur, Uruk, Lagash.",
     "start_year": -4500, "end_year": -1900, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Sumer",
     "priorities": pri(940_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Akkadian Empire",
     "description": "Sargon's empire; first known empire in history; conquered much of Mesopotamia; Akkadian becomes lingua franca of Near East.",
     "start_year": -2334, "end_year": -2154, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Akkadian_Empire",
     "priorities": pri(900_000),
     "region_weights": RW_MIDEAST},

    {"type": "person", "title": "Hammurabi",
     "description": "Sixth king of Babylon's First Dynasty; promulgated one of the earliest comprehensive law codes (\"eye for an eye\").",
     "start_year": -1810, "end_year": -1750, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hammurabi",
     "priorities": pri(920_000, people=930_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Code of Hammurabi",
     "description": "Babylonian law code inscribed on a stele; ~282 laws covering commerce, family, slavery; oldest substantial extant law code.",
     "start_year": -1754,
     "wikipedia": "https://en.wikipedia.org/wiki/Code_of_Hammurabi",
     "priorities": pri(910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Hittite Empire",
     "description": "Anatolian empire; major Bronze Age power; clashed with Egypt at Kadesh; collapsed during Bronze Age Collapse.",
     "start_year": -1600, "end_year": -1180, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hittites",
     "priorities": pri(870_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Phoenician civilisation",
     "description": "Seafaring city-states (Tyre, Sidon, Byblos); Mediterranean trade; alphabet that gave rise to Greek and Latin scripts.",
     "start_year": -1500, "end_year": -300, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Phoenicia",
     "priorities": pri(900_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Phoenician alphabet",
     "description": "Phoenicians develop the consonantal alphabet ancestor of Greek, Hebrew, Arabic, Latin and most modern alphabets.",
     "start_year": -1050, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Phoenician_alphabet",
     "priorities": pri(930_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Neo-Assyrian Empire at peak",
     "description": "Iron Age empire dominating Near East; militarised, deportation policies, brutal warfare; capitals at Nineveh and Nimrud.",
     "start_year": -911, "end_year": -609, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Neo-Assyrian_Empire",
     "priorities": pri(890_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Fall of Nineveh",
     "description": "Medes and Babylonians sack the Assyrian capital; ends the Assyrian empire and shifts power south to Babylon.",
     "start_year": -612,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Nineveh_(612_BC)",
     "priorities": pri(860_000),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Neo-Assyrian Empire at peak"},

    {"type": "event", "title": "Babylonian Captivity",
     "description": "Nebuchadnezzar II destroys First Temple and exiles Jewish elite to Babylon; reshapes Judaism into a portable religion of text.",
     "start_year": -586, "end_year": -538,
     "wikipedia": "https://en.wikipedia.org/wiki/Babylonian_captivity",
     "priorities": pri(920_000),
     "region_weights": RW_MIDEAST},

    # =================================================================
    # MORE SCIENCE & TECH (20th century)
    # =================================================================
    {"type": "person", "title": "Marie Curie",
     "description": "Polish-French physicist; first woman to win a Nobel Prize, only person to win Nobels in two sciences (physics and chemistry); discovered radium and polonium.",
     "start_year": 1867, "end_year": 1934, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Marie_Curie",
     "priorities": pri(960_000, people=970_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Albert Einstein",
     "description": "German-born theoretical physicist; special and general relativity; photoelectric effect; transformed physics in the 20th century.",
     "start_year": 1879, "end_year": 1955, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Albert_Einstein",
     "priorities": pri(990_000, people=990_000, germany=920_000, **{"arts-and-thoughts": 990_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Einstein's miracle year (Annus Mirabilis)",
     "description": "Einstein publishes four revolutionary papers — photoelectric effect, Brownian motion, special relativity, mass-energy equivalence.",
     "start_year": 1905,
     "wikipedia": "https://en.wikipedia.org/wiki/Annus_Mirabilis_papers",
     "priorities": pri(970_000, **{"arts-and-thoughts": 980_000}, germany=900_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "General relativity published",
     "description": "Einstein's theory of gravity as curvature of spacetime; predicts light-bending later confirmed by Eddington 1919.",
     "start_year": 1915, "start_month": 11, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/General_relativity",
     "priorities": pri(960_000, **{"arts-and-thoughts": 970_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Discovery of penicillin",
     "description": "Alexander Fleming notices that mould has killed bacteria on a Petri dish; Florey and Chain develop it as a drug a decade later.",
     "start_year": 1928, "start_month": 9, "start_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Penicillin",
     "priorities": pri(950_000, england=940_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Watson and Crick announce DNA structure",
     "description": "Watson and Crick at Cambridge, drawing on Franklin's X-ray crystallography, propose the double-helix structure of DNA.",
     "start_year": 1953, "start_month": 4, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Molecular_structure_of_Nucleic_Acids",
     "priorities": pri(970_000, england=940_000, **{"arts-and-thoughts": 970_000}),
     "region_weights": RW_GLOBAL},

    {"type": "person", "title": "Rosalind Franklin",
     "description": "British chemist; X-ray diffraction work on DNA crucial to Watson and Crick's discovery; died of cancer aged 37 before Nobels were awarded.",
     "start_year": 1920, "end_year": 1958, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Rosalind_Franklin",
     "priorities": pri(900_000, england=910_000, people=920_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "First moon landing",
     "description": "Apollo 11; Neil Armstrong steps onto the Moon; \"one small step for [a] man, one giant leap for mankind\".",
     "start_year": 1969, "start_month": 7, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Apollo_11",
     "priorities": pri(990_000, usa=990_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Sputnik 1 launched",
     "description": "Soviet artificial satellite; first object placed in Earth orbit; opens the Space Age and the Space Race.",
     "start_year": 1957, "start_month": 10, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Sputnik_1",
     "priorities": pri(960_000, **{"cold-war": 940_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Yuri Gagarin first in space",
     "description": "Soviet cosmonaut becomes the first human to fly to space and orbit Earth aboard Vostok 1.",
     "start_year": 1961, "start_month": 4, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Yuri_Gagarin",
     "priorities": pri(950_000, **{"cold-war": 920_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Human Genome Project completed",
     "description": "International collaboration completes the first draft sequence of the human genome.",
     "start_year": 2003, "start_month": 4, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Human_Genome_Project",
     "priorities": pri(910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "First electronic computer (ENIAC)",
     "description": "ENIAC unveiled at the University of Pennsylvania; first programmable general-purpose electronic computer.",
     "start_year": 1946, "start_month": 2, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/ENIAC",
     "priorities": pri(940_000, usa=910_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Invention of the transistor",
     "description": "Bell Labs scientists Bardeen, Brattain, Shockley invent the semiconductor transistor; foundation of the digital age.",
     "start_year": 1947, "start_month": 12, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Transistor",
     "priorities": pri(950_000, usa=920_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Birth of the World Wide Web",
     "description": "Tim Berners-Lee at CERN proposes hypertext system; first website published 1991; transforms information access globally.",
     "start_year": 1989, "start_month": 3, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/History_of_the_World_Wide_Web",
     "priorities": pri(970_000, england=940_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Founding of Apple",
     "description": "Steve Jobs, Steve Wozniak, Ronald Wayne found Apple in a Los Altos garage; Apple I launched within months.",
     "start_year": 1976, "start_month": 4, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Apple_Inc.",
     "priorities": pri(930_000, usa=930_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "IBM PC launched",
     "description": "IBM introduces the personal computer based on Intel 8088 and MS-DOS; sets industry standard; \"PC compatible\" emerges.",
     "start_year": 1981, "start_month": 8, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/IBM_Personal_Computer",
     "priorities": pri(920_000, usa=910_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "First iPhone launched",
     "description": "Apple's iPhone unveiled by Steve Jobs; reshapes the mobile phone industry and consumer computing.",
     "start_year": 2007, "start_month": 6, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/IPhone_(1st_generation)",
     "priorities": pri(940_000, usa=930_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "ChatGPT launched",
     "description": "OpenAI's chatbot ChatGPT (GPT-3.5) publicly released; reaches 100M users in two months; ignites the generative-AI era.",
     "start_year": 2022, "start_month": 11, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/ChatGPT",
     "priorities": pri(950_000, usa=920_000),
     "region_weights": RW_GLOBAL},

    # =================================================================
    # MORE MUSIC + LITERATURE
    # =================================================================
    {"type": "person", "title": "Wolfgang Amadeus Mozart",
     "description": "Classical composer of staggering range; over 600 works including The Marriage of Figaro, Don Giovanni, the Requiem; died at 35.",
     "start_year": 1756, "end_year": 1791, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart",
     "priorities": pri(970_000, people=970_000, **{"arts-and-thoughts": 980_000}),
     "region_weights": RW_GLOBAL},

    {"type": "person", "title": "Frédéric Chopin",
     "description": "Polish-French Romantic composer-pianist; revolutionised piano music; died of tuberculosis at 39.",
     "start_year": 1810, "end_year": 1849, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Fr%C3%A9d%C3%A9ric_Chopin",
     "priorities": pri(910_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Richard Wagner",
     "description": "German Romantic opera composer; revolutionised music drama (Ring Cycle, Tristan und Isolde); built his own opera house at Bayreuth.",
     "start_year": 1813, "end_year": 1883, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Richard_Wagner",
     "priorities": pri(930_000, germany=920_000, people=930_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Pyotr Ilyich Tchaikovsky",
     "description": "Russian Romantic composer; The Nutcracker, Swan Lake, 1812 Overture, Symphony No. 6; among most-performed classical composers.",
     "start_year": 1840, "end_year": 1893, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pyotr_Ilyich_Tchaikovsky",
     "priorities": pri(920_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Igor Stravinsky",
     "description": "Russian-born composer; The Firebird, Petrushka, The Rite of Spring; remade 20th-century classical music three or four times.",
     "start_year": 1882, "end_year": 1971, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Igor_Stravinsky",
     "priorities": pri(920_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_GLOBAL},

    {"type": "art", "title": "The Rite of Spring premieres",
     "description": "Stravinsky's ballet premieres in Paris; near-riot in the auditorium; landmark of modernist music.",
     "start_year": 1913, "start_month": 5, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Rite_of_Spring",
     "priorities": pri(910_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_GLOBAL},

    {"type": "person", "title": "Pablo Picasso",
     "description": "Spanish painter and co-founder of Cubism; defining figure of 20th-century art; immense and varied output.",
     "start_year": 1881, "end_year": 1973, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pablo_Picasso",
     "priorities": pri(970_000, people=970_000, **{"arts-and-thoughts": 970_000}),
     "region_weights": RW_GLOBAL},

    {"type": "person", "title": "Henri Matisse",
     "description": "French Fauvist and Modernist; major innovator in colour and form; bold cut-out work in old age.",
     "start_year": 1869, "end_year": 1954, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Henri_Matisse",
     "priorities": pri(910_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Claude Monet",
     "description": "French Impressionist; Impression, Sunrise gave the movement its name; later water-lily paintings preview abstraction.",
     "start_year": 1840, "end_year": 1926, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Claude_Monet",
     "priorities": pri(940_000, france=930_000, people=940_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_GLOBAL},

    {"type": "person", "title": "Vincent van Gogh",
     "description": "Dutch post-Impressionist; sold one painting in his lifetime; mental illness; iconic Sunflowers, Starry Night.",
     "start_year": 1853, "end_year": 1890, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Vincent_van_Gogh",
     "priorities": pri(960_000, people=960_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_GLOBAL},

    {"type": "person", "title": "Fyodor Dostoevsky",
     "description": "Russian novelist; Crime and Punishment, The Brothers Karamazov; explored faith, suffering, and free will; influenced Western philosophy.",
     "start_year": 1821, "end_year": 1881, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Fyodor_Dostoevsky",
     "priorities": pri(960_000, people=970_000, **{"arts-and-thoughts": 970_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Leo Tolstoy",
     "description": "Russian novelist; War and Peace, Anna Karenina; later religious pacifism influenced Gandhi and others.",
     "start_year": 1828, "end_year": 1910, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Leo_Tolstoy",
     "priorities": pri(950_000, people=960_000, **{"arts-and-thoughts": 970_000}),
     "region_weights": RW_EU},

    # =================================================================
    # MISCELLANEOUS GAPS
    # =================================================================
    {"type": "event", "title": "Norman conquest of southern Italy",
     "description": "Norman adventurers under Robert Guiscard conquer southern Italy and Sicily from Byzantines and Arabs; Norman kingdom of Sicily.",
     "start_year": 999, "end_year": 1130, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Norman_conquest_of_southern_Italy",
     "priorities": pri(840_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Hagia Sophia converted to mosque",
     "description": "Mehmed II converts Hagia Sophia into the Ayasofya Mosque on the day Constantinople falls; remains a mosque until 1934 (and again from 2020).",
     "start_year": 1453, "start_month": 5, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Hagia_Sophia",
     "priorities": pri(870_000, **{"roman-history": 850_000}),
     "region_weights": RW_EU},

    {"type": "event", "title": "Suez Canal opens",
     "description": "Ferdinand de Lesseps's canal links Mediterranean and Red Sea; transforms global shipping and British strategic position.",
     "start_year": 1869, "start_month": 11, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Suez_Canal",
     "priorities": pri(910_000, france=860_000, england=870_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Panama Canal opens",
     "description": "US engineering effort completes a route across the Isthmus of Panama; transforms global shipping.",
     "start_year": 1914, "start_month": 8, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Panama_Canal",
     "priorities": pri(910_000, usa=900_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Spanish flu pandemic",
     "description": "Influenza pandemic kills 50-100 million worldwide; deadlier than WWI; misnamed for early Spanish press coverage.",
     "start_year": 1918, "end_year": 1920,
     "wikipedia": "https://en.wikipedia.org/wiki/1918_Spanish_flu_pandemic",
     "priorities": pri(970_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Stock Market Crash of 1929",
     "description": "Black Tuesday: Dow loses ~12% in a day; ushers in the Great Depression.",
     "start_year": 1929, "start_month": 10, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Wall_Street_Crash_of_1929",
     "priorities": pri(960_000, usa=970_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Founding of NATO",
     "description": "Twelve nations sign the North Atlantic Treaty in Washington; collective defence pact against Soviet bloc.",
     "start_year": 1949, "start_month": 4, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/NATO",
     "priorities": pri(960_000, **{"cold-war": 970_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Treaty of Rome / EEC founded",
     "description": "Six European states sign the Treaty of Rome; European Economic Community is born; nucleus of today's European Union.",
     "start_year": 1957, "start_month": 3, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Rome",
     "priorities": pri(940_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Maastricht Treaty",
     "description": "Twelve EEC members sign at Maastricht; creates the European Union and the path to the Euro.",
     "start_year": 1992, "start_month": 2, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Maastricht_Treaty",
     "priorities": pri(940_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Euro introduced",
     "description": "Euro launched as accounting currency in 11 EU states; physical notes and coins in 2002; reshapes European economy.",
     "start_year": 1999, "start_month": 1, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Euro",
     "priorities": pri(940_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Iranian Revolution",
     "description": "Pro-Western Shah overthrown; Ayatollah Khomeini returns from exile; Islamic Republic founded; reshapes Middle East.",
     "start_year": 1978, "end_year": 1979,
     "wikipedia": "https://en.wikipedia.org/wiki/Iranian_Revolution",
     "priorities": pri(950_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Iran hostage crisis",
     "description": "444-day standoff after Iranian students seize US embassy in Tehran; cripples Carter, helps elect Reagan.",
     "start_year": 1979, "start_month": 11, "start_day": 4, "end_year": 1981, "end_month": 1, "end_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Iran_hostage_crisis",
     "priorities": pri(880_000, usa=900_000, **{"cold-war": 870_000}),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Iranian Revolution"},
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
