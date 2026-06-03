from django.core.management.base import BaseCommand
from korrupsiya_app.models import Vacancy
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate sample vacancy data'

    def handle(self, *args, **options):
        vacancies_data = [
            {
                'company': 'IT Park',
                'title': 'Backend Developer',
                'type': 'Full Time',
                'work_hours': '09:00 - 18:00',
                'location': 'Tashkent',
                'salary': '10,000,000 - 15,000,000 UZS',
                'experience': '2-3 yil',
                'education': 'Bachelor',
                'status': 'active',
                'published_date': datetime.now().date(),
                'deadline': (datetime.now() + timedelta(days=30)).date(),
                'responsibilities': [
                    'RESTful API yozish',
                    'Database design',
                    'Kod review qilish',
                    'Team bilan hamkorlik'
                ],
                'requirements': [
                    'Python 3.9+',
                    'Django / DRF',
                    'PostgreSQL',
                    'Git'
                ],
                'languages': ['Uzbek', 'English', 'Russian'],
                'conditions': [
                    'Health insurance',
                    'Professional development',
                    'Remote work available',
                    'Competitive salary'
                ],
                'positions': 1,
                'title_translations': {
                    'uz': 'Backend Dasturchi',
                    'ru': 'Backend разработчик',
                    'en': 'Backend Developer'
                }
            },
            {
                'company': 'Univer Tech',
                'title': 'Frontend Developer',
                'type': 'Full Time',
                'work_hours': '10:00 - 19:00',
                'location': 'Tashkent',
                'salary': '8,000,000 - 12,000,000 UZS',
                'experience': '1-2 yil',
                'education': 'Bachelor',
                'status': 'active',
                'published_date': datetime.now().date(),
                'deadline': (datetime.now() + timedelta(days=25)).date(),
                'responsibilities': [
                    'React bilan UI develop qilish',
                    'Responsive design',
                    'API integration',
                    'Testing'
                ],
                'requirements': [
                    'React.js',
                    'TypeScript',
                    'HTML/CSS',
                    'Figma'
                ],
                'languages': ['Uzbek', 'English'],
                'conditions': [
                    'Flexible schedule',
                    'Bonus system',
                    'Team events',
                    'Modern tools'
                ],
                'positions': 2,
                'title_translations': {
                    'uz': 'Frontend Dasturchi',
                    'ru': 'Frontend разработчик',
                    'en': 'Frontend Developer'
                }
            },
            {
                'company': 'DataWay',
                'title': 'Data Analyst',
                'type': 'Full Time',
                'work_hours': '08:30 - 17:30',
                'location': 'Tashkent',
                'salary': '7,000,000 - 10,000,000 UZS',
                'experience': '1-2 yil',
                'education': 'Bachelor',
                'status': 'active',
                'published_date': datetime.now().date(),
                'deadline': (datetime.now() + timedelta(days=20)).date(),
                'responsibilities': [
                    'Data analysis',
                    'Report generation',
                    'SQL queries',
                    'Data visualization'
                ],
                'requirements': [
                    'SQL',
                    'Python',
                    'Excel',
                    'Tableau/Power BI'
                ],
                'languages': ['Uzbek', 'Russian'],
                'conditions': [
                    'Training provided',
                    'Career growth',
                    'Stable company',
                    'Good team'
                ],
                'positions': 1,
                'title_translations': {
                    'uz': 'Ma\'lumot Analitikasi',
                    'ru': 'Аналитик данных',
                    'en': 'Data Analyst'
                }
            }
        ]

        for data in vacancies_data:
            vacancy, created = Vacancy.objects.get_or_create(
                company=data['company'],
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {vacancy.company} - {vacancy.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {vacancy.company} - {vacancy.title}"))

        self.stdout.write(self.style.SUCCESS('Successfully populated vacancies!'))
