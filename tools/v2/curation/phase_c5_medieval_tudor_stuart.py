"""
Phase C5 — Norman / Plantagenet / Tudor / Stuart England (1100-1700).
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_BRIT = {"europe": 10, "americas": 2, "asia": 2, "australasia": 2, "africa": 2}
RW_BRIT_EU = {"europe": 10, "americas": 3, "asia": 3, "australasia": 2, "africa": 2}


def e(master_pri: int, eng_pri: int, **extra) -> dict:
    out = {"master": master_pri, "england": eng_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- Norman & early Plantagenet -----
    {"type": "event", "title": "White Ship disaster",
     "description": "Henry I's heir William Adelin drowns when the White Ship sinks off Barfleur; succession crisis leads to the Anarchy.",
     "start_year": 1120, "start_month": 11, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/White_Ship",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Murder of Thomas Becket",
     "description": "Four knights kill Archbishop Thomas Becket in Canterbury Cathedral after Henry II's rash words; canonised in 1173.",
     "start_year": 1170, "start_month": 12, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Thomas_Becket",
     "priorities": e(880_000, 920_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Henry II's reforms of English law",
     "description": "Assize of Clarendon (1166) and other measures establish royal travelling justices and trial juries; foundation of common law.",
     "start_year": 1166,
     "wikipedia": "https://en.wikipedia.org/wiki/Henry_II_of_England",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Norman invasion of Ireland",
     "description": "Anglo-Norman lords cross to Ireland at Strongbow's lead; Henry II asserts overlordship; 800 years of intermittent rule begins.",
     "start_year": 1169, "end_year": 1175,
     "wikipedia": "https://en.wikipedia.org/wiki/Norman_invasion_of_Ireland",
     "priorities": e(840_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Richard I and the Third Crusade",
     "description": "Lionheart leads English contingent against Saladin; victories at Acre and Arsuf, no recapture of Jerusalem.",
     "start_year": 1190, "end_year": 1192,
     "wikipedia": "https://en.wikipedia.org/wiki/Third_Crusade",
     "priorities": e(870_000, 910_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "John loses Normandy",
     "description": "Philip II of France seizes Normandy from King John, ending the cross-Channel Angevin Empire.",
     "start_year": 1204,
     "wikipedia": "https://en.wikipedia.org/wiki/King_John,_King_of_England",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Papal interdict on England",
     "description": "Innocent III places England under interdict after John refuses Stephen Langton as Archbishop of Canterbury; lifted after John submits in 1213.",
     "start_year": 1208, "end_year": 1213,
     "wikipedia": "https://en.wikipedia.org/wiki/John,_King_of_England",
     "priorities": e(790_000, 850_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "First Barons' War",
     "description": "Barons rebel against King John, invite Louis of France; ends after John's death with Henry III's coronation.",
     "start_year": 1215, "end_year": 1217,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Barons%27_War",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Second Barons' War",
     "description": "Simon de Montfort leads barons against Henry III; his 1265 parliament includes commoners but he is killed at Evesham.",
     "start_year": 1264, "end_year": 1267,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Barons%27_War",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Model Parliament of Edward I",
     "description": "Edward I summons a representative parliament that includes lords, clergy, knights and burgesses; precedent for later parliaments.",
     "start_year": 1295, "start_month": 11, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Model_Parliament",
     "priorities": e(850_000, 910_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Statute of Wales",
     "description": "Edward I's Statute of Rhuddlan annexes the Principality of Wales to the English Crown.",
     "start_year": 1284, "start_month": 3, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Statute_of_Rhuddlan",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Bannockburn",
     "description": "Robert the Bruce defeats Edward II near Stirling; secures Scottish independence for centuries.",
     "start_year": 1314, "start_month": 6, "start_day": 23, "end_month": 6, "end_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Bannockburn",
     "priorities": e(850_000, 910_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Murder of Edward II",
     "description": "Deposed king allegedly murdered at Berkeley Castle by partisans of Isabella and Mortimer; mode of death legendarily savage.",
     "start_year": 1327, "start_month": 9, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Edward_II_of_England",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    # ----- Hundred Years' War detail -----
    {"type": "event", "title": "Battle of Crécy",
     "description": "Edward III's outnumbered English army crushes French chivalry with the longbow; transformative battle in medieval warfare.",
     "start_year": 1346, "start_month": 8, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Cr%C3%A9cy",
     "priorities": e(870_000, 920_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Siege of Calais",
     "description": "Edward III captures Calais after eleven-month siege; town remains English until 1558.",
     "start_year": 1346, "end_year": 1347,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Calais_(1346%E2%80%931347)",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Battle of Poitiers (1356)",
     "description": "Black Prince captures King John II of France in another disastrous French defeat to the longbow-and-dismounted-men-at-arms tactic.",
     "start_year": 1356, "start_month": 9, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Poitiers",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Treaty of Brétigny",
     "description": "End of first phase of Hundred Years' War; Edward III renounces French crown in exchange for vastly expanded Aquitaine.",
     "start_year": 1360, "start_month": 5, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Br%C3%A9tigny",
     "priorities": e(800_000, 870_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Black Death in England",
     "description": "Bubonic plague reaches England in summer 1348; kills perhaps half the population over the next two years.",
     "start_year": 1348, "end_year": 1350,
     "wikipedia": "https://en.wikipedia.org/wiki/Black_Death_in_England",
     "priorities": e(890_000, 940_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Statute of Labourers",
     "description": "Parliament freezes wages after Black Death labour shortage; resentment helps fuel the Peasants' Revolt of 1381.",
     "start_year": 1351,
     "wikipedia": "https://en.wikipedia.org/wiki/Statute_of_Labourers_1351",
     "priorities": e(790_000, 850_000), "region_weights": RW_BRIT},

    {"type": "art", "title": "Chaucer's Canterbury Tales",
     "description": "Geoffrey Chaucer composes the unfinished Middle English poem-cycle of pilgrim stories; landmark of English literature.",
     "start_year": 1387, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Canterbury_Tales",
     "priorities": e(870_000, 910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_BRIT},

    {"type": "event", "title": "Lollard movement",
     "description": "Followers of John Wycliffe propagate vernacular Bibles and proto-Protestant ideas in 14th- and 15th-century England.",
     "start_year": 1380, "end_year": 1500, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Lollardy",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Henry IV deposes Richard II",
     "description": "Bolingbroke returns from exile, deposes his cousin Richard II at Flint Castle; opens the Lancastrian dynasty.",
     "start_year": 1399, "start_month": 9, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Henry_IV_of_England",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Owain Glyndŵr's revolt",
     "description": "Welsh rising against English rule under Glyndŵr; he holds parliaments and proclaims Welsh independence before defeat.",
     "start_year": 1400, "end_year": 1415,
     "wikipedia": "https://en.wikipedia.org/wiki/Glynd%C5%B5r_Rising",
     "priorities": e(810_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Shrewsbury",
     "description": "Henry IV defeats the Percy rebellion; Henry, Prince of Wales (future Henry V) takes an arrow to the face and survives.",
     "start_year": 1403, "start_month": 7, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Shrewsbury",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Henry V invades France",
     "description": "Renewal of the Hundred Years' War; lands at Harfleur and marches to Calais via Agincourt.",
     "start_year": 1415, "start_month": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Henry_V_of_England",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Treaty of Troyes",
     "description": "Henry V marries Catherine of Valois and is recognised as heir to Charles VI of France; the dual monarchy collapses on his early death.",
     "start_year": 1420, "start_month": 5, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Troyes",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Joan of Arc relieves Orleans",
     "description": "Maid of Orleans turns the war; lifts the English siege of Orleans and crowns Charles VII at Reims.",
     "start_year": 1429, "start_month": 4, "start_day": 29, "end_month": 5, "end_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Orl%C3%A9ans",
     "priorities": e(870_000, 910_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "End of Hundred Years' War (Castillon)",
     "description": "French victory at Castillon; English driven from continental France except for Calais.",
     "start_year": 1453, "start_month": 7, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Castillon",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT_EU},

    # ----- Wars of the Roses + Tudor consolidation -----
    {"type": "event", "title": "First Battle of St Albans",
     "description": "Yorkist victory over Lancastrian forces; conventional start of the Wars of the Roses.",
     "start_year": 1455, "start_month": 5, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Battle_of_St_Albans",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Towton",
     "description": "Largest and bloodiest battle ever fought on English soil; Yorkist victory secures the throne for Edward IV.",
     "start_year": 1461, "start_month": 3, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Towton",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Princes in the Tower",
     "description": "Sons of Edward IV disappear in the Tower of London under uncle Richard III's protection; fate notoriously unresolved.",
     "start_year": 1483, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Princes_in_the_Tower",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Henry VII marries Elizabeth of York",
     "description": "Lancastrian Henry Tudor marries Yorkist heiress; symbolically ends the Wars of the Roses.",
     "start_year": 1486, "start_month": 1, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Elizabeth_of_York",
     "priorities": e(800_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Star Chamber prerogative court",
     "description": "Henry VII strengthens the Court of Star Chamber as a tool of royal justice over over-mighty subjects; later abused by Stuarts.",
     "start_year": 1487, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Star_Chamber",
     "priorities": e(780_000, 850_000), "region_weights": RW_BRIT},

    # ----- Henry VIII / Reformation -----
    {"type": "event", "title": "Cardinal Wolsey at peak",
     "description": "Lord Chancellor Thomas Wolsey effectively governs Henry VIII's England in the 1510s-20s; falls over failure to secure annulment.",
     "start_year": 1515, "end_year": 1529,
     "wikipedia": "https://en.wikipedia.org/wiki/Thomas_Wolsey",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Field of the Cloth of Gold",
     "description": "Lavish summit between Henry VIII and Francis I near Calais; theatrical attempt at Anglo-French alliance.",
     "start_year": 1520, "start_month": 6, "start_day": 7, "end_month": 6, "end_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Field_of_the_Cloth_of_Gold",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Act of Supremacy (1534)",
     "description": "Parliament declares Henry VIII Supreme Head of the Church of England; legislative break with Rome.",
     "start_year": 1534, "start_month": 11, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Acts_of_Supremacy",
     "priorities": e(880_000, 940_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Execution of Thomas More",
     "description": "Henry VIII's former chancellor beheaded on Tower Hill for refusing to swear the oath of supremacy; later canonised.",
     "start_year": 1535, "start_month": 7, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Thomas_More",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Dissolution of the monasteries",
     "description": "Henry VIII suppresses 800+ English and Welsh religious houses; massive transfer of land and art to crown and gentry.",
     "start_year": 1536, "end_year": 1541,
     "wikipedia": "https://en.wikipedia.org/wiki/Dissolution_of_the_Monasteries",
     "priorities": e(880_000, 940_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Pilgrimage of Grace",
     "description": "Massive northern rising against Henry VIII's religious policies; over 30,000 men gather under Robert Aske before brutal suppression.",
     "start_year": 1536, "start_month": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Pilgrimage_of_Grace",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Execution of Anne Boleyn",
     "description": "Henry VIII's second wife beheaded at the Tower on charges of treason and adultery; cleared the way for Jane Seymour.",
     "start_year": 1536, "start_month": 5, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Anne_Boleyn",
     "priorities": e(840_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Acts of Union (Wales, 1536-1543)",
     "description": "Series of acts incorporates Wales into the Kingdom of England with full parliamentary representation; English law and language imposed.",
     "start_year": 1536, "end_year": 1543,
     "wikipedia": "https://en.wikipedia.org/wiki/Laws_in_Wales_Acts_1535_and_1542",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Book of Common Prayer (1549)",
     "description": "Cranmer's vernacular liturgy imposed by Edward VI; doctrinally Protestant; replaces Latin services.",
     "start_year": 1549, "start_month": 6, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Book_of_Common_Prayer",
     "priorities": e(840_000, 890_000, **{"arts-and-thoughts": 870_000}),
     "region_weights": RW_BRIT},

    {"type": "event", "title": "Marian persecutions",
     "description": "Mary I burns nearly 300 Protestants — including Cranmer, Latimer, Ridley — earning the sobriquet 'Bloody Mary'.",
     "start_year": 1555, "end_year": 1558,
     "wikipedia": "https://en.wikipedia.org/wiki/Marian_persecutions",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Loss of Calais",
     "description": "Last English continental possession captured by France during the war on Spain's side; humiliating end of medieval English France.",
     "start_year": 1558, "start_month": 1, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Calais_(1558)",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Elizabethan Religious Settlement",
     "description": "Acts of Supremacy and Uniformity restore Protestant Church of England under Elizabeth I; broad middle path holds for centuries.",
     "start_year": 1559,
     "wikipedia": "https://en.wikipedia.org/wiki/Elizabethan_Religious_Settlement",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Drake circumnavigates the globe",
     "description": "Francis Drake's Golden Hind voyage reaches around the world plundering Spanish ports; second circumnavigation after Magellan.",
     "start_year": 1577, "end_year": 1580, "start_month": 12, "start_day": 13, "end_month": 9, "end_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Francis_Drake",
     "priorities": e(860_000, 910_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Execution of Mary, Queen of Scots",
     "description": "Mary Stuart beheaded at Fotheringhay after years of Catholic plotting; Elizabeth's reluctant signature embarrasses the regime.",
     "start_year": 1587, "start_month": 2, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Mary,_Queen_of_Scots",
     "priorities": e(850_000, 910_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Spanish Armada",
     "description": "Philip II's invasion fleet defeated in the Channel by English ships and storms; emblem of Elizabethan England.",
     "start_year": 1588, "start_month": 7, "end_month": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Spanish_Armada",
     "priorities": e(900_000, 950_000), "region_weights": RW_BRIT_EU},

    {"type": "event", "title": "Globe Theatre opens",
     "description": "Shakespeare's company opens the Globe on the south bank of the Thames; home of his greatest plays.",
     "start_year": 1599,
     "wikipedia": "https://en.wikipedia.org/wiki/Globe_Theatre",
     "priorities": e(870_000, 910_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_BRIT},

    # ----- Stuart England -----
    {"type": "event", "title": "Union of the Crowns",
     "description": "James VI of Scotland succeeds Elizabeth I as James I of England; one monarch, two parliaments.",
     "start_year": 1603, "start_month": 3, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Union_of_the_Crowns",
     "priorities": e(860_000, 920_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Plantation of Ulster",
     "description": "James I confiscates Gaelic Ulster lands and settles Scottish and English Protestants; roots of long sectarian conflict.",
     "start_year": 1609, "end_year": 1625,
     "wikipedia": "https://en.wikipedia.org/wiki/Plantation_of_Ulster",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Mayflower sails to New England",
     "description": "Pilgrim Fathers sail from Plymouth and found Plymouth Colony in Massachusetts; mythic seed of New England.",
     "start_year": 1620, "start_month": 9, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Mayflower",
     "priorities": e(870_000, 920_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Petition of Right",
     "description": "Parliament's statement of subject's rights — no taxation without consent, no arbitrary imprisonment — that Charles I reluctantly accepts.",
     "start_year": 1628, "start_month": 6, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Petition_of_Right",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Personal Rule of Charles I",
     "description": "Charles I governs England for eleven years without parliament; raises ship money and other prerogative taxes that provoke crisis.",
     "start_year": 1629, "end_year": 1640,
     "wikipedia": "https://en.wikipedia.org/wiki/Personal_Rule",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Bishops' Wars",
     "description": "Scottish Covenanters defy Charles I's imposition of an English-style prayer book; humiliating defeats force him to recall parliament.",
     "start_year": 1639, "end_year": 1640,
     "wikipedia": "https://en.wikipedia.org/wiki/Bishops%27_Wars",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Long Parliament",
     "description": "Parliament summoned by Charles I that effectively governs through Civil War, Commonwealth, and Restoration; dissolved 1660.",
     "start_year": 1640, "end_year": 1660, "start_month": 11, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Long_Parliament",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Edgehill",
     "description": "First major battle of the English Civil War; inconclusive clash between royalists and parliamentarians.",
     "start_year": 1642, "start_month": 10, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Edgehill",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Marston Moor",
     "description": "Decisive parliamentarian victory in Yorkshire; Cromwell's Ironsides establish their reputation; royalists lose the north.",
     "start_year": 1644, "start_month": 7, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Marston_Moor",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "New Model Army",
     "description": "Parliament creates a national professional army under Fairfax and Cromwell; wins Naseby and finishes the first civil war.",
     "start_year": 1645, "start_month": 2, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/New_Model_Army",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Naseby",
     "description": "Cromwell's New Model Army destroys the main royalist army; effective end of the first English Civil War.",
     "start_year": 1645, "start_month": 6, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Naseby",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Execution of Charles I",
     "description": "King beheaded outside the Banqueting House at Whitehall after Rump Parliament trial; only English monarch executed.",
     "start_year": 1649, "start_month": 1, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Execution_of_Charles_I",
     "priorities": e(910_000, 950_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Commonwealth of England",
     "description": "Republican government replaces the monarchy under the Rump Parliament and Cromwell; lasts until Restoration in 1660.",
     "start_year": 1649, "end_year": 1660,
     "wikipedia": "https://en.wikipedia.org/wiki/Commonwealth_of_England",
     "priorities": e(870_000, 920_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Cromwell's Protectorate",
     "description": "Oliver Cromwell becomes Lord Protector under the Instrument of Government; rules from 1653 until his death in 1658.",
     "start_year": 1653, "end_year": 1659, "start_month": 12, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/The_Protectorate",
     "priorities": e(860_000, 920_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Restoration of Charles II",
     "description": "Charles II returns from exile; monarchy, House of Lords and Church of England restored after the Cromwellian republic.",
     "start_year": 1660, "start_month": 5, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Restoration_(England)",
     "priorities": e(880_000, 930_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Pepys' diary kept",
     "description": "Samuel Pepys writes the diary that becomes the great record of Restoration London — including the Great Plague and Fire.",
     "start_year": 1660, "end_year": 1669,
     "wikipedia": "https://en.wikipedia.org/wiki/Samuel_Pepys",
     "priorities": e(830_000, 890_000, **{"arts-and-thoughts": 870_000}),
     "region_weights": RW_BRIT},

    {"type": "event", "title": "Act of Uniformity 1662",
     "description": "Parliament mandates use of the new Book of Common Prayer; 2,000 dissenting ministers ejected from the Church of England.",
     "start_year": 1662, "start_month": 8, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Act_of_Uniformity_1662",
     "priorities": e(790_000, 850_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Test Acts",
     "description": "Series of acts excluding Catholics (and later non-Anglicans generally) from office in England; not fully repealed until 1828.",
     "start_year": 1673,
     "wikipedia": "https://en.wikipedia.org/wiki/Test_Acts",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Popish Plot",
     "description": "Titus Oates's fabricated tale of a Catholic plot against Charles II provokes a wave of executions and the Exclusion Crisis.",
     "start_year": 1678,
     "wikipedia": "https://en.wikipedia.org/wiki/Popish_Plot",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Habeas Corpus Act 1679",
     "description": "Statute against arbitrary imprisonment; standard against which later detention laws are measured.",
     "start_year": 1679, "start_month": 5, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Habeas_Corpus_Act_1679",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Monmouth Rebellion",
     "description": "Charles II's illegitimate Protestant son lands in Lyme Regis, is defeated at Sedgemoor and beheaded; precedes the Glorious Revolution.",
     "start_year": 1685, "start_month": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Monmouth_Rebellion",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Bloody Assizes",
     "description": "Judge George Jeffreys hangs hundreds of Monmouth rebels; sets seal on James II's reputation for despotism.",
     "start_year": 1685, "start_month": 8, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Bloody_Assizes",
     "priorities": e(790_000, 850_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Glorious Revolution",
     "description": "William of Orange invades; James II flees; Parliament invites William and Mary to rule under conditions that limit royal power.",
     "start_year": 1688, "end_year": 1689, "start_month": 11, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Glorious_Revolution",
     "priorities": e(910_000, 950_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of the Boyne",
     "description": "William III defeats James II's Catholic Irish-French army in Ireland; consolidates Protestant ascendancy.",
     "start_year": 1690, "start_month": 7, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Boyne",
     "priorities": e(860_000, 910_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Act of Settlement 1701",
     "description": "Statute restricting throne to Protestant heirs of Sophia of Hanover; sets up the Hanoverian succession of 1714.",
     "start_year": 1701, "start_month": 6, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Act_of_Settlement_1701",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},
]


def main() -> int:
    base = next_available_id()
    for i, e in enumerate(ENTRIES):
        e["id"] = base + i
    n = append_entries(ENTRIES)
    print(f"Appended {n} entries (IDs {base}..{base+n-1}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
