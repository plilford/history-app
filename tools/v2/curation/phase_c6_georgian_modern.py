"""
Phase C6 — Georgian, Victorian, and Modern UK (1700-2025).
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_BRIT = {"europe": 10, "americas": 4, "asia": 3, "australasia": 3, "africa": 3}
RW_BRIT_GLOBAL = {"europe": 9, "americas": 7, "asia": 7, "australasia": 6, "africa": 6}


def e(master_pri: int, eng_pri: int, **extra) -> dict:
    out = {"master": master_pri, "england": eng_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- Early Hanoverian -----
    {"type": "event", "title": "Act of Union 1707",
     "description": "Parliaments of England and Scotland merge into the Parliament of Great Britain; United Kingdom of Great Britain created.",
     "start_year": 1707, "start_month": 5, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Acts_of_Union_1707",
     "priorities": e(900_000, 950_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "South Sea Bubble bursts",
     "description": "Speculative collapse of South Sea Company stock ruins thousands; Walpole emerges as the dominant political figure.",
     "start_year": 1720,
     "wikipedia": "https://en.wikipedia.org/wiki/South_Sea_Bubble",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Walpole's premiership",
     "description": "Sir Robert Walpole serves as de-facto first Prime Minister; sets the pattern of cabinet government.",
     "start_year": 1721, "end_year": 1742, "start_month": 4, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Robert_Walpole",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Jacobite rising of 1745",
     "description": "Bonnie Prince Charlie lands in Scotland, marches into England before retreating; crushed at Culloden in 1746.",
     "start_year": 1745, "end_year": 1746,
     "wikipedia": "https://en.wikipedia.org/wiki/Jacobite_rising_of_1745",
     "priorities": e(850_000, 910_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Culloden",
     "description": "Cumberland's redcoats crush Jacobite Highland army on Drumossie Moor; ends Jacobitism and presages Highland Clearances.",
     "start_year": 1746, "start_month": 4, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Culloden",
     "priorities": e(860_000, 920_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Seven Years' War",
     "description": "First true world war; Britain wins Canada, India and naval supremacy from France; foundation of First British Empire.",
     "start_year": 1756, "end_year": 1763,
     "wikipedia": "https://en.wikipedia.org/wiki/Seven_Years%27_War",
     "priorities": e(890_000, 930_000, france=890_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Battle of Plassey",
     "description": "Clive defeats Siraj-ud-Daulah in Bengal; foundation of British rule in India.",
     "start_year": 1757, "start_month": 6, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Plassey",
     "priorities": e(880_000, 920_000, india=900_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Battle of the Plains of Abraham",
     "description": "British capture Quebec from France; both commanders (Wolfe, Montcalm) killed; opens conquest of Canada.",
     "start_year": 1759, "start_month": 9, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Plains_of_Abraham",
     "priorities": e(840_000, 890_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Treaty of Paris (1763)",
     "description": "France cedes Canada and most of India to Britain; Britain becomes the dominant European colonial power.",
     "start_year": 1763, "start_month": 2, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Treaty_of_Paris_(1763)",
     "priorities": e(850_000, 900_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Captain Cook's first voyage",
     "description": "James Cook charts New Zealand and Australia's east coast in HMS Endeavour; opens Pacific to British settlement.",
     "start_year": 1768, "end_year": 1771,
     "wikipedia": "https://en.wikipedia.org/wiki/First_voyage_of_James_Cook",
     "priorities": e(880_000, 920_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Wilkes and Liberty riots",
     "description": "John Wilkes' fight against general warrants and his Middlesex election fuels a popular reform movement for press and parliamentary liberties.",
     "start_year": 1763, "end_year": 1774,
     "wikipedia": "https://en.wikipedia.org/wiki/John_Wilkes",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "American War of Independence (British perspective)",
     "description": "Loss of thirteen American colonies; Yorktown defeat ends Britain's First Empire and accelerates pivot to India and Pacific.",
     "start_year": 1775, "end_year": 1783,
     "wikipedia": "https://en.wikipedia.org/wiki/American_Revolutionary_War",
     "priorities": e(910_000, 940_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "First Fleet arrives at Botany Bay",
     "description": "British penal colony established at Port Jackson; founding of European Australia.",
     "start_year": 1788, "start_month": 1, "start_day": 26,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Fleet",
     "priorities": e(880_000, 920_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Slave Trade Act 1807",
     "description": "Britain bans the Atlantic slave trade; Royal Navy West Africa Squadron enforces the ban.",
     "start_year": 1807, "start_month": 3, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Slave_Trade_Act_1807",
     "priorities": e(890_000, 930_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Battle of Trafalgar",
     "description": "Nelson destroys French-Spanish fleet off Cape Trafalgar; secures British naval supremacy for a century.",
     "start_year": 1805, "start_month": 10, "start_day": 21,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Trafalgar",
     "priorities": e(910_000, 950_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "person", "title": "Horatio Nelson",
     "description": "Royal Navy admiral; victor of the Nile and Trafalgar; killed at his greatest victory.",
     "start_year": 1758, "end_year": 1805, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Horatio_Nelson,_1st_Viscount_Nelson",
     "priorities": e(880_000, 930_000, people=920_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Act of Union 1800 (Ireland)",
     "description": "Kingdom of Ireland merged into the United Kingdom of Great Britain and Ireland; Irish Parliament abolished.",
     "start_year": 1801, "start_month": 1, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Acts_of_Union_1800",
     "priorities": e(850_000, 910_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of Waterloo (British perspective)",
     "description": "Wellington and Blücher defeat Napoleon at Waterloo; ends 22 years of war and inaugurates a century of British global dominance.",
     "start_year": 1815, "start_month": 6, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Waterloo",
     "priorities": e(900_000, 950_000, napoleonic=970_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "person", "title": "Duke of Wellington",
     "description": "Victor of Waterloo and Peninsular War; Tory prime minister 1828-30; embodiment of post-Napoleonic British power.",
     "start_year": 1769, "end_year": 1852, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Arthur_Wellesley,_1st_Duke_of_Wellington",
     "priorities": e(870_000, 920_000, people=900_000), "region_weights": RW_BRIT_GLOBAL},

    # ----- Reform era -----
    {"type": "event", "title": "Peterloo Massacre",
     "description": "Yeomanry charge a pro-reform meeting at St Peter's Field, Manchester; 18 dead, hundreds injured; galvanises reform movement.",
     "start_year": 1819, "start_month": 8, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Peterloo_massacre",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Catholic Emancipation",
     "description": "Roman Catholic Relief Act lets Catholics sit in Parliament for first time since the Reformation.",
     "start_year": 1829, "start_month": 4, "start_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/Roman_Catholic_Relief_Act_1829",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Great Reform Act 1832",
     "description": "Reform Act extends the franchise to ~1 in 5 adult men, abolishes rotten boroughs, redistributes seats; the first major step toward British democracy.",
     "start_year": 1832, "start_month": 6, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Reform_Act_1832",
     "priorities": e(880_000, 930_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Slavery Abolition Act 1833",
     "description": "Abolishes slavery throughout most of the British Empire; £20m paid in compensation — to slave-owners, not the freed.",
     "start_year": 1833, "start_month": 8, "start_day": 28,
     "wikipedia": "https://en.wikipedia.org/wiki/Slavery_Abolition_Act_1833",
     "priorities": e(890_000, 940_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Chartism",
     "description": "Working-class mass movement for universal male suffrage, secret ballot, and other democratic reforms; petitions to parliament rejected.",
     "start_year": 1838, "end_year": 1857,
     "wikipedia": "https://en.wikipedia.org/wiki/Chartism",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "First Opium War",
     "description": "Britain forces China to legalise opium imports and cede Hong Kong; opens century of \"unequal treaties\".",
     "start_year": 1839, "end_year": 1842,
     "wikipedia": "https://en.wikipedia.org/wiki/First_Opium_War",
     "priorities": e(870_000, 920_000, china=910_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Repeal of the Corn Laws",
     "description": "Peel's Conservative government repeals tariffs on grain after Irish Famine; ushers in era of British free trade and splits the party.",
     "start_year": 1846, "start_month": 6, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Corn_Laws",
     "priorities": e(860_000, 920_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Great Famine of Ireland",
     "description": "Potato blight plus laissez-faire British policy kills about a million Irish and triggers a similar exodus to North America.",
     "start_year": 1845, "end_year": 1852,
     "wikipedia": "https://en.wikipedia.org/wiki/Great_Famine_(Ireland)",
     "priorities": e(910_000, 950_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Great Exhibition (Crystal Palace)",
     "description": "First World's Fair, held at Joseph Paxton's Crystal Palace in Hyde Park; six million visitors celebrate British industrial and imperial might.",
     "start_year": 1851, "start_month": 5, "start_day": 1, "end_month": 10, "end_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Great_Exhibition",
     "priorities": e(870_000, 920_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Crimean War",
     "description": "Britain and France defeat Russia in Crimea; brutal mismanagement (Light Brigade, Nightingale's hospitals) reshapes army and nursing.",
     "start_year": 1853, "end_year": 1856,
     "wikipedia": "https://en.wikipedia.org/wiki/Crimean_War",
     "priorities": e(860_000, 910_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Indian Rebellion of 1857",
     "description": "Sepoy mutiny in Bengal becomes a general revolt against East India Company rule; suppressed; India placed under Crown.",
     "start_year": 1857, "end_year": 1858,
     "wikipedia": "https://en.wikipedia.org/wiki/Indian_Rebellion_of_1857",
     "priorities": e(890_000, 930_000, india=940_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "British Raj begins",
     "description": "Government of India Act dissolves the East India Company; direct rule by the British Crown follows.",
     "start_year": 1858, "start_month": 8, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/British_Raj",
     "priorities": e(900_000, 940_000, india=950_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Reform Act 1867",
     "description": "Disraeli's act roughly doubles the male electorate by enfranchising urban working class householders; \"leap in the dark\".",
     "start_year": 1867, "start_month": 8, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Reform_Act_1867",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Forster's Education Act 1870",
     "description": "Establishes school boards and elementary schools throughout England and Wales; first step toward universal education.",
     "start_year": 1870, "start_month": 8, "start_day": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Elementary_Education_Act_1870",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Disraeli buys Suez Canal shares",
     "description": "Prime Minister buys Egypt's stake in the Suez Canal Company with a Rothschild loan; secures Britain's route to India.",
     "start_year": 1875, "start_month": 11, "start_day": 25,
     "wikipedia": "https://en.wikipedia.org/wiki/Suez_Canal",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "person", "title": "Benjamin Disraeli",
     "description": "Twice Conservative prime minister; bought Suez shares, made Victoria Empress of India; novelist on the side.",
     "start_year": 1804, "end_year": 1881, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Benjamin_Disraeli",
     "priorities": e(860_000, 920_000, people=900_000), "region_weights": RW_BRIT},

    {"type": "person", "title": "William Gladstone",
     "description": "Four-times Liberal prime minister; pursued Irish Home Rule, expanded franchise, embodied Victorian liberalism.",
     "start_year": 1809, "end_year": 1898, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/William_Ewart_Gladstone",
     "priorities": e(870_000, 920_000, people=910_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Victoria becomes Empress of India",
     "description": "Royal Titles Act adds 'Empress of India' to Victoria's titles; Disraeli's flourish marks high tide of imperial monarchy.",
     "start_year": 1876, "start_month": 5, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Royal_Titles_Act_1876",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Berlin Conference and Scramble for Africa",
     "description": "European powers carve up Africa; Britain ends up with ~30% of the continent, including Egypt, Nigeria, and southern Africa.",
     "start_year": 1884, "end_year": 1885,
     "wikipedia": "https://en.wikipedia.org/wiki/Scramble_for_Africa",
     "priorities": e(890_000, 920_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Representation of the People Act 1884",
     "description": "Third Reform Act extends male householder franchise to the counties; ~60% of adult men can now vote.",
     "start_year": 1884, "start_month": 12, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Representation_of_the_People_Act_1884",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Irish Home Rule defeated",
     "description": "Gladstone's First Home Rule Bill rejected by Commons; splits Liberal party and locks Ireland into 30 more years of struggle.",
     "start_year": 1886, "start_month": 6, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Government_of_Ireland_Bill_1886",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Diamond Jubilee of Queen Victoria",
     "description": "60-year jubilee of Victoria's reign; vast imperial procession through London marks high tide of British Empire confidence.",
     "start_year": 1897, "start_month": 6, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Diamond_Jubilee_of_Queen_Victoria",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Second Boer War",
     "description": "Britain defeats Boer republics in South Africa after embarrassing early setbacks; introduces concentration camps; opens 20th century with imperial shock.",
     "start_year": 1899, "end_year": 1902,
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Boer_War",
     "priorities": e(860_000, 920_000), "region_weights": RW_BRIT_GLOBAL},

    # ----- Edwardian and Great War -----
    {"type": "event", "title": "Death of Queen Victoria",
     "description": "Victoria dies at Osborne House aged 81 after a 63-year reign; her son Edward VII succeeds.",
     "start_year": 1901, "start_month": 1, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/Death_and_state_funeral_of_Queen_Victoria",
     "priorities": e(880_000, 920_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Suffragette movement (WSPU)",
     "description": "Emmeline Pankhurst founds Women's Social and Political Union; militant campaign for the women's vote.",
     "start_year": 1903, "start_month": 10, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Suffragette",
     "priorities": e(870_000, 920_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "People's Budget",
     "description": "Lloyd George's 1909 budget taxes land and wealth to fund pensions and social insurance; Lords block it, triggering constitutional crisis.",
     "start_year": 1909, "start_month": 4, "start_day": 29,
     "wikipedia": "https://en.wikipedia.org/wiki/People%27s_Budget",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Parliament Act 1911",
     "description": "House of Lords stripped of its veto over money bills; reduces Lords' delay power on other bills to two years.",
     "start_year": 1911, "start_month": 8, "start_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Parliament_Act_1911",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Battle of the Somme",
     "description": "British and French offensive on the Western Front; 60,000 British casualties on the first day; 420,000 British by November.",
     "start_year": 1916, "start_month": 7, "start_day": 1, "end_month": 11, "end_day": 18,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Somme",
     "priorities": e(910_000, 950_000, ww1=970_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Representation of the People Act 1918",
     "description": "Vote extended to all men over 21 and women over 30 with property qualification; tripling the electorate.",
     "start_year": 1918, "start_month": 2, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Representation_of_the_People_Act_1918",
     "priorities": e(860_000, 920_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Equal Franchise Act 1928",
     "description": "Women aged 21 and over given vote on the same terms as men; universal adult suffrage achieved.",
     "start_year": 1928, "start_month": 7, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Representation_of_the_People_(Equal_Franchise)_Act_1928",
     "priorities": e(860_000, 920_000), "region_weights": RW_BRIT},

    # ----- Interwar and WW2 -----
    {"type": "event", "title": "General Strike of 1926",
     "description": "9-day TUC sympathy strike in support of miners; collapses without concessions; weakens the labour movement for a generation.",
     "start_year": 1926, "start_month": 5, "start_day": 4, "end_month": 5, "end_day": 13,
     "wikipedia": "https://en.wikipedia.org/wiki/1926_United_Kingdom_general_strike",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Abdication of Edward VIII",
     "description": "Edward VIII abdicates to marry Wallis Simpson; brother George VI takes the throne.",
     "start_year": 1936, "start_month": 12, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Edward_VIII_abdication_crisis",
     "priorities": e(860_000, 910_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Munich Agreement",
     "description": "Chamberlain returns from Munich proclaiming \"peace for our time\" after ceding Sudetenland to Hitler; appeasement at its peak.",
     "start_year": 1938, "start_month": 9, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Munich_Agreement",
     "priorities": e(900_000, 940_000, ww2=920_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Britain declares war on Germany 1939",
     "description": "Chamberlain announces UK is at war with Germany after Hitler ignores ultimatum on Poland.",
     "start_year": 1939, "start_month": 9, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/British_declaration_of_war_on_Germany_(1939)",
     "priorities": e(890_000, 930_000, ww2=950_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Churchill becomes Prime Minister",
     "description": "Churchill replaces Chamberlain on the day Germany invades Western Europe; leads coalition government for the duration.",
     "start_year": 1940, "start_month": 5, "start_day": 10,
     "wikipedia": "https://en.wikipedia.org/wiki/Premiership_of_Winston_Churchill",
     "priorities": e(910_000, 950_000, ww2=950_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Beveridge Report",
     "description": "Beveridge's wartime report on social insurance maps the post-war welfare state and NHS; bestseller.",
     "start_year": 1942, "start_month": 11, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Beveridge_Report",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "D-Day (Operation Overlord)",
     "description": "Allied amphibious invasion of Normandy with major British and Canadian assault sectors on the British-led 2nd Army front.",
     "start_year": 1944, "start_month": 6, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Normandy_landings",
     "priorities": e(940_000, 950_000, ww2=970_000), "region_weights": RW_BRIT_GLOBAL},

    # ----- Post-war / Welfare state / Empire wind-down -----
    {"type": "event", "title": "1945 Labour landslide",
     "description": "Attlee's Labour wins a 145-seat majority; Churchill rejected at the peak of his fame; mandate for welfare state.",
     "start_year": 1945, "start_month": 7, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/1945_United_Kingdom_general_election",
     "priorities": e(880_000, 930_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Indian independence and Partition",
     "description": "Mountbatten oversees rushed partition of British India into India and Pakistan; up to a million die in resulting violence.",
     "start_year": 1947, "start_month": 8, "start_day": 15,
     "wikipedia": "https://en.wikipedia.org/wiki/Partition_of_India",
     "priorities": e(940_000, 950_000, india=970_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "NHS founded",
     "description": "National Health Service launched by Aneurin Bevan; tax-funded, free at point of use; cornerstone of post-war Britain.",
     "start_year": 1948, "start_month": 7, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/National_Health_Service",
     "priorities": e(910_000, 950_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Empire Windrush arrives",
     "description": "Ship from Jamaica brings hundreds of West Indian migrants to Tilbury; symbolic beginning of post-war multi-racial Britain.",
     "start_year": 1948, "start_month": 6, "start_day": 22,
     "wikipedia": "https://en.wikipedia.org/wiki/HMT_Empire_Windrush",
     "priorities": e(860_000, 920_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Coronation of Elizabeth II",
     "description": "First televised British coronation; vast UK and Commonwealth audience watches the 27-year-old queen crowned.",
     "start_year": 1953, "start_month": 6, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Coronation_of_Elizabeth_II",
     "priorities": e(880_000, 930_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Wind of Change speech",
     "description": "Harold Macmillan's Cape Town address signals British acceptance of African decolonisation.",
     "start_year": 1960, "start_month": 2, "start_day": 3,
     "wikipedia": "https://en.wikipedia.org/wiki/Wind_of_Change_(speech)",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Profumo affair",
     "description": "War Secretary Profumo lies to Commons about affair with Christine Keeler; brings down Macmillan government.",
     "start_year": 1963, "start_month": 6, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Profumo_affair",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Abortion Act 1967",
     "description": "Legalises abortion in Great Britain up to 28 weeks (later 24); landmark of liberal social reform.",
     "start_year": 1967, "start_month": 10, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Abortion_Act_1967",
     "priorities": e(830_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Sexual Offences Act 1967",
     "description": "Decriminalises male homosexual acts in private in England and Wales; first step toward LGBT equality.",
     "start_year": 1967, "start_month": 7, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Sexual_Offences_Act_1967",
     "priorities": e(840_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Bloody Sunday (Derry)",
     "description": "British paratroopers kill 14 civil rights marchers in Derry; turning point of the Troubles.",
     "start_year": 1972, "start_month": 1, "start_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/Bloody_Sunday_(1972)",
     "priorities": e(870_000, 920_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Three-Day Week",
     "description": "Energy crisis forces commercial electricity rationing to three consecutive days; brings down Heath government.",
     "start_year": 1974, "start_month": 1, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Three-Day_Week",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Winter of Discontent",
     "description": "Wave of public-sector strikes in 1978-79; rubbish piles up; helps Thatcher to power in May 1979.",
     "start_year": 1978, "end_year": 1979,
     "wikipedia": "https://en.wikipedia.org/wiki/Winter_of_Discontent",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Thatcher becomes Prime Minister",
     "description": "Margaret Thatcher wins 1979 election; first woman PM; begins eleven years of Conservative dominance.",
     "start_year": 1979, "start_month": 5, "start_day": 4,
     "wikipedia": "https://en.wikipedia.org/wiki/Premiership_of_Margaret_Thatcher",
     "priorities": e(890_000, 940_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Privatisation programme (UK)",
     "description": "Thatcher-era privatisations of British Telecom, Gas, Airways, water and rail; reshapes British state and economy.",
     "start_year": 1984, "end_year": 1996,
     "wikipedia": "https://en.wikipedia.org/wiki/Privatisation_in_the_United_Kingdom",
     "priorities": e(850_000, 910_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Poll tax riots",
     "description": "Riots against the community charge in London and elsewhere; helps force Thatcher's resignation later in 1990.",
     "start_year": 1990, "start_month": 3, "start_day": 31,
     "wikipedia": "https://en.wikipedia.org/wiki/Poll_tax_riots",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Black Wednesday",
     "description": "UK forced out of the European Exchange Rate Mechanism after the pound collapses; damages Major government's reputation for competence.",
     "start_year": 1992, "start_month": 9, "start_day": 16,
     "wikipedia": "https://en.wikipedia.org/wiki/Black_Wednesday",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Death of Diana, Princess of Wales",
     "description": "Diana killed in a Paris car crash; unprecedented public mourning shakes the British monarchy.",
     "start_year": 1997, "start_month": 8, "start_day": 31,
     "wikipedia": "https://en.wikipedia.org/wiki/Death_of_Diana,_Princess_of_Wales",
     "priorities": e(890_000, 930_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Scotland devolution referendum (1997)",
     "description": "Scots vote for a devolved Scottish Parliament; sets up Holyrood and reshapes UK politics.",
     "start_year": 1997, "start_month": 9, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/1997_Scottish_devolution_referendum",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Iraq War (UK participation)",
     "description": "Blair joins US invasion of Iraq; 179 British military dead by 2009 withdrawal; defines his domestic legacy.",
     "start_year": 2003, "start_month": 3, "start_day": 20, "end_year": 2009, "end_month": 4, "end_day": 30,
     "wikipedia": "https://en.wikipedia.org/wiki/British_forces_casualties_in_Afghanistan",
     "priorities": e(870_000, 920_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Hutton Inquiry",
     "description": "Inquiry into death of Dr David Kelly clears Blair government; widely seen as a whitewash; damages BBC and public trust.",
     "start_year": 2003, "end_year": 2004,
     "wikipedia": "https://en.wikipedia.org/wiki/Hutton_Inquiry",
     "priorities": e(800_000, 860_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "UK ban on smoking in public places",
     "description": "Smoking prohibited in enclosed public spaces in England from July 2007; Scotland 2006, Wales/NI 2007.",
     "start_year": 2007, "start_month": 7, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Smoking_ban_in_England",
     "priorities": e(810_000, 870_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "MPs' expenses scandal",
     "description": "Daily Telegraph publishes details of fraudulent MP expenses; resignations, repayments, prosecutions; deepens distrust of Westminster.",
     "start_year": 2009, "start_month": 5, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/United_Kingdom_parliamentary_expenses_scandal",
     "priorities": e(820_000, 880_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "2010 UK general election (coalition)",
     "description": "Hung parliament; first peacetime coalition since the 1930s, Conservative-Lib Dem under Cameron and Clegg.",
     "start_year": 2010, "start_month": 5, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/2010_United_Kingdom_general_election",
     "priorities": e(830_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Marriage (Same Sex Couples) Act",
     "description": "Same-sex marriage legalised in England and Wales; first weddings March 2014.",
     "start_year": 2013, "start_month": 7, "start_day": 17,
     "wikipedia": "https://en.wikipedia.org/wiki/Marriage_(Same_Sex_Couples)_Act_2013",
     "priorities": e(850_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Grenfell Tower fire",
     "description": "72 die in tower-block fire in west London; cladding scandal triggers years of inquiry and policy upheaval.",
     "start_year": 2017, "start_month": 6, "start_day": 14,
     "wikipedia": "https://en.wikipedia.org/wiki/Grenfell_Tower_fire",
     "priorities": e(840_000, 890_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "COVID-19 in the UK",
     "description": "Pandemic kills over 230,000 in the UK by end of 2023; three national lockdowns; transforms public services and politics.",
     "start_year": 2020, "start_month": 1, "end_year": 2023, "end_month": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/COVID-19_pandemic_in_the_United_Kingdom",
     "priorities": e(910_000, 940_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Death of Queen Elizabeth II",
     "description": "Queen dies at Balmoral aged 96 after 70-year reign; King Charles III accedes; vast state funeral at Westminster Abbey.",
     "start_year": 2022, "start_month": 9, "start_day": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Death_and_state_funeral_of_Elizabeth_II",
     "priorities": e(910_000, 950_000), "region_weights": RW_BRIT_GLOBAL},

    {"type": "event", "title": "Truss-Kwarteng mini-budget",
     "description": "Liz Truss's tax-cutting mini-budget triggers gilt-market and pension-fund crisis; Truss resigns after 49 days.",
     "start_year": 2022, "start_month": 9, "start_day": 23,
     "wikipedia": "https://en.wikipedia.org/wiki/September_2022_United_Kingdom_mini-budget",
     "priorities": e(840_000, 900_000), "region_weights": RW_BRIT},

    {"type": "event", "title": "Coronation of King Charles III",
     "description": "First British coronation in 70 years; Charles and Camilla crowned at Westminster Abbey.",
     "start_year": 2023, "start_month": 5, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Coronation_of_Charles_III_and_Camilla",
     "priorities": e(860_000, 910_000), "region_weights": RW_BRIT_GLOBAL},
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
