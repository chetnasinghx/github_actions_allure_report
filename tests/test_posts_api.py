import pytest
import allure
import json
from conftest import verify_success_response, verify_response_fields

@allure.epic("API Testing")
@allure.feature("Posts API")
class TestPostsAPI:
    """Test suite for the Posts API"""
    
    @allure.story("Get all posts")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all_posts(self, api_service):
        """Test getting all posts returns 200 and proper data structure"""
        # Make the API request
        with allure.step("Send GET request to /posts endpoint"):
            response = api_service.get_posts()
        
        # Verify response
        verify_success_response(response)
        
        # Extract response data
        with allure.step("Parse response JSON"):
            posts = response.json()
        
        # Verify data structure
        with allure.step("Verify response is a list"):
            assert isinstance(posts, list), "Expected a list of posts"
        
        with allure.step("Verify list is not empty"):
            assert len(posts) > 0, "Expected at least one post"
        
        # Verify first post has expected fields
        with allure.step("Verify post has expected fields"):
            expected_fields = ["id", "title", "body", "userId"]
            verify_response_fields(posts[0], expected_fields)
        
        # Create an Allure attachment to show sample data
        with allure.step("Sample data from response"):
            allure.attach(
                json.dumps(posts[:2], indent=2),
                name="Sample Posts",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allure.story("Get a specific post")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_get_post_by_id(self, api_service, random_post_id):
        """Test getting a specific post by ID"""
        # Log the test data
        with allure.step(f"Testing with post ID: {random_post_id}"):
            pass
        
        # Make the API request
        with allure.step(f"Send GET request to /posts/{random_post_id} endpoint"):
            response = api_service.get_post(random_post_id)
        
        # Verify response
        verify_success_response(response)
        
        # Extract response data
        with allure.step("Parse response JSON"):
            post = response.json()
        
        # Verify data structure
        with allure.step("Verify post has expected fields"):
            expected_fields = ["id", "title", "body", "userId"]
            verify_response_fields(post, expected_fields)
        
        with allure.step("Verify post ID matches requested ID"):
            assert post["id"] == random_post_id, f"Expected post ID {random_post_id}, got {post['id']}"
        
        # Create an Allure attachment
        with allure.step("Post data"):
            allure.attach(
                json.dumps(post, indent=2),
                name=f"Post {random_post_id}",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allure.story("Create a new post")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_post(self, api_service, test_data):
        """Test creating a new post"""
        # Log the test data
        with allure.step(f"Creating post with title: {test_data['title']}"):
            pass
        
        # Make the API request
        with allure.step("Send POST request to /posts endpoint"):
            response = api_service.create_post(
                test_data["title"],
                test_data["body"],
                test_data["userId"]
            )
        
        # Verify response
        verify_success_response(response, 201)  # 201 Created
        
        # Extract response data
        with allure.step("Parse response JSON"):
            created_post = response.json()
        
        # Verify data structure
        with allure.step("Verify post has expected fields"):
            expected_fields = ["id", "title", "body", "userId"]
            verify_response_fields(created_post, expected_fields)
        
        with allure.step("Verify post data matches input"):
            assert created_post["title"] == test_data["title"], "Title doesn't match"
            assert created_post["body"] == test_data["body"], "Body doesn't match"
            assert created_post["userId"] == test_data["userId"], "User ID doesn't match"
        
        # Create an Allure attachment
        with allure.step("Created post data"):
            allure.attach(
                json.dumps(created_post, indent=2),
                name="Created Post",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allure.story("Update an existing post")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_update_post(self, api_service, random_post_id, test_data):
        """Test updating an existing post"""
        # Updated test data
        updated_title = f"Updated: {test_data['title']}"
        updated_body = f"Updated: {test_data['body']}"
        
        # Make the API request
        with allure.step(f"Send PUT request to /posts/{random_post_id} endpoint"):
            response = api_service.update_post(
                random_post_id,
                updated_title,
                updated_body,
                test_data["userId"]
            )
        
        # Verify response
        verify_success_response(response)
        
        # Extract response data
        with allure.step("Parse response JSON"):
            updated_post = response.json()
        
        # Verify data structure
        with allure.step("Verify updated post has expected fields"):
            expected_fields = ["id", "title", "body", "userId"]
            verify_response_fields(updated_post, expected_fields)
        
        with allure.step("Verify post data matches updated input"):
            assert updated_post["title"] == updated_title, "Updated title doesn't match"
            assert updated_post["body"] == updated_body, "Updated body doesn't match"
        
        # Create an Allure attachment
        with allure.step("Updated post data"):
            allure.attach(
                json.dumps(updated_post, indent=2),
                name=f"Updated Post {random_post_id}",
                attachment_type=allure.attachment_type.JSON
            )
    
    @allure.story("Delete a post")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_delete_post(self, api_service, random_post_id):
        """Test deleting a post"""
        # Make the API request
        with allure.step(f"Send DELETE request to /posts/{random_post_id} endpoint"):
            response = api_service.delete_post(random_post_id)
        
        # Verify response (empty 200 OK typically)
        with allure.step("Verify successful deletion."):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
