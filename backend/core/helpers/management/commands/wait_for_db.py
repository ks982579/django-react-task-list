"""
Django command to wait for database to become available
"""

from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Django command to wait for database."""
    def handle(self, *args, **options):
        """EntryPoint for Command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                # check() throws an error if database is not ready
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database still unavailable, continue to hold...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database is available!'))