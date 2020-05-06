import sys
from random import random
from phraselist import phrases_original
from character import Character
from phrase import Phrase


class Game:
    """Game takes the components of the Character and Phrase classes and runs through the steps of the guessing game.
    it also contains a function to reset the game to play again"""

    def __init__(self, phrases):
        self.phrases = [Phrase(phrase) for phrase in phrases]
        self.number_of_tries = 5

    def begin_game(self):
        selected_phrase = random.choice(self.phrases)
        heading = f"""
                {'~' * 41}
                {'<' * 9} PHRASE GUESSING GAME! {'>' * 9}
                {'~' * 41}
                """
        print(heading)
        see_instructions = input("enter 'i' for instructions or press enter to continue").lower()

        instructions = ("\n"
                        "Your job is to guess the phrase\n"
                        "You will be shown the length of the phrase with the letters hidden\n"
                        "Guess a letter: If your letter is in the phrase, you will be shown all the places that your "
                        "letter appears\n "
                        "               If your letter is not in the phrase, you will be given a strike\n"
                        "                If you guess the phrase incorrectly, you will be given a strike\n"
                        "                If you wish to guess the phrase, enter solve\n"
                        "                If your guessed phrase is incorrect, you will be given a strike\n"
                        "Guess the phrase correctly before you receive 5 strikes.  \n"
                        "If you do, You win!\n"
                        "if you don't, You're a loser!\n")

        if see_instructions == 'i':
            print(instructions)
            input("Press Enter to continue")
            self.letter_guesser()
        else:
            self.letter_guesser()

    def letter_guesser(self):

        while True:

            print(f"""
                    Your phrase is:
                    {loop_phrase.capitalize()} 
                    Strikes: {'X' * self.number_of_tries}
                    Guessed Letters: {', '.join(Character.incorrect_characters).upper()}
                    """)

            letter_guessed = input('Guess a letter:  ')

            if letter_guessed.lower() == "SOLVE".lower():
                answer = Phrase(self.phrase).phrase_guesser()
                if answer:
                    self.play_again()
                else:
                    self.number_of_tries -= 1
                    continue
            try:
                Character(letter_guessed).validate_input()
            except ValueError as err:
                print(err)
                continue

            else:
                character_indices = Character(letter_guessed).search_phrase(self.phrase)

            if not character_indices:
                Character(letter_guessed).incorrect_characters_append()
                self.number_of_tries -= 1
                if self.number_of_tries == 0:
                    print("You're a loser")
                    self.play_again()
                else:
                    print('Sorry, there is no {}'.format(letter_guessed.upper()))

            elif character_indices:
                Character(letter_guessed).correct_characters_append()
                print("Yes, {} is in your phrase".format(letter_guessed.upper()))
                loop_phrase = Character(letter_guessed).replace_character(loop_phrase, character_indices)
                if Phrase(self.phrase).phrase_match(loop_phrase):
                    print('{} is correct'.format(loop_phrase.capitalize()))
                    self.play_again()

    def play_again(self):
        while True:

            again = input('Would you like to play again? [y]es or [n]o.    ').lower()
            if again == ('NO'.lower()) or again == ('N'.lower()):
                sys.exit('Good day')

            elif again == ('YES'.lower()) or again == ('Y'.lower()):
                self.reset()

            else:
                print('that is not a valid entry')

    @staticmethod
    def reset():
        Character.incorrect_characters = []
        Character.correct_characters = []
        new_game = Game(phrases_original)
        return new_game.begin_game()
