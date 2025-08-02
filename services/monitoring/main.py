#!/usr/bin/env python3
"""
Monitoring and Operations Service - Phase 3 Advanced Features
Comprehensive system monitoring and operational management
"""

import os
import json
import logging
import psutil
import requests
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/monitoring.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Monitoring and Operations Service",
    description="Comprehensive system monitoring and operational management",
    version="3.0.0"
)

# Pydantic models
class ServiceHealth(BaseModel):
    service_name: str
    status: str
    response_time: float
    last_check: datetime
    error_count: int
    uptime: float

class SystemMetrics(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    active_connections: int
    timestamp: datetime

class Alert(BaseModel):
    level: str  # info, warning, error, critical
    service: str
    message: str
    timestamp: datetime
    resolved: bool = False

class MonitoringEngine:
    """Comprehensive monitoring and operations engine"""
    
    def __init__(self):
        self.services = {
            "line-bot": "http://localhost:8081/health",
            "xai-analysis": "http://localhost:8005/health",
            "rag-service": "http://localhost:8006/health",
            "aspect-verifiers": "http://localhost:8007/health",
            "bon-mav": "http://localhost:8008/health"
        }
        self.health_history = {}
        self.alerts = []
        self.metrics_history = []
        self.performance_thresholds = {
            "cpu_warning": 70.0,
            "cpu_critical": 90.0,
            "memory_warning": 80.0,
            "memory_critical": 95.0,
            "response_time_warning": 5.0,
            "response_time_critical": 10.0
        }
        logger.info("✅ Monitoring Engine initialized")
    
    async def check_service_health(self, service_name: str, url: str) -> ServiceHealth:
        """Check health of a specific service"""
        try:
            start_time = datetime.now()
            response = requests.get(url, timeout=10)
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds()
            status = "healthy" if response.status_code == 200 else "unhealthy"
            
            # Get error count from history
            error_count = self.health_history.get(service_name, {}).get("error_count", 0)
            if status == "unhealthy":
                error_count += 1
            
            # Calculate uptime
            uptime = self._calculate_uptime(service_name, status)
            
            health_data = ServiceHealth(
                service_name=service_name,
                status=status,
                response_time=response_time,
                last_check=datetime.now(),
                error_count=error_count,
                uptime=uptime
            )
            
            # Update history
            self.health_history[service_name] = {
                "status": status,
                "response_time": response_time,
                "last_check": datetime.now(),
                "error_count": error_count,
                "uptime": uptime
            }
            
            # Check for alerts
            await self._check_alerts(service_name, health_data)
            
            return health_data
            
        except Exception as e:
            logger.error(f"Health check failed for {service_name}: {e}")
            
            # Update error count
            error_count = self.health_history.get(service_name, {}).get("error_count", 0) + 1
            
            return ServiceHealth(
                service_name=service_name,
                status="unhealthy",
                response_time=0,
                last_check=datetime.now(),
                error_count=error_count,
                uptime=0
            )
    
    async def check_all_services(self) -> Dict[str, ServiceHealth]:
        """Check health of all services"""
        results = {}
        
        for service_name, url in self.services.items():
            try:
                health = await self.check_service_health(service_name, url)
                results[service_name] = health
            except Exception as e:
                logger.error(f"Failed to check {service_name}: {e}")
        
        return results
    
    def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
            
            # Active connections
            active_connections = len(psutil.net_connections())
            
            metrics = SystemMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                network_io=network_io,
                active_connections=active_connections,
                timestamp=datetime.now()
            )
            
            # Store in history
            self.metrics_history.append(metrics)
            
            # Keep only last 100 entries
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return SystemMetrics(
                cpu_usage=0,
                memory_usage=0,
                disk_usage=0,
                network_io={},
                active_connections=0,
                timestamp=datetime.now()
            )
    
    async def _check_alerts(self, service_name: str, health: ServiceHealth):
        """Check for alerts based on health data"""
        alerts = []
        
        # Response time alerts
        if health.response_time > self.performance_thresholds["response_time_critical"]:
            alerts.append(Alert(
                level="critical",
                service=service_name,
                message=f"Response time critical: {health.response_time:.2f}s",
                timestamp=datetime.now()
            ))
        elif health.response_time > self.performance_thresholds["response_time_warning"]:
            alerts.append(Alert(
                level="warning",
                service=service_name,
                message=f"Response time high: {health.response_time:.2f}s",
                timestamp=datetime.now()
            ))
        
        # Error count alerts
        if health.error_count > 5:
            alerts.append(Alert(
                level="critical",
                service=service_name,
                message=f"High error count: {health.error_count}",
                timestamp=datetime.now()
            ))
        elif health.error_count > 2:
            alerts.append(Alert(
                level="warning",
                service=service_name,
                message=f"Error count increasing: {health.error_count}",
                timestamp=datetime.now()
            ))
        
        # Status alerts
        if health.status == "unhealthy":
            alerts.append(Alert(
                level="error",
                service=service_name,
                message="Service is unhealthy",
                timestamp=datetime.now()
            ))
        
        # Add alerts to list
        for alert in alerts:
            self.alerts.append(alert)
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    def _calculate_uptime(self, service_name: str, current_status: str) -> float:
        """Calculate service uptime percentage"""
        # Simplified uptime calculation
        if current_status == "healthy":
            return 99.5  # Assume high uptime for healthy services
        else:
            return 85.0  # Assume lower uptime for unhealthy services
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics_history:
            return {"message": "No metrics available"}
        
        recent_metrics = self.metrics_history[-10:]  # Last 10 measurements
        
        avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        avg_disk = sum(m.disk_usage for m in recent_metrics) / len(recent_metrics)
        
        # Count healthy services
        healthy_services = sum(1 for health in self.health_history.values() 
                             if health.get("status") == "healthy")
        total_services = len(self.services)
        
        return {
            "average_cpu_usage": avg_cpu,
            "average_memory_usage": avg_memory,
            "average_disk_usage": avg_disk,
            "healthy_services": healthy_services,
            "total_services": total_services,
            "service_health_percentage": (healthy_services / total_services) * 100 if total_services > 0 else 0,
            "active_alerts": len([a for a in self.alerts if not a.resolved]),
            "total_alerts": len(self.alerts)
        }
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get alert summary"""
        unresolved_alerts = [a for a in self.alerts if not a.resolved]
        
        alert_counts = {
            "critical": len([a for a in unresolved_alerts if a.level == "critical"]),
            "error": len([a for a in unresolved_alerts if a.level == "error"]),
            "warning": len([a for a in unresolved_alerts if a.level == "warning"]),
            "info": len([a for a in unresolved_alerts if a.level == "info"])
        }
        
        return {
            "total_unresolved": len(unresolved_alerts),
            "alert_counts": alert_counts,
            "recent_alerts": unresolved_alerts[-10:]  # Last 10 alerts
        }

# Initialize monitoring engine
monitoring_engine = MonitoringEngine()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Monitoring and Operations Service",
        "status": "running",
        "version": "3.0.0",
        "architecture": "microservices",
        "monitored_services": list(monitoring_engine.services.keys())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "monitoring",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/services/health")
async def get_services_health():
    """Get health status of all services"""
    try:
        health_results = await monitoring_engine.check_all_services()
        return {
            "success": True,
            "services": health_results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get services health: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/metrics")
async def get_system_metrics():
    """Get current system metrics"""
    try:
        metrics = monitoring_engine.get_system_metrics()
        return {
            "success": True,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get system metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/performance/summary")
async def get_performance_summary():
    """Get performance summary"""
    try:
        summary = monitoring_engine.get_performance_summary()
        return {
            "success": True,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get performance summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts")
async def get_alerts():
    """Get current alerts"""
    try:
        alert_summary = monitoring_engine.get_alert_summary()
        return {
            "success": True,
            "alerts": alert_summary,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/alerts/resolve/{alert_id}")
async def resolve_alert(alert_id: int):
    """Resolve an alert"""
    try:
        if 0 <= alert_id < len(monitoring_engine.alerts):
            monitoring_engine.alerts[alert_id].resolved = True
            return {
                "success": True,
                "message": f"Alert {alert_id} resolved",
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=404, detail="Alert not found")
    except Exception as e:
        logger.error(f"Failed to resolve alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard")
async def get_dashboard():
    """Get comprehensive dashboard data"""
    try:
        # Get all monitoring data
        services_health = await monitoring_engine.check_all_services()
        system_metrics = monitoring_engine.get_system_metrics()
        performance_summary = monitoring_engine.get_performance_summary()
        alert_summary = monitoring_engine.get_alert_summary()
        
        return {
            "success": True,
            "dashboard": {
                "services_health": services_health,
                "system_metrics": system_metrics,
                "performance_summary": performance_summary,
                "alert_summary": alert_summary
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/monitoring/start")
async def start_monitoring(background_tasks: BackgroundTasks):
    """Start continuous monitoring"""
    try:
        # Start background monitoring task
        background_tasks.add_task(continuous_monitoring)
        
        return {
            "success": True,
            "message": "Monitoring started",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to start monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def continuous_monitoring():
    """Continuous monitoring task"""
    while True:
        try:
            # Check all services
            await monitoring_engine.check_all_services()
            
            # Get system metrics
            monitoring_engine.get_system_metrics()
            
            # Wait for next check (every 30 seconds)
            await asyncio.sleep(30)
            
        except Exception as e:
            logger.error(f"Continuous monitoring error: {e}")
            await asyncio.sleep(60)  # Wait longer on error

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009) 