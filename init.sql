-- Database initialization script
-- Removed MySQL-specific CREATE DATABASE IF NOT EXISTS and \c lines for PostgreSQL compatibility

-- User interactions table
CREATE TABLE IF NOT EXISTS user_interactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    input_text TEXT NOT NULL,
    selected_module VARCHAR(10),
    confidence_score FLOAT,
    response_data JSONB,
    feedback_score INTEGER
);

-- Analysis cache table
CREATE TABLE IF NOT EXISTS analysis_cache (
    id SERIAL PRIMARY KEY,
    input_hash VARCHAR(64) UNIQUE NOT NULL,
    analysis_result JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    hit_count INTEGER DEFAULT 0
);

-- Module metrics table
CREATE TABLE IF NOT EXISTS module_metrics (
    id SERIAL PRIMARY KEY,
    module_id VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    usage_count INTEGER DEFAULT 0,
    avg_confidence FLOAT,
    avg_response_time FLOAT,
    satisfaction_score FLOAT,
    UNIQUE(module_id, date)
);

-- Create indexes
CREATE INDEX idx_user_interactions_user_id ON user_interactions(user_id);
CREATE INDEX idx_user_interactions_timestamp ON user_interactions(timestamp);
CREATE INDEX idx_analysis_cache_expires ON analysis_cache(expires_at);
CREATE INDEX idx_module_metrics_date ON module_metrics(date);
