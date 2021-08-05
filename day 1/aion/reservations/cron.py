from django_cron import CronJobBase, Schedule
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Resource, TimeBlock

class DatabaseCleanup(CronJobBase):
    '''This Cron Job is scheduled to run daily and cleanup the database. 
    This job will remove:
      - Users whose email has not been activated ( > 1 day old)
      - Resources that have been 'deleted' by building admins ( > 30 days old)
      - TimeBlocks that have been 'deleted' by building admins ( > 30 days old)
    
    To run this once:
      - python3 manage.py runcrons
    
    To schedule a CronTab at 1:01am every day:
      - cron -e 
      - 01 01 * * * source /home/ubuntu/.bashrc && source /home/ubuntu/workspace/venv/bin/activate && python3 /home/ubuntu/workspace/aion/src/manage.py runcrons > /home/ubuntu/cronjob.log
    '''
    RUN_EVERY_MINS = 60*24 # Daily

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'reservations.database_cleanup'    # a unique code

    def do(self):
        success={} # success message for log
        
        # Get inactive users
        inactive_users = User.objects.filter(
            profile__email_confirmed=False
        ).filter(
            date_joined__lt=timezone.now()-timezone.timedelta(days=1) # > 1 day old.
        )
        
        # Purge inactive users.
        if inactive_users.exists():
            success['users_removed'] = list(inactive_users) # for the log
            inactive_users.delete()
        else:
            success['users_removed'] ='None'
            
        # Get 'deleted' resources
        deleted_resources = Resource.objects.filter(
            deleted=True
        ).filter(
            deleted_on__lt=timezone.now()-timezone.timedelta(days=30) # > 30 days old.
        )
        
        # Purge 'deleted' resources.
        if deleted_resources.exists():
            success['resources_removed'] = list(deleted_resources) # for the log
            deleted_resources.delete()
        else:
            success['resources_removed'] = 'None'
            
        
        # Get 'deleted' time blocks
        deleted_time_blocks = TimeBlock.objects.filter(
            deleted=True
        ).filter(
            deleted_on__lt=timezone.now()-timezone.timedelta(days=30) # > 30 days old.
        )

        # Purge 'deleted' time blocks.
        if deleted_time_blocks.exists():
            success['time_blocks_removed'] = list(deleted_time_blocks) # for the log
            deleted_time_blocks.delete()
        else:
            success['time_blocks_removed'] = 'None'
            
        return str(success)
