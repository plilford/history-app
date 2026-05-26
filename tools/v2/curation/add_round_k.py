"""
Round K — add subjects routinely referenced by popular history podcasts and
books but missing from master.py. Drawn from
`tools/v2/curation/suggested_new_occurrences.md` with duplicate-checking
against the live dataset done in this session.

For each new person (`type: "person"`, `is_full_life: True`) we ALSO add one
key event from their lifespan IF no existing master.py event already
name-matches them — this keeps the search-bar's lifespan fallback satisfied
without spawning gratuitous duplicates of existing entries.

Run from `tools/`:
    .venv\\Scripts\\python.exe -m v2.curation.add_round_k
    .venv\\Scripts\\python.exe -m v2.validate
    .venv\\Scripts\\python.exe -m v2.import_v2
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from v2.curation.append_entries import append_entries
from v2.data.master import OCCURRENCES as EXISTING

EXISTING_TITLES = {(o.get("title") or "").strip().lower() for o in EXISTING}

START_ID = 1_007_500

# Each entry below is a plain dict, same shape as master.py. Format follows
# the canonical 5-line dict style after the append_entries helper renders it.
# Priorities calibrated against existing similar-tier entries (see session
# trace for the calibration sample).

PERSONS_AND_EVENTS: list[dict] = [
    # ===== US presidents / founding fathers =====
    {"type": "person", "title": "John Adams",
     "start_year": 1735, "start_month": 10, "start_day": 30,
     "end_year": 1826, "end_month": 7, "end_day": 4,
     "is_full_life": True,
     "description": "Founding Father, principal author of the Massachusetts Constitution, diplomat who helped negotiate the Treaty of Paris (1783), and second President of the United States (1797-1801).",
     "wikipedia": "https://en.wikipedia.org/wiki/John_Adams",
     "priorities": {"master": 905000, "people": 920000, "usa": 935000, "us-presidents": 945000},
     "region_weights": {"europe": 5, "americas": 9, "asia": 3, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Alien and Sedition Acts",
     "start_year": 1798, "start_month": 6, "start_day": 18,
     "description": "Four acts signed by John Adams restricting immigration and criminalising criticism of the federal government. Bitterly contested by Jefferson and Madison; central to the 1800 election that unseated Adams.",
     "wikipedia": "https://en.wikipedia.org/wiki/Alien_and_Sedition_Acts",
     "priorities": {"master": 800000, "usa": 850000},
     "region_weights": {"europe": 4, "americas": 8, "asia": 3, "australasia": 3, "africa": 3}},

    {"type": "person", "title": "Alexander Hamilton",
     "start_year": 1755, "start_month": 1, "start_day": 11,
     "end_year": 1804, "end_month": 7, "end_day": 12,
     "is_full_life": True,
     "description": "Founding Father, principal author of the Federalist Papers, first U.S. Secretary of the Treasury who built the financial architecture of the new republic. Killed in a duel with Aaron Burr in 1804.",
     "wikipedia": "https://en.wikipedia.org/wiki/Alexander_Hamilton",
     "priorities": {"master": 900000, "people": 915000, "usa": 925000},
     "region_weights": {"europe": 4, "americas": 9, "asia": 3, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Burr-Hamilton duel",
     "start_year": 1804, "start_month": 7, "start_day": 11,
     "description": "Vice-President Aaron Burr mortally wounds Alexander Hamilton in a pistol duel at Weehawken, New Jersey. Hamilton dies the following day; Burr's political career is destroyed.",
     "wikipedia": "https://en.wikipedia.org/wiki/Burr%E2%80%93Hamilton_duel",
     "priorities": {"master": 850000, "usa": 880000},
     "region_weights": {"europe": 4, "americas": 8, "asia": 3, "australasia": 3, "africa": 3}},

    {"type": "person", "title": "Ulysses S. Grant",
     "start_year": 1822, "start_month": 4, "start_day": 27,
     "end_year": 1885, "end_month": 7, "end_day": 23,
     "is_full_life": True,
     "description": "Commanding general of the Union Army in the final years of the American Civil War; accepted Lee's surrender at Appomattox in 1865. Served as 18th President of the United States (1869-1877).",
     "wikipedia": "https://en.wikipedia.org/wiki/Ulysses_S._Grant",
     "priorities": {"master": 890000, "people": 905000, "usa": 920000, "us-presidents": 930000},
     "region_weights": {"europe": 4, "americas": 9, "asia": 3, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Siege of Vicksburg",
     "start_year": 1863, "start_month": 5, "start_day": 18,
     "end_year": 1863, "end_month": 7, "end_day": 4,
     "description": "Grant's 47-day siege of the Confederate stronghold on the Mississippi ends with the surrender of Pemberton's army on 4 July 1863, cleaving the Confederacy in two. Coincides with Gettysburg as the turning point of the Civil War.",
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Vicksburg",
     "first_zoom_out": "American Civil War",
     "priorities": {"master": 920000, "usa": 950000},
     "region_weights": {"europe": 4, "americas": 9, "asia": 3, "australasia": 3, "africa": 3}},

    {"type": "person", "title": "Lyndon B. Johnson",
     "start_year": 1908, "start_month": 8, "start_day": 27,
     "end_year": 1973, "end_month": 1, "end_day": 22,
     "is_full_life": True,
     "description": "36th President of the United States, sworn in after JFK's assassination in 1963. Architect of the Great Society and the Civil Rights and Voting Rights Acts; presided over the escalation of the Vietnam War.",
     "wikipedia": "https://en.wikipedia.org/wiki/Lyndon_B._Johnson",
     "priorities": {"master": 905000, "people": 920000, "usa": 935000, "us-presidents": 945000},
     "region_weights": {"europe": 4, "americas": 9, "asia": 4, "australasia": 3, "africa": 3}},
    # Gulf of Tonkin already exists; lifespan satisfied by Presidency of LBJ + Civil Rights / Voting Rights Acts.

    {"type": "person", "title": "Richard Nixon",
     "start_year": 1913, "start_month": 1, "start_day": 9,
     "end_year": 1994, "end_month": 4, "end_day": 22,
     "is_full_life": True,
     "description": "37th President of the United States (1969-1974). Opened relations with China, ended US ground combat in Vietnam, and resigned in disgrace over the Watergate scandal — the only President to do so.",
     "wikipedia": "https://en.wikipedia.org/wiki/Richard_Nixon",
     "priorities": {"master": 925000, "people": 935000, "usa": 945000, "us-presidents": 955000},
     "region_weights": {"europe": 4, "americas": 9, "asia": 5, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Resignation of Richard Nixon",
     "start_year": 1974, "start_month": 8, "start_day": 9,
     "description": "Facing certain impeachment over the Watergate cover-up, Nixon becomes the only US President to resign. Gerald Ford is sworn in the same day and pardons Nixon a month later.",
     "wikipedia": "https://en.wikipedia.org/wiki/Resignation_of_Richard_Nixon",
     "first_zoom_out": "Watergate scandal",
     "priorities": {"master": 940000, "usa": 960000},
     "region_weights": {"europe": 4, "americas": 9, "asia": 3, "australasia": 3, "africa": 3}},

    {"type": "person", "title": "Harry S. Truman",
     "start_year": 1884, "start_month": 5, "start_day": 8,
     "end_year": 1972, "end_month": 12, "end_day": 26,
     "is_full_life": True,
     "description": "33rd President of the United States, sworn in days before VE-day. Authorised the atomic bombings of Hiroshima and Nagasaki, launched the Marshall Plan and the Truman Doctrine, and committed US forces to the Korean War.",
     "wikipedia": "https://en.wikipedia.org/wiki/Harry_S._Truman",
     "priorities": {"master": 920000, "people": 930000, "usa": 940000, "us-presidents": 950000},
     "region_weights": {"europe": 6, "americas": 9, "asia": 5, "australasia": 3, "africa": 3}},
    # Truman Doctrine, Marshall Plan, Hiroshima/Nagasaki, Korean War already exist.

    # ===== Roman emperors =====
    {"type": "person", "title": "Nero",
     "start_year": 37, "start_month": 12, "start_day": 15,
     "end_year": 68, "end_month": 6, "end_day": 9,
     "is_full_life": True,
     "description": "Fifth Roman Emperor (54-68 AD); last of the Julio-Claudian dynasty. Notorious in tradition for his persecution of Christians after the Great Fire of Rome (64); died by suicide as the legions revolted.",
     "wikipedia": "https://en.wikipedia.org/wiki/Nero",
     "priorities": {"master": 905000, "people": 920000, "roman-history": 930000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 4, "australasia": 3, "africa": 4}},
    # Reign of Nero + Great Fire of Rome already exist.

    {"type": "person", "title": "Hadrian",
     "start_year": 76, "start_month": 1, "start_day": 24,
     "end_year": 138, "end_month": 7, "end_day": 10,
     "is_full_life": True,
     "description": "14th Roman Emperor (117-138). Consolidated empire on defensible borders — most famously the wall across northern Britain that bears his name. Patron of Greek culture and architect-emperor.",
     "wikipedia": "https://en.wikipedia.org/wiki/Hadrian",
     "priorities": {"master": 890000, "people": 905000, "roman-history": 920000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 5, "australasia": 3, "africa": 4}},
    # Hadrian's Wall built + Bar Kokhba revolt already exist.

    # ===== Economist =====
    {"type": "person", "title": "John Maynard Keynes",
     "start_year": 1883, "start_month": 6, "start_day": 5,
     "end_year": 1946, "end_month": 4, "end_day": 21,
     "is_full_life": True,
     "description": "British economist whose General Theory (1936) overturned classical orthodoxy and underpinned post-war macroeconomic policy. Lead UK delegate at Bretton Woods (1944), architect of the IMF and World Bank.",
     "wikipedia": "https://en.wikipedia.org/wiki/John_Maynard_Keynes",
     "priorities": {"master": 890000, "people": 905000, "arts-and-thoughts": 920000},
     "region_weights": {"europe": 7, "americas": 6, "asia": 4, "australasia": 4, "africa": 3}},
    {"type": "art", "title": "Keynes publishes The General Theory",
     "start_year": 1936, "start_month": 2, "start_day": 4,
     "description": "The General Theory of Employment, Interest and Money — Keynes's argument that aggregate demand drives output and employment, justifying counter-cyclical fiscal policy. Foundational text of modern macroeconomics.",
     "wikipedia": "https://en.wikipedia.org/wiki/The_General_Theory_of_Employment,_Interest_and_Money",
     "priorities": {"master": 870000, "arts-and-thoughts": 910000},
     "region_weights": {"europe": 7, "americas": 6, "asia": 4, "australasia": 4, "africa": 3}},

    # ===== Henry VIII's wives =====
    {"type": "person", "title": "Catherine of Aragon",
     "start_year": 1485, "start_month": 12, "start_day": 16,
     "end_year": 1536, "end_month": 1, "end_day": 7,
     "is_full_life": True,
     "description": "First wife of Henry VIII (married 1509), daughter of Ferdinand and Isabella of Spain. Her refusal to consent to annulment triggered the English Reformation and the break with Rome.",
     "wikipedia": "https://en.wikipedia.org/wiki/Catherine_of_Aragon",
     "priorities": {"master": 860000, "people": 880000, "england": 890000, "england-monarchs": 895000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 3, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Marriage of Henry VIII and Catherine of Aragon",
     "start_year": 1509, "start_month": 6, "start_day": 11,
     "description": "Henry weds his late brother Arthur's widow at Greenwich, six weeks after his accession. The 24-year marriage produces only one surviving child, Mary, and ends in the annulment that breaks England from Rome.",
     "wikipedia": "https://en.wikipedia.org/wiki/Catherine_of_Aragon",
     "priorities": {"master": 800000, "england": 850000, "england-monarchs": 860000},
     "region_weights": {"europe": 7, "americas": 3, "asia": 3, "australasia": 3, "africa": 3}},

    {"type": "person", "title": "Mary Boleyn",
     "start_year": 1499,
     "end_year": 1543, "end_month": 7, "end_day": 19,
     "is_full_life": True,
     "description": "Elder sister of Anne Boleyn and mistress of Henry VIII before he turned his attention to Anne. Her quiet second marriage to William Stafford (1534) outraged the Boleyn family but kept her clear of the executioner.",
     "wikipedia": "https://en.wikipedia.org/wiki/Mary_Boleyn",
     "priorities": {"master": 790000, "people": 820000, "england": 830000, "england-monarchs": 835000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 3, "australasia": 3, "africa": 3}},

    {"type": "person", "title": "Jane Seymour",
     "start_year": 1508,
     "end_year": 1537, "end_month": 10, "end_day": 24,
     "is_full_life": True,
     "description": "Third wife of Henry VIII (married 1536); only one of his wives to bear him a surviving son, the future Edward VI. Died of childbed complications twelve days after the birth — Henry mourned her for years.",
     "wikipedia": "https://en.wikipedia.org/wiki/Jane_Seymour",
     "priorities": {"master": 830000, "people": 855000, "england": 865000, "england-monarchs": 870000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 3, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Death of Jane Seymour",
     "start_year": 1537, "start_month": 10, "start_day": 24,
     "description": "Twelve days after giving birth to the future Edward VI, Jane Seymour dies of postnatal complications at Hampton Court. Henry VIII, who had finally got a male heir, mourned her as his 'true love'.",
     "wikipedia": "https://en.wikipedia.org/wiki/Jane_Seymour",
     "priorities": {"master": 780000, "england": 830000, "england-monarchs": 840000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 3, "australasia": 3, "africa": 3}},

    {"type": "person", "title": "Catherine Howard",
     "start_year": 1523,
     "end_year": 1542, "end_month": 2, "end_day": 13,
     "is_full_life": True,
     "description": "Fifth wife of Henry VIII (married 1540); a teenage cousin of Anne Boleyn. Executed on Tower Green after barely 19 months as queen, accused of adultery with Thomas Culpeper.",
     "wikipedia": "https://en.wikipedia.org/wiki/Catherine_Howard",
     "priorities": {"master": 820000, "people": 848000, "england": 855000, "england-monarchs": 860000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 3, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Execution of Catherine Howard",
     "start_year": 1542, "start_month": 2, "start_day": 13,
     "description": "Henry VIII's fifth queen is beheaded on Tower Green after evidence of premarital relationships and an alleged affair with Thomas Culpeper. Her lady-in-waiting Jane Boleyn (Anne's sister-in-law) is executed beside her.",
     "wikipedia": "https://en.wikipedia.org/wiki/Catherine_Howard",
     "priorities": {"master": 790000, "england": 840000, "england-monarchs": 850000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 3, "australasia": 3, "africa": 3}},

    {"type": "person", "title": "Catherine Parr",
     "start_year": 1512,
     "end_year": 1548, "end_month": 9, "end_day": 5,
     "is_full_life": True,
     "description": "Sixth and last wife of Henry VIII (married 1543); outlived him to remarry Thomas Seymour. The first English queen to publish original prose under her own name, and a Protestant influence on Henry's children.",
     "wikipedia": "https://en.wikipedia.org/wiki/Catherine_Parr",
     "priorities": {"master": 830000, "people": 853000, "england": 862000, "england-monarchs": 867000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 3, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Catherine Parr marries Henry VIII",
     "start_year": 1543, "start_month": 7, "start_day": 12,
     "description": "Twice-widowed Catherine Parr becomes Henry VIII's sixth and final wife at Hampton Court. She outlives him by 19 months and brings the king's three children together at court for the first time.",
     "wikipedia": "https://en.wikipedia.org/wiki/Catherine_Parr",
     "priorities": {"master": 770000, "england": 815000, "england-monarchs": 825000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 3, "australasia": 3, "africa": 3}},

    # ===== Cold War / 20c leaders =====
    {"type": "person", "title": "Fidel Castro",
     "start_year": 1926, "start_month": 8, "start_day": 13,
     "end_year": 2016, "end_month": 11, "end_day": 25,
     "is_full_life": True,
     "description": "Cuban revolutionary leader who overthrew Batista in 1959 and ruled Cuba as Prime Minister and then President for nearly five decades. Defining figure of Cold War Latin America.",
     "wikipedia": "https://en.wikipedia.org/wiki/Fidel_Castro",
     "priorities": {"master": 940000, "people": 952000},
     "region_weights": {"europe": 5, "americas": 9, "asia": 4, "australasia": 3, "africa": 4}},
    # Castro takes Havana + Cuban Revolution + Bay of Pigs + Cuban Missile Crisis already exist.

    {"type": "person", "title": "Josip Broz Tito",
     "start_year": 1892, "start_month": 5, "start_day": 7,
     "end_year": 1980, "end_month": 5, "end_day": 4,
     "is_full_life": True,
     "description": "Yugoslav Partisan leader and post-war head of state who held a multi-ethnic federation together for 35 years. Broke with Stalin in 1948 to found the Non-Aligned Movement; Yugoslavia disintegrated within a decade of his death.",
     "wikipedia": "https://en.wikipedia.org/wiki/Josip_Broz_Tito",
     "priorities": {"master": 885000, "people": 900000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 4, "australasia": 3, "africa": 4}},
    {"type": "event", "title": "Tito-Stalin split",
     "start_year": 1948, "start_month": 6, "start_day": 28,
     "description": "The Cominform expels Yugoslavia at Soviet insistence after Tito refuses to subordinate his country to Moscow. The first major rupture in the Eastern bloc; sets the template for non-alignment.",
     "wikipedia": "https://en.wikipedia.org/wiki/Tito%E2%80%93Stalin_split",
     "priorities": {"master": 880000},
     "region_weights": {"europe": 8, "americas": 4, "asia": 4, "australasia": 3, "africa": 4}},

    {"type": "person", "title": "Konrad Adenauer",
     "start_year": 1876, "start_month": 1, "start_day": 5,
     "end_year": 1967, "end_month": 4, "end_day": 19,
     "is_full_life": True,
     "description": "First Chancellor of the Federal Republic of Germany (1949-1963). Anchored West Germany in the Western alliance, secured Franco-German reconciliation, and oversaw the Wirtschaftswunder economic recovery.",
     "wikipedia": "https://en.wikipedia.org/wiki/Konrad_Adenauer",
     "priorities": {"master": 855000, "people": 875000, "germany": 905000},
     "region_weights": {"europe": 8, "americas": 4, "asia": 3, "australasia": 3, "africa": 3}},
    # Adenauer's chancellorship + Treaty of Rome / EEC already exist.

    # ===== American Civil War battles =====
    {"type": "event", "title": "Battle of Antietam",
     "start_year": 1862, "start_month": 9, "start_day": 17,
     "description": "Bloodiest single day in American history (~22,700 casualties). McClellan halts Lee's first invasion of the North in Maryland; Lincoln uses the tactical Union outcome to issue the Emancipation Proclamation five days later.",
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Antietam",
     "first_zoom_out": "American Civil War",
     "priorities": {"master": 920000, "usa": 945000},
     "region_weights": {"europe": 4, "americas": 9, "asia": 3, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Battle of Fredericksburg",
     "start_year": 1862, "start_month": 12, "start_day": 11,
     "end_year": 1862, "end_month": 12, "end_day": 15,
     "description": "Crushing Confederate defensive victory in Virginia: Burnside's repeated assaults on Lee's prepared positions on Marye's Heights cost the Union 12,600 casualties to the Confederates' 5,400.",
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Fredericksburg",
     "first_zoom_out": "American Civil War",
     "priorities": {"master": 850000, "usa": 900000},
     "region_weights": {"europe": 4, "americas": 9, "asia": 3, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Battle of Chancellorsville",
     "start_year": 1863, "start_month": 4, "start_day": 30,
     "end_year": 1863, "end_month": 5, "end_day": 6,
     "description": "Lee's tactical masterpiece against a Union force more than twice his size, but at the cost of Stonewall Jackson — mortally wounded by his own pickets after his flanking march. The high-water mark of Confederate generalship.",
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Chancellorsville",
     "first_zoom_out": "American Civil War",
     "priorities": {"master": 870000, "usa": 910000},
     "region_weights": {"europe": 4, "americas": 9, "asia": 3, "australasia": 3, "africa": 3}},

    # ===== Modern conflicts =====
    {"type": "event", "title": "Battle of Mogadishu",
     "start_year": 1993, "start_month": 10, "start_day": 3,
     "end_year": 1993, "end_month": 10, "end_day": 4,
     "description": "US Rangers and Delta Force attempt to capture lieutenants of Somali warlord Aidid; two Black Hawk helicopters are shot down and a 15-hour urban firefight follows. 18 American and several hundred Somali deaths; pulls the US out of Somalia and conditions Clinton-era restraint on intervention.",
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Mogadishu_(1993)",
     "priorities": {"master": 845000, "usa": 870000},
     "region_weights": {"europe": 4, "americas": 7, "asia": 3, "australasia": 3, "africa": 8}},
    {"type": "event", "title": "Bosnian War",
     "start_year": 1992, "start_month": 4, "start_day": 6,
     "end_year": 1995, "end_month": 12, "end_day": 14,
     "description": "Multi-sided war in the former Yugoslavia involving Bosniaks, Bosnian Serbs and Bosnian Croats. Saw the worst atrocities in Europe since 1945 — including the Srebrenica genocide — and ended with the Dayton Accords.",
     "wikipedia": "https://en.wikipedia.org/wiki/Bosnian_War",
     "priorities": {"master": 905000},
     "region_weights": {"europe": 9, "americas": 5, "asia": 4, "australasia": 3, "africa": 3}},
    {"type": "event", "title": "Siege of Sarajevo",
     "start_year": 1992, "start_month": 4, "start_day": 5,
     "end_year": 1996, "end_month": 2, "end_day": 29,
     "description": "Longest siege of a capital city in modern warfare (1,425 days). Bosnian Serb forces shell Sarajevo from the surrounding hills; an estimated 13,952 are killed, including 5,434 civilians.",
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Sarajevo",
     "first_zoom_out": "Bosnian War",
     "priorities": {"master": 890000},
     "region_weights": {"europe": 9, "americas": 4, "asia": 4, "australasia": 3, "africa": 3}},

    # ===== Roman / classical =====
    {"type": "event", "title": "Catilinarian conspiracy",
     "start_year": -63,
     "description": "Cicero, in his consular year, exposes Lucius Sergius Catilina's plot to overthrow the Roman Republic. The conspirators are executed without trial under the senatus consultum ultimum — an act that haunts Cicero for the rest of his career.",
     "wikipedia": "https://en.wikipedia.org/wiki/Catilinarian_conspiracy",
     "display_date": "63 BCE",
     "priorities": {"master": 830000, "roman-history": 880000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 4, "australasia": 3, "africa": 4}},
    {"type": "event", "title": "Second Punic War",
     "start_year": -218,
     "end_year": -201,
     "description": "Carthage versus Rome, decided by Hannibal's audacious crossing of the Alps, his victories at Trebia, Lake Trasimene and Cannae, and Scipio Africanus's eventual counter-stroke at Zama in 202 BCE. Confirms Roman dominance of the western Mediterranean.",
     "wikipedia": "https://en.wikipedia.org/wiki/Second_Punic_War",
     "display_date": "218-201 BCE",
     "priorities": {"master": 920000, "roman-history": 950000},
     "region_weights": {"europe": 8, "americas": 3, "asia": 4, "australasia": 3, "africa": 7}},

    # ===== Cold War endgame =====
    {"type": "event", "title": "Fall of the Berlin Wall",
     "start_year": 1989, "start_month": 11, "start_day": 9,
     "description": "East Germany opens its border crossings after a botched Politburo announcement; thousands of East Berliners stream into the West. Symbolic end of the Iron Curtain and trigger for German reunification.",
     "wikipedia": "https://en.wikipedia.org/wiki/Fall_of_the_Berlin_Wall",
     "priorities": {"master": 990000, "germany": 990000, "cold-war": 990000},
     "region_weights": {"europe": 9, "americas": 7, "asia": 5, "australasia": 4, "africa": 4}},
]


def assign_ids(entries: list[dict], start: int) -> list[dict]:
    """Mutate in place — give each entry a sequential ID starting at `start`."""
    nid = start
    for e in entries:
        e["id"] = nid
        nid += 1
    return entries


def main() -> int:
    # Pre-flight: warn (and skip) any entry whose title already exists.
    fresh: list[dict] = []
    skipped: list[tuple[str, int]] = []
    for e in PERSONS_AND_EVENTS:
        t = e["title"].strip().lower()
        if t in EXISTING_TITLES:
            existing = next(o for o in EXISTING if (o.get("title") or "").strip().lower() == t)
            skipped.append((e["title"], existing["id"]))
            continue
        fresh.append(e)

    print(f"Total drafted: {len(PERSONS_AND_EVENTS)}")
    print(f"Already in master.py (skipped): {len(skipped)}")
    for title, eid in skipped:
        print(f"  skip {title!r} (existing id={eid})")
    print(f"To append: {len(fresh)}")

    if not fresh:
        print("Nothing to append — exiting cleanly.")
        return 0

    assign_ids(fresh, START_ID)
    n = append_entries(fresh)
    print(f"Appended {n} entries to master.py (ids {fresh[0]['id']}..{fresh[-1]['id']})")

    # Counts by type for the record.
    from collections import Counter
    by_type = Counter(e["type"] for e in fresh)
    for t, c in by_type.most_common():
        print(f"  {t}: {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
