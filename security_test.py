
#!/usr/bin/env python3
"""
Comprehensive security testing script for Brüggen Innovation Catalogue
"""

import json
import requests
import sqlite3
import os
import re
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.vulnerabilities = []
        
    def log_vulnerability(self, severity, description, endpoint=None):
        """Log a security vulnerability"""
        vuln = {
            'severity': severity,
            'description': description,
            'endpoint': endpoint,
        }
        self.vulnerabilities.append(vuln)
        logger.warning(f"[{severity}] {description} - {endpoint}")
        
    def test_sql_injection(self):
        """Test for SQL injection vulnerabilities"""
        logger.info("Testing SQL injection...")
        
        # Test endpoints with parameters
        test_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE products;--",
            "' UNION SELECT * FROM sqlite_master--",
            "1' AND 1=1--",
            "1' AND 1=2--"
        ]
        
        endpoints = [
            "/competence?category={}",
            "/competence?ingredient={}",
            "/competence?claim={}",
            "/product/{}"
        ]
        
        for endpoint in endpoints:
            for payload in test_payloads:
                try:
                    if "/product/" in endpoint:
                        url = urljoin(self.base_url, endpoint.format(payload))
                    else:
                        url = urljoin(self.base_url, endpoint.format(payload))
                    
                    response = self.session.get(url)
                    
                    # Check for SQL error messages
                    error_patterns = [
                        r'sqlite3\.',
                        r'SQL syntax',
                        r'mysql_fetch',
                        r'ORA-\d+',
                        r'PostgreSQL.*ERROR',
                        r'Warning.*mysql_.*'
                    ]
                    
                    for pattern in error_patterns:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            self.log_vulnerability(
                                "HIGH",
                                f"Potential SQL injection vulnerability - SQL error exposed",
                                endpoint
                            )
                            break
                            
                except Exception as e:
                    logger.error(f"Error testing {endpoint}: {e}")
    
    def test_xss(self):
        """Test for Cross-Site Scripting vulnerabilities"""
        logger.info("Testing XSS...")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "';alert('XSS');//"
        ]
        
        # Test GET parameters
        for payload in xss_payloads:
            try:
                response = self.session.get(f"{self.base_url}/competence?category={payload}")
                if payload in response.text and 'text/html' in response.headers.get('content-type', ''):
                    self.log_vulnerability(
                        "HIGH",
                        f"Potential XSS vulnerability - payload reflected without encoding",
                        "/competence"
                    )
            except Exception as e:
                logger.error(f"Error testing XSS: {e}")
    
    def test_csrf(self):
        """Test for CSRF vulnerabilities"""
        logger.info("Testing CSRF...")
        
        # Test POST endpoints without CSRF tokens
        csrf_endpoints = [
            "/cocreation/save_concept",
            "/cocreation/send_email"
        ]
        
        for endpoint in csrf_endpoints:
            try:
                response = self.session.post(
                    urljoin(self.base_url, endpoint),
                    json={"test": "data"}
                )
                
                if response.status_code != 403:  # Should be forbidden without CSRF token
                    self.log_vulnerability(
                        "MEDIUM",
                        f"Potential CSRF vulnerability - no CSRF protection detected",
                        endpoint
                    )
            except Exception as e:
                logger.error(f"Error testing CSRF on {endpoint}: {e}")
    
    def test_information_disclosure(self):
        """Test for information disclosure"""
        logger.info("Testing information disclosure...")
        
        # Test debug mode
        try:
            response = self.session.get(f"{self.base_url}/nonexistent")
            if 'Traceback' in response.text or 'Debug mode' in response.text:
                self.log_vulnerability(
                    "MEDIUM",
                    "Debug mode enabled - stack traces exposed",
                    "/nonexistent"
                )
        except Exception as e:
            logger.error(f"Error testing debug mode: {e}")
        
        # Test for exposed files
        sensitive_files = [
            "/.env",
            "/config.py",
            "/app.py",
            "/requirements.txt",
            "/database.db"
        ]
        
        for file_path in sensitive_files:
            try:
                response = self.session.get(f"{self.base_url}{file_path}")
                if response.status_code == 200:
                    self.log_vulnerability(
                        "HIGH",
                        f"Sensitive file exposed",
                        file_path
                    )
            except Exception as e:
                logger.error(f"Error testing file exposure: {e}")
    
    def test_security_headers(self):
        """Test for security headers"""
        logger.info("Testing security headers...")
        
        try:
            response = self.session.get(self.base_url)
            headers = response.headers
            
            # Check for important security headers
            security_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                'Content-Security-Policy': 'default-src'
            }
            
            for header, expected in security_headers.items():
                if header not in headers:
                    self.log_vulnerability(
                        "MEDIUM",
                        f"Missing security header: {header}",
                        "/"
                    )
                elif expected not in headers[header]:
                    self.log_vulnerability(
                        "LOW",
                        f"Security header {header} may be misconfigured",
                        "/"
                    )
                    
        except Exception as e:
            logger.error(f"Error testing security headers: {e}")
    
    def test_file_upload_security(self):
        """Test file upload security"""
        logger.info("Testing file upload security...")
        
        # Test if file uploads are properly validated
        malicious_files = [
            ('test.php', b'<?php system($_GET["cmd"]); ?>'),
            ('test.jsp', b'<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>'),
            ('test.py', b'import os; os.system("whoami")'),
            ('test.exe', b'MZ\x90\x00'),  # PE header
        ]
        
        # Note: This would need actual file upload endpoints to test
        logger.info("File upload endpoints not found - manual testing required")
    
    def test_database_security(self):
        """Test database security"""
        logger.info("Testing database security...")
        
        db_path = "instance/bruggen_innovation.db"
        if os.path.exists(db_path):
            # Check database permissions
            stat = os.stat(db_path)
            permissions = oct(stat.st_mode)[-3:]
            
            if permissions != '600':
                self.log_vulnerability(
                    "MEDIUM",
                    f"Database file permissions too permissive: {permissions}",
                    db_path
                )
            
            # Test for default/weak credentials (not applicable to SQLite)
            logger.info("SQLite database - credential testing not applicable")
        else:
            logger.warning("Database file not found")
    
    def test_session_security(self):
        """Test session security"""
        logger.info("Testing session security...")
        
        try:
            response = self.session.get(self.base_url)
            
            # Check session cookie security
            for cookie in response.cookies:
                if not cookie.secure:
                    self.log_vulnerability(
                        "MEDIUM",
                        f"Session cookie not marked as secure",
                        "/"
                    )
                if not cookie.has_nonstandard_attr('HttpOnly'):
                    self.log_vulnerability(
                        "MEDIUM",
                        f"Session cookie not marked as HttpOnly",
                        "/"
                    )
                    
        except Exception as e:
            logger.error(f"Error testing session security: {e}")
    
    def run_all_tests(self):
        """Run all security tests"""
        logger.info("Starting comprehensive security testing...")
        
        test_methods = [
            self.test_sql_injection,
            self.test_xss,
            self.test_csrf,
            self.test_information_disclosure,
            self.test_security_headers,
            self.test_file_upload_security,
            self.test_database_security,
            self.test_session_security
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                logger.error(f"Error running {test_method.__name__}: {e}")
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate security test report"""
        logger.info("Generating security report...")
        
        print("\n" + "="*60)
        print("SECURITY TESTING REPORT")
        print("="*60)
        
        if not self.vulnerabilities:
            print("✅ No security vulnerabilities detected!")
            return
        
        severity_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for vuln in self.vulnerabilities:
            severity_counts[vuln['severity']] += 1
            
        print(f"\nSUMMARY:")
        print(f"High Risk: {severity_counts['HIGH']}")
        print(f"Medium Risk: {severity_counts['MEDIUM']}")
        print(f"Low Risk: {severity_counts['LOW']}")
        
        print(f"\nDETAILS:")
        for vuln in self.vulnerabilities:
            print(f"[{vuln['severity']}] {vuln['description']}")
            if vuln['endpoint']:
                print(f"    Endpoint: {vuln['endpoint']}")
            print()

if __name__ == "__main__":
    tester = SecurityTester()
    tester.run_all_tests()
