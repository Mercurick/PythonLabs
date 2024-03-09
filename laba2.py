import re

digit_to_word = {
    '0': 'ноль',
    '1': 'один',
    '2': 'два',
    '3': 'три',
    '4': 'четыре',
    '5': 'пять',
    '6': 'шесть',
    '7': 'семь',
    '8': 'восемь',
    '9': 'девять'
}

file_path = "text.txt"

def number_to_words(number):
    return ' '.join(digit_to_word[digit] for digit in str(number))

def has_repeating_digits(number):
    repeating_digits = set()
    for digit in str(number):
        if str(number).count(digit) > 1:
            repeating_digits.add(digit)
    return repeating_digits

try:
    with open(file_path, "r") as file:
        block_size = 1024

        block = file.read(block_size)

        while block:
            numbers = [int(num) for num in re.findall(r'-?\b\d+\b', block)]

            for num in numbers:
                repeating_digits = has_repeating_digits(num)
                if repeating_digits:
                    print(' '.join(number_to_words(d) for d in repeating_digits))

            block = file.read(block_size)

except ValueError:
    print("Ошибка: Файл содержит некорректные данные. Очистите файл text.txt.")
    exit()