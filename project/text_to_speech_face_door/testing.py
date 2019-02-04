from gtts import gTTS
import os
tts = gTTS(text='Bienvenido, Juan Camilo?', lang='es')
tts.save("bienvenido.mp3")
os.system("mpg321 good.mp3")