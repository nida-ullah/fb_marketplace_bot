from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BulkAccountUploadForm
from .models import FacebookAccount
from automation.post_to_facebook import save_session
import os
from threading import Thread


def cleanup_orphaned_sessions():
    """Automatically clean up session files without matching database accounts"""
    sessions_dir = "sessions"
    
    if not os.path.exists(sessions_dir):
        return
    
    # Get all emails from database
    db_emails = set(FacebookAccount.objects.values_list('email', flat=True))
    
    # Get all session files
    session_files = [f for f in os.listdir(sessions_dir) if f.endswith('.json')]
    
    for session_file in session_files:
        # Convert filename back to email (handle the conversion properly)
        filename = session_file.replace('.json', '')
        parts = filename.split('_')
        
        # Reconstruct email
        if len(parts) >= 3:
            email = f"{parts[0]}@{'_'.join(parts[1:-1])}.{parts[-1]}"
            
            # If email not in database, delete session
            if email not in db_emails:
                file_path = os.path.join(sessions_dir, session_file)
                try:
                    os.remove(file_path)
                    print(f"🗑️ Auto-deleted orphaned session: {session_file}")
                except Exception as e:
                    print(f"Error deleting {session_file}: {e}")


def bulk_upload_accounts(request):
    # Auto cleanup orphaned sessions
    cleanup_orphaned_sessions()
    if request.method == 'POST':
        form = BulkAccountUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            # Read and parse file
            content = file.read().decode('utf-8')
            lines = content.strip().split('\n')
            
            accounts_to_process = []
            
            for line in lines:
                line = line.strip()
                if not line or ':' not in line:
                    continue
                
                email, password = line.split(':', 1)
                email = email.strip()
                password = password.strip()
                
                # Create or update account in database
                account, created = FacebookAccount.objects.get_or_create(
                    email=email,
                    defaults={'password': password}
                )
                
                if not created:
                    account.password = password
                    account.save()
                
                accounts_to_process.append((email, created))
            
            # Process sessions in background
            Thread(target=process_sessions, args=(accounts_to_process,), daemon=True).start()
            
            messages.success(request, f'Uploaded {len(accounts_to_process)} accounts. Sessions are being created in background.')
            return redirect('bulk_upload_accounts')
    else:
        form = BulkAccountUploadForm()
    
    accounts = FacebookAccount.objects.all().order_by('-created_at')
    return render(request, 'accounts/bulk_upload.html', {'form': form, 'accounts': accounts})


def process_sessions(accounts_list):
    """Process sessions for accounts in background"""
    for email, is_new in accounts_list:
        session_file = f"sessions/{email.replace('@', '_').replace('.', '_')}.json"
        
        # If session exists, skip
        if os.path.exists(session_file):
            print(f"✅ Session exists for {email}, skipping...")
            continue
        
        # Get password from database
        try:
            account = FacebookAccount.objects.get(email=email)
            password = account.password
        except FacebookAccount.DoesNotExist:
            password = None
        
        # Open browser for login and save session with auto-login
        print(f"🌐 Opening browser for {email}...")
        try:
            success = save_session(email, password)
            if success:
                print(f"✅ Session saved for {email}")
            else:
                print(f"❌ Login failed for {email} - Session NOT saved")
        except Exception as e:
            print(f"❌ Failed to save session for {email}: {e}")
