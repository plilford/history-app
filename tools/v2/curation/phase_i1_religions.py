"""
Phase I1 — Religion content: umbrellas + new religious-history entries.

Each of christianity / islam / judaism gets:
  - An umbrella row spanning the religion's history.
  - Several new entries that didn't exist (founding events, key councils,
    schisms, modern history).

major-religions: just an umbrella row; tagged entries already in by the
tagging pass. Plus a few comparative-religion events that don't fit one
of the three Abrahamic slugs (Buddhism founding etc.).
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_MIDEAST = {"europe": 5, "americas": 2, "asia": 10, "australasia": 1, "africa": 5}
RW_EU = {"europe": 10, "americas": 3, "asia": 3, "australasia": 1, "africa": 3}
RW_ASIA = {"europe": 4, "americas": 1, "asia": 10, "australasia": 2, "africa": 4}
RW_GLOBAL = {"europe": 8, "americas": 7, "asia": 8, "australasia": 3, "africa": 5}


def pri(master: int, **extras) -> dict:
    return {"master": master, **extras}


ENTRIES = [
    # =================================================================
    # UMBRELLAS for each religion slug
    # =================================================================
    {"type": "event", "title": "Major religions of the world",
     "description": "Long-running global religious traditions — Abrahamic (Judaism, Christianity, Islam), Indic (Hinduism, Buddhism, Jainism, Sikhism), East Asian (Confucianism, Taoism, Shinto), and others — shape billions of lives.",
     "start_year": -2000, "end_year": 2025, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Major_religious_groups",
     "priorities": pri(990_000, **{"major-religions": 999_000, "arts-and-thoughts": 990_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Christianity",
     "description": "Religion based on the life and teachings of Jesus of Nazareth; today the world's largest religion with ~2.4 billion adherents.",
     "start_year": 30, "end_year": 2025, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Christianity",
     "priorities": pri(990_000, christianity=999_000, **{"major-religions": 980_000, "arts-and-thoughts": 980_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Islam",
     "description": "Religion founded on the Quran and the teachings of Muhammad; world's second-largest religion with ~1.9 billion Muslims.",
     "start_year": 610, "end_year": 2025, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Islam",
     "priorities": pri(990_000, islam=999_000, **{"major-religions": 980_000, "arts-and-thoughts": 980_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Judaism",
     "description": "Religion of the Jewish people; oldest of the Abrahamic faiths; rooted in the Torah and the covenant tradition of ancient Israel.",
     "start_year": -2000, "end_year": 2025, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Judaism",
     "priorities": pri(960_000, judaism=999_000, **{"major-religions": 950_000, "arts-and-thoughts": 960_000}),
     "region_weights": RW_GLOBAL},

    # =================================================================
    # CHRISTIANITY — additional entries
    # =================================================================
    {"type": "person", "title": "Jesus of Nazareth",
     "description": "Jewish preacher in 1st-century Roman Palestine; central figure of Christianity; crucified under Pontius Pilate; the basis of Christian theology.",
     "start_year": -4, "end_year": 33, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Jesus",
     "priorities": pri(995_000, christianity=999_000, **{"major-religions": 990_000}, people=995_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Council of Chalcedon",
     "description": "Fourth ecumenical council; defines Christ as one person in two natures; precipitates schism with Coptic, Syriac, Armenian churches.",
     "start_year": 451, "start_month": 10, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Council_of_Chalcedon",
     "priorities": pri(890_000, christianity=920_000, **{"major-religions": 870_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Christianity"},

    {"type": "event", "title": "Christianisation of Ireland",
     "description": "Traditionally attributed to St Patrick (~432); Ireland becomes a Christian centre of learning, dispatching missionaries to Britain and Europe.",
     "start_year": 432, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Christianisation_of_Ireland",
     "priorities": pri(840_000, christianity=890_000, **{"major-religions": 820_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Christianity"},

    {"type": "event", "title": "Mission of Augustine to England",
     "description": "Pope Gregory I sends Augustine to convert the Anglo-Saxons; founds the See of Canterbury; Christianises Kent.",
     "start_year": 597,
     "wikipedia": "https://en.wikipedia.org/wiki/Augustine_of_Canterbury",
     "priorities": pri(870_000, christianity=900_000, england=870_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Christianity"},

    {"type": "person", "title": "Thomas Aquinas",
     "description": "Dominican friar and philosopher; synthesised Aristotelian philosophy with Christian theology; the Summa Theologica.",
     "start_year": 1225, "end_year": 1274, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Thomas_Aquinas",
     "priorities": pri(940_000, christianity=950_000, **{"arts-and-thoughts": 950_000, "major-religions": 920_000}, people=940_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Great Schism (East-West, 1054)",
     "description": "Mutual excommunications between Pope Leo IX's legate and Patriarch Michael Cerularius split Latin and Greek Christianity.",
     "start_year": 1054, "start_month": 7, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/East%E2%80%93West_Schism",
     "priorities": pri(930_000, christianity=950_000, **{"major-religions": 910_000, "roman-history": 890_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Christianity"},

    {"type": "event", "title": "Western Schism (Three Popes)",
     "description": "Multiple rival popes claim authority for nearly 40 years (Rome, Avignon, Pisa); resolved by the Council of Constance.",
     "start_year": 1378, "end_year": 1417,
     "wikipedia": "https://en.wikipedia.org/wiki/Western_Schism",
     "priorities": pri(870_000, christianity=900_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Christianity"},

    {"type": "event", "title": "First Vatican Council (Vatican I)",
     "description": "Pope Pius IX's ecumenical council; defines papal infallibility; aimed at countering 19th-century liberalism.",
     "start_year": 1869, "start_month": 12, "start_day": 8, "end_year": 1870, "end_month": 10, "end_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Vatican_Council",
     "priorities": pri(840_000, christianity=890_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Christianity"},

    {"type": "event", "title": "Second Vatican Council (Vatican II)",
     "description": "Pope John XXIII opens the 21st ecumenical council; modernises Catholic liturgy, ecumenism, religious freedom.",
     "start_year": 1962, "start_month": 10, "start_day": 11, "end_year": 1965, "end_month": 12, "end_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Vatican_Council",
     "priorities": pri(910_000, christianity=940_000, **{"major-religions": 890_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Christianity"},

    {"type": "person", "title": "Pope John Paul II",
     "description": "Polish pope; longest pontificate of modern times; played major role in collapse of communism; canonised in 2014.",
     "start_year": 1920, "end_year": 2005, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pope_John_Paul_II",
     "priorities": pri(940_000, christianity=950_000, **{"major-religions": 920_000}, people=940_000),
     "region_weights": RW_GLOBAL},

    {"type": "person", "title": "Pope Francis",
     "description": "First Jesuit pope, first from the Americas; focus on poverty, climate, mercy; reformed Vatican governance.",
     "start_year": 1936, "is_full_life": False, "is_ongoing": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pope_Francis",
     "priorities": pri(900_000, christianity=930_000, **{"major-religions": 890_000}, people=910_000),
     "region_weights": RW_GLOBAL},

    {"type": "person", "title": "Mother Teresa",
     "description": "Albanian-Indian nun; founded the Missionaries of Charity in Kolkata; Nobel Peace Prize 1979; canonised 2016.",
     "start_year": 1910, "end_year": 1997, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mother_Teresa",
     "priorities": pri(910_000, christianity=920_000, india=890_000, **{"major-religions": 890_000}, people=920_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Mormonism founded",
     "description": "Joseph Smith publishes the Book of Mormon; founds The Church of Jesus Christ of Latter-day Saints in New York state.",
     "start_year": 1830, "start_month": 4, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Origin_of_Latter_Day_Saint_polygamy",
     "priorities": pri(820_000, christianity=860_000, usa=860_000, **{"major-religions": 800_000}),
     "region_weights": {"europe": 1, "americas": 10, "asia": 1, "australasia": 2, "africa": 1},
     "first_zoom_out": "Christianity"},

    # =================================================================
    # ISLAM — additional entries
    # =================================================================
    {"type": "person", "title": "Muhammad",
     "description": "Arabian prophet; founder of Islam; recipient of the Quranic revelations; military and political leader of the early Muslim community.",
     "start_year": 570, "end_year": 632, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Muhammad",
     "priorities": pri(990_000, islam=999_000, **{"major-religions": 990_000}, people=990_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Muhammad's first revelation",
     "description": "Muhammad reports receiving the first Quranic revelation from the angel Gabriel in the cave at Mount Hira.",
     "start_year": 610, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Muhammad",
     "priorities": pri(940_000, islam=960_000, **{"major-religions": 920_000}),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Islam"},

    {"type": "event", "title": "Hijra",
     "description": "Muhammad and the early Muslim community emigrate from Mecca to Medina; conventional start of the Islamic calendar.",
     "start_year": 622, "start_month": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Hijra_(Islam)",
     "priorities": pri(960_000, islam=970_000, **{"major-religions": 940_000}),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Islam"},

    {"type": "event", "title": "Rashidun Caliphate",
     "description": "First four 'rightly guided' caliphs after Muhammad; massive Arab conquests across the Levant, Egypt, Persia.",
     "start_year": 632, "end_year": 661,
     "wikipedia": "https://en.wikipedia.org/wiki/Rashidun_Caliphate",
     "priorities": pri(910_000, islam=940_000, **{"major-religions": 880_000}),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Islam"},

    {"type": "event", "title": "Sunni-Shia split",
     "description": "Dispute over succession to Muhammad fractures the early Muslim community; deepens at Karbala 680.",
     "start_year": 656, "end_year": 680,
     "wikipedia": "https://en.wikipedia.org/wiki/Sunni%E2%80%93Shia_relations",
     "priorities": pri(940_000, islam=960_000, **{"major-religions": 920_000}),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Islam"},

    {"type": "event", "title": "Battle of Karbala",
     "description": "Husayn ibn Ali, grandson of Muhammad, killed by Umayyad forces in Iraq; central event in Shia identity and mourning.",
     "start_year": 680, "start_month": 10, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Karbala",
     "priorities": pri(880_000, islam=920_000),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Sunni-Shia split"},

    {"type": "event", "title": "Conquest of Iberia (711)",
     "description": "Umayyad-Berber army under Tariq ibn Ziyad crosses Gibraltar; destroys the Visigothic kingdom of Spain.",
     "start_year": 711,
     "wikipedia": "https://en.wikipedia.org/wiki/Umayyad_conquest_of_Hispania",
     "priorities": pri(910_000, islam=920_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Islam"},

    {"type": "event", "title": "Caliphate of Córdoba",
     "description": "Abd al-Rahman III proclaims caliphate at Córdoba; al-Andalus reaches cultural and political peak; great library and mosque.",
     "start_year": 929, "end_year": 1031,
     "wikipedia": "https://en.wikipedia.org/wiki/Caliphate_of_C%C3%B3rdoba",
     "priorities": pri(900_000, islam=920_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Islam"},

    {"type": "event", "title": "Founding of Fatimid Caliphate",
     "description": "Shia Fatimids establish caliphate in North Africa, rival to Sunni Abbasids; later move capital to Cairo (969).",
     "start_year": 909, "end_year": 1171,
     "wikipedia": "https://en.wikipedia.org/wiki/Fatimid_Caliphate",
     "priorities": pri(880_000, islam=910_000),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Islam"},

    {"type": "event", "title": "Founding of Cairo (al-Qahira)",
     "description": "Fatimids found their new capital just north of Fustat; remains Egypt's capital ever since.",
     "start_year": 969, "start_month": 7, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Cairo",
     "priorities": pri(870_000, islam=890_000),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Founding of Fatimid Caliphate"},

    {"type": "event", "title": "Al-Azhar founded",
     "description": "Founded by Fatimids as a Shia learning centre; later becomes the most influential Sunni university and one of the world's oldest universities.",
     "start_year": 970, "start_month": 4, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Al-Azhar_University",
     "priorities": pri(870_000, islam=900_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Islam"},

    {"type": "event", "title": "Wahhabism founded",
     "description": "Muhammad ibn Abd al-Wahhab launches puritan Sunni movement in the Najd; aligns with the House of Saud; dominant religious doctrine of modern Saudi Arabia.",
     "start_year": 1744, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Wahhabism",
     "priorities": pri(860_000, islam=890_000),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Islam"},

    {"type": "event", "title": "Muslim Brotherhood founded",
     "description": "Hassan al-Banna founds the Muslim Brotherhood in Egypt; pioneering pan-Islamic political movement.",
     "start_year": 1928, "start_month": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Muslim_Brotherhood",
     "priorities": pri(880_000, islam=910_000),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Islam"},

    {"type": "event", "title": "Rushdie fatwa",
     "description": "Ayatollah Khomeini issues a death fatwa against Salman Rushdie over The Satanic Verses; deep international rift over free speech and Islam.",
     "start_year": 1989, "start_month": 2, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Satanic_Verses_controversy",
     "priorities": pri(870_000, islam=890_000, england=860_000),
     "region_weights": RW_MIDEAST},

    # =================================================================
    # JUDAISM — additional entries
    # =================================================================
    {"type": "person", "title": "Abraham",
     "description": "Patriarch of the Hebrew Bible; ancestor of the Jewish people; foundational figure for Judaism, Christianity, and Islam.",
     "start_year": -1813, "end_year": -1638, "is_full_life": True, "date_uncertain": True,
     "display_date": "traditional dates c. 1800 BCE",
     "wikipedia": "https://en.wikipedia.org/wiki/Abraham",
     "priorities": pri(960_000, judaism=990_000, **{"major-religions": 940_000}, people=970_000),
     "region_weights": RW_MIDEAST},

    {"type": "person", "title": "Moses",
     "description": "Hebrew prophet; received the Ten Commandments at Mount Sinai; led the Israelites out of Egypt; central figure of the Torah.",
     "start_year": -1391, "end_year": -1271, "is_full_life": True, "date_uncertain": True,
     "display_date": "traditional dates c. 1400 BCE",
     "wikipedia": "https://en.wikipedia.org/wiki/Moses",
     "priorities": pri(960_000, judaism=990_000, **{"major-religions": 940_000}, people=970_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Exodus from Egypt",
     "description": "Biblical narrative of Hebrew slaves' liberation under Moses; foundational story of Jewish identity (historical evidence debated).",
     "start_year": -1300, "date_uncertain": True,
     "display_date": "traditional date c. 13th century BCE",
     "wikipedia": "https://en.wikipedia.org/wiki/The_Exodus",
     "priorities": pri(910_000, judaism=950_000, **{"major-religions": 890_000}),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Judaism"},

    {"type": "person", "title": "King David",
     "description": "Second king of Israel; united tribes; conquered Jerusalem; in Jewish tradition the ancestor of the Messiah; harpist and psalmist.",
     "start_year": -1010, "end_year": -970, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/David",
     "priorities": pri(940_000, judaism=960_000, people=950_000),
     "region_weights": RW_MIDEAST},

    {"type": "person", "title": "King Solomon",
     "description": "Son of David; third king of Israel; legendary for wisdom and wealth; built the First Temple in Jerusalem.",
     "start_year": -970, "end_year": -931, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Solomon",
     "priorities": pri(930_000, judaism=950_000, people=940_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Construction of Solomon's Temple",
     "description": "First Temple built in Jerusalem; centre of ancient Israelite worship; destroyed by Nebuchadnezzar in 586 BCE.",
     "start_year": -957, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Solomon%27s_Temple",
     "priorities": pri(890_000, judaism=940_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Judaism"},

    {"type": "event", "title": "Maccabean revolt",
     "description": "Jewish revolt against the Seleucid Empire; restoration of Temple worship celebrated as Hanukkah; brief Hasmonean dynasty.",
     "start_year": -167, "end_year": -160,
     "wikipedia": "https://en.wikipedia.org/wiki/Maccabean_Revolt",
     "priorities": pri(890_000, judaism=920_000),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Judaism"},

    {"type": "event", "title": "Talmud completed (Babylonian)",
     "description": "Rabbinic commentary on the Mishnah completed in Sasanian Mesopotamia; central text of Rabbinic Judaism.",
     "start_year": 500, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Talmud",
     "priorities": pri(900_000, judaism=940_000, **{"arts-and-thoughts": 910_000, "major-religions": 880_000}),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Judaism"},

    {"type": "person", "title": "Maimonides",
     "description": "Medieval Sephardi Torah scholar, philosopher, physician; Guide for the Perplexed and Mishneh Torah; preeminent Jewish thinker of the Middle Ages.",
     "start_year": 1138, "end_year": 1204, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Maimonides",
     "priorities": pri(900_000, judaism=930_000, people=910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Expulsion of Jews from Spain",
     "description": "Ferdinand and Isabella's Alhambra Decree forces ~200,000 Jews to convert or leave; ends seven centuries of Sephardi Jewish life in Iberia.",
     "start_year": 1492, "start_month": 7, "start_day": 31,
     "wikipedia": "https://en.wikipedia.org/wiki/Alhambra_Decree",
     "priorities": pri(910_000, judaism=950_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Judaism"},

    {"type": "event", "title": "Chmielnicki Uprising",
     "description": "Cossack uprising in Ukraine massacres tens of thousands of Jews; trauma reshapes Eastern European Jewish life.",
     "start_year": 1648, "end_year": 1657,
     "wikipedia": "https://en.wikipedia.org/wiki/Khmelnytsky_Uprising",
     "priorities": pri(830_000, judaism=890_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Judaism"},

    {"type": "event", "title": "Dreyfus Affair",
     "description": "Jewish French officer wrongly convicted of treason; bitter public controversy; Zola's J'Accuse...!; catalyses Theodor Herzl's Zionism.",
     "start_year": 1894, "end_year": 1906,
     "wikipedia": "https://en.wikipedia.org/wiki/Dreyfus_affair",
     "priorities": pri(910_000, judaism=920_000, france=920_000),
     "region_weights": RW_EU},

    {"type": "person", "title": "Theodor Herzl",
     "description": "Austro-Hungarian Jewish journalist; The Jewish State (1896); founder of modern political Zionism.",
     "start_year": 1860, "end_year": 1904, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Theodor_Herzl",
     "priorities": pri(910_000, judaism=940_000, people=920_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "First Zionist Congress",
     "description": "Herzl convenes congress in Basel; founds the World Zionist Organization; commits to a Jewish homeland in Palestine.",
     "start_year": 1897, "start_month": 8, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Zionist_Congress",
     "priorities": pri(900_000, judaism=930_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Judaism"},

    {"type": "event", "title": "Balfour Declaration",
     "description": "British Foreign Secretary Balfour writes Lord Rothschild supporting a Jewish national home in Palestine; rests on assumed continued British control.",
     "start_year": 1917, "start_month": 11, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Balfour_Declaration",
     "priorities": pri(940_000, judaism=950_000, england=920_000),
     "region_weights": RW_MIDEAST,
     "first_zoom_out": "Judaism"},

    {"type": "event", "title": "Founding of Israel",
     "description": "David Ben-Gurion declares the State of Israel as the British Mandate ends; war with Arab neighbours begins immediately.",
     "start_year": 1948, "start_month": 5, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Israeli_Declaration_of_Independence",
     "priorities": pri(970_000, judaism=970_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Six-Day War",
     "description": "Israel captures Sinai, Gaza, West Bank, East Jerusalem and Golan Heights from Egypt, Jordan, Syria; redraws Middle East map.",
     "start_year": 1967, "start_month": 6, "start_day": 5, "end_month": 6, "end_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Six-Day_War",
     "priorities": pri(950_000, judaism=920_000, **{"cold-war": 910_000}),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Yom Kippur War",
     "description": "Egypt and Syria launch surprise attack on Israel during the Yom Kippur holiday; leads to OPEC oil embargo.",
     "start_year": 1973, "start_month": 10, "start_day": 6, "end_month": 10, "end_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Yom_Kippur_War",
     "priorities": pri(930_000, judaism=900_000, **{"cold-war": 900_000}),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Camp David Accords",
     "description": "Sadat, Begin and Carter agree framework for Egypt-Israel peace at Camp David; Israel cedes Sinai for diplomatic recognition.",
     "start_year": 1978, "start_month": 9, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Camp_David_Accords",
     "priorities": pri(910_000, judaism=910_000, usa=890_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "First Intifada",
     "description": "Palestinian uprising in West Bank and Gaza against Israeli occupation; lasts five years; sets stage for Oslo Accords.",
     "start_year": 1987, "start_month": 12, "start_day": 9, "end_year": 1993, "end_month": 9, "end_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Intifada",
     "priorities": pri(880_000, judaism=890_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Oslo Accords",
     "description": "Rabin-Arafat handshake at the White House; framework for Israeli-Palestinian peace; mutual recognition; Palestinian Authority established.",
     "start_year": 1993, "start_month": 9, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Oslo_Accords",
     "priorities": pri(910_000, judaism=920_000),
     "region_weights": RW_MIDEAST},

    {"type": "event", "title": "Assassination of Yitzhak Rabin",
     "description": "Israeli prime minister and Nobel laureate shot dead at a Tel Aviv peace rally by a right-wing Israeli extremist.",
     "start_year": 1995, "start_month": 11, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Assassination_of_Yitzhak_Rabin",
     "priorities": pri(910_000, judaism=920_000),
     "region_weights": RW_MIDEAST},

    # =================================================================
    # OTHER MAJOR RELIGIONS (Buddhism / Hinduism / Sikhism / etc.)
    # =================================================================
    {"type": "person", "title": "Confucius",
     "description": "Chinese philosopher and political theorist; the Analects codify his teachings on ethics, family, and government; defining figure of East Asian thought.",
     "start_year": -551, "end_year": -479, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Confucius",
     "priorities": pri(990_000, china=990_000, people=990_000, **{"arts-and-thoughts": 990_000, "major-religions": 970_000}),
     "region_weights": RW_ASIA},

    {"type": "person", "title": "Laozi",
     "description": "Legendary Chinese sage; traditional author of the Tao Te Ching; founder of philosophical Taoism.",
     "start_year": -571, "end_year": -471, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Laozi",
     "priorities": pri(940_000, china=940_000, **{"arts-and-thoughts": 950_000, "major-religions": 920_000}, people=950_000),
     "region_weights": RW_ASIA},

    {"type": "art", "title": "Tao Te Ching",
     "description": "Brief, gnomic philosophical text attributed to Laozi; foundational scripture of Taoism; among the most-translated works in world literature.",
     "start_year": -400, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tao_Te_Ching",
     "priorities": pri(920_000, china=940_000, **{"arts-and-thoughts": 940_000, "major-religions": 900_000}),
     "region_weights": RW_ASIA,
     "first_zoom_out": "Major religions of the world"},

    {"type": "person", "title": "Mencius",
     "description": "Second great Confucian sage; tour of Warring States; argued human nature is innately good.",
     "start_year": -372, "end_year": -289, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mencius",
     "priorities": pri(870_000, china=900_000, people=890_000, **{"arts-and-thoughts": 900_000, "major-religions": 870_000}),
     "region_weights": RW_ASIA},

    {"type": "event", "title": "Buddha's enlightenment",
     "description": "Siddhartha Gautama attains enlightenment under the Bodhi tree at Bodh Gaya; foundational moment of Buddhism.",
     "start_year": -528, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Gautama_Buddha",
     "priorities": pri(960_000, india=960_000, **{"major-religions": 950_000, "arts-and-thoughts": 960_000}),
     "region_weights": RW_ASIA,
     "first_zoom_out": "Major religions of the world"},

    {"type": "person", "title": "Gautama Buddha",
     "description": "Wandering teacher in northern India; founder of Buddhism; insights into suffering, attachment, and the eightfold path.",
     "start_year": -563, "end_year": -483, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Gautama_Buddha",
     "priorities": pri(980_000, india=970_000, people=980_000, **{"major-religions": 980_000, "arts-and-thoughts": 980_000}),
     "region_weights": RW_ASIA},

    {"type": "event", "title": "Ashoka spreads Buddhism",
     "description": "Maurya emperor Ashoka becomes Buddhist after Kalinga and sends missions across South and Southeast Asia; Buddhism transformed from a regional movement.",
     "start_year": -261, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ashoka",
     "priorities": pri(920_000, india=950_000, **{"major-religions": 900_000}),
     "region_weights": RW_ASIA,
     "first_zoom_out": "Buddha's enlightenment"},

    {"type": "event", "title": "Buddhism reaches China",
     "description": "Buddhism brought to China via the Silk Road during the Han dynasty; reshapes Chinese religious life over centuries.",
     "start_year": 67, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Chinese_Buddhism",
     "priorities": pri(880_000, china=900_000, **{"major-religions": 880_000}),
     "region_weights": RW_ASIA,
     "first_zoom_out": "Major religions of the world"},

    {"type": "event", "title": "Bhagavad Gita composed",
     "description": "Sanskrit verse dialogue between Arjuna and Krishna within the Mahabharata; foundational Hindu text on dharma and yoga.",
     "start_year": -200, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Bhagavad_Gita",
     "priorities": pri(940_000, india=950_000, **{"arts-and-thoughts": 950_000, "major-religions": 920_000}),
     "region_weights": RW_ASIA,
     "first_zoom_out": "Major religions of the world"},

    {"type": "event", "title": "Mahabharata composed",
     "description": "Vast Sanskrit epic of the Bharata war; longest epic poem ever written; central to Hindu culture.",
     "start_year": -400, "end_year": 400, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mahabharata",
     "priorities": pri(920_000, india=940_000, **{"arts-and-thoughts": 940_000, "major-religions": 900_000}),
     "region_weights": RW_ASIA},

    {"type": "event", "title": "Ramayana composed",
     "description": "Sanskrit epic of Rama; the model of dharmic kingship and conjugal love; central to Hindu literature and Southeast Asian culture.",
     "start_year": -500, "end_year": 0, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ramayana",
     "priorities": pri(910_000, india=940_000, **{"arts-and-thoughts": 930_000, "major-religions": 900_000}),
     "region_weights": RW_ASIA},

    {"type": "person", "title": "Guru Nanak",
     "description": "Indian spiritual teacher; founder of Sikhism; emphasised the formlessness of the One God and equality of all peoples.",
     "start_year": 1469, "end_year": 1539, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Guru_Nanak",
     "priorities": pri(910_000, india=940_000, **{"major-religions": 900_000, "arts-and-thoughts": 900_000}, people=920_000),
     "region_weights": RW_ASIA},

    {"type": "event", "title": "Founding of Sikhism",
     "description": "Guru Nanak begins teaching at age 30; founds Sikh religion in the Punjab; succeeded by nine more Gurus.",
     "start_year": 1499, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Sikhism",
     "priorities": pri(890_000, india=920_000, **{"major-religions": 880_000}),
     "region_weights": RW_ASIA,
     "first_zoom_out": "Major religions of the world"},

    {"type": "event", "title": "Adoption of Shinto as state religion",
     "description": "Meiji-era State Shinto bonds religion to Japanese imperial state; reversed by SCAP after WWII.",
     "start_year": 1868, "end_year": 1946,
     "wikipedia": "https://en.wikipedia.org/wiki/State_Shinto",
     "priorities": pri(830_000, japan=870_000, **{"major-religions": 820_000}),
     "region_weights": RW_ASIA},

    {"type": "person", "title": "14th Dalai Lama",
     "description": "Tenzin Gyatso; spiritual leader of Tibetan Buddhism in exile since 1959; Nobel Peace Prize 1989.",
     "start_year": 1935, "is_full_life": False, "is_ongoing": True,
     "wikipedia": "https://en.wikipedia.org/wiki/14th_Dalai_Lama",
     "priorities": pri(910_000, china=890_000, **{"major-religions": 910_000}, people=920_000),
     "region_weights": RW_ASIA},

    {"type": "event", "title": "Chinese annexation of Tibet",
     "description": "PLA invades Tibet; Dalai Lama later flees to India after 1959 uprising; ongoing dispute over Tibetan religious freedom.",
     "start_year": 1950, "start_month": 10, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Annexation_of_Tibet_by_the_People%27s_Republic_of_China",
     "priorities": pri(880_000, china=910_000, **{"major-religions": 870_000}),
     "region_weights": RW_ASIA},
]


def main() -> int:
    base = next_available_id()
    for i, en in enumerate(ENTRIES):
        en["id"] = base + i
    n = append_entries(ENTRIES)
    print(f"Appended {n} religion entries (IDs {base}..{base+n-1}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
