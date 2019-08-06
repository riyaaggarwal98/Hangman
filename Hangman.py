# Hangman Game (Console Mode Only)

import random
import time
import threading
import requests
from bs4 import BeautifulSoup


class Thread1(threading.Thread):
    def run(self):
        link = requests.get('http://www.dictionary.com/wordoftheday')
        soup = BeautifulSoup(link.text, 'html.parser')
        tag = soup.find('div', class_='wotd-item__definition')
        word = ""
        if tag.find('h1') is not None:
            word = tag.find('h1').text.strip()

        file1 = open('Words.txt', 'r')

        data = file1.readlines()
        words = []
        for elm in data:
            words.append(elm.strip())
        if word.upper() in words:
            pass
        else:
            file2 = open('Words.txt', 'a')
            file2.write('\n'+word.upper())
            file2.close()

        file1.close()


class HangmanLexicon:
    words = []

    def setWords(self, words):
        HangmanLexicon.words = words

    def getCount(self):
        n = len(HangmanLexicon.words)
        return n

    def getWord(self):
        word = random.choice(HangmanLexicon.words)
        return word

    def getMeaning(self, wd):
        url = 'http://www.dictionary.com/browse/'
        link = url + wd
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        spanTags = soup.find_all('span', class_='one-click-content')
        meanings = []
        for tag in spanTags:
            mean = tag.text.strip()
            meanings.append(mean)
        meaning = meanings[0]
        return meaning


def getPattern(ind):
    pattern = ['\n _\n', '| ', '|\n', '| ',
               '0\n', ' -|-\n', ' / \\ ', '\n______']
    result = ""
    for i in range(ind):
        result += pattern[i]
    return result


t1 = Thread1()
t1.start()
file = open('Words.txt', 'r')
data = file.readlines()
words = []
for elm in data:
    words.append(elm.strip())
# print (words)
h1 = HangmanLexicon()
h1.setWords(words)

word = h1.getWord()
meaning = h1.getMeaning(word)

n = len(word)
puzzleWord = ""
for i in range(n):
    if word[i] == '-' or word[i] == ' ':
        puzzleWord += word[i]
    else:
        puzzleWord += '-'
# print (word)
# print (puzzleWord)
time.sleep(0.5)
print()
print('--------------------')
print('Welcome to Hangman!')
print('--------------------')
time.sleep(0.5)

print()
print('Please go through the rules before you start to play!')
print()
time.sleep(1)
print('-------RULES--------')
time.sleep(1)
print('1. Your guess must be an alphabet.')
time.sleep(2)
print('2. Only 1 alphabet can be guessed in 1 turn.')
time.sleep(2)
print('3. If you enter anything EXCEPT a SINGLE ALPHABET,\nthen every second wrong guess would reduce your number of guesses by 1.')
time.sleep(3.25)
print('4. If you guess the correct alphabet again,\nthen every second such guess would reduce your number of guesses by 1.')
time.sleep(3.25)
print('5. You will have 8 guesses to find out the word correctly.')
time.sleep(2)
print('6. Every wrong alphabet guess would result in reduction of number of guesses by 1.')
time.sleep(2.5)
print('7. You would lose the game if you run out of your guesses.')
time.sleep(2)
print('--------------------')
print()

j = 0
y = 0
g = 0
ind = 0
guesses = 8
guessList = []
print('Start Guessing and save the man from Hanging!')
print()
while guesses > 0:
    time.sleep(0.5)
    print('The word now looks like:', puzzleWord)
    print('Save the man or watch him hang:', getPattern(ind))

    if guesses > 1:
        print('You have', guesses, 'guesses left.')
    else:
        print('You have only', guesses, 'guess left.')

    guess = input('Your guess: ')
    if guess.isalpha():
        guess = guess.upper()

        m = len(guess)
        if m == 1:
            if guess in word:
                if guess not in guessList:
                    print('That guess is correct')
                    guessList.append(guess)
                else:
                    print('You have already made that guess!')
                    g += 1
                    if g == 1:
                        continue
                    else:
                        guesses -= 1
                        g = 0
                        ind += 1

            else:
                guesses -= 1
                ind += 1
                print('There are no', guess+"'s in the word!")

            index = []
            for i in range(len(word)):
                if word[i] == guess:
                    index.append(i)
                else:
                    pass
            # print (index)
            k = len(index)
            if k != 0:
                for elm in index:
                    # print (elm)
                    puzzleWord = puzzleWord[0:elm] + guess + puzzleWord[elm+1:]
            else:
                pass
        else:
            print('You can guess only 1 character at a time!')
            y += 1
            if y == 1:
                continue
            else:
                guesses -= 1
                y = 0
                ind += 1

        time.sleep(0.5)
        if puzzleWord == word:
            print('You Win!')
            print("You saved the man's life!")
            print("{} means: {}".format(word, meaning))
            break
        elif guesses == 0:
            print('The word was:', word,",meaning:",meaning)
            print("You couldn't save the man from hanging!")
            print(getPattern(ind))
            print('\nYou Lose!')
    else:
        print('Your guess must be an alphabet only!')
        j += 1
        if j == 1:
            continue
        else:
            guesses -= 1
            j = 0
            ind += 1