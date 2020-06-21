import json
from unittest import TestCase

from django.conf import settings

from rest_framework.reverse import reverse

from caloriecounter.voice.intents.create_diary_entry import utils


class CreateDiaryEntryIntentTest(TestCase):
    """
    A TestCase that performs tests on the create_diary_entry intent.
    """

    def test_command_parsing(self):
        """
        Assert:
        1. For each command in the provided JSON file, the automatically extracted data matches the hand-curated data.
        """

        nlp = settings.LANGUAGE_MODELS['en']

        errors = []

        with open('fixtures/create_diary_entry_commands.json') as json_file:
            commands = json.load(json_file)['commands']
            for command in commands:
                try:
                    doc = nlp(command['text'])

                    matches = utils.get_unique_matches_for_food_and_quantities(doc)
                    for match_id, start, end in matches:
                        print(doc[start:end])
                    if len(matches) != len(command['results']):
                        print('Error parsing command:', command['text'], '- expected {0} results, got {1}'
                              .format(len(command['results']), len(matches)))
                        errors.append(command['text'])
                        continue

                    food_items = []
                    for match_id, start, end in matches:
                        result = utils.get_food_item_in_span(doc[start:end])
                        expected_result = command['results'].pop(0)
                        if result != expected_result:
                            errors.append(command['text'])
                            print('Error parsing command:', command['text'], '-', result, 'does not match', expected_result)
                except Exception as e:
                    print('Error parsing command', command['text'], '-', str(e))
                    raise e

        self.assertEqual(errors, [])




