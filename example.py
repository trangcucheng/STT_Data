from pydub import AudioSegment
from pydub.silence import split_on_silence
 
sound_file = AudioSegment.from_file("demo_file.mp3")
print(len(sound_file))