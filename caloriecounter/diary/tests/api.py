from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from caloriecounter.diary.models import DiaryEntry
from caloriecounter.diary.tests import DiaryEntryBaseTest


class DiaryEntryViewSetTestCase(DiaryEntryBaseTest):
    """
    A TestCase that performs tests on the DiaryEntryViewSet in the api package of the diary app.
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()

        self.user_client = APIClient()
        self.user_client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)

        self.user_client_2 = APIClient()
        self.user_client_2.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token_2.key)

    def test_diary_entry_list_not_logged_in(self):
        """
        Assert:
        1. The diary_entry-list view returns 403 (Not authenticated) fo the diary_entry_list
        when no authentication is provided.
        """
        url = reverse("diary_entry-list")
        response = self.client.get(url)

        # Assert 1.
        self.assertEqual(response.status_code, 401)

    def test_diary_entry_item_not_logged_in(self):
        """
        Assert:
        1. The diary_entry-detail view returns 403 (Not authenticated) fo the diary_entry_list
        when no authentication is provided.
        """
        url = reverse("diary_entry-detail", kwargs={'pk': self.diary_entry.pk})
        response = self.client.get(url)

        # Assert 1.
        self.assertEqual(response.status_code, 401)

    def test_diary_entry_create_not_logged_in(self):
        """
        Assert:
        1. The diary_entry-create view returns 403 (Not authenticated) fo the diary_entry_list
        when no authentication is provided.
        """
        url = reverse("diary_entry-list")
        response = self.client.post(url, {'name': 'Mushrooms'})

        # Assert 1.
        self.assertEqual(response.status_code, 401)

    def test_diary_entry_update_not_logged_in(self):
        """
        Assert:
        1. The diary_entry-detail view returns a 403 (Method not allowed) status code for a full update.
        2. The diary_entry-detail view returns a 403 (Method not allowed) status code for a partial update.
        3. The diary_entry-list view returns a 403 (Method not allowed) status code for a full update.
        4. The diary_entry-list view returns a 403 (Method not allowed) status code for a partial update.
        """
        url = reverse("diary_entry-detail", kwargs={'pk': self.diary_entry.pk})
        response = self.client.patch(url, {'name': 'Liter'})

        # Assert 1.
        self.assertEqual(response.status_code, 401)

        response = self.client.patch(url, {'name': 'Liter'})

        # Assert 2.
        self.assertEqual(response.status_code, 401)

        # Assert 3.
        url = reverse("diary_entry-list")
        response = self.client.put(url, {'pk': self.diary_entry.pk, 'name': 'Mushrooms'})
        self.assertEqual(response.status_code, 401)

        # Assert 4.
        url = reverse("diary_entry-list")
        response = self.client.patch(url, {'pk': self.diary_entry.pk, 'name': 'Mushrooms'})
        self.assertEqual(response.status_code, 401)

    def test_diary_entry_delete_not_logged_in(self):
        """
        Assert:
        1. The diary_entry-delete view returns a 405 (Method not allowed) status code.
        """
        url = reverse("diary_entry-detail", kwargs={'pk': self.diary_entry.pk})
        response = self.client.delete(url)

        # Assert 1.
        self.assertEqual(response.status_code, 401)

    def test_diary_entry_list(self):
        """
        Assert:
        1. A logged in user can list their own (and only their own) DiaryEntries
        2. The DiaryEntries are correct and in the correct order.
        """
        url = reverse("diary_entry-list")
        response = self.user_client.get(url)

        # Assert 1.
        self.assertEqual(response.data['count'], 2)

        # Assert 2.
        self.assertEqual(response.data['results'][0]['pk'], self.diary_entry.pk)
        self.assertEqual(response.data['results'][1]['pk'], self.diary_entry_2.pk)

    def test_diary_entry_item(self):
        """
        Assert:
        1. Only the user who owns a DiaryEntry can retrieve it using the diary_entry-detail view
        2. All fields on the returned DiaryEntry are present and correct
        """

        # Assert 1.
        url = reverse("diary_entry-detail", kwargs={'pk': self.diary_entry.pk})
        response = self.user_client_2.get(url)

        self.assertEqual(response.status_code, 404)

        url = reverse("diary_entry-detail", kwargs={'pk': self.diary_entry.pk})
        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)

        # Assert 2.
        dict = response.data
        self.assertIn('pk', dict)
        self.assertEqual(self.diary_entry.pk, dict['pk'])

        self.assertIn('date', dict)
        self.assertEqual(str(self.diary_entry.date), dict['date'])

        self.assertIn('time', dict)
        self.assertEqual(str(self.diary_entry.time), dict['time'])

        self.assertIn('product', dict)
        self.assertEqual(self.diary_entry.product.pk, dict['product'])

        self.assertIn('quantity', dict)
        self.assertEqual(self.diary_entry.quantity, dict['quantity'])

        self.assertIn('unit', dict)
        self.assertEqual(self.diary_entry.unit.pk, dict['unit'])

        self.assertIn('nutritional_information', dict)
        self.assertEqual(self.diary_entry.nutritional_information[0][0], dict['nutritional_information'][0]['quantity'])
        self.assertEqual(self.diary_entry.nutritional_information[0][1].pk, dict['nutritional_information'][0]['nutrient'])
        self.assertEqual(self.diary_entry.nutritional_information[1][0], dict['nutritional_information'][1]['quantity'])
        self.assertEqual(self.diary_entry.nutritional_information[1][1].pk, dict['nutritional_information'][1]['nutrient'])

    def test_diary_entry_create(self):
        """
        Assert:
        1. A logged in user can create a DiaryEntry.
        """
        url = reverse("diary_entry-list")

        # Assert 1.
        response = self.user_client.post(url,
        {
            'date': '2019-03-03',
            'time': '08:00',
            'product': self.product.pk,
            'quantity': 0.02,
            'unit': self.kg.pk
        }, format='json')

        self.assertEqual(response.status_code, 201)
        DiaryEntry.objects.get(pk = response.data['pk'])

    def test_diary_entry_create_missing_data(self):
        """
        Assert:
        1. A 400 error (Bad request) is returned when data is missing (Testing the default validators behaviour).
        """
        url = reverse("diary_entry-list")
        response = self.user_client.post(url, {
            'date': '2019-03-03',
            'time': '08:00',
            'product': None,
            'quantity': 0.02,
            'unit': self.kg.pk

        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('product', response.data)

    def test_diary_entry_create_missing_unit_no_default_quantity(self):
        """
        Assert:
        1. A 400 error (Bad request) is returned when a unit is missing, and the product has no default quantity.
        """
        url = reverse("diary_entry-list")
        response = self.user_client.post(url, {
            'date': '2019-03-03',
            'time': '08:00',
            'product': self.product_no_default_quantity.pk,
            'quantity': 0.02,
        }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('product', response.data)

    def test_diary_entry_create_incompatible_unit(self):
        """
        Assert:
        1. A 400 error (Bad request) is returned when an incompatible unit is passed.
        """
        url = reverse("diary_entry-list")
        response = self.user_client.post(url,
                                         {
                                             'date': '2019-03-03',
                                             'time': '08:00',
                                             'product': self.product.pk,
                                             'quantity': 0.02,
                                             'unit': self.handful.pk
                                         }, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('unit', response.data)

    def test_diary_entry_update(self):
        """
        Assert:
        1. Only the user who owns a DiaryEntry can update it using the diary_entry-detail view.
        2. The updated fields on the DiaryEntry are present and correct.
        """
        # Assert 1.
        pk = self.diary_entry.pk
        url = reverse("diary_entry-detail", kwargs={'pk': pk})
        response = self.user_client_2.patch(url, {'quantity' : 10}, format='json')
        self.assertEqual(response.status_code, 404)

        url = reverse("diary_entry-detail", kwargs={'pk': pk})
        response = self.user_client.patch(url, {'quantity' : 20}, format='json')
        self.assertEqual(response.status_code, 200)

        # Assert 2.
        diary_entry = DiaryEntry.objects.get(pk=pk)
        self.assertEqual(diary_entry.quantity, 20)

    def test_diary_entry_delete(self):
        """
        Assert:
        1. Only the user who owns a DiaryEntry can delete it using the diary_entry-detail view.
        2. The DiaryEntry is actually deleted.
        """

        # Assert 1.
        pk = self.diary_entry.pk
        url = reverse("diary_entry-detail", kwargs={'pk': pk})
        response = self.user_client_2.delete(url)
        self.assertEqual(response.status_code, 404)

        url = reverse("diary_entry-detail", kwargs={'pk': pk})
        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, 204)

        # Assert 2.
        with self.assertRaises(DiaryEntry.DoesNotExist):
            diary_entry = DiaryEntry.objects.get(pk=pk)
