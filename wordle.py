import json
import random

import requests


class Wordle:
    def __init__(self, key):
        self.key = key
        self.dashboard = [
            ['-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-'],
        ]
        self.word_length = 5

    def valid_dict_word(self, word):
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        if response.status_code != 200:
            return False
        return True

    def validate_word(self, word):
        if len(word) < 5:
            return "Word Length Too Short, Please Enter Again", False
        if len(word) > 5:
            return "Word Length Too High,  Please Enter Again", False
        is_valid_word = self.valid_dict_word(word)
        if not is_valid_word:
            return 'Not A Valid Word,  Please Enter Again', False
        return "Valid Word", True

    def compare(self, input_word, index):
        '''
            () means at correct place
            [] means at incorrect place
            ^^ means does not exists
        '''
        key_array = [char.lower() for char in self.key]
        input_word_array = [char.lower() for char in input_word]
        if key_array == input_word_array:
            return True

        for i, char in enumerate(input_word_array):
            if char in key_array:
                if key_array.index(char) == input_word_array.index(char):
                    input_word_array[i] = f"({char})"
                else:
                    input_word_array[i] = f"[{char}]"
            else:
                input_word_array[i] = f"^{char}^"
        self.dashboard[index] = input_word_array
        return False

    def play(self):
        print(self.dashboard)
        current_index = 0
        while current_index < 5:
            word = input("Enter Your Word  : ")
            message, is_valid_word = self.validate_word(word)
            if not is_valid_word:
                print(f"{message} - {word}")
            else:
                result = self.compare(word, current_index)
                if result:
                    return "VOILA, YOU WIN THE GAME"
                current_index += 1
            print(self.dashboard)
            print(f"Chances Left : {5 - current_index}")
            print("\n")
            print('-----------------------------------------------------------')
            print("\n")
        return f"The Word is {self.key}, Better Luck Next time"


if __name__ == "__main__":
    with open('words.json', 'r') as outf:
        words_json = json.load(outf)
    words_chart_5 = words_json['5']
    random_index = random.randint(0, len(words_chart_5) - 1)
    key = words_chart_5[random_index]
    print(key, "--Answer")
    wordle = Wordle(key)
    res = wordle.play()
    print(res)
