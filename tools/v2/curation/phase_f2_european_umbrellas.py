"""
Phase F2 — Children for high-priority European umbrellas.

Targets:
  Industrial Revolution (~45 entries)
  Victorian era (~35 entries)
  Napoleonic Wars (~30 entries)
  Hundred Years' War + Thirty Years' War (~20 entries combined)
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_BRIT = {"europe": 10, "americas": 4, "asia": 3, "australasia": 3, "africa": 3}
RW_BRIT_GLOBAL = {"europe": 9, "americas": 7, "asia": 7, "australasia": 6, "africa": 6}
RW_EU = {"europe": 10, "americas": 3, "asia": 3, "australasia": 1, "africa": 2}


# Helper for entries on multiple slugs.
def pri(master: int, **extras) -> dict:
    return {"master": master, **extras}


ENTRIES = [
    # ============================================================
    # INDUSTRIAL REVOLUTION (~45 entries)
    # ============================================================
    {"type": "event", "title": "Newcomen atmospheric engine",
     "description": "Thomas Newcomen's piston-cylinder steam engine pumps water from mines; first commercially successful steam engine.",
     "start_year": 1712,
     "wikipedia": "https://en.wikipedia.org/wiki/Newcomen_atmospheric_engine",
     "priorities": pri(910_000, industrial=940_000, **{"arts-and-thoughts": 900_000, "england": 900_000}),
     "region_weights": RW_BRIT_GLOBAL,
     "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Abraham Darby's coke-fired blast furnace",
     "description": "Quaker ironmaster develops a way to smelt iron with coke instead of charcoal; clears bottleneck for British iron production.",
     "start_year": 1709,
     "wikipedia": "https://en.wikipedia.org/wiki/Abraham_Darby_I",
     "priorities": pri(880_000, industrial=920_000, england=880_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Flying shuttle invented",
     "description": "John Kay's flying shuttle (1733) doubles weaver productivity; first major textile innovation of the Industrial Revolution.",
     "start_year": 1733,
     "wikipedia": "https://en.wikipedia.org/wiki/Flying_shuttle",
     "priorities": pri(850_000, industrial=900_000, england=860_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Spinning jenny invented",
     "description": "James Hargreaves's machine spins eight threads at once; transforms cottage weaving and feeds factory industrialisation.",
     "start_year": 1764, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Spinning_jenny",
     "priorities": pri(890_000, industrial=940_000, england=880_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Arkwright's water frame",
     "description": "Richard Arkwright's water-powered spinning frame and Cromford mill model the factory system.",
     "start_year": 1769,
     "wikipedia": "https://en.wikipedia.org/wiki/Water_frame",
     "priorities": pri(890_000, industrial=940_000, england=890_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Watt's separate condenser",
     "description": "James Watt's improvement makes steam engines several times more fuel-efficient; foundation of practical steam power.",
     "start_year": 1769, "start_month": 1, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Watt_steam_engine",
     "priorities": pri(950_000, industrial=970_000, england=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Crompton's spinning mule",
     "description": "Samuel Crompton combines the jenny and the water frame; produces fine yarn at industrial scale.",
     "start_year": 1779,
     "wikipedia": "https://en.wikipedia.org/wiki/Spinning_mule",
     "priorities": pri(840_000, industrial=890_000, england=860_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Cartwright's power loom",
     "description": "Edmund Cartwright's mechanical loom completes the industrialisation of weaving begun by Kay and Hargreaves.",
     "start_year": 1785,
     "wikipedia": "https://en.wikipedia.org/wiki/Power_loom",
     "priorities": pri(840_000, industrial=890_000, england=860_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Cotton gin invented",
     "description": "Eli Whitney's machine separates cotton fibre from seed; revolutionises cotton economics and entrenches American slavery.",
     "start_year": 1793,
     "wikipedia": "https://en.wikipedia.org/wiki/Cotton_gin",
     "priorities": pri(910_000, industrial=910_000, usa=900_000),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Trevithick's high-pressure steam locomotive",
     "description": "Cornish engineer Richard Trevithick builds the first working steam locomotive; runs on the Penydarren tramway in Wales.",
     "start_year": 1804, "start_month": 2, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Richard_Trevithick",
     "priorities": pri(870_000, industrial=920_000, england=870_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Luddite uprisings",
     "description": "Skilled English textile workers smash power-loom machinery; brutal repression follows; 'Luddite' enters English as an epithet.",
     "start_year": 1811, "end_year": 1816,
     "wikipedia": "https://en.wikipedia.org/wiki/Luddite",
     "priorities": pri(870_000, industrial=890_000, england=880_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Stockton and Darlington Railway opens",
     "description": "First public railway to use steam locomotion, between Stockton and Darlington in Co. Durham; engineer George Stephenson.",
     "start_year": 1825, "start_month": 9, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Stockton_and_Darlington_Railway",
     "priorities": pri(880_000, industrial=930_000, england=870_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Liverpool and Manchester Railway",
     "description": "First inter-city steam railway; opening day marred by death of William Huskisson; railway mania follows across Britain.",
     "start_year": 1830, "start_month": 9, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Liverpool_and_Manchester_Railway",
     "priorities": pri(900_000, industrial=940_000, england=900_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "person", "title": "George Stephenson",
     "description": "Engineer; built the Stockton and Darlington and Liverpool and Manchester railways; the Rocket; standard gauge.",
     "start_year": 1781, "end_year": 1848, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/George_Stephenson",
     "priorities": pri(890_000, industrial=920_000, england=900_000, people=910_000),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "person", "title": "Isambard Kingdom Brunel",
     "description": "Visionary engineer of railways, bridges and ships; Great Western Railway, SS Great Britain, Clifton Suspension Bridge.",
     "start_year": 1806, "end_year": 1859, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Isambard_Kingdom_Brunel",
     "priorities": pri(910_000, industrial=940_000, england=920_000, people=920_000),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Factory Act 1833",
     "description": "Bans factory employment of children under nine; limits hours for under-18s; first effective British labour regulation; appoints inspectors.",
     "start_year": 1833, "start_month": 8, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Factory_Acts",
     "priorities": pri(880_000, industrial=910_000, england=890_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Mines and Collieries Act 1842",
     "description": "Bans women and children under 10 from underground work in British mines; response to the 1842 Mines Commission's grim findings.",
     "start_year": 1842, "start_month": 8, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Mines_and_Collieries_Act_1842",
     "priorities": pri(820_000, industrial=880_000, england=850_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Public Health Act 1848",
     "description": "Edwin Chadwick's act creates local boards of health; first major British public-health legislation; sewers, sanitation, clean water.",
     "start_year": 1848, "start_month": 8, "start_day": 31,
     "wikipedia": "https://en.wikipedia.org/wiki/Public_Health_Act_1848",
     "priorities": pri(840_000, industrial=880_000, england=870_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Bessemer process",
     "description": "Henry Bessemer's converter mass-produces cheap steel; transforms construction, railways and warfare.",
     "start_year": 1856, "start_month": 8, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Bessemer_process",
     "priorities": pri(910_000, industrial=940_000, england=890_000, **{"arts-and-thoughts": 890_000}),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Morse telegraph",
     "description": "Samuel Morse's electrical telegraph, with code, transforms long-distance communication from days to seconds.",
     "start_year": 1844, "start_month": 5, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Electrical_telegraph",
     "priorities": pri(920_000, industrial=900_000, usa=860_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Transatlantic telegraph cable",
     "description": "Cyrus Field's cable from Ireland to Newfoundland links Europe and North America by telegraph; first message sent August 1858.",
     "start_year": 1858, "start_month": 8, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Transatlantic_telegraph_cable",
     "priorities": pri(880_000, industrial=890_000, england=870_000),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Bell patents the telephone",
     "description": "Alexander Graham Bell files patent for voice transmission over wire; \"Mr Watson, come here, I want to see you.\"",
     "start_year": 1876, "start_month": 3, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/History_of_the_telephone",
     "priorities": pri(940_000, industrial=920_000, usa=890_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Edison's incandescent light bulb",
     "description": "Thomas Edison demonstrates a practical long-lasting incandescent bulb at Menlo Park; opens the electric age.",
     "start_year": 1879, "start_month": 10, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Incandescent_light_bulb",
     "priorities": pri(950_000, industrial=920_000, usa=920_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Pearl Street power station",
     "description": "Edison opens the world's first commercial central power station in lower Manhattan; serves 85 customers with DC electricity.",
     "start_year": 1882, "start_month": 9, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Pearl_Street_Station",
     "priorities": pri(880_000, industrial=900_000, usa=870_000),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Industrial Revolution"},

    {"type": "event", "title": "Daguerreotype announced",
     "description": "Louis Daguerre's photographic process publicly announced in Paris; first widely accessible photographic medium.",
     "start_year": 1839, "start_month": 8, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Daguerreotype",
     "priorities": pri(880_000, industrial=850_000, france=870_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_EU},

    {"type": "event", "title": "Otto's four-stroke engine",
     "description": "Nicolaus Otto patents the four-stroke internal combustion engine; foundation of the automobile.",
     "start_year": 1876, "start_month": 5, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Four-stroke_engine",
     "priorities": pri(880_000, industrial=900_000, germany=870_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Benz Patent-Motorwagen",
     "description": "Karl Benz patents the first automobile powered by an internal-combustion engine; modern motoring begins.",
     "start_year": 1886, "start_month": 1, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Benz_Patent-Motorwagen",
     "priorities": pri(940_000, industrial=920_000, germany=900_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Ford Model T",
     "description": "Henry Ford's affordable mass-produced car using the moving assembly line; transforms American society and global manufacturing.",
     "start_year": 1908, "start_month": 10, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Ford_Model_T",
     "priorities": pri(960_000, industrial=920_000, usa=940_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Bessemer's converter sees first commercial use",
     "description": "Sheffield steel-makers adopt the Bessemer converter; steel rails replace iron; reshapes Britain's industrial cities.",
     "start_year": 1858, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Bessemer_process",
     "priorities": pri(810_000, industrial=860_000, england=830_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Bessemer process"},

    # ============================================================
    # VICTORIAN ERA (~30 entries)
    # ============================================================
    {"type": "event", "title": "Reform of the British army (Cardwell)",
     "description": "Edward Cardwell abolishes purchase of officer commissions, shortens enlistment, modernises British army for industrial-era warfare.",
     "start_year": 1870, "end_year": 1881,
     "wikipedia": "https://en.wikipedia.org/wiki/Cardwell_Reforms",
     "priorities": pri(770_000, england=820_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Victorian era"},

    {"type": "event", "title": "Marriage of Victoria and Albert",
     "description": "Queen Victoria marries Albert of Saxe-Coburg and Gotha; partnership shapes the early Victorian era.",
     "start_year": 1840, "start_month": 2, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Wedding_of_Queen_Victoria_and_Prince_Albert",
     "priorities": pri(830_000, england=880_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Victorian era"},

    {"type": "event", "title": "Death of Prince Albert",
     "description": "Victoria's husband dies of typhoid; Queen withdraws into seclusion for years; reshapes the monarchy.",
     "start_year": 1861, "start_month": 12, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Albert,_Prince_Consort",
     "priorities": pri(840_000, england=870_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Victorian era"},

    {"type": "person", "title": "Charles Dickens",
     "description": "Most-read English novelist of the Victorian era; Oliver Twist, A Christmas Carol, Bleak House, David Copperfield, Great Expectations.",
     "start_year": 1812, "end_year": 1870, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Charles_Dickens",
     "priorities": pri(960_000, england=950_000, people=960_000, **{"arts-and-thoughts": 960_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "art", "title": "Alice's Adventures in Wonderland",
     "description": "Lewis Carroll's children's classic; surreal humour and wordplay; gives English 'rabbit hole' and 'mad as a hatter'.",
     "start_year": 1865, "start_month": 11, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Alice%27s_Adventures_in_Wonderland",
     "priorities": pri(910_000, england=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "art", "title": "Origin of Species",
     "description": "Charles Darwin's On the Origin of Species lays out natural selection; transforms biology and human self-understanding.",
     "start_year": 1859, "start_month": 11, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/On_the_Origin_of_Species",
     "priorities": pri(990_000, england=970_000, **{"arts-and-thoughts": 980_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Beagle voyage of Charles Darwin",
     "description": "Darwin's five-year voyage on HMS Beagle provides the observations that lead to Origin of Species.",
     "start_year": 1831, "end_year": 1836,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_voyage_of_HMS_Beagle",
     "priorities": pri(920_000, england=910_000),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "person", "title": "Florence Nightingale",
     "description": "Founder of modern nursing; reformed military medicine after the Crimean War; pioneered the use of statistics in healthcare.",
     "start_year": 1820, "end_year": 1910, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Florence_Nightingale",
     "priorities": pri(910_000, england=920_000, people=920_000),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Cholera epidemic of 1854 / John Snow",
     "description": "Dr John Snow traces a London cholera outbreak to the Broad Street pump; landmark in epidemiology.",
     "start_year": 1854, "start_month": 8, "start_day": 31,
     "wikipedia": "https://en.wikipedia.org/wiki/1854_Broad_Street_cholera_outbreak",
     "priorities": pri(870_000, england=890_000, **{"arts-and-thoughts": 870_000}),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Victorian era"},

    {"type": "person", "title": "Michael Faraday",
     "description": "Self-taught chemist and physicist; discovered electromagnetic induction; Faraday cage; one of the greatest experimentalists in history.",
     "start_year": 1791, "end_year": 1867, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Michael_Faraday",
     "priorities": pri(930_000, england=920_000, people=930_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "person", "title": "James Clerk Maxwell",
     "description": "Scottish physicist; unified electricity, magnetism and light in Maxwell's equations; one of the great theoretical achievements.",
     "start_year": 1831, "end_year": 1879, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/James_Clerk_Maxwell",
     "priorities": pri(940_000, england=910_000, people=940_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Indian Mutiny of 1857 (British view)",
     "description": "Mutiny of Bengal sepoys becomes a general rebellion across north India; suppressed by Britain; East India Company replaced by Crown rule.",
     "start_year": 1857, "start_month": 5, "start_day": 10, "end_year": 1858, "end_month": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Indian_Rebellion_of_1857",
     "priorities": pri(870_000, england=890_000, india=930_000),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Victorian era"},

    {"type": "event", "title": "Battle of Isandlwana",
     "description": "Zulu impi annihilates a British force in southern Africa; biggest defeat of British arms by a non-industrial army in the 19th century.",
     "start_year": 1879, "start_month": 1, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Isandlwana",
     "priorities": pri(840_000, england=860_000),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Victorian era"},

    {"type": "event", "title": "Battle of Rorke's Drift",
     "description": "100 British soldiers hold off ~4,000 Zulu warriors a day after Isandlwana; eleven Victoria Crosses awarded.",
     "start_year": 1879, "start_month": 1, "start_day": 22, "end_month": 1, "end_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Rorke%27s_Drift",
     "priorities": pri(810_000, england=840_000),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Battle of Isandlwana"},

    {"type": "event", "title": "Khartoum besieged; death of Gordon",
     "description": "Mahdist forces capture Khartoum; General Charles Gordon killed two days before British relief column arrives.",
     "start_year": 1884, "start_month": 3, "start_day": 13, "end_year": 1885, "end_month": 1, "end_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Khartoum",
     "priorities": pri(820_000, england=860_000),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Victorian era"},

    {"type": "event", "title": "Battle of Omdurman",
     "description": "Kitchener's army crushes the Mahdist state at Omdurman; avenges Gordon; Winston Churchill takes part as a young cavalryman.",
     "start_year": 1898, "start_month": 9, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Omdurman",
     "priorities": pri(840_000, england=870_000),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Victorian era"},

    {"type": "event", "title": "Jack the Ripper murders",
     "description": "Series of unsolved murders in Whitechapel, London; defines the late-Victorian fascination with sensational crime.",
     "start_year": 1888, "start_month": 8, "start_day": 31, "end_month": 11, "end_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Jack_the_Ripper",
     "priorities": pri(890_000, england=900_000),
     "region_weights": RW_BRIT_GLOBAL, "first_zoom_out": "Victorian era"},

    {"type": "person", "title": "Oscar Wilde",
     "description": "Anglo-Irish playwright, poet, novelist; wit and aphorist; convicted of gross indecency 1895; died in Paris exile.",
     "start_year": 1854, "end_year": 1900, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Oscar_Wilde",
     "priorities": pri(910_000, england=920_000, people=920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Trial of Oscar Wilde",
     "description": "Wilde sues for libel, loses, is then prosecuted for gross indecency and sentenced to two years' hard labour; case shapes attitudes for decades.",
     "start_year": 1895, "start_month": 4, "start_day": 26, "end_month": 5, "end_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Trials_of_Oscar_Wilde",
     "priorities": pri(840_000, england=870_000),
     "region_weights": RW_BRIT, "first_zoom_out": "Victorian era"},

    # ============================================================
    # NAPOLEONIC WARS (~25 entries)
    # ============================================================
    {"type": "event", "title": "French Revolutionary Wars",
     "description": "France's war with European monarchies from 1792; precursor to the Napoleonic Wars; the young general Bonaparte rises through Italy and Egypt.",
     "start_year": 1792, "end_year": 1802,
     "wikipedia": "https://en.wikipedia.org/wiki/French_Revolutionary_Wars",
     "priorities": pri(900_000, france=910_000, napoleonic=920_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Battle of the Nile",
     "description": "Nelson destroys the French fleet in Aboukir Bay, stranding Bonaparte's army in Egypt and reasserting British naval dominance.",
     "start_year": 1798, "start_month": 8, "start_day": 1, "end_month": 8, "end_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Nile",
     "priorities": pri(880_000, england=900_000, napoleonic=900_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Napoleon's coup of 18 Brumaire",
     "description": "Bonaparte overthrows the Directory and installs the Consulate; effective end of the French Revolution; he becomes First Consul.",
     "start_year": 1799, "start_month": 11, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Coup_of_18_Brumaire",
     "priorities": pri(920_000, france=930_000, napoleonic=920_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Marengo",
     "description": "Napoleon's narrow victory over the Austrians in northern Italy consolidates his political power as First Consul.",
     "start_year": 1800, "start_month": 6, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Marengo",
     "priorities": pri(820_000, france=850_000, napoleonic=890_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleonic Wars"},

    {"type": "event", "title": "Coronation of Napoleon",
     "description": "Bonaparte crowns himself Emperor of the French in Notre-Dame; Pope Pius VII attends; Jacques-Louis David paints it.",
     "start_year": 1804, "start_month": 12, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Coronation_of_Napoleon",
     "priorities": pri(920_000, france=940_000, napoleonic=930_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_EU},

    {"type": "event", "title": "Napoleonic Code",
     "description": "Comprehensive civil code promulgated under Napoleon; basis of civil law in much of continental Europe and beyond.",
     "start_year": 1804, "start_month": 3, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Napoleonic_Code",
     "priorities": pri(940_000, france=950_000, napoleonic=910_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Ulm",
     "description": "Napoleon envelops an Austrian army at Ulm in three weeks; surrender of 60,000 prisoners; opens the road to Vienna.",
     "start_year": 1805, "start_month": 10, "start_day": 16, "end_month": 10, "end_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Ulm",
     "priorities": pri(830_000, france=860_000, napoleonic=890_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleonic Wars"},

    {"type": "event", "title": "Battle of Austerlitz",
     "description": "Napoleon's masterpiece; crushes the combined Austrian and Russian armies; Holy Roman Empire dissolved a year later.",
     "start_year": 1805, "start_month": 12, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Austerlitz",
     "priorities": pri(920_000, france=940_000, napoleonic=950_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleonic Wars"},

    {"type": "event", "title": "Battle of Friedland",
     "description": "Napoleon decisively defeats the Russian army; leads to the Treaty of Tilsit and a partition of Europe between France and Russia.",
     "start_year": 1807, "start_month": 6, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Friedland",
     "priorities": pri(820_000, france=850_000, napoleonic=880_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleonic Wars"},

    {"type": "event", "title": "Treaties of Tilsit",
     "description": "Napoleon and Alexander I meet on a raft on the Niemen; treaties partition Europe; Prussia humiliated; brief Franco-Russian alliance.",
     "start_year": 1807, "start_month": 7, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaties_of_Tilsit",
     "priorities": pri(870_000, france=890_000, napoleonic=900_000, germany=850_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleonic Wars"},

    {"type": "event", "title": "Peninsular War",
     "description": "British, Portuguese, and Spanish forces (the Wellingtonian army) fight a long campaign against French armies on the Iberian peninsula.",
     "start_year": 1808, "end_year": 1814,
     "wikipedia": "https://en.wikipedia.org/wiki/Peninsular_War",
     "priorities": pri(910_000, england=920_000, france=890_000, napoleonic=940_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Wagram",
     "description": "Napoleon defeats the Austrians on the Marchfeld; very high casualties signal that Napoleon's enemies are catching up.",
     "start_year": 1809, "start_month": 7, "start_day": 5, "end_month": 7, "end_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Wagram",
     "priorities": pri(820_000, france=840_000, napoleonic=880_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleonic Wars"},

    {"type": "event", "title": "Napoleon's invasion of Russia",
     "description": "Grande Armée of ~600,000 invades Russia; takes Moscow but cannot force peace; retreat in winter destroys the army.",
     "start_year": 1812, "start_month": 6, "start_day": 24, "end_month": 12, "end_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/French_invasion_of_Russia",
     "priorities": pri(950_000, france=950_000, napoleonic=970_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Battle of Borodino",
     "description": "Bloodiest single day of the Napoleonic Wars; Napoleon defeats Kutuzov but cannot destroy the Russian army; opens the road to Moscow.",
     "start_year": 1812, "start_month": 9, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Borodino",
     "priorities": pri(880_000, france=890_000, napoleonic=910_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleon's invasion of Russia"},

    {"type": "event", "title": "Burning of Moscow",
     "description": "Russians set fire to Moscow during Napoleon's occupation; deprives the Grande Armée of winter quarters; triggers the catastrophic retreat.",
     "start_year": 1812, "start_month": 9, "start_day": 14, "end_month": 9, "end_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Fire_of_Moscow_(1812)",
     "priorities": pri(860_000, france=870_000, napoleonic=900_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleon's invasion of Russia"},

    {"type": "event", "title": "Crossing of the Berezina",
     "description": "Last desperate phase of the Russian retreat; Napoleon's army crosses the Berezina under attack; iconic image of the disaster.",
     "start_year": 1812, "start_month": 11, "start_day": 26, "end_month": 11, "end_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Berezina",
     "priorities": pri(820_000, france=840_000, napoleonic=880_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleon's invasion of Russia"},

    {"type": "event", "title": "Battle of Vitoria",
     "description": "Wellington crushes a French army at Vitoria; effectively expels French forces from Spain; Napoleon's empire crumbles.",
     "start_year": 1813, "start_month": 6, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Vitoria",
     "priorities": pri(810_000, england=850_000, napoleonic=860_000),
     "region_weights": RW_EU, "first_zoom_out": "Peninsular War"},

    {"type": "event", "title": "Napoleon abdicates (Fontainebleau)",
     "description": "After allies enter Paris, Napoleon abdicates unconditionally at Fontainebleau; sent to Elba; Bourbons restored.",
     "start_year": 1814, "start_month": 4, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Fontainebleau_(1814)",
     "priorities": pri(900_000, france=910_000, napoleonic=920_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleonic Wars"},

    {"type": "event", "title": "Congress of Vienna",
     "description": "Metternich, Talleyrand, Castlereagh and Alexander I redraw the European map; balance-of-power settlement endures for 40 years.",
     "start_year": 1814, "start_month": 11, "start_day": 1, "end_year": 1815, "end_month": 6, "end_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Congress_of_Vienna",
     "priorities": pri(920_000, france=890_000, napoleonic=900_000, germany=870_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Hundred Days",
     "description": "Napoleon escapes Elba, returns to Paris, rebuilds his army, and is defeated at Waterloo within four months; final exile to Saint Helena.",
     "start_year": 1815, "start_month": 3, "start_day": 20, "end_month": 7, "end_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Hundred_Days",
     "priorities": pri(920_000, france=920_000, napoleonic=950_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleonic Wars"},

    {"type": "event", "title": "Battle of Quatre Bras",
     "description": "Two days before Waterloo, Ney attacks Wellington's right wing at Quatre Bras; tactical draw but Wellington holds.",
     "start_year": 1815, "start_month": 6, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Quatre_Bras",
     "priorities": pri(790_000, england=820_000, napoleonic=860_000),
     "region_weights": RW_EU, "first_zoom_out": "Hundred Days"},

    {"type": "event", "title": "Battle of Ligny",
     "description": "Napoleon's last victory; defeats the Prussians under Blücher; but Blücher escapes intact and rejoins Wellington at Waterloo.",
     "start_year": 1815, "start_month": 6, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Ligny",
     "priorities": pri(800_000, france=820_000, napoleonic=860_000),
     "region_weights": RW_EU, "first_zoom_out": "Hundred Days"},

    {"type": "event", "title": "Exile of Napoleon to Saint Helena",
     "description": "Napoleon surrenders to the British after Waterloo; exiled to remote Saint Helena in the South Atlantic; dies there in 1821.",
     "start_year": 1815, "start_month": 10, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Napoleon's_exile_to_Saint_Helena",
     "priorities": pri(880_000, france=890_000, napoleonic=900_000),
     "region_weights": RW_EU, "first_zoom_out": "Napoleonic Wars"},

    {"type": "person", "title": "Napoleon Bonaparte",
     "description": "Corsican-born general, First Consul, and Emperor of the French; transformed Europe through war and the Napoleonic Code; died on Saint Helena.",
     "start_year": 1769, "end_year": 1821, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Napoleon",
     "priorities": pri(990_000, france=990_000, napoleonic=960_000, people=990_000),
     "region_weights": RW_BRIT_GLOBAL},

    # ============================================================
    # HUNDRED YEARS' WAR (~10 entries)
    # ============================================================
    {"type": "event", "title": "Battle of Sluys",
     "description": "Edward III's English fleet destroys the French fleet in the harbour of Sluys; secures cross-Channel supply for English armies.",
     "start_year": 1340, "start_month": 6, "start_day": 24,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Sluys",
     "priorities": pri(820_000, england=860_000),
     "region_weights": RW_EU, "first_zoom_out": "Hundred Years' War"},

    {"type": "event", "title": "Black Prince's chevauchée of 1355",
     "description": "Edward, the Black Prince, leads devastating raid across Languedoc; standard English strategy of ruinous plundering campaigns.",
     "start_year": 1355, "end_year": 1356,
     "wikipedia": "https://en.wikipedia.org/wiki/Chevauch%C3%A9e",
     "priorities": pri(780_000, england=820_000),
     "region_weights": RW_EU, "first_zoom_out": "Hundred Years' War"},

    {"type": "person", "title": "Edward the Black Prince",
     "description": "Eldest son of Edward III; victor at Crécy and Poitiers; never king; died a year before his father.",
     "start_year": 1330, "end_year": 1376, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Edward_the_Black_Prince",
     "priorities": pri(870_000, england=890_000, people=890_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Caroline War phase of HYW",
     "description": "Charles V of France and his Constable Bertrand du Guesclin recover most English continental possessions through Fabian warfare.",
     "start_year": 1369, "end_year": 1389,
     "wikipedia": "https://en.wikipedia.org/wiki/Caroline_War",
     "priorities": pri(800_000, england=830_000, france=830_000),
     "region_weights": RW_EU, "first_zoom_out": "Hundred Years' War"},

    {"type": "event", "title": "Trial and execution of Joan of Arc",
     "description": "Captured by Burgundians, sold to the English, condemned by an ecclesiastical court at Rouen, burned at the stake aged 19.",
     "start_year": 1431, "start_month": 5, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Joan_of_Arc",
     "priorities": pri(900_000, france=920_000, england=870_000),
     "region_weights": RW_EU, "first_zoom_out": "Hundred Years' War"},

    # ============================================================
    # THIRTY YEARS' WAR (~10 entries)
    # ============================================================
    {"type": "person", "title": "Gustavus Adolphus of Sweden",
     "description": "Soldier-king who transformed Sweden into a Great Power and intervened in the Thirty Years' War; killed at Lützen.",
     "start_year": 1594, "end_year": 1632, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Gustavus_Adolphus",
     "priorities": pri(890_000, germany=850_000, people=900_000),
     "region_weights": RW_EU},

    {"type": "person", "title": "Cardinal Richelieu",
     "description": "Chief minister of Louis XIII; centralised French royal power; backed Protestants abroad while crushing them at home.",
     "start_year": 1585, "end_year": 1642, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Cardinal_Richelieu",
     "priorities": pri(910_000, france=930_000, people=920_000),
     "region_weights": RW_EU},

    {"type": "event", "title": "Edict of Restitution",
     "description": "Emperor Ferdinand II orders restoration of Catholic Church property seized since 1552; provokes Protestant alarm and Swedish intervention.",
     "start_year": 1629, "start_month": 3, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Edict_of_Restitution",
     "priorities": pri(800_000, germany=830_000),
     "region_weights": RW_EU, "first_zoom_out": "Thirty Years' War"},

    {"type": "event", "title": "Battle of Rocroi",
     "description": "Young Duc d'Enghien crushes the previously invincible Spanish tercios; symbolic end of Spanish military supremacy.",
     "start_year": 1643, "start_month": 5, "start_day": 19,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Rocroi",
     "priorities": pri(830_000, france=860_000),
     "region_weights": RW_EU, "first_zoom_out": "Thirty Years' War"},

    {"type": "event", "title": "Battle of Nördlingen (1634)",
     "description": "Imperial-Spanish army crushes the Swedish-Protestant force; turning point that drags France openly into the war.",
     "start_year": 1634, "start_month": 9, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_N%C3%B6rdlingen_(1634)",
     "priorities": pri(790_000, germany=820_000),
     "region_weights": RW_EU, "first_zoom_out": "Thirty Years' War"},
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
