import pyttsx3
import speech_recognition as sr
import datetime
import pywhatkit as kit
import weather
import jokes
import news
import movie_recommendation
import music
import emails
import screenshots
import images
import os
from fuzzywuzzy import fuzz
import webbrowser
import ai_chat

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak a text
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to listen to voice commands
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        command = ""
        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        return command.lower()

# Function for fuzzy matching commands
def match_command(user_command, command_list, threshold=70):
    """
    Matches the user's spoken command against a list of target phrases using fuzzy matching.

    Args:
    - user_command (str): The user's input command.
    - command_list (list): List of possible command phrases.
    - threshold (int): Minimum matching score to consider a match.

    Returns:
    - str or None: The matched command phrase or None if no match.
    """
    for target_command in command_list:
        if fuzz.ratio(user_command, target_command) >= threshold:
            return target_command
    return None

# Main function to process commands
def run_assistant():
    speak("Hello, how can I assist you today?")
    while True:
        command = listen()

        if match_command(command, ['time', 'what time is it', 'current time', 'whats the time']):
            speak(f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}")

        elif match_command(command, ['date', 'what is the date today', 'today\'s date']):
            speak(f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}")

        elif match_command(command, ['weather', 'how is the weather today', 'current weather today']):
            weather_info = weather.get_weather()
            speak(weather_info)

        elif match_command(command, ['joke', 'tell me a joke', 'make me laugh']):
            joke = jokes.get_joke()
            speak(joke)

        elif match_command(command, ['news', 'latest news', 'tell me the news']):
            news_info = news.get_latest_news()
            speak(news_info)

        elif 'open' in command:
            if 'google' in command:
                speak("Opening Google.")
                import webbrowser
                webbrowser.open('https://www.google.com')
            elif 'youtube' in command:
                speak("Opening YouTube.")
                import webbrowser
                webbrowser.open('https://www.youtube.com')
            # Add more website handling here as needed
            
        elif match_command(command, ['movie', 'recommend a movie', 'suggest a movie']):
            recommendation = movie_recommendation.get_movie_recommendation()
            speak(f"How about watching {recommendation}.")

        elif 'music' in command:
            music.play_music()

        elif 'screenshot' in command:
            screenshots.take_screenshot()

        elif match_command(command, ['generate image', 'image', 'create image', 'make an image']):
            images.generate_image()

        elif 'gmail' in command or 'mail' in command:
            emails.open_gmail()
        
        elif 'chat' in command or 'talk' in command:
            speak("Sure! What would you like to discuss?")
            user_prompt = listen()
            if user_prompt:
                response = ai_chat.generate_response(user_prompt)
                speak(response)
    
        elif match_command(command, ['exit', 'quit', 'goodbye']):
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't catch that. Please try again.")

if __name__ == "__main__":
    run_assistant()
