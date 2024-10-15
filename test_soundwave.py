import os
import pytest
from soundwave import SoundWaveFactory

@pytest.fixture
def sound_wave_factory():
    """Fixture to initialize a new instance of SoundWaveFactory."""
    return SoundWaveFactory()

def test_create_note(sound_wave_factory):
    """Test if a sound wave is created when a note is generated."""
    sound_wave = sound_wave_factory.create_note()
    assert sound_wave is not None, "No sound wave generated for note 'a4'"

def test_save_wave_as_txt(sound_wave_factory):
    """Test saving the sound wave as a .txt file."""
    sound_wave_factory.create_note()
    sound_wave_factory.save_wave('a4_sin.txt')
    assert os.path.exists('a4_sin.txt'), ".txt file not saved"
    os.remove('a4_sin.txt')

def test_save_wave_as_wav(sound_wave_factory):
    """Test saving the sound wave as a .wav file."""
    sound_wave_factory.create_note()
    sound_wave_factory.save_wave('a4_sin.wav', file_type='WAV')
    assert os.path.exists('a4_sin.wav'), ".wav file not saved"
    os.remove('a4_sin.wav')

def test_read_wave_from_txt(sound_wave_factory):
    """Test reading the sound wave from a .txt file."""
    sound_wave_factory.create_note()
    sound_wave_factory.save_wave('a4_sin.txt')
    sound_wave_factory.read_wave_from_txt('a4_sin.txt')
    assert sound_wave_factory.sound_wave is not None, "No wave loaded from .txt file"
    os.remove('a4_sin.txt')

def test_normalize_sound_waves():
    """Test normalizing sound waves of different lengths and amplitudes."""
    factory1 = SoundWaveFactory()
    factory1.create_note()

    factory2 = SoundWaveFactory()
    factory2.create_note(note="g4")

    normalized_waves = factory1.normalize_sound_waves(factory1, factory2)
    assert len(normalized_waves) == 2, "Normalization of waves failed"
    assert len(normalized_waves[0]) == len(normalized_waves[1]), "Normalized waves are not of equal length"

def test_print_wave_details(capsys, sound_wave_factory):
    """Test printing wave details."""
    sound_wave_factory.create_note()
    sound_wave_factory.print_wave_details()
    
    captured = capsys.readouterr()
    assert "Duration" in captured.out, "Wave details not printed correctly"

