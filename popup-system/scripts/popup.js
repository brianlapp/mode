/**
 * Mode Popup Management System - Production Script
 * Embeddable JavaScript popup for Mode properties
 * Exact Thanks.co replica design with Mode branding
 * 
 * Usage:
 * <script src="https://mode-dash-production.up.railway.app/popup.js"></script>
 * <script>ModePopup.init({ property: 'mff', placement: 'thankyou' });</script>
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        API_BASE: 'https://mode-dash-production.up.railway.app/api',
        POPUP_ID: 'mode-popup-container',
        OVERLAY_ID: 'mode-popup-overlay',
        STORAGE_KEY: 'mode_popup_session',
        DEFAULT_FREQUENCY: 'session', // 'session', 'daily', 'always'
        DEFAULT_PLACEMENT: 'thankyou', // 'thankyou', 'exit-intent', 'timed'
        ANIMATION_DURATION: 300,
        ROTATION_DELAY: 15000, // 15 seconds between auto-rotation
        MOBILE_BREAKPOINT: 768,
        DESKTOP_BREAKPOINT: 1024
    };

    // Main ModePopup class
    class ModePopup {
        constructor() {
            this.campaigns = [];
            this.currentCampaignIndex = 0;
            this.config = {};
            this.isVisible = false;
            this.autoRotateTimer = null;
            this.sessionId = this.generateSessionId();
            this.trackingData = this.captureTrackingData(); // Phase 2: Capture URL params
        }

        /**
         * Initialize the popup system
         * @param {Object} options - Configuration options
         */
        async init(options = {}) {
            this.config = {
                property: options.property || 'mff',
                placement: options.placement || CONFIG.DEFAULT_PLACEMENT,
                frequency: options.frequency || CONFIG.DEFAULT_FREQUENCY,
                debug: options.debug || false,
                autoRotate: options.autoRotate !== false, // Default true
                ...options
            };

            this.debug('Initializing Mode Popup', this.config);

            // Check if popup should be shown based on frequency
            if (!this.shouldShowPopup()) {
                this.debug('Popup frequency check failed, not showing');
                return;
            }

            try {
                // Load campaigns from API
                await this.loadCampaigns();

                if (this.campaigns.length === 0) {
                    this.debug('No active campaigns found');
                    return;
                }

                // Show popup based on placement
                this.handlePlacement();

            } catch (error) {
                this.debug('Error initializing popup:', error);
            }
        }

        /**
         * Load active campaigns from API
         */
        async loadCampaigns() {
            try {
                const response = await fetch(`${CONFIG.API_BASE}/campaigns`);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                this.campaigns = data || [];
                this.debug(`Loaded ${this.campaigns.length} campaigns for ${this.config.property}`);
                
            } catch (error) {
                this.debug('Failed to load campaigns:', error);
                this.campaigns = [];
            }
        }

        /**
         * Handle popup placement strategy
         */
        handlePlacement() {
            switch (this.config.placement) {
                case 'thankyou':
                    // Show immediately on thank you pages
                    this.showPopup();
                    break;
                    
                case 'exit-intent':
                    // Show on exit intent
                    this.setupExitIntent();
                    break;
                    
                case 'timed':
                    // Show after delay
                    setTimeout(() => this.showPopup(), 3000);
                    break;
                    
                default:
                    this.showPopup();
            }
        }

        /**
         * Setup exit intent detection
         */
        setupExitIntent() {
            let exitIntentTriggered = false;
            
            const handleMouseLeave = (e) => {
                if (e.clientY <= 50 && !exitIntentTriggered) {
                    exitIntentTriggered = true;
                    this.showPopup();
                    document.removeEventListener('mouseleave', handleMouseLeave);
                }
            };

            document.addEventListener('mouseleave', handleMouseLeave);
        }

        /**
         * Check if popup should be shown based on frequency settings
         */
        shouldShowPopup() {
            const storageKey = `${CONFIG.STORAGE_KEY}_${this.config.property}`;
            const lastShown = localStorage.getItem(storageKey);
            
            if (!lastShown) return true;
            
            const lastShownDate = new Date(lastShown);
            const now = new Date();
            
            switch (this.config.frequency) {
                case 'always':
                    return true;
                    
                case 'daily':
                    return now.toDateString() !== lastShownDate.toDateString();
                    
                case 'session':
                default:
                    return false; // Already shown in this session
            }
        }

        /**
         * Mark popup as shown for frequency control
         */
        markPopupShown() {
            const storageKey = `${CONFIG.STORAGE_KEY}_${this.config.property}`;
            localStorage.setItem(storageKey, new Date().toISOString());
        }

        /**
         * Show the popup with current campaign
         */
        showPopup() {
            if (this.isVisible || this.campaigns.length === 0) return;

            this.createPopupHTML();
            this.isVisible = true;
            this.markPopupShown();
            
            // Track impression
            this.trackImpression();
            
            // Start auto-rotation if enabled and multiple campaigns
            if (this.config.autoRotate && this.campaigns.length > 1) {
                this.startAutoRotation();
            }

            this.debug('Popup shown');
        }

        /**
         * Create the popup HTML with exact Thanks.co replica design
         */
        createPopupHTML() {
            // Remove existing popup if any
            this.removePopup();

            const campaign = this.campaigns[this.currentCampaignIndex];
            
            // Create overlay
            const overlay = document.createElement('div');
            overlay.id = CONFIG.OVERLAY_ID;
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 999999;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                transition: opacity ${CONFIG.ANIMATION_DURATION}ms ease;
                padding: 16px;
                box-sizing: border-box;
            `;

            // Create popup container with responsive sizing
            const popup = document.createElement('div');
            popup.id = CONFIG.POPUP_ID;
            const isDesktop = window.innerWidth >= CONFIG.DESKTOP_BREAKPOINT;
            const maxWidth = isDesktop ? '600px' : '340px';
            
            popup.style.cssText = `
                max-width: ${maxWidth};
                width: 100%;
                background: white;
                border-radius: 24px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                overflow: hidden;
                position: relative;
                transform: scale(0.8);
                transition: transform ${CONFIG.ANIMATION_DURATION}ms ease;
                margin: 0 auto;
            `;

            // Create popup content with exact Thanks.co design
            popup.innerHTML = this.getPopupHTML(campaign);

            // Assemble and add to DOM
            overlay.appendChild(popup);
            document.body.appendChild(overlay);

            // Trigger animations
            requestAnimationFrame(() => {
                overlay.style.opacity = '1';
                popup.style.transform = 'scale(1)';
            });

            // Add event listeners
            this.attachEventListeners(overlay, popup, campaign);
        }

        /**
         * Get property-specific branding (logos and messaging)
         */
        getPropertyBranding() {
            const property = this.config.property?.toLowerCase() || 'mff';
            
            const brandingMap = {
                'mff': {
                    name: 'ModeFreeFinds',
                    tagline: 'Thanks for Reading - You\'ve unlocked bonus offers',
                    circleLogo: 'https://assets.isu.pub/document-structure/230821210201-6b2c1d176d5b4af7574d98b41de5de0d/v1/d08ce648ec2d8a39bf81ea8b6f317a12.jpeg',
                    footerLogo: 'https://i0.wp.com/modefreefinds.com/wp-content/uploads/2024/11/FreeFinds-Large.png?resize=1024%2C310&ssl=1',
                    color: '#F7007C'
                },
                'mmm': {
                    name: 'ModeMarketMunchies',
                    tagline: 'Thanks for Reading - You\'ve unlocked bonus offers',
                    circleLogo: 'https://assets.isu.pub/document-structure/230821210201-6b2c1d176d5b4af7574d98b41de5de0d/v1/d08ce648ec2d8a39bf81ea8b6f317a12.jpeg',
                    footerLogo: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjgwIiB2aWV3Qm94PSIwIDAgMzAwIDgwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iODAiIHJ4PSI0MCIgZmlsbD0iIzAwRkY3RiIvPjx0ZXh0IHg9IjE1MCIgeT0iNDAiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZm9udC13ZWlnaHQ9ImJvbGQiIGZpbGw9ImJsYWNrIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+TWFya2V0IE11bmNoaWVzPC90ZXh0Pjx0ZXh0IHg9IjI0MCIgeT0iNjAiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMiIgZmlsbD0iYmxhY2siPmZyb20gbW9kZTwvdGV4dD48L3N2Zz4=',
                    color: '#00FF7F'
                },
                'mcad': {
                    name: 'ModeClassActionsDaily',
                    tagline: 'Thanks for Joining - You\'ve unlocked bonus offers',
                    circleLogo: 'https://assets.isu.pub/document-structure/230821210201-6b2c1d176d5b4af7574d98b41de5de0d/v1/d08ce648ec2d8a39bf81ea8b6f317a12.jpeg',
                    footerLogo: 'https://modeclassactionsdaily.com/wp-content/uploads/2025/04/class-actions-logo.png',
                    color: '#F7007C'
                },
                'mmd': {
                    name: 'ModeMobileDaily',
                    tagline: 'Thanks for Reading - You\'ve unlocked bonus offers',
                    circleLogo: 'https://assets.isu.pub/document-structure/230821210201-6b2c1d176d5b4af7574d98b41de5de0d/v1/d08ce648ec2d8a39bf81ea8b6f317a12.jpeg',
                    footerLogo: 'https://assets.isu.pub/document-structure/230821210201-6b2c1d176d5b4af7574d98b41de5de0d/v1/d08ce648ec2d8a39bf81ea8b6f317a12.jpeg',
                    color: '#F7007C'
                }
            };
            
            return brandingMap[property] || brandingMap['mff'];
        }

        /**
         * Get the popup HTML content with exact Thanks.co replica design
         */
        getPopupHTML(campaign) {
            const screenWidth = window.innerWidth;
            const isMobile = screenWidth < CONFIG.MOBILE_BREAKPOINT;
            const isDesktop = screenWidth >= CONFIG.DESKTOP_BREAKPOINT;
            
            // Progressive image sizing for better desktop experience
            let imageSize;
            if (isDesktop) {
                imageSize = 'width: 480px; height: 240px;'; // Wide desktop images (taller landscape)
            } else if (isMobile) {
                imageSize = 'width: 260px; height: 200px;'; // Mobile images
            } else {
                imageSize = 'width: 280px; height: 220px;'; // Tablet images
            }

            // Co-branding system: Property-specific logos and messaging
            const propertyBranding = this.getPropertyBranding();

            return `
                <!-- Close Button -->
                <button class="mode-popup-close" style="
                    position: absolute;
                    top: 16px;
                    right: 16px;
                    background: rgba(0, 0, 0, 0.1);
                    border: none;
                    border-radius: 50%;
                    width: 32px;
                    height: 32px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    z-index: 10;
                    transition: background 0.2s ease;
                " onmouseover="this.style.background='rgba(0,0,0,0.2)'" onmouseout="this.style.background='rgba(0,0,0,0.1)'">
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <path d="M13 1L1 13M1 1L13 13" stroke="#666" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </button>

                <!-- Logo Circle (Exact Match) -->
                <div style="
                    position: absolute;
                    top: 24px; 
                    left: 24px;
                    width: 56px; 
                    height: 56px;
                    background: transparent;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 10;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                ">
                    <img src="${campaign.logo_url || 'https://via.placeholder.com/56/F7007C/FFFFFF?text=LOGO'}" 
                         alt="Campaign Logo"
                         style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;"
                         onerror="this.src='https://via.placeholder.com/56/F7007C/FFFFFF?text=LOGO'">
                </div>
                
                <!-- Main Content (Responsive padding for desktop) -->
                <div style="padding: ${isDesktop ? '24px 32px' : '24px'}; padding-top: ${isDesktop ? '50px' : '100px'}; text-align: center;">
                    
                    <!-- Tagline Pill -->
                    <div style="
                        background: #F3F4F6;
                        color: #6B7280;
                        padding: 6px 12px;
                        border-radius: 16px;
                        font-size: 12px;
                        margin-bottom: ${isDesktop ? '12px' : '24px'};
                        display: inline-block;
                        font-weight: 500;
                    ">${propertyBranding.tagline}</div>
                    
                    <!-- Title (Responsive sizing) -->
                    <h2 style="
                        margin: 0 0 8px 0;
                        font-size: ${isDesktop ? '28px' : '24px'};
                        font-weight: 800;
                        line-height: 1.2;
                        color: #111827;
                    ">${campaign.name || 'Exclusive Offer'}</h2>
                    
                    <!-- Campaign Image (Full Size) -->
                    <div style="margin: ${isDesktop ? '12px 0' : '16px 0'}; display: flex; align-items: center; justify-content: center;">
                        <img src="${campaign.main_image_url || 'https://via.placeholder.com/280x220/F7007C/FFFFFF?text=Offer'}" 
                             alt="Campaign" 
                             style="${imageSize} object-fit: contain; object-position: center; border-radius: 12px; background-color: white;"
                             onerror="this.src='https://via.placeholder.com/280x220/F7007C/FFFFFF?text=Offer'">
                    </div>
                    
                    <!-- Description (Exact Match) -->
                    <p style="
                        color: #6B7280;
                        font-size: 14px;
                        line-height: 1.4;
                        margin: ${isDesktop ? '12px 0 16px 0' : '16px 0 24px 0'};
                        text-align: center;
                    ">${campaign.description || 'Exclusive financial opportunity - limited time offer.'}</p>
                    
                    <!-- CTA Button (Exact Match) -->
                    <button class="mode-popup-cta" style="
                        width: 100%;
                        background: #7C3AED;
                        color: white;
                        border: none;
                        padding: 16px;
                        border-radius: 16px;
                        font-size: 16px;
                        font-weight: 600;
                        cursor: pointer;
                        margin-bottom: ${isDesktop ? '8px' : '12px'};
                        transition: background 0.2s ease;
                    " onmouseover="this.style.background='#6D28D9'" onmouseout="this.style.background='#7C3AED'">
                        ${campaign.cta_text || 'View Offer'}
                    </button>
                    
                    ${this.campaigns.length > 1 ? `
                    <!-- Next Button (From Approved Demo) -->
                    <button class="mode-popup-next" style="
                        width: 100%;
                        background: white;
                        color: #6B7280;
                        border: 2px solid #E5E7EB;
                        padding: 14px;
                        border-radius: 16px;
                        font-size: 14px;
                        font-weight: 500;
                        cursor: pointer;
                        margin-bottom: ${isDesktop ? '12px' : '16px'};
                        transition: all 0.2s ease;
                    " onmouseover="this.style.borderColor='#D1D5DB'; this.style.background='#F9FAFB'" 
                       onmouseout="this.style.borderColor='#E5E7EB'; this.style.background='white'">
                        Next >
                    </button>
                    
                    <!-- Pagination Dots -->
                    <div style="text-align: center; margin-bottom: 16px;">
                        ${this.campaigns.map((_, index) => `
                            <span style="
                                width: 8px; 
                                height: 8px; 
                                background: ${index === this.currentCampaignIndex ? '#374151' : '#D1D5DB'}; 
                                border-radius: 50%; 
                                margin: 0 3px; 
                                display: inline-block;
                                transition: background 0.2s ease;
                            "></span>
                        `).join('')}
                    </div>
                    ` : ''}
                    
                    <!-- Footer (Exact Match) -->
                    <div style="
                        color: #9CA3AF;
                        font-size: 11px;
                        text-align: center;
                        line-height: 1.3;
                    ">T&Cs Apply | Powered by <strong>${propertyBranding.name}</strong> • Privacy Policy</div>
                    
                    <!-- Property Brand Logo (Below Footer) -->
                    <div style="
                        text-align: center;
                        margin-top: 12px;
                        padding-bottom: 8px;
                    ">
                        <img src="${propertyBranding.footerLogo}" 
                             alt="${propertyBranding.name}"
                             style="
                                max-width: 75px;
                                max-height: 24px;
                                object-fit: contain;
                                opacity: 0.8;
                             "
                             onerror="this.style.display='none'">
                    </div>
                </div>
            `;
        }

        /**
         * Attach event listeners to popup elements
         */
        attachEventListeners(overlay, popup, campaign) {
            // Close button
            const closeBtn = popup.querySelector('.mode-popup-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.hidePopup();
                });
            }

            // CTA button
            const ctaBtn = popup.querySelector('.mode-popup-cta');
            if (ctaBtn) {
                ctaBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.handleCTAClick(campaign);
                });
            }

            // Next button
            const nextBtn = popup.querySelector('.mode-popup-next');
            if (nextBtn) {
                nextBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.nextCampaign();
                });
            }

            // Overlay click to close
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    this.hidePopup();
                }
            });

            // ESC key to close
            const handleKeyDown = (e) => {
                if (e.key === 'Escape') {
                    this.hidePopup();
                    document.removeEventListener('keydown', handleKeyDown);
                }
            };
            document.addEventListener('keydown', handleKeyDown);
        }

        /**
         * Handle CTA button click
         */
        handleCTAClick(campaign) {
            this.debug('CTA clicked', campaign);
            
            // Track click
            this.trackClick(campaign);
            
            // Open campaign URL with aff_sub3 for traffic source tracking
            if (campaign.tune_url) {
                const utm_source = this.trackingData.source || 'direct';
                const separator = campaign.tune_url.includes('?') ? '&' : '?';
                const trackingUrl = `${campaign.tune_url}${separator}aff_sub3=${encodeURIComponent(utm_source)}`;
                this.debug('Opening Tune URL with aff_sub3:', trackingUrl);
                window.open(trackingUrl, '_blank');
            }
            
            // Hide popup after click
            setTimeout(() => this.hidePopup(), 500);
        }

        /**
         * Move to next campaign
         */
        nextCampaign() {
            if (this.campaigns.length <= 1) return;

            this.currentCampaignIndex = (this.currentCampaignIndex + 1) % this.campaigns.length;
            
            // Update popup content with animation
            this.updatePopupContent();
            
            // Reset auto-rotation timer
            if (this.config.autoRotate) {
                this.resetAutoRotation();
            }

            this.debug(`Switched to campaign ${this.currentCampaignIndex + 1}/${this.campaigns.length}`);
        }

        /**
         * Update popup content with smooth transition
         */
        updatePopupContent() {
            const popup = document.getElementById(CONFIG.POPUP_ID);
            if (!popup) return;

            const campaign = this.campaigns[this.currentCampaignIndex];

            // Fade out
            popup.style.opacity = '0.7';
            popup.style.transform = 'scale(0.98)';

            setTimeout(() => {
                // Update content
                popup.innerHTML = this.getPopupHTML(campaign);
                
                // Re-attach event listeners
                const overlay = document.getElementById(CONFIG.OVERLAY_ID);
                this.attachEventListeners(overlay, popup, campaign);
                
                // Fade in
                popup.style.opacity = '1';
                popup.style.transform = 'scale(1)';
                
                // Track impression for new campaign
                this.trackImpression();
                
            }, 100);
        }

        /**
         * Start auto-rotation timer
         */
        startAutoRotation() {
            this.stopAutoRotation();
            this.autoRotateTimer = setInterval(() => {
                this.nextCampaign();
            }, CONFIG.ROTATION_DELAY);
        }

        /**
         * Stop auto-rotation timer
         */
        stopAutoRotation() {
            if (this.autoRotateTimer) {
                clearInterval(this.autoRotateTimer);
                this.autoRotateTimer = null;
            }
        }

        /**
         * Reset auto-rotation timer
         */
        resetAutoRotation() {
            if (this.config.autoRotate && this.campaigns.length > 1) {
                this.startAutoRotation();
            }
        }

        /**
         * Hide the popup with animation
         */
        hidePopup() {
            const overlay = document.getElementById(CONFIG.OVERLAY_ID);
            const popup = document.getElementById(CONFIG.POPUP_ID);
            
            if (!overlay || !popup) return;

            this.stopAutoRotation();

            // Animate out
            overlay.style.opacity = '0';
            popup.style.transform = 'scale(0.8)';

            setTimeout(() => {
                this.removePopup();
                this.isVisible = false;
            }, CONFIG.ANIMATION_DURATION);

            this.debug('Popup hidden');
        }

        /**
         * Remove popup from DOM
         */
        removePopup() {
            const overlay = document.getElementById(CONFIG.OVERLAY_ID);
            if (overlay) {
                overlay.remove();
            }
        }

        /**
         * Track impression event
         */
        async trackImpression() {
            const campaign = this.campaigns[this.currentCampaignIndex];
            if (!campaign) return;

            try {
                await fetch(`${CONFIG.API_BASE}/impression`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        campaign_id: campaign.id,
                        property_code: this.config.property,
                        session_id: this.sessionId,
                        placement: this.config.placement,
                        user_agent: navigator.userAgent,
                        timestamp: new Date().toISOString(),
                        // Phase 2: Enhanced tracking data
                        source: this.trackingData.source,
                        subsource: this.trackingData.subsource,
                        utm_campaign: this.trackingData.utm_campaign,
                        referrer: this.trackingData.referrer,
                        landing_page: this.trackingData.landing_page
                    })
                });

                this.debug('Impression tracked', campaign.id);
            } catch (error) {
                this.debug('Failed to track impression:', error);
            }
        }

        /**
         * Track click event
         */
        async trackClick(campaign) {
            try {
                await fetch(`${CONFIG.API_BASE}/click`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        campaign_id: campaign.id,
                        property_code: this.config.property,
                        session_id: this.sessionId,
                        placement: this.config.placement,
                        user_agent: navigator.userAgent,
                        timestamp: new Date().toISOString(),
                        // Phase 2: Enhanced tracking data
                        source: this.trackingData.source,
                        subsource: this.trackingData.subsource,
                        utm_campaign: this.trackingData.utm_campaign,
                        referrer: this.trackingData.referrer,
                        landing_page: this.trackingData.landing_page
                    })
                });

                this.debug('Click tracked', campaign.id);
            } catch (error) {
                this.debug('Failed to track click:', error);
            }
        }

        /**
         * Generate unique session ID
         */
        generateSessionId() {
            return 'mode_' + Date.now() + '_' + Math.random().toString(36).substring(2, 15);
        }

        /**
         * Phase 2: Capture URL parameters for traffic attribution
         */
        captureTrackingData() {
            const urlParams = new URLSearchParams(window.location.search);
            
            // Multiple parameter names for different tracking systems
            const getFirstParam = (params) => {
                for (const param of params) {
                    const value = urlParams.get(param);
                    if (value) return value;
                }
                return '';
            };

            return {
                source: getFirstParam(['utm_source', 'source', 'src', 'ref']),
                subsource: getFirstParam(['utm_medium', 'subsource', 'sub', 'medium']),
                utm_campaign: getFirstParam(['utm_campaign', 'campaign', 'camp']),
                referrer: document.referrer || '',
                landing_page: window.location.href
            };
        }

        /**
         * Debug logging
         */
        debug(...args) {
            if (this.config.debug) {
                console.log('[ModePopup]', ...args);
            }
        }
    }

    // Create global instance
    window.ModePopup = new ModePopup();

    // Auto-initialize if data attributes are present
    document.addEventListener('DOMContentLoaded', () => {
        const script = document.querySelector('script[src*="popup.js"]');
        if (script) {
            const property = script.getAttribute('data-property');
            const placement = script.getAttribute('data-placement');
            const frequency = script.getAttribute('data-frequency');
            
            if (property) {
                window.ModePopup.init({
                    property,
                    placement: placement || 'thankyou',
                    frequency: frequency || 'session'
                });
            }
        }
    });

})(); 