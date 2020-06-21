import caloriecounter.voice.utils as utils
from .models import VoiceSession, VoiceSessionItem

from django.conf import settings

nlp = settings.LANGUAGE_MODELS['en']


def process_session(session : VoiceSession):

    try:
        # Get last item from VoiceSession, this is the users last query.
        last_item = session.items.last()
        text = last_item.text
        doc = nlp(text)

        # Extract the intent from the text, and perform the action that is linked to this intent.
        intent = utils.get_probable_intent(doc)

        items = intent.perform(doc, session)

        # Save all voice session items from the conversation.
        for item in items:
            item.save()

        # Return the updated session.
        return session

    except Exception as e:
        VoiceSessionItem(text="Uh oh! Something went wrong. Could you try that again?",
                         session=session,
                         type='feedback',
                         user_created=False,
                         data={
                             'exception': str(e)
                         }).save()

        raise e

