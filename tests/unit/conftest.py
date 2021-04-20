import os
import pytest
import json
import sqlite3
import datetime
from unittest.mock import patch
from config import config


@pytest.fixture(scope='session')
def client(request):
    os.environ['ADMS_CONFIG'] = 'testing'
    
