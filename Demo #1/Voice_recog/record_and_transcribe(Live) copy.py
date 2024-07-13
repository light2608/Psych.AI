import sounddevice as sd
import speech_recognition as sr

def record_audio(duration, sample_rate):
    print(f"Recording for {duration} seconds...")
    myrecording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print("Recording done.")
    return myrecording

def transcribe_audio(audio_data, sample_rate):
    recognizer = sr.Recognizer()
    audio_source = sr.AudioData(audio_data.tobytes(), sample_rate, 2)  # 2 bytes per sample (16-bit PCM audio)
    
    try:
        text = recognizer.recognize_google(audio_source)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    duration = 10  # seconds
    sample_rate = 16000  # 16 kHz (you can adjust this if needed)

    # Record audio
    audio_data = record_audio(duration, sample_rate)

    # Transcribe audio to text
    text = transcribe_audio(audio_data, sample_rate)
    if text:
        print(f"You said: {text}")
