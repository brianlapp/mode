-- PostgreSQL schema for Mode Popup System
-- Drop existing tables if they exist
DROP TABLE IF EXISTS campaign_properties CASCADE;
DROP TABLE IF EXISTS impressions CASCADE;
DROP TABLE IF EXISTS clicks CASCADE;
DROP TABLE IF EXISTS conversions CASCADE;
DROP TABLE IF EXISTS campaigns CASCADE;

-- Create campaigns table
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    tune_url TEXT NOT NULL,
    logo_url TEXT NOT NULL,
    main_image_url TEXT NOT NULL,
    description TEXT,
    cta_text TEXT DEFAULT 'View Offer',
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    offer_id TEXT,
    aff_id TEXT,
    partner_name TEXT,
    advertiser_name TEXT,
    payout_amount DECIMAL(10,2) DEFAULT 0.45,
    creative_file TEXT,
    featured BOOLEAN DEFAULT false
);

-- Create campaign_properties table
CREATE TABLE campaign_properties (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id),
    property_code TEXT NOT NULL,
    weight INTEGER DEFAULT 100,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create impressions table
CREATE TABLE impressions (
    id SERIAL PRIMARY KEY,
    offer_id TEXT,
    property_code TEXT,
    source TEXT DEFAULT 'popup',
    subsource TEXT,
    session_id TEXT,
    utm_campaign TEXT,
    utm_source TEXT,
    utm_medium TEXT,
    utm_content TEXT,
    utm_term TEXT,
    referrer TEXT,
    landing_page TEXT,
    user_agent TEXT,
    ip_address TEXT,
    country TEXT,
    region TEXT,
    city TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create clicks table
CREATE TABLE clicks (
    id SERIAL PRIMARY KEY,
    offer_id TEXT,
    property_code TEXT,
    source TEXT DEFAULT 'popup',
    subsource TEXT,
    session_id TEXT,
    utm_campaign TEXT,
    utm_source TEXT,
    utm_medium TEXT,
    utm_content TEXT,
    utm_term TEXT,
    referrer TEXT,
    landing_page TEXT,
    user_agent TEXT,
    ip_address TEXT,
    country TEXT,
    region TEXT,
    city TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create conversions table
CREATE TABLE conversions (
    id SERIAL PRIMARY KEY,
    offer_id TEXT,
    property_code TEXT,
    source TEXT DEFAULT 'popup',
    subsource TEXT,
    session_id TEXT,
    conversion_value DECIMAL(10,2) DEFAULT 0.45,
    utm_campaign TEXT,
    utm_source TEXT,
    utm_medium TEXT,
    utm_content TEXT,
    utm_term TEXT,
    referrer TEXT,
    landing_page TEXT,
    user_agent TEXT,
    ip_address TEXT,
    country TEXT,
    region TEXT,
    city TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_impressions_offer_property ON impressions(offer_id, property_code);
CREATE INDEX idx_impressions_timestamp ON impressions(timestamp);
CREATE INDEX idx_clicks_offer_property ON clicks(offer_id, property_code);
CREATE INDEX idx_clicks_timestamp ON clicks(timestamp);
CREATE INDEX idx_conversions_offer_property ON conversions(offer_id, property_code);
CREATE INDEX idx_conversions_timestamp ON conversions(timestamp);
CREATE INDEX idx_campaign_properties_campaign_id ON campaign_properties(campaign_id);
CREATE INDEX idx_campaign_properties_property_code ON campaign_properties(property_code);
