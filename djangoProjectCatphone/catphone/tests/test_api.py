from rest_framework.test import APITestCase
from django.urls import reverse
from catphone.models import Catsphone
from catphone.serializers import CatphoneSerializers
from rest_framework import status


class FruitApiTestCase(APITestCase):
    def test_get_list(self):
        product_1 = Catsphone.objects.create(name='Iphone 12', price=60000)
        product_2 = Catsphone.objects.create(name='Samsung', price=55000)

        response = self.client.get(reverse('product_api_list'))

        serial_data = CatphoneSerializers([product_1, product_2], many=True).data
        serial_data = {'product_list': serial_data}

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serial_data, response.data)
