#========== Imports
import re
import speech_recognition as sr
from autocorrect import Speller
import subprocess
import playsound as ps
import time
import webbrowser


#========== Setting
assisent_name = 'hey jack'
keywords = [(assisent_name, 1), ]
search_engines = {
    'google'     :'https://www.google.com/search?q=',
    # 'bing'       : 'https://www.bing.com/search?q=',
    # 'duckduckgo' : 'https://duckduckgo.com/?t=',
}

#========== Paths
FireFox_path = 'Enter the firefox app path here'


#========== Define Classes
spell = Speller() #define speller
recognizer = sr.Recognizer() #define recognizer
microphone = sr.Microphone() #define microphone
webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(FireFox_path),1)


#========== AudioPlayer
def playsound(file_name):
    ps.playsound(f'audios/{file_name}',True)


#========== Do commands
def recognize_the_command(text):
    text = text.lower()
    if 'open firefox' in text:
        if 'and search' in text:
            
            query = text.partition(' and search ')[2]
            if query:
                firefox(query)
            else:
                firefox()
        else:
            firefox()
    else:
        playsound('cant-understand.mp3')
        recognize_main()


#========== Voice to Text process
def spell_checker(text):
    clean_text = re.sub(r'(.)\1+', r'\1\1',text) #remove_extra_letters 
    checked_spell_text = spell(clean_text) #spelling checker
    print('you said :',checked_spell_text)
    return checked_spell_text

def recognize_main():
    audio_data = recognizer.listen(microphone)
    print('recognizing your voice...')
    text = recognizer.recognize_google(audio_data)
    text = spell_checker(text)

    #check for exit
    if 'thank you and goodbye' in text:
        playsound('goodbye.mp3')
    else:
        recognize_the_command(text)


#========== Check if program running right now
def check_active_proccess(path):
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description, Path' 
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    programs_list = [program.decode().rstrip() for program in proc.stdout if not program.decode()[0].isspace() ]
    for i in programs_list:
        if path in i:
            return True
    return False


#========== All commands functions
def firefox(query=''):
    if query:
        webbrowser.get('firefox').open_new_tab(search_engines['google']+query)
    else:
        # if program already opened
        if check_active_proccess(FireFox_path):
            playsound('firefox.mp3')
        else:
            webbrowser.get('firefox')


# Check to see if it's called and start
def callapp(recognizer, audio):
    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
        if assisent_name in speech_as_text:
            playsound('help.mp3')
            print('listening to you...')
            recognize_main()
    except:
        print('cant get it')


def main():
    print('lets go')
    recognizer.listen_in_background(microphone, callapp)
    time.sleep(1000000)

if __name__ == '__main__':
    main()