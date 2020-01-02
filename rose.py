from gtts import gTTS
import speech_recognition as sr
from subprocess import call
from requests import get
from bs4 import BeautifulSoup


##configurações
hotword = 'rose'



##funcoes principais
def monitora_microfone():
    # esta biblioteca esta sendo desativada Google Speech Recognition
    # outra biblioteca testada foi da IBM porem é paga a partir de 100 minutos de utilizacao mensal, criar user e password no
    microfone = sr.Recognizer()
    with sr.Microphone() as source:

        while True:    
            print("Aguardando o comando!")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google(audio, language='pt-BR')
                trigger = trigger.lower()

                if hotword in trigger:
                    print('comando:', trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return trigger

def responde(arquivo):
    call(['mpg123', 'audios/'+ arquivo +'.mp3'])


def cria_audio(messagem):
    tts = gTTS(messagem, lang='pt-br')
    tts.save('audios/mensagem.mp3')
    call(['mpg123', 'audios/mensagem.mp3'])

def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()
    else:
        responde('comando-invalido')



##funcoes comandos
def ultimas_noticias():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419')
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:2]:
        mensagem = item.title.text
        print(mensagem)
        cria_audio(mensagem)

def main():
    monitora_microfone()

main()
#ultimas_noticias()