# Copy of script by TabsNotSpaces, revised by murla.

## TabsNotSpaces and murla 2021, ‘Answer to “Convert multiple .mp3 files (or single .m4a) into .m4b with ffmpeg and afconvert on macOS”’, Ask Different, retrieved October 10, 2022, from <https://apple.stackexchange.com/a/426095>.

import re
import glob
from mutagen.mp3 import MP3
import os
import datetime
from pprint import pprint

chapterFileName = "chapters.txt"
metadataFileName = "FFMETADATAFILE"

def main():
   global chapterFileName
   global metadataFileName

   print("This script will help generate an FFMETADATA file to facilitate\nconverting an .m4a to a .m4b file")

   # scan given directory for file type
   directory=input('Directory (default pwd): ') or os.getcwd()
   print('   using: "' + directory + '"')
   chapterFileName = directory + "/chapters.txt";
   metadataFileName = directory + "/FFMETADATAFILE"

   skip = input('Skip chapter.txt creation? (default n): ') or 'n'
   if skip == 'y':
      createMetadataFile()
      return

   fileType=input('Input audio file type (default mp3): ') or 'mp3'
   print('   using: "' + fileType + '"')
   numberSeparator=input('Enumeration separator (symbol/phrase between enumeration and title): ') or ''
   print('   using: "' + (numberSeparator or '(blank)') + '"')
   if not directory or not fileType:
      print('Input missing - exiting')
      return

   fileNames = list()
   for file in glob.glob(directory + '/*.' + fileType):
      fileNames.append(file)
   fileNames.sort()

   rawChapters = list()
   currentTimestamp = 0 # in seconds
   for file in fileNames:
      audioLength = ''
      if fileType == 'mp3':
         audioLength = MP3(file).info.length
      else:
         audioLength = with_ffprobe(file)

      
      time = str(datetime.timedelta(seconds=currentTimestamp)) + '.000'

      title = os.path.splitext(file)[0].split('/')[-1]
      if numberSeparator != '':
         title = numberSeparator.join(title.split(numberSeparator)[1:])

      rawChapters.append(time + ' ' + title)
      currentTimestamp = int(currentTimestamp + audioLength)

   with open(chapterFileName, "w") as chaptersFile:
      for chapter in rawChapters:
         chaptersFile.write(chapter + "\n")

   input('File created at "' + chapterFileName + '". Review to make sure it looks right\n ("<timestamp> <title>"), then hit Enter to continue... ')
   createMetadataFile()

def createMetadataFile():
   global chapterFileName
   global metadataFileName

   # import chapters and create ffmetadatafile
   chapters = list()
   with open(chapterFileName, 'r') as f:
      for line in f:
         x = re.match(r"(\d*):(\d{2}):(\d{2}).(\d{3}) (.*)", line)
         hrs = int(x.group(1))
         mins = int(x.group(2))
         secs = int(x.group(3))
         title = x.group(5)

         minutes = (hrs * 60) + mins
         seconds = secs + (minutes * 60)
         timestamp = (seconds * 1000)
         chap = {
            "title": title,
            "startTime": timestamp
         }
         chapters.append(chap)

   text = ";FFMETADATA1\n"
   for i in range(len(chapters)-1):
      chap = chapters[i]
      title = chap['title']
      start = chap['startTime']
      end = chapters[i+1]['startTime']-1
      text += f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={start}\nEND={end}\ntitle={title}\n"

   with open(metadataFileName, "w") as myfile:
       myfile.write(text)
   
   print('Created metadata file at "' + metadataFileName + '"')
   removeChapters = input('Remove chapter.txt? (default n): ') or 'n'
   if removeChapters == 'y':
      os.remove(chapterFileName)


def with_ffprobe(filename):
    import subprocess, json

    result = subprocess.check_output(
            f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{filename}"',
            shell=True).decode()
    fields = json.loads(result)['streams'][0]
    return float(fields['duration'])

main()
