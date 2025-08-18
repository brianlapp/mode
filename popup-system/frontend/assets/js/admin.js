/**
 * Mode Popup Campaign Manager - Admin Interface
 * JavaScript functionality for Mike's campaign management dashboard
 * CACHE BUSTER: 2025-01-27-EDIT-MODAL-FIX
 */

class CampaignManager {
    constructor() {
        this.baseURL = '/api';
        this.campaigns = [];
        this.properties = ['mff', 'mmm', 'mcad', 'mmd'];
        this.propertyNames = {
            'mff': 'ModeFreeFinds',
            'mmm': 'ModeMarketMunchies', 
            'mcad': 'ModeClassActionsDaily',
            'mmd': 'ModeMobileDaily'
        };
        this.init();
    }

    async init() {
        console.log('🚀 Mode Campaign Manager initializing...');
        await this.loadCampaigns();
        await this.loadPropertiesGrid();
        this.setupEventListeners();
        await this.updateStats();
        
        // Set up auto-refresh for real-time data (every 30 seconds)
        setInterval(async () => {
            await this.updateStats();
        }, 30000);
        
        console.log('📊 Auto-refresh enabled: Dashboard will update every 30 seconds');
    }

    async loadCampaigns() {
        try {
            console.log(`🔄 Fetching campaigns from: ${this.baseURL}/campaigns`);
            const response = await fetch(`${this.baseURL}/campaigns`);
            console.log(`📡 Response status: ${response.status}`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            this.campaigns = await response.json();
            console.log(`✅ Loaded ${this.campaigns.length} campaigns:`, this.campaigns);
            this.renderCampaigns();
        } catch (error) {
            console.error('❌ Failed to load campaigns:', error);
            console.error('❌ Error details:', error.message);
            this.showAlert(`Failed to load campaigns: ${error.message}`, 'error');
        }
    }

    renderCampaigns() {
        console.log(`🎨 Rendering ${this.campaigns.length} campaigns`);
        const tableBody = document.getElementById('campaignsTableBody');
        
        if (!tableBody) {
            console.error('❌ Table body element not found!');
            return;
        }

        if (this.campaigns.length === 0) {
            console.log('⚠️ No campaigns to display');
            tableBody.innerHTML = `
                <tr>
                    <td colspan="1" class="px-6 py-4 text-center text-gray-500">
                        No campaigns yet<br>
                        <span class="text-sm">Click "Add New Campaign" to get started</span>
                    </td>
                </tr>
            `;
            return;
        }

        console.log(`✅ Rendering ${this.campaigns.length} campaigns in table`);

        tableBody.innerHTML = this.campaigns.map(campaign => `
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center">
                            <div class="h-10 w-10 flex-shrink-0">
                                <img class="h-10 w-10 rounded-full object-cover" 
                                     src="${campaign.logo_url}" 
                                     alt="${campaign.name}"
                                     onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' fill=\\'%23F7007C\\' viewBox=\\'0 0 24 24\\'%3E%3Cpath d=\\'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z\\'/%3E%3C/svg%3E'">
                            </div>
                            <div class="ml-4">
                                <div class="text-sm font-medium text-gray-900">${campaign.name}</div>
                                <div class="text-sm text-gray-500 truncate" style="max-width: 200px;">${campaign.tune_url}</div>
                                <div class="text-xs text-gray-500 mt-1">Show on all domains • Auto-configured</div>
                            </div>
                        </div>
                        <div class="flex items-center space-x-4">
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${campaign.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                                ${campaign.active ? 'Active' : 'Inactive'}
                            </span>
                            <div class="flex space-x-2 text-sm">
                                <button onclick="campaignManager.editCampaign(${campaign.id})" 
                                        class="text-mode-pink hover:text-mode-pink-dark">Edit</button>
                                <button onclick="campaignManager.showPropertyModal(${campaign.id})" 
                                        class="text-mode-blue hover:text-mode-blue-dark">Properties</button>
                                <button onclick="campaignManager.toggleCampaign(${campaign.id}, ${!campaign.is_active})" 
                                        class="text-gray-600 hover:text-gray-900">
                                    ${campaign.active ? 'Deactivate' : 'Activate'}
                                </button>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
        `).join('');
    }

    async loadPropertiesGrid() {
        try {
            console.log('🏢 Loading properties grid with featured campaign settings...');
            
            const propertiesGrid = document.getElementById('propertiesGrid');
            if (!propertiesGrid) return;

            // Build property cards with featured campaign dropdowns
            const propertyCards = await Promise.all(this.properties.map(async (propertyCode) => {
                const propertyName = this.propertyNames[propertyCode];
                
                // Get current featured campaign for this property
                let currentFeaturedId = null;
                try {
                    const response = await fetch(`${this.baseURL}/properties/${propertyCode}/featured`);
                    if (response.ok) {
                        const data = await response.json();
                        currentFeaturedId = data.featured_campaign_id;
                    }
                } catch (error) {
                    console.log(`No featured campaign set for ${propertyCode}`);
                }
                
                return `
                    <div class="property-card border border-gray-200 rounded-lg p-4 bg-gradient-to-br from-gray-50 to-white">
                        <div class="flex items-center mb-4">
                            <div class="w-12 h-12 bg-mode-pink rounded-full flex items-center justify-center text-white font-bold text-lg">
                                ${propertyCode.toUpperCase()}
                            </div>
                            <div class="ml-3">
                                <h4 class="font-semibold text-gray-900">${propertyName}</h4>
                                <p class="text-sm text-gray-500">${propertyCode}.com</p>
                            </div>
                        </div>
                        
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-2">
                                Featured Campaign
                            </label>
                            <select id="featured-${propertyCode}" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-mode-pink text-sm">
                                <option value="">No featured campaign</option>
                                ${this.campaigns.map(campaign => 
                                    `<option value="${campaign.id}" ${currentFeaturedId == campaign.id ? 'selected' : ''}>${campaign.name}</option>`
                                ).join('')}
                            </select>
                            <p class="text-xs text-gray-500 mt-1">🌟 Shows first, then others by RPM</p>
                        </div>
                        
                        <button onclick="campaignManager.saveFeaturedCampaign('${propertyCode}')" 
                                class="w-full bg-mode-pink text-white px-4 py-2 rounded-md hover:bg-mode-pink-dark transition-colors text-sm font-medium">
                            Save Featured
                        </button>
                    </div>
                `;
            }));

            propertiesGrid.innerHTML = propertyCards.join('');
            
        } catch (error) {
            console.error('❌ Failed to load properties grid:', error);
            this.showAlert(`Failed to load properties: ${error.message}`, 'error');
        }
    }

    setupEventListeners() {
        // Add Campaign button
        const addBtn = document.getElementById('addCampaignBtn');
        if (addBtn) {
            addBtn.addEventListener('click', () => this.showAddCampaignModal());
        }

        // Modal close buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-close')) {
                this.closeModals();
            }
        });

        // Form submissions
        const addForm = document.getElementById('addCampaignForm');
        if (addForm) {
            addForm.addEventListener('submit', (e) => this.handleAddCampaign(e));
        }

        // Live Preview Functionality
        this.setupLivePreview();

        // Featured Toggle Functionality - MOVED TO PROPERTIES SECTION
        // this.setupFeaturedToggle(); // Removed - now property-specific

        // Image preview for URL inputs (small previews)
        const logoInput = document.getElementById('logo_url');
        const imageInput = document.getElementById('main_image_url');
        
        if (logoInput) {
            logoInput.addEventListener('input', (e) => {
                const preview = document.getElementById('logoPreview');
                if (preview && e.target.value) {
                    preview.src = e.target.value;
                    preview.classList.remove('hidden');
                }
            });
        }
        
        if (imageInput) {
            imageInput.addEventListener('input', (e) => {
                const preview = document.getElementById('imagePreview');
                if (preview && e.target.value) {
                    preview.src = e.target.value;
                    preview.classList.remove('hidden');
                }
            });
        }
    }

    setupLivePreview() {
        // Get all the form inputs that affect the preview
        const nameInput = document.getElementById('name');
        const descriptionInput = document.getElementById('description');
        const ctaInput = document.getElementById('cta_text');
        const logoInput = document.getElementById('logo_url');
        const imageInput = document.getElementById('main_image_url');

        // Get all the preview elements
        const previewTitle = document.getElementById('preview-title');
        const previewDescription = document.getElementById('preview-description');
        const previewCta = document.getElementById('preview-cta');
        const previewLogo = document.getElementById('preview-logo');
        const previewImage = document.getElementById('preview-main-image');

        // Real-time update function
        const updatePreview = () => {
            if (previewTitle && nameInput) {
                previewTitle.textContent = nameInput.value || 'Campaign Name';
            }
            
            if (previewDescription && descriptionInput) {
                previewDescription.textContent = descriptionInput.value || 'Campaign description will appear here...';
            }
            
            if (previewCta && ctaInput) {
                previewCta.textContent = ctaInput.value || 'View Offer';
                // Update button color based on Mode branding
                if (ctaInput.value) {
                    previewCta.style.background = '#7C3AED'; // Purple like approved design
                } else {
                    previewCta.style.background = '#7C3AED';
                }
            }
            
            if (previewLogo && logoInput && logoInput.value) {
                previewLogo.src = logoInput.value;
                // Keep background transparent - no gray ring!
                const logoCircle = document.getElementById('preview-logo-circle');
                if (logoCircle) {
                    logoCircle.style.background = 'transparent';
                }
            }
            
            if (previewImage && imageInput && imageInput.value) {
                previewImage.src = imageInput.value;
            }
        };

        // Add event listeners for real-time updates
        if (nameInput) nameInput.addEventListener('input', updatePreview);
        if (descriptionInput) descriptionInput.addEventListener('input', updatePreview);
        if (ctaInput) ctaInput.addEventListener('input', updatePreview);
        if (logoInput) logoInput.addEventListener('input', updatePreview);
        if (imageInput) imageInput.addEventListener('input', updatePreview);

        console.log('✨ Live preview functionality activated!');
    }

    // Featured toggle functionality moved to Properties section
    // setupFeaturedToggle() - REMOVED: Featured campaigns now managed per-property

    showAddCampaignModal() {
        const modal = document.getElementById('addCampaignModal');
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
    }

    closeModals() {
        const modal = document.getElementById('addCampaignModal');
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
        
        // Reset forms
        const forms = document.querySelectorAll('form');
        forms.forEach(form => form.reset());
        
        // Reset image previews
        const previews = document.querySelectorAll('.image-preview');
        previews.forEach(preview => preview.classList.add('hidden'));
    }

    async handleAddCampaign(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const campaignData = {
            name: formData.get('name'),
            tune_url: formData.get('tune_url'),
            logo_url: formData.get('logo_url'),
            main_image_url: formData.get('main_image_url'),
            description: formData.get('description'),
            cta_text: formData.get('cta_text') || 'View Offer'
            // featured: removed - now managed per-property
        };

        // Validate required fields
        if (!campaignData.name || !campaignData.tune_url || !campaignData.description) {
            this.showAlert('Please fill in all required fields.', 'error');
            return;
        }

        try {
            const response = await fetch(`${this.baseURL}/campaigns`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(campaignData)
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const result = await response.json();
            console.log('✅ Campaign created:', result);

            // Initialize default property: enable only current site at 100%
            try {
                const newId = result.id;
                const host = (window.location.hostname || '').toLowerCase();
                let propertyCode = 'mff';
                if (host.includes('modefreefinds')) propertyCode = 'mff';
                else if (host.includes('marketmunchies')) propertyCode = 'mmm';
                else if (host.includes('modeclassactions')) propertyCode = 'mcad';
                else if (host.includes('modemobiledaily')) propertyCode = 'mmd';

                const initSettings = {};
                for (const prop of this.properties) {
                    initSettings[prop] = {
                        active: prop === propertyCode,
                        visibility_percentage: prop === propertyCode ? 100 : 0,
                        impression_cap_daily: null,
                        click_cap_daily: null
                    };
                }

                const propResp = await fetch(`${this.baseURL}/campaigns/${newId}/properties`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(initSettings)
                });
                if (!propResp.ok) {
                    console.warn('⚠️ Failed to initialize default property settings');
                }
            } catch (e) {
                console.warn('⚠️ Default property init error:', e);
            }

            this.showAlert('Campaign created successfully!', 'success');
            this.closeModals();
            await this.loadCampaigns(); // Refresh the list
            this.updateStats();
            
        } catch (error) {
            console.error('❌ Failed to create campaign:', error);
            this.showAlert('Failed to create campaign. Please try again.', 'error');
        }
    }

    async editCampaign(campaignId) {
        console.log(`🔧 EDIT MODAL - Clicked for campaign ID: ${campaignId}`);
        const campaign = this.campaigns.find(c => c.id === campaignId);
        
        if (!campaign) {
            console.error(`❌ Campaign with ID ${campaignId} not found in campaigns array:`, this.campaigns);
            this.showAlert(`Campaign not found! ID: ${campaignId}`, 'error');
            return;
        }

        console.log(`✅ Found campaign for EDITING:`, campaign);
        // Force show editable campaign form modal (not preview!)
        this.showEditCampaignModal(campaign);
        console.log(`🎯 Called showEditCampaignModal() - should show EDITABLE form!`);
    }

    showEditCampaignModal(campaign) {
        // Create editable campaign modal
        const modalHTML = `
            <div id="editCampaignModal" class="modal fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
                <div class="modal-content bg-white p-8 rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-2xl font-bold text-gray-900">Edit Campaign: ${campaign.name}</h3>
                        <button class="modal-close text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
                    </div>
                    
                    <form id="editCampaignForm" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        <!-- Left Column: Editable Form -->
                        <div class="space-y-4">
                            <h4 class="text-lg font-semibold text-gray-800">Campaign Details</h4>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Campaign Name</label>
                                <input type="text" id="edit_name" value="${campaign.name}" 
                                       class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-mode-pink">
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                                <textarea id="edit_description" rows="3" 
                                          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-mode-pink">${campaign.description || ''}</textarea>
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">CTA Button Text</label>
                                <input type="text" id="edit_cta_text" value="${campaign.cta_text}" 
                                       class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-mode-pink">
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Logo URL (Circle Image)</label>
                                <input type="url" id="edit_logo_url" value="${campaign.logo_url}" 
                                       class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-mode-pink"
                                       placeholder="https://example.com/logo.png">
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Main Image URL (Campaign Image)</label>
                                <input type="url" id="edit_main_image_url" value="${campaign.main_image_url}" 
                                       class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-mode-pink"
                                       placeholder="https://example.com/campaign-image.jpg">
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Tune URL (Editable for Subsource Tracking)</label>
                                <input type="url" id="edit_tune_url" value="${campaign.tune_url}" 
                                       class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-mode-pink"
                                       placeholder="https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup">
                                <div class="text-xs text-gray-500 mt-1">
                                    💡 Add &aff_sub5=popup_[offerName] for enhanced tracking
                                </div>
                            </div>
                            
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Offer ID</label>
                                    <input type="text" value="${campaign.offer_id || ''}" readonly
                                           class="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Aff ID</label>
                                    <input type="text" id="edit_aff_id" value="${campaign.aff_id || ''}"
                                           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-mode-pink">
                                </div>
                            </div>
                        </div>
                        
                        <!-- Right Column: Live Preview -->
                        <div>
                            <h4 class="text-lg font-semibold text-gray-800 mb-4">Live Preview</h4>
                            
                            <!-- Mode Popup Preview -->
                            <div id="edit-popup-preview" style="
                                max-width: 340px;
                                width: 100%;
                                margin: 0 auto;
                                background: white;
                                border-radius: 24px;
                                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                                overflow: hidden;
                                position: relative;
                                border: 2px solid #e5e7eb;
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
                                     border: none;
                                 ">
                                     <img id="edit-preview-logo" 
                                         src="${campaign.logo_url || 'https://via.placeholder.com/56/F7007C/FFFFFF?text=LOGO'}" 
                                         alt="Logo"
                                         style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">
                                </div>
                                
                                <!-- Main Content -->
                                <div style="padding: 24px; padding-top: 100px; text-align: center;">
                                    <!-- Tagline Pill -->
                                    <div style="
                                        background: #F3F4F6;
                                        color: #6B7280;
                                        padding: 6px 12px;
                                        border-radius: 16px;
                                        font-size: 12px;
                                        margin-bottom: 24px;
                                        display: inline-block;
                                        font-weight: 500;
                                    ">Mode Campaign Preview</div>
                                    
                                    <!-- Title -->
                                    <h2 id="edit-preview-title" style="
                                        margin: 0 0 8px 0;
                                        font-size: 24px;
                                        font-weight: 800;
                                        line-height: 1.2;
                                        color: #111827;
                                    ">${campaign.name}</h2>
                                    
                                                                         <!-- Campaign Image -->
                                     <div style="margin: 16px 0; display: flex; align-items: center; justify-content: center;">
                                         <img id="edit-preview-main-image" 
                                              src="${campaign.main_image_url || 'https://via.placeholder.com/280x220/F7007C/FFFFFF?text=No+Image'}" 
                                              alt="Campaign" 
                                              style="width: 280px; height: 220px; object-fit: contain; object-position: center; border-radius: 12px; background-color: #f8f9fa;">
                                     </div>
                                    
                                    <!-- Description -->
                                    <p id="edit-preview-description" style="
                                        color: #6B7280;
                                        font-size: 14px;
                                        line-height: 1.4;
                                        margin: 16px 0 24px 0;
                                        text-align: center;
                                    ">${campaign.description || 'Campaign description will appear here...'}</p>
                                    
                                    <!-- CTA Button -->
                                    <button id="edit-preview-cta" style="
                                        width: 100%;
                                        background: #7C3AED;
                                        color: white;
                                        border: none;
                                        padding: 16px;
                                        border-radius: 16px;
                                        font-size: 16px;
                                        font-weight: 600;
                                        cursor: pointer;
                                        margin-bottom: 12px;
                                    ">${campaign.cta_text}</button>
                                    
                                    <!-- Next Button -->
                                    <button style="
                                        width: 100%;
                                        background: white;
                                        color: #6B7280;
                                        border: 2px solid #E5E7EB;
                                        padding: 14px;
                                        border-radius: 16px;
                                        font-size: 14px;
                                        font-weight: 500;
                                        cursor: pointer;
                                        margin-bottom: 16px;
                                    ">Next ></button>
                                    
                                    <!-- Pagination Dots -->
                                    <div style="text-align: center; margin-bottom: 16px;">
                                        <span style="width: 8px; height: 8px; background: #374151; border-radius: 50%; margin: 0 3px; display: inline-block;"></span>
                                        <span style="width: 8px; height: 8px; background: #D1D5DB; border-radius: 50%; margin: 0 3px; display: inline-block;"></span>
                                        <span style="width: 8px; height: 8px; background: #D1D5DB; border-radius: 50%; margin: 0 3px; display: inline-block;"></span>
                                    </div>
                                    
                                    <!-- Footer -->
                                    <div style="
                                        color: #9CA3AF;
                                        font-size: 11px;
                                        text-align: center;
                                        line-height: 1.3;
                                    ">T&Cs Apply | Powered by <strong>Mode</strong> • Privacy Policy</div>
                                </div>
                            </div>
                        </div>
                    </form>
                    
                    <div class="flex justify-end space-x-3 mt-8">
                        <button class="modal-close px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
                            Cancel
                        </button>
                        <button type="button" onclick="campaignManager.saveEditedCampaign(${campaign.id})" 
                                class="px-4 py-2 bg-mode-pink text-white rounded-md hover:bg-mode-pink/80">
                            Save Changes
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal if any
        const existingModal = document.getElementById('editCampaignModal');
        if (existingModal) existingModal.remove();

        // Add new modal
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Show modal
        const modal = document.getElementById('editCampaignModal');
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        // Add event listeners for closing
        const closeButtons = modal.querySelectorAll('.modal-close');
        closeButtons.forEach(button => {
            button.addEventListener('click', () => {
                modal.remove();
            });
        });
        
        // Close on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
        
        // Set up real-time preview updates
        this.setupEditLivePreview();
    }

    setupEditLivePreview() {
        // Get all the form inputs that affect the preview
        const nameInput = document.getElementById('edit_name');
        const descriptionInput = document.getElementById('edit_description');
        const ctaInput = document.getElementById('edit_cta_text');
        const logoInput = document.getElementById('edit_logo_url');
        const imageInput = document.getElementById('edit_main_image_url');

        // Get all the preview elements
        const previewTitle = document.getElementById('edit-preview-title');
        const previewDescription = document.getElementById('edit-preview-description');
        const previewCta = document.getElementById('edit-preview-cta');
        const previewLogo = document.getElementById('edit-preview-logo');
        const previewImage = document.getElementById('edit-preview-main-image');

        // Real-time update function
        const updatePreview = () => {
            if (previewTitle && nameInput) {
                previewTitle.textContent = nameInput.value || 'Campaign Name';
            }
            
            if (previewDescription && descriptionInput) {
                previewDescription.textContent = descriptionInput.value || 'Campaign description will appear here...';
            }
            
            if (previewCta && ctaInput) {
                previewCta.textContent = ctaInput.value || 'View Offer';
            }
            
            if (previewLogo && logoInput && logoInput.value) {
                previewLogo.src = logoInput.value;
                previewLogo.onerror = () => {
                    previewLogo.src = 'https://via.placeholder.com/56/F7007C/FFFFFF?text=LOGO';
                };
            }
            
            if (previewImage && imageInput && imageInput.value) {
                previewImage.src = imageInput.value;
                previewImage.onerror = () => {
                    previewImage.src = 'https://via.placeholder.com/280x220/F7007C/FFFFFF?text=No+Image';
                };
            }
        };

        // Add event listeners for real-time updates
        if (nameInput) nameInput.addEventListener('input', updatePreview);
        if (descriptionInput) descriptionInput.addEventListener('input', updatePreview);
        if (ctaInput) ctaInput.addEventListener('input', updatePreview);
        if (logoInput) logoInput.addEventListener('input', updatePreview);
        if (imageInput) imageInput.addEventListener('input', updatePreview);

        console.log('✨ Edit modal live preview functionality activated!');
    }

    async saveEditedCampaign(campaignId) {
        console.log(`💾 Saving changes for campaign ID: ${campaignId}`);
        
        // Get form values
        const name = document.getElementById('edit_name').value;
        const description = document.getElementById('edit_description').value;
        const cta_text = document.getElementById('edit_cta_text').value;
        const logo_url = document.getElementById('edit_logo_url').value;
        const main_image_url = document.getElementById('edit_main_image_url').value;
        const tune_url = document.getElementById('edit_tune_url').value;
        const aff_id = document.getElementById('edit_aff_id').value;
        
        // Validate required fields
        if (!name.trim()) {
            this.showAlert('Campaign name is required!', 'error');
            return;
        }
        
        if (!cta_text.trim()) {
            this.showAlert('CTA button text is required!', 'error');
            return;
        }
        
        if (!tune_url.trim()) {
            this.showAlert('Tune URL is required!', 'error');
            return;
        }
        
        const updateData = {
            name: name.trim(),
            description: description.trim(),
            cta_text: cta_text.trim(),
            logo_url: logo_url.trim(),
            main_image_url: main_image_url.trim(),
            tune_url: tune_url.trim(),
            aff_id: aff_id.trim()
        };
        
        try {
            console.log('📡 Sending update request:', updateData);
            const response = await fetch(`${this.baseURL}/campaigns/${campaignId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updateData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const result = await response.json();
            console.log('✅ Campaign updated successfully:', result);
            
            // Close modal
            const modal = document.getElementById('editCampaignModal');
            if (modal) modal.remove();
            
            // Reload campaigns to show updated data
            await this.loadCampaigns();
            
            this.showAlert('Campaign updated successfully!', 'success');
            
        } catch (error) {
            console.error('❌ Failed to update campaign:', error);
            this.showAlert(`Failed to update campaign: ${error.message}`, 'error');
        }
    }

    showCampaignPreview(campaign) {
        // Create campaign preview modal
        const modalHTML = `
            <div id="campaignPreviewModal" class="modal fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
                <div class="modal-content bg-white p-8 rounded-lg shadow-xl max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-2xl font-bold text-gray-900">Campaign Preview: ${campaign.name}</h3>
                        <button class="modal-close text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
                    </div>
                    
                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        <!-- Campaign Details -->
                        <div class="space-y-4">
                            <h4 class="text-lg font-semibold text-gray-800">Campaign Details</h4>
                            
                            <div class="space-y-3">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700">Campaign Name</label>
                                    <p class="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded">${campaign.name}</p>
                                </div>
                                
                                <div>
                                    <label class="block text-sm font-medium text-gray-700">Description</label>
                                    <p class="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded">${campaign.description || 'No description provided'}</p>
                                </div>
                                
                                <div>
                                    <label class="block text-sm font-medium text-gray-700">CTA Button Text</label>
                                    <p class="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded">${campaign.cta_text}</p>
                                </div>
                                
                                <div>
                                    <label class="block text-sm font-medium text-gray-700">Tune URL</label>
                                    <p class="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded break-all">${campaign.tune_url}</p>
                                </div>
                                
                                <div>
                                    <label class="block text-sm font-medium text-gray-700">Status</label>
                                    <span class="mt-1 inline-flex px-2 py-1 text-xs font-medium rounded-full ${campaign.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                                        ${campaign.active ? 'Active' : 'Inactive'}
                                    </span>
                                </div>
                                
                                <div>
                                    <label class="block text-sm font-medium text-gray-700">Created</label>
                                    <p class="mt-1 text-sm text-gray-900 bg-gray-50 p-2 rounded">${new Date(campaign.created_at).toLocaleDateString()}</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Live Preview -->
                        <div>
                            <h4 class="text-lg font-semibold text-gray-800 mb-4">Live Preview</h4>
                            
                            <!-- Mode Popup Preview -->
                            <div style="
                                max-width: 340px;
                                width: 100%;
                                margin: 0 auto;
                                background: white;
                                border-radius: 24px;
                                box-shadow: 0 20px 60px rgba(0,0,0,0.2);
                                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                                overflow: hidden;
                                position: relative;
                                border: 2px solid #e5e7eb;
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
                                    <img src="${campaign.logo_url || 'https://via.placeholder.com/56/F7007C/FFFFFF?text=LOGO'}" 
                                         alt="Logo"
                                         style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">
                                </div>
                                
                                <!-- Main Content -->
                                <div style="padding: 24px; padding-top: 100px; text-align: center;">
                                    <!-- Tagline Pill -->
                                    <div style="
                                        background: #F3F4F6;
                                        color: #6B7280;
                                        padding: 6px 12px;
                                        border-radius: 16px;
                                        font-size: 12px;
                                        margin-bottom: 24px;
                                        display: inline-block;
                                        font-weight: 500;
                                    ">Mode Campaign Preview</div>
                                    
                                    <!-- Title -->
                                    <h2 style="
                                        margin: 0 0 8px 0;
                                        font-size: 24px;
                                        font-weight: 800;
                                        line-height: 1.2;
                                        color: #111827;
                                    ">${campaign.name}</h2>
                                    
                                    <!-- Campaign Image -->
                                    <div style="margin: 16px 0; display: flex; align-items: center; justify-content: center;">
                                        <img src="${campaign.main_image_url || 'https://via.placeholder.com/280x220/F7007C/FFFFFF?text=No+Image'}" 
                                             alt="Campaign" 
                                             style="width: 280px; height: 220px; object-fit: cover; border-radius: 12px;">
                                    </div>
                                    
                                    <!-- Description -->
                                    <p style="
                                        color: #6B7280;
                                        font-size: 14px;
                                        line-height: 1.4;
                                        margin: 16px 0 24px 0;
                                        text-align: center;
                                    ">${campaign.description || 'Campaign description will appear here...'}</p>
                                    
                                    <!-- CTA Button -->
                                    <button style="
                                        width: 100%;
                                        background: #7C3AED;
                                        color: white;
                                        border: none;
                                        padding: 16px;
                                        border-radius: 16px;
                                        font-size: 16px;
                                        font-weight: 600;
                                        cursor: pointer;
                                        margin-bottom: 12px;
                                    ">${campaign.cta_text}</button>
                                    
                                    <!-- Next Button -->
                                    <button style="
                                        width: 100%;
                                        background: white;
                                        color: #6B7280;
                                        border: 2px solid #E5E7EB;
                                        padding: 14px;
                                        border-radius: 16px;
                                        font-size: 14px;
                                        font-weight: 500;
                                        cursor: pointer;
                                        margin-bottom: 16px;
                                    ">Next ></button>
                                    
                                    <!-- Pagination Dots -->
                                    <div style="text-align: center; margin-bottom: 16px;">
                                        <span style="width: 8px; height: 8px; background: #374151; border-radius: 50%; margin: 0 3px; display: inline-block;"></span>
                                        <span style="width: 8px; height: 8px; background: #D1D5DB; border-radius: 50%; margin: 0 3px; display: inline-block;"></span>
                                        <span style="width: 8px; height: 8px; background: #D1D5DB; border-radius: 50%; margin: 0 3px; display: inline-block;"></span>
                                    </div>
                                    
                                    <!-- Footer -->
                                    <div style="
                                        color: #9CA3AF;
                                        font-size: 11px;
                                        text-align: center;
                                        line-height: 1.3;
                                    ">T&Cs Apply | Powered by <strong>Mode</strong> • Privacy Policy</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="flex justify-end space-x-3 mt-8">
                        <button class="modal-close px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
                            Close
                        </button>
                        <button onclick="campaignManager.manageProperties(${campaign.id})" 
                                class="px-4 py-2 bg-mode-blue text-white rounded-md hover:bg-mode-blue/80">
                            Manage Properties
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal if any
        const existingModal = document.getElementById('campaignPreviewModal');
        if (existingModal) existingModal.remove();

        // Add new modal
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Show modal
        const modal = document.getElementById('campaignPreviewModal');
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        // Add event listeners for closing
        const closeButtons = modal.querySelectorAll('.modal-close');
        closeButtons.forEach(button => {
            button.addEventListener('click', () => {
                modal.remove();
            });
        });
        
        // Close on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    manageProperties(campaignId) {
        const campaign = this.campaigns.find(c => c.id === campaignId);
        if (!campaign) return;

        // Show property management modal
        this.showPropertyModal(campaign);
    }

    showPropertyModal(campaignOrId) {
        // Handle both campaign object and campaign ID
        const campaign = typeof campaignOrId === 'object' ? campaignOrId : this.campaigns.find(c => c.id == campaignOrId);
        
        if (!campaign) {
            console.error('❌ Campaign not found for modal:', campaignOrId);
            this.showAlert('Campaign not found', 'error');
            return;
        }
        
        console.log('🔍 DEBUG: Opening properties modal for campaign:', campaign);
        
        // Create dynamic property modal
        const modalHTML = `
            <div id="propertyModal" class="modal fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
                <div class="modal-content bg-white p-8 rounded-lg shadow-xl max-w-2xl w-full mx-4">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-xl font-bold text-gray-900">Property Settings: ${campaign.name}</h3>
                        <button class="modal-close text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
                    </div>
                    
                    <div class="space-y-6">
                        ${this.properties.map(prop => `
                            <div class="border rounded-lg p-4">
                                <div class="flex items-center justify-between mb-3">
                                    <h4 class="font-medium text-gray-900">${this.propertyNames[prop]}</h4>
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" class="sr-only peer" 
                                               id="active_${prop}_${campaign.id}" checked>
                                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-mode-pink/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-mode-pink"></div>
                                    </label>
                                </div>
                                <!-- Featured Campaign Toggle -->
                                <div class="mb-4 p-3 border border-yellow-200 rounded-lg bg-gradient-to-r from-yellow-50 to-orange-50">
                                    <div class="flex items-center justify-between">
                                        <div class="flex-1">
                                            <label class="flex items-center cursor-pointer">
                                                <input type="checkbox" 
                                                       id="featured_${prop}_${campaign.id}" 
                                                       class="sr-only peer"
                                                       onchange="campaignManager.handleFeaturedToggle('${prop}', ${campaign.id}, this.checked)">
                                                <div class="relative">
                                                    <div class="w-11 h-6 bg-gray-200 rounded-full shadow-inner toggle-bg"></div>
                                                    <div class="absolute w-4 h-4 bg-white rounded-full shadow toggle-dot transition-transform duration-200 ease-in-out transform translate-x-1 top-1 left-1"></div>
                                                </div>
                                                <span class="ml-3 text-sm font-medium text-gray-700">Featured Campaign</span>
                                            </label>
                                            <p class="text-xs text-gray-500 mt-1 ml-14">🌟 Show this campaign first on ${this.propertyNames[prop]}, then others by RPM</p>
                                        </div>

                                    </div>
                                </div>

                                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-2">
                                            Visibility Percentage: <span id="visibility_${prop}_${campaign.id}_display">100%</span>
                                        </label>
                                        <input type="range" min="0" max="100" value="100" 
                                               class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                                               id="visibility_${prop}_${campaign.id}"
                                               oninput="document.getElementById('visibility_${prop}_${campaign.id}_display').textContent = this.value + '%'">
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-2">Daily Impression Cap (EST)</label>
                                        <input type="number" min="0" step="1" placeholder="No Cap"
                                               id="imp_cap_${prop}_${campaign.id}" class="form-input w-full" />
                                    </div>
                                    <div>
                                        <label class="block text-sm font-medium text-gray-700 mb-2">Daily Click Cap (EST)</label>
                                        <input type="number" min="0" step="1" placeholder="No Cap"
                                               id="clk_cap_${prop}_${campaign.id}" class="form-input w-full" />
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    
                    <div class="flex justify-end space-x-3 mt-8">
                        <button class="modal-close px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
                            Cancel
                        </button>
                        <button onclick="campaignManager.savePropertySettings(${campaign.id})" 
                                class="px-4 py-2 bg-mode-pink text-white rounded-md hover:bg-mode-pink-dark">
                            Save Settings
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal if any
        const existingModal = document.getElementById('propertyModal');
        if (existingModal) existingModal.remove();

        // Add new modal
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Show modal
        const modal = document.getElementById('propertyModal');
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        // Add event listeners for closing
        const closeButtons = modal.querySelectorAll('.modal-close');
        closeButtons.forEach(button => {
            button.addEventListener('click', () => {
                modal.remove();
            });
        });
        
        // Close on background click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
        
        // Load existing property settings
        this.loadPropertySettings(campaign.id);
    }

    async loadPropertySettings(campaignId) {
        try {
            console.log('📄 Loading property settings for campaign:', campaignId);
            const response = await fetch(`${this.baseURL}/campaigns/${campaignId}/properties`);
            
            if (!response.ok) {
                console.warn('⚠️ No existing property settings found, status:', response.status);
                if (response.status === 500) {
                    console.warn('⚠️ Server error - will use default settings');
                }
                return;
            }
            
            const settings = await response.json();
            console.log('✅ Loaded property settings:', settings);
            console.log('🔍 DEBUG: Settings array length:', settings.length);
            
            // Populate form fields with existing values
            settings.forEach(setting => {
                const prop = setting.property_code;
                console.log(`🔍 DEBUG: Loading settings for ${prop}:`, setting);
                
                // Set active checkbox
                const activeCheckbox = document.getElementById(`active_${prop}_${campaignId}`);
                console.log(`🔍 DEBUG: Active checkbox for ${prop}:`, activeCheckbox ? 'found' : 'NOT FOUND');
                if (activeCheckbox) {
                    activeCheckbox.checked = setting.active;
                    console.log(`🔍 DEBUG: Set ${prop} active to:`, setting.active);
                }
                
                // Set visibility slider
                const visibilitySlider = document.getElementById(`visibility_${prop}_${campaignId}`);
                const visibilityDisplay = document.getElementById(`visibility_${prop}_${campaignId}_display`);
                console.log(`🔍 DEBUG: Visibility elements for ${prop}:`, {
                    slider: visibilitySlider ? 'found' : 'NOT FOUND',
                    display: visibilityDisplay ? 'found' : 'NOT FOUND'
                });
                if (visibilitySlider && visibilityDisplay) {
                    visibilitySlider.value = setting.visibility_percentage;
                    visibilityDisplay.textContent = setting.visibility_percentage + '%';
                    console.log(`🔍 DEBUG: Set ${prop} visibility to:`, setting.visibility_percentage);
                }
                
                // Set impression cap
                const impCapInput = document.getElementById(`imp_cap_${prop}_${campaignId}`);
                if (impCapInput && setting.impression_cap_daily !== null) {
                    impCapInput.value = setting.impression_cap_daily;
                }
                
                // Set click cap
                const clkCapInput = document.getElementById(`clk_cap_${prop}_${campaignId}`);
                if (clkCapInput && setting.click_cap_daily !== null) {
                    clkCapInput.value = setting.click_cap_daily;
                }
            });

            // Load featured campaign status for each property
            for (const prop of this.properties) {
                try {
                    console.log(`🔍 DEBUG: Loading featured status for ${prop}, campaign ${campaignId}`);
                    const featuredResponse = await fetch(`${this.baseURL}/properties/${prop}/featured`);
                    if (featuredResponse.ok) {
                        const featuredData = await featuredResponse.json();
                        console.log(`🔍 DEBUG: Featured data for ${prop}:`, featuredData);
                        const isFeatured = featuredData.featured_campaign_id == campaignId;
                        console.log(`🔍 DEBUG: Is campaign ${campaignId} featured for ${prop}? ${isFeatured}`);
                        
                        // Set featured toggle
                        const featuredToggle = document.getElementById(`featured_${prop}_${campaignId}`);
                        console.log(`🔍 DEBUG: Featured toggle element for ${prop}:`, featuredToggle ? 'found' : 'NOT FOUND');
                        if (featuredToggle) {
                            featuredToggle.checked = isFeatured;
                            console.log(`🔍 DEBUG: Set ${prop} featured toggle to:`, isFeatured);
                            
                            // Update toggle visual state
                            const toggleBg = featuredToggle.nextElementSibling.querySelector('.toggle-bg');
                            const toggleDot = featuredToggle.nextElementSibling.querySelector('.toggle-dot');
                            if (isFeatured) {
                                toggleBg.style.backgroundColor = '#F7007C';
                                toggleDot.style.transform = 'translateX(20px)';
                            }
                            
                            // Add change listener
                            featuredToggle.addEventListener('change', () => {
                                this.handleFeaturedToggle(prop, campaignId, featuredToggle.checked);
                            });
                        }
                    }
                } catch (error) {
                    console.log(`🔍 DEBUG: No featured campaign data for ${prop}:`, error.message);
                }
            }
            
        } catch (error) {
            console.error('❌ Failed to load property settings:', error);
        }
    }

    async handleFeaturedToggle(propertyCode, campaignId, isChecked) {
        try {
            console.log(`🌟 Setting featured campaign for ${propertyCode}: ${isChecked ? campaignId : 'none'}`);
            
            // Update toggle visual state
            const featuredToggle = document.getElementById(`featured_${propertyCode}_${campaignId}`);
            if (featuredToggle) {
                const toggleBg = featuredToggle.nextElementSibling.querySelector('.toggle-bg');
                const toggleDot = featuredToggle.nextElementSibling.querySelector('.toggle-dot');
                
                if (isChecked) {
                    toggleBg.style.backgroundColor = '#F7007C';
                    toggleDot.style.transform = 'translateX(20px)';
                } else {
                    toggleBg.style.backgroundColor = '#d1d5db';
                    toggleDot.style.transform = 'translateX(0)';
                }
            }
            
            // Call API to save featured campaign
            const response = await fetch(`${this.baseURL}/properties/${propertyCode}/featured`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    campaign_id: isChecked ? campaignId : null 
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const campaignName = this.campaigns.find(c => c.id == campaignId)?.name;
            const propertyName = this.propertyNames[propertyCode];
            
            this.showAlert(
                `✅ ${campaignName} ${isChecked ? 'set as featured' : 'removed as featured'} for ${propertyName}`, 
                'success'
            );
            
        } catch (error) {
            console.error('❌ Failed to update featured campaign:', error);
            this.showAlert(`Failed to update featured campaign: ${error.message}`, 'error');
            
            // Revert toggle on error
            const featuredToggle = document.getElementById(`featured_${propertyCode}_${campaignId}`);
            if (featuredToggle) {
                featuredToggle.checked = !isChecked;
            }
        }
    }

    async savePropertySettings(campaignId) {
        const settings = {};
        
        console.log('🔍 DEBUG: Starting savePropertySettings for campaign:', campaignId);
        console.log('🔍 DEBUG: Available properties:', this.properties);
        
        for (const prop of this.properties) {
            const activeCheckbox = document.getElementById(`active_${prop}_${campaignId}`);
            const visibilitySlider = document.getElementById(`visibility_${prop}_${campaignId}`);
            const impCapInput = document.getElementById(`imp_cap_${prop}_${campaignId}`);
            const clkCapInput = document.getElementById(`clk_cap_${prop}_${campaignId}`);
            
            console.log(`🔍 DEBUG: ${prop} elements:`, {
                activeCheckbox: !!activeCheckbox,
                visibilitySlider: !!visibilitySlider,
                impCapInput: !!impCapInput,
                clkCapInput: !!clkCapInput
            });
            
            if (activeCheckbox && visibilitySlider) {
                settings[prop] = {
                    active: activeCheckbox.checked,
                    visibility_percentage: parseInt(visibilitySlider.value),
                    impression_cap_daily: impCapInput && impCapInput.value !== '' ? parseInt(impCapInput.value) : null,
                    click_cap_daily: clkCapInput && clkCapInput.value !== '' ? parseInt(clkCapInput.value) : null
                };
                console.log(`🔍 DEBUG: Settings for ${prop}:`, settings[prop]);
            } else {
                console.log(`🔍 DEBUG: Missing elements for ${prop}`);
            }
        }

        try {
            console.log('💾 Saving property settings:', { campaignId, settings });
            const response = await fetch(`${this.baseURL}/campaigns/${campaignId}/properties`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings)
            });

            console.log('🔍 DEBUG: Response status:', response.status);
            console.log('🔍 DEBUG: Response ok:', response.ok);

            if (!response.ok) {
                const msg = await response.text();
                console.log('🔍 DEBUG: Error response:', msg);
                throw new Error(`HTTP ${response.status} ${msg}`);
            }

            const result = await response.json();
            console.log('🔍 DEBUG: Success response:', result);

            this.showAlert('Property settings saved successfully!', 'success');
            this.closeModals();
        } catch (error) {
            console.error('❌ Failed to save property settings:', error);
            console.error('❌ Error details:', {
                message: error.message,
                stack: error.stack,
                campaignId,
                settings
            });
            this.showAlert(`Failed to save settings: ${error.message}`, 'error');
        }
    }

    async toggleActive(campaignId) {
        const campaign = this.campaigns.find(c => c.id === campaignId);
        if (!campaign) return;

        try {
            const response = await fetch(`${this.baseURL}/campaigns/${campaignId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    active: !campaign.active
                })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            console.log(`✅ Campaign ${campaignId} ${campaign.active ? 'deactivated' : 'activated'}`);
            
            this.showAlert(`Campaign ${campaign.active ? 'deactivated' : 'activated'} successfully!`, 'success');
            await this.loadCampaigns(); // Refresh
            this.updateStats();
            
        } catch (error) {
            console.error('❌ Failed to toggle campaign:', error);
            this.showAlert('Failed to update campaign. Please try again.', 'error');
        }
    }

    async updateStats() {
        // Update campaign stats from loaded data
        const totalCampaigns = this.campaigns.length;
        const activeCampaigns = this.campaigns.filter(c => c.active).length;
        
        // Update active campaigns count immediately
        const activeElement = document.getElementById('active-campaigns');
        if (activeElement) activeElement.textContent = activeCampaigns;
        
        console.log(`📊 Campaign stats updated: ${activeCampaigns} active campaigns out of ${totalCampaigns} total`);
        
        // Fetch real-time analytics data from API
        try {
            console.log('🔄 Fetching real-time performance metrics...');
            const response = await fetch(`${this.baseURL}/analytics/performance-metrics`);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('📊 Performance metrics received:', data);
            
            if (data.success && data.today) {
                // Update Daily Impressions 
                const impressionsElement = document.getElementById('daily-impressions');
                if (impressionsElement) {
                    impressionsElement.textContent = data.today.today_impressions.toLocaleString();
                }
                
                // Update Daily Revenue
                const revenueElement = document.getElementById('daily-revenue');
                if (revenueElement) {
                    revenueElement.textContent = `$${data.today.today_revenue.toFixed(2)}`;
                }
                
                // Update Total Properties (static count - 4 properties)
                const propertiesElement = document.getElementById('total-properties');
                if (propertiesElement) {
                    propertiesElement.textContent = '4'; // MFF, MMM, MCAD, MMD
                }
                
                console.log(`✅ Real-time stats updated: ${data.today.today_impressions} impressions, $${data.today.today_revenue} revenue`);
            }
            
        } catch (error) {
            console.error('❌ Failed to fetch performance metrics:', error);
            // Don't show error to user, just log it
        }
    }

    showAlert(message, type = 'info') {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());

        const alertColors = {
            success: 'bg-green-100 border-green-400 text-green-700',
            error: 'bg-red-100 border-red-400 text-red-700',
            info: 'bg-blue-100 border-blue-400 text-blue-700',
            warning: 'bg-yellow-100 border-yellow-400 text-yellow-700'
        };

        const alertHTML = `
            <div class="alert fixed top-4 right-4 max-w-sm w-full bg-white border-l-4 ${alertColors[type]} p-4 shadow-lg rounded-r-lg z-50">
                <div class="flex">
                    <div class="flex-shrink-0">
                        ${type === 'success' ? '✅' : type === 'error' ? '❌' : type === 'warning' ? '⚠️' : 'ℹ️'}
                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium">${message}</p>
                    </div>
                    <div class="ml-auto pl-3">
                        <button onclick="this.parentElement.parentElement.remove()" class="text-gray-400 hover:text-gray-600">
                            ×
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', alertHTML);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            const alert = document.querySelector('.alert');
            if (alert) alert.remove();
        }, 5000);
    }

    async saveFeaturedCampaign(propertyCode) {
        try {
            const selectElement = document.getElementById(`featured-${propertyCode}`);
            const campaignId = selectElement.value || null;
            
            console.log(`💾 Saving featured campaign for ${propertyCode}: ${campaignId || 'none'}`);
            
            // Call API to save featured campaign
            const response = await fetch(`${this.baseURL}/properties/${propertyCode}/featured`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ campaign_id: campaignId })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const result = await response.json();
            const campaignName = campaignId ? 
                this.campaigns.find(c => c.id == campaignId)?.name : 'None';
            
            this.showAlert(
                `✅ Featured campaign for ${this.propertyNames[propertyCode]} set to: ${campaignName}`, 
                'success'
            );
            
        } catch (error) {
            console.error('❌ Failed to save featured campaign:', error);
            this.showAlert(`Failed to save featured campaign: ${error.message}`, 'error');
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.campaignManager = new CampaignManager();
});

// Global functions for HTML onclick handlers
function showAddCampaignModal() {
    if (window.campaignManager) {
        window.campaignManager.showAddCampaignModal();
    }
}

function hideAddCampaignModal() {
    if (window.campaignManager) {
        window.campaignManager.closeModals();
    }
}

/**
 * Analytics Dashboard Manager
 * Handles Mike's Tune-style analytics reporting
 */
class AnalyticsManager {
    constructor() {
        this.baseURL = '/api';
        this.currentData = null;
        this.currentPreset = 'last_7_days'; // Default to Mike's preference
        this.init();
    }

    init() {
        console.log('📊 Analytics Manager initializing...');
        this.setupTabNavigation();
        this.setupAnalyticsEventListeners();
    }

    setupTabNavigation() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const targetTab = e.currentTarget.dataset.tab;
                this.switchTab(targetTab);
            });
        });

        // Handle URL hash for direct linking
        const hash = window.location.hash.substring(1);
        if (hash === 'analytics') {
            this.switchTab('analytics');
        }
    }

    switchTab(tabName) {
        console.log(`🔄 Switching to tab: ${tabName}`);
        
        // Update URL hash
        window.location.hash = tabName;
        
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
        
        // Update content sections
        document.querySelectorAll('.tab-content').forEach(section => {
            section.classList.add('hidden');
        });
        document.getElementById(`${tabName}-section`).classList.remove('hidden');
        
        // Load analytics data if switching to analytics tab
        if (tabName === 'analytics') {
            this.loadAnalyticsData();
        }
    }

    setupAnalyticsEventListeners() {
        // Refresh button
        const refreshBtn = document.getElementById('refresh-analytics');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.loadAnalyticsData();
            });
        }
        
        // Date preset selector
        const datePreset = document.getElementById('date-preset');
        if (datePreset) {
            datePreset.addEventListener('change', (e) => {
                console.log(`📅 Date preset changed to: ${e.target.value}`);
                this.currentPreset = e.target.value;
                this.loadAnalyticsData();
            });
        }

        // Export CSV button
        const exportBtn = document.getElementById('export-csv');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportToCSV();
            });
        }
    }

    async loadAnalyticsData() {
        console.log('📊 Loading analytics data...');
        
        try {
            // Show loading state
            this.showLoading();
            
                    // Load attribution analytics and tune-style report in parallel
        const [attributionResponse, reportResponse] = await Promise.all([
            fetch(`${this.baseURL}/analytics/attribution?preset=${this.currentPreset}`),
            fetch(`${this.baseURL}/analytics/tune-style-report?preset=${this.currentPreset}`)
        ]);

            if (!attributionResponse.ok || !reportResponse.ok) {
                throw new Error('Failed to fetch analytics data');
            }

            const attributionData = await attributionResponse.json();
            const reportData = await reportResponse.json();

            console.log('📊 Attribution data:', attributionData);
            console.log('📊 Report data:', reportData);

            // Update UI with real data
            this.updatePerformanceMetrics(attributionData);
            this.updateTuneStyleReport(reportData);
            this.currentData = reportData;

            // Hide loading state
            this.hideLoading();

        } catch (error) {
            console.error('❌ Failed to load analytics:', error);
            this.hideLoading();
            this.showAnalyticsError(error);
        }
    }

    updatePerformanceMetrics(data) {
        // Use attribution data format instead of performance metrics
        const summary = data.summary;
        const bySource = data.by_source;
        
        // Calculate total impressions from campaign data
        const totalImpressions = data.by_campaign.reduce((sum, campaign) => sum + (campaign.impressions || 0), 0);
        
        // Find best performing source
        const bestSource = bySource.length > 0 ? 
            bySource.reduce((a, b) => (a.estimated_revenue || 0) > (b.estimated_revenue || 0) ? a : b) : null;

        // Update metrics
        document.getElementById('today-impressions').textContent = totalImpressions.toLocaleString();
        document.getElementById('today-clicks').textContent = summary.total_clicks || 0;
        document.getElementById('today-revenue').textContent = summary.total_revenue ? `$${summary.total_revenue.toFixed(2)}` : '$0.00';
        document.getElementById('best-campaign').textContent = bestSource ? bestSource.source : 'No data';
    }

    updateTuneStyleReport(data) {
        if (!data.success) return;

        const tableBody = document.getElementById('analytics-table-body');
        const tableContainer = document.getElementById('analytics-table-container');
        
        if (!tableBody || !tableContainer) return;

        // Clear existing data
        tableBody.innerHTML = '';

        if (!data.data || data.data.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="11" class="px-6 py-8 text-center text-gray-500">
                        <div class="flex flex-col items-center">
                            <svg class="w-12 h-12 text-gray-300 mb-4" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"></path>
                                <path fill-rule="evenodd" d="M4 5a2 2 0 012-2v1a1 1 0 001 1h6a1 1 0 001-1V3a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5z"></path>
                            </svg>
                            <h3 class="text-lg font-medium text-gray-900 mb-2">No Campaign Data</h3>
                            <p class="text-sm">Analytics will appear here as your campaigns generate traffic</p>
                        </div>
                    </td>
                </tr>
            `;
        } else {
            // Populate table with real data
            data.data.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-gray-50';
                
                tr.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${row.offer}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 uppercase">${row.partner}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">${row.campaign}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">${row.creative}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-semibold">${row.impressions.toLocaleString()}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-semibold">${row.clicks.toLocaleString()}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${(row.ctr || 0).toFixed(2)}%</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-semibold">$${(row.revenue || 0).toFixed(2)}</td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-blue-600">${(row.rpm || 0).toFixed(2)}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-purple-600">$${(row.rpc || 0).toFixed(2)}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">$${(row.payout || 0).toFixed(2)}</td>
                `;
                
                tableBody.appendChild(tr);
            });
        }

        // Show the table
        tableContainer.classList.remove('hidden');
    }

    showLoading() {
        document.getElementById('analytics-loading').classList.remove('hidden');
        document.getElementById('analytics-table-container').classList.add('hidden');
    }

    hideLoading() {
        document.getElementById('analytics-loading').classList.add('hidden');
    }

    showAnalyticsError(error) {
        const tableContainer = document.getElementById('analytics-table-container');
        const loadingContainer = document.getElementById('analytics-loading');
        
        if (!tableContainer || !loadingContainer) return;
        
        // Hide loading, show error in table container
        loadingContainer.classList.add('hidden');
        tableContainer.classList.remove('hidden');
        
        const tableBody = document.getElementById('analytics-table-body');
        if (tableBody) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="11" class="px-6 py-12 text-center">
                        <div class="flex flex-col items-center max-w-md mx-auto">
                            <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
                                <svg class="w-8 h-8 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"></path>
                                </svg>
                            </div>
                            <h3 class="text-lg font-semibold text-gray-900 mb-2">Analytics Loading Failed</h3>
                            <p class="text-sm text-gray-600 mb-4 text-center">
                                ${error.message || 'Unable to load analytics data. Please check your connection and try again.'}
                            </p>
                            <button onclick="window.analyticsManager.loadAnalyticsData()" 
                                    class="flex items-center gap-2 px-4 py-2 bg-mode-pink text-white rounded-lg hover:bg-mode-pink/80 transition-colors">
                                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1z"></path>
                                </svg>
                                Try Again
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }
        
        // Also show toast notification
        this.showAlert(`Analytics error: ${error.message}`, 'error');
    }

    exportToCSV() {
        if (!this.currentData || !this.currentData.data) {
            this.showAlert('No data available to export', 'warning');
            return;
        }

        // Show export progress
        const exportBtn = document.getElementById('export-csv');
        const originalText = exportBtn.innerHTML;
        exportBtn.innerHTML = `
            <svg class="w-4 h-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1z"></path>
            </svg>
            Exporting...
        `;
        exportBtn.disabled = true;

        try {
            const csvContent = this.convertToCSV(this.currentData.data);
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            
            if (link.download !== undefined) {
                const url = URL.createObjectURL(blob);
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
                const filename = `mode-tune-analytics-${timestamp}-${this.currentData.data.length}-campaigns.csv`;
                
                link.setAttribute('href', url);
                link.setAttribute('download', filename);
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
                
                this.showAlert(`Successfully exported ${this.currentData.data.length} campaigns to ${filename}`, 'success');
            }
        } catch (error) {
            console.error('Export failed:', error);
            this.showAlert('Export failed. Please try again.', 'error');
        } finally {
            // Restore button
            setTimeout(() => {
                exportBtn.innerHTML = originalText;
                exportBtn.disabled = false;
            }, 1000);
        }
    }

    convertToCSV(data) {
        if (!data || data.length === 0) return '';

        const csvArray = [];
        
        // Add report metadata
        csvArray.push(`# Mode Analytics - Tune-Style Report`);
        csvArray.push(`# Generated: ${new Date().toISOString()}`);
        csvArray.push(`# Period: ${this.currentData.period || 'Last 30 days'}`);
        csvArray.push(`# Total Campaigns: ${data.length}`);
        csvArray.push(`# Total Impressions: ${data.reduce((sum, row) => sum + row.impressions, 0).toLocaleString()}`);
        csvArray.push(`# Total Clicks: ${data.reduce((sum, row) => sum + row.clicks, 0).toLocaleString()}`);
        csvArray.push(`# Total Revenue: $${data.reduce((sum, row) => sum + row.revenue, 0).toFixed(2)}`);
        csvArray.push(''); // Empty line
        
        // Add headers
        const headers = ['Offer', 'Partner', 'Campaign', 'Creative', 'Impressions', 'Clicks', 'CTR %', 'Revenue', 'RPM', 'RPC', 'Payout'];
        csvArray.push(headers.join(','));

        // Add data rows
        data.forEach(row => {
            const csvRow = [
                `"${row.offer}"`,
                `"${row.partner}"`,
                `"${row.campaign}"`,
                `"${row.creative}"`,
                row.impressions,
                row.clicks,
                row.ctr.toFixed(2),
                row.revenue.toFixed(2),
                row.rpm.toFixed(2),
                row.rpc.toFixed(2),
                row.payout.toFixed(2)
            ];
            csvArray.push(csvRow.join(','));
        });

        return csvArray.join('\n');
    }

    showAlert(message, type = 'info') {
        // Reuse existing alert system from CampaignManager
        if (window.campaignManager) {
            window.campaignManager.showAlert(message, type);
        } else {
            console.log(`${type.toUpperCase()}: ${message}`);
        }
    }
}

// Initialize Analytics Manager
window.analyticsManager = new AnalyticsManager(); 