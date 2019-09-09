from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from caloriecounter.food.tests import BaseTest


# Since at the time most of the logic is handled by Django and DRF,
# we only run integration testing by calling requests on the views.
# Right now, these tests ensure that the configuration of the DRF viewsets and their serializers is correct.

class FoodProductViewSetTestCase(BaseTest):
    """
    A TestCase that performs tests on the foodproductViewSet in the api package of the food app.
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_foodproduct_list(self):
        """
        Assert:
        1. The foodproduct-list view can be called without authentication.
        2. The foodproduct-list view contains the correct number items.
        """
        url = reverse("foodproduct-list")
        response = self.client.get(url)

        # Assert 1.
        self.assertEqual(response.status_code, 200)

        # Assert 2.
        self.assertEqual(response.data['count'], 4)

    def test_foodproduct_item(self):
        """
        Assert:
        1. The foodproduct-detail view can be called without authentication.
        2. The foodproduct-detail_view returns the correct number items.
        """
        url = reverse("foodproduct-detail", kwargs={'pk': self.product.pk})
        response = self.client.get(url)

        # Assert 1.
        self.assertEqual(response.status_code, 200)

        # Assert 2.
        self.assertEqual(response.data['pk'], self.product.pk)

    def test_foodproduct_create_not_allowed(self):
        """
        Assert:
        1. The foodproduct-create view returns a 405 (Method not allowed) status code.
        """
        url = reverse("foodproduct-list")
        response = self.client.post(url, {'name': 'Mushrooms'})

        # Assert 1.
        self.assertEqual(response.status_code, 405)

    def test_foodproduct_update_not_allowed(self):
        """
        Assert:
        1. The foodproduct-detail view returns a 405 (Method not allowed) status code for a full update.
        2. The foodproduct-detail view returns a 405 (Method not allowed) status code for a partial update.
        3. The foodproduct-list view returns a 405 (Method not allowed) status code for a full update.
        4. The foodproduct-list view returns a 405 (Method not allowed) status code for a partial update.
        """
        url = reverse("foodproduct-detail", kwargs={'pk': self.product.pk})
        response = self.client.patch(url, {'name': 'Liter'})

        # Assert 1.
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(url, {'name': 'Mushrooms'})

        # Assert 2.
        self.assertEqual(response.status_code, 405)

        # Assert 3.
        url = reverse("foodproduct-list")
        response = self.client.put(url, {'pk': self.product.pk, 'name': 'Mushrooms'})
        self.assertEqual(response.status_code, 405)

        # Assert 4.
        url = reverse("foodproduct-list")
        response = self.client.patch(url, {'pk': self.product.pk, 'name': 'Mushrooms'})
        self.assertEqual(response.status_code, 405)

    def test_foodproduct_delete_not_allowed(self):
        """
        Assert:
        1. The foodproduct-delete view returns a 405 (Method not allowed) status code.
        """
        url = reverse("foodproduct-detail", kwargs={'pk': self.product.pk})
        response = self.client.delete(url)

        # Assert 1.
        self.assertEqual(response.status_code, 405)


class NutrientViewSetTestCase(BaseTest):
    """
    A TestCase that performs tests on the nutrientViewSet in the api package of the food app.
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_nutrient_list(self):
        """
        Assert:
        1. The nutrient-list view can be called without authentication.
        2. The nutrient-list view contains the correct number items.
        """
        url = reverse("nutrient-list")
        response = self.client.get(url)

        # Assert 1.
        self.assertEqual(response.status_code, 200)

        # Assert 2.
        self.assertEqual(response.data['count'], 2)

    def test_nutrient_item(self):
        """
        Assert:
        1. The nutrient-detail view can be called without authentication.
        2. The nutrient-detail_view returns the correct number items.
        """
        url = reverse("nutrient-detail", kwargs={'pk': self.fat.pk})
        response = self.client.get(url)

        # Assert 1.
        self.assertEqual(response.status_code, 200)

        # Assert 2.
        self.assertEqual(response.data['pk'], self.fat.pk)

    def test_nutrient_create_not_allowed(self):
        """
        Assert:
        1. The nutrient-create view returns a 405 (Method not allowed) status code.
        """
        url = reverse("nutrient-list")
        response = self.client.post(url, {'name': 'Eggs & Dairy products'})

        # Assert 1.
        self.assertEqual(response.status_code, 405)

    def test_nutrient_update_not_allowed(self):
        """
        Assert:
        1. The nutrient-detail view returns a 405 (Method not allowed) status code for a full update.
        2. The nutrient-detail view returns a 405 (Method not allowed) status code for a partial update.
        3. The nutrient-list view returns a 405 (Method not allowed) status code for a full update.
        4. The nutrient-list view returns a 405 (Method not allowed) status code for a partial update.
        """
        url = reverse("nutrient-detail", kwargs={'pk': self.l.pk})
        response = self.client.patch(url, {'name': 'Liter'})

        # Assert 1.
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(url, {'name': 'Liter'})

        # Assert 2.
        self.assertEqual(response.status_code, 405)

        # Assert 3.
        url = reverse("nutrient-list")
        response = self.client.put(url, {'pk': self.l.pk, 'name': 'Liter'})
        self.assertEqual(response.status_code, 405)

        # Assert 4.
        url = reverse("nutrient-list")
        response = self.client.patch(url, {'pk': self.l.pk, 'name': 'Liter'})
        self.assertEqual(response.status_code, 405)

    def test_nutrient_delete_not_allowed(self):
        """
        Assert:
        1. The nutrient-delete view returns a 405 (Method not allowed) status code.
        """
        url = reverse("nutrient-detail", kwargs={'pk': self.l.pk})
        response = self.client.delete(url)

        # Assert 1.
        self.assertEqual(response.status_code, 405)


