from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase, Client
from django.utils import timezone
from django.urls import reverse, resolve
from feedback.views import home, AboutView, ResourcesView
from feedback.models import Report


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.report_success_url = reverse('report_success')
        
    def test_home_Get(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/home.html')

    def test_report_success_Get(self):
        response = self.client.get(self.report_success_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback/report_success.html')


class UrlsTest(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_about_url_is_resolved(self):
        url = reverse('about')
        resolved_view = resolve(url).func.view_class
        self.assertEquals(resolved_view, AboutView)

    def test_resources_url_is_resolved(self):
        url = reverse('resources')
        resolved_view = resolve(url).func.view_class
        self.assertEquals(resolved_view, ResourcesView)


class ReportModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.report = Report.objects.create(
            user=self.user,
            date=timezone.now().date(),
            restaurant_name='Test Restaurant 1',
            restaurant_address='123 Test St',
            restaurant_city='Test City',
            restaurant_state='VA',
            restaurant_zip='22903',
            consumption_date_time=timezone.now(), 
            symptoms='Headache and stomach ache',
            symptoms_start_date_time=timezone.now(), 
            suspected_illness_source='Test Source',
            additional_info='Test Additional Info'
        )

    def test_report_str_method(self):
        self.assertEqual(str(self.report), f"Report has been submitted for {self.report.restaurant_name}")

    def test_anonymous_user_report(self):
        report = Report.objects.create(
            date=timezone.now().date(), 
            restaurant_name='Test Restaurant 2',
            restaurant_address='123 Test St',
            restaurant_city='Test City',
            restaurant_state='TS',
            restaurant_zip='12345',
            consumption_date_time=timezone.now(), 
            symptoms='Test Symptoms',
            symptoms_start_date_time=timezone.now(), 
            suspected_illness_source='Test Source',
            additional_info='Test Additional Info'
        )
        self.assertEqual(report.user.username, 'Anonymous')
    
    def test_another_user_report_submission(self):
        report_data = {
            'user': self.user,
            'date': timezone.now().date(),
            'restaurant_name': 'Test Restaurant 2',
            'restaurant_address': '456 Test St',
            'restaurant_city': 'Test City',
            'restaurant_state': 'VA',
            'restaurant_zip': '22904',
            'consumption_date_time': timezone.now(), 
            'symptoms': 'Nausea',
            'symptoms_start_date_time': timezone.now(), 
            'suspected_illness_source': 'Source',
            'additional_info': 'Additional Info'
        }

        Report.objects.create(**report_data)

        saved_report = Report.objects.last()

        self.assertEqual(saved_report.user, self.user)
        self.assertEqual(saved_report.restaurant_name, 'Test Restaurant 2')
    
