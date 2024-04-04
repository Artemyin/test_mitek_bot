from pydub import AudioSegment


def convert_ogg_to_wav(input_file: str, output_file: str, sample_rate=16000):
    try:
        audio = AudioSegment.from_ogg(input_file)
        audio = audio.set_frame_rate(sample_rate)
        audio.export(output_file, format="wav")
    except Exception as e:
        print(f"Error converting {input_file} to .wav: {e}")
