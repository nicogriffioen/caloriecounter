from datetime import time, date, datetime

from django.contrib.postgres.search import SearchVector, TrigramDistance
from django.db.models import Q

from caloriecounter.diary.api.serializers import DiaryEntrySerializer
from caloriecounter.diary.models import DiaryEntry
from caloriecounter.food.models import FoodProduct, Unit, FoodProductSearchCacheItem
from caloriecounter.voice.models import VoiceSessionItem, VoiceSession

from . import utils


def perform(doc, session : VoiceSession):
    items = []

    matches = utils.get_unique_matches_for_food_and_quantities(doc)

    food_items = []
    for match_id, start, end in matches:
        food_items.append(utils.get_food_item_in_span(doc[start:end]))

    items.append(
        VoiceSessionItem(text="Got it!",
                         session=session,
                         type='feedback',
                         user_created=False,
                         data=None)
    )

    diary_entries = []

    for food_item in food_items:
        diary_entries.append(get_diary_entry(food_item, session))

    for diary_entry in diary_entries:
        diary_entry.save()

    items.append(
        VoiceSessionItem(text=None,
                         session=session,
                         type='objects_created',
                         user_created=False,
                         data=[DiaryEntrySerializer().to_representation(diary_entry)
                               for diary_entry
                               in diary_entries])
    )

    return items


def get_diary_entry(food_item, session : VoiceSession):
    # return {
    #     'quantity': str(number_of_items),
    #     'unit': str(unit_of_items),
    #     'unit_extra': str(unit_modifier),
    #     'name': str(item_name),
    #     'extra': str(item_modifier),
    # }

    # Try to get aproduct in a few different ways:
    # 1. Find the product in the FoodProductSearchCache (High probability of matching a common food.)
    # 2. Find the product in the sr_legacy_food and survey_fndds_food group.
    # 3. Find the product in all FoodProducts.

    quantity = float(food_item.get('quantity'))

    unit = Unit.objects.annotate(search=SearchVector('name', '_name_plural', 'short_name'))\
        .filter(search=food_item.get('unit'))\
        .first()

    # 1.

    try:
        search_cache_item = FoodProductSearchCacheItem.objects.get(text__iexact= food_item.get('name'))
        product = search_cache_item.food_product
    except FoodProductSearchCacheItem.DoesNotExist:
        search_cache_item = None

    if not search_cache_item:
        try:
            search_cache_item = FoodProductSearchCacheItem.objects\
                .get(text__iexact='{0} {1}'.format(food_item.get('extra'), food_item.get('name')))
            product = search_cache_item.food_product
        except FoodProductSearchCacheItem.DoesNotExist:
            search_cache_item = None

    # 2.
    product = FoodProduct.objects.annotate(
        distance = TrigramDistance('full_name', '{0} {1}'
                                   .format(food_item.get('name'), food_item.get('extra'))))\
        .filter(Q(food_source='sr_legacy_food') | Q(food_source='survey_fndds_food'))\
        .filter(full_name__istartswith = food_item.get('name')) \
        .filter(distance__lte=0.7)\
        .order_by('distance').first()

    diary_entry = DiaryEntry(user=session.user,
                             product=product,
                             quantity= quantity,
                             unit = unit,
                             date=datetime.now(),
                             time=datetime.now())

    diary_entry.full_clean()
    return diary_entry
