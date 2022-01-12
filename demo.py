from pydub import AudioSegment
from pydub.silence import split_on_silence
 
sound_file = AudioSegment.from_file("demo_file.mp3")
audio_chunks = split_on_silence(sound_file, min_silence_len=1000, silence_thresh=-40 )
 
for i, chunk in enumerate(audio_chunks):
   out_file = "chunk_{0}.mp3".format(i)
   print("exporting", out_file)
   chunk.export(out_file, format="mp3")