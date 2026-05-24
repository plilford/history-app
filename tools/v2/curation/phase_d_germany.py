"""
Phase D — Germany. From Germanic tribes through modern reunification.

Priority calibration (full 0-1M range):
  990k+: civilizational hinges (Luther's 95 Theses, fall of Berlin Wall)
  950k+: major events most know (Treaty of Westphalia, founding of Reich,
          Hitler chancellor, German reunification)
  900k+: significant turning points (Diet of Worms, Battle of Sedan, V-E Day)
  850k+: important but specific (Frederick the Great accession, Bismarck's reforms)
  750k+: notable medium-tier (specific battles, treaties, chancellors)
  600-750: minor regional
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_GERMANY = {"europe": 10, "americas": 3, "asia": 2, "australasia": 1, "africa": 2}
RW_GERMANY_GLOBAL = {"europe": 10, "americas": 6, "asia": 5, "australasia": 4, "africa": 4}


def g(master_pri: int, ger_pri: int | None = None, **extra) -> dict:
    if ger_pri is None:
        ger_pri = min(999_000, master_pri + 30_000)
    out = {"master": master_pri, "germany": ger_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- Germanic tribes & Frankish kingdom -----
    {"type": "event", "title": "Germanic tribes east of the Rhine",
     "description": "Tribal confederations (Cherusci, Suebi, Franks, Alemanni, Saxons) inhabit the lands between Rhine and Elbe through antiquity.",
     "start_year": -200, "end_year": 500, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ancient_Germanic_peoples",
     "priorities": g(800_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Frankish kingdom of Clovis I",
     "description": "Clovis I unites the Franks, converts to Catholic Christianity, founds the Merovingian dynasty.",
     "start_year": 481, "end_year": 511,
     "wikipedia": "https://en.wikipedia.org/wiki/Clovis_I",
     "priorities": g(880_000, **{"france": 880_000}), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Battle of Tours",
     "description": "Charles Martel halts the Umayyad advance into Frankish lands; Carolingian power rises on the back of victory.",
     "start_year": 732, "start_month": 10, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Tours",
     "priorities": g(900_000, **{"france": 870_000}), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Carolingian Renaissance",
     "description": "Cultural and intellectual revival under Charlemagne and his successors; Carolingian minuscule script, monastic learning.",
     "start_year": 780, "end_year": 900, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Carolingian_Renaissance",
     "priorities": g(860_000, **{"arts-and-thoughts": 860_000}), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Treaty of Verdun",
     "description": "Charlemagne's grandsons divide the Carolingian Empire into West Francia (France), East Francia (Germany), and Middle Francia.",
     "start_year": 843, "start_month": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Verdun",
     "priorities": g(910_000, **{"france": 870_000}), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Otto I crowned Holy Roman Emperor",
     "description": "East Frankish king Otto I crowned by Pope John XII; revives the imperial title and founds the Holy Roman Empire (Ottonian dynasty).",
     "start_year": 962, "start_month": 2, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Otto_I,_Holy_Roman_Emperor",
     "priorities": g(910_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Battle of Lechfeld",
     "description": "Otto I crushes Magyar invaders near Augsburg; ends nomadic raids on Germany and consolidates Ottonian power.",
     "start_year": 955, "start_month": 8, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Lechfeld",
     "priorities": g(810_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Holy Roman Empire",
     "description": "Loose German-centred polity claiming Roman lineage; the 'First Reich' until Napoleon dissolved it in 1806.",
     "start_year": 962, "end_year": 1806,
     "wikipedia": "https://en.wikipedia.org/wiki/Holy_Roman_Empire",
     "priorities": g(950_000), "region_weights": RW_GERMANY},

    # ----- Salian / Hohenstaufen era -----
    {"type": "event", "title": "Walk to Canossa",
     "description": "Emperor Henry IV stands barefoot in the snow at Canossa to beg Pope Gregory VII's absolution; emblem of the Investiture struggle.",
     "start_year": 1077, "start_month": 1, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Road_to_Canossa",
     "priorities": g(870_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Concordat of Worms",
     "description": "Compromise between Pope Calixtus II and Emperor Henry V ends the Investiture Controversy; spiritual investiture remains the pope's.",
     "start_year": 1122, "start_month": 9, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Concordat_of_Worms",
     "priorities": g(810_000), "region_weights": RW_GERMANY},

    {"type": "person", "title": "Frederick I Barbarossa",
     "description": "Hohenstaufen emperor; campaigns in Italy against Lombard League; drowns en route to the Third Crusade.",
     "start_year": 1122, "end_year": 1190, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Frederick_I,_Holy_Roman_Emperor",
     "priorities": g(880_000, people=890_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Hanseatic League founded",
     "description": "Confederation of Baltic and North Sea trading towns led by Lübeck; dominates northern European commerce for centuries.",
     "start_year": 1356, "date_uncertain": True,
     "display_date": "formalised 1356; trading league active since ~1200",
     "wikipedia": "https://en.wikipedia.org/wiki/Hanseatic_League",
     "priorities": g(870_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Cologne Cathedral begun",
     "description": "Construction of Cologne Cathedral begins in Gothic style; halted in the 16th century, finally completed in 1880.",
     "start_year": 1248, "start_month": 8, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Cologne_Cathedral",
     "priorities": g(810_000, **{"arts-and-thoughts": 820_000}), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Golden Bull of 1356",
     "description": "Charles IV's imperial constitution; fixes the seven electors who choose the Holy Roman Emperor.",
     "start_year": 1356, "start_month": 1, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Golden_Bull_of_1356",
     "priorities": g(830_000), "region_weights": RW_GERMANY},

    # ----- Reformation & 16th century -----
    {"type": "event", "title": "Gutenberg prints the 42-line Bible",
     "description": "Johannes Gutenberg in Mainz produces the first major book printed with movable metal type; transforms European literacy.",
     "start_year": 1455, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Gutenberg_Bible",
     "priorities": g(960_000, **{"renaissance": 960_000, "arts-and-thoughts": 960_000}),
     "region_weights": RW_GERMANY_GLOBAL},

    {"type": "person", "title": "Albrecht Dürer",
     "description": "Nuremberg painter and printmaker; defining figure of the Northern Renaissance; self-portraits, Melencolia I, Knight, Death and the Devil.",
     "start_year": 1471, "end_year": 1528, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Albrecht_D%C3%BCrer",
     "priorities": g(900_000, people=910_000, **{"arts-and-thoughts": 920_000, "renaissance": 920_000}),
     "region_weights": RW_GERMANY},

    {"type": "person", "title": "Martin Luther",
     "description": "Augustinian friar whose 95 Theses launched the Protestant Reformation; translated the Bible into German.",
     "start_year": 1483, "end_year": 1546, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Martin_Luther",
     "priorities": g(970_000, people=980_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Luther's 95 Theses",
     "description": "Augustinian friar Luther posts (or sends) his 95 critiques of indulgences at Wittenberg; conventional start of the Reformation.",
     "start_year": 1517, "start_month": 10, "start_day": 31,
     "wikipedia": "https://en.wikipedia.org/wiki/Ninety-five_Theses",
     "priorities": g(985_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Diet of Worms",
     "description": "Imperial Diet at Worms summons Luther; he refuses to recant ('Here I stand'); Emperor Charles V bans his works.",
     "start_year": 1521, "start_month": 1, "start_day": 28, "end_month": 5, "end_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Diet_of_Worms",
     "priorities": g(920_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "German Peasants' War",
     "description": "Largest popular uprising in Europe before the French Revolution; up to 100,000 peasants killed; Luther condemns the rebels.",
     "start_year": 1524, "end_year": 1525,
     "wikipedia": "https://en.wikipedia.org/wiki/German_Peasants%27_War",
     "priorities": g(870_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Luther's German Bible",
     "description": "Luther's New Testament (1522) and complete Bible (1534) translation; defines modern High German prose.",
     "start_year": 1534, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Luther_Bible",
     "priorities": g(920_000, **{"arts-and-thoughts": 920_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Schmalkaldic War",
     "description": "Catholic emperor Charles V crushes the Schmalkaldic League of Protestant princes at Mühlberg, but cannot reverse the Reformation.",
     "start_year": 1546, "end_year": 1547,
     "wikipedia": "https://en.wikipedia.org/wiki/Schmalkaldic_War",
     "priorities": g(800_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Peace of Augsburg",
     "description": "Imperial settlement permits each prince to choose between Catholicism and Lutheranism (cuius regio, eius religio).",
     "start_year": 1555, "start_month": 9, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Peace_of_Augsburg",
     "priorities": g(900_000), "region_weights": RW_GERMANY},

    # ----- Thirty Years' War -----
    {"type": "event", "title": "Defenestration of Prague",
     "description": "Protestant nobles throw two Catholic regents out of a Hradčany window; conventional start of the Thirty Years' War.",
     "start_year": 1618, "start_month": 5, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Defenestrations_of_Prague",
     "priorities": g(890_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Thirty Years' War",
     "description": "Devastating religious-dynastic war across the Holy Roman Empire; perhaps 8 million dead; ends with Peace of Westphalia.",
     "start_year": 1618, "end_year": 1648,
     "wikipedia": "https://en.wikipedia.org/wiki/Thirty_Years%27_War",
     "priorities": g(960_000, **{"france": 870_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Battle of White Mountain",
     "description": "Imperial-Catholic forces crush Bohemian Protestant nobility outside Prague; recatholicises Bohemia and ends Czech autonomy.",
     "start_year": 1620, "start_month": 11, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_White_Mountain",
     "priorities": g(820_000), "region_weights": RW_GERMANY},

    {"type": "person", "title": "Albrecht von Wallenstein",
     "description": "Bohemian-born imperial generalissimo of the Thirty Years' War; built his own army and was assassinated on imperial orders.",
     "start_year": 1583, "end_year": 1634, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Albrecht_von_Wallenstein",
     "priorities": g(830_000, people=860_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Sack of Magdeburg",
     "description": "Catholic Imperial army sacks Magdeburg; up to 20,000 civilians killed and the city burned to the ground.",
     "start_year": 1631, "start_month": 5, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Sack_of_Magdeburg",
     "priorities": g(820_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Battle of Breitenfeld",
     "description": "Gustavus Adolphus of Sweden crushes Tilly's imperial army; saves Protestant cause in Germany.",
     "start_year": 1631, "start_month": 9, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Breitenfeld_(1631)",
     "priorities": g(810_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Battle of Lützen (1632)",
     "description": "Swedish Protestants defeat imperial-Catholic Wallenstein; King Gustavus Adolphus killed in the fight.",
     "start_year": 1632, "start_month": 11, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_L%C3%BCtzen_(1632)",
     "priorities": g(820_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Peace of Westphalia",
     "description": "Treaties of Münster and Osnabrück end the Thirty Years' War; foundational moment for the modern state system.",
     "start_year": 1648, "start_month": 10, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Peace_of_Westphalia",
     "priorities": g(960_000), "region_weights": RW_GERMANY_GLOBAL},

    # ----- Rise of Brandenburg-Prussia -----
    {"type": "event", "title": "Great Elector of Brandenburg",
     "description": "Frederick William rebuilds Brandenburg-Prussia after the Thirty Years' War; standing army and tolerance for Huguenot refugees.",
     "start_year": 1640, "end_year": 1688,
     "wikipedia": "https://en.wikipedia.org/wiki/Frederick_William,_Elector_of_Brandenburg",
     "priorities": g(820_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Kingdom of Prussia proclaimed",
     "description": "Elector Frederick III crowns himself King in Prussia at Königsberg; rise of Brandenburg-Prussia as a kingdom begins.",
     "start_year": 1701, "start_month": 1, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Kingdom_of_Prussia",
     "priorities": g(870_000), "region_weights": RW_GERMANY},

    {"type": "person", "title": "Frederick the Great",
     "description": "Soldier-king of Prussia; brilliant general (Rossbach, Leuthen) and Enlightenment monarch; doubled Prussian territory.",
     "start_year": 1712, "end_year": 1786, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Frederick_the_Great",
     "priorities": g(930_000, people=940_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "War of Austrian Succession",
     "description": "Prussia seizes Silesia from Austria under young Frederick II; opens the great-power rivalry of central Europe.",
     "start_year": 1740, "end_year": 1748,
     "wikipedia": "https://en.wikipedia.org/wiki/War_of_the_Austrian_Succession",
     "priorities": g(870_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Battle of Rossbach",
     "description": "Frederick the Great destroys a French-Imperial army in 90 minutes; one of the most one-sided victories in 18th-century warfare.",
     "start_year": 1757, "start_month": 11, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Rossbach",
     "priorities": g(810_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Battle of Leuthen",
     "description": "Frederick's oblique attack defeats much larger Austrian army; embodies Prussian military art.",
     "start_year": 1757, "start_month": 12, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Leuthen",
     "priorities": g(810_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "First Partition of Poland",
     "description": "Russia, Prussia, and Austria seize a third of Poland; Prussia gains Royal Prussia, connecting Brandenburg to East Prussia.",
     "start_year": 1772, "start_month": 8, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Partition_of_Poland",
     "priorities": g(860_000), "region_weights": RW_GERMANY},

    {"type": "person", "title": "Immanuel Kant",
     "description": "Königsberg philosopher; Critique of Pure Reason redefined epistemology; central figure of the Enlightenment.",
     "start_year": 1724, "end_year": 1804, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Immanuel_Kant",
     "priorities": g(930_000, people=950_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_GERMANY_GLOBAL},

    {"type": "person", "title": "Johann Sebastian Bach",
     "description": "Baroque composer working in Leipzig; sacred and instrumental masterworks; defining figure of Western classical music.",
     "start_year": 1685, "end_year": 1750, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Johann_Sebastian_Bach",
     "priorities": g(960_000, people=970_000, **{"arts-and-thoughts": 970_000}),
     "region_weights": RW_GERMANY_GLOBAL},

    {"type": "person", "title": "Goethe",
     "description": "Polymath of German letters; Faust, The Sorrows of Young Werther, Wilhelm Meister; Weimar's central cultural figure.",
     "start_year": 1749, "end_year": 1832, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Johann_Wolfgang_von_Goethe",
     "priorities": g(930_000, people=950_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_GERMANY_GLOBAL},

    {"type": "person", "title": "Beethoven",
     "description": "Bonn-born composer working in Vienna; bridged Classical and Romantic; nine symphonies, late quartets.",
     "start_year": 1770, "end_year": 1827, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ludwig_van_Beethoven",
     "priorities": g(960_000, people=970_000, **{"arts-and-thoughts": 970_000}),
     "region_weights": RW_GERMANY_GLOBAL},

    # ----- Napoleonic / Confederation era -----
    {"type": "event", "title": "Holy Roman Empire dissolved",
     "description": "Francis II abdicates the imperial throne; the thousand-year Holy Roman Empire ends under Napoleonic pressure.",
     "start_year": 1806, "start_month": 8, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Dissolution_of_the_Holy_Roman_Empire",
     "priorities": g(890_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Battle of Jena-Auerstedt",
     "description": "Napoleon crushes Prussia in a single day; triggers reformist response by Stein and Hardenberg.",
     "start_year": 1806, "start_month": 10, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Jena%E2%80%93Auerstedt",
     "priorities": g(830_000, **{"napoleonic": 870_000}), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Stein-Hardenberg reforms",
     "description": "Prussian reforms after Jena: serfdom abolished, municipal self-government, military reorganised; foundation of 19th-century Prussia.",
     "start_year": 1807, "end_year": 1815,
     "wikipedia": "https://en.wikipedia.org/wiki/Prussian_reform_movement",
     "priorities": g(800_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Battle of Leipzig (Battle of the Nations)",
     "description": "Largest battle of the Napoleonic Wars; coalition of Russia, Prussia, Austria, Sweden defeats Napoleon decisively.",
     "start_year": 1813, "start_month": 10, "start_day": 16, "end_month": 10, "end_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Leipzig",
     "priorities": g(890_000, **{"napoleonic": 920_000}), "region_weights": RW_GERMANY},

    {"type": "event", "title": "German Confederation",
     "description": "Loose union of 39 German-speaking states from Holstein to Lombardy after Congress of Vienna; Austria and Prussia jockey for primacy.",
     "start_year": 1815, "end_year": 1866,
     "wikipedia": "https://en.wikipedia.org/wiki/German_Confederation",
     "priorities": g(820_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Carlsbad Decrees",
     "description": "Metternich's Decrees impose press censorship and suppress liberal student fraternities across the German Confederation.",
     "start_year": 1819, "start_month": 9, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Carlsbad_Decrees",
     "priorities": g(740_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Zollverein (German customs union)",
     "description": "Customs union among most German states under Prussian leadership; economic integration that prefigures political unification.",
     "start_year": 1834, "start_month": 1, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Zollverein",
     "priorities": g(870_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Revolutions of 1848 in Germany",
     "description": "Liberal-nationalist uprisings across the German Confederation; Frankfurt Parliament tries to draft constitution; collapses by 1849.",
     "start_year": 1848, "end_year": 1849,
     "wikipedia": "https://en.wikipedia.org/wiki/German_revolutions_of_1848%E2%80%931849",
     "priorities": g(890_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Frankfurt Parliament",
     "description": "First freely elected German parliament tries to fashion a liberal unified Germany; offers the crown to Prussian Frederick William IV, who refuses.",
     "start_year": 1848, "end_year": 1849,
     "wikipedia": "https://en.wikipedia.org/wiki/Frankfurt_Parliament",
     "priorities": g(820_000), "region_weights": RW_GERMANY},

    # ----- Wars of Unification & Empire -----
    {"type": "person", "title": "Otto von Bismarck",
     "description": "Iron Chancellor of Prussia and Germany; engineered three wars to unify Germany; dominated European diplomacy until 1890.",
     "start_year": 1815, "end_year": 1898, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Otto_von_Bismarck",
     "priorities": g(950_000, people=960_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Second Schleswig War",
     "description": "Prussia and Austria seize Schleswig and Holstein from Denmark; first of Bismarck's three wars of unification.",
     "start_year": 1864, "start_month": 2, "end_month": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Schleswig_War",
     "priorities": g(820_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Austro-Prussian War",
     "description": "Bismarck provokes war with Austria over Schleswig-Holstein; Prussia's victory at Königgrätz expels Austria from German affairs.",
     "start_year": 1866, "start_month": 6, "end_month": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Austro-Prussian_War",
     "priorities": g(880_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Battle of Königgrätz (Sadowa)",
     "description": "Prussian needle-gun and railway-driven mobilisation crush Austrian army; decides German question in Prussia's favour.",
     "start_year": 1866, "start_month": 7, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_K%C3%B6niggr%C3%A4tz",
     "priorities": g(830_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "North German Confederation",
     "description": "Federation of north German states under Prussian leadership after defeat of Austria; precursor to the German Empire.",
     "start_year": 1867, "end_year": 1871,
     "wikipedia": "https://en.wikipedia.org/wiki/North_German_Confederation",
     "priorities": g(810_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Franco-Prussian War",
     "description": "Bismarck provokes war with France; mass conscription, rail mobilisation, and the new Krupp guns crush the Second Empire.",
     "start_year": 1870, "start_month": 7, "end_year": 1871, "end_month": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Franco-Prussian_War",
     "priorities": g(920_000, **{"france": 900_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Battle of Sedan",
     "description": "Prussians capture Napoleon III and his army; ends the Second French Empire and clears the path to German unification.",
     "start_year": 1870, "start_month": 9, "start_day": 1, "end_month": 9, "end_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Sedan",
     "priorities": g(890_000, **{"france": 870_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "German Empire proclaimed",
     "description": "Wilhelm I proclaimed German Emperor in the Hall of Mirrors at Versailles; unifies Germany under Prussian leadership.",
     "start_year": 1871, "start_month": 1, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Proclamation_of_the_German_Empire",
     "priorities": g(950_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Kulturkampf",
     "description": "Bismarck's campaign against political Catholicism in Germany; expels Jesuits, restricts Catholic schooling; ends in compromise by 1880s.",
     "start_year": 1871, "end_year": 1878,
     "wikipedia": "https://en.wikipedia.org/wiki/Kulturkampf",
     "priorities": g(800_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Bismarck's social insurance laws",
     "description": "Health, accident, and old-age insurance laws (1883-89) — the world's first national social insurance system, designed to undercut socialism.",
     "start_year": 1883, "end_year": 1889,
     "wikipedia": "https://en.wikipedia.org/wiki/State_Socialism_(Germany)",
     "priorities": g(880_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Anti-Socialist Laws",
     "description": "Bismarck's 1878 laws ban Social Democratic publications and meetings; party survives and re-emerges stronger after lapse in 1890.",
     "start_year": 1878, "end_year": 1890,
     "wikipedia": "https://en.wikipedia.org/wiki/Anti-Socialist_Laws",
     "priorities": g(770_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Dismissal of Bismarck",
     "description": "Young Wilhelm II forces Bismarck to resign; ends the Iron Chancellor's 28 years of dominance and changes German policy.",
     "start_year": 1890, "start_month": 3, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Otto_von_Bismarck",
     "priorities": g(870_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Anglo-German naval race",
     "description": "Germany under Tirpitz builds a battle-fleet to challenge the Royal Navy; central to deteriorating Anglo-German relations before WW1.",
     "start_year": 1898, "end_year": 1912,
     "wikipedia": "https://en.wikipedia.org/wiki/Anglo-German_naval_arms_race",
     "priorities": g(830_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "person", "title": "Karl Marx",
     "description": "Trier-born philosopher and economist; co-author of the Communist Manifesto; Das Kapital; spent most of his life exiled in London.",
     "start_year": 1818, "end_year": 1883, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Karl_Marx",
     "priorities": g(960_000, people=970_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_GERMANY_GLOBAL},

    {"type": "person", "title": "Friedrich Nietzsche",
     "description": "Saxon philosopher; Thus Spoke Zarathustra; On the Genealogy of Morals; declared 'God is dead'.",
     "start_year": 1844, "end_year": 1900, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Friedrich_Nietzsche",
     "priorities": g(930_000, people=940_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_GERMANY_GLOBAL},

    # ----- WWI -----
    {"type": "event", "title": "Schlieffen Plan",
     "description": "German pre-war plan to defeat France quickly via Belgium before turning east on Russia; modified version executed 1914 and fails at the Marne.",
     "start_year": 1905, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Schlieffen_Plan",
     "priorities": g(820_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Germany invades Belgium",
     "description": "German army violates Belgian neutrality on 4 August 1914; Britain enters the war the same day.",
     "start_year": 1914, "start_month": 8, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/German_invasion_of_Belgium",
     "priorities": g(890_000, **{"ww1": 940_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Battle of Tannenberg (1914)",
     "description": "Hindenburg and Ludendorff destroy the Russian Second Army in East Prussia; defining German victory of the Eastern Front.",
     "start_year": 1914, "start_month": 8, "start_day": 26, "end_month": 8, "end_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Tannenberg",
     "priorities": g(830_000, **{"ww1": 880_000}), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Unrestricted submarine warfare resumed",
     "description": "Germany resumes attacks on neutral shipping; bring the US into the war within months.",
     "start_year": 1917, "start_month": 2, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/U-boat_campaign",
     "priorities": g(840_000, **{"ww1": 880_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "German Spring Offensive",
     "description": "Ludendorff's last great offensive against the British and French; stalls and Germany has no reserves left.",
     "start_year": 1918, "start_month": 3, "start_day": 21, "end_month": 7, "end_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/German_spring_offensive",
     "priorities": g(840_000, **{"ww1": 890_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "German Revolution of 1918-19",
     "description": "Sailors mutiny at Kiel; workers' councils across Germany; Kaiser abdicates; Weimar Republic proclaimed.",
     "start_year": 1918, "start_month": 11, "start_day": 3, "end_year": 1919, "end_month": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/German_Revolution_of_1918%E2%80%931919",
     "priorities": g(910_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Abdication of Wilhelm II",
     "description": "Kaiser Wilhelm II abdicates and flees to the Netherlands; end of the German Empire and the Hohenzollern monarchy.",
     "start_year": 1918, "start_month": 11, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Wilhelm_II,_German_Emperor",
     "priorities": g(890_000), "region_weights": RW_GERMANY},

    # ----- Weimar / Nazi era -----
    {"type": "event", "title": "Treaty of Versailles (German perspective)",
     "description": "Diktat imposed on defeated Germany; war guilt clause, reparations, territorial losses; loathed across the political spectrum.",
     "start_year": 1919, "start_month": 6, "start_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Versailles",
     "priorities": g(950_000, **{"ww1": 950_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Weimar Republic",
     "description": "Germany's first parliamentary democracy; created at Weimar 1919, undone by economic crisis and Nazi takeover 1933.",
     "start_year": 1919, "end_year": 1933, "start_month": 8, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Weimar_Republic",
     "priorities": g(920_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Spartacist uprising",
     "description": "Communist revolt in Berlin under Karl Liebknecht and Rosa Luxemburg crushed by Freikorps; both leaders murdered.",
     "start_year": 1919, "start_month": 1, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Spartacist_uprising",
     "priorities": g(830_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Hyperinflation of 1923",
     "description": "Reichsmark collapses; price of a loaf of bread reaches billions of marks; wipes out middle-class savings.",
     "start_year": 1923, "end_year": 1924,
     "wikipedia": "https://en.wikipedia.org/wiki/Hyperinflation_in_the_Weimar_Republic",
     "priorities": g(900_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Beer Hall Putsch",
     "description": "Hitler and Ludendorff attempt coup at a Munich beer hall; crushed by police; Hitler imprisoned and writes Mein Kampf.",
     "start_year": 1923, "start_month": 11, "start_day": 8, "end_month": 11, "end_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Beer_Hall_Putsch",
     "priorities": g(880_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Dawes Plan",
     "description": "American-brokered restructuring of German reparations and stabilisation of the currency; opens the 'golden twenties'.",
     "start_year": 1924, "start_month": 8, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Dawes_Plan",
     "priorities": g(790_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Hindenburg becomes President",
     "description": "Old field marshal Hindenburg elected President of Germany; symbolically restores imperial-era authority.",
     "start_year": 1925, "start_month": 4, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Paul_von_Hindenburg",
     "priorities": g(780_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Hitler appointed Chancellor",
     "description": "President Hindenburg names Hitler chancellor of Germany; effective end of Weimar democracy within months.",
     "start_year": 1933, "start_month": 1, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Adolf_Hitler%27s_rise_to_power",
     "priorities": g(970_000, **{"ww2": 960_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Reichstag fire",
     "description": "Berlin parliament building burned by Marinus van der Lubbe; pretext for the Reichstag Fire Decree suspending civil liberties.",
     "start_year": 1933, "start_month": 2, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Reichstag_fire",
     "priorities": g(890_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Enabling Act",
     "description": "Reichstag votes Hitler the power to legislate without parliament; formal end of the Weimar constitution.",
     "start_year": 1933, "start_month": 3, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Enabling_Act_of_1933",
     "priorities": g(900_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Night of the Long Knives",
     "description": "Hitler purges the SA leadership and other enemies; Röhm and dozens killed; cements Hitler's grip on Nazi party and state.",
     "start_year": 1934, "start_month": 6, "start_day": 30, "end_month": 7, "end_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Night_of_the_Long_Knives",
     "priorities": g(870_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Nuremberg Race Laws",
     "description": "Reichstag at Nuremberg passes anti-Jewish citizenship and blood laws; legal armature of the Holocaust.",
     "start_year": 1935, "start_month": 9, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Nuremberg_Laws",
     "priorities": g(910_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Remilitarisation of the Rhineland",
     "description": "Hitler sends troops into the demilitarised Rhineland in violation of Versailles; Allies do nothing.",
     "start_year": 1936, "start_month": 3, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Remilitarization_of_the_Rhineland",
     "priorities": g(850_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Anschluss (annexation of Austria)",
     "description": "Wehrmacht enters Austria; Hitler proclaims union with the Reich at Vienna; cheered by crowds.",
     "start_year": 1938, "start_month": 3, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Anschluss",
     "priorities": g(900_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Kristallnacht",
     "description": "Nazi-coordinated pogroms across Germany and Austria; synagogues burned, Jewish-owned shops smashed, ~30,000 sent to camps.",
     "start_year": 1938, "start_month": 11, "start_day": 9, "end_month": 11, "end_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Kristallnacht",
     "priorities": g(910_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Wannsee Conference",
     "description": "Heydrich coordinates Nazi ministries' role in the 'Final Solution' to the Jewish question; bureaucratic blueprint for genocide.",
     "start_year": 1942, "start_month": 1, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Wannsee_Conference",
     "priorities": g(910_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "July 20 plot to kill Hitler",
     "description": "Claus von Stauffenberg's bomb at Wolf's Lair fails to kill Hitler; thousands of suspects executed in retaliation.",
     "start_year": 1944, "start_month": 7, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/20_July_plot",
     "priorities": g(870_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Battle of Berlin",
     "description": "Soviet final assault on Berlin; Hitler commits suicide in the Führerbunker; Reich falls.",
     "start_year": 1945, "start_month": 4, "start_day": 16, "end_month": 5, "end_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Berlin",
     "priorities": g(920_000, **{"ww2": 950_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "German Instrument of Surrender",
     "description": "Germany signs unconditional surrender at Reims and Berlin-Karlshorst; V-E Day.",
     "start_year": 1945, "start_month": 5, "start_day": 7, "end_month": 5, "end_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/German_Instrument_of_Surrender",
     "priorities": g(960_000, **{"ww2": 970_000}), "region_weights": RW_GERMANY_GLOBAL},

    # ----- Divided Germany / Cold War -----
    {"type": "event", "title": "Allied occupation of Germany",
     "description": "Germany divided into US, UK, French, and Soviet zones with quadripartite occupation of Berlin; 1945-1949.",
     "start_year": 1945, "end_year": 1949,
     "wikipedia": "https://en.wikipedia.org/wiki/Allied-occupied_Germany",
     "priorities": g(900_000, **{"cold-war": 880_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Nuremberg trials open",
     "description": "International Military Tribunal at Nuremberg tries surviving Nazi leadership; legal landmark for crimes against humanity.",
     "start_year": 1945, "start_month": 11, "start_day": 20, "end_year": 1946, "end_month": 10, "end_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Nuremberg_trials",
     "priorities": g(920_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Marshall Plan funds reach Germany",
     "description": "American economic aid pours in to rebuild western Germany; cornerstone of Wirtschaftswunder and integration into the West.",
     "start_year": 1948,
     "wikipedia": "https://en.wikipedia.org/wiki/Marshall_Plan",
     "priorities": g(900_000, **{"cold-war": 910_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Wirtschaftswunder (economic miracle)",
     "description": "West Germany's rapid postwar recovery under Adenauer and finance minister Erhard; full employment and global competitiveness by mid-1950s.",
     "start_year": 1948, "end_year": 1973,
     "wikipedia": "https://en.wikipedia.org/wiki/Wirtschaftswunder",
     "priorities": g(890_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Adenauer's chancellorship",
     "description": "Konrad Adenauer leads West Germany from founding through integration into NATO and the European Community.",
     "start_year": 1949, "end_year": 1963, "start_month": 9, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Konrad_Adenauer",
     "priorities": g(880_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "East German uprising of 1953",
     "description": "Strikes and street protests across East Germany suppressed by Soviet troops; first major Eastern Bloc revolt.",
     "start_year": 1953, "start_month": 6, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/East_German_uprising_of_1953",
     "priorities": g(800_000, **{"cold-war": 820_000}), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Germany joins NATO",
     "description": "West Germany admitted to NATO; rearmament under Allied supervision; Bundeswehr created.",
     "start_year": 1955, "start_month": 5, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Germany_in_NATO",
     "priorities": g(830_000, **{"cold-war": 850_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Berlin Wall built",
     "description": "East Germany seals off West Berlin overnight with barbed wire that becomes a concrete wall; symbol of Cold War for 28 years.",
     "start_year": 1961, "start_month": 8, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Berlin_Wall",
     "priorities": g(950_000, **{"cold-war": 970_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Ich bin ein Berliner speech",
     "description": "John F. Kennedy speaks in West Berlin in solidarity with the city; defining Cold War rhetorical moment.",
     "start_year": 1963, "start_month": 6, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Ich_bin_ein_Berliner",
     "priorities": g(870_000, **{"cold-war": 870_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Brandt's Ostpolitik",
     "description": "Chancellor Willy Brandt seeks normalisation with Eastern Bloc; treaties with Soviet Union, Poland, GDR; kneels at the Warsaw Ghetto memorial.",
     "start_year": 1969, "end_year": 1974,
     "wikipedia": "https://en.wikipedia.org/wiki/Ostpolitik",
     "priorities": g(890_000, **{"cold-war": 880_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Red Army Faction terrorism",
     "description": "Left-wing terrorist group (Baader-Meinhof) commits bombings, kidnappings, assassinations across West Germany.",
     "start_year": 1970, "end_year": 1998,
     "wikipedia": "https://en.wikipedia.org/wiki/Red_Army_Faction",
     "priorities": g(820_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "German Autumn",
     "description": "Crisis of 1977: RAF kidnaps and kills employer's federation president Schleyer; Lufthansa hijacking; suicides at Stammheim.",
     "start_year": 1977, "start_month": 9, "end_month": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/German_Autumn",
     "priorities": g(800_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Helmut Kohl's chancellorship",
     "description": "Christian Democrat Helmut Kohl leads West Germany through Cold War's end; mastermind of reunification; longest-serving postwar chancellor.",
     "start_year": 1982, "end_year": 1998, "start_month": 10, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Helmut_Kohl",
     "priorities": g(860_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Tear down this wall speech",
     "description": "Ronald Reagan at the Brandenburg Gate calls on Gorbachev to 'tear down this wall'.",
     "start_year": 1987, "start_month": 6, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Tear_down_this_wall!",
     "priorities": g(860_000, **{"cold-war": 870_000}), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Monday demonstrations in Leipzig",
     "description": "Weekly mass protests in East German cities; tens of thousands chant 'Wir sind das Volk' and erode the regime's authority.",
     "start_year": 1989, "start_month": 9, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Monday_demonstrations_in_East_Germany",
     "priorities": g(830_000, **{"cold-war": 870_000}), "region_weights": RW_GERMANY},

    {"type": "event", "title": "German reunification",
     "description": "GDR accedes to the Federal Republic; Germany reunified after 45 years of division; Two Plus Four Treaty restores full sovereignty.",
     "start_year": 1990, "start_month": 10, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/German_reunification",
     "priorities": g(960_000, **{"cold-war": 960_000}), "region_weights": RW_GERMANY_GLOBAL},

    # ----- Reunified Germany -----
    {"type": "event", "title": "Treaty of Maastricht (German role)",
     "description": "Germany accepts loss of the Deutsche Mark in exchange for European political union; the deal makes the euro possible.",
     "start_year": 1992, "start_month": 2, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Maastricht_Treaty",
     "priorities": g(880_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Berlin returns as German capital",
     "description": "Federal government moves from Bonn back to Berlin; Reichstag restored under Norman Foster's glass dome.",
     "start_year": 1999, "start_month": 9, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Berlin",
     "priorities": g(820_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Hartz IV labour reforms",
     "description": "Schröder government's controversial labour and welfare reforms; cut unemployment but split SPD and birthed the Left party.",
     "start_year": 2003, "end_year": 2005,
     "wikipedia": "https://en.wikipedia.org/wiki/Hartz_concept",
     "priorities": g(800_000), "region_weights": RW_GERMANY},

    {"type": "event", "title": "Angela Merkel's chancellorship",
     "description": "First female German chancellor; physicist from the GDR; defines European politics for 16 years (2005-2021).",
     "start_year": 2005, "end_year": 2021, "start_month": 11, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Angela_Merkel",
     "priorities": g(910_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Eurozone crisis (German role)",
     "description": "Germany leads austerity-conditioned bailouts of Greece, Ireland, Portugal, Spain; defines its European role for a decade.",
     "start_year": 2010, "end_year": 2015,
     "wikipedia": "https://en.wikipedia.org/wiki/European_debt_crisis",
     "priorities": g(870_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Energiewende (energy transition)",
     "description": "Merkel accelerates nuclear phase-out after Fukushima; massive expansion of renewables; reshapes German energy policy.",
     "start_year": 2011, "start_month": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Energiewende",
     "priorities": g(840_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "2015 European migrant crisis",
     "description": "Merkel opens border to Syrian refugees; over 800,000 asylum seekers reach Germany in a year; transforms domestic politics.",
     "start_year": 2015, "start_month": 8, "start_day": 31,
     "wikipedia": "https://en.wikipedia.org/wiki/2015_European_migrant_crisis",
     "priorities": g(890_000), "region_weights": RW_GERMANY_GLOBAL},

    {"type": "event", "title": "Zeitenwende speech",
     "description": "Chancellor Scholz announces €100bn rearmament and end of decades of restrained defence policy in response to Russian invasion of Ukraine.",
     "start_year": 2022, "start_month": 2, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Zeitenwende",
     "priorities": g(870_000), "region_weights": RW_GERMANY_GLOBAL},
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
