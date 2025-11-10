#!/usr/bin/env python3
"""
Tourism Guide FastAPI - Setup Verification Script
This script checks if all required files and configurations are in place.
"""

import os
import sys
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def check_mark(condition):
    """Return checkmark or cross based on condition"""
    return f"{Colors.GREEN}✓{Colors.END}" if condition else f"{Colors.RED}✗{Colors.END}"

def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BLUE}{'='*50}")
    print(f"{text}")
    print(f"{'='*50}{Colors.END}\n")

def check_file(filepath, description):
    """Check if file exists"""
    exists = os.path.exists(filepath)
    status = check_mark(exists)
    status_text = f"{Colors.GREEN}Found{Colors.END}" if exists else f"{Colors.RED}Missing{Colors.END}"
    print(f"{status} {description:40} [{status_text}]")
    return exists

def check_directory(dirpath, description):
    """Check if directory exists"""
    exists = os.path.isdir(dirpath)
    status = check_mark(exists)
    status_text = f"{Colors.GREEN}Found{Colors.END}" if exists else f"{Colors.RED}Missing{Colors.END}"
    print(f"{status} {description:40} [{status_text}]")
    return exists

def check_python_package(package_name):
    """Check if Python package is installed"""
    try:
        __import__(package_name)
        status = f"{Colors.GREEN}✓{Colors.END}"
        status_text = f"{Colors.GREEN}Installed{Colors.END}"
    except ImportError:
        status = f"{Colors.RED}✗{Colors.END}"
        status_text = f"{Colors.RED}Missing{Colors.END}"
    
    print(f"{status} {package_name:40} [{status_text}]")
    return status == f"{Colors.GREEN}✓{Colors.END}"

