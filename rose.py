from gtts import gTTS
import speech_recognition as sr
from subprocess import call
from requests import get
from bs4 import BeautifulSoup
import webbrowser as browser


##configurações
hotword = 'rose'



##funcoes principais
def monitora_microfone():
    # esta biblioteca esta sendo desativada Google Speech Recognition
    # outra biblioteca testada foi da IBM porem é paga a partir de 100 minutos de utilizacao mensal, criar user e password no site
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


def cria_audio(mensagem):
    tts = gTTS(mensagem, lang='pt-br')
    tts.save('audios/mensagem.mp3')
    print('Rose: ', mensagem)
    call(['mpg123', 'audios/mensagem.mp3'])

def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()

    if 'toca' in trigger:
        if 'queen' in trigger:
            playlists('queen')
        if 'kiss' in trigger:
            playlists('kiss')
        else:
            print('nao entendi o nome')

    if 'tempo hoje' in trigger:
        previsao_tempo(tempo=True)
    
    if 'temperatura hoje' in trigger:
        previsao_tempo(minmax=True)


    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem + '?')
        print('Comando inválido', mensagem)
        responde('comando-invalido')



##funcoes comandos
def ultimas_noticias():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419')
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:2]:
        mensagem = item.title.text
        cria_audio(mensagem)

def playlists(album):
    if album == 'queen':
        browser.open('https://open.spotify.com/album/6i6folBtxKV28WX3msQ4FE')
    elif album == 'kiss':
        browser.open('https://open.spotify.com/album/5rf66ReWkobYT88G0Ky52y')
    else:
        print('album nao encontrado')


def previsao_tempo(tempo=False, minmax=False):
    site = get('http://api.openweathermap.org/data/2.5/weather?q=porto%20alegre,br&APPID=7cbcc39c129cb9d3caecc17c70258968&units=metric&lang=pt')
    clima = site.json()
    temperatura=clima['main']['temp']
    minima=clima['main']['temp_min']
    maxima=clima['main']['temp_max']
    descricao=clima['weather'][0]['description']

    if tempo:
        mensagem=f'No momento fazem {temperatura} graus com: {descricao}'
    if minmax:
        mensagem=f'Mínima de {minima} e máxima de {maxima}'
    
    cria_audio(mensagem)


##programa principal
def main():
    monitora_microfone()

main()




