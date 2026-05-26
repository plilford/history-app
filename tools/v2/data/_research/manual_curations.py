"""
Per-item manual curation overrides for The Rest Is History episodes 1–300.

Keyed by the FIRST ep_num of the item (for multi-part series, that's the
ep_num of Part 1). Each value is either:
    None    → skip this item entirely (truly thematic / no datable subject)
    dict    → override the auto-curator with these fields (any subset of
              start, end, tags, title). Auto-curator output is used as
              fallback for any fields the override doesn't set.

Tags are master.py titles — must match exactly (case-insensitive trim).
The merger validates tags and drops unresolved ones with a warning.

Curation policy:
- For items the auto-curator dated correctly, an explicit override is still
  preferable because it pins down the exact intended subject and tags.
- "Skip" (None) is reserved for truly thematic episodes with no historical
  anchor (essays on Greatness, Lessons of History, Empires as a concept,
  Top Ten lists, etc.) AND for fictional/non-historical episodes (Game of
  Thrones, James Bond).
- Where the historical record gives a precise range, the start/end pair is
  set to that (e.g. Battle of Verdun begin/end days, not the year).
- Where the subject is a person, dates are usually their lifespan (unless
  the episode focuses on a specific event in their life).
- Where the subject is "X dynasty" or "X period", dates are start–end of
  that period.
- Books/films/works of art are dated to their publication/release year.
"""

from __future__ import annotations

