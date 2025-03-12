import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to recognize speech
def recognize_speech_from_microphone():
    try:
        # Use the microphone as the audio source
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=2)  # Adjust to ambient noise
            
            print("Listening for your speech...")
            audio = recognizer.listen(source)  # Capture the audio input
            
            print("Processing your speech...")
            # Convert speech to text
            text = recognizer.recognize_google(audio)
            print(f"Recognized Speech: {text}")
            
            return text
    
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Request error from Google Speech Recognition service: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the speech recognizer
if __name__ == "__main__":
    print("Speech Recognizer System")
    print("------------------------")
    result = recognize_speech_from_microphone()
    if result:
        print(f"Final Output: {result}")
