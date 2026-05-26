# Suggested new occurrences for master.py

Compiled from gaps surfaced during TRIH episode + books curation
(2026-05-26 session). These are subjects routinely referenced by
popular history podcasts and books but absent or only present as
a related (presidency / reign / event-about-them) entry, making
tag matches harder.

Reserve an ID range for this batch (e.g. `1_007_500 – 1_007_700`).
After importing, run:

```
cd tools
python -m v2.curation.suggest_resource_tags --since 1_007_500
```

…then add the new titles to the relevant resources' `tags` lists.

---

## Persons (`type: "person"`, `is_full_life: True`)

People often referenced but missing the person-entry (only an event
or presidency entry exists). Include `priorities: {"master": <pri>, "people": <pri>}`
plus any country slug (e.g. `usa`, `england`).

- Cicero (-106 to -43)
- John Adams (1735 - 1826)
- John F. Kennedy (1917 - 1963)
- Lyndon B. Johnson (1908 - 1973)
- Richard Nixon (1913 - 1994)
- Joseph Stalin (1878 - 1953)
- Mao Zedong (1893 - 1976)
- Charles I of England (1600 - 1649)
- Mary, Queen of Scots (1542 - 1587)
- Joan of Arc (1412 - 1431)
- Thomas Cromwell (1485 - 1540)
- Augustus / Octavian (-63 to 14)
- Nero (37 - 68)
- Hadrian (76 - 138)
- John Maynard Keynes (1883 - 1946)
- Anne Frank (1929 - 1945)
- Frida Kahlo (1907 - 1954)
- Indira Gandhi (1917 - 1984)
- Jawaharlal Nehru (1889 - 1964)
- Nelson Mandela (1918 - 2013)
- Harry S. Truman (1884 - 1972)
- Ulysses S. Grant (1822 - 1885)
- Alexander Hamilton (1755 - 1804)
- George Washington (1732 - 1799)
- Catherine the Great (1729 - 1796)
- Abraham Lincoln (1809 - 1865)
- Anne Boleyn (1501 - 1536)
- Jane Seymour (1508 - 1537)
- Mary Boleyn (1499 - 1543)
- Catherine of Aragon (1485 - 1536)
- Catherine Howard (1523 - 1542)
- Catherine Parr (1512 - 1548)
- Saladin (1137 - 1193)
- Tamerlane (1336 - 1405)
- Suleiman the Magnificent (1494 - 1566)
- Akbar the Great (1542 - 1605)
- Bismarck (1815 - 1898)
- Kemal Atatürk (1881 - 1938)
- Tito (1892 - 1980)
- Castro (1926 - 2016)
- Lenin (1870 - 1924) — check whether already there as event
- Trotsky (1879 - 1940)
- Khrushchev (1894 - 1971)
- Gorbachev (1931 - 2022)
- Mussolini (already exists)
- de Gaulle (already exists)
- Konrad Adenauer (1876 - 1967)

## Specific battles / events (`type: "event"`)

