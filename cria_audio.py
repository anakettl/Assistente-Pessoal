from gtts import gTTS
from subprocess import call

def speak(message):
    tts = gTTS(message, lang='pt-br')
    tts.save('audios/comando-invalido.mp3')

    call(['mpg123', 'audios/comando-invalido.mp3'])

speak('Não sou obrigada.')