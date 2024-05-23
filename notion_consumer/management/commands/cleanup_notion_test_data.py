# notion_consumer/management/commands/cleanup_notion_test_data.py

import os
from django.core.management.base import BaseCommand
from notion_client import Client

class Command(BaseCommand):
    help = 'Cleanup test data in Notion'

    def handle(self, *args, **kwargs):
        notion = Client(auth=os.getenv('NOTION_TOKEN'))
        parent_page_id = kwargs.get('parent_page_id')
        database_id = kwargs.get('database_id')

        if not database_id or not parent_page_id:
            self.stdout.write(self.style.ERROR('No test database or parent page ID provided.'))
            return

        try:
            # Archive the test database
            notion.databases.update(database_id, archived=True)
            # Archive the test parent page
            notion.pages.update(parent_page_id, archived=True)
            self.stdout.write(self.style.SUCCESS('Test database and parent page cleaned up in Notion.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clean up test data: {e}'))
