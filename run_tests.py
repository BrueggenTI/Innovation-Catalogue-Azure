
#!/usr/bin/env python3
"""
Comprehensive test runner for Brüggen Innovation Catalogue
"""

import subprocess
import sys
import time
import os
from multiprocessing import Process
import signal

def start_server():
    """Start the Flask development server"""
    print("Starting Flask server...")
    return subprocess.Popen([
        sys.executable, 'main.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def wait_for_server(server_process, url="http://localhost:5000", timeout=30):
    """Wait for server to be ready"""
    import requests
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Server is ready!")
                return True
        except requests.ConnectionError:
            pass
        time.sleep(1)
    
    print("Server failed to start within timeout")
    # Print server output for debugging
    stdout, stderr = server_process.communicate()
    print("SERVER STDOUT:")
    print(stdout.decode() if stdout else "N/A")
    print("SERVER STDERR:")
    print(stderr.decode() if stderr else "N/A")
    return False

def run_functional_tests():
    """Run functional tests"""
    print("\n" + "="*60)
    print("RUNNING FUNCTIONAL TESTS")
    print("="*60)
    
    try:
        result = subprocess.run([sys.executable, 'functional_test.py'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running functional tests: {e}")
        return False

def run_security_tests():
    """Run security tests"""
    print("\n" + "="*60)
    print("RUNNING SECURITY TESTS")
    print("="*60)
    
    try:
        result = subprocess.run([sys.executable, 'security_test.py'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running security tests: {e}")
        return False

def main():
    """Main test execution"""
    print("Brüggen Innovation Catalogue - Comprehensive Testing")
    print("="*60)
    
    # Start server
    server_process = start_server()
    
    try:
        # Wait for server to start
        if not wait_for_server(server_process):
            print("Failed to start server, exiting...")
            return 1
        
        # Run tests
        functional_passed = run_functional_tests()
        security_passed = run_security_tests()
        
        # Summary
        print("\n" + "="*60)
        print("TESTING SUMMARY")
        print("="*60)
        
        print(f"Functional Tests: {'✅ PASSED' if functional_passed else '❌ FAILED'}")
        print(f"Security Tests: {'✅ PASSED' if security_passed else '❌ FAILED'}")
        
        if functional_passed and security_passed:
            print("\n🎉 ALL TESTS PASSED!")
            return 0
        else:
            print("\n⚠️  SOME TESTS FAILED - Review output above")
            return 1
            
    finally:
        # Clean up server
        print("\nStopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    sys.exit(main())
