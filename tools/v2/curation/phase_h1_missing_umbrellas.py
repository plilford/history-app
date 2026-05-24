"""
Phase H1 — Create missing umbrellas (parent rows) and scaffold their
children. Each cluster already has many entries scattered in the dataset
that lack a single parent; the new umbrella entries make the rollup zoom
collapse them cleanly.

Conventions:
  - Each umbrella entry's title is referenceable from children's
    first_zoom_out / second_zoom_out fields.
  - Umbrella master priority is high (980k+) when the topic is
    universally famous; ~900k-960k otherwise.
  - Umbrella has a long span (start_year..end_year of the period).
  - Children that are NOT in this script (i.e., already exist in the
    dataset) need a separate retrofit step to point their first_zoom_out
    at the new umbrella. We do that in a follow-up script
    (phase_h_retrofit_umbrella_refs.py) so this file stays declarative.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_GLOBAL = {"europe": 8, "americas": 7, "asia": 5, "australasia": 3, "africa": 4}
RW_EU = {"europe": 10, "americas": 3, "asia": 3, "australasia": 1, "africa": 3}
RW_AMER = {"europe": 4, "americas": 10, "asia": 1, "australasia": 1, "africa": 3}
RW_CRUSADE = {"europe": 10, "americas": 1, "asia": 9, "australasia": 1, "africa": 6}
RW_AFRICA = {"europe": 3, "americas": 4, "asia": 2, "australasia": 1, "africa": 10}
RW_RUSSIA = {"europe": 9, "americas": 4, "asia": 5, "australasia": 1, "africa": 1}


def pri(master: int, **extras) -> dict:
    return {"master": master, **extras}


ENTRIES = [
    # =================================================================
    # PUNIC WARS — just the umbrella; children all exist
    # =================================================================
    {"type": "event", "title": "Punic Wars",
     "description": "Three wars between Rome and Carthage (264-146 BCE) for western Mediterranean supremacy; ends with Carthage's destruction.",
     "start_year": -264, "end_year": -146,
     "wikipedia": "https://en.wikipedia.org/wiki/Punic_Wars",
     "priorities": pri(960_000, **{"roman-history": 950_000}),
     "region_weights": {"europe": 10, "americas": 1, "asia": 2, "australasia": 1, "africa": 8}},

    # =================================================================
    # VIKING AGE
    # =================================================================
    {"type": "event", "title": "Viking Age",
     "description": "Era of Norse seaborne raiding, trading and settlement from Lindisfarne 793 to Stamford Bridge 1066.",
     "start_year": 793, "end_year": 1066,
     "wikipedia": "https://en.wikipedia.org/wiki/Viking_Age",
     "priorities": pri(960_000, england=940_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Rollo and Normandy founded",
     "description": "Treaty of Saint-Clair-sur-Epte grants Viking leader Rollo land that becomes Normandy; his descendants conquer England in 1066.",
     "start_year": 911,
     "wikipedia": "https://en.wikipedia.org/wiki/Rollo",
     "priorities": pri(890_000, france=900_000, england=860_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Viking Age"},

    {"type": "person", "title": "Leif Erikson",
     "description": "Icelandic explorer; first European known to have landed in continental North America (Vinland, c. 1000), 500 years before Columbus.",
     "start_year": 970, "end_year": 1020, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Leif_Erikson",
     "priorities": pri(890_000, people=900_000),
     "region_weights": RW_EU},

    {"type": "person", "title": "Erik the Red",
     "description": "Founder of the first Norse settlement in Greenland; outlawed from Iceland for manslaughter; father of Leif Erikson.",
     "start_year": 950, "end_year": 1003, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Erik_the_Red",
     "priorities": pri(840_000, people=860_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Norse settlement of Greenland",
     "description": "Erik the Red leads colonists from Iceland; Norse Greenlanders survive ~450 years before mysterious 15th-century collapse.",
     "start_year": 985, "end_year": 1450, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Norse_colonization_of_North_America",
     "priorities": pri(830_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Viking Age"},

    {"type": "event", "title": "Varangian Guard formed",
     "description": "Elite Norse mercenary unit serving Byzantine emperors; founded by Vladimir of Kiev's gift to Basil II; serves for over two centuries.",
     "start_year": 988,
     "wikipedia": "https://en.wikipedia.org/wiki/Varangian_Guard",
     "priorities": pri(820_000, **{"roman-history": 830_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Viking Age"},

    # =================================================================
    # SCIENTIFIC REVOLUTION
    # =================================================================
    {"type": "event", "title": "Scientific Revolution",
     "description": "European intellectual transformation in physics, astronomy, biology, and chemistry; Copernicus to Newton; foundation of modern science.",
     "start_year": 1543, "end_year": 1727,
     "wikipedia": "https://en.wikipedia.org/wiki/Scientific_Revolution",
     "priorities": pri(980_000, renaissance=970_000, **{"arts-and-thoughts": 980_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Galileo's heliocentric advocacy",
     "description": "Galileo champions Copernicanism; clashes with Catholic Church; trial 1633; placed under house arrest for the rest of his life.",
     "start_year": 1613, "end_year": 1633,
     "wikipedia": "https://en.wikipedia.org/wiki/Galileo_affair",
     "priorities": pri(910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Scientific Revolution"},

    {"type": "person", "title": "Francis Bacon",
     "description": "Lord Chancellor and philosopher; founder of empirical scientific method; Novum Organum (1620) lays out inductive reasoning.",
     "start_year": 1561, "end_year": 1626, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Francis_Bacon",
     "priorities": pri(890_000, england=880_000, people=900_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Robert Boyle",
     "description": "Anglo-Irish founder of modern chemistry; Boyle's law of gases; The Sceptical Chymist (1661).",
     "start_year": 1627, "end_year": 1691, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Robert_Boyle",
     "priorities": pri(870_000, england=850_000, people=880_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_EU},

    {"type": "event", "title": "Vesalius's De humani corporis fabrica",
     "description": "Andreas Vesalius's anatomical treatise based on dissection; overturns 1,400 years of Galenic anatomy.",
     "start_year": 1543,
     "wikipedia": "https://en.wikipedia.org/wiki/De_humani_corporis_fabrica",
     "priorities": pri(880_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Scientific Revolution"},

    {"type": "person", "title": "Christiaan Huygens",
     "description": "Dutch polymath; invented pendulum clock; first to identify Saturn's rings; wave theory of light.",
     "start_year": 1629, "end_year": 1695, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Christiaan_Huygens",
     "priorities": pri(870_000, people=880_000, **{"arts-and-thoughts": 890_000}),
     "region_weights": RW_EU},

    {"type": "person", "title": "Antonie van Leeuwenhoek",
     "description": "Dutch microscopist; first to see microorganisms, bacteria, sperm cells; founder of microbiology.",
     "start_year": 1632, "end_year": 1723, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Antonie_van_Leeuwenhoek",
     "priorities": pri(870_000, people=890_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_EU},

    {"type": "event", "title": "Royal Society founded",
     "description": "Royal Society of London chartered to promote experimental natural philosophy; first national scientific society in the world.",
     "start_year": 1660, "start_month": 11, "start_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Royal_Society",
     "priorities": pri(910_000, england=920_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Scientific Revolution"},

    # =================================================================
    # ENLIGHTENMENT
    # =================================================================
    {"type": "event", "title": "Age of Enlightenment",
     "description": "Intellectual movement championing reason, individualism, scepticism toward authority; from Locke through Kant; underpins American and French Revolutions.",
     "start_year": 1685, "end_year": 1815,
     "wikipedia": "https://en.wikipedia.org/wiki/Age_of_Enlightenment",
     "priorities": pri(980_000, **{"arts-and-thoughts": 980_000}),
     "region_weights": RW_GLOBAL},

    {"type": "art", "title": "Locke's Two Treatises of Government",
     "description": "Foundational text of liberal political philosophy; natural rights; right of revolution; deep influence on American founding.",
     "start_year": 1689,
     "wikipedia": "https://en.wikipedia.org/wiki/Two_Treatises_of_Government",
     "priorities": pri(920_000, england=910_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Age of Enlightenment"},

    {"type": "person", "title": "Montesquieu",
     "description": "French Enlightenment political philosopher; The Spirit of the Laws articulates separation of powers; shapes US Constitution.",
     "start_year": 1689, "end_year": 1755, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Montesquieu",
     "priorities": pri(900_000, france=910_000, people=910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_EU},

    {"type": "art", "title": "Montesquieu's The Spirit of the Laws",
     "description": "Major treatise on political theory; arguments for separation of powers shape constitutional thought across the Atlantic.",
     "start_year": 1748,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Spirit_of_the_Laws",
     "priorities": pri(890_000, france=900_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Age of Enlightenment"},

    {"type": "person", "title": "Adam Smith",
     "description": "Scottish moral philosopher; The Wealth of Nations (1776) founds classical economics; The Theory of Moral Sentiments.",
     "start_year": 1723, "end_year": 1790, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Adam_Smith",
     "priorities": pri(950_000, england=920_000, people=950_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_GLOBAL},

    {"type": "art", "title": "Smith's The Wealth of Nations",
     "description": "Foundational text of modern economics; division of labour, the invisible hand, free trade.",
     "start_year": 1776, "start_month": 3, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Wealth_of_Nations",
     "priorities": pri(940_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Age of Enlightenment"},

    {"type": "person", "title": "Edward Gibbon",
     "description": "English historian; The History of the Decline and Fall of the Roman Empire; defining work of 18th-century historiography.",
     "start_year": 1737, "end_year": 1794, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Edward_Gibbon",
     "priorities": pri(880_000, england=890_000, people=900_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_EU},

    {"type": "art", "title": "Gibbon's Decline and Fall of the Roman Empire",
     "description": "Six-volume narrative history of Rome from the Antonines to Constantinople; landmark of English prose.",
     "start_year": 1776, "end_year": 1789,
     "wikipedia": "https://en.wikipedia.org/wiki/The_History_of_the_Decline_and_Fall_of_the_Roman_Empire",
     "priorities": pri(910_000, **{"arts-and-thoughts": 930_000, "roman-history": 870_000}),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Age of Enlightenment"},

    {"type": "person", "title": "Mary Wollstonecraft",
     "description": "English writer and proto-feminist; A Vindication of the Rights of Woman (1792); mother of Mary Shelley.",
     "start_year": 1759, "end_year": 1797, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mary_Wollstonecraft",
     "priorities": pri(890_000, england=910_000, people=910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_GLOBAL},

    {"type": "art", "title": "A Vindication of the Rights of Woman",
     "description": "Mary Wollstonecraft's foundational text for liberal feminism; argues for equal education and rights.",
     "start_year": 1792,
     "wikipedia": "https://en.wikipedia.org/wiki/A_Vindication_of_the_Rights_of_Woman",
     "priorities": pri(910_000, england=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Age of Enlightenment"},

    {"type": "person", "title": "Benjamin Franklin",
     "description": "American polymath; printer, scientist, diplomat; Founding Father; experiments with electricity; minister to France during Revolution.",
     "start_year": 1706, "end_year": 1790, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Benjamin_Franklin",
     "priorities": pri(940_000, usa=950_000, people=950_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_AMER},

    # =================================================================
    # AGE OF EXPLORATION
    # =================================================================
    {"type": "event", "title": "Age of Exploration",
     "description": "European maritime discoveries from Prince Henry the Navigator's Atlantic voyages to the Pacific charting of Cook; reshapes the world.",
     "start_year": 1418, "end_year": 1779,
     "wikipedia": "https://en.wikipedia.org/wiki/Age_of_Discovery",
     "priorities": pri(970_000),
     "region_weights": RW_GLOBAL},

    {"type": "person", "title": "Henry the Navigator",
     "description": "Portuguese prince; financed exploratory voyages down the West African coast; school of navigators at Sagres; godfather of European overseas expansion.",
     "start_year": 1394, "end_year": 1460, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Prince_Henry_the_Navigator",
     "priorities": pri(870_000, people=890_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Bartolomeu Dias rounds the Cape",
     "description": "Portuguese explorer sails round Cape of Good Hope; opens sea route to India.",
     "start_year": 1488,
     "wikipedia": "https://en.wikipedia.org/wiki/Bartolomeu_Dias",
     "priorities": pri(880_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Age of Exploration"},

    {"type": "event", "title": "John Cabot reaches North America",
     "description": "Italian-born English explorer reaches Newfoundland; first verified European landing on continental North America since the Vikings.",
     "start_year": 1497, "start_month": 6, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/John_Cabot",
     "priorities": pri(840_000, england=860_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Age of Exploration"},

    {"type": "event", "title": "Cabral reaches Brazil",
     "description": "Portuguese fleet under Pedro Álvares Cabral, bound for India, lands on the Brazilian coast; Portugal claims and colonises Brazil.",
     "start_year": 1500, "start_month": 4, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Pedro_%C3%81lvares_Cabral",
     "priorities": pri(870_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Age of Exploration"},

    {"type": "event", "title": "Balboa crosses the Isthmus of Panama",
     "description": "Vasco Núñez de Balboa sights the Pacific Ocean from a peak in Panama; first European to view the Pacific from the Americas.",
     "start_year": 1513, "start_month": 9, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Vasco_N%C3%BA%C3%B1ez_de_Balboa",
     "priorities": pri(830_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Age of Exploration"},

    {"type": "event", "title": "Cook's first Pacific voyage",
     "description": "Captain James Cook's HMS Endeavour charts New Zealand and east coast of Australia; opens Pacific to European exploration and colonisation.",
     "start_year": 1768, "end_year": 1771,
     "wikipedia": "https://en.wikipedia.org/wiki/First_voyage_of_James_Cook",
     "priorities": pri(890_000, england=900_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Age of Exploration"},

    {"type": "person", "title": "Captain James Cook",
     "description": "British naval explorer; three Pacific voyages charted New Zealand, Australia, Hawaii; killed in Hawaii in 1779.",
     "start_year": 1728, "end_year": 1779, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/James_Cook",
     "priorities": pri(900_000, england=910_000, people=910_000),
     "region_weights": RW_GLOBAL},

    # =================================================================
    # ATLANTIC SLAVE TRADE
    # =================================================================
    {"type": "event", "title": "Atlantic slave trade",
     "description": "Trans-Atlantic trade in enslaved Africans; ~12 million people transported from c. 1500 to 1888; defines economy of Americas, Africa, Europe.",
     "start_year": 1500, "end_year": 1888,
     "wikipedia": "https://en.wikipedia.org/wiki/Atlantic_slave_trade",
     "priorities": pri(960_000),
     "region_weights": {"europe": 7, "americas": 10, "asia": 1, "australasia": 1, "africa": 10}},

    {"type": "event", "title": "Asiento system",
     "description": "Spanish royal contract granting trading companies the monopoly on importing slaves to its colonies; British asiento after Utrecht.",
     "start_year": 1518, "end_year": 1789,
     "wikipedia": "https://en.wikipedia.org/wiki/Asiento_de_Negros",
     "priorities": pri(830_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Atlantic slave trade"},

    {"type": "event", "title": "Royal African Company founded",
     "description": "English chartered company dominating English slave trade through late 17th century; transports ~150,000 enslaved Africans by 1731.",
     "start_year": 1672,
     "wikipedia": "https://en.wikipedia.org/wiki/Royal_African_Company",
     "priorities": pri(830_000, england=850_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Atlantic slave trade"},

    {"type": "event", "title": "Stono Rebellion",
     "description": "Largest slave rebellion in British colonial America; slaves in South Carolina kill ~25 whites; brutally suppressed.",
     "start_year": 1739, "start_month": 9, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Stono_Rebellion",
     "priorities": pri(820_000, usa=860_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "Atlantic slave trade"},

    {"type": "event", "title": "Somerset case",
     "description": "English court rules slavery has no foundation in English law; James Somerset freed; symbolically ends slavery on English soil.",
     "start_year": 1772, "start_month": 6, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Somerset_v_Stewart",
     "priorities": pri(870_000, england=890_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Atlantic slave trade"},

    {"type": "person", "title": "William Wilberforce",
     "description": "British MP and abolitionist; led the parliamentary campaign that ended the slave trade (1807) and slavery (1833).",
     "start_year": 1759, "end_year": 1833, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/William_Wilberforce",
     "priorities": pri(900_000, england=920_000, people=910_000),
     "region_weights": RW_EU},

    {"type": "person", "title": "Olaudah Equiano",
     "description": "Igbo abolitionist; bought his own freedom; The Interesting Narrative (1789) became a key abolitionist text and bestseller.",
     "start_year": 1745, "end_year": 1797, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Olaudah_Equiano",
     "priorities": pri(870_000, england=890_000, people=890_000, **{"arts-and-thoughts": 890_000}),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Nat Turner's rebellion",
     "description": "Slave revolt in Virginia led by Nat Turner; 60 whites killed; ferocious retaliation; tightens slave laws across the South.",
     "start_year": 1831, "start_month": 8, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Nat_Turner%27s_slave_rebellion",
     "priorities": pri(870_000, usa=890_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "Atlantic slave trade"},

    {"type": "event", "title": "Underground Railroad",
     "description": "Informal network helping enslaved people escape to free states and Canada; tens of thousands escape; figures like Harriet Tubman.",
     "start_year": 1810, "end_year": 1865, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Underground_Railroad",
     "priorities": pri(900_000, usa=920_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "Atlantic slave trade"},

    {"type": "person", "title": "Harriet Tubman",
     "description": "Escaped slave and Underground Railroad conductor; led ~70 enslaved people to freedom; Union Army scout during the Civil War.",
     "start_year": 1822, "end_year": 1913, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Harriet_Tubman",
     "priorities": pri(910_000, usa=930_000, people=920_000),
     "region_weights": RW_AMER},

    # =================================================================
    # US CIVIL RIGHTS MOVEMENT
    # =================================================================
    {"type": "event", "title": "US Civil Rights Movement",
     "description": "Mass nonviolent campaign for African-American rights from Brown v. Board (1954) through 1968; culminates in Civil Rights and Voting Rights Acts.",
     "start_year": 1954, "end_year": 1968,
     "wikipedia": "https://en.wikipedia.org/wiki/Civil_rights_movement",
     "priorities": pri(970_000, usa=970_000),
     "region_weights": RW_AMER},

    {"type": "event", "title": "Plessy v. Ferguson",
     "description": "Supreme Court upholds 'separate but equal'; legal foundation of US segregation until overturned by Brown in 1954.",
     "start_year": 1896, "start_month": 5, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Plessy_v._Ferguson",
     "priorities": pri(890_000, usa=920_000),
     "region_weights": RW_AMER},

    {"type": "event", "title": "Lynching of Emmett Till",
     "description": "14-year-old African-American murdered in Mississippi; his mother insists on an open casket; photo galvanises civil rights movement.",
     "start_year": 1955, "start_month": 8, "start_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Murder_of_Emmett_Till",
     "priorities": pri(870_000, usa=910_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "US Civil Rights Movement"},

    {"type": "event", "title": "Little Rock Nine",
     "description": "Nine African-American students escorted by federal troops into Little Rock Central High School after governor's segregationist stand.",
     "start_year": 1957, "start_month": 9, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Little_Rock_Nine",
     "priorities": pri(860_000, usa=890_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "US Civil Rights Movement"},

    {"type": "event", "title": "Greensboro sit-ins",
     "description": "Four African-American students sit at a Woolworth's lunch counter; touches off sit-in movement across the South.",
     "start_year": 1960, "start_month": 2, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Greensboro_sit-ins",
     "priorities": pri(860_000, usa=890_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "US Civil Rights Movement"},

    {"type": "event", "title": "Birmingham campaign",
     "description": "MLK and SCLC campaign in Birmingham; police use fire hoses and dogs on children; photos shock the nation.",
     "start_year": 1963, "start_month": 4, "start_day": 3, "end_month": 5, "end_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Birmingham_campaign",
     "priorities": pri(870_000, usa=900_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "US Civil Rights Movement"},

    {"type": "event", "title": "Selma to Montgomery marches",
     "description": "Voting-rights marchers attacked on Edmund Pettus Bridge on 'Bloody Sunday'; LBJ's response: Voting Rights Act.",
     "start_year": 1965, "start_month": 3, "start_day": 7, "end_month": 3, "end_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Selma_to_Montgomery_marches",
     "priorities": pri(900_000, usa=920_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "US Civil Rights Movement"},

    {"type": "event", "title": "Voting Rights Act of 1965",
     "description": "Federal law banning racial discrimination in voting; centerpiece civil rights legislation; transforms Southern politics.",
     "start_year": 1965, "start_month": 8, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Voting_Rights_Act_of_1965",
     "priorities": pri(920_000, usa=940_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "US Civil Rights Movement"},

    {"type": "event", "title": "Loving v. Virginia",
     "description": "Supreme Court strikes down state bans on interracial marriage; final dismantling of legal segregation in private life.",
     "start_year": 1967, "start_month": 6, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Loving_v._Virginia",
     "priorities": pri(880_000, usa=910_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "US Civil Rights Movement"},

    {"type": "event", "title": "Watts riots",
     "description": "Six-day uprising in Los Angeles after a traffic stop; 34 killed; foreshadows the wave of 'long hot summer' riots of the late 60s.",
     "start_year": 1965, "start_month": 8, "start_day": 11, "end_month": 8, "end_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Watts_riots",
     "priorities": pri(830_000, usa=870_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "US Civil Rights Movement"},

    # =================================================================
    # RUSSIAN CIVIL WAR
    # =================================================================
    {"type": "event", "title": "Russian Civil War",
     "description": "Multi-sided conflict 1917-1923; Bolshevik Red Army defeats Whites, foreign interventionists, and Greens; consolidates Soviet rule.",
     "start_year": 1917, "end_year": 1923,
     "wikipedia": "https://en.wikipedia.org/wiki/Russian_Civil_War",
     "priorities": pri(940_000),
     "region_weights": RW_RUSSIA},

    {"type": "person", "title": "Vladimir Lenin",
     "description": "Bolshevik leader; mastermind of October Revolution; first head of Soviet Russia; theoretician of Marxism-Leninism.",
     "start_year": 1870, "end_year": 1924, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Vladimir_Lenin",
     "priorities": pri(970_000, people=970_000),
     "region_weights": RW_RUSSIA},

    {"type": "person", "title": "Leon Trotsky",
     "description": "Bolshevik revolutionary; founder of Red Army; lost power struggle to Stalin; exiled and assassinated in Mexico City 1940.",
     "start_year": 1879, "end_year": 1940, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Leon_Trotsky",
     "priorities": pri(910_000, people=920_000),
     "region_weights": RW_RUSSIA},

    {"type": "event", "title": "Kornilov affair",
     "description": "General Kornilov's attempted march on Petrograd to restore order; collapse leaves Bolsheviks armed and the Provisional Government discredited.",
     "start_year": 1917, "start_month": 9, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Kornilov_affair",
     "priorities": pri(820_000),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "Russian Civil War"},

    {"type": "event", "title": "Treaty of Brest-Litovsk (Russian view)",
     "description": "Russia signs humiliating peace with Central Powers; cedes vast territory; ratchets civil war as Whites refuse to accept.",
     "start_year": 1918, "start_month": 3, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Brest-Litovsk",
     "priorities": pri(890_000, **{"ww1": 920_000}),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "Russian Civil War"},

    {"type": "event", "title": "Red Terror (1918-1922)",
     "description": "Mass executions, imprisonments and forced labour carried out by Cheka secret police; tens of thousands killed.",
     "start_year": 1918, "start_month": 9, "start_day": 5, "end_year": 1922,
     "wikipedia": "https://en.wikipedia.org/wiki/Red_Terror",
     "priorities": pri(870_000),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "Russian Civil War"},

    {"type": "event", "title": "Polish-Soviet War",
     "description": "Newly independent Poland defeats Bolshevik attempt to spread revolution westward; Polish 'miracle on the Vistula' at Warsaw 1920.",
     "start_year": 1919, "end_year": 1921,
     "wikipedia": "https://en.wikipedia.org/wiki/Polish%E2%80%93Soviet_War",
     "priorities": pri(870_000),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "Russian Civil War"},

    {"type": "event", "title": "Soviet Union founded",
     "description": "Treaty on the Creation of the USSR brings together Russian, Ukrainian, Belarusian and Transcaucasian republics.",
     "start_year": 1922, "start_month": 12, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_on_the_Creation_of_the_USSR",
     "priorities": pri(940_000),
     "region_weights": RW_RUSSIA},

    {"type": "event", "title": "Kronstadt rebellion",
     "description": "Soviet sailors rebel against Bolshevik rule; Trotsky leads brutal suppression; pushes Lenin to introduce the New Economic Policy.",
     "start_year": 1921, "start_month": 3, "start_day": 1, "end_month": 3, "end_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Kronstadt_rebellion",
     "priorities": pri(810_000),
     "region_weights": RW_RUSSIA,
     "first_zoom_out": "Russian Civil War"},

    # =================================================================
    # ROMANTICISM
    # =================================================================
    {"type": "event", "title": "Romanticism (movement)",
     "description": "Late-18th to mid-19th century cultural movement valuing emotion, nature, the sublime; reacts against Enlightenment rationalism and Industrial Revolution.",
     "start_year": 1798, "end_year": 1850,
     "wikipedia": "https://en.wikipedia.org/wiki/Romanticism",
     "priorities": pri(960_000, **{"arts-and-thoughts": 970_000}),
     "region_weights": RW_GLOBAL},

    {"type": "art", "title": "Goethe's Faust",
     "description": "Goethe's masterwork in two parts; the German Romantic-era tragedy of selling one's soul to Mephistopheles.",
     "start_year": 1808, "end_year": 1832,
     "wikipedia": "https://en.wikipedia.org/wiki/Goethe%27s_Faust",
     "priorities": pri(920_000, germany=930_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Romanticism (movement)"},

    {"type": "art", "title": "Frankenstein",
     "description": "Mary Shelley's gothic novel; written during a wet summer at Lake Geneva with Byron and Percy Shelley; founds science fiction.",
     "start_year": 1818, "start_month": 1, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Frankenstein",
     "priorities": pri(930_000, england=940_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Romanticism (movement)"},

    {"type": "art", "title": "Beethoven's Ninth Symphony",
     "description": "Final completed symphony; choral finale on Schiller's An die Freude; landmark of Romantic music.",
     "start_year": 1824, "start_month": 5, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Symphony_No._9_(Beethoven)",
     "priorities": pri(950_000, germany=940_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Romanticism (movement)"},

    {"type": "art", "title": "Berlioz's Symphonie fantastique",
     "description": "Programme symphony depicting a poet's opium dreams of his beloved; defining work of musical Romanticism.",
     "start_year": 1830, "start_month": 12, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Symphonie_fantastique",
     "priorities": pri(870_000, france=890_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Romanticism (movement)"},

    {"type": "art", "title": "Liberty Leading the People",
     "description": "Delacroix's painting commemorating the July 1830 revolution in France; allegorical Liberty leads citizens over barricades.",
     "start_year": 1830,
     "wikipedia": "https://en.wikipedia.org/wiki/Liberty_Leading_the_People",
     "priorities": pri(900_000, france=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Romanticism (movement)"},

    {"type": "person", "title": "J. M. W. Turner",
     "description": "English Romantic landscape and seascape painter; revolutionised use of colour and light; precursor of Impressionism.",
     "start_year": 1775, "end_year": 1851, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/J._M._W._Turner",
     "priorities": pri(910_000, england=920_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_GLOBAL},

    {"type": "art", "title": "Pride and Prejudice",
     "description": "Jane Austen's most-loved novel; comedy of manners about the Bennet sisters and Mr Darcy; never out of print since 1813.",
     "start_year": 1813, "start_month": 1, "start_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Pride_and_Prejudice",
     "priorities": pri(920_000, england=940_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Romanticism (movement)"},

    # =================================================================
    # COUNTER-REFORMATION
    # =================================================================
    {"type": "event", "title": "Counter-Reformation",
     "description": "Catholic response to the Protestant Reformation; renewal of Catholic doctrine, founding of Jesuits, Roman Inquisition, missionary expansion.",
     "start_year": 1545, "end_year": 1648,
     "wikipedia": "https://en.wikipedia.org/wiki/Counter-Reformation",
     "priorities": pri(940_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Society of Jesus founded",
     "description": "Ignatius of Loyola founds the Jesuits; militant order at the spearhead of Counter-Reformation and Catholic missions worldwide.",
     "start_year": 1540, "start_month": 9, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Society_of_Jesus",
     "priorities": pri(910_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Counter-Reformation"},

    {"type": "person", "title": "Ignatius of Loyola",
     "description": "Basque soldier turned mystic; founded the Society of Jesus; author of the Spiritual Exercises.",
     "start_year": 1491, "end_year": 1556, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ignatius_of_Loyola",
     "priorities": pri(870_000, people=890_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Roman Inquisition established",
     "description": "Pope Paul III sets up a Holy Office of the Inquisition based in Rome to combat heresy; central institution of Counter-Reformation.",
     "start_year": 1542, "start_month": 7, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Roman_Inquisition",
     "priorities": pri(860_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Counter-Reformation"},

    {"type": "event", "title": "Index Librorum Prohibitorum",
     "description": "Catholic list of forbidden books, instituted by Pope Paul IV; updated for four centuries until abolition by Vatican II in 1966.",
     "start_year": 1559,
     "wikipedia": "https://en.wikipedia.org/wiki/Index_Librorum_Prohibitorum",
     "priorities": pri(840_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Counter-Reformation"},

    {"type": "person", "title": "Teresa of Ávila",
     "description": "Spanish mystic; reformer of the Carmelite order; mystical theologian; canonised in 1622; named a Doctor of the Church in 1970.",
     "start_year": 1515, "end_year": 1582, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Teresa_of_%C3%81vila",
     "priorities": pri(870_000, people=890_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_EU},

    {"type": "event", "title": "Jesuit missions in China",
     "description": "Matteo Ricci and successors establish Jesuit presence at the Ming and Qing courts; remarkable cultural exchange in astronomy, mathematics.",
     "start_year": 1582, "end_year": 1773,
     "wikipedia": "https://en.wikipedia.org/wiki/Jesuit_China_missions",
     "priorities": pri(850_000, china=830_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Counter-Reformation"},

    {"type": "event", "title": "Baroque art and architecture",
     "description": "Dramatic, emotionally direct artistic style favoured by Counter-Reformation Church; Bernini, Caravaggio, Rubens; spreads across Catholic Europe.",
     "start_year": 1600, "end_year": 1750,
     "wikipedia": "https://en.wikipedia.org/wiki/Baroque",
     "priorities": pri(900_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Counter-Reformation"},

    {"type": "person", "title": "Caravaggio",
     "description": "Italian Baroque painter; revolutionary use of chiaroscuro and tenebrism; turbulent life ending in early death.",
     "start_year": 1571, "end_year": 1610, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Caravaggio",
     "priorities": pri(910_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_EU},

    # =================================================================
    # AMERICAN REVOLUTION
    # =================================================================
    {"type": "event", "title": "American Revolution",
     "description": "American colonies' war for independence from Britain (1775-1783) and the political revolution that founded the United States.",
     "start_year": 1775, "end_year": 1783,
     "wikipedia": "https://en.wikipedia.org/wiki/American_Revolution",
     "priorities": pri(970_000, usa=970_000),
     "region_weights": RW_AMER},

    {"type": "event", "title": "Stamp Act crisis",
     "description": "British Parliament imposes stamp tax on the colonies; \"no taxation without representation\"; widespread riots; tax repealed in 1766.",
     "start_year": 1765, "start_month": 3, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Stamp_Act_1765",
     "priorities": pri(870_000, usa=900_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "Boston Massacre",
     "description": "British soldiers fire on a Boston crowd; five colonists killed; Paul Revere's engraving inflames colonial opinion.",
     "start_year": 1770, "start_month": 3, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Boston_Massacre",
     "priorities": pri(890_000, usa=920_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "First Continental Congress",
     "description": "Delegates from 12 colonies meet in Philadelphia in response to the Intolerable Acts; lays groundwork for united response to Britain.",
     "start_year": 1774, "start_month": 9, "start_day": 5, "end_month": 10, "end_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Continental_Congress",
     "priorities": pri(870_000, usa=910_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "Battles of Lexington and Concord",
     "description": "First armed engagements of the American Revolution; Paul Revere's ride; \"shot heard round the world\".",
     "start_year": 1775, "start_month": 4, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Battles_of_Lexington_and_Concord",
     "priorities": pri(910_000, usa=940_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "Battle of Bunker Hill",
     "description": "Costly British tactical victory near Boston; \"Don't fire until you see the whites of their eyes\"; emboldens American resistance.",
     "start_year": 1775, "start_month": 6, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Bunker_Hill",
     "priorities": pri(880_000, usa=910_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "art", "title": "Paine's Common Sense",
     "description": "Thomas Paine's pamphlet making the case for American independence; 500,000 copies sold; transforms colonial opinion.",
     "start_year": 1776, "start_month": 1, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Common_Sense_(pamphlet)",
     "priorities": pri(890_000, usa=920_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "Battles of Saratoga",
     "description": "American victory over Burgoyne's army; turning point of the war; persuades France to enter as American ally.",
     "start_year": 1777, "start_month": 9, "start_day": 19, "end_month": 10, "end_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Battles_of_Saratoga",
     "priorities": pri(910_000, usa=930_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "Valley Forge winter",
     "description": "Washington's army winters in Pennsylvania under brutal conditions; emerges trained and disciplined under Steuben's drill.",
     "start_year": 1777, "start_month": 12, "start_day": 19, "end_year": 1778, "end_month": 6, "end_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Valley_Forge",
     "priorities": pri(870_000, usa=910_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "Siege of Yorktown",
     "description": "Combined American-French force under Washington and Rochambeau forces Cornwallis to surrender; effectively ends the Revolutionary War.",
     "start_year": 1781, "start_month": 9, "start_day": 28, "end_month": 10, "end_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Yorktown",
     "priorities": pri(920_000, usa=940_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "Treaty of Paris (1783)",
     "description": "Britain recognises American independence with generous boundaries; ends Revolutionary War.",
     "start_year": 1783, "start_month": 9, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Paris_(1783)",
     "priorities": pri(920_000, usa=940_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "Constitutional Convention (US)",
     "description": "Delegates in Philadelphia draft the US Constitution; replaces the Articles of Confederation with a federal republic.",
     "start_year": 1787, "start_month": 5, "start_day": 25, "end_month": 9, "end_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Constitutional_Convention_(United_States)",
     "priorities": pri(950_000, usa=970_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "Federalist Papers",
     "description": "Hamilton, Madison and Jay anonymously argue for ratification of the Constitution; foundational text of American political theory.",
     "start_year": 1787, "end_year": 1788,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Federalist_Papers",
     "priorities": pri(900_000, usa=930_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    {"type": "event", "title": "US Bill of Rights ratified",
     "description": "First ten amendments to the Constitution guarantee individual rights; bedrock of American constitutional law.",
     "start_year": 1791, "start_month": 12, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/United_States_Bill_of_Rights",
     "priorities": pri(940_000, usa=960_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "American Revolution"},

    # =================================================================
    # RECONQUISTA
    # =================================================================
    {"type": "event", "title": "Reconquista",
     "description": "Christian reconquest of the Iberian peninsula from Muslim rule; 781 years from Covadonga (722) to Granada (1492).",
     "start_year": 722, "end_year": 1492,
     "wikipedia": "https://en.wikipedia.org/wiki/Reconquista",
     "priorities": pri(950_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Al-Andalus / Caliphate of Córdoba",
     "description": "Muslim al-Andalus; Caliphate of Córdoba (929-1031) is one of the great cultural centres of the medieval world.",
     "start_year": 711, "end_year": 1492,
     "wikipedia": "https://en.wikipedia.org/wiki/Al-Andalus",
     "priorities": pri(900_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Tours / Poitiers (732)",
     "description": "Charles Martel halts Umayyad advance; classically (but contestably) seen as saving European Christianity.",
     "start_year": 732,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Tours",
     "priorities": pri(880_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Reconquista"},

    {"type": "event", "title": "Capture of Toledo (1085)",
     "description": "Alfonso VI of León-Castile takes Toledo from the Taifa kingdoms; opens reconquest of central Iberia.",
     "start_year": 1085, "start_month": 5, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Capture_of_Toledo_(1085)",
     "priorities": pri(810_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Reconquista"},

    {"type": "person", "title": "El Cid",
     "description": "Rodrigo Díaz de Vivar; Castilian nobleman; mercenary who served Christian and Muslim lords; subject of the Cantar de mio Cid.",
     "start_year": 1043, "end_year": 1099, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/El_Cid",
     "priorities": pri(880_000, people=890_000),
     "region_weights": RW_EU},

    # =================================================================
    # HOLOCAUST — umbrella exists ("The Holocaust"); add more children
    # =================================================================
    {"type": "event", "title": "Babi Yar massacre",
     "description": "Nazi Einsatzgruppen kill 33,771 Jews in two days in a ravine outside Kyiv; one of the largest single massacres of the Holocaust.",
     "start_year": 1941, "start_month": 9, "start_day": 29, "end_month": 9, "end_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Babi_Yar",
     "priorities": pri(880_000, **{"ww2": 900_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "The Holocaust"},

    {"type": "event", "title": "Treblinka extermination camp",
     "description": "Nazi camp where ~900,000 Jews were murdered in gas chambers; uprising in August 1943; almost no survivors.",
     "start_year": 1942, "start_month": 7, "start_day": 23, "end_year": 1943, "end_month": 10, "end_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Treblinka_extermination_camp",
     "priorities": pri(870_000, **{"ww2": 890_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "The Holocaust"},

    {"type": "event", "title": "Sobibór extermination camp",
     "description": "Nazi camp where ~167,000 Jews were murdered; uprising in October 1943 forced the camp's closure.",
     "start_year": 1942, "start_month": 4, "end_year": 1943, "end_month": 10, "end_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Sobib%C3%B3r_extermination_camp",
     "priorities": pri(860_000, **{"ww2": 880_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "The Holocaust"},

    {"type": "event", "title": "Nazi death marches",
     "description": "As Soviet armies advanced, Nazis forced ~250,000 concentration-camp prisoners on death marches; tens of thousands died.",
     "start_year": 1944, "start_month": 7, "end_year": 1945, "end_month": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Death_marches_(Holocaust)",
     "priorities": pri(870_000, **{"ww2": 880_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "The Holocaust"},

    {"type": "person", "title": "Anne Frank",
     "description": "Jewish teenager who hid with her family in an Amsterdam attic; her diary survived; one of the most read works of Holocaust literature.",
     "start_year": 1929, "end_year": 1945, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Anne_Frank",
     "priorities": pri(960_000, people=960_000),
     "region_weights": RW_GLOBAL},

    {"type": "art", "title": "Anne Frank's Diary",
     "description": "Diary of a young girl hiding from the Nazis in Amsterdam; published 1947; translated into ~70 languages.",
     "start_year": 1947, "start_month": 6, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Diary_of_a_Young_Girl",
     "priorities": pri(950_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "The Holocaust"},

    # =================================================================
    # COVID-19 PANDEMIC — umbrella exists; add deepening children
    # =================================================================
    {"type": "event", "title": "COVID-19 pandemic",
     "description": "Pandemic caused by SARS-CoV-2; first cases in Wuhan late 2019; ~7 million reported deaths globally; ends mass-emergency phase in 2023.",
     "start_year": 2019, "start_month": 12, "end_year": 2023, "end_month": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/COVID-19_pandemic",
     "priorities": pri(960_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Wuhan lockdown",
     "description": "Chinese authorities lock down Wuhan (population 11M) to contain the novel coronavirus outbreak; first lockdown of a major modern city.",
     "start_year": 2020, "start_month": 1, "start_day": 23, "end_month": 4, "end_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/COVID-19_lockdown_in_Wuhan",
     "priorities": pri(900_000, china=900_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "COVID-19 pandemic"},

    {"type": "event", "title": "WHO declares COVID-19 a pandemic",
     "description": "World Health Organization officially designates COVID-19 a pandemic; triggers wave of national lockdowns and emergency measures.",
     "start_year": 2020, "start_month": 3, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/COVID-19_pandemic",
     "priorities": pri(940_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "COVID-19 pandemic"},

    {"type": "event", "title": "First COVID-19 vaccines approved",
     "description": "Pfizer-BioNTech and Moderna mRNA vaccines authorised in late 2020; fastest vaccine development in history.",
     "start_year": 2020, "start_month": 12, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/COVID-19_vaccine",
     "priorities": pri(930_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "COVID-19 pandemic"},

    {"type": "event", "title": "Delta and Omicron variants",
     "description": "Highly transmissible SARS-CoV-2 variants (Delta mid-2021, Omicron late 2021) drive new waves; vaccines retain protection against severe disease.",
     "start_year": 2021, "start_month": 6, "end_year": 2022, "end_month": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Variants_of_SARS-CoV-2",
     "priorities": pri(860_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "COVID-19 pandemic"},
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
