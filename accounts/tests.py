from django.db.models import Q
from decimal import *
from django.test import TestCase
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Profile

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        inn_list = [
            '123456789011',
            '123456789011',
            '123456789012',
            '123456789013',
            '123456789014',
        ]
        self.users = []
        for inn in inn_list:
            self.users.append(mommy.make(Profile, inn=inn, balance=100))

    def tearDown(self):
        Profile.objects.all().delete()

    def test_list(self):
        url = reverse('api-user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

    def test_send_money(self):
        url = reverse('api-user-money-transfer')
        form_data = {
            'usersSelect': '1',
            'inn': '123456789013',
            'amount': '10',
        }
        # single INN
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertDictEqual(resp_data, {'message': 'success'})
        profile_sender = Profile.objects.get(user__pk=form_data['usersSelect'])
        profile_reciever = Profile.objects.get(inn='123456789013')
        self.assertEqual(profile_sender.balance, 90)
        self.assertEqual(profile_reciever.balance, 110)
        # multiple INN
        form_data['inn'] = '123456789013, 123456789014'
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertDictEqual(resp_data, {'message': 'success'})
        profile_sender = Profile.objects.get(user__pk=form_data['usersSelect'])
        profile_reciever_1 = Profile.objects.get(inn='123456789013')
        profile_reciever_2 = Profile.objects.get(inn='123456789014')
        self.assertEqual(profile_sender.balance, 80)
        self.assertEqual(profile_reciever_1.balance, 115)
        self.assertEqual(profile_reciever_2.balance, 105)

    def test_send_money_equal_inn(self):
        url = reverse('api-user-money-transfer')
        form_data = {
            'usersSelect': '1',
            'inn': '123456789011, 123456789014',
            'amount': '10',
        }
        # sender and reciever equal INN
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertDictEqual(resp_data, {'message': 'success'})
        profile_sender = Profile.objects.get(user__pk=form_data['usersSelect'])
        profile_reciever_1 = Profile.objects.get(~Q(user=profile_sender.user), inn='123456789011')
        profile_reciever_2 = Profile.objects.get(inn='123456789014')
        self.assertEqual(profile_sender.balance, 90)
        self.assertEqual(profile_reciever_1.balance, 105)
        self.assertEqual(profile_reciever_2.balance, 105)

    def test_send_money_ramainder(self):
        url = reverse('api-user-money-transfer')
        form_data = {
            'usersSelect': '1',
            'inn': '123456789012, 123456789013, 123456789014',
            'amount': '20',
        }
        # division remainder
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertDictEqual(resp_data, {'message': 'success'})
        profile_sender = Profile.objects.get(user__pk=form_data['usersSelect'])
        profile_reciever_1 = Profile.objects.get(inn='123456789012')
        profile_reciever_2 = Profile.objects.get(inn='123456789013')
        profile_reciever_3 = Profile.objects.get(inn='123456789014')
        self.assertEqual(profile_sender.balance, 80)
        self.assertEqual(profile_reciever_1.balance, Decimal('106.67'))
        self.assertEqual(profile_reciever_2.balance, Decimal('106.67'))
        self.assertEqual(profile_reciever_3.balance, Decimal('106.66'))

    def test_send_money_errors(self):
        url = reverse('api-user-money-transfer')
        # set all data to wrong values
        form_data = {
            'usersSelect': '0',
            'inn': '123',
            'amount': '9000',
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 400)
        resp_data = response.json()
        self.assertDictEqual(resp_data, {'error': 'user does not exist'})
        # existed user
        form_data['usersSelect'] = '1';
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 400)
        resp_data = response.json()
        self.assertDictEqual(resp_data, {'error': 'not enough funds on user balance'})
        # correct amount
        form_data['amount'] = '10'
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 400)
        resp_data = response.json()
        self.assertDictEqual(resp_data, {'error': 'wrong INN'})
        # all fields are correct
        form_data['inn'] = '123456789012'
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertDictEqual(resp_data, {'message': 'success'})

