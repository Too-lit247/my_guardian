from django.core.management.base import BaseCommand
from geography.models import Region


class Command(BaseCommand):
    help = 'Populate the database with initial regions'

    def handle(self, *args, **options):
        regions_data = [
            {
                'name': 'central',
                'display_name': 'Central Region',
                'description': 'Central region covering the main metropolitan areas'
            },
            {
                'name': 'north',
                'display_name': 'Northern Region',
                'description': 'Northern region covering the northern territories'
            },
            {
                'name': 'southern',
                'display_name': 'Southern Region',
                'description': 'Southern region covering the southern territories'
            }
        ]

        for region_data in regions_data:
            region, created = Region.objects.get_or_create(
                name=region_data['name'],
                defaults={
                    'display_name': region_data['display_name'],
                    'description': region_data['description']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created region: {region.display_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Region already exists: {region.display_name}')
                )
