/*! Mode Popup v1.0 | (c) 2025 Mode | Production Build */
!function(){"use strict";

    const CONFIG = {
    API_BASE: "https://mode-dash-production.up.railway.app/api",
    POPUP_ID: "mode-popup-container",
    OVERLAY_ID: "mode-popup-overlay",
    STORAGE_KEY: "mode_popup_session",
    DEFAULT_FREQUENCY: "session",
    DEFAULT_PLACEMENT: "thankyou",
        ANIMATION_DURATION: 300,
    ROTATION_DELAY: 15000,
        MOBILE_BREAKPOINT: 768
    };

    class ModePopup {
        constructor() {
            this.campaigns = [];
            this.currentCampaignIndex = 0;
            this.isVisible = false;
            this.sessionId = this.generateSessionId();
        this.rotationInterval = null;
        this.config = {
            property: 'mff',
            placement: 'thankyou', 
            frequency: 'session',
            debug: false
        };
        this.debug('🚀 ModePopup initialized');
    }

        async init(options = {}) {
        this.config = { ...this.config, ...options };
        this.debug(`🔧 Initializing with config:`, this.config);
        
        try {
            await this.loadCampaigns();
            this.handlePlacement();
        } catch (error) {
            this.debug('❌ Initialization failed:', error);
        }
    }

    async loadCampaigns() {
        try {
            this.debug('📡 Loading campaigns from API...');
            // Use the working endpoint and filter locally
            const response = await fetch(`${CONFIG.API_BASE}/campaigns`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const allCampaigns = await response.json();
            this.debug(`📊 Received ${allCampaigns.length} total campaigns`);
            
            // Filter for active campaigns only
            this.campaigns = allCampaigns.filter(campaign => campaign.active === true);
            this.debug(`✅ Filtered to ${this.campaigns.length} active campaigns:`, this.campaigns.map(c => c.name));
            
            if (this.campaigns.length === 0) {
                this.debug('⚠️ No active campaigns available');
                return;
            }

            // Shuffle campaigns for variety
            this.campaigns = this.shuffleArray(this.campaigns);
            this.currentCampaignIndex = 0;
            
        } catch (error) {
            this.debug('❌ Failed to load campaigns:', error);
            throw error;
        }
    }

    shuffleArray(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    handlePlacement() {
                if (this.campaigns.length === 0) {
            this.debug('⚠️ No campaigns to show');
                    return;
                }

        const { placement, frequency } = this.config;
        
        this.debug(`📍 Handling placement: ${placement}, frequency: ${frequency}`);
        
        // Check if should show based on frequency
        if (!this.shouldShowPopup()) {
            this.debug('🚫 Popup already shown for this session/day');
            return;
        }

        if (placement === 'thankyou') {
                    // Show immediately on thank you pages
            setTimeout(() => this.showPopup(), 1000);
        } else if (placement === 'exit-intent') {
            // Add exit intent listener
            this.addExitIntentListener();
        } else if (placement === 'timed') {
                    // Show after delay
            setTimeout(() => this.showPopup(), 10000);
        }
    }

    shouldShowPopup() {
        const { frequency } = this.config;
        const storageKey = `${CONFIG.STORAGE_KEY}_${frequency}`;
        
        if (frequency === 'always') {
            return true;
        }
        
        const lastShown = localStorage.getItem(storageKey);
        
        if (frequency === 'session') {
            return !sessionStorage.getItem(storageKey);
        } else if (frequency === 'daily') {
            const today = new Date().toDateString();
            return lastShown !== today;
        }
        
        return true;
    }

    markPopupShown() {
        const { frequency } = this.config;
        const storageKey = `${CONFIG.STORAGE_KEY}_${frequency}`;
        
        if (frequency === 'session') {
            sessionStorage.setItem(storageKey, 'shown');
        } else if (frequency === 'daily') {
            const today = new Date().toDateString();
            localStorage.setItem(storageKey, today);
        }
    }

    addExitIntentListener() {
        let shown = false;
            
            const handleMouseLeave = (e) => {
            if (e.clientY <= 0 && !shown) {
                shown = true;
                    this.showPopup();
                    document.removeEventListener('mouseleave', handleMouseLeave);
                }
            };

            document.addEventListener('mouseleave', handleMouseLeave);
        }

    showPopup() {
        if (this.isVisible || this.campaigns.length === 0) {
            return;
        }

        this.debug(`🎭 Showing popup for campaign: ${this.campaigns[this.currentCampaignIndex].name}`);
        
            this.isVisible = true;
            this.markPopupShown();
        
        // Remove existing popup if any
        this.removePopup();
        
        // Create popup HTML
        const popupHTML = this.createPopupHTML();
        document.body.insertAdjacentHTML('beforeend', popupHTML);
        
        // Attach event listeners
        this.attachEventListeners();
            
            // Track impression
            this.trackImpression();
            
        // Start auto-rotation if multiple campaigns
        if (this.campaigns.length > 1) {
                this.startAutoRotation();
            }

        // Animate in
        setTimeout(() => {
            const popup = document.getElementById(CONFIG.POPUP_ID);
            if (popup) {
                popup.style.opacity = '1';
                popup.style.transform = 'translate(-50%, -50%) scale(1)';
            }
        }, 50);
    }

        createPopupHTML() {
            const campaign = this.campaigns[this.currentCampaignIndex];
        const currentNum = this.currentCampaignIndex + 1;
        const totalCount = this.campaigns.length;
        
        return `
            <div id="${CONFIG.OVERLAY_ID}" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.6);
                z-index: 999998;
                backdrop-filter: blur(4px);
            ">
                <div id="${CONFIG.POPUP_ID}" style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%) scale(0.9);
                max-width: 340px;
                    width: 90%;
                    margin: 0 auto;
                background: white;
                border-radius: 24px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                overflow: hidden;
                    z-index: 999999;
                    opacity: 0;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                ">
                    <!-- Logo Circle -->
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
                        <img src="${campaign.logo_url}" 
                         alt="Logo"
                         style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;"
                         onerror="this.src='https://via.placeholder.com/56/F7007C/FFFFFF?text=LOGO'">
                </div>
                
                    <!-- Close button -->
                    <button id="mode-popup-close" style="
                        position: absolute;
                        top: 16px;
                        right: 16px;
                        width: 32px;
                        height: 32px;
                        border: none;
                        background: rgba(0, 0, 0, 0.1);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        cursor: pointer;
                        z-index: 10;
                        font-size: 18px;
                        color: #666;
                        transition: all 0.2s ease;
                    " onmouseover="this.style.background='rgba(0,0,0,0.2)'" onmouseout="this.style.background='rgba(0,0,0,0.1)'">
                        ×
                    </button>

                                         <!-- Main content -->
                <div style="padding: 24px; padding-top: 100px; text-align: center;">
                         <!-- Mode tagline -->
                    <div style="
                        background: #F3F4F6;
                        color: #6B7280;
                        padding: 6px 12px;
                        border-radius: 16px;
                        font-size: 12px;
                             font-weight: 500;
                        display: inline-block;
                             margin-bottom: 16px;
                         ">
                             Exclusive Financial Offers
                         </div>
                    
                         <!-- Campaign title -->
                         <h3 style="
                        font-size: 24px;
                        font-weight: 800;
                        line-height: 1.2;
                             margin: 0 0 12px 0;
                        color: #111827;
                             text-align: center;
                         ">
                             ${campaign.name}
                         </h3>
 
                         <!-- Campaign description -->
                    <p style="
                             font-size: 16px;
                        line-height: 1.4;
                             margin: 0 0 20px 0;
                             color: #374151;
                        text-align: center;
                         ">
                             ${campaign.description}
                         </p>
                    
                        <!-- Campaign image -->
                        <div style="
                        width: 100%;
                            height: 200px;
                            border-radius: 16px;
                            overflow: hidden;
                            margin-bottom: 24px;
                            background: #f8f9fa;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">
                            <img src="${campaign.main_image_url}" 
                                 alt="${campaign.name}"
                                 style="width: 100%; height: 100%; object-fit: contain;"
                                 onerror="this.src='https://via.placeholder.com/280x220/F7007C/FFFFFF?text=OFFER'">
                        </div>

                        <!-- Action buttons -->
                        <div style="display: flex; gap: 12px; margin-bottom: 20px;">
                            <button id="mode-popup-cta" style="
                                flex: 1;
                                background: #F7007C;
                        color: white;
                        border: none;
                                padding: 16px 24px;
                                border-radius: 12px;
                        font-size: 16px;
                        font-weight: 600;
                        cursor: pointer;
                                transition: all 0.2s ease;
                            " onmouseover="this.style.background='#E6006F'" onmouseout="this.style.background='#F7007C'">
                        ${campaign.cta_text || 'View Offer'}
                    </button>
                    
                            ${totalCount > 1 ? `
                            <button id="mode-popup-next" style="
                        background: white;
                        color: #6B7280;
                        border: 2px solid #E5E7EB;
                                padding: 16px 20px;
                                border-radius: 12px;
                        font-size: 14px;
                                font-weight: 600;
                        cursor: pointer;
                        transition: all 0.2s ease;
                                white-space: nowrap;
                            " onmouseover="this.style.borderColor='#D1D5DB'; this.style.color='#374151'" onmouseout="this.style.borderColor='#E5E7EB'; this.style.color='#6B7280'">
                                Next ›
                    </button>
                            ` : ''}
                        </div>

                        ${totalCount > 1 ? `
                        <!-- Pagination dots -->
                        <div style="display: flex; justify-content: center; gap: 6px; margin-bottom: 20px;">
                            ${Array.from({length: totalCount}, (_, i) => `
                                <div style="
                                width: 8px; 
                                height: 8px; 
                                border-radius: 50%; 
                                    background: ${i === this.currentCampaignIndex ? '#F7007C' : '#E5E7EB'};
                                    transition: all 0.2s ease;
                                "></div>
                        `).join('')}
                    </div>
                    ` : ''}
                    
                        <!-- Footer -->
                    <div style="
                            text-align: center;
                            font-size: 12px;
                        color: #9CA3AF;
                            line-height: 1.4;
                        ">
                            T&Cs Apply | Powered by <span style="color: #F7007C; font-weight: 600;">Mode</span> • Privacy Policy
                        </div>
                    </div>
                </div>
                </div>
            `;
        }

    attachEventListeners() {
            // Close button
        const closeBtn = document.getElementById('mode-popup-close');
        const overlay = document.getElementById(CONFIG.OVERLAY_ID);
        const ctaBtn = document.getElementById('mode-popup-cta');
        const nextBtn = document.getElementById('mode-popup-next');

            if (closeBtn) {
            closeBtn.addEventListener('click', () => this.hidePopup());
            }

        if (overlay) {
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    this.hidePopup();
                }
            });
        }

        if (ctaBtn) {
            ctaBtn.addEventListener('click', () => this.handleCTAClick());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextCampaign());
        }

        // ESC key
        const escapeHandler = (e) => {
                if (e.key === 'Escape') {
                    this.hidePopup();
                document.removeEventListener('keydown', escapeHandler);
                }
            };
        document.addEventListener('keydown', escapeHandler);
        }

    handleCTAClick() {
        const campaign = this.campaigns[this.currentCampaignIndex];
        this.debug(`🎯 CTA clicked for campaign: ${campaign.name}`);
            
            // Track click
        this.trackClick();
            
        // Open URL
                window.open(campaign.tune_url, '_blank');
            
        // Hide popup
        this.hidePopup();
        }

        nextCampaign() {
            if (this.campaigns.length <= 1) return;

            this.currentCampaignIndex = (this.currentCampaignIndex + 1) % this.campaigns.length;
        this.debug(`➡️ Switching to campaign ${this.currentCampaignIndex + 1}: ${this.campaigns[this.currentCampaignIndex].name}`);
            
            this.updatePopupContent();
                this.resetAutoRotation();

        // Track impression for new campaign
        this.trackImpression();
        }

        updatePopupContent() {
            const popup = document.getElementById(CONFIG.POPUP_ID);
            if (!popup) return;

            // Fade out
            popup.style.opacity = '0.7';

            setTimeout(() => {
            // Remove and recreate
            this.removePopup();
            const popupHTML = this.createPopupHTML();
            document.body.insertAdjacentHTML('beforeend', popupHTML);
            this.attachEventListeners();
                
                // Fade in
            setTimeout(() => {
                const newPopup = document.getElementById(CONFIG.POPUP_ID);
                if (newPopup) {
                    newPopup.style.opacity = '1';
                }
            }, 50);
        }, 150);
        }

        startAutoRotation() {
        if (this.campaigns.length <= 1) return;
        
        this.rotationInterval = setInterval(() => {
                this.nextCampaign();
            }, CONFIG.ROTATION_DELAY);
        }

        stopAutoRotation() {
        if (this.rotationInterval) {
            clearInterval(this.rotationInterval);
            this.rotationInterval = null;
            }
        }

        resetAutoRotation() {
        this.stopAutoRotation();
                this.startAutoRotation();
            }

    hidePopup() {
        this.debug('🚪 Hiding popup');
        
            const popup = document.getElementById(CONFIG.POPUP_ID);
        if (popup) {
            popup.style.opacity = '0';
            popup.style.transform = 'translate(-50%, -50%) scale(0.9)';
        }

            setTimeout(() => {
                this.removePopup();
            }, CONFIG.ANIMATION_DURATION);

        this.isVisible = false;
        this.stopAutoRotation();
        }

        removePopup() {
            const overlay = document.getElementById(CONFIG.OVERLAY_ID);
            if (overlay) {
                overlay.remove();
            }
        }

        async trackImpression() {
        if (this.campaigns.length === 0) return;
        
            const campaign = this.campaigns[this.currentCampaignIndex];

            try {
                await fetch(`${CONFIG.API_BASE}/impression`, {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        campaign_id: campaign.id,
                        property_code: this.config.property,
                        session_id: this.sessionId,
                    placement: this.config.placement
                    })
                });

            this.debug(`📊 Tracked impression for campaign: ${campaign.name}`);
            } catch (error) {
            this.debug('❌ Failed to track impression:', error);
            }
        }

    async trackClick() {
        if (this.campaigns.length === 0) return;
        
        const campaign = this.campaigns[this.currentCampaignIndex];
        
            try {
                await fetch(`${CONFIG.API_BASE}/click`, {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        campaign_id: campaign.id,
                        property_code: this.config.property,
                        session_id: this.sessionId,
                    placement: this.config.placement
                    })
                });

            this.debug(`🎯 Tracked click for campaign: ${campaign.name}`);
            } catch (error) {
            this.debug('❌ Failed to track click:', error);
            }
        }

        generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
        }

    debug(message, ...args) {
            if (this.config.debug) {
            console.log('[ModePopup]', message, ...args);
            }
        }
    }

    // Create global instance
    window.ModePopup = new ModePopup();

// Auto-initialize if script has data attributes
    document.addEventListener('DOMContentLoaded', () => {
        const script = document.querySelector('script[src*="popup.js"]');
        if (script) {
            const property = script.getAttribute('data-property');
            const placement = script.getAttribute('data-placement');
            const frequency = script.getAttribute('data-frequency');
            
            if (property) {
                window.ModePopup.init({
                property: property,
                    placement: placement || 'thankyou',
                    frequency: frequency || 'session'
                });
            }
        }
    });

}(); 