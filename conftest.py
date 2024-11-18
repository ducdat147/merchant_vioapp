import pytest
from django.conf import settings
import logging

# Tắt các log không cần thiết trong quá trình test
logging.disable(logging.WARNING)

def pytest_configure():
    settings.DEBUG = False 