import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer


# You may need to download the required NLTK data
nltk.download('wordnet')
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

def is_proper_phrase(phrase, sentence):
    # Tokenize the sentence
    sent_tokens = word_tokenize(sentence)

    # Get the POS tags for the words in the sentence
    pos_tags = pos_tag(sent_tokens)

    # Get the indices of the words in the phrase within the sentence
    phrase_indices = [i for i, word in enumerate(sent_tokens) if word in phrase.split()]

    # Check if the phrase is part of the sentence
    if not phrase_indices:
        return "error", "Noun doesn't exist in the sentence."

    # Check if the first word is a proper noun or if the phrase contains at least one proper noun
    if pos_tags[phrase_indices[0]][1] == "NNP" or any(tag == "NNP" for _, tag in [pos_tags[i] for i in phrase_indices]):
        return "success", True

    return "error", "Noun is common."

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import nltk
from nltk.corpus import wordnet

def analyze_noun_phrase(phrase, sentence):
    result_type, message = is_proper_phrase(phrase, sentence)
    response = {
        "status": result_type,
        "message": message
    }
    return json.dumps(response)

def analyze_last_word(phrase):
    # Get the last word of the sentence
    last_word = phrase.split()[-1]
    
    # Determine if the last word is a proper noun
    is_proper_noun = any(tag.startswith('NNP') for _, tag in nltk.pos_tag([last_word]))
    
    # Get the synsets for the last word
    last_word_synsets = wordnet.synsets(last_word)
    if last_word_synsets:
        last_word_found_in_dictionary = True
        # Get the singular form of the last word
        if last_word_synsets[0].pos() == 'n':
            singular_form = last_word_synsets[0].lemmas()[0].name()
        else:
            singular_form = last_word
    else:
        last_word_found_in_dictionary = False
        # Get the singular form of the last word
        singular_form = nltk.WordNetLemmatizer().lemmatize(last_word, 'n')
        # Get the synsets for the singular form of the last word
        singular_form_synsets = wordnet.synsets(singular_form)
        if singular_form_synsets:
            singular_form_found_in_dictionary = True
        else:
            singular_form_found_in_dictionary = False
    
    # Determine if the original last word was in singular or plural
    is_singular = singular_form == last_word
    
    # Return the results as a dictionary
    return {
        'last_word': last_word,
        'last_word_found_in_dictionary': last_word_found_in_dictionary,
        'singular_form': singular_form,
        'is_proper_noun': is_proper_noun,
        'is_singular': is_singular
    }

def get_dic_info( noun_phrase ):
    result = analyze_last_word( noun_phrase )
    # if last word is a dictionary word, mark it as a dictionary word and mark as checked
    return {    "isDicEntry": result["last_word_found_in_dictionary"],
                "isSingular": result["is_singular"],
                "singular": result["singular_form"]
    }

def get_lemma(word):
    """
    gets the lemma of an action
    """
    pos = "v"  # 'v' represents verb

    lemmatizer = WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word, pos)
    return lemma



if __name__ == "main":
    objs = get_objects()
    for obj in objs[:100]:
        print( analyze_last_word( obj[1]) )
        
if __name__  == "main":
    # Example usage
    phrase = "Elon Musk"
    sentence = "Elon Musk is the CEO of SpaceX and Tesla."
    print(analyze_noun_phrase(phrase, sentence))
    # Output: {"status": "success", "message": true}

    phrase = "Space"
    sentence = "Elon Musk is the CEO of SpaceX and Tesla."
    print(analyze_noun_phrase(phrase, sentence))
    # Output: {"status": "success", "message": true}

    phrase = "chair"
    sentence = "The chair is in the living room."
    print(analyze_noun_phrase(phrase, sentence))
    # Output: {"status": "error", "message": "Noun is common."}

    phrase = "nonexistent"
    sentence = "This noun is not in the sentence."
    print(analyze_noun_phrase(phrase, sentence))
    # Output: {"status": "error", "message": "Noun doesn't exist in the sentence."}

    phrase = "Kennedy"
    sentence = "Kilby killed Kennedy."
    print(analyze_noun_phrase(phrase, sentence))
    # Output: {"status": "error", "message": "Noun doesn't exist in the sentence."}

