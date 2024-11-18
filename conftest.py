import pytest
from django.conf import settings
import logging

# Disable unnecessary logs during testing
logging.disable(logging.WARNING)

def pytest_configure():
    settings.DEBUG = False 