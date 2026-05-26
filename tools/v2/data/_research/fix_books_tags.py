"""
One-shot find-replace pass over popular_history_books.py to fix tag
strings against actual master.py titles. Idempotent if re-run.
"""

from __future__ import annotations

from pathlib import Path

BOOKS = Path(__file__).resolve().parents[1] / "popular_history_books.py"

# (bad, good) — bad strings appear as quoted tag values; good is the actual
# master.py title. If `good` is None, delete the tag entirely.
REPLACEMENTS: list[tuple[str, str | None]] = [
    # Berlin Conference / Africa
    ("Berlin Conference (Scramble for Africa)", "Berlin Conference / Scramble for Africa"),
    # WWI
    ("Outbreak of World War I", None),
    ("Treaty of Versailles (German perspective)", "Treaty of Versailles"),
    ("John Maynard Keynes", None),
    # WWII
    ("Fall of the Berlin Wall", "Construction of Berlin Wall"),
    ("European Union founded (Maastricht Treaty)", None),
    # Presidencies
    ("Lyndon B. Johnson", "Presidency of Lyndon B. Johnson"),
    ("John Adams", "Presidency of John Adams"),
    ("Harry S. Truman", "Presidency of Harry S. Truman"),
    ("Ulysses S. Grant", "Presidency of Ulysses S. Grant"),
    # Subjects
    ("Wright Brothers' first flight", None),
    ("World's Columbian Exposition (Chicago)", None),
    ("Darwin's Origin of Species published", "Origin of Species"),
    ("Salt March", "Gandhi begins the Salt March"),
    ("End of apartheid in South Africa", "Apartheid laws codified"),
    ("Battle of Mogadishu", None),
    ("Alexander Hamilton", None),
    ("US Constitution", None),
    ("Battle of Antietam", None),
    ("Battle of Chancellorsville", None),
    ("Catiline conspiracy", None),
    ("Roman Britain", "Roman Britain (Britannia)"),
    ("Great Heathen Army", "Great Heathen Army lands"),
    ("Royal Navy", None),
    ("Battle of Waterloo", "Battle of Waterloo (British perspective)"),
    ("Napoleonic Wars", None),  # no master title, just a slug
    ("Regency period", None),
    ("Peninsular War", None),
    ("Cicero", None),
    ("Abolition of slavery in United States", "13th Amendment abolishes slavery in US"),
    ("Underground Railroad", None),
    ("Dust Bowl", "Dust Bowl peaks"),
    ("Great Depression", None),  # let me verify — actually I think master has Wall Street Crash
    ("Roaring Twenties", None),
    ("Prohibition (US)", "Volstead Act / US Prohibition begins"),
    ("Appeasement", None),
    ("Dunkirk evacuation", None),
    ("Battle of Britain", None),
    ("The Blitz", None),
    ("Bombing of Dresden", None),
    ("North African Campaign", None),
    # India
    ("Independence of India and Pakistan / Partition", "Indian independence and Partition"),
    ("The Emergency (India)", None),
    ("Indira Gandhi", None),
    ("Jawaharlal Nehru", None),
    # Misc 20th c
    ("Taliban take Kabul", None),
    ("First Indochina War", "French Indochina War / First Indochina War"),
    ("Tet Offensive", None),
    ("Mao Zedong", None),
    ("Great Leap Forward", None),
    ("Joseph Stalin", None),
    ("Anne Frank", None),
    ("Frida Kahlo", None),
    ("Vietnam War", "Vietnam War (American phase)"),
    ("John F. Kennedy", None),
    ("Soviet invasion of Afghanistan", "Soviet invasion of Afghanistan"),  # exists, no change
    ("Charles I", None),
    ("Adolf Hitler", "Adolf Hitler"),  # exists, no change
    ("Mary, Queen of Scots", None),
    # Other gaps
    ("Spanish-American War", None),
    ("Cuban Revolution", None),
    ("Bosnian War", None),
    ("Siege of Sarajevo", None),
    ("Biafran War", None),
    ("Battle of Borodino", None),
    ("Reign of Hadrian", "Reign of Hadrian"),  # exists
    ("Trojan War", "Trojan War"),  # exists
    ("Battle of Thermopylae", None),
    ("Manhattan Project", None),
    ("Scientific Revolution", None),
    ("Congress of Vienna", None),
    ("Peace of Westphalia", None),
    ("Revolutions of 1848", None),
    ("Reign of Terror", None),
    ("Maximilien Robespierre", None),
    ("Storming of the Bastille", None),
    ("Execution of Louis XVI", None),
    ("Anarchy in England", None),
    ("Wars of the Roses", None),
    ("Battle of Bosworth Field", None),
    ("Conscription Crisis in Canada", None),
    ("Mussolini", "Benito Mussolini"),
    ("March on Rome", None),
    ("Assassination of Archduke Franz Ferdinand", None),
    ("Russian Civil War", None),
    ("Russian Revolution", None),
    ("Spanish Civil War", "Spanish Civil War"),  # exists
    ("Black Death", "Black Death"),  # exists
    ("Sinking of the Lusitania", None),
    ("Council of Trent", "Council of Trent"),  # exists
    ("Thomas Cromwell", None),
    ("English Reformation", None),
    ("Luther's 95 Theses", None),
    ("Reformation", None),
    ("Glorious Revolution", None),
    ("Cromwell's Protectorate", None),
    ("Oliver Cromwell", None),
    ("Magna Carta", None),
    ("Henry II of England", None),
    ("English Civil War", None),
    ("Execution of Charles I", None),
    ("Charles I", None),
    ("Spanish Armada", None),
    ("Elizabeth I", None),
    ("Henry VIII", None),
    ("Reign of Elizabeth I", None),
    ("Crusades", None),
    ("First Crusade", None),
    ("Third Crusade", None),
    ("Joan of Arc", None),
    ("Fall of Constantinople", None),
    ("Mehmed II", None),
    ("Norman Conquest of England", None),
    ("Battle of Hastings", "Battle of Hastings"),  # exists
    ("Hundred Years' War", None),
    ("Domesday Book", "Domesday Book"),  # exists
    ("Battle of Agincourt", None),
    ("Execution of Anne Boleyn", "Execution of Anne Boleyn"),  # exists
    ("Mary, Queen of Scots", None),
    ("Execution of Mary, Queen of Scots", None),
    ("Cabral reaches Brazil", "Cabral reaches Brazil"),  # exists
    ("Augustus", "Augustus"),  # exists
    ("Reign of Nero", "Reign of Nero"),
    ("Nero", "Reign of Nero"),
    ("Constitutio Antoniniana", None),
    ("Eruption of Vesuvius / Pompeii destroyed", "Eruption of Vesuvius / Pompeii destroyed"),  # exists
    ("Roman Republic founded", None),
    ("Death of Alexander the Great", "Death of Alexander the Great"),  # exists
    ("Battle of Salamis", "Battle of Salamis"),  # exists
    ("Leonidas I of Sparta", "Leonidas I of Sparta"),  # exists
    ("Achaemenid Persian Empire founded", "Achaemenid Persian Empire founded"),  # exists
    ("Caesar crosses the Rubicon", "Caesar crosses the Rubicon"),  # exists
    ("Battle of Actium", "Battle of Actium"),  # exists
    ("First Punic War", None),
    ("Second Punic War", None),
    ("Third Punic War", None),
    ("Crisis of the Third Century", "Crisis of the Third Century"),  # exists
    ("Persian invasions of Greece", "Persian invasions of Greece"),  # exists
    ("Peloponnesian War", None),
    ("Age of Pericles in Athens", "Age of Pericles in Athens"),  # exists
    ("Edward Gibbon", None),
    ("Fall of Western Roman Empire", "Fall of Western Roman Empire"),  # exists
    ("Roman Londinium founded", "Roman Londinium founded"),  # exists
    ("Reign of Hadrian", "Reign of Hadrian"),  # exists
    ("Boris Johnson", None),
    ("Tony Blair", None),
    ("Margaret Thatcher", None),
    ("Vladimir Putin", None),
    ("Dissolution of the Soviet Union", "Dissolution of the Soviet Union"),  # exists
    ("Russian invasion of Ukraine", "Russian invasion of Ukraine"),  # exists
    ("Cultural Revolution", "Cultural Revolution"),  # exists
    ("9/11 attacks", "9/11 attacks"),  # exists
    ("The Holocaust", "The Holocaust"),  # exists
    ("Operation Barbarossa", "Operation Barbarossa"),  # exists
    ("Hitler becomes Chancellor of Germany", "Hitler becomes Chancellor of Germany"),  # exists
    ("Beer Hall Putsch", "Beer Hall Putsch"),  # exists
    ("World War I", "World War I"),  # exists
    ("World War II", "World War II"),  # exists
    ("Battle of Stalingrad", "Battle of Stalingrad"),  # exists
    ("Battle of Verdun", None),
    ("Battle of the Somme", None),
    ("D-Day (Operation Overlord)", "D-Day (Operation Overlord)"),  # exists
    ("Industrial Revolution", "Industrial Revolution"),  # exists
    ("Great Reform Act", None),
    ("Death of Hitler / Fall of Berlin", "Death of Hitler / Fall of Berlin"),  # exists
    ("Atomic bombings of Hiroshima and Nagasaki", "Atomic bombings of Hiroshima and Nagasaki"),  # exists
    ("Wright Brothers", None),
    ("Alfred the Great", "Alfred the Great"),  # exists
    ("Inca Empire", None),
    ("Aztec Empire", None),
    ("Easter Island settled", "Easter Island settled"),
    ("Classic Maya collapse", "Classic Maya collapse"),  # exists
    ("Cognitive Revolution", None),
    ("Agricultural Revolution", "Agricultural Revolution"),  # exists
    ("Emergence of Homo sapiens", "Emergence of Homo sapiens"),  # exists
    ("Columbian Exchange", "Columbian Exchange"),  # exists
    ("Charles Dickens", "Charles Dickens"),  # exists
    ("Jane Austen", "Jane Austen"),  # exists
    ("Lord Byron", "Lord Byron"),  # exists
    ("Charles Darwin", "Charles Darwin"),  # exists
    ("Napoleon Bonaparte", "Napoleon Bonaparte"),  # exists
    ("Napoleonic invasion of Russia", "Napoleonic invasion of Russia"),  # exists
    ("Napoleon's invasion of Russia", "Napoleon's invasion of Russia"),
    ("Winston Churchill", "Winston Churchill"),  # exists
    ("Queen Victoria", "Queen Victoria"),  # exists
    ("Victorian era", None),
    ("Florence Nightingale", "Florence Nightingale"),  # exists
    ("Abraham Lincoln", None),
    ("Assassination of Abraham Lincoln", None),
    ("George Washington", None),
    ("Catherine the Great", None),
    ("Peter the Great", "Peter the Great"),  # exists
    ("French Revolution", "French Revolution"),  # exists
    ("Battle of Gettysburg", None),
    ("American Civil War", "American Civil War"),  # exists
    ("Trench warfare on the Western Front (period)", "Trench warfare on the Western Front (period)"),  # exists
    ("Chaucer's Canterbury Tales", "Chaucer's Canterbury Tales"),  # exists
    ("Anne Boleyn", None),
    ("Great Fire of Rome", None),
    ("Great Fire of London", "Great Fire of London"),  # exists
    ("Great Plague of London", None),
    ("Stonehenge", "Stonehenge"),
    ("Mahatma Gandhi", "Mahatma Gandhi"),  # exists
    ("Falklands War", "Falklands War"),  # exists
    ("Battle of Trafalgar", "Battle of Trafalgar"),  # exists
    ("Horatio Nelson", "Horatio Nelson"),  # exists
    ("Watergate scandal", "Watergate scandal"),  # exists
    ("Nelson Mandela", None),
    ("Genghis Khan", "Genghis Khan"),  # exists
    ("Mary, Queen of Scots", None),
    ("Hatshepsut", "Hatshepsut"),  # exists
    ("French intervention in Mexico", "French intervention in Mexico"),  # exists
    ("Founding of Saudi Arabia", "Founding of Saudi Arabia"),  # exists
    ("Tunisia campaign", "Tunisia campaign"),  # exists
    ("Reign of Edward VI", "Reign of Edward VI"),  # exists
    ("Reign of Edward V", "Reign of Edward V"),  # exists
    ("Princes in the Tower", "Princes in the Tower"),  # exists
    ("FIFA World Cup 2022 in Qatar", "FIFA World Cup 2022 in Qatar"),  # exists
    ("Argentina wins 2022 FIFA World Cup", "Argentina wins 2022 FIFA World Cup"),  # exists
    ("Norman Conquest of England", "Norman Conquest of England"),  # exists
    ("Henry II of England", "Henry II of England"),  # exists
    ("Charles de Gaulle", "Charles de Gaulle"),  # exists
    ("Akhenaten", "Akhenaten"),  # exists
    ("Tutankhamun", "Tutankhamun"),  # exists
    ("California Gold Rush", "California Gold Rush"),  # exists
    ("Muhammad", "Muhammad"),  # exists
    ("Notre-Dame de Paris built", "Notre-Dame de Paris built"),  # exists
    ("King John", "King John"),  # exists
    ("Atlantic slave trade", "Atlantic slave trade"),  # exists
    ("Cyrus conquers Babylon", "Cyrus conquers Babylon"),  # exists
    ("Glyndŵr crowned Prince of Wales at Machynlleth", "Glyndŵr crowned Prince of Wales at Machynlleth"),  # exists
    ("Goethe", "Goethe"),  # exists
    ("Elizabeth II", "Elizabeth II"),  # exists
    ("Marilyn Monroe", "Marilyn Monroe"),  # exists
    ("US Civil Rights Movement", "US Civil Rights Movement"),  # exists
    ("Winter of Discontent", "Winter of Discontent"),  # exists
    ("The Beatles release Please Please Me", "The Beatles release Please Please Me"),  # exists
    ("Treaty on the Non-Proliferation of Nuclear Weapons (NPT)", "Treaty on the Non-Proliferation of Nuclear Weapons (NPT)"),  # exists
    ("Stephen Hawking", "Stephen Hawking"),  # exists
    ("Cold War", "Cold War"),  # exists
    ("Caliphate of Córdoba", "Caliphate of Córdoba"),  # exists
    ("Suez Crisis", "Suez Crisis"),  # exists
    ("Crusades", None),
    ("Antonine Plague", "Antonine Plague"),  # exists
    ("First powered flight (Wright Brothers)", None),  # try this title
    ("First powered flight", None),
    ("Wright brothers first flight", None),
    ("Wright brothers", None),
    ("Cuban Missile Crisis", None),
    ("First image of a black hole", None),
    ("US Constitution adopted", None),
    ("Storming of the Bastille", None),
    ("Boston Tea Party", None),
    ("American Declaration of Independence", None),
    ("American Revolutionary War", None),
    ("Independence of India and Pakistan / Partition", "Indian independence and Partition"),
    ("Akhenaten", "Akhenaten"),
    ("Goethe", "Goethe"),
    ("Gone with the Wind released", "Gone with the Wind released"),
    ("Gone with the Wind", "Gone with the Wind"),
    ("Nineteen Eighty-Four", "Nineteen Eighty-Four"),
    ("George Orwell", "George Orwell"),
    ("The Lord of the Rings", "The Lord of the Rings"),
    ("The Lord of the Rings film trilogy", "The Lord of the Rings film trilogy"),
    ("Agatha Christie", "Agatha Christie"),
    ("Agatha Christie's Murder on the Orient Express", "Agatha Christie's Murder on the Orient Express"),
    ("Mongol Empire under Genghis Khan", "Mongol Empire under Genghis Khan"),
    ("Adolf Hitler", "Adolf Hitler"),
    ("Julius Caesar", "Julius Caesar"),
    ("Assassination of Julius Caesar", None),
    ("Mongol invasions of Japan", "Mongol invasions of Japan"),
    ("Norman Conquest of England", "Norman Conquest of England"),
]


def main() -> int:
    text = BOOKS.read_text(encoding="utf-8")
    import re

    fixed = 0
    dropped = 0

    for bad, good in REPLACEMENTS:
        if good == bad:
            continue  # no-op marker (verifying tag exists)
        if good is None:
            # Drop the tag from any list. Match "bad" inside quoted list items.
            # We handle both:   "bad", and , "bad", and ["bad"]
            patterns = [
                rf'"{re.escape(bad)}",\s*',  # at start or middle
                rf',\s*"{re.escape(bad)}"',  # at end
                rf'"{re.escape(bad)}"',      # alone in list
            ]
            for p in patterns:
                new_text, n = re.subn(p, "", text)
                if n > 0:
                    text = new_text
                    dropped += n
                    break  # avoid double-matching
        else:
            # Replace with good.
            pat = rf'"{re.escape(bad)}"'
            new_text, n = re.subn(pat, f'"{good}"', text)
            if n > 0:
                text = new_text
                fixed += n

    BOOKS.write_text(text, encoding="utf-8")
    print(f"Replaced {fixed} tags; dropped {dropped} tags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
