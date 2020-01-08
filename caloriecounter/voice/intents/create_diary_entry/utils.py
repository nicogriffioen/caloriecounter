from operator import itemgetter

from django.conf import settings
from spacy.matcher import Matcher

nlp = settings.LANGUAGE_MODELS['en']


def get_unique_matches_for_food_and_quantities(doc):
    matcher = Matcher(nlp.vocab)
    # Add match ID "HelloWorld" with no callback and one pattern
    # pattern = [{"LOWER": "is"}, {"OP": "*", "IS_PUNCT": False}, {"LOWER": "example"}]
    patterns = []

    # 2 grams of chicken breast or 2 hamburgers from McDonalds
    patterns.append([{"POS": "NUM"}, {"OP": "*", "POS": "ADJ"}, {"OP": "+", "POS": "NOUN"}, {"OP": "?", "POS": "ADP"},
                     {"OP": "*", "POS": "ADJ"}, {"OP": "*", "POS": "NOUN"}])

    # A slice of bread
    patterns.append(
        [{"POS": "DET", "OP": "?"}, {"OP": "*", "POS": "ADJ"}, {"OP": "+", "POS": "NOUN"}, {"OP": "?", "POS": "ADP"},
         {"OP": "*", "POS": "ADJ"}, {"OP": "*", "POS": "NOUN"}])

    # A raw broccoli stalk
    # patterns.append([{"POS": "DET"}, {"OP" : "?", "POS": "ADJ"}, {"OP" : "+", "POS": "NOUN"}])

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

    unit_of_items = span[1] if span[1].ent_type_ == "QUANTITY" else None

    unit_modifier = []

    if unit_of_items is None:
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
                unit_modifier.append(str(span[i - 1]))
            i = i + 1

    unit_modifier = ' '.join(unit_modifier)

    item_name = ' '.join([token.lemma_ for token in span if token.pos_ == "NOUN" and token.ent_type_ != "QUANTITY"])

    item_modifier = ' '.join([token.lemma_ for token in span if token.pos_ == "ADJ" and token.ent_type_ != "QUANTITY"])

    return {
        'quantity': str(number_of_items),
        'unit': str(unit_of_items),
        'unit_extra': str(unit_modifier),
        'name': str(item_name),
        'extra': str(item_modifier),
    }