from pydub import AudioSegment

# Load the audio file
audio = AudioSegment.from_file("./sample.wav")
silence_audio = audio - 10

silence_audio.fade_in(10000).fade_out(10000).export("output.wav", format="wav")