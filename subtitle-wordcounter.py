
# coding: utf-8

"""
    Copyright 2015 Jacob Boon

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

def intro(words_together, path):
    print("")
    print("  == SUBTITLE WORD COUNTER ==")
    print("     written by Jacob Boon")
    print("")
    print("This script will count the words from subtitle files in a given folder")
    print("")

    path = input("In which folder should I look? Press enter to look here.")
    if path == "":
        path = "."
    

    print("Ok, I see the following files:")
    for filename in sorted(glob.glob(os.path.join(path, '*.srt'))):
        print(filename)
    
    print("")
    print("Do you want me to check for two specific words appearing together?")
    answer = input("(y/n) ")
    while answer.lower() == 'y' or answer.lower() == 'yes':
        word1 = ""
        word2 = ""
        while word1 == "":
            word1 = input("Word 1: ")
        while word2 == "":
            word2 = input("Word 2: ")
        words_together.append([0,word1,word2])
        answer = input("Want me to check for two more? (y/n) ")

    print("")
    print("Ok, here I go!")
    print("")
    


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False




def is_timeline(t):
    if t[12:17] == " --> ":
        return True
    else:
        return False




def count_words(dictionary, wordlist, excludes):
    for w in wordlist:
        w = w.lower()
        if w in dictionary:
            dictionary[w] += 1
        elif w not in excludes:
            dictionary[w] = 1




def make_big_numbers(wordlist):
    i = 1
    big = ['one', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'hundred', 'thousand', 'million', 'billion', 'trillion']
    while i in range(1, len(wordlist)):
        if is_number(wordlist[i]) == True and is_number(wordlist[i-1]) == True:
            wordlist[i] = "%s.%s" % (wordlist[i-1], wordlist[i])
            del wordlist[i-1]
            i = i-1
        elif is_number(wordlist[i-1]) == True and wordlist[i] in big:
            wordlist[i] = "%s %s" % (wordlist[i-1], wordlist[i])
            del wordlist[i-1]
            i = i-1
        elif wordlist[i-1] in big and wordlist[i] in big:
            wordlist[i] = "%s %s" % (wordlist[i-1], wordlist[i])
            del wordlist[i-1]
            i = i-1
        i += 1




def print_most_used(wordlist, cutoff):
    maxlength = 1
    # find the longest number for alignment purposes
    for w in wordlist:
        if len(str(w[1])) > maxlength:
            maxlength = len(str(w[1]))
    
    # print only the words that appear often enough
    for w in wordlist:
        if w[1] > cutoff:
            spaces = maxlength - len(str(w[1]))
            print(" "*(spaces),w[1]," | ",w[0], sep='')




def print_top_10(wordlist, episode):
    maxlength = 1
    # find the longest number for alignment purposes
    for w in wordlist:
        if len(str(w[1])) > maxlength:
            maxlength = len(str(w[1]))
    
    last_slash = 0
    for i in range(0,len(episode)-4):
        if episode[i] == '/':
            last_slash = i
    print("")
    print("In the episode '", episode[last_slash:len(episode)-4],"' these are the top 10 most-used words:", sep='')
    counter = 10
    for w in wordlist:
        if counter > 0:
            spaces = maxlength - len(str(w[1]))
            print(" "*(spaces),w[1]," | ",w[0], sep='')
            counter -= 1
        else:
            break




def count_togethers(checklist, wordlist):
    # checks wether the sets of words in checklist appear together in the wordlist
    # the checklist should be a list of lists, where each list has the # of occurences as 0-th value
    for c in checklist:
        together = True
        for i in range(1,len(c)):
#            print("Gonna check for", c[i], "in", wordlist)
            if c[i] not in wordlist:
                together = False # one of the words does not appear
        if together: # if all the words have been found
            c[0] += 1
#            print("I got one!", c)




def print_words_together(checklist):
    for c in checklist:
        print("")
        print("The words",end=' ')
        for i in range(1,len(c)):
            if i > 1:
                print("and", end=' ')
            print(c[i],end=' ')
        print("appear together", c[0], "times")




def count_words_in_episode(dictionary, episode):
    episode_dictionary = {}
    wordlist = []
    line_number = 0
    lines = {}
    f = open(episode)
    current_time = time.strptime("00:00:00", "%H:%M:%S")
    for line in f:
        if is_number(line):
            if line_number != 0:
                count_words(dictionary, lines[line_number], excludes)
                count_words(episode_dictionary, lines[line_number],excludes)
                count_togethers(words_together,lines[line_number])
            line_number = int(line)
        
        elif is_timeline(line):
            current_time = time.strptime(line[0:8], "%H:%M:%S")
        
        elif line != "\n":
            wordlist = re.sub("[^a-zA-Z0-9_-]", " ",  line).split()
            make_big_numbers(wordlist)
            if line_number in lines:
                lines[line_number] = lines[line_number] + wordlist
            else:
                lines[line_number] = wordlist
            
    
    count_words(dictionary, lines[line_number], excludes)
    count_words(episode_dictionary, lines[line_number],excludes)
    count_togethers(words_together,lines[line_number])
    
    sorted_dict = sorted(episode_dictionary.items(), key=operator.itemgetter(1), reverse=True)
    print_top_10(sorted_dict, episode)




import re
import time
import operator
import glob
import os

words_together = []
path = ""
number_of_episodes = 0

with open('excludes.txt') as e:
    excludes = e.read().splitlines()
dictionary = {}

cutoff_frequency = 100

intro(words_together, path)
    
for filename in sorted(glob.glob(os.path.join(path, '*.srt'))):
#for filename in os.listdir(path):
    count_words_in_episode(dictionary, filename)
    number_of_episodes += 1
    
print("")
print("Over all", number_of_episodes, "episodes, these words appear more than", cutoff_frequency, "times")
sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
print_most_used(sorted_dict, cutoff_frequency)
print_words_together(words_together)

