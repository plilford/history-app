"""
Phase E2 — Japan timeline. New slug 'japan'.

Sweep: prehistoric Jōmon → Yayoi → Yamato → Asuka/Nara → Heian → Kamakura
shogunate → Mongol invasions → Muromachi → Sengoku → Tokugawa → Bakumatsu
→ Meiji Restoration → Imperial Japan / WWII → Occupation → post-war
economic miracle → modern.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_JAPAN = {"europe": 2, "americas": 3, "asia": 10, "australasia": 3, "africa": 1}
RW_JAPAN_GLOBAL = {"europe": 4, "americas": 6, "asia": 10, "australasia": 5, "africa": 2}


def j(master_pri: int, jp_pri: int | None = None, **extra) -> dict:
    if jp_pri is None:
        jp_pri = min(999_000, master_pri + 30_000)
    out = {"master": master_pri, "japan": jp_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- Jōmon / Yayoi / Yamato -----
    {"type": "event", "title": "Jōmon period",
     "description": "Long Mesolithic-Neolithic culture of the Japanese archipelago; distinctive cord-marked pottery; one of the oldest pottery traditions in the world.",
     "start_year": -14000, "end_year": -300, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/J%C5%8Dmon_period",
     "priorities": j(820_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Yayoi period",
     "description": "Rice cultivation, bronze and iron metallurgy reach Japan from the continent; emergence of stratified society.",
     "start_year": -300, "end_year": 300, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Yayoi_period",
     "priorities": j(810_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Kofun period",
     "description": "Large keyhole-shaped tomb mounds (kofun) built by the early Yamato elite; first traceable Japanese state.",
     "start_year": 300, "end_year": 538, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Kofun_period",
     "priorities": j(800_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Buddhism arrives in Japan",
     "description": "Korean king of Baekje sends Buddhist scriptures and images to the Yamato court; transforms Japanese religion, art and politics.",
     "start_year": 538, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Buddhism_in_Japan",
     "priorities": j(900_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Asuka period",
     "description": "Early state formation under the Soga clan and Prince Shōtoku; first lasting capital at Asuka; Chinese-style government adopted.",
     "start_year": 538, "end_year": 710,
     "wikipedia": "https://en.wikipedia.org/wiki/Asuka_period",
     "priorities": j(830_000), "region_weights": RW_JAPAN},

    {"type": "person", "title": "Prince Shōtoku",
     "description": "Asuka-era regent and reformer; promoted Buddhism, sent the first official embassy to Sui China, drafted the Seventeen-Article Constitution.",
     "start_year": 574, "end_year": 622, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Prince_Sh%C5%8Dtoku",
     "priorities": j(850_000, people=860_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Seventeen-Article Constitution",
     "description": "Prince Shōtoku's moral code for officials; first codified statement of Japanese political philosophy.",
     "start_year": 604,
     "wikipedia": "https://en.wikipedia.org/wiki/Seventeen-article_constitution",
     "priorities": j(790_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Asuka period"},

    {"type": "event", "title": "Taika Reforms",
     "description": "Emperor Kōtoku's edicts centralise government on the Tang Chinese model; nationalise land; create a bureaucratic state.",
     "start_year": 645, "start_month": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Taika_Reform",
     "priorities": j(870_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Asuka period"},

    {"type": "event", "title": "Nara period",
     "description": "First permanent capital at Heijō-kyō (Nara); great Buddhist monuments built; Kojiki and Nihon Shoki chronicles compiled.",
     "start_year": 710, "end_year": 794,
     "wikipedia": "https://en.wikipedia.org/wiki/Nara_period",
     "priorities": j(870_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Tōdai-ji Great Buddha cast",
     "description": "Sixteen-metre bronze Vairocana Buddha at Tōdai-ji, Nara; biggest cast-bronze sculpture in the world.",
     "start_year": 752, "start_month": 4, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/T%C5%8Ddai-ji",
     "priorities": j(820_000, **{"arts-and-thoughts": 850_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Nara period"},

    {"type": "art", "title": "Kojiki compiled",
     "description": "Oldest surviving Japanese chronicle; mythological origins of the imperial line.",
     "start_year": 712,
     "wikipedia": "https://en.wikipedia.org/wiki/Kojiki",
     "priorities": j(820_000, **{"arts-and-thoughts": 850_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Nara period"},

    {"type": "art", "title": "Nihon Shoki compiled",
     "description": "Imperially commissioned chronicle in classical Chinese; complement to the Kojiki, more historical in tone.",
     "start_year": 720,
     "wikipedia": "https://en.wikipedia.org/wiki/Nihon_Shoki",
     "priorities": j(810_000, **{"arts-and-thoughts": 830_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Nara period"},

    # ----- Heian -----
    {"type": "event", "title": "Heian period",
     "description": "Capital moved to Heian-kyō (Kyoto); Fujiwara regents dominate; high classical court culture; weakening of central control.",
     "start_year": 794, "end_year": 1185,
     "wikipedia": "https://en.wikipedia.org/wiki/Heian_period",
     "priorities": j(890_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Fujiwara regency",
     "description": "Fujiwara clan dominates Heian government via marriage to imperial line; effective rulers for nearly two centuries.",
     "start_year": 858, "end_year": 1086,
     "wikipedia": "https://en.wikipedia.org/wiki/Fujiwara_clan",
     "priorities": j(830_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Heian period"},

    {"type": "person", "title": "Murasaki Shikibu",
     "description": "Heian court lady; author of The Tale of Genji, often called the world's first psychological novel.",
     "start_year": 973, "end_year": 1014, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Murasaki_Shikibu",
     "priorities": j(910_000, people=920_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_JAPAN_GLOBAL},

    {"type": "art", "title": "The Tale of Genji",
     "description": "Murasaki Shikibu's prose masterpiece of Heian court life; foundational text of Japanese and world literature.",
     "start_year": 1008, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Tale_of_Genji",
     "priorities": j(930_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "Heian period"},

    {"type": "art", "title": "The Pillow Book",
     "description": "Sei Shōnagon's collection of observations and lists from the Heian court; companion piece to Genji.",
     "start_year": 1002, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Pillow_Book",
     "priorities": j(860_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Heian period"},

    # ----- Kamakura / shogunate -----
    {"type": "event", "title": "Genpei War",
     "description": "Minamoto vs Taira clans contest control of Japan; Minamoto victory at Dan-no-ura founds the first shogunate.",
     "start_year": 1180, "end_year": 1185,
     "wikipedia": "https://en.wikipedia.org/wiki/Genpei_War",
     "priorities": j(880_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Battle of Dan-no-ura",
     "description": "Final naval battle of the Genpei War; child Emperor Antoku drowns; Minamoto Yoritomo becomes effective ruler.",
     "start_year": 1185, "start_month": 4, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Dan-no-ura",
     "priorities": j(840_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Genpei War"},

    {"type": "event", "title": "Kamakura shogunate",
     "description": "Japan's first samurai government; founded by Minamoto Yoritomo; ruled in parallel with the powerless Kyoto imperial court.",
     "start_year": 1185, "end_year": 1333,
     "wikipedia": "https://en.wikipedia.org/wiki/Kamakura_shogunate",
     "priorities": j(910_000), "region_weights": RW_JAPAN},

    {"type": "person", "title": "Minamoto no Yoritomo",
     "description": "First shōgun; founder of the Kamakura government; ruthless consolidator who eliminated rivals including his half-brother Yoshitsune.",
     "start_year": 1147, "end_year": 1199, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Minamoto_no_Yoritomo",
     "priorities": j(870_000, people=880_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "First Mongol invasion of Japan",
     "description": "Kublai Khan's army lands at Hakata Bay; typhoon (kamikaze) destroys the fleet after inconclusive fighting.",
     "start_year": 1274, "start_month": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Mongol_invasions_of_Japan",
     "priorities": j(880_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Second Mongol invasion of Japan",
     "description": "Vastly larger fleet of ~140,000 Mongol-Korean troops; defeated by reinforced defences plus a second 'divine wind' typhoon.",
     "start_year": 1281, "start_month": 7, "end_month": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Mongol_invasions_of_Japan",
     "priorities": j(890_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Kemmu Restoration",
     "description": "Emperor Go-Daigo briefly restores direct imperial rule after the Kamakura shogunate falls; lasts only three years.",
     "start_year": 1333, "end_year": 1336,
     "wikipedia": "https://en.wikipedia.org/wiki/Kenmu_Restoration",
     "priorities": j(800_000), "region_weights": RW_JAPAN},

    # ----- Muromachi / Sengoku -----
    {"type": "event", "title": "Muromachi shogunate (Ashikaga)",
     "description": "Ashikaga Takauji founds new shogunate based in Kyoto's Muromachi district; cultural flowering despite political weakness.",
     "start_year": 1336, "end_year": 1573,
     "wikipedia": "https://en.wikipedia.org/wiki/Muromachi_period",
     "priorities": j(880_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Northern and Southern Courts",
     "description": "Rival imperial lines based in Kyoto (Ashikaga-backed) and Yoshino split Japan for 56 years before reunification in 1392.",
     "start_year": 1336, "end_year": 1392,
     "wikipedia": "https://en.wikipedia.org/wiki/Nanboku-ch%C5%8D_period",
     "priorities": j(800_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Muromachi shogunate (Ashikaga)"},

    {"type": "event", "title": "Kinkaku-ji built",
     "description": "Golden Pavilion temple in Kyoto built by retired shōgun Ashikaga Yoshimitsu; iconic example of Muromachi architecture.",
     "start_year": 1397,
     "wikipedia": "https://en.wikipedia.org/wiki/Kinkaku-ji",
     "priorities": j(840_000, **{"arts-and-thoughts": 860_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Muromachi shogunate (Ashikaga)"},

    {"type": "event", "title": "Ōnin War",
     "description": "Succession dispute among Ashikaga retainers devastates Kyoto and opens the Sengoku ('warring states') century.",
     "start_year": 1467, "end_year": 1477,
     "wikipedia": "https://en.wikipedia.org/wiki/%C5%8Cnin_War",
     "priorities": j(880_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Sengoku period",
     "description": "Century of feuding daimyō; warfare transforms Japan socially and militarily; ends with reunification under Oda-Toyotomi-Tokugawa.",
     "start_year": 1467, "end_year": 1603,
     "wikipedia": "https://en.wikipedia.org/wiki/Sengoku_period",
     "priorities": j(930_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Arrival of Portuguese traders",
     "description": "Portuguese ship blown off course lands at Tanegashima; introduces firearms and revolutionises Sengoku warfare.",
     "start_year": 1543,
     "wikipedia": "https://en.wikipedia.org/wiki/Nanban_trade",
     "priorities": j(870_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "Sengoku period"},

    {"type": "event", "title": "Francis Xavier's mission to Japan",
     "description": "Jesuit Francis Xavier arrives in Kagoshima; opens Japan to Catholic missionary activity for nearly a century.",
     "start_year": 1549, "start_month": 8, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Francis_Xavier",
     "priorities": j(830_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "Sengoku period"},

    {"type": "person", "title": "Oda Nobunaga",
     "description": "First of three great unifiers; brutal innovator who broke clerical and clan power before assassination at Honnō-ji.",
     "start_year": 1534, "end_year": 1582, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Oda_Nobunaga",
     "priorities": j(920_000, people=930_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Battle of Okehazama",
     "description": "Young Oda Nobunaga ambushes and kills Imagawa Yoshimoto in pouring rain; launches him onto the national stage.",
     "start_year": 1560, "start_month": 6, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Okehazama",
     "priorities": j(810_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Sengoku period"},

    {"type": "event", "title": "Battle of Nagashino",
     "description": "Oda Nobunaga and Tokugawa Ieyasu use disciplined volleys of matchlock fire to crush the Takeda cavalry; firearms warfare comes of age in Japan.",
     "start_year": 1575, "start_month": 6, "start_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Nagashino",
     "priorities": j(840_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Sengoku period"},

    {"type": "event", "title": "Honnō-ji Incident",
     "description": "Oda Nobunaga betrayed by Akechi Mitsuhide and forced to commit seppuku at Honnō-ji temple; Hideyoshi avenges him 11 days later.",
     "start_year": 1582, "start_month": 6, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Incident_at_Honn%C5%8D-ji",
     "priorities": j(860_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Sengoku period"},

    {"type": "person", "title": "Toyotomi Hideyoshi",
     "description": "Second great unifier; peasant-born regent who completed reunification of Japan; banned weapons among the peasantry; failed Korea invasions.",
     "start_year": 1537, "end_year": 1598, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Toyotomi_Hideyoshi",
     "priorities": j(910_000, people=920_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Hideyoshi's sword hunt",
     "description": "Hideyoshi confiscates weapons from peasants and monks; reinforces the rigid samurai-commoner class divide that defines Tokugawa Japan.",
     "start_year": 1588, "start_month": 8, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Sword_hunt",
     "priorities": j(820_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Japanese invasions of Korea (Imjin War)",
     "description": "Hideyoshi's two invasions; defeated by Korean naval hero Yi Sun-sin and Ming Chinese reinforcements; massive devastation in Korea.",
     "start_year": 1592, "end_year": 1598,
     "wikipedia": "https://en.wikipedia.org/wiki/Japanese_invasions_of_Korea_(1592%E2%80%931598)",
     "priorities": j(870_000), "region_weights": RW_JAPAN_GLOBAL},

    # ----- Tokugawa / Edo -----
    {"type": "event", "title": "Battle of Sekigahara",
     "description": "Tokugawa Ieyasu defeats western daimyō coalition in a single day; clears his path to the shogunate.",
     "start_year": 1600, "start_month": 10, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Sekigahara",
     "priorities": j(910_000), "region_weights": RW_JAPAN},

    {"type": "person", "title": "Tokugawa Ieyasu",
     "description": "Third great unifier; founded the Tokugawa shogunate; established the institutional framework that endured for 250 years.",
     "start_year": 1543, "end_year": 1616, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tokugawa_Ieyasu",
     "priorities": j(920_000, people=920_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Tokugawa shogunate (Edo period)",
     "description": "Centralised feudal regime ruled from Edo (Tokyo); peace, urban culture, sakoku isolation; ends with the Meiji Restoration.",
     "start_year": 1603, "end_year": 1868,
     "wikipedia": "https://en.wikipedia.org/wiki/Edo_period",
     "priorities": j(940_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Siege of Osaka",
     "description": "Tokugawa Ieyasu destroys the Toyotomi heirs and their stronghold at Osaka Castle; consolidates the shogunate.",
     "start_year": 1614, "end_year": 1615,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Osaka",
     "priorities": j(810_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Tokugawa shogunate (Edo period)"},

    {"type": "event", "title": "Shimabara Rebellion",
     "description": "Christian and peasant uprising on Kyushu crushed by Tokugawa forces; triggers near-total ban on Christianity and isolation policy.",
     "start_year": 1637, "end_year": 1638,
     "wikipedia": "https://en.wikipedia.org/wiki/Shimabara_Rebellion",
     "priorities": j(820_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Tokugawa shogunate (Edo period)"},

    {"type": "event", "title": "Sakoku (closed country policy)",
     "description": "Series of edicts restricts foreign trade and travel; Japan effectively sealed off except for limited Dutch/Chinese contact via Nagasaki.",
     "start_year": 1639, "end_year": 1853,
     "wikipedia": "https://en.wikipedia.org/wiki/Sakoku",
     "priorities": j(900_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Genroku era",
     "description": "Cultural high point of Tokugawa Japan: kabuki, haiku, ukiyo-e woodblock prints, samurai-class literature.",
     "start_year": 1688, "end_year": 1704,
     "wikipedia": "https://en.wikipedia.org/wiki/Genroku",
     "priorities": j(820_000, **{"arts-and-thoughts": 860_000}),
     "region_weights": RW_JAPAN,
     "first_zoom_out": "Tokugawa shogunate (Edo period)"},

    {"type": "person", "title": "Matsuo Bashō",
     "description": "Greatest Japanese haiku poet; The Narrow Road to the Deep North set the standard for Edo-period travel writing.",
     "start_year": 1644, "end_year": 1694, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Matsuo_Bash%C5%8D",
     "priorities": j(870_000, people=890_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_JAPAN},

    {"type": "event", "title": "Forty-seven Rōnin",
     "description": "Masterless samurai avenge their lord's enforced suicide, then ritually kill themselves; iconic tale of Tokugawa-era honour.",
     "start_year": 1703, "start_month": 1, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Forty-seven_r%C5%8Dnin",
     "priorities": j(830_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Tokugawa shogunate (Edo period)"},

    {"type": "person", "title": "Katsushika Hokusai",
     "description": "Edo-period printmaker; The Great Wave off Kanagawa and other ukiyo-e works influenced European impressionism.",
     "start_year": 1760, "end_year": 1849, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hokusai",
     "priorities": j(900_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_JAPAN_GLOBAL},

    {"type": "art", "title": "The Great Wave off Kanagawa",
     "description": "Hokusai's iconic ukiyo-e print, c. 1831, from the series Thirty-six Views of Mount Fuji.",
     "start_year": 1831, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Great_Wave_off_Kanagawa",
     "priorities": j(940_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "Tokugawa shogunate (Edo period)"},

    # ----- Bakumatsu / Meiji -----
    {"type": "event", "title": "Perry's black ships arrive",
     "description": "US Commodore Matthew Perry arrives in Edo Bay with steam warships; demands Japan open to trade. End of sakoku.",
     "start_year": 1853, "start_month": 7, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Perry_Expedition",
     "priorities": j(930_000, usa=870_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Treaty of Kanagawa",
     "description": "Japan signs first unequal treaty with the US, opening two ports to American ships; other Western powers quickly follow.",
     "start_year": 1854, "start_month": 3, "start_day": 31,
     "wikipedia": "https://en.wikipedia.org/wiki/Convention_of_Kanagawa",
     "priorities": j(870_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Bakumatsu",
     "description": "Final decade of Tokugawa rule; civil war between shogunate loyalists and pro-emperor southern domains; ends with Meiji Restoration.",
     "start_year": 1853, "end_year": 1868,
     "wikipedia": "https://en.wikipedia.org/wiki/Bakumatsu",
     "priorities": j(870_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Boshin War",
     "description": "Civil war between Tokugawa forces and pro-imperial Satsuma-Chōshū alliance; imperial victory enables the Meiji Restoration.",
     "start_year": 1868, "start_month": 1, "start_day": 27, "end_year": 1869, "end_month": 6, "end_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Boshin_War",
     "priorities": j(850_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Bakumatsu"},

    {"type": "event", "title": "Meiji Restoration",
     "description": "Emperor Meiji restored to political authority; abolition of the shogunate; programme of accelerated modernisation begins.",
     "start_year": 1868, "start_month": 1, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Meiji_Restoration",
     "priorities": j(950_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Meiji era",
     "description": "Reign of Emperor Meiji; Japan transforms from feudal society to industrial great power in 45 years.",
     "start_year": 1868, "end_year": 1912,
     "wikipedia": "https://en.wikipedia.org/wiki/Meiji_era",
     "priorities": j(920_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Abolition of the han system",
     "description": "Meiji government replaces feudal domains with centrally administered prefectures; transforms Japanese government overnight.",
     "start_year": 1871, "start_month": 8, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Abolition_of_the_han_system",
     "priorities": j(830_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Meiji era"},

    {"type": "event", "title": "Satsuma Rebellion",
     "description": "Last samurai uprising under Saigō Takamori, crushed by the new conscript imperial army; cements modernisation.",
     "start_year": 1877, "start_month": 1, "start_day": 29, "end_month": 9, "end_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Satsuma_Rebellion",
     "priorities": j(850_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Meiji era"},

    {"type": "event", "title": "Meiji Constitution",
     "description": "First Japanese constitution; modeled on Prussian model; emperor formally supreme, with a Diet and partial cabinet government.",
     "start_year": 1889, "start_month": 2, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Meiji_Constitution",
     "priorities": j(870_000), "region_weights": RW_JAPAN,
     "first_zoom_out": "Meiji era"},

    {"type": "event", "title": "First Sino-Japanese War",
     "description": "Japan defeats Qing China over influence in Korea; Treaty of Shimonoseki cedes Taiwan; signals Japan's emergence as a great power.",
     "start_year": 1894, "end_year": 1895,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Sino-Japanese_War",
     "priorities": j(900_000, china=860_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "Meiji era"},

    {"type": "event", "title": "Russo-Japanese War",
     "description": "Japan defeats Imperial Russia on land and sea; first major Asian victory over a European power in modern times; reshapes geopolitics.",
     "start_year": 1904, "end_year": 1905,
     "wikipedia": "https://en.wikipedia.org/wiki/Russo-Japanese_War",
     "priorities": j(930_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Battle of Tsushima",
     "description": "Admiral Tōgō annihilates the Russian Baltic Fleet in the Tsushima Strait; one of history's most one-sided naval victories.",
     "start_year": 1905, "start_month": 5, "start_day": 27, "end_month": 5, "end_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Tsushima",
     "priorities": j(880_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "Russo-Japanese War"},

    {"type": "event", "title": "Annexation of Korea",
     "description": "Japan formally annexes Korea after years of de-facto control; colonial rule lasts until 1945.",
     "start_year": 1910, "start_month": 8, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Japan%E2%80%93Korea_Treaty_of_1910",
     "priorities": j(880_000), "region_weights": RW_JAPAN_GLOBAL},

    # ----- Imperial / WWII -----
    {"type": "event", "title": "Taishō democracy",
     "description": "Period of liberal politics, party cabinets, and universal male suffrage; ends with military ascendancy in the early Shōwa era.",
     "start_year": 1912, "end_year": 1926,
     "wikipedia": "https://en.wikipedia.org/wiki/Taish%C5%8D_era",
     "priorities": j(810_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Great Kantō earthquake",
     "description": "Magnitude 7.9 quake devastates Tokyo and Yokohama; ~140,000 killed; mass-violence pogrom against ethnic Koreans follows.",
     "start_year": 1923, "start_month": 9, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/1923_Great_Kant%C5%8D_earthquake",
     "priorities": j(890_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Mukden Incident",
     "description": "Japanese Kwantung Army stages explosion on the South Manchuria Railway as pretext for full invasion of Manchuria.",
     "start_year": 1931, "start_month": 9, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Mukden_Incident",
     "priorities": j(870_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Manchukuo founded",
     "description": "Japan installs Puyi, last Qing emperor, as figurehead ruler of puppet state of Manchukuo; League of Nations condemns; Japan withdraws.",
     "start_year": 1932, "start_month": 3, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Manchukuo",
     "priorities": j(840_000, china=850_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Second Sino-Japanese War",
     "description": "Full-scale war between Japan and China; 1937 Marco Polo Bridge incident triggers eight years of devastation; merges into WWII.",
     "start_year": 1937, "end_year": 1945,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Sino-Japanese_War",
     "priorities": j(920_000, china=920_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Nanking Massacre",
     "description": "Japanese forces commit mass killings, rape and looting in Nationalist Chinese capital; up to 300,000 killed in six weeks.",
     "start_year": 1937, "start_month": 12, "start_day": 13, "end_year": 1938, "end_month": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Nanjing_Massacre",
     "priorities": j(900_000, china=900_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "Second Sino-Japanese War"},

    {"type": "event", "title": "Attack on Pearl Harbor",
     "description": "Japanese carrier strike on the US Pacific Fleet at Pearl Harbor brings America into WWII.",
     "start_year": 1941, "start_month": 12, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Attack_on_Pearl_Harbor",
     "priorities": j(960_000, usa=960_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Battle of Midway",
     "description": "US Navy sinks four Japanese aircraft carriers; decisive turning point in the Pacific War.",
     "start_year": 1942, "start_month": 6, "start_day": 4, "end_month": 6, "end_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Midway",
     "priorities": j(930_000, usa=920_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Battle of Iwo Jima",
     "description": "US Marines take volcanic Pacific island after a month of brutal combat; iconic flag-raising on Mount Suribachi.",
     "start_year": 1945, "start_month": 2, "start_day": 19, "end_month": 3, "end_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Iwo_Jima",
     "priorities": j(890_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Battle of Okinawa",
     "description": "Last major Pacific battle; ~200,000 killed including ~100,000 civilians; foreshadows expected cost of invading the Home Islands.",
     "start_year": 1945, "start_month": 4, "start_day": 1, "end_month": 6, "end_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Okinawa",
     "priorities": j(890_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Atomic bombing of Hiroshima",
     "description": "US B-29 Enola Gay drops first nuclear weapon used in war; ~140,000 dead by year's end.",
     "start_year": 1945, "start_month": 8, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Atomic_bombings_of_Hiroshima_and_Nagasaki",
     "priorities": j(970_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Atomic bombing of Nagasaki",
     "description": "Second nuclear weapon used in war; ~70,000 dead by year's end; Japan accepts unconditional surrender within days.",
     "start_year": 1945, "start_month": 8, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Atomic_bombings_of_Hiroshima_and_Nagasaki",
     "priorities": j(960_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "World War II"},

    {"type": "event", "title": "Japanese surrender (V-J Day)",
     "description": "Emperor Hirohito's recorded broadcast announces surrender; formal signing on USS Missouri 2 September 1945.",
     "start_year": 1945, "start_month": 8, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Surrender_of_Japan",
     "priorities": j(950_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "World War II"},

    # ----- Postwar -----
    {"type": "event", "title": "Allied occupation of Japan",
     "description": "Douglas MacArthur as SCAP oversees demilitarisation, land reform, and a new constitution; lasts 1945-1952.",
     "start_year": 1945, "end_year": 1952,
     "wikipedia": "https://en.wikipedia.org/wiki/Occupation_of_Japan",
     "priorities": j(900_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Constitution of Japan",
     "description": "American-drafted post-war constitution; Article 9 renounces war; emperor reduced to symbolic role.",
     "start_year": 1947, "start_month": 5, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Constitution_of_Japan",
     "priorities": j(900_000), "region_weights": RW_JAPAN_GLOBAL,
     "first_zoom_out": "Allied occupation of Japan"},

    {"type": "event", "title": "San Francisco Peace Treaty",
     "description": "Formal end of state of war between Japan and 48 Allied nations; restores Japanese sovereignty.",
     "start_year": 1951, "start_month": 9, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_San_Francisco",
     "priorities": j(880_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Japanese economic miracle",
     "description": "Three decades of ~10% GDP growth turn Japan into the world's second-largest economy by 1968; export-led industrial transformation.",
     "start_year": 1955, "end_year": 1991,
     "wikipedia": "https://en.wikipedia.org/wiki/Japanese_economic_miracle",
     "priorities": j(920_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Tokyo 1964 Olympics",
     "description": "First Olympics held in Asia; showcase of post-war recovery; introduces the Shinkansen bullet train.",
     "start_year": 1964, "start_month": 10, "start_day": 10, "end_month": 10, "end_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/1964_Summer_Olympics",
     "priorities": j(880_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Shinkansen bullet train",
     "description": "First high-speed rail line, Tokyo to Osaka, opens ahead of 1964 Olympics; spawns a global industry.",
     "start_year": 1964, "start_month": 10, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Shinkansen",
     "priorities": j(890_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Reversion of Okinawa",
     "description": "US returns Okinawa to Japan after 27 years of military rule; American bases remain.",
     "start_year": 1972, "start_month": 5, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Reversion_of_Okinawa",
     "priorities": j(820_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Japanese asset price bubble",
     "description": "Late 1980s real-estate and stock bubble peaks then collapses, triggering Japan's 'Lost Decades' of stagnant growth.",
     "start_year": 1986, "end_year": 1991,
     "wikipedia": "https://en.wikipedia.org/wiki/Japanese_asset_price_bubble",
     "priorities": j(880_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Lost Decades (Japan)",
     "description": "Three decades of low growth, near-zero interest rates, and deflation following the asset bubble collapse.",
     "start_year": 1991, "end_year": 2020, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Lost_Decades",
     "priorities": j(870_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Great Hanshin earthquake",
     "description": "Magnitude 6.9 quake hits Kobe; ~6,400 killed; exposes weaknesses in Japanese disaster response.",
     "start_year": 1995, "start_month": 1, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Great_Hansh%C3%ABn_earthquake",
     "priorities": j(840_000), "region_weights": RW_JAPAN},

    {"type": "event", "title": "Tokyo subway sarin attack",
     "description": "Aum Shinrikyo cult releases sarin nerve gas on five subway lines during rush hour; 14 killed, ~1,000 injured.",
     "start_year": 1995, "start_month": 3, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Tokyo_subway_sarin_attack",
     "priorities": j(860_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Tōhoku earthquake and Fukushima disaster",
     "description": "Magnitude 9.0 earthquake and tsunami devastate northeast Japan; meltdowns at Fukushima Daiichi reshape global nuclear policy.",
     "start_year": 2011, "start_month": 3, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/2011_T%C5%8Dhoku_earthquake_and_tsunami",
     "priorities": j(930_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Abenomics",
     "description": "Shinzō Abe's three-arrow economic programme — monetary easing, fiscal stimulus, structural reform — to break decades of stagnation.",
     "start_year": 2012, "end_year": 2020,
     "wikipedia": "https://en.wikipedia.org/wiki/Abenomics",
     "priorities": j(840_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Tokyo 2020 Olympics",
     "description": "Pandemic-delayed games held in 2021 with no spectators; bittersweet contrast to 1964.",
     "start_year": 2021, "start_month": 7, "start_day": 23, "end_month": 8, "end_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/2020_Summer_Olympics",
     "priorities": j(830_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "event", "title": "Assassination of Shinzō Abe",
     "description": "Former prime minister Abe shot dead while campaigning in Nara; ends an era of Japanese political stability.",
     "start_year": 2022, "start_month": 7, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Assassination_of_Shinzo_Abe",
     "priorities": j(870_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "person", "title": "Hirohito (Emperor Shōwa)",
     "description": "Reigned 1926-1989, longest of any Japanese emperor; presided over imperial expansion, WWII defeat, post-war recovery.",
     "start_year": 1901, "end_year": 1989, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hirohito",
     "priorities": j(910_000, people=920_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "person", "title": "Emperor Meiji",
     "description": "Symbol of and overseer of Japan's modernisation; reigned 1867-1912.",
     "start_year": 1852, "end_year": 1912, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Emperor_Meiji",
     "priorities": j(890_000, people=900_000), "region_weights": RW_JAPAN_GLOBAL},

    {"type": "person", "title": "Yukio Mishima",
     "description": "Novelist, playwright and right-wing nationalist; ritual suicide at a JSDF base in 1970 shocked Japan.",
     "start_year": 1925, "end_year": 1970, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Yukio_Mishima",
     "priorities": j(860_000, people=880_000, **{"arts-and-thoughts": 890_000}),
     "region_weights": RW_JAPAN},

    {"type": "person", "title": "Akira Kurosawa",
     "description": "Most internationally influential Japanese film director; Rashomon, Seven Samurai, Yojimbo, Ran.",
     "start_year": 1910, "end_year": 1998, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Akira_Kurosawa",
     "priorities": j(910_000, people=920_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_JAPAN_GLOBAL},

    {"type": "person", "title": "Hayao Miyazaki",
     "description": "Co-founder of Studio Ghibli; Spirited Away, Princess Mononoke, My Neighbor Totoro; defining animator of his generation.",
     "start_year": 1941, "is_full_life": False, "is_ongoing": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hayao_Miyazaki",
     "priorities": j(900_000, people=910_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_JAPAN_GLOBAL},
]


def main() -> int:
    base = next_available_id()
    for i, en in enumerate(ENTRIES):
        en["id"] = base + i
    n = append_entries(ENTRIES)
    print(f"Appended {n} Japan entries (IDs {base}..{base+n-1}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
