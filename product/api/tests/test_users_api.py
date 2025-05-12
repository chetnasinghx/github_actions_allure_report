import pytest
import allure
import json
import requests
from conftest import verify_success_response, verify_response_fields

@allure.epic("API Testing")
@allure.feature("Users API")
class TestUsersAPI:
    """Test suite for the Users API"""
    
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    @allure.story("Get all users")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all_users(self):
        """Test getting all users returns 200 and proper data structure"""
        # Make the API request
        with allure.step("Send GET request to /users endpoint"):
            response = requests.get(f"{self.BASE_URL}/users")
        
        # Verify response
        verify_success_response(response)
        
        # Extract response data
        with allure.step("Parse response JSON"):
            users = response.json()
        
        # Verify data structure
        with allure.step("Verify response is a list"):
            assert isinstance(users, list), "Expected a list of users"
        
        with allure.step("Verify list is not empty"):
            assert len(users) > 0, "Expected at least one user"
        
        # Verify first user has expected fields
        with allure.step("Verify user has expected fields"):
            expected_fields = ["id", "name", "username", "email"]
            verify_response_fields(users[0], expected_fields)
        
        # Create an Allure attachment to show sample data
        with allure.step("Sample data from response"):
            allure.attach(
                json.dumps(users[:2], indent=2),
                name="Sample Users",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allure.story("Get a specific user")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_get_user_by_id(self):
        """Test getting a specific user by ID"""
        # Choose a user ID
        user_id = 1
        
        # Make the API request
        with allure.step(f"Send GET request to /users/{user_id} endpoint"):
            response = requests.get(f"{self.BASE_URL}/users/{user_id}")
        
        # Verify response
        verify_success_response(response)
        
        # Extract response data
        with allure.step("Parse response JSON"):
            user = response.json()
        
        # Verify data structure
        with allure.step("Verify user has expected fields"):
            expected_fields = ["id", "name", "username", "email", "address", "phone", "website", "company"]
            verify_response_fields(user, expected_fields)
        
        with allure.step("Verify user ID matches requested ID"):
            assert user["id"] == user_id, f"Expected user ID {user_id}, got {user['id']}"
        
        # Create an Allure attachment
        with allure.step("User data"):
            allure.attach(
                json.dumps(user, indent=2),
                name=f"User {user_id}",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allure.story("Verify user company info")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    def test_user_company_info(self):
        """Test that user company info has the correct structure"""
        # Choose a user ID
        user_id = 2
        
        # Make the API request
        with allure.step(f"Send GET request to /users/{user_id} endpoint"):
            response = requests.get(f"{self.BASE_URL}/users/{user_id}")
        
        # Verify response
        verify_success_response(response)
        
        # Extract response data
        with allure.step("Parse response JSON"):
            user = response.json()
        
        # Verify company info
        with allure.step("Verify company information"):
            assert "company" in user, "User should have company information"
            company = user["company"]
            
            expected_fields = ["name", "catchPhrase", "bs"]
            verify_response_fields(company, expected_fields)
        
        # Create an Allure attachment
        with allure.step("Company data"):
            allure.attach(
                json.dumps(company, indent=2),
                name=f"Company Info for User {user_id}",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allure.story("Verify user address")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    def test_user_address(self):
        """Test that user address has the correct structure"""
        # Choose a user ID
        user_id = 3
        
        # Make the API request
        with allure.step(f"Send GET request to /users/{user_id} endpoint"):
            response = requests.get(f"{self.BASE_URL}/users/{user_id}")
        
        # Verify response
        verify_success_response(response)
        
        # Extract response data
        with allure.step("Parse response JSON"):
            user = response.json()
        
        # Verify address info
        with allure.step("Verify address information"):
            assert "address" in user, "User should have address information"
            address = user["address"]
            
            expected_fields = ["street", "suite", "city", "zipcode", "geo"]
            verify_response_fields(address, expected_fields)
            
            # Verify geo coordinates
            assert "geo" in address, "Address should have geo coordinates"
            geo = address["geo"]
            
            expected_geo_fields = ["lat", "lng"]
            verify_response_fields(geo, expected_geo_fields)
        
        # Create an Allure attachment
        with allure.step("Address data"):
            allure.attach(
                json.dumps(address, indent=2),
                name=f"Address Info for User {user_id}",
                attachment_type=allure.attachment_type.JSON
            )
