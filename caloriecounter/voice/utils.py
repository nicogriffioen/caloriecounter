from operator import itemgetter
import functools

from spacy.matcher import Matcher

from django.conf import settings

nlp = settings.LANGUAGE_MODELS['en']


def get_matches_for_subject_and_main_verb(doc):
    matcher = Matcher(nlp.vocab)
    # Add match ID "HelloWorld" with no callback and one pattern
    patterns = []
    # patterns.append([{"POS": "PRON"}, {"IS_STOP" : True, "OP" : "?"} ,{"POS": "VERB"}])
    patterns.append([{"POS": "VERB"}])
    matcher.add("i-ate", None, *patterns)
    return matcher(doc)


def get_probable_intent(doc):
    from caloriecounter.voice.intents import create_diary_entry

    list_of_spans = get_matches_for_subject_and_main_verb(doc)

    if len(list_of_spans) == 0:
        return create_diary_entry
    intents = {
        create_diary_entry : ['ate', 'log', 'register', 'write'],
        #'query': ['are', 'is'],
        #'recommend': ['should', 'recommend', 'can', 'eat', 'could'],
    }

    new_dict = {}

    for (key, value) in intents.items():
        for span_id, start, end in list_of_spans:
            similarities = [0]
            for token in filter(lambda x: x.pos_ == "VERB", doc[start:end]):
                max_similarity = 0
                for comparison_token_str in value:
                    comparison_token = nlp(comparison_token_str)[0]
                    similarity = token.similarity(comparison_token)
                    max_similarity = max(similarity, max_similarity)
                similarities.append(max_similarity)

        new_dict[key] = functools.reduce(lambda x, y: x * y, similarities, 1)

    return max(new_dict.items(), key=itemgetter(1))[0]