class UnitViewSetTestCase(BaseTest):
    """
    A TestCase that performs tests on the UnitViewSet in the api package of the food app.
    """
    
    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_unit_list(self):
        """
        Assert:
        1. The unit-list view can be called without authentication.
        2. The unit-list view contains the correct number items.
        """
        url = reverse("unit-list")
        response = self.client.get(url)

        # Assert 1.
        self.assertEqual(response.status_code, 200)

        # Assert 2.
        self.assertEqual(response.data['count'], 7)

    def test_unit_item(self):
        """
        Assert:
        1. The unit-detail view can be called without authentication.
        2. The unit-detail_view returns the correct number items.
        """
        url = reverse("unit-detail", kwargs= {'pk' : self.g.pk})
        response = self.client.get(url)

        # Assert 1.
        self.assertEqual(response.status_code, 200)

        # Assert 2.
        self.assertEqual(response.data['pk'], self.g.pk)

    def test_unit_create_not_allowed(self):
        """
        Assert:
        1. The unit-create view returns a 405 (Method not allowed) status code.
        """
        url = reverse("unit-list")
        response = self.client.post(url, {'name' : 'Eggs & Dairy products'})

        # Assert 1.
        self.assertEqual(response.status_code, 405)

    def test_unit_update_not_allowed(self):
        """
        Assert:
        1. The unit-detail view returns a 405 (Method not allowed) status code for a full update.
        2. The unit-detail view returns a 405 (Method not allowed) status code for a partial update.
        3. The unit-list view returns a 405 (Method not allowed) status code for a full update.
        4. The unit-list view returns a 405 (Method not allowed) status code for a partial update.
        """
        url = reverse("unit-detail", kwargs={'pk': self.l.pk})
        response = self.client.patch(url, {'name': 'Liter'})

        # Assert 1.
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(url, {'name': 'Liter'})

        # Assert 2.
        self.assertEqual(response.status_code, 405)

        # Assert 3.
        url = reverse("unit-list")
        response = self.client.put(url, {'pk': self.l.pk, 'name': 'Liter'})
        self.assertEqual(response.status_code, 405)

        # Assert 4.
        url = reverse("unit-list")
        response = self.client.patch(url, {'pk': self.l.pk, 'name': 'Liter'})
        self.assertEqual(response.status_code, 405)

    def test_unit_delete_not_allowed(self):
        """
        Assert:
        1. The unit-delete view returns a 405 (Method not allowed) status code.
        """
        url = reverse("unit-detail", kwargs={'pk': self.l.pk})
        response = self.client.delete(url)

        # Assert 1.
        self.assertEqual(response.status_code, 405)


class FoodGroupViewSetTestCase(BaseTest):
    """
    A TestCase that performs tests on the FoodGroupViewSet in the api package of the food app.
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_food_group_list(self):
        """
        Assert:
        1. The foodgroup-list view can be called without authentication.
        2. The foodgroup-list view contains the correct number items.
        3. The items in the foodgroup-list_view are in the correct order.
        """
        url = reverse("foodgroup-list")
        response = self.client.get(url)

        # Assert 1.
        self.assertEqual(response.status_code, 200)

        # Assert 2.
        self.assertEqual(len(response.data['results']), 2)

        # Assert 3.
        print(response.data['results'][0]['name'])
        self.assertEqual(response.data['results'][0]['name'], 'Meat')

    def test_food_group_item(self):
        """
        Assert:
        1. The foodgroup-detail view can be called without authentication.
        2. The foodgroup-detail_view returns the correct number items.
        """
        url = reverse("foodgroup-detail", kwargs= {'pk' : self.food_group.pk})
        response = self.client.get(url)

        # Assert 1.
        self.assertEqual(response.status_code, 200)

        # Assert 2.
        self.assertEqual(response.data['pk'], self.food_group.pk)

    def test_food_group_create_not_allowed(self):
        """
        Assert:
        1. The foodgroup-create view returns a 405 (Method not allowed) status code.
        """
        url = reverse("foodgroup-list")
        response = self.client.post(url, {'name' : 'Eggs & Dairy products'})

        # Assert 1.
        self.assertEqual(response.status_code, 405)

    def test_food_group_update_not_allowed(self):
        """
        Assert:
        1. The foodgroup-detail view returns a 405 (Method not allowed) status code for a full update.
        2. The foodgroup-detail view returns a 405 (Method not allowed) status code for a partial update.
        3. The foodgroup-list view returns a 405 (Method not allowed) status code for a full update.
        4. The foodgroup-list view returns a 405 (Method not allowed) status code for a partial update.
        """
        url = reverse("foodgroup-detail", kwargs={'pk': self.food_group.pk})
        response = self.client.patch(url, {'name': 'Eggs & Dairy products'})

        # Assert 1.
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(url, {'name': 'Eggs & Dairy products'})

        # Assert 2.
        self.assertEqual(response.status_code, 405)

        # Assert 3.
        url = reverse("foodgroup-list")
        response = self.client.put(url, {'pk': self.food_group.pk, 'name': 'Eggs & Dairy products'})
        self.assertEqual(response.status_code, 405)

        # Assert 4.
        url = reverse("foodgroup-list")
        response = self.client.patch(url, {'pk': self.food_group.pk, 'name': 'Eggs & Dairy products'})
        self.assertEqual(response.status_code, 405)

    def test_food_group_delete_not_allowed(self):
        """
        Assert:
        1. The foodgroup-delete view returns a 405 (Method not allowed) status code.
        """
        url = reverse("foodgroup-detail", kwargs={'pk': self.food_group.pk})
        response = self.client.delete(url)

        # Assert 1.
        self.assertEqual(response.status_code, 405)