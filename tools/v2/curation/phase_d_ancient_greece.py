"""
Phase D — Ancient Greece. Bronze Age through Hellenistic.

Priority notes (no 800k floor):
  Master priority is calibrated to the existing dataset:
    980k+ : civilizational milestones (Trojan War, Alexander, fall of Rome)
    950k+ : major events most educated people know (Marathon, Salamis)
    900k+ : major regional events (Plataea, Peloponnesian War, Chaeronea)
    850k+ : important but not universally known (Solon, Cleisthenes, Leuctra)
    750k+ : notable but specific (battles, treaties)
    600-750: regional importance only
    below : minor curiosities

Ancient-greece slug priority follows the same convention used in re-curation:
  base = master_priority
  +30k if title contains a strong Greek-anchored marker (most do, so default)
  -90k if entry also tagged on another regional slug
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from v2.curation.append_entries import append_entries, next_available_id

RW_GREECE = {"europe": 10, "americas": 2, "asia": 6, "australasia": 1, "africa": 3}
RW_HELLEN = {"europe": 9, "americas": 2, "asia": 8, "australasia": 1, "africa": 5}


def g(master_pri: int, greek_pri: int | None = None, **extra) -> dict:
    """Build priority dict. If greek_pri omitted, default to master+30k."""
    if greek_pri is None:
        greek_pri = min(999_000, master_pri + 30_000)
    out = {"master": master_pri, "ancient-greece": greek_pri}
    out.update(extra)
    return out


ENTRIES = [
    # ----- Bronze Age & Dark Age -----
    {"type": "event", "title": "Minoan civilization",
     "description": "Bronze Age Aegean civilization centred on Crete; palaces at Knossos and Phaistos, Linear A script, frescoes.",
     "start_year": -2000, "end_year": -1450, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Minoan_civilization",
     "priorities": g(910_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Eruption of Thera",
     "description": "Volcanic eruption on Santorini around 1600 BCE; devastates the Minoan settlement at Akrotiri; possible origin of Atlantis legend.",
     "start_year": -1600, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Minoan_eruption",
     "priorities": g(820_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Mycenaean civilization",
     "description": "Bronze Age Greek civilization on the mainland; warrior aristocracy, palace economy, Linear B script (early Greek).",
     "start_year": -1600, "end_year": -1100, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Mycenaean_Greece",
     "priorities": g(890_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Linear B deciphered",
     "description": "Michael Ventris shows in 1952 that the Linear B tablets of Knossos and Pylos are written in an early form of Greek.",
     "start_year": -1450, "date_uncertain": True,
     "display_date": "tablets ~1450 BCE; deciphered 1952",
     "wikipedia": "https://en.wikipedia.org/wiki/Linear_B",
     "priorities": g(700_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Bronze Age collapse",
     "description": "Sudden collapse of Mediterranean palace civilizations around 1200 BCE; Mycenaean palaces destroyed; Sea Peoples appear in Egyptian records.",
     "start_year": -1200, "end_year": -1150, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Late_Bronze_Age_collapse",
     "priorities": g(900_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Greek Dark Age",
     "description": "Period after the Bronze Age collapse; literacy lost, populations fall, polis system slowly emerges.",
     "start_year": -1100, "end_year": -800, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Greek_Dark_Ages",
     "priorities": g(810_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "First Olympic Games",
     "description": "Traditional first Olympic Games at Olympia; held every four years for over a millennium; emblem of Panhellenic identity.",
     "start_year": -776,
     "wikipedia": "https://en.wikipedia.org/wiki/Ancient_Olympic_Games",
     "priorities": g(880_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Greek alphabet developed",
     "description": "Greeks adapt the Phoenician abjad and add vowel letters; basis of all European alphabets.",
     "start_year": -800, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Greek_alphabet",
     "priorities": g(890_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Greek colonization of the Mediterranean",
     "description": "Greek poleis plant colonies from Marseille to the Black Sea between c. 750 and 550 BCE.",
     "start_year": -750, "end_year": -550, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Greek_colonisation",
     "priorities": g(840_000), "region_weights": RW_HELLEN},

    {"type": "art", "title": "Iliad and Odyssey composed",
     "description": "Homeric epics committed to writing around 750-700 BCE; foundational works of Greek and Western literature.",
     "start_year": -750, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Homer",
     "priorities": g(960_000, **{"arts-and-thoughts": 970_000}),
     "region_weights": RW_GREECE},

    {"type": "art", "title": "Hesiod's Theogony and Works and Days",
     "description": "Boeotian poet's account of the gods' genealogy and a verse calendar of farming and ethics.",
     "start_year": -700, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hesiod",
     "priorities": g(780_000, **{"arts-and-thoughts": 820_000}),
     "region_weights": RW_GREECE},

    # ----- Archaic Greece -----
    {"type": "event", "title": "Rise of the polis",
     "description": "Independent city-states (poleis) become the defining Greek political form; Athens, Sparta, Corinth, Thebes the major players.",
     "start_year": -750, "end_year": -500, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Polis",
     "priorities": g(860_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Lycurgus and Spartan constitution",
     "description": "Legendary lawgiver supposedly fashions Sparta's mixed constitution and rigorous training regime (agoge).",
     "start_year": -700, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Lycurgus_of_Sparta",
     "priorities": g(800_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Messenian Wars (Sparta vs Messenia)",
     "description": "Sparta subjugates Messenia in two long wars; Messenians become helots, the foundation of Spartan agricultural economy.",
     "start_year": -740, "end_year": -650, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Messenian_Wars",
     "priorities": g(740_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Draco's law code at Athens",
     "description": "Draco posts the first written law code at Athens; harsh penalties give us the word 'draconian'.",
     "start_year": -621,
     "wikipedia": "https://en.wikipedia.org/wiki/Draco_(lawgiver)",
     "priorities": g(810_000), "region_weights": RW_GREECE},

    {"type": "person", "title": "Sappho",
     "description": "Lyric poet of Lesbos; surviving fragments include the great ode to Aphrodite; canonical figure of Greek poetry.",
     "start_year": -630, "end_year": -570, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Sappho",
     "priorities": g(870_000, people=890_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_GREECE},

    {"type": "event", "title": "Solon's reforms at Athens",
     "description": "Archon Solon cancels debts, reorganises citizen classes by wealth, and lays the groundwork for Athenian democracy.",
     "start_year": -594,
     "wikipedia": "https://en.wikipedia.org/wiki/Solon",
     "priorities": g(880_000), "region_weights": RW_GREECE},

    {"type": "person", "title": "Solon",
     "description": "Athenian lawgiver and one of the Seven Sages of Greece; debt cancellation and constitutional reforms.",
     "start_year": -638, "end_year": -558, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Solon",
     "priorities": g(830_000, people=850_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Peisistratid tyranny at Athens",
     "description": "Peisistratus and sons rule Athens as 'tyrants' (in the Greek sense); patronise the arts, fix the Homeric text, build temples.",
     "start_year": -546, "end_year": -510, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Peisistratos",
     "priorities": g(780_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Cleisthenes' reforms",
     "description": "Cleisthenes reorganises Athens into ten new tribes; introduces ostracism and the council of 500; effective birth of democracy.",
     "start_year": -508,
     "wikipedia": "https://en.wikipedia.org/wiki/Cleisthenes",
     "priorities": g(900_000), "region_weights": RW_GREECE},

    {"type": "person", "title": "Pythagoras",
     "description": "Ionian-born philosopher and mathematician active in Croton, southern Italy; founder of the Pythagorean school.",
     "start_year": -570, "end_year": -495, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pythagoras",
     "priorities": g(900_000, people=920_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_GREECE},

    {"type": "person", "title": "Heraclitus",
     "description": "Pre-Socratic philosopher of Ephesus; emphasised constant change and unity of opposites ('one cannot step into the same river twice').",
     "start_year": -535, "end_year": -475, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Heraclitus",
     "priorities": g(820_000, people=850_000), "region_weights": RW_GREECE},

    # ----- Persian Wars -----
    {"type": "event", "title": "Ionian Revolt",
     "description": "Greek cities of Ionia rebel against Persian rule under Aristagoras of Miletus; Athens sends help, triggering Persian retaliation.",
     "start_year": -499, "end_year": -493,
     "wikipedia": "https://en.wikipedia.org/wiki/Ionian_Revolt",
     "priorities": g(830_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Battle of Marathon",
     "description": "Athenian and Plataean hoplites defeat Darius I's Persian invasion force on the plain of Marathon.",
     "start_year": -490, "start_month": 9, "start_day": 12,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Marathon",
     "priorities": g(950_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Battle of Thermopylae",
     "description": "Leonidas's 300 Spartans (and Thespians and Thebans) hold the pass for three days against Xerxes' army before being outflanked.",
     "start_year": -480, "start_month": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Thermopylae",
     "priorities": g(960_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Battle of Salamis",
     "description": "Themistocles lures the Persian fleet into the Salamis straits; allied Greek triremes shatter Xerxes' navy.",
     "start_year": -480, "start_month": 9,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Salamis",
     "priorities": g(950_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Battle of Plataea",
     "description": "Largest hoplite battle in Greek history; Spartan-led coalition crushes Persian land force under Mardonius.",
     "start_year": -479, "start_month": 8,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Plataea",
     "priorities": g(900_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Battle of Mycale",
     "description": "Greek fleet under Leotychidas destroys the Persian fleet at Mycale on the same day as Plataea; ends Persian invasions.",
     "start_year": -479, "start_month": 8, "start_day": 27,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Mycale",
     "priorities": g(800_000), "region_weights": RW_GREECE},

    {"type": "person", "title": "Themistocles",
     "description": "Athenian general and politician; builder of the Athenian fleet; architect of victory at Salamis.",
     "start_year": -524, "end_year": -459, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Themistocles",
     "priorities": g(870_000, people=890_000), "region_weights": RW_GREECE},

    {"type": "person", "title": "Leonidas I of Sparta",
     "description": "Agiad king of Sparta; commanded the Greek force at Thermopylae; iconic emblem of resistance.",
     "start_year": -540, "end_year": -480, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Leonidas_I",
     "priorities": g(880_000, people=910_000), "region_weights": RW_GREECE},

    # ----- Pentecontaetia & Periclean Athens -----
    {"type": "event", "title": "Delian League founded",
     "description": "Anti-Persian alliance led by Athens; treasury kept on Delos, then moved to Athens in 454; effectively an Athenian empire.",
     "start_year": -478,
     "wikipedia": "https://en.wikipedia.org/wiki/Delian_League",
     "priorities": g(870_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Periclean Athens",
     "description": "Pericles dominates Athenian politics for three decades; Acropolis rebuilt; Athens at cultural and imperial peak.",
     "start_year": -461, "end_year": -429,
     "wikipedia": "https://en.wikipedia.org/wiki/Pericles",
     "priorities": g(910_000), "region_weights": RW_GREECE},

    {"type": "person", "title": "Pericles",
     "description": "Athenian statesman who shaped Athenian democracy and empire; commissioned the Parthenon; died in the Plague of Athens.",
     "start_year": -495, "end_year": -429, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Pericles",
     "priorities": g(920_000, people=940_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Parthenon built",
     "description": "Temple of Athena Parthenos on the Athenian Acropolis; designed by Ictinus and Callicrates with sculpture by Phidias.",
     "start_year": -447, "end_year": -432,
     "wikipedia": "https://en.wikipedia.org/wiki/Parthenon",
     "priorities": g(940_000, **{"arts-and-thoughts": 950_000}),
     "region_weights": RW_GREECE},

    {"type": "person", "title": "Phidias",
     "description": "Most celebrated sculptor of classical Greece; directed Parthenon sculpture, made the chryselephantine Zeus of Olympia.",
     "start_year": -480, "end_year": -430, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Phidias",
     "priorities": g(840_000, people=860_000, **{"arts-and-thoughts": 870_000}),
     "region_weights": RW_GREECE},

    {"type": "person", "title": "Herodotus",
     "description": "Halicarnassian historian; 'father of history'; wrote the Histories of the Persian Wars.",
     "start_year": -484, "end_year": -425, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Herodotus",
     "priorities": g(890_000, people=910_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_GREECE},

    {"type": "person", "title": "Thucydides",
     "description": "Athenian historian and general; wrote the History of the Peloponnesian War, founding text of political realism.",
     "start_year": -460, "end_year": -400, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Thucydides",
     "priorities": g(900_000, people=910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_GREECE},

    {"type": "person", "title": "Aeschylus",
     "description": "Earliest of the three great Athenian tragedians; introduced the second actor; surviving plays include the Oresteia.",
     "start_year": -525, "end_year": -456, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Aeschylus",
     "priorities": g(880_000, people=890_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_GREECE},

    {"type": "person", "title": "Sophocles",
     "description": "Second Athenian tragedian; wrote Oedipus the King and Antigone; introduced a third actor.",
     "start_year": -497, "end_year": -406, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Sophocles",
     "priorities": g(890_000, people=910_000, **{"arts-and-thoughts": 920_000}),
     "region_weights": RW_GREECE},

    {"type": "person", "title": "Euripides",
     "description": "Most psychological of the three tragedians; wrote Medea, Bacchae, Trojan Women; champion of marginal voices.",
     "start_year": -480, "end_year": -406, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Euripides",
     "priorities": g(880_000, people=900_000, **{"arts-and-thoughts": 910_000}),
     "region_weights": RW_GREECE},

    {"type": "person", "title": "Aristophanes",
     "description": "Greatest writer of Athenian Old Comedy; plays include Lysistrata, Clouds, and The Birds.",
     "start_year": -446, "end_year": -386, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Aristophanes",
     "priorities": g(850_000, people=870_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_GREECE},

    {"type": "person", "title": "Hippocrates of Cos",
     "description": "Father of medicine; Hippocratic Corpus and oath; clinical observation replaces divine causation in healing.",
     "start_year": -460, "end_year": -370, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Hippocrates",
     "priorities": g(900_000, people=920_000, **{"arts-and-thoughts": 900_000}),
     "region_weights": RW_GREECE},

    # ----- Peloponnesian War -----
    {"type": "event", "title": "Peloponnesian War",
     "description": "Twenty-seven-year war between Athenian and Spartan alliances; ends with Athens's surrender in 404 BCE.",
     "start_year": -431, "end_year": -404,
     "wikipedia": "https://en.wikipedia.org/wiki/Peloponnesian_War",
     "priorities": g(940_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Plague of Athens",
     "description": "Epidemic in the second year of the Peloponnesian War kills perhaps a quarter of Athens including Pericles.",
     "start_year": -430, "end_year": -426,
     "wikipedia": "https://en.wikipedia.org/wiki/Plague_of_Athens",
     "priorities": g(870_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Pylos and Sphacteria",
     "description": "Athenian general Demosthenes captures 292 Spartiates on Sphacteria; first time elite Spartans surrender en masse.",
     "start_year": -425,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Pylos",
     "priorities": g(740_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Sicilian Expedition",
     "description": "Catastrophic Athenian expedition to Syracuse; entire force destroyed; tips Athens toward defeat.",
     "start_year": -415, "end_year": -413,
     "wikipedia": "https://en.wikipedia.org/wiki/Sicilian_Expedition",
     "priorities": g(890_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Battle of Aegospotami",
     "description": "Lysander's Spartan fleet destroys the Athenian navy on the Hellespont; cuts off Athens's grain; ends the war.",
     "start_year": -405,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Aegospotami",
     "priorities": g(830_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Surrender of Athens",
     "description": "Athens capitulates to Sparta; walls dismantled; Thirty Tyrants installed before democracy is restored.",
     "start_year": -404,
     "wikipedia": "https://en.wikipedia.org/wiki/Peloponnesian_War",
     "priorities": g(870_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Trial and execution of Socrates",
     "description": "Athenian jury condemns Socrates for impiety and corrupting the young; he drinks hemlock; founding moment of Western philosophy.",
     "start_year": -399,
     "wikipedia": "https://en.wikipedia.org/wiki/Trial_of_Socrates",
     "priorities": g(940_000), "region_weights": RW_GREECE},

    # ----- 4th century / Spartan & Theban hegemonies -----
    {"type": "event", "title": "March of the Ten Thousand",
     "description": "Greek mercenaries' fighting retreat through Persia after Cyrus's death at Cunaxa; narrated in Xenophon's Anabasis.",
     "start_year": -401, "end_year": -399,
     "wikipedia": "https://en.wikipedia.org/wiki/Ten_Thousand",
     "priorities": g(810_000), "region_weights": RW_HELLEN},

    {"type": "person", "title": "Xenophon",
     "description": "Athenian soldier and historian; companion of Socrates; wrote the Anabasis and Hellenica.",
     "start_year": -430, "end_year": -354, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Xenophon",
     "priorities": g(820_000, people=840_000, **{"arts-and-thoughts": 850_000}),
     "region_weights": RW_GREECE},

    {"type": "event", "title": "Corinthian War",
     "description": "Theban-Corinthian-Athenian-Argive coalition fights Sparta to a stalemate, ended by the Persian-imposed King's Peace.",
     "start_year": -395, "end_year": -387,
     "wikipedia": "https://en.wikipedia.org/wiki/Corinthian_War",
     "priorities": g(750_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Battle of Leuctra",
     "description": "Theban general Epaminondas crushes the Spartan army with oblique formation; breaks Sparta's military reputation forever.",
     "start_year": -371, "start_month": 7, "start_day": 6,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Leuctra",
     "priorities": g(870_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Theban Hegemony",
     "description": "Thebes briefly dominates Greece under Epaminondas and Pelopidas; Messenia freed; Spartan power broken.",
     "start_year": -371, "end_year": -362,
     "wikipedia": "https://en.wikipedia.org/wiki/Theban_hegemony",
     "priorities": g(780_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Battle of Mantinea (362 BCE)",
     "description": "Epaminondas defeats a Spartan-Athenian coalition but is killed in the moment of victory; Thebes's hegemony dies with him.",
     "start_year": -362,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Mantinea_(362_BC)",
     "priorities": g(720_000), "region_weights": RW_GREECE},

    # ----- Philip II and Alexander -----
    {"type": "person", "title": "Philip II of Macedon",
     "description": "King of Macedon who reforms the army (sarissa phalanx), unifies Greece under Macedonian hegemony, and bequeaths Alexander an empire-ready force.",
     "start_year": -382, "end_year": -336, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Philip_II_of_Macedon",
     "priorities": g(910_000, people=930_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Battle of Chaeronea",
     "description": "Philip II and Alexander defeat the Theban-Athenian coalition; Macedon becomes the dominant power in Greece.",
     "start_year": -338, "start_month": 8, "start_day": 2,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Chaeronea_(338_BC)",
     "priorities": g(870_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "League of Corinth",
     "description": "Philip II organises the Greek poleis (except Sparta) into a federal league for an invasion of Persia.",
     "start_year": -337,
     "wikipedia": "https://en.wikipedia.org/wiki/League_of_Corinth",
     "priorities": g(750_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Assassination of Philip II",
     "description": "Philip II stabbed to death at his daughter's wedding by his bodyguard Pausanias; Alexander succeeds him at 20.",
     "start_year": -336,
     "wikipedia": "https://en.wikipedia.org/wiki/Philip_II_of_Macedon",
     "priorities": g(810_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Alexander's destruction of Thebes",
     "description": "Alexander razes Thebes after revolt, sparing only Pindar's house; warning to other rebellious cities.",
     "start_year": -335,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Thebes",
     "priorities": g(770_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Battle of the Granicus",
     "description": "Alexander's first major victory over Persian forces in Asia Minor; opens the Anatolian coast.",
     "start_year": -334, "start_month": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Granicus",
     "priorities": g(830_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Battle of Issus",
     "description": "Alexander defeats Darius III in southern Anatolia; captures the Persian royal family.",
     "start_year": -333, "start_month": 11, "start_day": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Issus",
     "priorities": g(870_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Siege of Tyre (332 BCE)",
     "description": "Alexander takes the island city of Tyre after a seven-month siege using a mole built across the strait.",
     "start_year": -332, "start_month": 1, "end_month": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Siege_of_Tyre_(332_BC)",
     "priorities": g(810_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Alexander founds Alexandria",
     "description": "Alexander founds Alexandria on the Egyptian coast; later capital of the Ptolemies and Hellenistic centre of learning.",
     "start_year": -331, "start_month": 4, "start_day": 7,
     "wikipedia": "https://en.wikipedia.org/wiki/Alexandria",
     "priorities": g(910_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Battle of Gaugamela",
     "description": "Alexander's decisive victory over Darius III in Mesopotamia; effectively ends the Achaemenid Persian Empire.",
     "start_year": -331, "start_month": 10, "start_day": 1,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Gaugamela",
     "priorities": g(910_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Burning of Persepolis",
     "description": "Alexander burns the Achaemenid ceremonial capital; symbolic vengeance for the Persian sack of the Athenian Acropolis.",
     "start_year": -330,
     "wikipedia": "https://en.wikipedia.org/wiki/Persepolis",
     "priorities": g(820_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Battle of the Hydaspes",
     "description": "Alexander defeats Indian king Porus on the river Hydaspes (modern Jhelum); his last great battle before mutinous troops force him back.",
     "start_year": -326, "start_month": 5,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_the_Hydaspes",
     "priorities": g(820_000, india=820_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Death of Alexander the Great",
     "description": "Alexander dies in Babylon aged 32; his empire fragments among his generals (the Diadochi).",
     "start_year": -323, "start_month": 6, "start_day": 11,
     "wikipedia": "https://en.wikipedia.org/wiki/Death_of_Alexander_the_Great",
     "priorities": g(940_000), "region_weights": RW_HELLEN},

    # ----- Diadochi & Hellenistic -----
    {"type": "event", "title": "Wars of the Diadochi",
     "description": "Forty years of war between Alexander's generals; ends with the empire carved into Ptolemaic Egypt, Seleucid Asia, Antigonid Macedon.",
     "start_year": -322, "end_year": -281,
     "wikipedia": "https://en.wikipedia.org/wiki/Wars_of_the_Diadochi",
     "priorities": g(870_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Battle of Ipsus",
     "description": "Decisive Diadochi battle; Seleucus and Lysimachus defeat Antigonus I Monophthalmus; effectively partitions Alexander's empire.",
     "start_year": -301,
     "wikipedia": "https://en.wikipedia.org/wiki/Battle_of_Ipsus",
     "priorities": g(800_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Library of Alexandria founded",
     "description": "Ptolemy I founds the Mouseion and library at Alexandria; ambition is to collect every book in the world.",
     "start_year": -300, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Library_of_Alexandria",
     "priorities": g(920_000, **{"arts-and-thoughts": 930_000}),
     "region_weights": RW_HELLEN},

    {"type": "event", "title": "Ptolemaic Kingdom",
     "description": "Hellenistic kingdom of Egypt founded by Ptolemy I; lasts nearly three centuries until Cleopatra VII.",
     "start_year": -305, "end_year": -30,
     "wikipedia": "https://en.wikipedia.org/wiki/Ptolemaic_Kingdom",
     "priorities": g(900_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Seleucid Empire",
     "description": "Largest of the Hellenistic kingdoms; founded by Seleucus I; covers most of former Persian Empire from Anatolia to India.",
     "start_year": -312, "end_year": -63,
     "wikipedia": "https://en.wikipedia.org/wiki/Seleucid_Empire",
     "priorities": g(890_000), "region_weights": RW_HELLEN},

    {"type": "event", "title": "Antigonid dynasty of Macedon",
     "description": "Antigonid kings rule Macedon for over a century; finally defeated by Rome at Pydna in 168 BCE.",
     "start_year": -276, "end_year": -168,
     "wikipedia": "https://en.wikipedia.org/wiki/Antigonid_dynasty",
     "priorities": g(820_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Hellenistic period",
     "description": "Era between Alexander's death and Rome's conquest of the Greek east; Greek culture spread from Massalia to the Indus.",
     "start_year": -323, "end_year": -30,
     "wikipedia": "https://en.wikipedia.org/wiki/Hellenistic_period",
     "priorities": g(900_000), "region_weights": RW_HELLEN},

    {"type": "person", "title": "Euclid of Alexandria",
     "description": "Mathematician at Alexandria; his Elements organises classical geometry into 13 books used as a textbook for 2,000 years.",
     "start_year": -325, "end_year": -265, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Euclid",
     "priorities": g(920_000, people=940_000, **{"arts-and-thoughts": 940_000}),
     "region_weights": RW_HELLEN},

    {"type": "person", "title": "Eratosthenes",
     "description": "Cyrenean polymath; chief librarian at Alexandria; measured the Earth's circumference to within 1-2% using shadow at Aswan.",
     "start_year": -276, "end_year": -194, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Eratosthenes",
     "priorities": g(870_000, people=890_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_HELLEN},

    {"type": "person", "title": "Aristarchus of Samos",
     "description": "Hellenistic astronomer; proposed heliocentric model 1,800 years before Copernicus.",
     "start_year": -310, "end_year": -230, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Aristarchus_of_Samos",
     "priorities": g(820_000, people=850_000, **{"arts-and-thoughts": 850_000}),
     "region_weights": RW_HELLEN},

    {"type": "person", "title": "Epicurus",
     "description": "Founder of Epicureanism; school in the Garden at Athens taught that pleasure (absence of pain) is the highest good.",
     "start_year": -341, "end_year": -270, "is_full_life": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Epicurus",
     "priorities": g(840_000, people=860_000, **{"arts-and-thoughts": 880_000}),
     "region_weights": RW_GREECE},

    {"type": "person", "title": "Zeno of Citium",
     "description": "Founder of Stoicism; taught in the Painted Stoa (Stoa Poikile) in Athens; ethics centred on virtue as the only good.",
     "start_year": -334, "end_year": -262, "is_full_life": True, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Zeno_of_Citium",
     "priorities": g(820_000, people=850_000, **{"arts-and-thoughts": 870_000}),
     "region_weights": RW_GREECE},

    {"type": "event", "title": "Colossus of Rhodes",
     "description": "Hundred-foot bronze statue of Helios at the harbour of Rhodes; one of the Seven Wonders of the Ancient World; toppled by earthquake 226 BCE.",
     "start_year": -280, "end_year": -226,
     "wikipedia": "https://en.wikipedia.org/wiki/Colossus_of_Rhodes",
     "priorities": g(820_000, **{"arts-and-thoughts": 830_000}),
     "region_weights": RW_HELLEN},

    {"type": "event", "title": "Achaean League",
     "description": "Federation of Greek poleis in the northern Peloponnese; held off Macedon and Rome for over a century before final defeat in 146 BCE.",
     "start_year": -280, "end_year": -146,
     "wikipedia": "https://en.wikipedia.org/wiki/Achaean_League",
     "priorities": g(770_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Aetolian League",
     "description": "Rival Greek federation in central Greece; first major Greek power to ally with Rome against Macedon.",
     "start_year": -290, "end_year": -189, "date_uncertain": True,
     "wikipedia": "https://en.wikipedia.org/wiki/Aetolian_League",
     "priorities": g(720_000), "region_weights": RW_GREECE},

    {"type": "event", "title": "Roman conquest of Greece",
     "description": "Rome destroys Corinth in 146 BCE and absorbs Greece; ends Hellenistic political independence and starts Greco-Roman fusion.",
     "start_year": -146,
     "wikipedia": "https://en.wikipedia.org/wiki/Roman_Greece",
     "priorities": g(890_000, **{"roman-history": 870_000}),
     "region_weights": RW_HELLEN},
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
