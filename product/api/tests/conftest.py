import pytest
import allure
import json
import os
import random
from datetime import datetime

from api_service import APIService

@pytest.fixture(scope="session")
def api_service():
    """Create an API service instance for testing"""
    return APIService()

@pytest.fixture(scope="function")
def random_post_id():
    """Generate a random post ID between 1 and 100"""
    return random.randint(1, 100)

@pytest.fixture(scope="function")
def test_data():
    """Generate test data for creating posts"""
    return {
        "title": f"Test Post {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "body": "This is a test post created for the Allure report demo.",
        "userId": 1
    }

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Customize test report for Allure"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        # Add extra information to the report
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Only capture details for failed tests
            mode = "a" if os.path.exists("test-failures.txt") else "w"
            with open("test-failures.txt", mode) as f:
                f.write(f"{report.nodeid} - FAILED\\n")

@allure.step("Verify successful response")
def verify_success_response(response, expected_code=200):
    """Helper to verify success responses"""
    assert response.status_code == expected_code, \
        f"Expected status code {expected_code}, but got {response.status_code}"
    return True

@allure.step("Verify response data contains expected fields")
def verify_response_fields(response_data, expected_fields):
    """Helper to verify response data fields"""
    for field in expected_fields:
        assert field in response_data, f"Expected field '{field}' not found in response"
    return True
