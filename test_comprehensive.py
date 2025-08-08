#!/usr/bin/env python3
"""
Comprehensive LINE Bot Testing Script
Tests all aspects of the system including webhook, API, and service health
"""

import requests
import json
import time
from datetime import datetime


def test_health_endpoints():
    """Test all health endpoints"""
    print("🔍 Testing Health Endpoints...")

    endpoints = [
        ("External Health", "https://6f59006e1132.ngrok-free.app/health"),
        ("LINE Bot Health", "http://localhost:8081/health"),
        ("XAI Wrapper Health", "http://localhost:8005/health"),
    ]

    results = {}
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=10)
            status = "✅ PASS" if response.status_code == 200 else "❌ FAIL"
            results[name] = {
                "status": status,
                "code": response.status_code,
                "response": response.text[:100],
            }
            print(f"  {name}: {status} ({response.status_code})")
        except Exception as e:
            results[name] = {"status": "❌ ERROR", "error": str(e)}
            print(f"  {name}: ❌ ERROR - {e}")

    return results


def test_webhook_endpoint():
    """Test webhook endpoint with various scenarios"""
    print("\n🔍 Testing Webhook Endpoint...")

    base_url = "https://6f59006e1132.ngrok-free.app/webhook"

    # Test 1: Basic webhook call
    test_data = {
        "events": [
            {
                "type": "message",
                "message": {"type": "text", "text": "我最近常常忘記事情"},
                "replyToken": "test_reply_token_1",
                "source": {"userId": "test_user_1", "type": "user"},
            }
        ]
    }

    try:
        response = requests.post(
            base_url,
            headers={
                "Content-Type": "application/json",
                "X-Line-Signature": "test_signature",
            },
            json=test_data,
            timeout=10,
        )

        print(f"  Basic Webhook: ✅ PASS ({response.status_code})")
        if response.status_code == 200:
            print(f"    Response: {response.text[:100]}")
        return response.status_code == 200
    except Exception as e:
        print(f"  Basic Webhook: ❌ ERROR - {e}")
        return False


def test_api_endpoint():
    """Test API endpoint"""
    print("\n🔍 Testing API Endpoint...")

    test_data = {"user_input": "我最近常常忘記事情", "user_id": "test_user"}

    try:
        response = requests.post(
            "https://6f59006e1132.ngrok-free.app/api/v1/analyze",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=10,
        )

        print(f"  API Test: ✅ PASS ({response.status_code})")
        if response.status_code == 200:
            print(f"    Response: {response.text[:200]}")
        return response.status_code == 200
    except Exception as e:
        print(f"  API Test: ❌ ERROR - {e}")
        return False


def test_docker_services():
    """Test Docker services status"""
    print("\n🔍 Testing Docker Services...")

    import subprocess

    try:
        result = subprocess.run(
            ["docker-compose", "ps"], capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0:
            lines = result.stdout.split("\n")
            healthy_services = 0
            total_services = 0

            for line in lines:
                if "healthy" in line.lower():
                    healthy_services += 1
                if (
                    "line-bot" in line
                    or "xai-wrapper" in line
                    or "postgres" in line
                    or "redis" in line
                ):
                    total_services += 1

            print(f"  Docker Services: ✅ {healthy_services}/{total_services} healthy")
            return healthy_services >= 4  # At least 4 main services should be healthy
        else:
            print(f"  Docker Services: ❌ ERROR - {result.stderr}")
            return False
    except Exception as e:
        print(f"  Docker Services: ❌ ERROR - {e}")
        return False


def test_ngrok_tunnel():
    """Test ngrok tunnel status"""
    print("\n🔍 Testing ngrok Tunnel...")

    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json()
            if tunnels.get("tunnels"):
                tunnel = tunnels["tunnels"][0]
                url = tunnel.get("public_url", "")
                print(f"  ngrok Tunnel: ✅ ACTIVE - {url}")
                return True
            else:
                print("  ngrok Tunnel: ❌ NO TUNNELS")
                return False
        else:
            print(f"  ngrok Tunnel: ❌ ERROR - {response.status_code}")
            return False
    except Exception as e:
        print(f"  ngrok Tunnel: ❌ ERROR - {e}")
        return False


def test_line_bot_features():
    """Test LINE Bot specific features"""
    print("\n🔍 Testing LINE Bot Features...")

    # Test 1: Webhook URL endpoint
    try:
        response = requests.get("http://localhost:8081/webhook-url", timeout=5)
        if response.status_code == 200:
            data = response.json()
            webhook_url = data.get("webhook_url", "")
            print(f"  Webhook URL: ✅ {webhook_url}")
        else:
            print(f"  Webhook URL: ❌ ERROR - {response.status_code}")
    except Exception as e:
        print(f"  Webhook URL: ❌ ERROR - {e}")

    # Test 2: Root endpoint
    try:
        response = requests.get("http://localhost:8081/", timeout=5)
        if response.status_code == 200:
            print("  Root Endpoint: ✅ PASS")
        else:
            print(f"  Root Endpoint: ❌ ERROR - {response.status_code}")
    except Exception as e:
        print(f"  Root Endpoint: ❌ ERROR - {e}")


def run_comprehensive_test():
    """Run all comprehensive tests"""
    print("🧪 COMPREHENSIVE LINE BOT TESTING")
    print("=" * 50)

    # Run all tests
    health_results = test_health_endpoints()
    webhook_ok = test_webhook_endpoint()
    api_ok = test_api_endpoint()
    docker_ok = test_docker_services()
    ngrok_ok = test_ngrok_tunnel()
    test_line_bot_features()

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)

    tests = [
        (
            "Health Endpoints",
            all(r.get("status", "").startswith("✅") for r in health_results.values()),
        ),
        ("Webhook Endpoint", webhook_ok),
        ("API Endpoint", api_ok),
        ("Docker Services", docker_ok),
        ("ngrok Tunnel", ngrok_ok),
    ]

    passed = 0
    total = len(tests)

    for test_name, passed_test in tests:
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{test_name}: {status}")
        if passed_test:
            passed += 1

    print("\n" + "=" * 50)
    print(f"OVERALL RESULT: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Your LINE Bot is ready for real testing!")
        print("\n📋 Next Steps:")
        print("1. Update .env file with real LINE Bot credentials")
        print("2. Configure webhook URL in LINE Developer Console")
        print("3. Test with your actual LINE Bot")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")

    return passed == total


if __name__ == "__main__":
    run_comprehensive_test()
