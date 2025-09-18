-- Insert campaign data into PostgreSQL
INSERT INTO campaigns (id, name, tune_url, logo_url, main_image_url, description, cta_text, active, offer_id, aff_id, payout_amount) VALUES
(1, 'Trading Tips', 'https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup_tradingTips', 'https://i.imgur.com/lHn301q.png', 'https://i.imgur.com/ZVGOktR.png', 'Get exclusive trading tips and market insights delivered daily to your inbox.', 'Get Trading Tips', true, '6998', '43045', 0.45),
(2, 'Behind The Markets', 'https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045&aff_sub5=popup_behindMarkets', 'https://i.imgur.com/O3iEVP7.jpeg', 'https://i.imgur.com/NA0o7iJ.png', 'Discover what''s really happening behind the financial markets with expert analysis.', 'Learn More', true, '7521', '43045', 0.45),
(3, 'Brownstone Research', 'https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045&aff_sub5=popup_brownstone', 'https://i.imgur.com/3KVDcV7.jpeg', 'https://i.imgur.com/vzoiVpd.png', 'Advanced technology and investment research from Brownstone Research experts.', 'View Research', true, '7389', '43045', 0.45),
(4, 'Hotsheets', 'https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045&aff_sub5=popup_hotsheets', 'https://i.imgur.com/4JoGdZr.png', 'https://i.imgur.com/O81cPQJ.jpeg', 'Daily market hotsheets with the most profitable trading opportunities.', 'Get Hotsheets', true, '7385', '43045', 0.45),
(5, 'Best Gold', 'https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045&aff_sub5=popup_bestGold', 'https://i.imgur.com/5Yb0LJn.png', 'https://i.imgur.com/EEOyDuZ.jpeg', 'Premium gold investment insights and recommendations from industry experts.', 'Learn About Gold', true, '7390', '43045', 0.45),
(6, 'Daily Goodie Box', 'https://track.modemobile.com/aff_c?offer_id=6571&aff_id=42946&aff_sub2=perks', 'https://i.imgur.com/DH7Tp4A.jpeg', 'https://i.imgur.com/JpKD9AX.png', 'Get your daily goodie box filled with amazing free samples and deals.', 'Claim Now!', true, '6571', '42946', 0.45),
(7, 'Free Samples Guide', 'https://track.modemobile.com/aff_c?offer_id=3907&aff_id=42946&aff_sub2=perks', 'https://i.imgur.com/1Tn7Qkl.jpeg', 'https://i.imgur.com/qLVGJ7A.png', 'Your ultimate guide to getting free samples from top brands.', 'Get Guide', true, '3907', '42946', 0.45),
(8, 'Prizies', 'https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946&aff_sub2=perks', 'https://i.imgur.com/VpJOGLQ.jpeg', 'https://i.imgur.com/CyJLKBb.png', 'Win amazing prizes and rewards with Prizies - your chance to win big!', 'Enter Now', true, '4689', '42946', 0.45),
(9, 'Hulu - Hit Movies, TV and More', 'https://track.modemobile.com/aff_c?offer_id=5555&aff_id=42946&aff_sub2=perks', 'https://i.imgur.com/6LzrEjN.jpeg', 'https://i.imgur.com/8yGnQvG.png', 'Stream thousands of hit movies, TV shows and Hulu Originals.', 'Start Streaming', true, '5555', '42946', 0.45),
(10, 'Paramount', 'https://track.modemobile.com/aff_c?offer_id=5172&aff_id=42946&aff_sub2=perks', 'https://i.imgur.com/kWE8f1J.jpeg', 'https://i.imgur.com/mJcLKDL.png', 'Stream your favorite shows and movies on Paramount+ with exclusive content.', 'Watch Now', true, '5172', '42946', 0.45),
(11, 'Trend''n Daily', 'https://track.modemobile.com/aff_c?offer_id=5555&aff_id=42946&aff_sub2=perks', 'https://i.imgur.com/9Zj8Qjr.jpeg', 'https://i.imgur.com/KtYgR8A.png', 'Stay ahead of the trends with daily updates on fashion, lifestyle and more.', 'Get Updates', true, '5555', '42946', 0.45),
(12, 'UpLevelRewards', 'https://track.modemobile.com/aff_c?offer_id=4689&aff_id=42946&aff_sub2=perks', 'https://i.imgur.com/VpJOGLQ.jpeg', 'https://i.imgur.com/CyJLKBb.png', 'Unlock exclusive rewards and level up your lifestyle with UpLevelRewards.', 'Level Up', true, '4689', '42946', 0.45);

-- Insert campaign property assignments
INSERT INTO campaign_properties (campaign_id, property_code, weight, active) VALUES
-- MFF campaigns (lifestyle)
(6, 'mff', 100, true),   -- Daily Goodie Box
(7, 'mff', 100, true),   -- Free Samples Guide  
(8, 'mff', 100, true),   -- Prizies
(9, 'mff', 100, true),   -- Hulu
(10, 'mff', 100, true),  -- Paramount
(11, 'mff', 100, true),  -- Trend'n Daily
(12, 'mff', 100, true),  -- UpLevelRewards

-- MMM campaigns (finance)
(1, 'mmm', 100, true),   -- Trading Tips
(2, 'mmm', 100, true),   -- Behind The Markets
(3, 'mmm', 100, true),   -- Brownstone Research
(4, 'mmm', 100, true),   -- Hotsheets
(5, 'mmm', 100, true);   -- Best Gold

-- Reset sequences to proper values
SELECT setval('campaigns_id_seq', 12);
SELECT setval('campaign_properties_id_seq', (SELECT MAX(id) FROM campaign_properties));
