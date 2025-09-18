PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                tune_url TEXT NOT NULL,
                logo_url TEXT NOT NULL,           -- For top-left circle
                main_image_url TEXT NOT NULL,     -- For main offer display
                description TEXT,                 -- Optional campaign description
                cta_text TEXT DEFAULT 'View Offer', -- Customizable button text
                active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            , offer_id TEXT, aff_id TEXT, partner_name TEXT, advertiser_name TEXT, payout_amount DECIMAL(10,2) DEFAULT 0.45, creative_file TEXT, featured BOOLEAN DEFAULT false);
INSERT INTO campaigns VALUES(1,'Trading Tips','https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup_tradingTips','https://i.imgur.com/lHn301q.png','https://i.imgur.com/ZVGOktR.png','Get exclusive trading tips and market insights delivered daily to your inbox.','Get Trading Tips',1,'2025-07-31 14:30:20','2025-07-31 14:30:25','6998','43045',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(2,'Behind The Markets','https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045&aff_sub5=popup_behindMarkets','https://i.imgur.com/O3iEVP7.jpeg','https://i.imgur.com/NA0o7iJ.png','Discover what''s really happening behind the financial markets with expert analysis.','Learn More',1,'2025-07-31 14:30:20','2025-07-31 14:30:25','7521','43045',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(3,'Brownstone Research','https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045&aff_sub5=popup_brownstone','https://i.imgur.com/3KVDcV7.jpeg','https://i.imgur.com/vzoiVpd.png','Advanced technology and investment research from Brownstone Research experts.','View Research',1,'2025-07-31 14:30:20','2025-07-31 14:30:25','7389','43045',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(4,'Hotsheets','https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045&aff_sub5=popup_hotsheets','https://i.imgur.com/4JoGdZr.png','https://i.imgur.com/O81cPQJ.jpeg','Daily market hotsheets with the most profitable trading opportunities.','Get Hotsheets',1,'2025-07-31 14:30:20','2025-07-31 14:30:25','7385','43045',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(5,'Best Gold','https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045&aff_sub5=popup_bestGold','https://i.imgur.com/5Yb0LJn.png','https://i.imgur.com/EEOyDuZ.jpeg','Premium gold investment insights and recommendations from industry experts.','Learn About Gold',1,'2025-07-31 14:30:20','2025-07-31 14:30:25','7390','43045',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(6,'Daily Goodie Box','https://track.modemobile.com/aff_c?offer_id=6571&aff_id=42946&aff_sub2=perks','https://i.imgur.com/DH7Tp4A.jpeg','https://i.imgur.com/JpKD9AX.png','Get your daily goodie box filled with amazing free samples and deals.','Claim Now!',1,'2025-08-14 17:12:45','2025-08-15 14:25:13','6571','42946',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(7,'Free Samples Guide','https://track.modemobile.com/aff_c?offer_id=3907&aff_id=42946&aff_sub2=perks','https://resources.rndsystems.com/images/promo_pages/free-sample-icon.png','https://i.imgur.com/vbgSfMi.jpeg','Get your comprehensive free samples guide with exclusive offers.','Claim Now!',1,'2025-08-14 17:12:45','2025-08-15 14:25:24','3907','42946',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(8,'Prizies','https://track.modemobile.com/aff_c?offer_id=7774&aff_id=42946&aff_sub2=perks','https://imgur.com/QEt3znb.jpg','https://imgur.com/KCp0xqn.jpg','Win $1,000 Cashapp!','Win Now!',1,'2025-08-14 17:54:27','2025-08-15 14:25:00','7774','42946',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(9,'Hulu - Hit Movies, TV and More!','https://track.modemobile.com/aff_c?offer_id=5555&aff_id=42946&aff_sub2=perks','https://imgur.com/RHRuCvk.jpg','https://imgur.com/SEu1NtW.jpg','Exclusive Offers from Hulu!','Get Hulu!',1,'2025-08-14 17:54:28','2025-08-15 14:24:18','5555','42946',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(10,'Paramount','https://track.modemobile.com/aff_c?offer_id=5172&aff_id=42946&aff_sub2=perks','https://imgur.com/2IpSLaY.jpg','https://imgur.com/p8o0YSR.jpg','Exclusive Offers from Paramount+!','Get Paramount+!',1,'2025-08-14 17:54:28','2025-08-15 14:24:47','5172','42946',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(11,'Trend''n Daily','https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946&aff_sub2=perks','https://imgur.com/Xmb1P8t.jpg','https://imgur.com/tA8fYBO.jpg','Grab an Amazon Mystery Box!','Get Box!',1,'2025-08-14 17:54:39','2025-08-15 14:24:02','4689','42946',NULL,NULL,0.4500000000000000111,NULL,0);
INSERT INTO campaigns VALUES(12,'Prizies','https://track.modemobile.com/aff_c?offer_id=7774&aff_id=42946&aff_sub2=perks','https://imgur.com/QEt3znb.jpg','https://imgur.com/KCp0xqn.jpg','Win $1,000 Cashapp!','Win!',1,'2025-08-14 17:54:39','2025-08-15 14:23:50','3752','42946',NULL,NULL,0.4500000000000000111,NULL,0);
CREATE TABLE campaign_properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                property_code TEXT NOT NULL,      -- 'mff', 'mmm', 'mcad', 'mmd'
                visibility_percentage INTEGER DEFAULT 100,  -- 0-100%
                active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
                UNIQUE(campaign_id, property_code)  -- One setting per campaign per property
            );
INSERT INTO campaign_properties VALUES(42,11,'mff',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(43,12,'mff',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(44,9,'mff',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(45,10,'mff',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(46,8,'mff',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(47,6,'mff',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(48,7,'mff',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(49,1,'mmm',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(50,2,'mmm',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(51,3,'mmm',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(52,4,'mmm',100,1,'2025-08-16 18:03:21');
INSERT INTO campaign_properties VALUES(53,5,'mmm',100,1,'2025-08-16 18:03:21');
CREATE TABLE impressions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                property_code TEXT NOT NULL,
                session_id TEXT,
                placement TEXT DEFAULT 'thankyou',
                user_agent TEXT,
                ip_hash INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, source TEXT, subsource TEXT, utm_campaign TEXT, referrer TEXT, landing_page TEXT,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
            );
INSERT INTO impressions VALUES(1,6998,'mmm','final_validation','thankyou','Mozilla/5.0 Test Agent',123456,'2025-07-31 00:27:39','meta','cpc','finance_lookalike','https://facebook.com','https://modemarketmunchies.com/test');
CREATE TABLE clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                property_code TEXT NOT NULL,
                session_id TEXT,
                placement TEXT DEFAULT 'thankyou',
                user_agent TEXT,
                ip_hash INTEGER,
                revenue_estimate DECIMAL(10,2) DEFAULT 0.45,
                conversion_tracked BOOLEAN DEFAULT false,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, source TEXT, subsource TEXT, utm_campaign TEXT, referrer TEXT, landing_page TEXT,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
            );
INSERT INTO clicks VALUES(1,6998,'mmm','final_validation','thankyou','Mozilla/5.0 Test Agent',123456,0.4500000000000000111,0,'2025-07-31 00:27:39','meta','cpc','finance_lookalike','https://facebook.com','https://modemarketmunchies.com/test');
CREATE TABLE conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                property_code TEXT NOT NULL,
                session_id TEXT,
                conversion_value DECIMAL(10,2) DEFAULT 0.45,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source TEXT,
                subsource TEXT,
                utm_campaign TEXT,
                referrer TEXT,
                landing_page TEXT,
                tune_conversion_id TEXT,  -- Tune's conversion ID from webhook
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE
            );
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('impressions',1);
INSERT INTO sqlite_sequence VALUES('clicks',1);
INSERT INTO sqlite_sequence VALUES('campaigns',12);
INSERT INTO sqlite_sequence VALUES('campaign_properties',53);
CREATE INDEX idx_campaign_active ON campaigns(active);
CREATE INDEX idx_property_active ON campaign_properties(property_code, active);
CREATE INDEX idx_impressions_date ON impressions(timestamp);
CREATE INDEX idx_impressions_campaign ON impressions(campaign_id, timestamp);
CREATE INDEX idx_clicks_date ON clicks(timestamp);
CREATE INDEX idx_clicks_campaign ON clicks(campaign_id, timestamp);
CREATE INDEX idx_property_stats ON impressions(property_code, timestamp);
CREATE INDEX idx_conversions_campaign ON conversions(campaign_id, timestamp);
CREATE INDEX idx_conversions_property ON conversions(property_code, timestamp);
COMMIT;
