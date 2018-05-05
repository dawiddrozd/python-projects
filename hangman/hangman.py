from os import system
import sys
import random


class Hangman(object):
    def secret_word(self):
        return self._secret_word

    def __init__(self, chances, file):
        self._chances = chances
        try:
            with open(file) as f:
                words = f.read().splitlines()
        except FileNotFoundError:
            print("File not found. Try again with another filename.")
            exit(1)
        except:
            print("Unexpected error occurs")
            exit(1)
        try:
            self._secret_word = str(random.choice(words)).upper()
        except IndexError:
            print("Input file has the wrong format.")
            exit(1)
        if len(self._secret_word) < 2 or not any(str(letter).isalpha() for letter in self._secret_word):
            print("Input file has the wrong format.")
            exit(1)
        self._dict = {}
        for i in self._secret_word:
            if not i.isalpha():
                self._dict[i] = True
            else:
                self._dict[i] = False

    def guess(self, sign):
        if not self.is_correct(sign):
            print("Only letters are allowed!")
            return
        sign = sign.upper()
        if sign in self._dict and not self._dict[sign]:
            self._dict[sign] = True
            print("{0} is the right choice!".format(sign))
        else:
            self._chances -= 1
            print("No, it's not {0}. Try again! You have {1} chances.".format(sign, self._chances))

    def print_word(self):
        for sign in self._secret_word:
            if self._dict[sign]:
                print(sign, end=' ')
            else:
                print('_', end=' ')

    def has_chances(self):
        return self._chances > 0

    def guessed_word(self):
        return all(item is True for item in self._dict.values())

    @staticmethod
    def is_correct(char):
        return isinstance(char, str) and len(str(char)) > 0 and str(char[0]).isalpha()


nr_of_chances = 10
if len(sys.argv) > 1:
    hangman = Hangman(chances=nr_of_chances, file=sys.argv[1])
else:
    print("First parameter should be a filename!")
    exit(1)
print("Let's start game! You have {0} chances".format(nr_of_chances))
print("Try to guess one letter")

running = True
while running:
    hangman.print_word()
    char = input("\nYour letter: ")
    system('clear')
    hangman.guess(str(char))
    if hangman.guessed_word():
        hangman.print_word()
        print("\nYou won! Congratulations!")
        running = False
    elif not hangman.has_chances():
        print("You failed. Proper word: {0}. Try again with other word.".format(hangman.secret_word))
        running = False
