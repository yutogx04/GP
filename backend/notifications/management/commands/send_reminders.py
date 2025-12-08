"""
Django management command to send schedule reminders.
Run this command periodically (e.g., every 15 minutes via cron or Task Scheduler).

Usage:
    python manage.py send_reminders

Windows Task Scheduler (every 15 min):
    schtasks /create /tn "MedIntern Reminders" /tr "python manage.py send_reminders" /sc minute /mo 15

Linux cron (every 15 min):
    */15 * * * * cd /path/to/backend && python manage.py send_reminders
"""
from django.core.management.base import BaseCommand
from notifications.tasks import send_schedule_reminders


class Command(BaseCommand):
    help = 'Send reminder notifications for upcoming scheduled events'

    def handle(self, *args, **options):
        self.stdout.write('Checking for upcoming events...')
        
        result = send_schedule_reminders()
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Reminders sent - 1h: {result['reminders_1h']}, 24h: {result['reminders_24h']}"
            )
        )
