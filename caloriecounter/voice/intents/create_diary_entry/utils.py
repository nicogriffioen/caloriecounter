from operator import itemgetter

from django.conf import settings
from spacy.matcher import Matcher

nlp = settings.LANGUAGE_MODELS['en']


def get_unique_matches_for_food_and_quantities(doc):
    for chunk in doc.noun_chunks:
        print(chunk)
    matcher = Matcher(nlp.vocab)

    patterns = []
    # 2 grams of chicken breast or 2 hamburgers from McDonalds
    patterns.append([{"POS": "NUM"}, {"OP": "*", "POS": "ADJ"}, {"OP": "+", "POS": {"IN": ["NOUN", "PROPN"]}}, {"OP": "?", "POS": "ADP"},
                     {"OP": "*", "POS": "ADJ"}, {"OP": "*", "POS": {"IN": ["NOUN", "PROPN"]}}])

    # A slice of bread
    patterns.append(
        [{"POS": "DET", "OP": "?"}, {"OP": "*", "POS": "ADJ"}, {"OP": "+", "POS": {"IN": ["NOUN", "PROPN"]}}, {"OP": "?", "POS": "ADP"},
         {"OP": "*", "POS": "ADJ"}, {"OP": "*", "POS": {"IN": ["NOUN", "PROPN"]}}])

    # A raw broccoli stalk
    patterns.append([{"POS": "DET"}, {"OP": "*", "POS": "ADJ"}, {"OP": "+", "POS": {"IN": ["NOUN", "PROPN"]}}])

    matcher.add("quantities-of-food", None, *patterns)

    matches = matcher(doc)
    matches.sort(key=itemgetter(2), reverse=True)
    matches.sort(key=itemgetter(1))

    old_start = -1
    old_end = -1

    new_matches = []

    for match_id, start, end in matches:
        if start >= old_start and end <= old_end:
            continue
        old_start = start
        old_end = end
        new_matches.append((match_id, start, end))

    return new_matches


def get_food_item_in_span(span):
    number_of_items = ' '.join([str(token) for token in span if token.pos_ == "NUM"])

    unit_of_items = ''

    if len(span) > 1:
        unit_of_items = span[1] if span[1].ent_type_ == "QUANTITY" else ''

    unit_modifiers = []

    if unit_of_items is '':
        if len(span) > 2 and str(span[1]) in ['g', 'ml']:
            span[1].ent_type_ = "QUANTITY"
            unit_of_items = span[1]

        i = 2
        while i < len(span):
            if span[i].pos_ == "ADP":
                span[i - 1].ent_type_ = "QUANTITY"
                unit_of_items = span[i - 1]
                break
            else:
                unit_modifiers.append(span[i - 1])
            i = i + 1

    item_names = [token for token in span if (token.pos_ == "NOUN" or token.pos_ == "PROPN") and token.ent_type_ != "QUANTITY"]

    item_modifier = ' '.join([token.lemma_ for token in span if token not in unit_modifiers and token not in item_names and token.pos_ == "ADJ" and token.ent_type_ != "QUANTITY"])

    unit_modifier = ' '.join(str(x) for x in unit_modifiers if x not in item_names and str(x) != str(unit_of_items))

    item_name = ' '.join(token.lemma_ for token in item_names)

    # if unit_of_items is None:
    #    unit_of_items = ''

    return {
        'quantity': str(number_of_items),
        'unit': str(unit_of_items),
        'unit_extra': str(unit_modifier),
        'name': str(item_name),
        'extra': str(item_modifier),
        'raw': str(span)
    }
