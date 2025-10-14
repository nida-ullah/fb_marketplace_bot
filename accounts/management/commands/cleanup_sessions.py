from django.core.management.base import BaseCommand
from accounts.models import FacebookAccount
import os


class Command(BaseCommand):
    help = 'Clean up orphaned session files that have no matching account in database'

    def handle(self, *args, **options):
        sessions_dir = "sessions"
        
        if not os.path.exists(sessions_dir):
            self.stdout.write(self.style.WARNING('Sessions directory does not exist'))
            return
        
        # Get all emails from database
        db_emails = set(FacebookAccount.objects.values_list('email', flat=True))
        
        # Get all session files
        session_files = [f for f in os.listdir(sessions_dir) if f.endswith('.json')]
        
        deleted_count = 0
        
        for session_file in session_files:
            # Convert filename back to email
            email = session_file.replace('.json', '').replace('_', '@', 1).replace('_', '.')
            
            # If email not in database, delete session
            if email not in db_emails:
                file_path = os.path.join(sessions_dir, session_file)
                os.remove(file_path)
                deleted_count += 1
                self.stdout.write(self.style.SUCCESS(f'🗑️ Deleted orphaned session: {session_file}'))
        
        if deleted_count == 0:
            self.stdout.write(self.style.SUCCESS('✅ No orphaned sessions found'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Deleted {deleted_count} orphaned session(s)'))
