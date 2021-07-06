import argparse
import csv
import os
import shutil

STORAGE_DIR = ''

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=str, help='Streamer ID', default='')
    parser.add_argument('--streamer', type=str, help='Streamer Name', default='')
    args = parser.parse_args()

    with open('./meta/vot_meta.csv', 'r') as f:
        csv_reader = csv.reader(f, quotechar="'")
        query = [line for line in csv_reader if line[1] == args.streamer or line[2] == args.id]
        
    for line in query:
        print(line[0], '|', line[-1], '|', line[3])
        src = os.path.join(STORAGE_DIR, line[0] + '_audio.mp4')
        des = os.path.join('./wav', line[0] + '_audio.mp4')
        if os.path.isfile(src):
            shutil.copy(src, des)
        else:
            print(f'{src} Missing')