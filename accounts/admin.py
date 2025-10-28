from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import CustomUser, FacebookAccount
import os


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin with approval system"""
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_approved_display', 'is_staff', 'date_joined')
    list_filter = ('is_approved', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    # Add approval fields to fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Approval Information', {
            'fields': ('is_approved', 'approved_at', 'approved_by', 'rejection_reason')
        }),
    )

    readonly_fields = ('approved_at', 'approved_by',
                       'date_joined', 'last_login')

    actions = ['approve_users', 'reject_users']

    def is_approved_display(self, obj):
        """Display approval status with color"""
        if obj.is_approved:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Approved</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ Pending</span>'
            )

    is_approved_display.short_description = 'Approval Status'

    def approve_users(self, request, queryset):
        """Approve selected users"""
        count = 0
        for user in queryset.filter(is_approved=False):
            user.approve(request.user)
            count += 1

        self.message_user(
            request,
            f'{count} user(s) have been approved successfully.'
        )

    approve_users.short_description = 'Approve selected users'

    def reject_users(self, request, queryset):
        """Reject/unapprove selected users"""
        count = queryset.filter(is_approved=True).update(
            is_approved=False,
            approved_at=None,
            approved_by=None
        )

        self.message_user(
            request,
            f'{count} user(s) have been rejected/unapproved.'
        )

    reject_users.short_description = 'Reject/unapprove selected users'

    def save_model(self, request, obj, form, change):
        """Auto-set approved_by when approving"""
        if change and 'is_approved' in form.changed_data:
            if obj.is_approved:
                obj.approved_at = timezone.now()
                obj.approved_by = request.user
                obj.rejection_reason = None
            else:
                obj.approved_at = None
                obj.approved_by = None

        super().save_model(request, obj, form, change)


@admin.register(FacebookAccount)
class FacebookAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'has_session', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('email', 'user__username', 'user__email')
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
                print(
                    f"🌐 Opening browser for {obj.email} (session missing)...")
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
                        print(
                            f"❌ Failed to create session for {account.email}")
                except Exception as e:
                    print(f"❌ Error: {e}")

        Thread(target=process_accounts, daemon=True).start()
        self.message_user(
            request, f"Creating sessions for {queryset.count()} account(s) in background...")

    create_sessions.short_description = "Create sessions for selected accounts"
