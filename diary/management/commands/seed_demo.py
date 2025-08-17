from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from diary.models import Trip, Place

class Command(BaseCommand):
    help = 'Создаёт демо-пользователей и примеры поездок.'

    def handle(self, *args, **kwargs):
        # users
        users = []
        for username in ['anna', 'boris', 'katya']:
            u, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com'})
            if created or not u.has_usable_password():
                u.set_password('password'); u.save()
            users.append(u)
        anna, boris, katya = users

        # places
        old_town, _ = Place.objects.get_or_create(name='Старый город', kind=Place.Kind.VISIT)
        central_park, _ = Place.objects.get_or_create(name='Центральный парк', kind=Place.Kind.VISIT)
        cathedral, _ = Place.objects.get_or_create(name='Собор Св. Иакова', kind=Place.Kind.HERITAGE)
        fortress, _ = Place.objects.get_or_create(name='Крепость', kind=Place.Kind.HERITAGE)

        # trips
        t1, _ = Trip.objects.get_or_create(
            user=anna, title='Выходные в Риге',
            defaults=dict(
                description='Прогулки по набережной и Старому городу. Вкусный кофе и музеи.',
                country='Латвия', city='Рига', address='Vecrīga',
                latitude=56.9496, longitude=24.1052,
                total_cost=220.50, rating_convenience=4, rating_safety=5, rating_greenery=4,
                visibility=Trip.Visibility.PUBLIC
            )
        )
        t1.places_to_visit.set([old_town, central_park])
        t1.heritage_sites.set([cathedral])

        t2, _ = Trip.objects.get_or_create(
            user=boris, title='Париж весной',
            defaults=dict(
                description='Эйфелева башня, Лувр и круассаны.',
                country='Франция', city='Париж', address='Champ de Mars',
                latitude=48.8584, longitude=2.2945,
                total_cost=980.00, rating_convenience=5, rating_safety=4, rating_greenery=3,
                visibility=Trip.Visibility.PUBLIC
            )
        )
        t2.places_to_visit.set([central_park])
        t2.heritage_sites.set([fortress])

        t3, _ = Trip.objects.get_or_create(
            user=katya, title='Семейное море',
            defaults=dict(
                description='Тёплое море и фрукты.',
                country='Греция', city='Ханья', address='Old Venetian Harbor',
                latitude=35.5163, longitude=24.0180,
                total_cost=1200.00, rating_convenience=4, rating_safety=4, rating_greenery=5,
                visibility=Trip.Visibility.PRIVATE
            )
        )

        self.stdout.write(self.style.SUCCESS('Демо-данные созданы. Пользователи: anna/boris/katya (password)'))
