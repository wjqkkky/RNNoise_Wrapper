import wave

import numpy as np
from pydub import AudioSegment

from rnnoise_wrapper import RNNoise

denoiser = RNNoise()


def ns_process(pcm_str):
    audio = AudioSegment(data=pcm_str, sample_width=2, frame_rate=8000, channels=1)
    filtered_audio = b''
    buffer_size_ms = 10

    for i in range(buffer_size_ms, len(audio), buffer_size_ms):
        filtered_audio += denoiser.filter(audio[i - buffer_size_ms:i].raw_data, sample_rate=audio.frame_rate)
    if len(audio) % buffer_size_ms != 0:
        filtered_audio += denoiser.filter(audio[len(audio) - (len(audio) % buffer_size_ms):].raw_data,
                                          sample_rate=audio.frame_rate)

    if round(len(audio.raw_data) / 2 / 8000, 1) == round(len(filtered_audio) / 2 / 8000,
                                                         1) and audio.raw_data != filtered_audio:
        print('OK')
    else:
        print("False")
    return filtered_audio


if __name__ == '__main__':
    file_name = "lilin_c5f4730d-6f8c-4084-b851-23fec61af082_2213b6d2-4824-4c39-a974-2c32fda891fc_8.pcm"
    pcm = open(file_name, "rb")
    data = pcm.read()
    ns_data = ns_process(data)

    out_name = "ns.wav"
    wave_out = wave.open(out_name, 'wb')
    wave_out.setnchannels(1)
    wave_out.setsampwidth(2)
    wave_out.setframerate(8000)
    wave_out.writeframes(ns_data)
    wave_out.close()
