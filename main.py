from gtts import gTTS
from subprocess import call

def speak(message):
    tts = gTTS(message, lang='pt-br')
    tts.save('audios/feedback.mp3')

    call(['mpg123', 'audios/feedback.mp3'])

speak('Acalma o coração.')