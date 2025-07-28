                # integration_testing_suite.py
                """
                完整的整合測試套件
                驗證 M1 MVP + RAG 整合是否成功
                """

                import requests
                import json
                import time
                import os
                from typing import Dict, List
                from datetime import datetime

                class M1RAGIntegrationTester:
                    def __init__(self, base_url: str = "http://localhost:8001"):
                        self.base_url = base_url
                        self.session = requests.Session()
                        self.test_results = []

                    def log_test(self, test_name: str, success: bool, details: Dict = None):
                        """記錄測試結果"""
                        result = {
                            "test_name": test_name,
                            "success": success,
                            "timestamp": datetime.now().isoformat(),
                            "details": details or {}
                        }
                        self.test_results.append(result)

                        status = "✅" if success else "❌"
                        print(f"{status} {test_name}")
                        if details and not success:
                            print(f"   錯誤: {details.get('error', 'Unknown error')}")

                    def test_health_check(self) -> bool:
                        """測試系統健康狀況"""
                        print("\n🔍 測試系統健康狀況...")

                        try:
                            response = self.session.get(f"{self.base_url}/health", timeout=10)

                            if response.status_code == 200:
                                data = response.json()
                                components = data.get("components", {})

                                # 檢查關鍵組件
                                all_ready = (
                                    components.get("rag_engine") == "ready" and
                                    components.get("vector_index") == "ready" and
                                    components.get("chunks_loaded", 0) > 0
                                )

                                self.log_test("健康檢查", all_ready, {
                                    "components": components,
                                    "chunks_count": components.get("chunks_loaded", 0)
                                })

                                return all_ready
                            else:
                                self.log_test("健康檢查", False, {"error": f"HTTP {response.status_code}"})
                                return False

                        except Exception as e:
                            self.log_test("健康檢查", False, {"error": str(e)})
                            return False

                    def test_classic_m1_flex_api(self) -> bool:
                        """測試原有的 M1 Flex API（保持向後相容）"""
                        print("\n🤖 測試經典 M1 Flex API...")

                        test_cases = [
                            {
                                "input": "媽媽最近常忘記關瓦斯",
                                "expected_keywords": ["記憶", "忘記", "日常"]
                            },
                            {
                                "input": "爸爸開車會迷路",
                                "expected_keywords": ["方向", "地點", "空間"]
                            },
                            {
                                "input": "奶奶重複問同樣問題",
                                "expected_keywords": ["記憶", "重複", "問題"]
                            }
                        ]

                        all_passed = True

                        for i, test_case in enumerate(test_cases, 1):
                            try:
                                payload = {
                                    "user_input": test_case["input"],
                                    "analysis_mode": "enhanced"
                                }

                                start_time = time.time()
                                response = self.session.post(
                                    f"{self.base_url}/m1-flex",
                                    json=payload,
                                    timeout=30
                                )
                                response_time = time.time() - start_time

                                if response.status_code == 200:
                                    data = response.json()

                                    # 檢查回應結構
                                    has_flex = "flex_message" in data
                                    has_analysis = "analysis_data" in data
                                    has_enhancement = data.get("enhanced", False)

                                    success = has_flex and has_analysis and has_enhancement

                                    self.log_test(f"M1 Flex API - 測試 {i}", success, {
                                        "input": test_case["input"],
                                        "response_time": round(response_time, 2),
                                        "has_flex_message": has_flex,
                                        "has_analysis_data": has_analysis,
                                        "rag_enhanced": has_enhancement,
                                        "warning_code": data.get("analysis_data", {}).get("matched_warning_code")
                                    })

                                    if not success:
                                        all_passed = False

                                else:
                                    self.log_test(f"M1 Flex API - 測試 {i}", False, {
                                        "error": f"HTTP {response.status_code}",
                                        "response": response.text[:200]
                                    })
                                    all_passed = False

                            except Exception as e:
                                self.log_test(f"M1 Flex API - 測試 {i}", False, {"error": str(e)})
                                all_passed = False

                        return all_passed

                    def test_rag_retrieval(self) -> bool:
                        """測試 RAG 檢索功能"""
                        print("\n🔍 測試 RAG 檢索功能...")

                        test_queries = [
                            "記憶力問題",
                            "迷路",
                            "重複詢問",
                            "忘記事情",
                            "計劃困難"
                        ]

                        all_passed = True

                        for query in test_queries:
                            try:
                                response = self.session.get(
                                    f"{self.base_url}/api/v1/search",
                                    params={"q": query, "k": 3},
                                    timeout=10
                                )

                                if response.status_code == 200:
                                    data = response.json()
                                    chunks = data.get("chunks", [])

                                    # 檢查檢索品質
                                    has_results = len(chunks) > 0
                                    has_similarity = all(chunk.get("similarity_score", 0) > 0 for chunk in chunks)

                                    success = has_results and has_similarity

                                    self.log_test(f"RAG 檢索 - {query}", success, {
                                        "query": query,
                                        "results_count": len(chunks),
                                        "top_similarity": chunks[0].get("similarity_score", 0) if chunks else 0,
                                        "top_title": chunks[0].get("title", "") if chunks else ""
                                    })

                                    if not success:
                                        all_passed = False

                                else:
                                    self.log_test(f"RAG 檢索 - {query}", False, {
                                        "error": f"HTTP {response.status_code}"
                                    })
                                    all_passed = False

                            except Exception as e:
                                self.log_test(f"RAG 檢索 - {query}", False, {"error": str(e)})
                                all_passed = False

                        return all_passed

                    def test_unified_analyze_api(self) -> bool:
                        """測試統一分析 API"""
                        print("\n🧠 測試統一分析 API...")

                        try:
                            payload = {
                                "query": "我媽媽最近常常忘記關瓦斯爐，這正常嗎？",
                                "module_filter": "M1",
                                "k": 3
                            }

                            response = self.session.post(
                                f"{self.base_url}/api/v1/analyze",
                                json=payload,
                                timeout=30
                            )

                            if response.status_code == 200:
                                data = response.json()

                                # 檢查回應完整性
                                has_analysis = "analysis" in data
                                has_chunks = "retrieved_chunks" in data
                                chunks_count = len(data.get("retrieved_chunks", []))

                                success = has_analysis and has_chunks and chunks_count > 0

                                self.log_test("統一分析 API", success, {
                                    "has_analysis": has_analysis,
                                    "has_chunks": has_chunks,
                                    "chunks_retrieved": chunks_count,
                                    "warning_code": data.get("analysis", {}).get("matched_warning_code")
                                })

                                return success
                            else:
                                self.log_test("統一分析 API", False, {
                                    "error": f"HTTP {response.status_code}"
                                })
                                return False

                        except Exception as e:
                            self.log_test("統一分析 API", False, {"error": str(e)})
                            return False

                    def test_flex_message_generation(self) -> bool:
                        """測試 Flex Message 生成"""
                        print("\n📱 測試 Flex Message 生成...")

                        try:
                            payload = {
                                "user_input": "爸爸開車時經常迷路",
                                "return_format": "flex"
                            }

                            response = self.session.post(
                                f"{self.base_url}/api/v1/flex-message",
                                json=payload,
                                timeout=20
                            )

                            if response.status_code == 200:
                                data = response.json()

                                # 檢查 Flex Message 結構
                                flex_message = data.get("flex_message", {})
                                has_valid_structure = (
                                    flex_message.get("type") == "flex" and
                                    "contents" in flex_message and
                                    "altText" in flex_message
                                )

                                # 檢查分析資料
                                analysis_data = data.get("analysis_data", {})
                                has_analysis = "matched_warning_code" in analysis_data

                                # 檢查 metadata
                                metadata = data.get("metadata", {})
                                is_rag_enhanced = metadata.get("rag_enhanced", False)

                                success = has_valid_structure and has_analysis and is_rag_enhanced

                                self.log_test("Flex Message 生成", success, {
                                    "valid_flex_structure": has_valid_structure,
                                    "has_analysis_data": has_analysis,
                                    "rag_enhanced": is_rag_enhanced,
                                    "chunks_used": metadata.get("chunks_used", 0)
                                })

                                return success
                            else:
                                self.log_test("Flex Message 生成", False, {
                                    "error": f"HTTP {response.status_code}"
                                })
                                return False

                        except Exception as e:
                            self.log_test("Flex Message 生成", False, {"error": str(e)})
                            return False

                    def test_performance_benchmarks(self) -> bool:
                        """測試效能基準"""
                        print("\n⚡ 測試效能基準...")

                        # 測試回應時間
                        test_inputs = [
                            "記憶力衰退",
                            "計劃困難", 
                            "迷路問題"
                        ]

                        response_times = []
                        all_passed = True

                        for test_input in test_inputs:
                            try:
                                start_time = time.time()

                                response = self.session.post(
                                    f"{self.base_url}/m1-flex",
                                    json={"user_input": test_input},
                                    timeout=15
                                )

                                response_time = time.time() - start_time
                                response_times.append(response_time)

                                # 檢查回應時間（應該在 10 秒內）
                                time_ok = response_time < 10.0
                                status_ok = response.status_code == 200

                                success = time_ok and status_ok

                                self.log_test(f"效能測試 - {test_input}", success, {
                                    "response_time": round(response_time, 2),
                                    "status_code": response.status_code,
                                    "time_threshold": "< 10s"
                                })

                                if not success:
                                    all_passed = False

                            except Exception as e:
                                self.log_test(f"效能測試 - {test_input}", False, {"error": str(e)})
                                all_passed = False

                        # 計算平均回應時間
                        if response_times:
                            avg_time = sum(response_times) / len(response_times)
                            self.log_test("平均回應時間", avg_time < 5.0, {
                                "average_time": round(avg_time, 2),
                                "target": "< 5s"
                            })

                        return all_passed

                    def test_error_handling(self) -> bool:
                        """測試錯誤處理機制"""
                        print("\n🛡️ 測試錯誤處理...")

                        error_test_cases = [
                            {
                                "name": "空輸入",
                                "payload": {"user_input": ""},
                                "expected_graceful": True
                            },
                            {
                                "name": "超長輸入",
                                "payload": {"user_input": "A" * 2000},
                                "expected_graceful": True
                            },
                            {
                                "name": "特殊字元",
                                "payload": {"user_input": "!@#$%^&*()"},
                                "expected_graceful": True
                            }
                        ]

                        all_passed = True

                        for test_case in error_test_cases:
                            try:
                                response = self.session.post(
                                    f"{self.base_url}/m1-flex",
                                    json=test_case["payload"],
                                    timeout=10
                                )

                                # 檢查是否優雅處理錯誤（不應該 500 錯誤）
                                graceful_handling = response.status_code != 500

                                success = graceful_handling if test_case["expected_graceful"] else not graceful_handling

                                self.log_test(f"錯誤處理 - {test_case['name']}", success, {
                                    "status_code": response.status_code,
                                    "graceful_handling": graceful_handling
                                })

                                if not success:
                                    all_passed = False

                            except Exception as e:
                                # 連接錯誤也算作處理失敗
                                self.log_test(f"錯誤處理 - {test_case['name']}", False, {"error": str(e)})
                                all_passed = False

                        return all_passed

                    def run_full_test_suite(self) -> Dict:
                        """執行完整測試套件"""
                        print("🧪 開始執行完整整合測試套件")
                        print("=" * 60)

                        test_start_time = time.time()

                        # 執行所有測試
                        tests = [
                            ("系統健康檢查", self.test_health_check),
                            ("經典 M1 Flex API", self.test_classic_m1_flex_api),
                            ("RAG 檢索功能", self.test_rag_retrieval),
                            ("統一分析 API", self.test_unified_analyze_api),
                            ("Flex Message 生成", self.test_flex_message_generation),
                            ("效能基準測試", self.test_performance_benchmarks),
                            ("錯誤處理機制", self.test_error_handling)
                        ]

                        passed_tests = 0
                        total_tests = len(tests)

                        for test_name, test_func in tests:
                            try:
                                result = test_func()
                                if result:
                                    passed_tests += 1
                            except Exception as e:
                                print(f"❌ {test_name} 執行失敗: {e}")

                        test_duration = time.time() - test_start_time

                        # 生成測試報告
                        report = {
                            "timestamp": datetime.now().isoformat(),
                            "duration_seconds": round(test_duration, 2),
                            "summary": {
                                "total_tests": total_tests,
                                "passed_tests": passed_tests,
                                "failed_tests": total_tests - passed_tests,
                                "pass_rate": round(passed_tests / total_tests * 100, 1)
                            },
                            "detailed_results": self.test_results,
                            "overall_status": "PASS" if passed_tests == total_tests else "FAIL"
                        }

                        # 顯示摘要
                        print("\n" + "=" * 60)
                        print("📊 測試結果摘要:")
                        print(f"   總測試數: {total_tests}")
                        print(f"   通過測試: {passed_tests}")
                        print(f"   失敗測試: {total_tests - passed_tests}")
                        print(f"   通過率: {report['summary']['pass_rate']}%")
                        print(f"   測試時間: {test_duration:.2f} 秒")
                        print(f"   整體狀態: {report['overall_status']}")

                        # 儲存詳細報告
                        with open("integration_test_report.json", "w", encoding="utf-8") as f:
                            json.dump(report, f, ensure_ascii=False, indent=2)

                        print(f"\n📄 詳細報告已儲存到: integration_test_report.json")

                        return report

                def check_prerequisites():
                    """檢查前置條件"""
                    print("🔍 檢查整合前置條件...")

                    checks = [
                        ("Day 1 資料檔案", "data/chunks/m1_enhanced_chunks.jsonl"),
                        ("Gemini API Key", os.getenv('AISTUDIO_API_KEY')),
                        ("API 伺服器", "http://localhost:8001/health")
                    ]

                    all_ready = True

                    for name, check_item in checks:
                        if name == "Gemini API Key":
                            status = "✅" if check_item else "❌ 未設定 AISTUDIO_API_KEY"
                        elif name == "API 伺服器":
                            try:
                                response = requests.get(check_item, timeout=5)
                                status = "✅" if response.status_code == 200 else f"❌ 伺服器未回應 ({response.status_code})"
                            except:
                                status = "❌ 無法連接到伺服器"
                        else:
                            status = "✅" if os.path.exists(check_item) else f"❌ 找不到 {check_item}"

                        print(f"{name}: {status}")
                        if "❌" in status:
                            all_ready = False

                    return all_ready

                if __name__ == "__main__":
                    print("🚀 M1 MVP + RAG 整合測試套件")
                    print("=" * 50)

                    # 檢查前置條件
                    if not check_prerequisites():
                        print("\n⚠️  前置條件未滿足，請先完成以下步驟：")
                        print("1. 執行 python day1_m1_rag_integration.py")
                        print("2. 設定 export AISTUDIO_API_KEY='your-key'")
                        print("3. 啟動 python day2_unified_api.py")
                        exit(1)

                    print("\n✅ 前置條件檢查通過，開始執行整合測試...")

                    # 執行測試
                    tester = M1RAGIntegrationTester()
                    report = tester.run_full_test_suite()

                    # 根據測試結果給出建議
                    if report["overall_status"] == "PASS":
                        print("\n🎉 恭喜！整合測試全部通過！")
                        print("\n📋 系統已準備就緒，具備以下功能：")
                        print("   ✅ 保持與現有 LINE Bot 的完全相容性")
                        print("   ✅ RAG 增強的失智症警訊分析")
                        print("   ✅ 智能向量檢索與相似度比對")
                        print("   ✅ 結構化 Flex Message 回應")
                        print("   ✅ 多 API 端點支援")
                        print("   ✅ 優雅的錯誤處理機制")

                        print("\n🚀 下一步建議：")
                        print("   1. 部署到你的 Replit 環境")
                        print("   2. 更新 LINE Bot Webhook URL")
                        print("   3. 進行真實使用者測試")
                        print("   4. 準備擴展 M2、M3 模組")

                    else:
                        print("\n⚠️  整合測試發現問題，需要修正：")

                        failed_tests = [r for r in report["detailed_results"] if not r["success"]]
                        for test in failed_tests[:5]:  # 顯示前 5 個失敗測試
                            print(f"   ❌ {test['test_name']}: {test['details'].get('error', '未知錯誤')}")

                        print(f"\n📄 完整錯誤報告請查看: integration_test_report.json")
                        print("\n🔧 常見解決方案：")
                        print("   1. 確認 Gemini API Key 正確設定")
                        print("   2. 檢查網路連接與 API 額度")
                        print("   3. 重新執行 day1_m1_rag_integration.py")
                        print("   4. 重啟 day2_unified_api.py 伺服器")