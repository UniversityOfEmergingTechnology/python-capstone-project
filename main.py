import os
import speech_recognition as sr
from gtts import gTTS
import webbrowser
import datetime
from openai import OpenAI
from config import apikey


client = OpenAI(api_key = apikey)

def say(text):
    tts = gTTS(text=text, lang='en')
    tts.save("speech.mp3")
    os.system("afplay speech.mp3") 

# def say(text) :
#     os.system(f'say -r 100 "{text}"')  

chatStr = ""
def chat(query):
    global chatStr
    chatStr = f"Mudit: {query}\n"
    print(chatStr)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if response.choices:
        responseAudio = client.audio.speech.create(
            model = "tts-1",
            voice = "alloy",
            input = response.choices[0].message.content,
        )
        chatStr = f"Virtual Assistant : {response.choices[0].message.content}\n"
        print(chatStr)
        responseAudio.stream_to_file("output.mp3")
        os.system("afplay output.mp3")

 
def ai(prompt):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "user",
        "content": prompt
        }
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    # Accessing the message content
    if response.choices:
        message_content = response.choices[0].message.content
        print(message_content)
    else:
        print("No response generated.")
        return
    
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    answer = response.choices[0].message.content

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(answer)




def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said this : {query}\n")
            return query
        except Exception as e:
            return "Some error occured. Sorry from my side."


if __name__ == '__main__':
    say("Hello , I am an virtual assistant Mudit. What you want me to do?")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        if "open music" in query:
            musicPath = "/Users/mudit/Desktop/PythonProject/Capstone/speech.mp3"
            os.system(f"open {musicPath}")
        elif "the time" in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir time is {time}")
        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "exit".lower() in query.lower():
            say("Bye Bye Sir , Have a nice day")
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
        # say(query)