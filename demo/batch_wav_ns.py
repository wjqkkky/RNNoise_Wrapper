import os
import time

from rnnoise_wrapper import RNNoise

denoiser = RNNoise()


def ns_process(f_name_audio, out_dir):
    audio = denoiser.read_wav(f_name_audio)
    filtered_audio = b''
    buffer_size_ms = 10

    start_time = time.time()
    average_work_time_per_frame = []
    for i in range(buffer_size_ms, len(audio), buffer_size_ms):
        time_per_frame = time.time()
        filtered_audio += denoiser.filter(audio[i - buffer_size_ms:i].raw_data, sample_rate=audio.frame_rate)
        average_work_time_per_frame.append(time.time() - time_per_frame)
    if len(audio) % buffer_size_ms != 0:
        time_per_frame = time.time()
        filtered_audio += denoiser.filter(audio[len(audio) - (len(audio) % buffer_size_ms):].raw_data,
                                          sample_rate=audio.frame_rate)
        average_work_time_per_frame.append(time.time() - time_per_frame)
    work_time = time.time() - start_time
    average_work_time = sum(average_work_time_per_frame) / len(average_work_time_per_frame)

    f_name_denoised_audio = os.path.basename(f_name_audio)[:f_name_audio.rfind('.wav')] + '_denoised.wav'
    f_name_denoised_audio = os.path.join(out_dir, f_name_denoised_audio)
    denoiser.write_wav(f_name_denoised_audio, filtered_audio, sample_rate=audio.frame_rate)
    print(
        '\nAudio: %s\nLength audio: %.4f s\nDenoised audio: %s\nTotal work time (by frames): %.4f s\nAverage work time (per 1 frame): %.6f s'
        % (f_name_audio, len(audio) / 1000, f_name_denoised_audio, work_time, average_work_time))

    if round(len(audio.raw_data) / 2 / 8000, 1) == round(len(filtered_audio) / 2 / 8000,
                                                         1) and audio.raw_data != filtered_audio:
        print('OK')
    else:
        print("False")


if __name__ == '__main__':
    wav_path = "./vad/70"
    out_path = "./vad/denoised/70"
    files = os.listdir(wav_path)
    for file in files:
        if not os.path.isdir(file):
            path_file = os.path.join(wav_path, file)
            ns_process(path_file, out_path)
