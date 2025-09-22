import random
from music21 import environment, stream, note, midi

# --- Set a new MIDI player path ---
env = environment.UserSettings()
# Change this path to a player you have. Example: QuickTime Player
env['midiPath'] = '/System/Applications/QuickTime Player.app'

# Transition probabilities (rows sum to 1000)
transitions = {
    "C4": {"C4":250, "D4":80,  "E4":250, "F4":80,  "G4":200, "A4":50,  "B4":20,  "C5":70},
    "D4": {"C4":150, "D4":100, "E4":300, "F4":120, "G4":180, "A4":80,  "B4":50,  "C5":20},
    "E4": {"C4":200, "D4":120, "E4":100, "F4":180, "G4":200, "A4":120, "B4":50,  "C5":30},
    "F4": {"C4":150, "D4":80,  "E4":200, "F4":100, "G4":250, "A4":150, "B4":40,  "C5":30},
    "G4": {"C4":350, "D4":50,  "E4":200, "F4":80,  "G4":100, "A4":120, "B4":60,  "C5":40},
    "A4": {"C4":100, "D4":120, "E4":150, "F4":220, "G4":200, "A4":80,  "B4":70,  "C5":60},
    "B4": {"C4":50,  "D4":40,  "E4":60,  "F4":50,  "G4":80,  "A4":120, "B4":100, "C5":500},
    "C5": {"C4":300, "D4":50,  "E4":200, "F4":80,  "G4":200, "A4":80,  "B4":30,  "C5":60},
}


def weighted_choice(prob_dict):
    """Pick a note based on weighted probabilities (sum = 1000)."""
    r = random.randint(1, 1000)
    cumulative = 0
    for note, prob in prob_dict.items():
        cumulative += prob
        if r <= cumulative:
            return note
    
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
