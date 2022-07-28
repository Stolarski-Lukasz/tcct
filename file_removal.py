import os
import glob
import schedule
import time


def delete_audio_files():
    list_of_audio_files = glob.glob('media/*.cha')
    # print(list_of_audio_files)
    for file in list_of_audio_files:
        # only these mp3 files will be removed which were created more than 5h ago (or 18000 seconds)
        # this may be changed to some other value in seconds, but the value in every() below should also be changed
        if time.time() - os.stat(file).st_mtime > 18000:
            os.remove(file)


schedule.every(5).hours.do(delete_audio_files)

while True:
    schedule.run_pending()
    time.sleep(1)

