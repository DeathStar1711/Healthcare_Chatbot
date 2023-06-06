from flask import Flask, render_template, request, after_this_request
import requests
import os
import openai
from gtts import gTTS
from playsound import playsound

app = Flask(__name__, template_folder="")
messages = []
audio_path = 'assistant_response.mp3'


@app.route('/')
def home():
    global messages
    messages = []
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    global audio_path
    if not messages:
        condition = request.form.get('condition')
        severity = request.form.get('severity')
        openai.api_key = os.getenv("API_KEY_OPENAI")
        messages.append({'role': 'system',
                         'content': f'You are a Healthcare chatbot. User has health problems due to {condition} with {severity} severity. First of all, greet him  and then wait for the user to reply.'})
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages)
        chat_response = completion['choices'][0]['message']['content']
        tts = gTTS(text=chat_response, lang='en')
        tts.save('assistant_response.mp3')
        playsound(audio_path)
        os.remove(path=audio_path)
        messages.append({'role': 'assistant', 'content': chat_response})
        return render_template('chat.html', messages=messages)
    else:
        user_message = request.form.get('user_message')
        messages.append({'role': 'user', 'content': user_message})
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages)
        chat_response = completion['choices'][0]['message']['content']
        tts = gTTS(text=chat_response, lang='en')
        tts.save('assistant_response.mp3')
        playsound(audio_path)
        os.remove(path=audio_path)
        messages.append({'role': 'assistant', 'content': chat_response})
        return render_template('chat.html', messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
