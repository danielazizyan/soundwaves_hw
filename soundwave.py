import numpy as np
from scipy.io import wavfile
import os


class SoundWaveFactory:

    """
    A class to generate and manipulate sound waves based on musical notes.
    Supports saving to WAV and TXT formats, reading from TXT, 
    and normalizing multiple waves.
    """

    SAMPLING_RATE = 44100  # like 44.1 KHz
    DURATION_SECONDS = 5
    SOUND_ARRAY_LEN = SAMPLING_RATE * DURATION_SECONDS
    MAX_AMPLITUDE = 2**13

    # From a list of https://en.wikipedia.org/wiki/Piano_key_frequencies
    NOTES = {
        "0": 0,
        "e0": 20.60172,
        "f0": 21.82676,
        "f#0": 23.12465,
        "g0": 24.49971,
        "g#0": 25.95654,
        "a0": 27.50000,
        "a#0": 29.13524,
        "b0": 30.86771,
        "c0": 32.70320,
        "c#0": 34.64783,
        "d0": 36.70810,
        "d#0": 38.89087,
        "e1": 41.20344,
        "f1": 43.65353,
        "f#1": 46.24930,
        "g1": 48.99943,
        "g#1": 51.91309,
        "a1": 55.00000,
        "a#1": 58.27047,
        "b1": 61.73541,
        "c1": 65.40639,
        "c#1": 69.29566,
        "d1": 73.41619,
        "d#1": 77.78175,
        "e2": 82.40689,
        "f2": 87.30706,
        "f#2": 92.49861,
        "g2": 97.99886,
        "g#2": 103.8262,
        "a2": 110.0000,
        "a#2": 116.5409,
        "b2": 123.4708,
        "c2": 130.8128,
        "c#2": 138.5913,
        "d2": 146.8324,
        "d#2": 155.5635,
        "e3": 164.8138,
        "f3": 174.6141,
        "f#3": 184.9972,
        "g3": 195.9977,
        "g#3": 207.6523,
        "a3": 220.0000,
        "a#3": 233.0819,
        "b3": 246.9417,
        "c3": 261.6256,
        "c#3": 277.1826,
        "d3": 293.6648,
        "d#3": 311.1270,
        "e4": 329.6276,
        "f4": 349.2282,
        "f#4": 369.9944,
        "g4": 391.9954,
        "g#4": 415.3047,
        "a4": 440.0000,
        "a#4": 466.1638,
        "b4": 493.8833,
        "c4": 523.2511,
        "c#4": 554.3653,
        "d4": 587.3295,
        "d#4": 622.2540,
        "e5": 659.2551,
        "f5": 698.4565,
        "f#5": 739.9888,
        "g5": 783.9909,
        "g#5": 830.6094,
        "a5": 880.0000,
        "a#5": 932.3275,
        "b5": 987.7666,
        "c5": 1046.502,
        "c#5": 1108.731,
        "d5": 1174.659,
        "d#5": 1244.508,
        "e6": 1318.510,
        "f6": 1396.913,
        "f#6": 1479.978,
        "g6": 1567.982,
        "g#6": 1661.219,
        "a6": 1760.000,
        "a#6": 1864.655,
        "b6": 1975.533,
        "c6": 2093.005,
        "c#6": 2217.461,
        "d6": 2349.318,
        "d#6": 2489.016,
        "e7": 2637.020,
        "f7": 2793.826,
        "f#7": 2959.955,
        "g7": 3135.963,
        "g#7": 3322.438,
        "a7": 3520.000,
        "a#7": 3729.310,
        "b7": 3951.066,
        "c7": 4186.009,
        "c#7": 4434.922,
        "d7": 4698.636,
        "d#7": 4978.032,
    }

    def __init__(self):
        self.common_timeline = np.linspace(
            0, self.DURATION_SECONDS, num=self.SOUND_ARRAY_LEN
        )
        self.sound_wave = None
        self.note = None


    def get_normed_sin(self, timeline, frequency):
        """Generates a sine wave for a given frequency over the specified timeline."""
        return self.MAX_AMPLITUDE * np.sin(2 * np.pi * frequency * timeline)


    def get_soundwave(self, timeline, note):
        """Generates a sound wave for a given note."""
        if note not in self.NOTES:
            raise ValueError(f"Note '{note}' not found in NOTES.")
        return self.get_normed_sin(timeline, self.NOTES[note])


    def create_note(self, note="a4", name=None, timeline=None):
        """Generates a sound wave for a given note and saves it as a WAV file."""

        if timeline is None:
            timeline = self.common_timeline

        self.note = note
        self.sound_wave = self.get_soundwave(timeline, note).astype(np.int16)

        #Generates the file name
        if name is None:
            file_name = f"{note}_sin.wav".replace("#", "s")
        else:
            file_name = f"{name}.wav"

        wavfile.write(file_name, self.SAMPLING_RATE, self.sound_wave)
        return self.sound_wave


    def read_wave_from_txt(self, file_name):
        """Loads a sound wave from a .txt file into the sound_wave attribute."""
        if os.path.exists(file_name):
            try:
                self.sound_wave = np.loadtxt(file_name, dtype=np.int16)
                print(f"Successfully loaded wave from {file_name}")
            except Exception as e:
                print(f"Error loading wave from {file_name}: {e}")
        else:
            raise FileNotFoundError(f"{file_name} not found.")


    def print_wave_details(self):
        """Prints the details of the current sound wave"""

        if self.sound_wave is None:
            print("No sound wave is loaded or generated yet.")
            return
        
        print(
            f"Details for the wave generated from note '{self.note}':\n"
            f"Duration: {self.DURATION_SECONDS} seconds\n"
            f"Sampling Rate: {self.SAMPLING_RATE} Hz\n"
            f"Number of Samples: {len(self.sound_wave)}\n"
            f"Max Amplitude: {np.max(self.sound_wave)}\n"
            f"Min Amplitude: {np.min(self.sound_wave)}\n"
            f"Mean Amplitude: {np.mean(self.sound_wave):.2f}"
        )


    def normalize_sound_waves(self, *waves):
        """Normalizes multiple sound waves to the same length and amplitude."""

        if not waves:
            print("No waves provided.")
            return None

        # Finds the minimum length among all waves
        min_length = min(
            len(wave.sound_wave if isinstance(wave, SoundWaveFactory) else wave)
            for wave in waves
        )

        normalized_waves = []

        for wave in waves:
            if isinstance(wave, SoundWaveFactory):
                sound_wave = wave.sound_wave
            else:
                sound_wave = wave

            # Trims the wave to the minimum length
            trimmed_wave = sound_wave[:min_length] 

            # Normalizes the amplitude
            max_amplitude = np.max(np.abs(trimmed_wave))
            if max_amplitude > 0:
                normalized_wave = (
                    trimmed_wave * (self.MAX_AMPLITUDE / max_amplitude)
                ).astype(np.int16)
            else:
                normalized_wave = trimmed_wave

            normalized_waves.append(normalized_wave)

        return normalized_waves


    def save_wave(self, file_name, file_type="txt"):
        """Saves the current sound wave to a file (either .txt or .wav)."""

        if self.sound_wave is None:
            print("No sound wave to save.")
            return

        if file_type.upper() == "WAV":
            wavfile.write(file_name, self.SAMPLING_RATE, self.sound_wave)
            print(f"Wave saved as WAV file: {file_name}")
        else:
            np.savetxt(file_name, self.sound_wave, fmt="%d")
            print(f"Wave saved as text file: {file_name}")