- Outbreak of World War I (28 July 1914) — a specific point distinct from "World War I" period
- Battle of the Somme (1 Jul - 18 Nov 1916)
- Battle of Verdun (21 Feb - 18 Dec 1916) — convert from point to period
- Battle of Borodino (7 Sep 1812)
- Battle of Antietam (17 Sep 1862)
- Battle of Chancellorsville (30 Apr - 6 May 1863)
- Battle of Fredericksburg (11-15 Dec 1862)
- Battle of Mogadishu (3-4 Oct 1993)
- Tet Offensive (30 Jan - 23 Sep 1968)
- Storming of the Bastille (14 Jul 1789)
- Execution of Louis XVI (21 Jan 1793)
- Reign of Terror (5 Sep 1793 - 28 Jul 1794) — period
- Assassination of Archduke Franz Ferdinand (28 Jun 1914)
- Sinking of the Lusitania (7 May 1915)
- Cuban Missile Crisis (16-29 Oct 1962)
- Cuban Revolution (26 Jul 1953 - 1 Jan 1959) — period
- Spanish-American War (1898) — period
- Biafran War (1967-1970) — period
- Bosnian War (1992-1995) — period
- Siege of Sarajevo (1992-1996) — period
- Catiline conspiracy (63 BCE)
- First / Second / Third Punic War (-264 to -146) — three periods
- Peloponnesian War (-431 to -404) — period
- Battle of Bosworth Field (22 Aug 1485)
- Wars of the Roses (1455-1487) — period umbrella
- Battle of Agincourt (25 Oct 1415)
- Anarchy in England (already exists)
- English Reformation (1534-1559) — already exists?
- Luther's 95 Theses (31 Oct 1517)
- Council of Trent (already exists)
- Edict of Nantes (1598)
- Glorious Revolution (already exists)
- Magna Carta (already exists — verify)
- Norman Conquest of England (already exists)
- Hundred Years' War (1337-1453) — umbrella period
- Fall of Constantinople (already exists)
- Spanish Armada (already exists)
- English Civil War (1642-1651) — period
- Cromwell's Protectorate (already exists)
- Execution of Charles I (already exists)
- Battle of Salamis (already exists)
- Battle of Thermopylae (already exists)
- Death of Alexander the Great (already exists)
- Assassination of Julius Caesar (already exists?)
- Roman Republic founded (753 BCE-ish — verify)
- Constitutio Antoniniana (212 CE)
- Bombing of Dresden (13-15 Feb 1945)
- North African Campaign (1940-1943)
- Battle of Britain (1940)
- Dunkirk evacuation (26 May - 4 Jun 1940)
- The Blitz (7 Sep 1940 - 11 May 1941)
- Battle of Midway (4-7 Jun 1942)
- Battle of Iwo Jima (19 Feb - 26 Mar 1945)
- Pearl Harbor attack (7 Dec 1941)
- Operation Market Garden (17-25 Sep 1944)
- Battle of the Bulge (16 Dec 1944 - 25 Jan 1945)
- Marshall Plan (1948-1952)
- Berlin Airlift (1948-1949)
- Korean War (1950-1953)
- McCarthy hearings (1953-1954)
- Suez Crisis (already exists)
- Cuban Missile Crisis (above)
- Civil Rights Act 1964 (US)
- Voting Rights Act 1965 (US)
- Tiananmen Square protests (3-4 Jun 1989)
- Fall of the Berlin Wall (9 Nov 1989) — distinct from "Construction of"
- Dissolution of the Soviet Union (already exists)

## Works of art / books / ideas (`type: "art"`)

Many already exist; suggestions for gaps:

- The Wealth of Nations (Adam Smith, 1776)
- On the Origin of Species (already exists)
- The Communist Manifesto (1848)
- Das Kapital (Marx, vol 1 1867)
- The Federalist Papers (1787-1788)
- Hamilton (musical) — already exists as "Hamilton premieres on Broadway"
- The Iliad (Homer, ~750 BCE)
- The Odyssey (Homer, ~750 BCE)
- Aeneid (Virgil, ~19 BCE)
- Confessions (Augustine, 397)
- City of God (Augustine, 426)
- Summa Theologica (Aquinas, 1265-1274)
- Divine Comedy (Dante, 1320) — already exists
- Prince (Machiavelli, 1532)
- Don Quixote (Cervantes, 1605/1615)
- Leviathan (Hobbes, 1651)
- Principia Mathematica (Newton, 1687)
- Wealth of Nations (above)
- Critique of Pure Reason (Kant, 1781)
- Origin of Species (above)
- War and Peace (Tolstoy, 1869) — already exists
- 1984 (Orwell, 1949) — already exists as "Nineteen Eighty-Four"

## Notes

- Run `validate.py` after appending — any tags that match these new titles
  will resolve, lifting the silent-drop rate on resource tags.
- After import, run the tag suggester (see CLAUDE.md "Authoring a new
  SUBJECT") so existing resources get linked to the new subjects.
- Many of these may already exist under slightly different names — grep
  before adding to avoid duplicates.
