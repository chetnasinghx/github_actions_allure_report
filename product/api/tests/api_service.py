import requests

class APIService:
    """Simple service to make API calls to JSONPlaceholder"""
    
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    def get_posts(self):
        """Get all posts"""
        response = requests.get(f"{self.BASE_URL}/posts")
        return response
    
    def get_post(self, post_id):
        """Get a specific post by ID"""
        response = requests.get(f"{self.BASE_URL}/posts/{post_id}")
        return response
    
    def create_post(self, title, body, user_id):
        """Create a new post"""
        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        response = requests.post(f"{self.BASE_URL}/posts", json=payload)
        return response
    
    def update_post(self, post_id, title, body, user_id):
        """Update an existing post"""
        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        response = requests.put(f"{self.BASE_URL}/posts/{post_id}", json=payload)
        return response
    
    def delete_post(self, post_id):
        """Delete a post"""
        response = requests.delete(f"{self.BASE_URL}/posts/{post_id}")
        return response
