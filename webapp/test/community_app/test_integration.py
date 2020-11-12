"""Test integration with other BH libraries with mocks.
This is only to test that the internal plumbing of Core Framework works with the community app.

Currently includes:
    * bh-settings-python
    * core-framework-python
"""
# from bh.core_utils.test_utils import mock_settings, mock_service_call, ServiceCallMock
# from bh.services.factory import Factory

# import bh_settings

# @mock_settings({"hello": "goodbye", "global_instance_warming_default": 10})
# def test_get_setting(_setting_mock):
#     # Verify CF defaults are pulled in
#     assert bh_settings.get_settings("default_warmed_instances") == 5

#     # Verify mocked new settings are pulled in
#     assert bh_settings.get_settings("hello") == "goodbye"

#     # Verify mocked overridden settings are pulled in
#     assert bh_settings.get_settings("global_instance_warming_default") == 10

# @mock_service_call(ServiceCallMock("Blah", "1", "test", return_value="hello"))
# def test_service_call(self):
#     assert Factory.create("Blah", "1").test() == "hello"
