import random
from music21 import environment, stream, note, midi

# --- Set a new MIDI player path ---
env = environment.UserSettings()
# Change this path to a player you have. Example: QuickTime Player
env['midiPath'] = '/System/Applications/QuickTime Player.app'

# Transition probabilities (rows sum to 1000)
transitions = {
    "C4": {"C4":100, "D4":300, "E4":200, "F4":100, "G4":100, "A4":50,  "B4":50,  "C5":100},
    "D4": {"C4":300, "D4":100, "E4":300, "F4":150, "G4":75,  "A4":25,  "B4":25,  "C5":25},
    "E4": {"C4":200, "D4":250, "E4":100, "F4":200, "G4":100, "A4":50,  "B4":50,  "C5":50},
    "F4": {"C4":100, "D4":150, "E4":250, "F4":100, "G4":250, "A4":75,  "B4":50,  "C5":25},
    "G4": {"C4":100, "D4":100, "E4":150, "F4":250, "G4":100, "A4":200, "B4":75,  "C5":25},
    "A4": {"C4":50,  "D4":75,  "E4":100, "F4":150, "G4":250, "A4":100, "B4":200, "C5":75},
    "B4": {"C4":50,  "D4":50,  "E4":75,  "F4":100, "G4":150, "A4":250, "B4":100, "C5":225},
    "C5": {"C4":100, "D4":50,  "E4":50,  "F4":75,  "G4":75,  "A4":150, "B4":250, "C5":250},
}

def weighted_choice(prob_dict):
    """Pick a note based on weighted probabilities (sum = 1000)."""
    r = random.randint(1, 1000)
    cumulative = 0
    for note, prob in prob_dict.items():
        cumulative += prob
        if r <= cumulative:
            return note
    # fallback (shouldn't happen if sum == 1000)
    return random.choice(list(prob_dict.keys()))

def generate_melody(start_note="C4", length=400):
    melody = [start_note]
    current_note = start_note
    for _ in range(length - 1):
        next_note = weighted_choice(transitions[current_note])
        melody.append(next_note)
        current_note = next_note
    return melody


melody = generate_melody("C4", length=400)
print("Generated melody:")
print(" ".join(melody))

_stream = stream.Stream()

for n in melody:
    _stream.append(note.Note(n, quarterLength=0.1))  


mf = midi.translate.streamToMidiFile(_stream)
mf.open('generated_melody.mid', 'wb')
mf.write()
mf.close()