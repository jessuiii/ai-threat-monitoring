# PostgreSQL DB schema for MVP

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    features JSONB NOT NULL,
    source VARCHAR(32),
    is_simulated BOOLEAN DEFAULT FALSE
);

CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    log_id INTEGER REFERENCES logs(id),
    predicted_label VARCHAR(32),
    confidence FLOAT,
    explanation JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    prediction_id INTEGER REFERENCES predictions(id),
    severity VARCHAR(16),
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
