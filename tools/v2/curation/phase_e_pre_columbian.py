"""
Phase E3 — Pre-Columbian Americas timeline. New slug 'pre-columbian-americas'.

Scope: from Paleo-Indian peopling through Spanish conquests of the 16th
century. Covers all three culture areas: North American (Clovis, Mound
Builders, Mississippian, Puebloan, Iroquois), Mesoamerican (Olmec, Maya,
Toltec, Aztec), and Andean (Caral-Supe, Chavín, Moche, Wari, Tiwanaku,
Chimu, Inca). North American entries are dual-tagged on `usa` per request.
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_AMER = {"europe": 1, "americas": 10, "asia": 1, "australasia": 1, "africa": 1}


def p(master_pri: int, pca_pri: int | None = None, **extra) -> dict:
    if pca_pri is None:
        pca_pri = min(999_000, master_pri + 30_000)
    out = {"master": master_pri, "pre-columbian-americas": pca_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- Peopling of the Americas -----
    {"type": "event", "title": "Peopling of the Americas",
     "description": "Paleo-Indians cross Beringia and spread south; oldest secure sites date to at least 16,000 BP.",
     "start_year": -14000, "end_year": -10000, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Settlement_of_the_Americas",
     "priorities": p(890_000, usa=900_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Clovis culture",
     "description": "Paleo-Indian big-game hunters across North America; distinctive fluted spear points; rapid spread c. 13,000 BP.",
     "start_year": -11000, "end_year": -10800, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Clovis_culture",
     "priorities": p(870_000, usa=890_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Folsom culture",
     "description": "Successor to Clovis; bison-hunting Paleo-Indian culture across the Great Plains; finer fluted points.",
     "start_year": -10500, "end_year": -8500, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Folsom_tradition",
     "priorities": p(800_000, usa=830_000), "region_weights": RW_AMER},

    # ----- Mesoamerica earliest civilisations -----
    {"type": "event", "title": "Maize domestication",
     "description": "Wild teosinte gradually selected into modern maize in the Balsas River valley of Mexico; foundation crop of all Mesoamerican civilisation.",
     "start_year": -7000, "end_year": -5000, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Maize",
     "priorities": p(900_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Caral-Supe civilisation",
     "description": "One of the world's earliest urban societies, on the Peruvian coast; monumental architecture without ceramics or maize.",
     "start_year": -3500, "end_year": -1800, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Caral%E2%80%93Supe_civilization",
     "priorities": p(880_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Olmec civilisation",
     "description": "First major Mesoamerican civilisation, on the Gulf coast lowlands; colossal heads, La Venta, San Lorenzo; cultural template for later cultures.",
     "start_year": -1500, "end_year": -400, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Olmecs",
     "priorities": p(910_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Chavín culture",
     "description": "Andean civilisation centred on Chavín de Huántar; widespread religious style; flourished in the Early Horizon of Peruvian archaeology.",
     "start_year": -900, "end_year": -200, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Chav%C3%ADn_culture",
     "priorities": p(850_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Zapotec civilisation",
     "description": "Centred on Monte Albán in the Oaxaca valley; one of the first Mesoamerican states; their writing system is among the earliest in the Americas.",
     "start_year": -500, "end_year": 800, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Zapotec_civilization",
     "priorities": p(840_000), "region_weights": RW_AMER},

    # ----- Maya classic -----
    {"type": "event", "title": "Maya civilisation",
     "description": "Mesoamerican civilisation in the Yucatán and adjacent lowlands; the only fully developed writing system pre-Columbian America had.",
     "start_year": -2000, "end_year": 1500, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Maya_civilization",
     "priorities": p(940_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Maya Preclassic period",
     "description": "Early Maya city-states emerge in Petén; first monumental architecture; long-count calendar.",
     "start_year": -2000, "end_year": 250, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Preclassic_Maya",
     "priorities": p(820_000), "region_weights": RW_AMER,
     "first_zoom_out": "Maya civilisation"},

    {"type": "event", "title": "Maya Classic period",
     "description": "Peak of Maya civilisation; city-states like Tikal, Palenque, Calakmul build great pyramid complexes and produce elaborate inscriptions.",
     "start_year": 250, "end_year": 900, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Classic_Maya",
     "priorities": p(890_000), "region_weights": RW_AMER,
     "first_zoom_out": "Maya civilisation"},

    {"type": "event", "title": "Teotihuacán at its peak",
     "description": "Vast central-Mexican city of perhaps 125,000 people; Pyramids of the Sun and Moon; influence reaches into the Maya world.",
     "start_year": 100, "end_year": 550, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Teotihuacan",
     "priorities": p(910_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Moche civilisation",
     "description": "Peruvian coastal civilisation; spectacular gold work, sophisticated irrigation, the Lord of Sipán burial.",
     "start_year": 100, "end_year": 800, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Moche_culture",
     "priorities": p(830_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Nazca lines created",
     "description": "Giant geoglyphs etched into the Peruvian desert by the Nazca culture; visible only from the air; remain partly unexplained.",
     "start_year": -500, "end_year": 500, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Nazca_Lines",
     "priorities": p(860_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_AMER},

    {"type": "event", "title": "Tiwanaku civilisation",
     "description": "Andean culture centred on Lake Titicaca's southern shore; sophisticated stonework; influence across much of the Andes.",
     "start_year": -110, "end_year": 1000, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tiwanaku",
     "priorities": p(820_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Wari Empire",
     "description": "Andean empire centred on Wari in the central Peruvian highlands; possibly the first true empire in the Andes; precursor to the Inca.",
     "start_year": 500, "end_year": 1000, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Wari_culture",
     "priorities": p(820_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Maya Classic collapse",
     "description": "Most southern lowland Maya cities abandoned over 100-150 years; combination of drought, warfare and ecological strain.",
     "start_year": 800, "end_year": 900, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Classic_Maya_collapse",
     "priorities": p(880_000), "region_weights": RW_AMER,
     "first_zoom_out": "Maya civilisation"},

    {"type": "event", "title": "Maya Postclassic period",
     "description": "Northern Yucatán cities (Chichén Itzá, Mayapán) flourish; Maya civilisation continues to the Spanish arrival.",
     "start_year": 900, "end_year": 1500, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Postclassic_Maya",
     "priorities": p(820_000), "region_weights": RW_AMER,
     "first_zoom_out": "Maya civilisation"},

    {"type": "event", "title": "Chichén Itzá at its peak",
     "description": "Major Maya-Toltec city in northern Yucatán; pyramid of Kukulkan, sacred cenote.",
     "start_year": 800, "end_year": 1200, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Chichen_Itza",
     "priorities": p(890_000, **{"arts-and-thoughts": 870_000}),
     "region_weights": RW_AMER,
     "first_zoom_out": "Maya Postclassic period"},

    # ----- Toltec, Mixtec, Tarascan -----
    {"type": "event", "title": "Toltec civilisation",
     "description": "Mesoamerican civilisation centred on Tula in central Mexico; later remembered by the Aztecs as the model culture.",
     "start_year": 900, "end_year": 1150, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Toltec",
     "priorities": p(840_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Mixtec civilisation",
     "description": "Mesoamerican culture in highland Oaxaca; renowned for goldsmithing and pictorial codices.",
     "start_year": 1000, "end_year": 1521, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mixtec_civilization",
     "priorities": p(800_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Tarascan / Purépecha state",
     "description": "West Mexican empire centred on Tzintzuntzan; never conquered by the Aztecs; metallurgy advanced beyond their neighbours.",
     "start_year": 1300, "end_year": 1530, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tarascan_state",
     "priorities": p(800_000), "region_weights": RW_AMER},

    # ----- Chimú & Inca -----
    {"type": "event", "title": "Chimor (Chimú Kingdom)",
     "description": "Largest Andean state before the Inca; capital at Chan Chan, the largest adobe city in the world; conquered by Inca c. 1470.",
     "start_year": 900, "end_year": 1470, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Chim%C3%BA_culture",
     "priorities": p(840_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Chan Chan built",
     "description": "Capital of Chimor; largest adobe city in the Americas; covers 20 km² with grand royal compounds.",
     "start_year": 1300, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Chan_Chan",
     "priorities": p(820_000, **{"arts-and-thoughts": 830_000}),
     "region_weights": RW_AMER,
     "first_zoom_out": "Chimor (Chimú Kingdom)"},

    {"type": "event", "title": "Inca expansion under Pachacuti",
     "description": "Inca Pachacuti and his son Topa Inca conquer the central Andes from Quito to central Chile in ~30 years; foundation of the Inca empire.",
     "start_year": 1438, "end_year": 1493,
     "wikipedia": "https://en.wikipedia.org/wiki/Pachacuti",
     "priorities": p(910_000), "region_weights": RW_AMER,
     "first_zoom_out": "Inca Empire"},

    {"type": "person", "title": "Pachacuti",
     "description": "Ninth Sapa Inca; transformed the Inca polity from a small Cuzco kingdom into a continental empire; redesigned Cuzco.",
     "start_year": 1418, "end_year": 1471, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pachacuti",
     "priorities": p(880_000, people=890_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Machu Picchu built",
     "description": "Royal Inca estate in the Andes near Cuzco; never found by the Spanish; rediscovered by Hiram Bingham in 1911.",
     "start_year": 1450, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Machu_Picchu",
     "priorities": p(940_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_AMER},

    {"type": "event", "title": "Atahualpa vs Huáscar civil war",
     "description": "Half-brothers fight for Inca throne after Huayna Capac's death; Atahualpa wins just as Pizarro arrives.",
     "start_year": 1529, "end_year": 1532,
     "wikipedia": "https://en.wikipedia.org/wiki/Inca_Civil_War",
     "priorities": p(870_000), "region_weights": RW_AMER,
     "first_zoom_out": "Inca Empire"},

    {"type": "event", "title": "Capture of Atahualpa at Cajamarca",
     "description": "Pizarro's 168 conquistadors capture the Inca emperor in his own camp; the room of gold ransom is paid; Atahualpa executed.",
     "start_year": 1532, "start_month": 11, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Cajamarca",
     "priorities": p(910_000), "region_weights": RW_AMER,
     "first_zoom_out": "Spanish conquest of the Incas"},

    {"type": "event", "title": "Inca resistance at Vilcabamba",
     "description": "Neo-Inca state established by Manco Inca; resists Spanish rule from the eastern Andes for 36 years before its conquest.",
     "start_year": 1537, "end_year": 1572,
     "wikipedia": "https://en.wikipedia.org/wiki/Neo-Inca_State",
     "priorities": p(810_000), "region_weights": RW_AMER,
     "first_zoom_out": "Spanish conquest of the Incas"},

    # ----- Aztec -----
    {"type": "event", "title": "Mexica founding of Tenochtitlan",
     "description": "Mexica found their island capital after seeing an eagle on a cactus; rises to dominate the Valley of Mexico.",
     "start_year": 1325, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tenochtitlan",
     "priorities": p(900_000), "region_weights": RW_AMER,
     "first_zoom_out": "Aztec Empire"},

    {"type": "event", "title": "Aztec Triple Alliance formed",
     "description": "Tenochtitlan, Texcoco and Tlacopan ally to overthrow Tepanec hegemony; foundation of the Aztec Empire.",
     "start_year": 1428,
     "wikipedia": "https://en.wikipedia.org/wiki/Aztec_Empire",
     "priorities": p(870_000), "region_weights": RW_AMER,
     "first_zoom_out": "Aztec Empire"},

    {"type": "person", "title": "Moctezuma II",
     "description": "Last fully independent Aztec emperor; hosted then was deposed and killed during the Spanish conquest.",
     "start_year": 1466, "end_year": 1520, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Moctezuma_II",
     "priorities": p(880_000, people=890_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Cortés lands at Veracruz",
     "description": "Hernán Cortés disobeys Cuba governor's recall and lands ~600 men on the Mexican coast; burns his ships and marches inland.",
     "start_year": 1519, "start_month": 4, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Spanish_conquest_of_the_Aztec_Empire",
     "priorities": p(880_000), "region_weights": RW_AMER,
     "first_zoom_out": "Spanish conquest of the Aztec Empire"},

    {"type": "event", "title": "La Noche Triste",
     "description": "Spaniards and Tlaxcalan allies retreat from Tenochtitlan at night; hundreds drowned or killed; Cortés regroups before final siege.",
     "start_year": 1520, "start_month": 6, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/La_Noche_Triste",
     "priorities": p(810_000), "region_weights": RW_AMER,
     "first_zoom_out": "Spanish conquest of the Aztec Empire"},

    {"type": "event", "title": "Fall of Tenochtitlan",
     "description": "Cortés and Tlaxcalan allies besiege and capture the Aztec capital after 75 days; smallpox epidemic decimates the defenders.",
     "start_year": 1521, "start_month": 5, "start_day": 22, "end_month": 8, "end_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Fall_of_Tenochtitlan",
     "priorities": p(940_000), "region_weights": RW_AMER,
     "first_zoom_out": "Spanish conquest of the Aztec Empire"},

    {"type": "event", "title": "Spanish conquest of the Aztec Empire",
     "description": "Cortés, helped by indigenous allies and smallpox, destroys the Aztec state in two years; founding event of New Spain.",
     "start_year": 1519, "end_year": 1521,
     "wikipedia": "https://en.wikipedia.org/wiki/Spanish_conquest_of_the_Aztec_Empire",
     "priorities": p(950_000), "region_weights": RW_AMER},

    # ----- North America: dual-tagged USA -----
    {"type": "event", "title": "Adena culture",
     "description": "Eastern Woodlands burial-mound culture in the Ohio valley; among the earliest North American mound builders.",
     "start_year": -1000, "end_year": 100, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Adena_culture",
     "priorities": p(770_000, usa=820_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Hopewell tradition",
     "description": "Eastern Woodlands trade and ceremonial network; vast geometric earthworks (Newark, Mound City); fine copper, mica, obsidian artefacts.",
     "start_year": -200, "end_year": 500, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hopewell_tradition",
     "priorities": p(810_000, usa=860_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Ancestral Puebloan culture",
     "description": "Pre-contact Native culture of the Four Corners region; cliff dwellings at Mesa Verde, great houses at Chaco Canyon.",
     "start_year": 100, "end_year": 1600, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Ancestral_Puebloans",
     "priorities": p(860_000, usa=900_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Chaco Canyon at its peak",
     "description": "Centre of Ancestral Puebloan civilisation in northwest New Mexico; great houses (Pueblo Bonito), 400-mile road network.",
     "start_year": 850, "end_year": 1150, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Chaco_Culture_National_Historical_Park",
     "priorities": p(880_000, usa=910_000), "region_weights": RW_AMER,
     "first_zoom_out": "Ancestral Puebloan culture"},

    {"type": "event", "title": "Mesa Verde cliff dwellings",
     "description": "Multi-story stone dwellings under cliff overhangs in southwest Colorado; abandoned by 1300, possibly due to drought.",
     "start_year": 1190, "end_year": 1300, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mesa_Verde_National_Park",
     "priorities": p(890_000, usa=910_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_AMER,
     "first_zoom_out": "Ancestral Puebloan culture"},

    {"type": "event", "title": "Mississippian culture",
     "description": "Maize-based mound-building societies across the eastern North American river valleys; chiefdoms with platform mounds and plazas.",
     "start_year": 800, "end_year": 1600, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mississippian_culture",
     "priorities": p(880_000, usa=920_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Cahokia at its peak",
     "description": "Largest pre-Columbian city north of Mexico, near modern St Louis; population perhaps 40,000 at peak; vast Monks Mound.",
     "start_year": 1050, "end_year": 1250, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Cahokia",
     "priorities": p(910_000, usa=940_000), "region_weights": RW_AMER,
     "first_zoom_out": "Mississippian culture"},

    {"type": "event", "title": "Iroquois Confederacy founded",
     "description": "Haudenosaunee (Five Nations) league forms in modern New York; constitution influences later thinking about federations.",
     "start_year": 1142, "date_uncertain": True,
     "display_date": "traditional date 1142; some sources say 15th century",
     "wikipedia": "https://en.wikipedia.org/wiki/Iroquois",
     "priorities": p(900_000, usa=930_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Pueblo Revolt of 1680",
     "description": "Coordinated Pueblo uprising under Popé drives Spanish out of present-day New Mexico for 12 years; rare successful indigenous reconquest.",
     "start_year": 1680, "start_month": 8, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Pueblo_Revolt",
     "priorities": p(870_000, usa=900_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Cahokia decline",
     "description": "Cahokia gradually depopulated; reasons debated (climate change, soil exhaustion, political instability); abandoned by ~1400.",
     "start_year": 1250, "end_year": 1400, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Cahokia",
     "priorities": p(810_000, usa=850_000), "region_weights": RW_AMER,
     "first_zoom_out": "Mississippian culture"},

    {"type": "event", "title": "Thule Inuit expansion",
     "description": "Whale-hunting Thule people spread across the North American Arctic from Alaska to Greenland; ancestors of modern Inuit.",
     "start_year": 1000, "end_year": 1600, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Thule_people",
     "priorities": p(780_000, usa=800_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Norse contact at L'Anse aux Meadows",
     "description": "Norse settlement in Newfoundland; first verified European presence in the Americas; abandoned within a couple of decades.",
     "start_year": 1000, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/L%27Anse_aux_Meadows",
     "priorities": p(880_000), "region_weights": RW_AMER},

    # ----- Foundation events -----
    {"type": "event", "title": "Columbus reaches the Americas",
     "description": "Christopher Columbus's first voyage lands in the Bahamas; opens the Columbian Exchange and four centuries of European colonisation.",
     "start_year": 1492, "start_month": 10, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Voyages_of_Christopher_Columbus",
     "priorities": p(990_000, usa=910_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Treaty of Tordesillas",
     "description": "Spain and Portugal partition the non-European world along a meridian west of the Cape Verde Islands.",
     "start_year": 1494, "start_month": 6, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Tordesillas",
     "priorities": p(900_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Smallpox arrives in the Americas",
     "description": "First smallpox outbreaks devastate indigenous populations with no immunity; mortality often >50% within decades of contact.",
     "start_year": 1518, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/History_of_smallpox#Americas",
     "priorities": p(950_000, usa=900_000), "region_weights": RW_AMER},

    # ----- People -----
    {"type": "person", "title": "Hernán Cortés",
     "description": "Spanish conquistador; led the destruction of the Aztec Empire; first governor of New Spain.",
     "start_year": 1485, "end_year": 1547, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hern%C3%A1n_Cort%C3%A9s",
     "priorities": p(900_000, people=910_000), "region_weights": RW_AMER},

    {"type": "person", "title": "Francisco Pizarro",
     "description": "Spanish conquistador; led the destruction of the Inca Empire with under 200 men; killed in a power struggle in Lima.",
     "start_year": 1478, "end_year": 1541, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Francisco_Pizarro",
     "priorities": p(890_000, people=900_000), "region_weights": RW_AMER},

    {"type": "person", "title": "Atahualpa",
     "description": "Last sovereign Sapa Inca; captured at Cajamarca; ransom delivered; executed by garrote in 1533.",
     "start_year": 1500, "end_year": 1533, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Atahualpa",
     "priorities": p(870_000, people=890_000), "region_weights": RW_AMER},

    {"type": "person", "title": "Cuauhtémoc",
     "description": "Last Aztec emperor; defended Tenochtitlan during the final siege; tortured and executed by Cortés.",
     "start_year": 1495, "end_year": 1525, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Cuauht%C3%A9moc",
     "priorities": p(820_000, people=850_000), "region_weights": RW_AMER},

    {"type": "person", "title": "La Malinche",
     "description": "Nahua interpreter and consort of Cortés; pivotal in the conquest of Mexico; controversial figure in Mexican memory.",
     "start_year": 1500, "end_year": 1551, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/La_Malinche",
     "priorities": p(820_000, people=850_000), "region_weights": RW_AMER},

    {"type": "event", "title": "Bartolomé de las Casas defends indigenous rights",
     "description": "Dominican friar denounces Spanish atrocities; A Short Account of the Destruction of the Indies (1552) shapes the Black Legend.",
     "start_year": 1542,
     "wikipedia": "https://en.wikipedia.org/wiki/Bartolom%C3%A9_de_las_Casas",
     "priorities": p(860_000), "region_weights": RW_AMER},

    # ----- Misc cultural -----
    {"type": "event", "title": "Maya Long Count calendar baseline",
     "description": "Maya date system anchors creation on 11 August 3114 BCE (Gregorian); accurate astronomical observations underpin religious life.",
     "start_year": -3114, "start_month": 8, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Mesoamerican_Long_Count_calendar",
     "priorities": p(840_000, **{"arts-and-thoughts": 850_000}),
     "region_weights": RW_AMER,
     "first_zoom_out": "Maya civilisation"},

    {"type": "event", "title": "Popol Vuh recorded",
     "description": "K'iche' Maya creation epic written down in alphabetic K'iche'; one of the great surviving texts of pre-Columbian Mesoamerica.",
     "start_year": 1554, "end_year": 1558, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Popol_Vuh",
     "priorities": p(840_000, **{"arts-and-thoughts": 870_000}),
     "region_weights": RW_AMER,
     "first_zoom_out": "Maya civilisation"},

    {"type": "event", "title": "Codex Mendoza compiled",
     "description": "Aztec pictorial manuscript commissioned by the first viceroy; records tribute lists, history, and daily life; Spanish gloss accompanies pictograms.",
     "start_year": 1541, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Codex_Mendoza",
     "priorities": p(810_000, **{"arts-and-thoughts": 840_000}),
     "region_weights": RW_AMER},

    {"type": "event", "title": "Triple alliance vs Tarascans",
     "description": "Aztec Empire's last major war before the Spanish arrival; Tarascan state retains independence west of Mexico.",
     "start_year": 1478, "start_month": 4, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Tarascan_state",
     "priorities": p(770_000), "region_weights": RW_AMER,
     "first_zoom_out": "Aztec Empire"},

    {"type": "event", "title": "Inca road system",
     "description": "Network of ~40,000 km of paved roads connecting the empire from Quito to central Chile; runners (chasquis) relayed messages.",
     "start_year": 1400, "end_year": 1530, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Inca_road_system",
     "priorities": p(870_000), "region_weights": RW_AMER,
     "first_zoom_out": "Inca Empire"},

    {"type": "event", "title": "Quipu record-keeping",
     "description": "Inca knotted-cord system records numerical and possibly narrative data; never deciphered as fully as expected.",
     "start_year": -2500, "end_year": 1600, "date_uncertain": True,
     "display_date": "in use c. 2500 BCE - 1600 CE",
     "wikipedia": "https://en.wikipedia.org/wiki/Quipu",
     "priorities": p(810_000, **{"arts-and-thoughts": 830_000}),
     "region_weights": RW_AMER},

    {"type": "event", "title": "Maya numerals and zero",
     "description": "Maya develop a vigesimal positional number system with a symbol for zero, independently of Babylonian or Indian mathematics.",
     "start_year": -36, "date_uncertain": True,
     "display_date": "developed by c. 36 BCE",
     "wikipedia": "https://en.wikipedia.org/wiki/Maya_numerals",
     "priorities": p(860_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_AMER,
     "first_zoom_out": "Maya civilisation"},
]


def main() -> int:
    base = next_available_id()
    for i, en in enumerate(ENTRIES):
        en["id"] = base + i
    n = append_entries(ENTRIES)
    print(f"Appended {n} Pre-Columbian Americas entries (IDs {base}..{base+n-1}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
