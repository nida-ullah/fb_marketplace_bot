from django.contrib import admin
from .models import FacebookAccount
import os


@admin.register(FacebookAccount)
class FacebookAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'has_session', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('email',)
    readonly_fields = ('created_at',)
    actions = ['create_sessions']
    
    def has_session(self, obj):
        session_file = f"sessions/{obj.email.replace('@', '_').replace('.', '_')}.json"
        return os.path.exists(session_file)
    
    has_session.boolean = True
    has_session.short_description = 'Session Exists'
    
    def save_model(self, request, obj, form, change):
        """Auto-create session when account is saved (new or edited without session)"""
        super().save_model(request, obj, form, change)
        
        # Check if session exists
        session_file = f"sessions/{obj.email.replace('@', '_').replace('.', '_')}.json"
        
        if not os.path.exists(session_file):
            # Open browser for login
            from automation.post_to_facebook import save_session
            from threading import Thread
            
            def create_session():
                print(f"🌐 Opening browser for {obj.email} (session missing)...")
                try:
                    success = save_session(obj.email, obj.password)
                    if success:
                        print(f"✅ Session created for {obj.email}")
                    else:
                        print(f"❌ Failed to create session for {obj.email}")
                except Exception as e:
                    print(f"❌ Error creating session: {e}")
            
            Thread(target=create_session, daemon=True).start()
    
    def create_sessions(self, request, queryset):
        """Admin action to create sessions for selected accounts"""
        from automation.post_to_facebook import save_session
        from threading import Thread
        
        def process_accounts():
            for account in queryset:
                session_file = f"sessions/{account.email.replace('@', '_').replace('.', '_')}.json"
                if os.path.exists(session_file):
                    print(f"✅ Session exists for {account.email}, skipping...")
                    continue
                
                print(f"🌐 Opening browser for {account.email}...")
                try:
                    success = save_session(account.email, account.password)
                    if success:
                        print(f"✅ Session created for {account.email}")
                    else:
                        print(f"❌ Failed to create session for {account.email}")
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        Thread(target=process_accounts, daemon=True).start()
        self.message_user(request, f"Creating sessions for {queryset.count()} account(s) in background...")
    
    create_sessions.short_description = "Create sessions for selected accounts"
