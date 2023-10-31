from django.test import TestCase


class TestMainapp(TestCase):

    def test_main_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_reg(self):
        response = self.client.get('/reg')
        self.assertEqual(response.status_code, 200)

    def test_account(self):
        response = self.client.get('/account')
        self.assertEqual(response.status_code, 302)

    def test_user_login(self):
        response = self.client.get('/user_login')
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        response = self.client.get('/user_logout')
        self.assertEqual(response.status_code, 302)

    def test_book_room(self):
        response = self.client.get('/book_room/1')
        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        response = self.client.get('/delete_booking/21')
        self.assertEqual(response.status_code, 302)




