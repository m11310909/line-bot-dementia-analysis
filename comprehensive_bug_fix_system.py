#!/usr/bin/env python3
"""
Comprehensive Bug Fix System
Identifies and fixes all potential issues in the LINE Bot Dementia Analysis System
"""

import os
import sys
import json
import time
import subprocess
import requests
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class IssueSeverity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class SystemIssue:
    id: str
    severity: IssueSeverity
    description: str
    component: str
    fix_applied: bool = False
    fix_description: str = ""
    timestamp: str = ""

class ComprehensiveBugFixSystem:
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []
        self.system_status = {}
        self.start_time = datetime.now()
        
    def log_issue(self, issue_id: str, severity: IssueSeverity, description: str, component: str):
        """Log a system issue"""
        issue = SystemIssue(
            id=issue_id,
            severity=severity,
            description=description,
            component=component,
            timestamp=datetime.now().isoformat()
        )
        self.issues_found.append(issue)
        logger.warning(f"[{severity.value}] {component}: {description}")
    
    def log_fix(self, issue_id: str, fix_description: str):
        """Log a fix that was applied"""
        for issue in self.issues_found:
            if issue.id == issue_id:
                issue.fix_applied = True
                issue.fix_description = fix_description
                self.fixes_applied.append({
                    "issue_id": issue_id,
                    "fix_description": fix_description,
                    "timestamp": datetime.now().isoformat()
                })
                logger.info(f"✅ FIXED: {fix_description}")
                break
    
    def check_environment_variables(self) -> bool:
        """Check if all required environment variables are set"""
        logger.info("🔍 Checking environment variables...")
        
        required_vars = [
            "LINE_CHANNEL_ACCESS_TOKEN",
            "LINE_CHANNEL_SECRET",
            "GOOGLE_GEMINI_API_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.log_issue(
                "ENV_MISSING_VARS",
                IssueSeverity.CRITICAL,
                f"Missing environment variables: {', '.join(missing_vars)}",
                "Environment"
            )
            return False
        
        logger.info("✅ All required environment variables are set")
        return True
    
    def check_file_permissions(self) -> bool:
        """Check file permissions and accessibility"""
        logger.info("🔍 Checking file permissions...")
        
        critical_files = [
            "enhanced_m1_m2_m3_m4_integrated_api.py",
            "updated_line_bot_webhook.py",
            "persistent_system_monitor.py",
            ".env"
        ]
        
        permission_issues = []
        for file in critical_files:
            if os.path.exists(file):
                if not os.access(file, os.R_OK):
                    permission_issues.append(f"{file} (not readable)")
                if not os.access(file, os.W_OK):
                    permission_issues.append(f"{file} (not writable)")
            else:
                permission_issues.append(f"{file} (not found)")
        
        if permission_issues:
            self.log_issue(
                "FILE_PERMISSION_ISSUES",
                IssueSeverity.HIGH,
                f"File permission issues: {', '.join(permission_issues)}",
                "File System"
            )
            return False
        
        logger.info("✅ All file permissions are correct")
        return True
    
    def check_port_availability(self) -> bool:
        """Check if required ports are available"""
        logger.info("🔍 Checking port availability...")
        
        required_ports = [8005, 8081, 4040]
        port_issues = []
        
        for port in required_ports:
            try:
                import socket
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
            except OSError:
                port_issues.append(str(port))
        
        if port_issues:
            self.log_issue(
                "PORT_CONFLICTS",
                IssueSeverity.HIGH,
                f"Port conflicts detected: {', '.join(port_issues)}",
                "Network"
            )
            return False
        
        logger.info("✅ All required ports are available")
        return True
    
    def check_service_health(self) -> Dict[str, bool]:
        """Check health of all services"""
        logger.info("🔍 Checking service health...")
        
        services = {
            "RAG_API": "http://localhost:8005/health",
            "WEBHOOK_SERVER": "http://localhost:8081/health",
            "NGROK": "http://localhost:4040/api/tunnels"
        }
        
        health_status = {}
        
        for service_name, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    health_status[service_name] = True
                    logger.info(f"✅ {service_name}: Healthy")
                else:
                    health_status[service_name] = False
                    self.log_issue(
                        f"SERVICE_{service_name}_UNHEALTHY",
                        IssueSeverity.HIGH,
                        f"{service_name} returned status {response.status_code}",
                        service_name
                    )
            except Exception as e:
                health_status[service_name] = False
                self.log_issue(
                    f"SERVICE_{service_name}_DOWN",
                    IssueSeverity.CRITICAL,
                    f"{service_name} is not responding: {str(e)}",
                    service_name
                )
        
        return health_status
    
    def check_process_status(self) -> Dict[str, bool]:
        """Check if all required processes are running"""
        logger.info("🔍 Checking process status...")
        
        processes = [
            "enhanced_m1_m2_m3_m4_integrated_api.py",
            "updated_line_bot_webhook.py",
            "ngrok"
        ]
        
        process_status = {}
        
        for process in processes:
            try:
                result = subprocess.run(['pgrep', '-f', process], capture_output=True, text=True)
                if result.returncode == 0:
                    process_status[process] = True
                    logger.info(f"✅ {process}: Running")
                else:
                    process_status[process] = False
                    self.log_issue(
                        f"PROCESS_{process}_NOT_RUNNING",
                        IssueSeverity.CRITICAL,
                        f"Process {process} is not running",
                        "Process Management"
                    )
            except Exception as e:
                process_status[process] = False
                self.log_issue(
                    f"PROCESS_{process}_CHECK_FAILED",
                    IssueSeverity.HIGH,
                    f"Failed to check process {process}: {str(e)}",
                    "Process Management"
                )
        
        return process_status
    
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are installed"""
        logger.info("🔍 Checking dependencies...")
        
        required_packages = [
            "fastapi",
            "uvicorn",
            "requests",
            "python-dotenv",
            "google-generativeai",
            "pydantic"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.log_issue(
                "MISSING_DEPENDENCIES",
                IssueSeverity.CRITICAL,
                f"Missing packages: {', '.join(missing_packages)}",
                "Dependencies"
            )
            return False
        
        logger.info("✅ All required dependencies are installed")
        return True
    
    def check_disk_space(self) -> bool:
        """Check available disk space"""
        logger.info("🔍 Checking disk space...")
        
        try:
            import shutil
            total, used, free = shutil.disk_usage('.')
            free_gb = free // (1024**3)
            
            if free_gb < 1:  # Less than 1GB free
                self.log_issue(
                    "LOW_DISK_SPACE",
                    IssueSeverity.HIGH,
                    f"Low disk space: {free_gb}GB free",
                    "Storage"
                )
                return False
            
            logger.info(f"✅ Sufficient disk space: {free_gb}GB free")
            return True
        except Exception as e:
            self.log_issue(
                "DISK_SPACE_CHECK_FAILED",
                IssueSeverity.MEDIUM,
                f"Failed to check disk space: {str(e)}",
                "Storage"
            )
            return False
    
    def fix_environment_variables(self) -> bool:
        """Create .env file if missing"""
        logger.info("🔧 Fixing environment variables...")
        
        if not os.path.exists(".env"):
            env_content = """# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_CHANNEL_SECRET=your_channel_secret_here

