"""
Phase F1 — Children for Chinese and Indian high-priority umbrellas.

Targets:
  China:  Han / Tang / Song / Yuan / Ming / Qing / Warring States / 3K /
          Sui / Three Kingdoms / late Qing transition
  India:  Maurya / Gupta / Delhi Sultanate / Vijayanagara / Mughal

Each child references its umbrella via first_zoom_out so the rollup zoom
collapses them at level 1+ as expected.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_CHINA = {"europe": 2, "americas": 1, "asia": 10, "australasia": 2, "africa": 1}
RW_INDIA = {"europe": 3, "americas": 1, "asia": 10, "australasia": 2, "africa": 2}


def cn(master_pri: int, china_pri: int | None = None, **extra) -> dict:
    if china_pri is None:
        china_pri = min(999_000, master_pri + 30_000)
    out = {"master": master_pri, "china": china_pri}
    out.update(extra)
    return out


def ind(master_pri: int, india_pri: int | None = None, **extra) -> dict:
    if india_pri is None:
        india_pri = min(999_000, master_pri + 30_000)
    out = {"master": master_pri, "india": india_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- Warring States (precursor) -----
    {"type": "event", "title": "Battle of Changping",
     "description": "Qin general Bai Qi annihilates Zhao army; 400,000 Zhao soldiers reportedly buried alive; clears Qin's path to unification.",
     "start_year": -260,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Changping",
     "priorities": cn(820_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Warring States period"},

    {"type": "event", "title": "Qin Shi Huang unifies China",
     "description": "Qin conquers the other six warring states; first emperor of unified China; standardises script, currency, weights.",
     "start_year": -221,
     "wikipedia": "https://en.wikipedia.org/wiki/Qin_Shi_Huang",
     "priorities": cn(960_000), "region_weights": RW_CHINA},

    {"type": "event", "title": "Burning of books and burying of scholars",
     "description": "Qin Shi Huang's notorious campaign against Confucian thought; classics burned, hundreds of scholars allegedly executed.",
     "start_year": -213, "end_year": -212,
     "wikipedia": "https://en.wikipedia.org/wiki/Burning_of_books_and_burying_of_scholars",
     "priorities": cn(840_000), "region_weights": RW_CHINA},

    {"type": "event", "title": "Terracotta Army constructed",
     "description": "~8,000 life-size terracotta warriors buried with Qin Shi Huang at Xi'an; one of the great archaeological finds of the 20th century.",
     "start_year": -246, "end_year": -210,
     "wikipedia": "https://en.wikipedia.org/wiki/Terracotta_Army",
     "priorities": cn(930_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_CHINA},

    {"type": "event", "title": "Great Wall of China (Qin)",
     "description": "Qin Shi Huang links and extends earlier walls into a first version of the Great Wall; subsequent dynasties continue rebuilding.",
     "start_year": -221, "end_year": -207,
     "wikipedia": "https://en.wikipedia.org/wiki/Great_Wall_of_China",
     "priorities": cn(950_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_CHINA},

    # ----- Han dynasty -----
    {"type": "event", "title": "Reign of Emperor Wu of Han",
     "description": "Longest Han reign; vastly expands the empire into Central Asia and Korea; establishes Confucianism as state ideology; opens the Silk Road.",
     "start_year": -141, "end_year": -87,
     "wikipedia": "https://en.wikipedia.org/wiki/Emperor_Wu_of_Han",
     "priorities": cn(900_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Han dynasty"},

    {"type": "event", "title": "Silk Road established",
     "description": "Han diplomat Zhang Qian's missions to Central Asia open continental trade routes; Chinese silk flows west, Buddhism east.",
     "start_year": -130, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Silk_Road",
     "priorities": cn(940_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Han dynasty"},

    {"type": "event", "title": "Han invention of paper",
     "description": "Court official Cai Lun perfects papermaking from mulberry bark and other fibres; medium spreads slowly through Asia and to Europe.",
     "start_year": 105,
     "wikipedia": "https://en.wikipedia.org/wiki/Paper",
     "priorities": cn(950_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Han dynasty"},

    {"type": "event", "title": "Yellow Turban Rebellion",
     "description": "Massive Daoist-inspired peasant rebellion fatally weakens Han central authority; leads to the Three Kingdoms era.",
     "start_year": 184, "end_year": 205,
     "wikipedia": "https://en.wikipedia.org/wiki/Yellow_Turban_Rebellion",
     "priorities": cn(840_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Han dynasty"},

    {"type": "event", "title": "Wang Mang and Xin dynasty",
     "description": "Han regent Wang Mang usurps the throne, declares the short-lived Xin dynasty; reforms unwound after his death in 23 CE.",
     "start_year": 9, "end_year": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Wang_Mang",
     "priorities": cn(800_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Han dynasty"},

    {"type": "event", "title": "Battle of Red Cliffs",
     "description": "Sun Quan and Liu Bei defeat Cao Cao's vastly larger northern fleet; secures division of China into Three Kingdoms.",
     "start_year": 208, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Red_Cliffs",
     "priorities": cn(870_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Three Kingdoms period"},

    # ----- Sui & Tang -----
    {"type": "event", "title": "Sui dynasty reunifies China",
     "description": "After three centuries of division, the Sui reunite China; build the Grand Canal; collapse from over-extension.",
     "start_year": 581, "end_year": 618,
     "wikipedia": "https://en.wikipedia.org/wiki/Sui_dynasty",
     "priorities": cn(870_000), "region_weights": RW_CHINA},

    {"type": "event", "title": "Grand Canal completed",
     "description": "Sui Emperor Yang's massive labour project links north and south China by waterway; foundational infrastructure for the Tang and beyond.",
     "start_year": 605, "end_year": 609,
     "wikipedia": "https://en.wikipedia.org/wiki/Grand_Canal_(China)",
     "priorities": cn(880_000, **{"arts-and-thoughts": 850_000}),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Sui dynasty reunifies China"},

    {"type": "event", "title": "Tang dynasty founded",
     "description": "Li Yuan overthrows the Sui and founds the Tang; first century is a cultural and military zenith of medieval China.",
     "start_year": 618, "start_month": 6, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Tang_dynasty",
     "priorities": cn(900_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Tang dynasty"},

    {"type": "event", "title": "Reign of Empress Wu Zetian",
     "description": "Only female emperor in Chinese history; founded short-lived Zhou interregnum; reigned in her own right 690-705.",
     "start_year": 690, "end_year": 705, "start_month": 10, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Wu_Zetian",
     "priorities": cn(890_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Tang dynasty"},

    {"type": "event", "title": "Reign of Emperor Xuanzong of Tang",
     "description": "Tang golden age and then collapse; patron of poets Li Bai and Du Fu; reign ended by the An Lushan rebellion.",
     "start_year": 712, "end_year": 756,
     "wikipedia": "https://en.wikipedia.org/wiki/Emperor_Xuanzong_of_Tang",
     "priorities": cn(870_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Tang dynasty"},

    {"type": "event", "title": "An Lushan Rebellion",
     "description": "Devastating rebellion that may have caused tens of millions of deaths; Tang dynasty never fully recovers.",
     "start_year": 755, "end_year": 763,
     "wikipedia": "https://en.wikipedia.org/wiki/An_Lushan_Rebellion",
     "priorities": cn(900_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Tang dynasty"},

    {"type": "person", "title": "Li Bai (Li Po)",
     "description": "Tang poet of romantic excess; with Du Fu the greatest of Chinese poets; famous for wine and the moon.",
     "start_year": 701, "end_year": 762, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Li_Bai",
     "priorities": cn(890_000, people=900_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_CHINA},

    {"type": "person", "title": "Du Fu",
     "description": "Tang poet of moral seriousness and political concern; widely considered China's greatest poet of the Confucian conscience.",
     "start_year": 712, "end_year": 770, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Du_Fu",
     "priorities": cn(880_000, people=900_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_CHINA},

    # ----- Song & Yuan -----
    {"type": "event", "title": "Song invention of gunpowder",
     "description": "Chinese alchemists develop saltpetre-sulphur-charcoal formula; first military use against Mongols at Kaifeng 1232.",
     "start_year": 950, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/History_of_gunpowder",
     "priorities": cn(960_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Song dynasty"},

    {"type": "event", "title": "Song movable-type printing",
     "description": "Bi Sheng develops movable clay type centuries before Gutenberg; never quite displaces woodblock printing in China.",
     "start_year": 1040, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Bi_Sheng",
     "priorities": cn(930_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Song dynasty"},

    {"type": "event", "title": "Magnetic compass for navigation",
     "description": "Song sailors adopt the magnetic compass for navigation; technology spreads west via Arab traders.",
     "start_year": 1090, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Compass",
     "priorities": cn(910_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Song dynasty"},

    {"type": "event", "title": "Jurchen Jin conquest of northern China",
     "description": "Jurchen Jin dynasty captures Kaifeng; Northern Song collapses; rump Southern Song rules from Hangzhou.",
     "start_year": 1127, "start_month": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Jin%E2%80%93Song_Wars",
     "priorities": cn(830_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Song dynasty"},

    {"type": "event", "title": "Mongol conquest of Song China",
     "description": "Kublai Khan completes the Mongol conquest of southern China; Yuan dynasty established; first non-Han rule over all of China.",
     "start_year": 1268, "end_year": 1279,
     "wikipedia": "https://en.wikipedia.org/wiki/Mongol_conquest_of_China",
     "priorities": cn(900_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Yuan dynasty"},

    {"type": "event", "title": "Marco Polo at the Yuan court",
     "description": "Venetian merchant claims to serve Kublai Khan for ~17 years; his Travels shape European views of Asia for centuries.",
     "start_year": 1271, "end_year": 1295,
     "wikipedia": "https://en.wikipedia.org/wiki/Marco_Polo",
     "priorities": cn(900_000), "region_weights": RW_CHINA},

    {"type": "event", "title": "Red Turban Rebellion",
     "description": "Mass uprising overthrows the Mongol Yuan dynasty; rebel leader Zhu Yuanzhang founds the Ming.",
     "start_year": 1351, "end_year": 1368,
     "wikipedia": "https://en.wikipedia.org/wiki/Red_Turban_Rebellion",
     "priorities": cn(850_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Yuan dynasty"},

    # ----- Ming -----
    {"type": "event", "title": "Hongwu Emperor founds Ming",
     "description": "Former peasant rebel leader Zhu Yuanzhang proclaims the Ming dynasty in Nanjing; centralises imperial power.",
     "start_year": 1368, "start_month": 1, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Hongwu_Emperor",
     "priorities": cn(900_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Ming dynasty"},

    {"type": "event", "title": "Zheng He's treasure voyages",
     "description": "Ming admiral leads seven huge maritime expeditions to Southeast Asia, India, Arabia, and East Africa; abruptly ended after his death.",
     "start_year": 1405, "end_year": 1433,
     "wikipedia": "https://en.wikipedia.org/wiki/Zheng_He",
     "priorities": cn(930_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Ming dynasty"},

    {"type": "event", "title": "Forbidden City completed",
     "description": "Yongle Emperor moves Ming capital to Beijing; vast palace complex built in 14 years; serves as imperial residence for 500 years.",
     "start_year": 1420,
     "wikipedia": "https://en.wikipedia.org/wiki/Forbidden_City",
     "priorities": cn(940_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Ming dynasty"},

    {"type": "event", "title": "Great Wall (Ming reconstruction)",
     "description": "Ming dynasty rebuilds the Great Wall in stone and brick; this is the wall visible today.",
     "start_year": 1474, "end_year": 1644, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Great_Wall_of_China",
     "priorities": cn(890_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_CHINA,
     "first_zoom_out": "Ming dynasty"},

    {"type": "event", "title": "Late Ming silver economy",
     "description": "Silver from Spanish American mines pours into China through Manila; transforms Ming economy and ties it to global trade.",
     "start_year": 1571, "end_year": 1644, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Economy_of_the_Ming_dynasty",
     "priorities": cn(840_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Ming dynasty"},

    {"type": "event", "title": "Fall of Beijing (1644)",
     "description": "Rebel leader Li Zicheng captures Beijing; Chongzhen Emperor commits suicide; Manchu forces enter through Shanhai Pass and found the Qing.",
     "start_year": 1644, "start_month": 4, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Ming%E2%80%93Qing_transition",
     "priorities": cn(890_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Ming dynasty"},

    # ----- Qing -----
    {"type": "event", "title": "Qing dynasty founded",
     "description": "Manchu Qing dynasty conquers all of China after the Ming collapse; rules until 1912 — last imperial dynasty.",
     "start_year": 1644, "end_year": 1912,
     "wikipedia": "https://en.wikipedia.org/wiki/Qing_dynasty",
     "priorities": cn(940_000), "region_weights": RW_CHINA},

    {"type": "event", "title": "Reign of the Kangxi Emperor",
     "description": "Longest reign in Chinese history; consolidates Qing rule, suppresses revolts, sponsors monumental encyclopaedic projects.",
     "start_year": 1661, "end_year": 1722,
     "wikipedia": "https://en.wikipedia.org/wiki/Kangxi_Emperor",
     "priorities": cn(880_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Qing dynasty founded"},

    {"type": "event", "title": "Reign of the Qianlong Emperor",
     "description": "High Qing reign of 60 years; territorial expansion in Central Asia; cultural flowering; corruption and rebellion begin to surface late.",
     "start_year": 1735, "end_year": 1796,
     "wikipedia": "https://en.wikipedia.org/wiki/Qianlong_Emperor",
     "priorities": cn(870_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Qing dynasty founded"},

    {"type": "event", "title": "Macartney Embassy",
     "description": "British diplomatic mission to Qianlong fails to secure trade concessions; emperor's dismissal ('we possess all things') becomes notorious.",
     "start_year": 1793, "start_month": 9, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Macartney_Embassy",
     "priorities": cn(840_000, **{"england": 830_000}), "region_weights": RW_CHINA},

    {"type": "event", "title": "White Lotus Rebellion",
     "description": "Major sectarian rebellion in central China; takes nine years to suppress; reveals Qing institutional decline.",
     "start_year": 1794, "end_year": 1804,
     "wikipedia": "https://en.wikipedia.org/wiki/White_Lotus_Rebellion",
     "priorities": cn(800_000), "region_weights": RW_CHINA,
     "first_zoom_out": "Qing dynasty founded"},

    {"type": "event", "title": "Second Opium War",
     "description": "Anglo-French force burns the Summer Palace and forces further humiliating treaties on the Qing.",
     "start_year": 1856, "end_year": 1860,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Opium_War",
     "priorities": cn(870_000, **{"england": 870_000}), "region_weights": RW_CHINA},

    {"type": "event", "title": "Self-Strengthening Movement",
     "description": "Qing officials promote selective adoption of Western military and industrial technology; insufficient to reverse decline.",
     "start_year": 1861, "end_year": 1895,
     "wikipedia": "https://en.wikipedia.org/wiki/Self-Strengthening_Movement",
     "priorities": cn(810_000), "region_weights": RW_CHINA},

    {"type": "event", "title": "Empress Dowager Cixi rules",
     "description": "De-facto ruler of late Qing China for 47 years through three reigns; conservative blocker of Hundred Days' Reform.",
     "start_year": 1861, "end_year": 1908,
     "wikipedia": "https://en.wikipedia.org/wiki/Empress_Dowager_Cixi",
     "priorities": cn(870_000), "region_weights": RW_CHINA},

    {"type": "event", "title": "Boxer Rebellion",
     "description": "Anti-foreign uprising backed by Cixi; Eight-Nation Alliance crushes it and imposes Boxer Protocol; further humiliation.",
     "start_year": 1899, "end_year": 1901,
     "wikipedia": "https://en.wikipedia.org/wiki/Boxer_Rebellion",
     "priorities": cn(890_000), "region_weights": RW_CHINA},

    {"type": "event", "title": "Xinhai Revolution",
     "description": "Republican revolution ends the Qing dynasty and 2,000 years of imperial rule; Sun Yat-sen becomes first president of the Republic.",
     "start_year": 1911, "start_month": 10, "start_day": 10, "end_year": 1912, "end_month": 2, "end_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Xinhai_Revolution",
     "priorities": cn(940_000), "region_weights": RW_CHINA},

    # ----- India: Maurya / Gupta / Delhi / Vijayanagara / Mughal -----
    {"type": "event", "title": "Chandragupta Maurya unifies northern India",
     "description": "Chandragupta and his minister Chanakya overthrow the Nanda dynasty and build the Maurya empire across the Gangetic plain.",
     "start_year": -322,
     "wikipedia": "https://en.wikipedia.org/wiki/Chandragupta_Maurya",
     "priorities": ind(890_000), "region_weights": RW_INDIA,
     "first_zoom_out": "Maurya Empire"},

    {"type": "event", "title": "Reign of Ashoka the Great",
     "description": "Maurya emperor converts to Buddhism after the Kalinga War; spreads Buddhism via missions; pillars and edicts across the subcontinent.",
     "start_year": -268, "end_year": -232,
     "wikipedia": "https://en.wikipedia.org/wiki/Ashoka",
     "priorities": ind(940_000), "region_weights": RW_INDIA,
     "first_zoom_out": "Maurya Empire"},

    {"type": "event", "title": "Kalinga War",
     "description": "Ashoka's brutal conquest of Kalinga; horror at the slaughter (~100,000 killed) drives his conversion to Buddhism.",
     "start_year": -262, "end_year": -261,
     "wikipedia": "https://en.wikipedia.org/wiki/Kalinga_War",
     "priorities": ind(850_000), "region_weights": RW_INDIA,
     "first_zoom_out": "Maurya Empire"},

    {"type": "event", "title": "Gupta Empire founded",
     "description": "Chandragupta I founds the Gupta dynasty; ushers in classical India's golden age.",
     "start_year": 320,
     "wikipedia": "https://en.wikipedia.org/wiki/Gupta_Empire",
     "priorities": ind(900_000), "region_weights": RW_INDIA},

    {"type": "event", "title": "Aryabhata's mathematical work",
     "description": "Gupta-era astronomer-mathematician writes the Aryabhatiya; uses place-value decimal numerals and approximates π.",
     "start_year": 499,
     "wikipedia": "https://en.wikipedia.org/wiki/Aryabhata",
     "priorities": ind(890_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_INDIA,
     "first_zoom_out": "Gupta Empire founded"},

    {"type": "event", "title": "Decimal place-value system codified",
     "description": "Indian mathematicians develop the decimal positional system with zero; transmits via Arabic mathematicians to Europe centuries later.",
     "start_year": 458, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Indian_numerals",
     "priorities": ind(950_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_INDIA,
     "first_zoom_out": "Gupta Empire founded"},

    {"type": "event", "title": "Delhi Sultanate founded",
     "description": "Mamluk dynasty founded by Qutb al-Din Aibak; first major Muslim sultanate in India; rules northern India for over 300 years.",
     "start_year": 1206,
     "wikipedia": "https://en.wikipedia.org/wiki/Delhi_Sultanate",
     "priorities": ind(880_000), "region_weights": RW_INDIA},

    {"type": "event", "title": "Construction of Qutb Minar begun",
     "description": "Qutb al-Din Aibak begins the 73 m brick minaret in Delhi; tallest in the world for centuries; emblem of Indo-Islamic architecture.",
     "start_year": 1199,
     "wikipedia": "https://en.wikipedia.org/wiki/Qutb_Minar",
     "priorities": ind(850_000, **{"arts-and-thoughts": 860_000}),
     "region_weights": RW_INDIA,
     "first_zoom_out": "Delhi Sultanate founded"},

    {"type": "event", "title": "Mongol invasions of India",
     "description": "Repeated Mongol incursions into northwestern India; Delhi Sultanate withstands them; one of few states to do so.",
     "start_year": 1221, "end_year": 1327,
     "wikipedia": "https://en.wikipedia.org/wiki/Mongol_invasions_of_India",
     "priorities": ind(810_000), "region_weights": RW_INDIA,
     "first_zoom_out": "Delhi Sultanate founded"},

    {"type": "event", "title": "Vijayanagara Empire",
     "description": "Hindu South Indian empire centred on Vijayanagara (modern Hampi); resists Muslim expansion for over 200 years before falling at Talikota.",
     "start_year": 1336, "end_year": 1646,
     "wikipedia": "https://en.wikipedia.org/wiki/Vijayanagara_Empire",
     "priorities": ind(880_000), "region_weights": RW_INDIA},

    {"type": "event", "title": "Battle of Talikota",
     "description": "Deccan Sultanate alliance crushes Vijayanagara; city destroyed; effective end of major Hindu political power in southern India.",
     "start_year": 1565, "start_month": 1, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Talikota",
     "priorities": ind(840_000), "region_weights": RW_INDIA,
     "first_zoom_out": "Vijayanagara Empire"},

    {"type": "event", "title": "Babur founds Mughal Empire",
     "description": "Timurid prince Babur defeats Ibrahim Lodi at the First Battle of Panipat and founds the Mughal dynasty.",
     "start_year": 1526, "start_month": 4, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Babur",
     "priorities": ind(900_000), "region_weights": RW_INDIA,
     "first_zoom_out": "Mughal Empire"},

    {"type": "event", "title": "Reign of Akbar the Great",
     "description": "Third Mughal emperor; expands empire to most of the subcontinent; religious tolerance and Din-i Ilahi; centralised administration.",
     "start_year": 1556, "end_year": 1605,
     "wikipedia": "https://en.wikipedia.org/wiki/Akbar",
     "priorities": ind(920_000), "region_weights": RW_INDIA,
     "first_zoom_out": "Mughal Empire"},

    {"type": "event", "title": "Taj Mahal built",
     "description": "Mughal emperor Shah Jahan builds white-marble mausoleum at Agra for his wife Mumtaz Mahal; icon of Indo-Islamic architecture.",
     "start_year": 1632, "end_year": 1653,
     "wikipedia": "https://en.wikipedia.org/wiki/Taj_Mahal",
     "priorities": ind(970_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_INDIA,
     "first_zoom_out": "Mughal Empire"},

    {"type": "event", "title": "Reign of Aurangzeb",
     "description": "Last great Mughal; expands empire to its peak then fatally overextends; Hindu-Muslim tensions sharpen; empire begins to fragment after his death.",
     "start_year": 1658, "end_year": 1707,
     "wikipedia": "https://en.wikipedia.org/wiki/Aurangzeb",
     "priorities": ind(890_000), "region_weights": RW_INDIA,
     "first_zoom_out": "Mughal Empire"},

    {"type": "event", "title": "Maratha Empire rises",
     "description": "Shivaji founds the Maratha state and resists Mughal expansion; under his successors the Marathas come to dominate much of India.",
     "start_year": 1674, "end_year": 1818, "start_month": 6, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Maratha_Empire",
     "priorities": ind(880_000), "region_weights": RW_INDIA},

    {"type": "event", "title": "Battle of Buxar",
     "description": "East India Company defeats coalition of Mughal Shah Alam II, Mir Qasim and the Nawab of Awadh; opens India to British rule.",
     "start_year": 1764, "start_month": 10, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Buxar",
     "priorities": ind(870_000, **{"england": 850_000}), "region_weights": RW_INDIA},

    {"type": "event", "title": "Third Battle of Panipat",
     "description": "Afghan Durrani forces defeat the Maratha Empire's army; Maratha power crippled at the moment they might have replaced the Mughals.",
     "start_year": 1761, "start_month": 1, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Third_Battle_of_Panipat",
     "priorities": ind(850_000), "region_weights": RW_INDIA,
     "first_zoom_out": "Maratha Empire rises"},
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
