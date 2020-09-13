import subprocess
import os
from gtts import gTTS
from playsound import playsound

myText = "hi what is up man"

language = 'en'

output = gTTS(text=myText,lang=language,slow=False)
output.save("output.mp3")
print('saved')
playsound('output.mp3')