# Google Gemini API
GOOGLE_GEMINI_API_KEY=your_gemini_api_key_here

# System Configuration
DEBUG=false
LOG_LEVEL=INFO
"""
            
            try:
                with open(".env", "w") as f:
                    f.write(env_content)
                
                self.log_fix(
                    "ENV_MISSING_VARS",
                    "Created .env file with template variables"
                )
                return True
            except Exception as e:
                logger.error(f"Failed to create .env file: {e}")
                return False
        
        return True
    
    def fix_port_conflicts(self) -> bool:
        """Kill processes using required ports"""
        logger.info("🔧 Fixing port conflicts...")
        
        ports_to_check = [8005, 8081, 4040]
        fixed = False
        
        for port in ports_to_check:
            try:
                # Find process using the port
                result = subprocess.run(
                    ['lsof', '-ti', f':{port}'],
                    capture_output=True, text=True
                )
                
                if result.stdout.strip():
                    pids = result.stdout.strip().split('\n')
                    for pid in pids:
                        if pid:
                            subprocess.run(['kill', '-9', pid])
                            logger.info(f"Killed process {pid} using port {port}")
                            fixed = True
            except Exception as e:
                logger.warning(f"Could not check port {port}: {e}")
        
        if fixed:
            self.log_fix(
                "PORT_CONFLICTS",
                "Killed processes using required ports"
            )
            time.sleep(2)  # Wait for ports to be freed
        
        return True
    
    def restart_services(self) -> bool:
        """Restart all services"""
        logger.info("🔧 Restarting services...")
        
        services = [
            ("enhanced_m1_m2_m3_m4_integrated_api.py", "RAG API"),
            ("updated_line_bot_webhook.py", "Webhook Server")
        ]
        
        success = True
        
        for script, name in services:
            try:
                # Kill existing process
                subprocess.run(['pkill', '-f', script], capture_output=True)
                time.sleep(2)
                
                # Start new process
                subprocess.Popen(['python3', script], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
                
                logger.info(f"✅ Restarted {name}")
                time.sleep(5)  # Wait for startup
                
            except Exception as e:
                logger.error(f"Failed to restart {name}: {e}")
                success = False
        
        if success:
            self.log_fix(
                "SERVICE_RESTART",
                "Restarted all services"
            )
        
        return success
    
    def install_missing_dependencies(self) -> bool:
        """Install missing dependencies"""
        logger.info("🔧 Installing missing dependencies...")
        
        try:
            subprocess.run([
                'pip3', 'install', 
                'fastapi', 'uvicorn', 'requests', 'python-dotenv',
                'google-generativeai', 'pydantic'
            ], check=True)
            
            self.log_fix(
                "MISSING_DEPENDENCIES",
                "Installed missing dependencies"
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def create_backup(self) -> bool:
        """Create backup of current system"""
        logger.info("💾 Creating system backup...")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"backup_{timestamp}"
            
            # Create backup directory
            os.makedirs(backup_dir, exist_ok=True)
            
            # Copy critical files
            critical_files = [
                "enhanced_m1_m2_m3_m4_integrated_api.py",
                "updated_line_bot_webhook.py",
                "persistent_system_monitor.py",
                ".env",
                "requirements.txt"
            ]
            
            for file in critical_files:
                if os.path.exists(file):
                    subprocess.run(['cp', file, backup_dir])
            
            logger.info(f"✅ Backup created: {backup_dir}")
            return True
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False
    
    def run_comprehensive_check(self) -> Dict[str, Any]:
        """Run comprehensive system check"""
        logger.info("🚀 Starting comprehensive system check...")
        
        # Create backup first
        self.create_backup()
        
        # Run all checks
        checks = {
            "environment": self.check_environment_variables(),
            "permissions": self.check_file_permissions(),
            "ports": self.check_port_availability(),
            "dependencies": self.check_dependencies(),
            "disk_space": self.check_disk_space()
        }
        
        # Check services
        service_health = self.check_service_health()
        process_status = self.check_process_status()
        
        # Apply fixes for critical issues
        if not checks["environment"]:
            self.fix_environment_variables()
        
        if not checks["ports"]:
            self.fix_port_conflicts()
        
        if not checks["dependencies"]:
            self.install_missing_dependencies()
        
        # Restart services if needed
        if not all(service_health.values()) or not all(process_status.values()):
            self.restart_services()
        
        # Final status
        self.system_status = {
            "checks": checks,
            "service_health": service_health,
            "process_status": process_status,
            "issues_found": len(self.issues_found),
            "fixes_applied": len(self.fixes_applied),
            "timestamp": datetime.now().isoformat()
        }
        
        return self.system_status
    
    def generate_report(self) -> str:
        """Generate comprehensive system report"""
        report = {
            "system_check_report": {
                "timestamp": datetime.now().isoformat(),
                "duration": (datetime.now() - self.start_time).total_seconds(),
                "issues_found": len(self.issues_found),
                "fixes_applied": len(self.fixes_applied),
                "system_status": self.system_status
            },
            "issues": [
                {
                    "id": issue.id,
                    "severity": issue.severity.value,
                    "description": issue.description,
                    "component": issue.component,
                    "fix_applied": issue.fix_applied,
                    "fix_description": issue.fix_description,
                    "timestamp": issue.timestamp
                }
                for issue in self.issues_found
            ],
            "fixes": self.fixes_applied
        }
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bug_fix_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def print_summary(self):
        """Print summary of the bug fix operation"""
        print("\n" + "="*60)
        print("🐛 COMPREHENSIVE BUG FIX SYSTEM SUMMARY")
        print("="*60)
        
        print(f"📊 Issues Found: {len(self.issues_found)}")
        print(f"🔧 Fixes Applied: {len(self.fixes_applied)}")
        print(f"⏱️  Duration: {(datetime.now() - self.start_time).total_seconds():.2f}s")
        
        if self.issues_found:
            print("\n🚨 ISSUES FOUND:")
            for issue in self.issues_found:
                status = "✅ FIXED" if issue.fix_applied else "❌ UNFIXED"
                print(f"  [{issue.severity.value}] {issue.component}: {issue.description} - {status}")
        
        if self.fixes_applied:
            print("\n🔧 FIXES APPLIED:")
            for fix in self.fixes_applied:
                print(f"  ✅ {fix['fix_description']}")
        
        print("\n📈 SYSTEM STATUS:")
        if self.system_status:
            for check, status in self.system_status.get("checks", {}).items():
                status_icon = "✅" if status else "❌"
                print(f"  {status_icon} {check.replace('_', ' ').title()}")
        
        print("="*60)

def main():
    """Main function"""
    print("🐛 COMPREHENSIVE BUG FIX SYSTEM")
    print("="*50)
    print("This system will identify and fix all potential issues")
    print("="*50)
    
    bug_fix_system = ComprehensiveBugFixSystem()
    
    try:
        # Run comprehensive check
        status = bug_fix_system.run_comprehensive_check()
        
        # Generate report
        report_file = bug_fix_system.generate_report()
        
        # Print summary
        bug_fix_system.print_summary()
        
        print(f"\n📄 Detailed report saved: {report_file}")
        print("✅ Bug fix system completed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Bug fix system interrupted by user")
    except Exception as e:
        logger.error(f"Bug fix system failed: {e}")
        print(f"❌ Bug fix system failed: {e}")

if __name__ == "__main__":
    main() 