def main():
    """Main verification function"""
    
    print(f"\n{Colors.BLUE}{'='*70}")
    print("TOURISM GUIDE FASTAPI - SETUP VERIFICATION")
    print(f"{'='*70}{Colors.END}\n")
    
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0
    }
    
    # Check root files
    print_header("1. ROOT FILES")
    files_to_check = [
        ('.env', '.env file'),
        ('requirements.txt', 'requirements.txt'),
        ('tourism_guide.sql', 'tourism_guide.sql'),
        ('README.md', 'README.md'),
        ('SETUP.bat', 'SETUP.bat'),
        ('RUN.bat', 'RUN.bat'),
    ]
    
    for filepath, desc in files_to_check:
        results['total'] += 1
        if check_file(filepath, desc):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Check directories
    print_header("2. DIRECTORY STRUCTURE")
    dirs_to_check = [
        ('app', 'app directory'),
        ('app/models', 'models directory'),
        ('app/schemas', 'schemas directory'),
        ('app/routers', 'routers directory'),
        ('app/services', 'services directory'),
        ('app/templates', 'templates directory'),
        ('app/templates/admin', 'admin templates directory'),
        ('app/static', 'static directory'),
        ('uploads', 'uploads directory'),
        ('uploads/destinations', 'destinations upload directory'),
        ('uploads/categories', 'categories upload directory'),
    ]
    
    for dirpath, desc in dirs_to_check:
        results['total'] += 1
        if check_directory(dirpath, desc):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Check app core files
    print_header("3. APP CORE FILES")
    core_files = [
        ('app/__init__.py', 'app/__init__.py'),
        ('app/main.py', 'app/main.py'),
        ('app/config.py', 'app/config.py'),
        ('app/database.py', 'app/database.py'),
        ('app/dependencies.py', 'app/dependencies.py'),
    ]
    
    for filepath, desc in core_files:
        results['total'] += 1
        if check_file(filepath, desc):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Check models
    print_header("4. MODELS")
    model_files = [
        ('app/models/__init__.py', 'models/__init__.py'),
        ('app/models/user.py', 'models/user.py'),
        ('app/models/destination.py', 'models/destination.py'),
        ('app/models/review.py', 'models/review.py'),
        ('app/models/route.py', 'models/route.py'),
    ]
    
    for filepath, desc in model_files:
        results['total'] += 1
        if check_file(filepath, desc):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Check routers
    print_header("5. ROUTERS")
    router_files = [
        ('app/routers/__init__.py', 'routers/__init__.py'),
        ('app/routers/auth.py', 'routers/auth.py'),
        ('app/routers/destinations.py', 'routers/destinations.py'),
        ('app/routers/reviews.py', 'routers/reviews.py'),
        ('app/routers/routes_api.py', 'routers/routes_api.py'),
        ('app/routers/feedback.py', 'routers/feedback.py'),
        ('app/routers/admin.py', 'routers/admin.py'),
    ]
    
    for filepath, desc in router_files:
        results['total'] += 1
        if check_file(filepath, desc):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Check templates
    print_header("6. TEMPLATES")
    template_files = [
        ('app/templates/base.html', 'base.html'),
        ('app/templates/index.html', 'index.html'),
        ('app/templates/login.html', 'login.html'),
        ('app/templates/destination.html', 'destination.html'),
        ('app/templates/feedback.html', 'feedback.html'),
        ('app/templates/admin/dashboard.html', 'admin/dashboard.html'),
        ('app/templates/admin/destinations.html', 'admin/destinations.html'),
        ('app/templates/admin/categories.html', 'admin/categories.html'),
        ('app/templates/admin/routes.html', 'admin/routes.html'),
        ('app/templates/admin/reviews.html', 'admin/reviews.html'),
        ('app/templates/admin/users.html', 'admin/users.html'),
    ]
    
    for filepath, desc in template_files:
        results['total'] += 1
        if check_file(filepath, desc):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Check Python packages (if venv is activated)
    print_header("7. PYTHON PACKAGES")
    packages_to_check = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pymysql',
        'pydantic',
        'jose',
        'passlib',
    ]
    
    for package in packages_to_check:
        results['total'] += 1
        if check_python_package(package):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Check .env configuration
    print_header("8. CONFIGURATION CHECK")
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
            
        checks = [
            ('DATABASE_URL' in env_content, 'DATABASE_URL configured'),
            ('SECRET_KEY' in env_content, 'SECRET_KEY configured'),
            ('ALGORITHM' in env_content, 'ALGORITHM configured'),
        ]
        
        for condition, desc in checks:
            results['total'] += 1
            status = check_mark(condition)
            status_text = f"{Colors.GREEN}OK{Colors.END}" if condition else f"{Colors.YELLOW}Warning{Colors.END}"
            print(f"{status} {desc:40} [{status_text}]")
            if condition:
                results['passed'] += 1
            else:
                results['failed'] += 1
    else:
        print(f"{Colors.YELLOW}⚠ .env file not found - using default configuration{Colors.END}")
    
    # Print summary
    print_header("VERIFICATION SUMMARY")
    
    percentage = (results['passed'] / results['total']) * 100 if results['total'] > 0 else 0
    
    print(f"Total Checks: {results['total']}")
    print(f"{Colors.GREEN}Passed: {results['passed']}{Colors.END}")
    print(f"{Colors.RED}Failed: {results['failed']}{Colors.END}")
    print(f"\nCompletion: {percentage:.1f}%")
    
    if percentage == 100:
        print(f"\n{Colors.GREEN}{'='*50}")
        print("✓ ALL CHECKS PASSED!")
        print("Your system is ready to run!")
        print(f"{'='*50}{Colors.END}\n")
        print("Next steps:")
        print("1. Start MySQL in XAMPP")
        print("2. Import tourism_guide.sql to phpMyAdmin")
        print("3. Run: uvicorn app.main:app --reload")
        print("4. Visit: http://localhost:8000\n")
        return 0
    elif percentage >= 80:
        print(f"\n{Colors.YELLOW}{'='*50}")
        print("⚠ MOSTLY COMPLETE")
        print("Your system should work, but some files are missing.")
        print(f"{'='*50}{Colors.END}\n")
        print("Check the failed items above and add the missing files.\n")
        return 0
    else:
        print(f"\n{Colors.RED}{'='*50}")
        print("✗ SETUP INCOMPLETE")
        print("Many required files are missing.")
        print(f"{'='*50}{Colors.END}\n")
        print("Please run SETUP.bat or manually create missing files.\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())