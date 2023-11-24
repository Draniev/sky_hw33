from tests.factories import GoalFactory
import pytest
from django.conf import settings
from pytest_factoryboy import register


# @pytest.fixture(autouse=True)
# def set_test_database_settings(settings):
#     settings.DATABASES['default']['HOST'] = 'localhost'


# @pytest.fixture(autouse=True)
# def use_dummy_cache_backend(settings):
#     settings.DATABASES = {
#         "default": {
#             "HOST": "localhost",
#         }
#     }


# def pytest_configure():
#     data = {
#         "default": {
#             "HOST": "localhost",
#         }
#     }
#     settings.configure(DATABASES=data)


pytest_plugins = "tests.fixtures"
# register(AdsFactory)
# register(CatFactory)
# register(UserFactory)
