import time
from django.db  import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """django command to pause excution until db is availale"""

    def handle(self,*args,**kwargs):
        self.stdout.write('waiting for database.... ')
        db_conn  = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('database unavailable, waiting 1 second')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available'))

