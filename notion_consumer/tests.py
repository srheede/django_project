import os
from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from notion_client import Client
from decouple import config

class NotionIntegrationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command('setup_notion_test_data')

    def test_notion_data_creation(self):
        notion = Client(auth=os.getenv('NOTION_TOKEN'))
        database_id = config('TEST_DATABASE_ID')
        
        results = notion.databases.query(database_id=database_id)
        
        test_row_found = any(
            'Test Row' in page['properties']['Name']['title'][0]['text']['content'] 
            for page in results['results']
        )
        
        self.assertTrue(test_row_found, "Test Row was not found in the Test Database")

    @classmethod
    def tearDownClass(cls):
        call_command('cleanup_notion_test_data')
        super().tearDownClass()