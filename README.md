# subtitle-wordcounter
Counts all the words in (UTF-8 encoded) .srt files in a folder

How often does someone say 'danger' and 'zone' in a sentence? Which words to drink to during that one episode you're about to watch? These statistics are made easy-peezy with this little script.

The easiest way to run this is to copy both files to the folder where your subtitles are. Then simply run the script (for instance by typing `python3 subtitle-wordcounter.py`) and press enter twice. Now you will automatically be given the top 10 most-used words for all .srt files in the folder, as well as all words that, in total, have been used more than 100 times.

Many words that are heavily used in the English language have been filtered out of the results (even out of the counting algorithm). You can easily change which words are left out by editing the contents of 'excludes.txt'.

#### A notice on versions
This was written in python 3.4, so be weary of version issues when running on 2.x

#### A notice on UTF-8 encodiding ==
The .open() function in python automatically assumes that files are encoded in UTF-8. The script will even try to parse the file if it isn't UTF-8, but it will break once it comes across a character it cannot decode. Resolving this is on my to-do-list.
