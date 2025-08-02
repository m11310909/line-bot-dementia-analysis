import React, { useState, useEffect } from 'react';
import './App.css';

interface AnalysisResult {
  success: boolean;
  analysis_result: any;
  confidence: number;
  modules_used: string[];
  visualization_data?: any;
  explanation_path?: string[];
}

interface VerificationResult {
  success: boolean;
  verified_aspects: any;
  overall_confidence: number;
  verification_score: number;
  recommendations: string[];
}

interface MAVResult {
  success: boolean;
  network_results: any;
  ensemble_result: any;
  validation_score: number;
  recommendations: string[];
}

function App() {
  const [liff, setLiff] = useState<any>(null);
  const [profile, setProfile] = useState<any>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userInput, setUserInput] = useState('');
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [verificationResult, setVerificationResult] = useState<VerificationResult | null>(null);
  const [mavResult, setMavResult] = useState<MAVResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('analysis');

  useEffect(() => {
    const initLiff = async () => {
      try {
        const liffInstance = await import('@line/liff');
        await liffInstance.default.init({ liffId: process.env.REACT_APP_LIFF_ID || '' });
        setLiff(liffInstance.default);

        if (liffInstance.default.isLoggedIn()) {
          setIsLoggedIn(true);
          const profile = await liffInstance.default.getProfile();
          setProfile(profile);
        }
      } catch (error) {
        console.error('LIFF initialization failed:', error);
      }
    };

    initLiff();
  }, []);

  const handleAnalysis = async () => {
    if (!userInput.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8005/comprehensive-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: userInput,
          user_id: profile?.userId || 'anonymous',
          include_visualization: true
        }),
      });

      const result = await response.json();
      setAnalysisResult(result);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleVerification = async () => {
    if (!userInput.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8007/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: userInput,
          user_id: profile?.userId || 'anonymous',
          aspects: ['symptom', 'severity', 'urgency', 'context']
        }),
      });

      const result = await response.json();
      setVerificationResult(result);
    } catch (error) {
      console.error('Verification failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMAV = async () => {
    if (!userInput.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8008/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: userInput,
          user_id: profile?.userId || 'anonymous',
          networks: ['symptom', 'severity', 'context', 'temporal'],
          validation_mode: 'ensemble'
        }),
      });

      const result = await response.json();
      setMavResult(result);
    } catch (error) {
      console.error('MAV validation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderAnalysisResult = () => {
    if (!analysisResult) return null;

    return (
      <div className="result-card">
        <h3>🧠 智能分析結果</h3>
        <div className="confidence-bar">
          <span>可信度: {(analysisResult.confidence * 100).toFixed(1)}%</span>
          <div className="bar" style={{ width: `${analysisResult.confidence * 100}%` }}></div>
        </div>
        <div className="modules-used">
          <h4>使用的模組:</h4>
          <div className="module-tags">
            {analysisResult.modules_used.map((module, index) => (
              <span key={index} className="module-tag">{module}</span>
            ))}
          </div>
        </div>
        {analysisResult.explanation_path && (
          <div className="explanation-path">
            <h4>分析路徑:</h4>
            {analysisResult.explanation_path.slice(0, 3).map((explanation, index) => (
              <p key={index} className="explanation-item">📝 {explanation}</p>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderVerificationResult = () => {
    if (!verificationResult) return null;

    return (
      <div className="result-card">
        <h3>🔍 多角度驗證結果</h3>
        <div className="verification-score">
          <span>驗證分數: {(verificationResult.verification_score * 100).toFixed(1)}%</span>
          <div className="bar" style={{ width: `${verificationResult.verification_score * 100}%` }}></div>
        </div>
        <div className="verified-aspects">
          <h4>驗證面向:</h4>
          {Object.entries(verificationResult.verified_aspects).map(([aspect, data]: [string, any]) => (
            <div key={aspect} className="aspect-item">
              <span className={`aspect-status ${data.verified ? 'verified' : 'not-verified'}`}>
                {data.verified ? '✅' : '❌'} {aspect}
              </span>
              <span className="aspect-confidence">{(data.confidence * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>
        <div className="recommendations">
          <h4>建議:</h4>
          {verificationResult.recommendations.map((rec, index) => (
            <p key={index} className="recommendation-item">💡 {rec}</p>
          ))}
        </div>
      </div>
    );
  };

  const renderMAVResult = () => {
    if (!mavResult) return null;

    return (
      <div className="result-card">
        <h3>🌐 BoN-MAV 網路驗證結果</h3>
        <div className="validation-score">
          <span>驗證分數: {(mavResult.validation_score * 100).toFixed(1)}%</span>
          <div className="bar" style={{ width: `${mavResult.validation_score * 100}%` }}></div>
        </div>
        <div className="network-results">
          <h4>網路結果:</h4>
          {Object.entries(mavResult.network_results).map(([network, data]: [string, any]) => (
            <div key={network} className="network-item">
              <span className={`network-status ${data.validated ? 'validated' : 'not-validated'}`}>
                {data.validated ? '✅' : '❌'} {network}
              </span>
              <span className="network-confidence">{(data.confidence * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>
        <div className="ensemble-result">
          <h4>集成結果:</h4>
          <p>集成信心度: {(mavResult.ensemble_result.ensemble_confidence * 100).toFixed(1)}%</p>
          <p>通過驗證: {mavResult.ensemble_result.ensemble_validated ? '✅' : '❌'}</p>
        </div>
        <div className="recommendations">
          <h4>建議:</h4>
          {mavResult.recommendations.map((rec, index) => (
            <p key={index} className="recommendation-item">💡 {rec}</p>
          ))}
        </div>
      </div>
    );
  };

  if (!isLoggedIn) {
    return (
      <div className="App">
        <div className="login-container">
          <h1>🧠 失智症照護智能助手</h1>
          <p>請登入 LINE 以使用完整功能</p>
          <button onClick={() => liff?.login()}>登入 LINE</button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🧠 失智症照護智能助手</h1>
        {profile && (
          <div className="user-profile">
            <img src={profile.pictureUrl} alt="Profile" className="profile-pic" />
            <span>{profile.displayName}</span>
          </div>
        )}
      </header>

      <div className="main-container">
        <div className="input-section">
          <textarea
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="請描述您觀察到的症狀或行為..."
            className="input-textarea"
          />
          <div className="action-buttons">
            <button 
              onClick={handleAnalysis} 
              disabled={loading}
              className="action-btn analysis-btn"
            >
              {loading ? '分析中...' : '🧠 智能分析'}
            </button>
            <button 
              onClick={handleVerification} 
              disabled={loading}
              className="action-btn verification-btn"
            >
              {loading ? '驗證中...' : '🔍 多角度驗證'}
            </button>
            <button 
              onClick={handleMAV} 
              disabled={loading}
              className="action-btn mav-btn"
            >
              {loading ? '驗證中...' : '🌐 BoN-MAV 驗證'}
            </button>
          </div>
        </div>

        <div className="results-section">
          {renderAnalysisResult()}
          {renderVerificationResult()}
          {renderMAVResult()}
        </div>
      </div>
    </div>
  );
}

export default App; 