# audiobook_chapters - README.md

## Group of scripts to add chapters to audiobooks.

Firstly download the audiobook then

```bash
# get chapters from xml file
python3 extract_overdrive_chapters.py [optional directory path]

# convert to ffmpeg metadata file
python3 create_FFMETADATAFILE.py

# When script asks 'Skip chapter.txt creation?' type y 

# combine mp3 parts into one file
ffmpeg -f concat -safe 0 -i <(for f in ./*.mp3; do echo "file '$PWD/$f'"; done) -c copy output.mp3

# convert mp3 to aac (ie. m4a)
ffmpeg -i output.mp3 -c:a libfdk_aac output.m4a

# add chapters to m4a/m4b file

ffmpeg -i output.m4a -i FFMETADATAFILE -map_metadata 1 -codec copy output.m4b
```

Lastly add metadata using [kid3](https://sourceforge.net/projects/kid3/). Ben Dodson's [iTunes Artwork Finder](https://bendodson.com/projects/itunes-artwork-finder/index.html) is great for getting audiobook's cover images.

## References

*iTunes Artwork Finder by Ben Dodson*, retrieved 10 October 2022, from <https://bendodson.com/projects/itunes-artwork-finder/index.html>.

*Kid3 Tag Editor*, retrieved 10 October 2022, from <https://sourceforge.net/projects/kid3/>.

Petersen, C 2022 *python script to extract chapters · Issue #39 · chbrown/overdrive*, @ex-nerd, retrieved 10 October 2022, from <https://github.com/chbrown/overdrive/issues/39#issuecomment-1267998153>.

slhck 2011, *Answer to “FFmpeg command to convert MP3 to AAC”*, Super User, retrieved 10 October 2022, from <https://superuser.com/a/370637>.

TabsNotSpaces and murla 2021, *Answer to “Convert multiple .mp3 files (or single .m4a) into .m4b with ffmpeg and afconvert on macOS”*, Ask Different, retrieved 10 October 2022, from <https://apple.stackexchange.com/a/426095>.
