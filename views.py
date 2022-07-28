from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import re
import string
import os.path
from num2words import *

from datetime import datetime

from .models import Conversions



# diplaying interface
def home(request):
    return render(request, 'index.html')




exotic_punctuation = ["“", "”", "’", "‘", "—"]
basic_punctuation = "!?.,:'\""

@csrf_exempt
def convert_user_text(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']


    global some_result
    for c in string.punctuation:  # this removes punctuation
        user_text = user_text.replace(c, "")
    for c in exotic_punctuation:
        user_text = user_text.replace(c, "")  # this removes more exotic punctuation
    user_text = user_text.lower()
    data = user_text.split()
    for word in data:  # dealing with dashes
        word_index = data.index(word)
        if word == "xx":
            data[word_index] = ""
        elif "--" in word:
            double_dash_index = 0
            first_word = ""
            second_word = ""
            for c in basic_punctuation:
                word = word.replace(c, "")
            for letter in word:  # getting the index of the first dash
                if letter == "-":
                    break
                else:
                    double_dash_index += 1
            first_word = word[
                         :double_dash_index]  # below an attempt to remove double dashes and obtain words which are separeted by them
            second_word = word[double_dash_index + 2:]
            if first_word.isalpha() and second_word.isalpha():
                data[word_index:word_index + 1] = first_word, second_word
            elif first_word.isalpha():
                data[word_index] = first_word
            elif second_word.isalpha():
                data[word_index] = second_word
            else:
                word = word.replace("-", "")
                data[word_index] = word

    data = " ".join(
        data)  # going back to string for a moment - "the initial situation" - we need to remove all the puntuation now

    for c in string.punctuation:  # this removes punctuation
        data = data.replace(c, "")
    for c in exotic_punctuation:
        data = data.replace(c, "")  # this removes more exotic punctuation

    data = data.split()

    for word in data:  # dealing with numbers
        word_index = data.index(word)
        if word.isalpha():  # normal words - just pass
            pass
        elif word.isnumeric():  # numers - tranfromed into word numbers
            word_index = data.index(word)
            number_as_word = num2words(int(word))
            for c in string.punctuation:
                number_as_word = number_as_word.replace(c, "")
            data[word_index] = number_as_word
        else:  # complex cases - half-word half-number

            first_digit_index = 0  # obtaining the word version of the number
            for letter in word:
                if letter.isnumeric():
                    break
                else:
                    first_digit_index += 1

            remaining_numbers = ""
            index_counter_for_numbers = 0
            for letter in word[first_digit_index:]:
                if letter.isnumeric():
                    remaining_numbers += word[first_digit_index + index_counter_for_numbers]
                    index_counter_for_numbers += 1
            first_letter_index = 0
            for letter in word:
                if letter.isalpha():
                    break
                else:
                    first_letter_index += 1

            remaining_letters = ""  # gathering remaining letters into a separate word
            index_counter = 0
            for letter in word[first_letter_index:]:
                if letter.isalpha():
                    remaining_letters += word[first_letter_index + index_counter]
                    index_counter += 1

            if remaining_letters == "th" or remaining_letters == "st" or remaining_letters == "nd" or remaining_letters == "rd":  # dealing with ordinal numbers
                data[word_index] = num2words(int(remaining_numbers), ordinal=True)

            else:  # final addition of a word as a number and the remaining letters as a separate word
                number_as_word = num2words(int(remaining_numbers))
                for c in string.punctuation:
                    number_as_word = number_as_word.replace(c, "")
                data[word_index:word_index + 1] = number_as_word, remaining_letters

    converted_file_name = datetime.now().strftime('%Y_%m_%d %H_%M_%S_%f') + '.cha'

    converted_file = open('media/' + converted_file_name, 'w')
    converted_file.write("@Font:	Times New Roman\n"),
    converted_file.write("@Begin\n")
    converted_file.write("@Languages:	eng\n")
    converted_file.write("@Participants:	AUT Name Text\n")
    converted_file.write("@ID:	eng|change_me_later|AUT|||||Text|||\n")
    for word in data:
        for letter in word:
            if letter == int:
                pass
        else:
            converted_file.write("*AUT:	" + word + ".\n")
    converted_file.write("@End")

    response_data = {'result': converted_file_name}
    conversion = Conversions(text_sample = user_text[:100], text_length = len(data))
    conversion.save()
    return JsonResponse(response_data)
