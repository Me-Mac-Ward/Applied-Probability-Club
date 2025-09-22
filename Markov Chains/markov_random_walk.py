import random
from music21 import environment, stream, note, midi

# --- Set a new MIDI player path ---
env = environment.UserSettings()
# Change this path to a player you have. Example: QuickTime Player
env['midiPath'] = '/System/Applications/QuickTime Player.app'

# Transition probabilities (rows sum to 1000)
transitions = {
    "C4": {"C4":500, "D4":500, "E4":0, "F4":0, "G4":0, "A4":0,  "B4":0,  "C5":0},
    "D4": {"C4":333, "D4":334, "E4":333, "F4":0, "G4":0,  "A4":0,  "B4":0,  "C5":0},
    "E4": {"C4":0, "D4":333, "E4":334, "F4":333, "G4":0, "A4":0,  "B4":0,  "C5":0},
    "F4": {"C4":0, "D4":0, "E4":333, "F4":334, "G4":333, "A4":0,  "B4":0,  "C5":0},
    "G4": {"C4":0, "D4":0, "E4":0, "F4":333, "G4":334, "A4":333, "B4":0,  "C5":0},
    "A4": {"C4":0,  "D4":0,  "E4":0, "F4":0, "G4":333, "A4":334, "B4":333, "C5":0},
    "B4": {"C4":0,  "D4":0,  "E4":0,  "F4":0, "G4":0, "A4":333, "B4":334, "C5":333},
    "C5": {"C4":0, "D4":0,  "E4":0,  "F4":0,  "G4":0,  "A4":0, "B4":500, "C5":500},
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

def generate_melody(start_note="C4", length=16):
    melody = [start_note]
    current_note = start_note
    for _ in range(length - 1):
        next_note = weighted_choice(transitions[current_note])
        melody.append(next_note)
        current_note = next_note
    return melody


melody = generate_melody("C4", length=16)
print("Generated melody:")
print(" ".join(melody))

_stream = stream.Stream()

for n in melody:
    _stream.append(note.Note(n, quarterLength=1))  


mf = midi.translate.streamToMidiFile(_stream)
mf.open('generated_walk.mid', 'wb')
mf.write()
mf.close()