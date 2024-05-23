# notion_consumer/management/commands/setup_notion_test_data.py

import os
from django.core.management.base import BaseCommand
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Set up test data in Notion'

    def handle(self, *args, **kwargs):
        notion = Client(auth=os.getenv('NOTION_TOKEN'))

        # Create a new parent page in Notion
        new_page = {
            "parent": {"type": "workspace"},
            "properties": {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": "Test Parent Page"}
                    }
                ]
            }
        }

        try:
            created_page = notion.pages.create(**new_page)
            parent_page_id = created_page['id']

            # Store the parent page ID in an environment variable for later use
            with open('.env', 'a') as env_file:
                env_file.write(f'\nTEST_PARENT_PAGE_ID={parent_page_id}\n')

            # Create a new database in the Notion parent page
            new_database = {
                "parent": {"type": "page_id", "page_id": parent_page_id},
                "title": [
                    {
                        "type": "text",
                        "text": {"content": "Test Database"}
                    }
                ],
                "properties": {
                    "Name": {"title": {}},
                    "Description": {"rich_text": {}}
                }
            }

            created_database = notion.databases.create(**new_database)
            database_id = created_database['id']

            # Store the database ID in an environment variable for later use
            with open('.env', 'a') as env_file:
                env_file.write(f'\nTEST_DATABASE_ID={database_id}\n')

            # Create a test row in the new database
            test_page = {
                "parent": {"database_id": database_id},
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": "Test Row"
                                }
                            }
                        ]
                    },
                    "Description": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": "This is a test row"
                                }
                            }
                        ]
                    }
                }
            }

            notion.pages.create(**test_page)
            self.stdout.write(self.style.SUCCESS('Test database and data created in Notion.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to create test data: {e}'))
