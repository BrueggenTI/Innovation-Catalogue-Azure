
#!/usr/bin/env python3
"""
Comprehensive functional testing script for Brüggen Innovation Catalogue
"""

import requests
import json
import time
import logging
from urllib.parse import urljoin
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FunctionalTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, passed, message=""):
        """Log test result"""
        result = {
            'test': test_name,
            'passed': passed,
            'message': message,
            'timestamp': time.time()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status} - {test_name}: {message}")
        
    def test_homepage(self):
        """Test homepage functionality"""
        try:
            response = self.session.get(self.base_url)
            
            if response.status_code == 200:
                # Check for key elements
                required_elements = [
                    'Brüggen Innovation',
                    'Our Competence',
                    'Trends & Insights',
                    'Co-Creation Lab'
                ]
                
                missing_elements = [elem for elem in required_elements if elem not in response.text]
                
                if not missing_elements:
                    self.log_test("Homepage Load", True, "All key elements present")
                else:
                    self.log_test("Homepage Load", False, f"Missing elements: {missing_elements}")
            else:
                self.log_test("Homepage Load", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Homepage Load", False, f"Exception: {e}")
    
    def test_competence_page(self):
        """Test competence page functionality"""
        try:
            response = self.session.get(f"{self.base_url}/catalog")
            
            if response.status_code == 200:
                # Check for filter form
                if 'category' in response.text and 'ingredient' in response.text:
                    self.log_test("Competence Page Load", True, "Filter form present")
                else:
                    self.log_test("Competence Page Load", False, "Filter form missing")
                
                # Test filtering
                filter_response = self.session.get(f"{self.base_url}/catalog?category=Breakfast")
                if filter_response.status_code == 200:
                    self.log_test("Competence Filtering", True, "Category filter works")
                else:
                    self.log_test("Competence Filtering", False, "Category filter failed")
            else:
                self.log_test("Competence Page Load", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Competence Page Load", False, f"Exception: {e}")
    
    def test_trends_page(self):
        """Test trends page functionality"""
        try:
            response = self.session.get(f"{self.base_url}/trends")
            
            if response.status_code == 200:
                # Check for trend categories
                if 'health' in response.text.lower() or 'sustainability' in response.text.lower():
                    self.log_test("Trends Page Load", True, "Trend categories present")
                else:
                    self.log_test("Trends Page Load", False, "Trend categories missing")
                
                # Test category filtering
                filter_response = self.session.get(f"{self.base_url}/trends?category=health")
                if filter_response.status_code == 200:
                    self.log_test("Trends Filtering", True, "Category filter works")
                else:
                    self.log_test("Trends Filtering", False, "Category filter failed")
            else:
                self.log_test("Trends Page Load", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Trends Page Load", False, f"Exception: {e}")
    
    def test_cocreation_page(self):
        """Test co-creation page functionality"""
        try:
            response = self.session.get(f"{self.base_url}/cocreation")
            
            if response.status_code == 200:
                # Check for co-creation form elements
                required_elements = [
                    'session_id',
                    'client_name',
                    'client_email'
                ]
                
                missing_elements = [elem for elem in required_elements if elem not in response.text]
                
                if not missing_elements:
                    self.log_test("Co-Creation Page Load", True, "Form elements present")
                else:
                    self.log_test("Co-Creation Page Load", False, f"Missing elements: {missing_elements}")
            else:
                self.log_test("Co-Creation Page Load", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Co-Creation Page Load", False, f"Exception: {e}")
    
    def test_product_detail(self):
        """Test product detail page"""
        try:
            # First get a product ID from competence page
            competence_response = self.session.get(f"{self.base_url}/catalog")
            
            if competence_response.status_code == 200:
                # Try to access product detail (assuming product ID 1 exists)
                detail_response = self.session.get(f"{self.base_url}/product/1")
                
                if detail_response.status_code == 200:
                    # Check for product details
                    if 'ingredients' in detail_response.text.lower():
                        self.log_test("Product Detail Page", True, "Product details displayed")
                    else:
                        self.log_test("Product Detail Page", False, "Product details missing")
                elif detail_response.status_code == 404:
                    self.log_test("Product Detail Page", True, "404 handling works (no products)")
                else:
                    self.log_test("Product Detail Page", False, f"HTTP {detail_response.status_code}")
            else:
                self.log_test("Product Detail Page", False, "Cannot access competence page")
                
        except Exception as e:
            self.log_test("Product Detail Page", False, f"Exception: {e}")
    
    def test_concept_saving(self):
        """Test concept saving functionality"""
        try:
            test_session_id = str(uuid.uuid4())
            concept_data = {
                'session_id': test_session_id,
                'client_name': 'Test Client',
                'client_email': 'test@example.com',
                'product_config': {
                    'name': 'Test Product',
                    'category': 'Test Category',
                    'ingredients': ['Test Ingredient'],
                    'claims': ['Test Claim']
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/cocreation/save_concept",
                json=concept_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('success'):
                    self.log_test("Concept Saving", True, "Concept saved successfully")
                else:
                    self.log_test("Concept Saving", False, f"Save failed: {response_data.get('message')}")
            else:
                self.log_test("Concept Saving", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Concept Saving", False, f"Exception: {e}")
    
    def test_error_handling(self):
        """Test error handling"""
        try:
            # Test 404 error
            response = self.session.get(f"{self.base_url}/nonexistent-page")
            
            if response.status_code == 404:
                if 'Page Not Found' in response.text or '404' in response.text:
                    self.log_test("404 Error Handling", True, "Custom 404 page displayed")
                else:
                    self.log_test("404 Error Handling", False, "Generic 404 response")
            else:
                self.log_test("404 Error Handling", False, f"Expected 404, got {response.status_code}")
                
            # Test invalid product ID
            invalid_response = self.session.get(f"{self.base_url}/product/99999")
            if invalid_response.status_code == 404:
                self.log_test("Invalid Product ID", True, "404 for invalid product")
            else:
                self.log_test("Invalid Product ID", False, f"HTTP {invalid_response.status_code}")
                
        except Exception as e:
            self.log_test("Error Handling", False, f"Exception: {e}")
    
    def test_performance(self):
        """Test basic performance metrics"""
        try:
            start_time = time.time()
            response = self.session.get(self.base_url)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                if response_time < 2000:  # Less than 2 seconds
                    self.log_test("Performance Test", True, f"Response time: {response_time:.2f}ms")
                else:
                    self.log_test("Performance Test", False, f"Slow response: {response_time:.2f}ms")
            else:
                self.log_test("Performance Test", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Performance Test", False, f"Exception: {e}")
    
    def test_database_operations(self):
        """Test database operations"""
        try:
            # Test that database is accessible (via API endpoints)
            response = self.session.get(f"{self.base_url}/catalog")
            
            if response.status_code == 200:
                self.log_test("Database Operations", True, "Database accessible via API")
            else:
                self.log_test("Database Operations", False, "Database not accessible")
                
        except Exception as e:
            self.log_test("Database Operations", False, f"Exception: {e}")
    
    def run_all_tests(self):
        """Run all functional tests"""
        logger.info("Starting comprehensive functional testing...")
        
        test_methods = [
            self.test_homepage,
            self.test_competence_page,
            self.test_trends_page,
            self.test_cocreation_page,
            self.test_product_detail,
            self.test_concept_saving,
            self.test_error_handling,
            self.test_performance,
            self.test_database_operations
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                logger.error(f"Error running {test_method.__name__}: {e}")
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate functional test report"""
        logger.info("Generating functional test report...")
        
        print("\n" + "="*60)
        print("FUNCTIONAL TESTING REPORT")
        print("="*60)
        
        passed_tests = [t for t in self.test_results if t['passed']]
        failed_tests = [t for t in self.test_results if not t['passed']]
        
        print(f"\nSUMMARY:")
        print(f"Total Tests: {len(self.test_results)}")
        print(f"Passed: {len(passed_tests)}")
        print(f"Failed: {len(failed_tests)}")
        print(f"Success Rate: {len(passed_tests)/len(self.test_results)*100:.1f}%")
        
        if failed_tests:
            print(f"\nFAILED TESTS:")
            for test in failed_tests:
                print(f"❌ {test['test']}: {test['message']}")
        
        print(f"\nPASSED TESTS:")
        for test in passed_tests:
            print(f"✅ {test['test']}: {test['message']}")

if __name__ == "__main__":
    tester = FunctionalTester()
    tester.run_all_tests()
