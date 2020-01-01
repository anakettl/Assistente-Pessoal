import speech_recognition as sr
from subprocess import call

##configurações
hotword = 'rose'



##codigo principal
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
                    ##executar os comandos
                    responde('feedback')
                    break

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return trigger

def responde(arquivo):
    call(['mpg123', 'audios/'+ arquivo +'.mp3'])


def main():
    monitora_microfone()

main()