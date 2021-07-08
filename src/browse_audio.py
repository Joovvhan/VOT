from glob import glob
import argparse
from pydub import AudioSegment
import librosa
from datetime import datetime
import matplotlib.pyplot as plt
import sounddevice as sd

import numpy as np

import auditok
import webrtcvad
vad = webrtcvad.Vad()
vad.set_mode(1)


def read_stream(stream):
    try:
        data = next(stream)
    except StopIteration:
        data = None
    return data


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=str, help='Streamer ID', default='')
    # parser.add_argument('--frame_secs', type=float, help='Frame seconds', default=1.0)
    parser.add_argument('--frame_secs', type=float, help='Frame seconds', default=0.03)
    args = parser.parse_args()

    files = sorted(glob(f'./wav/{args.id}/*.wav'))

    file = files[0]

    sr = librosa.get_samplerate(file)
    secs = librosa.get_duration(filename=file)
    print(sr, secs)

    hop_length = frame_length = int(sr * args.frame_secs)

    '''

    # split returns a generator of AudioRegion objects
    audio_regions = auditok.split(
        file,
        min_dur=0.3,     # minimum duration of a valid audio event in seconds
        max_dur=4,       # maximum duration of an event
        max_silence=0.3, # maximum duration of tolerated continuous silence within an event
        energy_threshold=55 # threshold of detection
    )

    for i, r in enumerate(audio_regions):

        # Regions returned by `split` have 'start' and 'end' metadata fields
        print("Region {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i, r=r))
        filename = r.save("region_{meta.start:.3f}-{meta.end:.3f}.wav")
        
        if i == 20:
            break
    
    '''
    
    stream = librosa.stream(file,
                        block_length=1,
                        frame_length=frame_length,
                        hop_length=hop_length,
                        # duration=10.0,
                        )

    data = read_stream(stream)
    # plt.figure()
    # plt.plot(data)
    # plt.show()


    audio = np.array(data)
    vad_step = len(data)
    vad_offset = vad_step / 2
    vad_result = list()

    data = (data * 2 ** 15).astype(np.int16).tobytes()
    # plt.figure()
    # plt.plot(data)
    # plt.show()
    vad_result.append(vad.is_speech(data, sr))
    # print(f'Contains speech: {vad.is_speech(data, sr)}')

    # plt.figure()
    # plt.plot(data)
    # plt.show()

    # sd.play(data, blocking=True)



    while data is not None:

        data = read_stream(stream)
        # audio = np.concatenate((audio, data))
        data = (data * 2 ** 15).astype(np.int16).tobytes()
        # print(f'Contains speech: {vad.is_speech(data, sr)}')
        vad_result.append(vad.is_speech(data, sr))

        if len(vad_result) > 10000:
            break

    
        # sd.play(data, blocking=True)
    plt.figure()
    plt.plot(vad_result)
    plt.show()

    