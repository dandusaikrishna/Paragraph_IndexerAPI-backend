from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Paragraph, WordIndex
from rest_framework_simplejwt.tokens import RefreshToken 


class UserTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

    def test_user_registration(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'strongpassword123',
            'name': 'Test User',
            'dob': '1990-01-01'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_user_login(self):
        user = User.objects.create_user(email='testlogin@example.com', password='password123')
        data = {
            'email': 'testlogin@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class ParagraphTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='parauser@example.com', password='password123')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.paragraph_url = reverse('paragraphs')

    def test_submit_paragraphs(self):
        text = "Paragraph one.\n\nParagraph two.\n\nParagraph three."
        response = self.client.post(self.paragraph_url, {'text': text}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 3)
        # Check paragraphs saved correctly
        self.assertTrue(Paragraph.objects.filter(text="Paragraph one.").exists())
        self.assertTrue(Paragraph.objects.filter(text="Paragraph two.").exists())
        self.assertTrue(Paragraph.objects.filter(text="Paragraph three.").exists())

    def test_submit_paragraph_with_txt(self):
        text = "This is a paragraph with txt included.\n\nAnother paragraph."
        response = self.client.post(self.paragraph_url, {'text': text}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(Paragraph.objects.filter(text="This is a paragraph with txt included.").exists())
        self.assertTrue(Paragraph.objects.filter(text="Another paragraph.").exists())

    def test_submit_empty_text(self):
        response = self.client.post(self.paragraph_url, {'text': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_no_text_field(self):
        response = self.client.post(self.paragraph_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SearchTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='searchuser@example.com', password='password123')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.search_url = reverse('search')

        # Create paragraphs and word indices
        self.p1 = Paragraph.objects.create(text="Lorem ipsum dolor sit amet.")
        self.p2 = Paragraph.objects.create(text="Dolor sit amet consectetur.")
        WordIndex.objects.create(word='lorem', paragraph=self.p1)
        WordIndex.objects.create(word='ipsum', paragraph=self.p1)
        WordIndex.objects.create(word='dolor', paragraph=self.p1)
        WordIndex.objects.create(word='sit', paragraph=self.p1)
        WordIndex.objects.create(word='amet', paragraph=self.p1)
        WordIndex.objects.create(word='dolor', paragraph=self.p2)
        WordIndex.objects.create(word='sit', paragraph=self.p2)
        WordIndex.objects.create(word='amet', paragraph=self.p2)
        WordIndex.objects.create(word='consectetur', paragraph=self.p2)

    def test_search_word_found(self):
        response = self.client.get(self.search_url, {'word': 'dolor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        texts = [p['text'] for p in response.data]
        self.assertIn(self.p1.text, texts)
        self.assertIn(self.p2.text, texts)

    def test_search_word_case_insensitive(self):
        response = self.client.get(self.search_url, {'word': 'Dolor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_word_not_found(self):
        response = self.client.get(self.search_url, {'word': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_no_word_param(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_special_characters(self):
        response = self.client.get(self.search_url, {'word': '@#$%'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_authentication_required(self):
        self.client.credentials()  # Remove auth
        response = self.client.get(self.search_url, {'word': 'dolor'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthTests(APITestCase):
    def test_authentication_required(self):
        paragraph_url = reverse('paragraphs')
        search_url = reverse('search')

        # No auth token
        response = self.client.post(paragraph_url, {'text': 'Test paragraph.'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(search_url, {'word': 'test'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