# {first_ep_num: None | dict}
OVERRIDES: dict[int, dict | None] = {
    # ----- 2020 episodes (1-50) ----------------------------------------------
    1: None,   # Greatness — too thematic
    2: None,   # Civil War — too thematic (comparison essay)
    3: None,   # Trump as Caesar/Nixon — too speculative for placement
    4: {"start": 1599, "end": 1700, "tags": ["Oliver Cromwell", "Glorious Revolution"]},  # 17th century echoes
    5: {"start": 1981, "tags": []},
    6: {"start": -1260, "end": -1180, "tags": ["Trojan War", "Fall of Troy"]},
    7: None,  # Lessons of History
    8: None,  # Coffee House
    9: {"start": 1900, "end": 1914, "tags": ["World War I"]},  # Causes of WW1
    10: None,  # Christmas — thematic
    11: {"start": 2016, "tags": ["Brexit referendum"]},
    12: {"start": 1678, "end": 1681, "tags": ["Popish Plot"]},
    13: None,  # Stephen Fry and Troy — too conversational
    14: None,  # Historical Fiction — thematic
    15: None,  # Walls and Borders — thematic
    16: {"start": 79, "tags": ["Eruption of Vesuvius / Pompeii destroyed"]},
    17: {"start": 1919, "end": 1945, "tags": ["Benito Mussolini"]},  # Fascism
    18: None,  # North South Divide
    19: {"start": 500, "end": 600, "tags": []},  # King Arthur (legendary)
    20: None,  # China — too broad
    21: None,  # History of the Future
    22: None,  # Weird Wars
    23: {"start": 1990, "end": 1999, "tags": ["Tony Blair"]},  # The 90s
    24: None,  # Sex in the City
    25: None,  # Empires
    26: {"start": 1450, "end": 1750, "tags": []},  # Witches
    27: {"start": -1341, "end": -1323, "tags": ["Tutankhamun"]},
    28: None,  # Kings of Comedy
    29: None,  # Americanisation
    30: None,  # A Royal Row
    31: {"start": 1871, "end": 1918, "tags": []},  # Second Reich
    32: None,  # What if?
    33: None,  # The Beautiful Game (football)
    34: {"start": 634, "end": 687, "tags": []},  # St Cuthbert
    35: {"start": 1809, "end": 2024, "tags": ["Winston Churchill", "William Gladstone"]},  # PMs World Cup
    36: None,  # Our Greatest PM
    37: None,  # Spies with Macintyre — broad
    38: {"start": 1917, "end": 1991, "tags": ["Russian Revolution"]},  # Communism
    39: {"start": 1533, "end": 1603, "tags": ["Elizabeth I", "Reign of Elizabeth I"]},
    40: None,  # History as Entertainment
    41: {"start": -550, "end": -330, "tags": ["Achaemenid Persian Empire founded", "Persian invasions of Greece"]},
    42: {"start": 1850, "end": 1900, "tags": []},  # Wild West
    43: {"start": 1940, "tags": ["Winston Churchill"]},
    44: {"start": 1066, "tags": ["Battle of Hastings"]},
    45: None,  # Top Ten Eunuchs
    46: {"start": 1954, "end": 1968, "tags": ["US Civil Rights Movement"]},  # Culture Wars
    47: {"start": 1756, "end": 1763, "tags": ["Seven Years' War"]},
    48: {"start": 1789, "end": 1799, "tags": ["French Revolution"]},
    49: None,  # Food Glorious Food
    50: None,  # Teenagers

    # ----- 2021 episodes (51-150) --------------------------------------------
    51: {"start": 1428, "end": 1521, "tags": ["Aztec Empire"]},
    53: None,  # Game of Thrones — fiction
    54: {"start": 1599, "end": 1659, "tags": ["Oliver Cromwell", "Cromwell's Protectorate"]},
    55: None,  # World Cup of Gods preview
    56: {"start": 37, "end": 68, "tags": []},  # Nero
    57: {"start": 1163, "end": 1871, "tags": ["Notre-Dame de Paris built"]},
    58: None,  # World Cup of Gods (parts 1+2)
    60: {"start": 570, "end": 632, "tags": ["Muhammad"]},
    61: {"start": 1848, "end": 1855, "tags": ["California Gold Rush"]},
    62: {"start": 1199, "end": 1216, "tags": ["Magna Carta", "King John"]},
    63: {"start": 1889, "end": 1945, "tags": ["Adolf Hitler"]},  # Hitler (Kershaw)
    65: None,  # Very British Scandal
    66: None,  # Ghosts
    67: {"start": 1888, "end": 1945, "tags": []},  # Anglo-German Relations
    68: {"start": 1600, "end": 1997, "tags": []},  # British Empire (to handover of Hong Kong)
    69: None,  # England v Ukraine (football preview)
    70: None,  # Children's History
    71: None,  # England v Denmark
    72: {"start": 1955, "end": 1975, "tags": ["Vietnam War (American phase)"]},
    73: None,  # England v Italy
    74: {"start": 1509, "end": 1547, "tags": ["Henry VIII"]},  # Six Wives
    75: {"start": 1600, "end": 1858, "tags": []},  # East India Company
    76: None,  # Statues: Trafalgar Square
    77: None,  # Statues: Whitehall
    78: None,  # Statues: Parliament Square
    79: {"start": -776, "end": 393, "tags": []},  # Ancient Olympics
    80: {"start": 1896, "end": 2026, "tags": []},  # Modern Olympics
    82: {"start": -740, "end": -480, "tags": ["Messenian Wars (Sparta vs Messenia)", "Leonidas I of Sparta"]},
    83: {"start": 1961, "end": 1989, "tags": ["Berlin Wall built", "Construction of Berlin Wall"]},
    84: None,  # Exams
    85: {"start": 1887, "end": 1927, "tags": []},  # Sherlock Holmes
    86: {"start": 1685, "end": 1815, "tags": []},  # Enlightenment
    87: {"start": 1979, "end": 2021, "tags": ["Soviet invasion of Afghanistan", "US withdrawal from Afghanistan"]},
    88: {"start": 1839, "end": 1842, "tags": []},  # First Anglo-Afghan War
    89: {"start": 1978, "end": 1979, "tags": ["Winter of Discontent"]},  # Climate & Weather (UK 78-79)
    90: {"start": 1914, "end": 1918, "tags": ["World War I"]},  # Western Front
    91: {"start": 1962, "end": 1970, "tags": ["The Beatles release Please Please Me", "The Beatles release Sgt. Pepper's Lonely Hearts Club Band"]},
    92: {"start": 1945, "end": 2000, "tags": ["Atomic bombings of Hiroshima and Nagasaki", "Treaty on the Non-Proliferation of Nuclear Weapons (NPT)"]},
    93: {"start": 1970, "end": 2020, "tags": []},  # Silicon Valley
    95: {"start": 2001, "tags": ["9/11 attacks"]},
    96: None,  # UK's Best Churches
    97: None,  # Top Ten Mistresses
    98: {"start": -480, "end": -479, "tags": ["Battle of Salamis"]},  # Thermopylae/Salamis
    100: {"start": 1957, "end": 1980, "tags": []},  # Decolonising Africa
    101: {"start": 1953, "end": 2026, "tags": []},  # James Bond
    102: {"start": 1949, "end": 2021, "tags": []},  # Germany Adenauer to Angela
    103: {"start": 1180, "end": 1400, "tags": []},  # Norse Sagas
    104: {"start": 1606, "tags": ["Shakespeare's Macbeth"]},
    105: None,  # Classics — too thematic
    106: {"start": 1972, "end": 1974, "tags": ["Watergate scandal"]},
    108: {"start": 1760, "end": 1840, "tags": ["Industrial Revolution"]},
    109: {"start": -230000000, "end": -65000000, "tags": ["First dinosaurs", "K-Pg extinction (dinosaurs)"]},
    110: None,  # India in 10 Buildings — too broad
    111: None,  # Golden Ages
    112: {"start": 1100, "end": 1500, "tags": []},  # Medieval Science
    113: None,  # Hallowe'en pagan
    114: {"start": -3000, "end": -1600, "tags": ["Stonehenge", "Stonehenge erected"]},
    115: {"start": 1605, "tags": ["Gunpowder Plot"]},
    116: {"start": -356, "end": -323, "tags": ["Alexander the Great", "Death of Alexander the Great"]},
    118: {"start": 1918, "end": 1919, "tags": []},  # End of WWI Remembrance
    119: None,  # WC K&Q preview
    120: {"start": 1973, "end": 1974, "tags": []},  # Oil Weapon (OPEC embargo)
    121: {"start": -65000, "end": 1770, "tags": []},  # Australia before Cook
    122: {"start": 924, "end": 939, "tags": []},  # Athelstan
    123: None,  # WC K&Q (kings/queens)
    125: {"start": 1947, "end": 2026, "tags": []},  # CIA
    126: {"start": 1798, "end": 1801, "tags": []},  # Napoleon in Egypt (FIX from Alexander)
    127: {"start": -400000, "end": -40000, "tags": ["Neanderthals emerge"]},
    128: {"start": 1869, "end": 1916, "tags": []},  # Rasputin
    129: None,  # Cricket — broad
    130: {"start": 1938, "end": 2026, "tags": []},  # Superheroes
    131: {"start": 1363, "end": 1477, "tags": []},  # Burgundy
    132: {"start": 1843, "tags": ["Charles Dickens", "Dickens's A Christmas Carol"]},  # Christmas Carol (FIX)
    133: None,  # Christmas churches
    134: {"start": -49, "tags": ["Caesar crosses the Rubicon", "Julius Caesar"]},  # Crossing the Rubicon p1
    136: {"start": 1922, "tags": ["Winston Churchill"]},  # 1922 series
    138: {"start": 1483, "end": 1485, "tags": ["Princes in the Tower"]},  # Princes in the Tower (FIX end)
    140: {"start": 1825, "end": 1850, "tags": []},  # Birth of Railways
    141: {"start": 1833, "end": 1885, "tags": []},  # General Gordon
    142: {"start": 1884, "end": 1885, "tags": []},  # Siege of Khartoum (FIX from Victorian era)
    143: {"start": 1649, "tags": ["Execution of Charles I"]},  # Trial of Charles I
    145: {"start": -539, "tags": ["Cyrus conquers Babylon"]},  # Babylon
    146: None,  # Disease vs civilisation — broad
    147: None,  # Disease pandemics
    148: {"start": 800, "end": 1100, "tags": []},  # Vikings East
    149: {"start": 882, "end": 1240, "tags": ["Kievan Rus' begins", "Kievan Rus'"]},  # Birth of Russia

    # ----- 2022 episodes (150-260) -------------------------------------------
    150: None,  # Smuggling
    151: None,  # Valentine's Day
    152: {"start": 1095, "end": 1291, "tags": ["Crusades", "First Crusade"]},  # American Crusades
    153: {"start": 1947, "end": 1991, "tags": ["Cold War"]},  # God and American Empire
    154: None,  # Most Disastrous Party
    155: {"start": 2014, "end": 2026, "tags": ["Russian invasion of Ukraine"]},  # Ukraine and Russia (FIX)
    156: {"start": 376, "end": 476, "tags": ["Fall of Western Roman Empire"]},  # Roman Empire fall (FIX)
    157: {"start": 330, "end": 1453, "tags": []},  # Byzantium
    158: None,  # Killer Fashion
    159: {"start": 1952, "end": 2000, "tags": ["Vladimir Putin"]},  # Young Putin
    160: {"start": 1989, "end": 1991, "tags": ["Dissolution of the Soviet Union"]},  # Fall USSR (FIX)
    161: {"start": 1991, "end": 2000, "tags": ["Vladimir Putin"]},  # Yeltsin (FIX)
    162: {"start": 2000, "end": 2026, "tags": ["Vladimir Putin"]},  # Putin's Russia
    163: {"start": 1864, "end": 1867, "tags": ["French intervention in Mexico"]},  # Last Emperor of Mexico
    164: {"start": 385, "end": 461, "tags": []},  # Saint Patrick
    165: {"start": 1162, "end": 1227, "tags": ["Genghis Khan"]},  # Rise of Genghis
    167: {"start": 1900, "end": 1960, "tags": ["Suez Crisis"]},  # Oil Making Modern (FIX)
    168: {"start": 1900, "end": 2026, "tags": []},  # Oil Conflict
    169: {"start": 1982, "tags": ["Falklands War"]},  # Falklands
    173: {"start": 1966, "end": 1976, "tags": ["Cultural Revolution"]},  # Mao
    174: None,  # Merlin Magic British — too thematic
    175: {"start": 33, "tags": ["Crucifixion of Jesus"]},  # Crucifixion (FIX)
    178: {"start": 1958, "end": 1981, "tags": ["Charles de Gaulle"]},  # French Presidents p1
    180: {"start": 1903, "end": 1950, "tags": ["George Orwell"]},  # England and Englishness
    181: {"start": -1894, "end": -539, "tags": []},  # Birth of Babylon
    182: {"start": 1941, "end": 1942, "tags": ["Operation Barbarossa"]},  # Barbarossa (FIX end)
    183: {"start": 1861, "end": 1865, "tags": []},  # Big Questions w/ Carlin (mostly US Civil War)
    185: {"start": 1890, "end": 1976, "tags": ["Agatha Christie"]},
    186: {"start": 1533, "end": 2022, "tags": ["Elizabeth I", "Elizabeth II"]},  # New Elizabethan Age (both QEs)
    187: {"start": 1901, "end": 2000, "tags": []},  # Australian PMs
    190: {"start": 1837, "end": 2022, "tags": ["Queen Victoria", "Elizabeth II"]},  # Jubilees
    191: None,  # Childbirth
    192: {"start": 1100, "end": 1300, "tags": []},  # Robin Hood (legendary)
    193: {"start": 1939, "end": 2022, "tags": ["Boris Johnson"]},  # How PMs Fall
    194: None,  # The First Fascist — speculative
    195: {"start": -69, "end": -30, "tags": ["Julius Caesar"]},  # Cleopatra (FIX dates)
    199: {"start": -3000, "end": -1500, "tags": ["Stonehenge", "Stonehenge erected"]},
    200: {"start": 1861, "end": 1865, "tags": ["American Civil War"]},  # ACW series (FIX)
    204: {"start": 1939, "tags": ["Gone with the Wind", "Gone with the Wind released"]},
    205: {"start": 2019, "end": 2022, "tags": ["Boris Johnson"]},  # Boris last days (FIX)
    206: None,  # Historical Love Island
    207: {"start": 1788, "end": 1824, "tags": ["Lord Byron"]},  # Byron
    208: {"start": 1903, "end": 1950, "tags": ["George Orwell", "Nineteen Eighty-Four"]},
    209: {"start": 43, "end": 410, "tags": ["Roman Londinium founded"]},  # Londinium (Roman London)
    214: {"start": 1942, "end": 1943, "tags": ["Battle of Stalingrad"]},
    216: None,  # Pigeons
    217: {"start": 165, "end": 180, "tags": ["Antonine Plague"]},
    218: {"start": 500, "end": 565, "tags": []},  # Theodora/Justinian
    221: {"start": 1809, "end": 1811, "tags": ["Lord Byron"]},  # Byron Grand Tour
    222: {"start": 1837, "end": 1901, "tags": []},  # Victorian Holidays
    223: None,  # Sun Sea Sex
    224: None,  # Roman Holidays
    225: {"start": 1892, "end": 1973, "tags": ["The Lord of the Rings"]},  # Tolkien (FIX lifespan)
    226: {"start": 1954, "end": 2003, "tags": ["The Lord of the Rings", "The Lord of the Rings film trilogy"]},
    227: {"start": 1139, "end": 1910, "tags": []},  # Portugal series
    231: {"start": 1926, "end": 2022, "tags": ["Elizabeth II"]},  # QE2 (FIX from Liz I dates)
    233: None,  # Loch Ness
    234: {"start": 1749, "end": 1832, "tags": []},  # Goethe
    235: {"start": 1937, "end": 1945, "tags": ["World War II"]},  # China WW2 (FIX)
    237: {"start": 1926, "end": 1962, "tags": ["Marilyn Monroe"]},
    238: {"start": 1811, "end": 1820, "tags": ["Jane Austen"]},  # Regency
    239: {"start": 1874, "end": 1965, "tags": ["Winston Churchill"]},  # Young Churchill
    242: {"start": 1894, "end": 1979, "tags": []},  # French history on film
    243: {"start": 1805, "tags": ["Battle of Trafalgar", "Horatio Nelson"]},  # Trafalgar (FIX to event year)
    246: {"start": 2022, "tags": []},  # Liz Truss fall
    247: {"start": 1942, "end": 1945, "tags": []},  # Monty & Patton
    248: {"start": 1351, "end": 1547, "tags": ["Henry VIII"]},  # Medieval Treason
    250: {"start": 849, "end": 899, "tags": ["Alfred the Great", "Reign of Alfred the Great"]},
    252: None,  # WC British Imperialism
    255: {"start": 2022, "tags": ["FIFA World Cup 2022 in Qatar"]},

    # ----- World Cup country-survey series (eps 256-285) ---------------------
    256: {"start": 1942, "end": 1943, "tags": ["The Holocaust"]},  # White Rose (FIX from VE Day)
    257: {"start": 1948, "tags": []},  # Somerton Man (FIX from -65000)
    258: {"start": 1948, "tags": []},  # Costa Rica civil war (FIX from -1642)
    259: {"start": 1979, "end": 2026, "tags": []},  # Iran
    260: {"start": 235, "end": 284, "tags": ["Crisis of the Third Century"]},  # Croatia/Diocletian
    261: {"start": 1962, "end": 1973, "tags": []},  # Uruguay Tupamaros (FIX)
    262: {"start": 1942, "end": 1943, "tags": ["Tunisia campaign"]},  # Tunisia
    263: {"start": 1776, "end": 1812, "tags": ["War of 1812"]},  # USA vs England rivalry (FIX)
    264: {"start": 1864, "end": 1867, "tags": ["French intervention in Mexico"]},  # Mexico
    265: {"start": 1932, "tags": ["Founding of Saudi Arabia"]},  # Saudi Arabia
    266: None,  # South Korea Hwang Jini
    267: {"start": 1284, "end": 1997, "tags": ["Glyndŵr crowned Prince of Wales at Machynlleth"]},  # Wales
    268: {"start": 1822, "end": 1889, "tags": []},  # Brazil empire (FIX)
    269: {"start": 1701, "end": 1901, "tags": []},  # Ghana Ashanti (FIX)
    270: {"start": 1772, "end": 1989, "tags": []},  # Poland
    271: {"start": 1525, "end": 1569, "tags": []},  # Belgium (likely Bruegel)
    272: {"start": 1500, "end": 1888, "tags": ["Atlantic slave trade"]},  # Senegal
    273: {"start": 1974, "tags": []},  # Carnation Revolution
    274: {"start": 1509, "end": 1564, "tags": []},  # Switzerland Calvin
    275: {"start": 2022, "tags": ["Argentina wins 2022 FIFA World Cup"]},
    276: None,  # Netherlands Maid of Holland
    277: {"start": 1185, "end": 1868, "tags": []},  # Japan Samurai/Shoguns (FIX)
    278: None,  # France Le Prince — speculative (Henri II's father?)
    279: {"start": 1672, "end": 1725, "tags": ["Peter the Great"]},  # Cameroon
    280: {"start": 1914, "tags": ["Austria-Hungary declares war on Serbia"]},  # Serbia
    281: {"start": 929, "end": 1700, "tags": ["Caliphate of Córdoba"]},  # Spain
    282: {"start": 1920, "end": 1927, "tags": []},  # Morocco Rif War (FIX)
    283: {"start": 1809, "end": 1882, "tags": ["Charles Darwin"]},  # Ecuador/Darwin
    284: {"start": 1943, "tags": []},  # Denmark Great Escape (Jewish rescue)
    285: {"start": 1640, "end": 1701, "tags": []},  # Canada Beaver Wars (FIX)
    286: {"start": 1066, "end": 1625, "tags": ["Norman Conquest of England", "Henry II of England"]},  # England Beef
    287: {"start": -4, "end": 33, "tags": ["Crucifixion of Jesus"]},  # Jesus Christ Mystery
    289: None,  # Drink
    290: {"start": 2022, "tags": []},  # 2022 A History
    291: {"start": 1944, "tags": []},  # Man Who Escaped Auschwitz
    292: {"start": 1941, "end": 1945, "tags": ["The Holocaust"]},  # Holocaust shadow
    293: {"start": 1553, "tags": []},  # Lady Jane Grey (FIX to her actual reign year)
    295: {"start": 1919, "end": 1933, "tags": ["Beer Hall Putsch", "Hitler becomes Chancellor of Germany"]},  # Nazi rise (FIX)
    299: {"start": -1507, "end": -1458, "tags": ["Hatshepsut"]},
    300: {"start": 1912, "end": 1925, "tags": []},  # Real Downton Abbey (Edwardian/Interwar)
    301: {"start": 1452, "end": 1519, "tags": ["Leonardo da Vinci"]},  # Real Da Vinci Code
}
