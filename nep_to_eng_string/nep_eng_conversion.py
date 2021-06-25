"""
    File name           : nep_eng_conversion
    Author              : siddhi.bajracharya
    Date created        : 2/9/2021
    Date last modified  : 2/9/2021
    Python Version      : 3.6.5
    Description         : 
"""

import codecs, re, optparse, sys
import pandas as pd

# This is a quick python script to transliterate Nepali (Devnagari) to English.
# It uses a lossy transliteration that I defined to do the work, and converts to all Ascii characters (ie, no diacritics), and doesn't use capital / small letters.
# The issue of the schwa (ie, the sometimes implicit a at the end of words (ie, बन्द becomes band or banda? नाम becomes naam or naama?)) is dealt of in the following way:
#     If there is a punctuation or a halanta preceding the consonant, schwa is added (ex: बान्द => banda, म => ma)
#     However, if what precedes is a vowel, then no schwa is added (ex: नाााम => naam, प्रसाद => prasaad)
#     This is not a perfect rule: works well for nouns (see above) but not for verbs (पर्दैन => pardaina)
#     But its the best for right now

def unicodify(strdict):
    """

    changes string to unicode string.
    :param strdict: input string.
    :return: unicode string.
    """
    return dict([(str(x[0], 'utf-8'), str(x[1], 'utf-8')) for x in strdict.items()])


preprocess = {'ज्ञ': 'ग्य', 'ऊँ ': 'ओम् ', '।': '.'}
punctuations = r'.!?,"\')(&@#$%+-_ '
consonants = {'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ng', 'च': 'ch', 'छ': 'chh', 'ज': 'j', 'झ': 'jh', 'ञ': 'yn',
     'ट': 't', 'ठ': 'th', 'ड': 'd', 'ढ': 'dh', 'ण': 'n', 'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n', 'प': 'p',
     'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm', 'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v', 'श': 'sh', 'ष': 's', 'स': 's',
     'ह': 'h', 'श्र': 'shr'}
vowels = {'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo', 'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au', 'ऋ': '.r',
     'ॠ': '.rr', 'ऌ': '.l', 'ॡ': '.ll', 'अं': 'am', 'ँ': '(n)',
     'ं': '(m)'}  # अं and अँ are here because if they are not like ikars/ukars, ie, don't erase the "अ" at the end of consonants
akar_ukar = {'ा': 'aa', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo', 'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', 'ृ': 'ri',
     '्': ''}  # note the last two items (् halanta and  space): they are hacks to take out the a after the consonants. Also, ि has a special rule; see code below


def multiple_replace(dictionary, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dictionary.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dictionary[mo.string[mo.start():mo.end()]], text)


def transliterate(string):
    """
    Transliterates the string.
    :param string: Nepali String to transliterate.
    :return: English script string.
    """
    if string is None:
        return None
    string += ' '
    if isinstance(string, str) and not isinstance(string, str): string = string.encode(
        "utf-8")  # make sure we have unicode
    ret = ''
    or_list = []
    translate_list = []
    string = multiple_replace(preprocess, string)
    for i, v in enumerate(string):
        or_list.append(v)

        # akars, ukars and vowels are simple: you just transliterate based on the table.
        if v in akar_ukar :
            ret = ret + akar_ukar[v]
            translate_list.append(akar_ukar[v])
        elif v in vowels :
            ret = ret + vowels[v]
            translate_list.append(vowels[v])
        # Consonants are tricky (क is ka or just k depending on what follows).
        elif v in consonants :
            # If the consonant is followed by an akar or an ukar things are simple (see else)
            if i < len(string) and string[i + 1] in akar_ukar:
                ret = ret + consonants.get(v, v)
                translate_list.append(consonants.get(v, v))
            # If not, we have to check whether the consonant is at a word's end, and go into schwa rules
            else:
                if i == len(string) or string[i + 1] in punctuations:  # if its a schwa
                    # Schwa rule:
                    if i > 0 and (string[i - 1] == u'्' or string[
                        i - 1] in punctuations):  # if preceding char is halanta or a punctuation
                        ret = ret + consonants.get(v, v) + 'a'
                        translate_list.append(consonants.get(v, v)+ 'a')
                    else:
                        ret = ret + consonants.get(v, v)
                        translate_list.append(consonants.get(v, v))
                else:  # no schwa and no akar. means we have an अ following the consonant
                    ret = ret + consonants.get(v, v) + 'a'
                    translate_list.append(consonants.get(v, v)+'a')
        else:
            ret = ret + v
    return ret


def convert_digits(s):
    """
    Converts nepali digit to english.
    :param s: Digits in nepali.
    :return: Digits in english.
    """
    return s.replace("०","0").\
        replace("१", "1").\
        replace("२", "2", ).\
        replace("३", "3",).\
        replace("४", "4",).\
        replace("५", "5",).\
        replace("६", "6",).\
        replace("७", "7",).\
        replace("८", "8",).\
        replace("९", "9",)