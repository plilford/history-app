"""
Phase G1 — Children for mid-priority European and American umbrellas with
few existing children.

Targets:
  Haitian Revolution (~8)
  French Revolution depth (~12)
  Wars of the Roses (~10)
  Anglo-Saxon settlement (~6)
  English Reformation (~5)
  Suffragette movement (~6)
  Italian unification / Risorgimento (~6)
  War of the Spanish Succession (~6)
  Spanish Civil War context (~4)
  Greek / Russian / Spanish revolutions of the long 19th century (~8)
  Troubles in Northern Ireland (~5)
  Columbian Exchange / age of exploration (~10)
  Crusades main umbrella direct refs (~4)
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_EU = {"europe": 10, "americas": 3, "asia": 3, "australasia": 1, "africa": 3}
RW_AMER = {"europe": 4, "americas": 10, "asia": 1, "australasia": 1, "africa": 3}
RW_GLOBAL = {"europe": 8, "americas": 7, "asia": 5, "australasia": 3, "africa": 4}


def pri(master: int, **extras) -> dict:
    return {"master": master, **extras}


ENTRIES = [
    # ----- Haitian Revolution (~8) -----
    {"type": "person", "title": "Toussaint Louverture",
     "description": "Self-educated former slave; led the Haitian Revolution; betrayed by Napoleon; died in a French prison.",
     "start_year": 1743, "end_year": 1803, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Toussaint_Louverture",
     "priorities": pri(900_000, people=910_000),
     "region_weights": RW_AMER},

    {"type": "event", "title": "Boukman's Vodou ceremony at Bois Caïman",
     "description": "Houngan priest Boukman leads a ceremony in northern Haiti where slaves swear to rise; conventional trigger for the Haitian Revolution.",
     "start_year": 1791, "start_month": 8, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Bois_Ca%C3%AFman",
     "priorities": pri(840_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "Haitian Revolution"},

    {"type": "event", "title": "Saint-Domingue slave uprising begins",
     "description": "Mass slave uprising in northern Saint-Domingue; tens of thousands rise; French colonial society shaken.",
     "start_year": 1791, "start_month": 8, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Haitian_Revolution",
     "priorities": pri(880_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "Haitian Revolution"},

    {"type": "event", "title": "French abolition of slavery (1794)",
     "description": "National Convention abolishes slavery in all French territories; Toussaint Louverture switches from Spanish to French allegiance.",
     "start_year": 1794, "start_month": 2, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Law_of_4_February_1794",
     "priorities": pri(880_000, france=890_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Haitian Revolution"},

    {"type": "event", "title": "Leclerc expedition to Saint-Domingue",
     "description": "Napoleon sends his brother-in-law General Leclerc with 30,000 troops to reassert French rule and restore slavery; ravaged by yellow fever.",
     "start_year": 1802, "end_year": 1803,
     "wikipedia": "https://en.wikipedia.org/wiki/Saint-Domingue_expedition",
     "priorities": pri(830_000, france=820_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "Haitian Revolution"},

    {"type": "event", "title": "Battle of Vertières",
     "description": "Decisive Haitian victory under Dessalines over French forces; opens the path to formal independence two months later.",
     "start_year": 1803, "start_month": 11, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Verti%C3%A8res",
     "priorities": pri(870_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "Haitian Revolution"},

    {"type": "event", "title": "Haitian Declaration of Independence",
     "description": "Jean-Jacques Dessalines proclaims independence at Gonaïves; first independent state in Latin America; first Black-led republic.",
     "start_year": 1804, "start_month": 1, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Haitian_Declaration_of_Independence",
     "priorities": pri(910_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "Haitian Revolution"},

    {"type": "person", "title": "Jean-Jacques Dessalines",
     "description": "Toussaint's general and successor; declared Haitian independence; became first Emperor of Haiti before assassination.",
     "start_year": 1758, "end_year": 1806, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Jean-Jacques_Dessalines",
     "priorities": pri(840_000, people=870_000),
     "region_weights": RW_AMER},

    # ----- French Revolution depth (~12) -----
    {"type": "event", "title": "Estates-General of 1789 convoked",
     "description": "Louis XVI summons the Estates-General at Versailles for the first time since 1614; triggers the constitutional crisis.",
     "start_year": 1789, "start_month": 5, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Estates_General_of_1789",
     "priorities": pri(890_000, france=920_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "Tennis Court Oath",
     "description": "Third Estate, locked out of their hall, swears on a tennis court not to disband until France has a constitution.",
     "start_year": 1789, "start_month": 6, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Tennis_Court_Oath",
     "priorities": pri(900_000, france=920_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "Women's March on Versailles",
     "description": "Crowds of Parisian women march to Versailles and force the royal family to move to Paris; royal authority effectively ends.",
     "start_year": 1789, "start_month": 10, "start_day": 5, "end_month": 10, "end_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Women%27s_March_on_Versailles",
     "priorities": pri(860_000, france=890_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "Civil Constitution of the Clergy",
     "description": "Assembly subordinates the Catholic Church in France to the state; clergy must swear loyalty oath; splits the nation.",
     "start_year": 1790, "start_month": 7, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Civil_Constitution_of_the_Clergy",
     "priorities": pri(830_000, france=870_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "Flight to Varennes",
     "description": "Royal family disguised in coach flees Paris; recognised and arrested at Varennes; collapses public faith in constitutional monarchy.",
     "start_year": 1791, "start_month": 6, "start_day": 20, "end_month": 6, "end_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Flight_to_Varennes",
     "priorities": pri(880_000, france=910_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "Storming of the Tuileries",
     "description": "Sans-culottes and provincial fédérés storm the royal palace; Swiss Guards slaughtered; monarchy effectively over.",
     "start_year": 1792, "start_month": 8, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Insurrection_of_10_August_1792",
     "priorities": pri(870_000, france=900_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "September Massacres",
     "description": "Mobs slaughter ~1,200 prisoners in Paris jails over five days; foreshadows the Terror.",
     "start_year": 1792, "start_month": 9, "start_day": 2, "end_month": 9, "end_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/September_Massacres",
     "priorities": pri(840_000, france=870_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "Execution of Louis XVI",
     "description": "Citizen Louis Capet beheaded in the Place de la Révolution after the National Convention narrowly votes for death.",
     "start_year": 1793, "start_month": 1, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Execution_of_Louis_XVI",
     "priorities": pri(940_000, france=960_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "Reign of Terror",
     "description": "Robespierre and the Committee of Public Safety unleash mass executions to 'save the Revolution'; ~17,000 guillotined.",
     "start_year": 1793, "start_month": 9, "start_day": 5, "end_year": 1794, "end_month": 7, "end_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Reign_of_Terror",
     "priorities": pri(940_000, france=960_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "Execution of Marie Antoinette",
     "description": "The former queen, tried for treason, is guillotined nine months after her husband.",
     "start_year": 1793, "start_month": 10, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Marie_Antoinette",
     "priorities": pri(900_000, france=930_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Reign of Terror"},

    {"type": "event", "title": "Vendée uprising",
     "description": "Royalist Catholic counter-revolution in western France; brutally repressed; estimated 150-200,000 deaths.",
     "start_year": 1793, "end_year": 1796,
     "wikipedia": "https://en.wikipedia.org/wiki/War_in_the_Vend%C3%A9e",
     "priorities": pri(870_000, france=900_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "Thermidorian Reaction",
     "description": "Robespierre and his allies arrested and guillotined; ends the Reign of Terror; ushers in conservative Directory.",
     "start_year": 1794, "start_month": 7, "start_day": 27, "end_month": 7, "end_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Thermidorian_Reaction",
     "priorities": pri(900_000, france=930_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    {"type": "event", "title": "French Directory",
     "description": "Five-man executive governs France from 1795-99; unstable, scandal-ridden; ends in Bonaparte's coup of Brumaire.",
     "start_year": 1795, "end_year": 1799,
     "wikipedia": "https://en.wikipedia.org/wiki/French_Directory",
     "priorities": pri(870_000, france=910_000),
     "region_weights": RW_EU,
     "first_zoom_out": "French Revolution"},

    # ----- Wars of the Roses (~10) -----
    {"type": "event", "title": "Battle of Wakefield",
     "description": "Lancastrians kill Richard, Duke of York; his head exhibited on Micklegate Bar wearing a paper crown.",
     "start_year": 1460, "start_month": 12, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Wakefield",
     "priorities": pri(800_000, england=840_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Wars of the Roses"},

    {"type": "event", "title": "Battle of Mortimer's Cross",
     "description": "Edward, Earl of March (future Edward IV) defeats Lancastrian forces in Herefordshire; opens his path to the throne.",
     "start_year": 1461, "start_month": 2, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Mortimer%27s_Cross",
     "priorities": pri(770_000, england=820_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Wars of the Roses"},

    {"type": "event", "title": "Battle of Barnet",
     "description": "Edward IV defeats and kills Warwick the Kingmaker; eliminates the most dangerous noble in England.",
     "start_year": 1471, "start_month": 4, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Barnet",
     "priorities": pri(800_000, england=850_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Wars of the Roses"},

    {"type": "person", "title": "Margaret of Anjou",
     "description": "Queen of Henry VI; effective leader of the Lancastrian cause through the Wars of the Roses; defeated and ransomed in 1475.",
     "start_year": 1430, "end_year": 1482, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Margaret_of_Anjou",
     "priorities": pri(840_000, england=880_000, people=860_000),
     "region_weights": RW_EU},

    {"type": "person", "title": "Warwick the Kingmaker",
     "description": "Richard Neville, Earl of Warwick; central player in the Wars of the Roses; deposed Henry VI for Edward IV then switched sides.",
     "start_year": 1428, "end_year": 1471, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Richard_Neville,_16th_Earl_of_Warwick",
     "priorities": pri(840_000, england=890_000, people=860_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Stoke Field",
     "description": "Henry VII defeats Yorkist pretender Lambert Simnel; conventional end of the Wars of the Roses; last battle on English soil for centuries.",
     "start_year": 1487, "start_month": 6, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Stoke_Field",
     "priorities": pri(800_000, england=840_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Wars of the Roses"},

    {"type": "event", "title": "Perkin Warbeck pretender plot",
     "description": "Yorkist pretender claiming to be Richard, Duke of York; supported by foreign monarchs; finally executed in 1499.",
     "start_year": 1490, "end_year": 1499,
     "wikipedia": "https://en.wikipedia.org/wiki/Perkin_Warbeck",
     "priorities": pri(770_000, england=830_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Wars of the Roses"},

    {"type": "event", "title": "Battle of Tewkesbury",
     "description": "Edward IV crushes the Lancastrians; Edward of Westminster killed; Henry VI murdered in the Tower of London weeks later.",
     "start_year": 1471, "start_month": 5, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Tewkesbury",
     "priorities": pri(810_000, england=860_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Wars of the Roses"},

    # ----- Anglo-Saxon settlement (~6) -----
    {"type": "person", "title": "Vortigern",
     "description": "Legendary 5th-century British king who invited Saxon mercenaries; subject of Gildas's denunciation; semi-historical figure.",
     "start_year": 425, "end_year": 460, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Vortigern",
     "priorities": pri(800_000, england=860_000, people=830_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Deorham",
     "description": "West Saxon victory over British kings; cuts the Britons of the south-west off from those in Wales.",
     "start_year": 577, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Deorham",
     "priorities": pri(770_000, england=830_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Anglo-Saxon settlement of Britain"},

    {"type": "event", "title": "Conversion of King Æthelberht of Kent",
     "description": "First Anglo-Saxon king to convert to Christianity, baptised by Augustine of Canterbury; starts Kentish Christianity.",
     "start_year": 601, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/%C3%86thelberht_of_Kent",
     "priorities": pri(800_000, england=860_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Anglo-Saxon settlement of Britain"},

    {"type": "event", "title": "Synod of Whitby",
     "description": "Northumbrian church chooses the Roman over the Celtic dating of Easter; aligns English Christianity with Rome.",
     "start_year": 664,
     "wikipedia": "https://en.wikipedia.org/wiki/Synod_of_Whitby",
     "priorities": pri(820_000, england=870_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Anglo-Saxon settlement of Britain"},

    {"type": "event", "title": "Mercian supremacy",
     "description": "Kings of Mercia (Penda, Æthelbald, Offa) dominate Anglo-Saxon England for ~150 years before Wessex's rise under Egbert.",
     "start_year": 626, "end_year": 825, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mercian_Supremacy",
     "priorities": pri(800_000, england=850_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Anglo-Saxon settlement of Britain"},

    {"type": "event", "title": "Reign of Egbert of Wessex",
     "description": "Wessex king who defeated Mercia at Ellandun; West Saxon hegemony over southern England; styled Bretwalda.",
     "start_year": 802, "end_year": 839,
     "wikipedia": "https://en.wikipedia.org/wiki/Egbert,_King_of_Wessex",
     "priorities": pri(800_000, england=850_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Anglo-Saxon settlement of Britain"},

    # ----- English Reformation (~5) -----
    {"type": "person", "title": "Thomas Cranmer",
     "description": "First Protestant Archbishop of Canterbury; principal author of the Book of Common Prayer; burned at the stake under Mary I.",
     "start_year": 1489, "end_year": 1556, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Thomas_Cranmer",
     "priorities": pri(890_000, england=920_000, people=910_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Act in Restraint of Appeals",
     "description": "Bars appeals to Rome from English courts; legal pivot of Henry VIII's break with Rome; declares England a sovereign empire.",
     "start_year": 1533,
     "wikipedia": "https://en.wikipedia.org/wiki/Statute_in_Restraint_of_Appeals",
     "priorities": pri(840_000, england=890_000),
     "region_weights": RW_EU,
     "first_zoom_out": "English Reformation"},

    {"type": "event", "title": "Annulment of Henry VIII's marriage to Catherine of Aragon",
     "description": "Archbishop Cranmer's court declares the marriage void; clears the way for Henry to marry Anne Boleyn.",
     "start_year": 1533, "start_month": 5, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Annulment_of_the_marriage_of_Catherine_of_Aragon",
     "priorities": pri(880_000, england=910_000),
     "region_weights": RW_EU,
     "first_zoom_out": "English Reformation"},

    {"type": "event", "title": "Burning of Latimer and Ridley",
     "description": "Bishops Hugh Latimer and Nicholas Ridley burned at Oxford under Mary I; \"play the man, Master Ridley\".",
     "start_year": 1555, "start_month": 10, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Hugh_Latimer",
     "priorities": pri(830_000, england=870_000),
     "region_weights": RW_EU,
     "first_zoom_out": "English Reformation"},

    {"type": "event", "title": "King James Bible",
     "description": "Authorised English translation commissioned by James I; pinnacle of English religious literature; standard for 300 years.",
     "start_year": 1611,
     "wikipedia": "https://en.wikipedia.org/wiki/King_James_Version",
     "priorities": pri(940_000, england=950_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_EU},

    # ----- Suffragette movement (~6) -----
    {"type": "event", "title": "Black Friday (suffragette)",
     "description": "Police violently dispersed a delegation of suffragettes outside the Commons; 200 women assaulted; radicalises the movement.",
     "start_year": 1910, "start_month": 11, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Black_Friday_(1910)",
     "priorities": pri(810_000, england=860_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Suffragette movement intensifies"},

    {"type": "event", "title": "Suffragette window-smashing campaign",
     "description": "Mass coordinated breaking of West End shop windows by suffragettes; Mrs Pankhurst arrested.",
     "start_year": 1912, "start_month": 3, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Suffragette",
     "priorities": pri(800_000, england=850_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Suffragette movement intensifies"},

    {"type": "event", "title": "Cat and Mouse Act",
     "description": "Allows release of hunger-striking suffragettes when ill, with re-arrest on recovery; designed to avoid martyr deaths.",
     "start_year": 1913, "start_month": 4, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Prisoners_(Temporary_Discharge_for_Ill_Health)_Act_1913",
     "priorities": pri(800_000, england=850_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Suffragette movement intensifies"},

    {"type": "event", "title": "Death of Emily Davison at the Derby",
     "description": "Suffragette throws herself in front of the King's horse at Epsom Derby; dies of injuries; becomes the movement's martyr.",
     "start_year": 1913, "start_month": 6, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Emily_Davison",
     "priorities": pri(860_000, england=890_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Suffragette movement intensifies"},

    {"type": "person", "title": "Emmeline Pankhurst",
     "description": "Founder of the WSPU and the militant wing of British suffragism; her tactics shifted the women's vote campaign.",
     "start_year": 1858, "end_year": 1928, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Emmeline_Pankhurst",
     "priorities": pri(900_000, england=920_000, people=920_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "US women win the vote (19th Amendment)",
     "description": "Constitutional amendment grants American women the right to vote; ratified after a 72-year suffrage campaign.",
     "start_year": 1920, "start_month": 8, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Nineteenth_Amendment_to_the_United_States_Constitution",
     "priorities": pri(910_000, usa=940_000),
     "region_weights": RW_AMER},

    # ----- Italian unification (~6) -----
    {"type": "person", "title": "Giuseppe Garibaldi",
     "description": "Romantic-revolutionary general; led the Expedition of the Thousand that took Sicily and Naples; godfather of Italian unification.",
     "start_year": 1807, "end_year": 1882, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Giuseppe_Garibaldi",
     "priorities": pri(900_000, people=920_000),
     "region_weights": RW_EU},

    {"type": "person", "title": "Camillo Benso, Count of Cavour",
     "description": "Piedmontese statesman; architect of Italian unification by realpolitik; played the great powers off each other.",
     "start_year": 1810, "end_year": 1861, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Camillo_Benso,_Count_of_Cavour",
     "priorities": pri(880_000, people=900_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Expedition of the Thousand",
     "description": "Garibaldi's red-shirts conquer Sicily and Naples for the Italian crown; classic moment of 19th-century nationalism.",
     "start_year": 1860, "start_month": 5, "start_day": 11, "end_month": 11, "end_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Expedition_of_the_Thousand",
     "priorities": pri(870_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Italian unification (Risorgimento)"},

    {"type": "event", "title": "Kingdom of Italy proclaimed",
     "description": "Vittorio Emanuele II proclaimed King of Italy; first unified state on the peninsula since the Roman empire (Venice and Rome added later).",
     "start_year": 1861, "start_month": 3, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Italian_unification",
     "priorities": pri(900_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Italian unification (Risorgimento)"},

    {"type": "event", "title": "Capture of Rome (1870)",
     "description": "Italian troops breach the Aurelian walls at Porta Pia; ends Papal States and the temporal power of the Popes.",
     "start_year": 1870, "start_month": 9, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Capture_of_Rome",
     "priorities": pri(880_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Italian unification (Risorgimento)"},

    {"type": "event", "title": "Mille e Garibaldi land at Marsala",
     "description": "Garibaldi's expedition lands in Sicily; Bourbon defenders melt away; opens the conquest of the south.",
     "start_year": 1860, "start_month": 5, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Expedition_of_the_Thousand",
     "priorities": pri(780_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Expedition of the Thousand"},

    # ----- War of the Spanish Succession (~6) -----
    {"type": "event", "title": "Battle of Blenheim",
     "description": "Marlborough and Eugene of Savoy crush the Franco-Bavarian army on the Danube; saves Vienna and turns the war.",
     "start_year": 1704, "start_month": 8, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Blenheim",
     "priorities": pri(870_000, england=890_000, france=820_000),
     "region_weights": RW_EU,
     "first_zoom_out": "War of the Spanish Succession"},

    {"type": "event", "title": "Battle of Ramillies",
     "description": "Marlborough crushes the French at Ramillies in the Spanish Netherlands; opens the Low Countries to allied forces.",
     "start_year": 1706, "start_month": 5, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Ramillies",
     "priorities": pri(800_000, england=850_000),
     "region_weights": RW_EU,
     "first_zoom_out": "War of the Spanish Succession"},

    {"type": "event", "title": "Battle of Oudenarde",
     "description": "Marlborough and Eugene defeat the French at Oudenarde; further French setback in the Spanish Netherlands.",
     "start_year": 1708, "start_month": 7, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Oudenarde",
     "priorities": pri(770_000, england=820_000),
     "region_weights": RW_EU,
     "first_zoom_out": "War of the Spanish Succession"},

    {"type": "event", "title": "Battle of Malplaquet",
     "description": "Bloodiest battle of the war; Marlborough's allies suffer heavier casualties than the French; political backlash in Britain.",
     "start_year": 1709, "start_month": 9, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Malplaquet",
     "priorities": pri(800_000, england=830_000),
     "region_weights": RW_EU,
     "first_zoom_out": "War of the Spanish Succession"},

    {"type": "event", "title": "Treaty of Utrecht",
     "description": "Major peace settlement ending the War of the Spanish Succession; cements British naval and commercial supremacy.",
     "start_year": 1713, "start_month": 4, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Utrecht",
     "priorities": pri(890_000, england=900_000),
     "region_weights": RW_EU,
     "first_zoom_out": "War of the Spanish Succession"},

    {"type": "person", "title": "Duke of Marlborough",
     "description": "John Churchill, 1st Duke; greatest British general of his age; victories at Blenheim, Ramillies, Oudenarde, Malplaquet.",
     "start_year": 1650, "end_year": 1722, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/John_Churchill,_1st_Duke_of_Marlborough",
     "priorities": pri(880_000, england=900_000, people=900_000),
     "region_weights": RW_EU},

    # ----- Troubles in Northern Ireland (~5) -----
    {"type": "event", "title": "Operation Demetrius (internment)",
     "description": "British army interns hundreds of suspected republicans without trial; alienates Catholic population and intensifies the Troubles.",
     "start_year": 1971, "start_month": 8, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Operation_Demetrius",
     "priorities": pri(820_000, england=850_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Troubles in Northern Ireland begin"},

    {"type": "event", "title": "1981 Irish hunger strike",
     "description": "IRA and INLA prisoners strike for political status in Long Kesh; Bobby Sands dies after 66 days; 10 strikers die total.",
     "start_year": 1981, "start_month": 3, "start_day": 1, "end_month": 10, "end_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/1981_Irish_hunger_strike",
     "priorities": pri(880_000, england=890_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Troubles in Northern Ireland begin"},

    {"type": "event", "title": "Brighton hotel bombing",
     "description": "Provisional IRA bomb at the Grand Hotel during Conservative Party conference targets Margaret Thatcher; she escapes; five killed.",
     "start_year": 1984, "start_month": 10, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Brighton_hotel_bombing",
     "priorities": pri(870_000, england=890_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Troubles in Northern Ireland begin"},

    {"type": "event", "title": "Omagh bombing",
     "description": "Real IRA car bomb kills 29 in Omagh; deadliest single incident of the Troubles; turns public opinion decisively against violence.",
     "start_year": 1998, "start_month": 8, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Omagh_bombing",
     "priorities": pri(860_000, england=880_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Troubles in Northern Ireland begin"},

    {"type": "event", "title": "Anglo-Irish Agreement",
     "description": "Hillsborough agreement gives the Republic a consultative role in Northern Ireland's affairs; Unionist outrage but a path forward.",
     "start_year": 1985, "start_month": 11, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Anglo-Irish_Agreement",
     "priorities": pri(830_000, england=860_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Troubles in Northern Ireland begin"},

    # ----- Columbian Exchange / age of exploration (~10) -----
    {"type": "event", "title": "Vasco da Gama reaches India",
     "description": "Portuguese fleet arrives at Calicut; opens direct European sea route to Asian spices.",
     "start_year": 1498, "start_month": 5, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Vasco_da_Gama",
     "priorities": pri(910_000, india=860_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Magellan-Elcano circumnavigation",
     "description": "Ferdinand Magellan's fleet, completed by Juan Sebastián Elcano, sails around the world; first circumnavigation.",
     "start_year": 1519, "end_year": 1522,
     "wikipedia": "https://en.wikipedia.org/wiki/Magellan_expedition",
     "priorities": pri(930_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Potatoes reach Europe",
     "description": "Andean potato spreads from Spain to Ireland, then northern Europe; transforms agriculture, fuels population growth.",
     "start_year": 1570, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/History_of_the_potato",
     "priorities": pri(880_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Columbian Exchange"},

    {"type": "event", "title": "Tomato reaches Europe",
     "description": "South American tomato spreads from Mexico via Spain; initially distrusted as poisonous, eventually transforms Mediterranean cooking.",
     "start_year": 1540, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tomato",
     "priorities": pri(800_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Columbian Exchange"},

    {"type": "event", "title": "Horse reintroduced to the Americas",
     "description": "Spanish horses reach the Americas with Columbus and Cortés; spreads to Plains peoples by 17th century; transforms North American societies.",
     "start_year": 1493, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Horses_in_the_New_World",
     "priorities": pri(870_000, usa=860_000),
     "region_weights": RW_AMER,
     "first_zoom_out": "Columbian Exchange"},

    {"type": "event", "title": "Sugar plantations in the Caribbean",
     "description": "Brazilian model exported to English and French Caribbean; demand drives transatlantic slave trade; transforms world economy.",
     "start_year": 1640, "end_year": 1750, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Sugarcane#History",
     "priorities": pri(890_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Columbian Exchange"},

    {"type": "event", "title": "Syphilis epidemic in Europe",
     "description": "Disease emerges in Europe shortly after Columbus's return; possibly an American import; sweeps across the continent.",
     "start_year": 1495, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/History_of_syphilis",
     "priorities": pri(840_000),
     "region_weights": RW_GLOBAL,
     "first_zoom_out": "Columbian Exchange"},

    {"type": "event", "title": "Treaty of Saragossa",
     "description": "Spain and Portugal partition the Pacific; complements Tordesillas; resolves dispute over the Moluccas.",
     "start_year": 1529, "start_month": 4, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Zaragoza",
     "priorities": pri(810_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Manila galleon trade",
     "description": "Annual Spanish galleons link Manila and Acapulco; pumps American silver into China for two and a half centuries.",
     "start_year": 1565, "end_year": 1815,
     "wikipedia": "https://en.wikipedia.org/wiki/Manila_galleon",
     "priorities": pri(870_000),
     "region_weights": RW_GLOBAL},

    {"type": "event", "title": "Dutch East India Company chartered",
     "description": "VOC founded with extraordinary state-backed monopoly powers; first multinational joint-stock corporation; dominates Asia trade for 200 years.",
     "start_year": 1602, "start_month": 3, "start_day": 20,
     "wikipedia": "https://en.wikipedia.org/wiki/Dutch_East_India_Company",
     "priorities": pri(910_000),
     "region_weights": RW_GLOBAL},

    # ----- Direct refs to Crusades umbrella (~4) -----
    {"type": "event", "title": "Mongol-Mamluk alliance against Crusader states",
     "description": "Briefly, Mongol Ilkhanate and Christian Cilicia ally to crush Mamluks; alliance fails; Mamluk power consolidated.",
     "start_year": 1260, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Franco-Mongol_alliance",
     "priorities": pri(760_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Crusades"},

    {"type": "event", "title": "Pope Urban II proclaims indulgences for Crusaders",
     "description": "Foundation of crusading theology: full remission of sins for those who fight in the Holy Land.",
     "start_year": 1095, "start_month": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Indulgence",
     "priorities": pri(820_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Crusades"},

    {"type": "event", "title": "Crusader siege of Damascus (1148)",
     "description": "Mid-Second Crusade siege ends in failure after four days; emblematic of crusading military shortcomings.",
     "start_year": 1148, "start_month": 7, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Damascus_(1148)",
     "priorities": pri(770_000),
     "region_weights": RW_EU,
     "first_zoom_out": "Second Crusade"},

    {"type": "event", "title": "Massacre of the Latins (Constantinople 1182)",
     "description": "Anti-Latin rioters massacre Roman-Catholic residents of Constantinople; deepens Greek-Latin estrangement.",
     "start_year": 1182, "start_month": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Massacre_of_the_Latins",
     "priorities": pri(770_000, **{"roman-history": 800_000}),
     "region_weights": RW_EU,
     "first_zoom_out": "Crusades"},
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
