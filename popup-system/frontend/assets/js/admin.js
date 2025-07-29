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
        this.setupEventListeners();
        this.updateStats();
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
                    <td colspan="5" class="px-6 py-4 text-center text-gray-500">
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
                    <div class="flex items-center">
                        <div class="h-10 w-10 flex-shrink-0">
                            <img class="h-10 w-10 rounded-full object-cover" 
                                 src="${campaign.logo_url}" 
                                 alt="${campaign.name}"
                                 onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' fill=\\'%23F7007C\\' viewBox=\\'0 0 24 24\\'%3E%3Cpath d=\\'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z\\'/%3E%3C/svg%3E'">
                        </div>
                        <div class="ml-4">
                            <div class="text-sm font-medium text-gray-900">${campaign.name}</div>
                            <div class="text-sm text-gray-500">ID: ${campaign.id}</div>
                        </div>
                    </div>
                </td>
                <td class="px-6 py-4">
                    <div class="text-sm text-gray-900">${campaign.description}</div>
                    <div class="text-xs text-gray-500 truncate" style="max-width: 200px;">${campaign.tune_url}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${campaign.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                        ${campaign.active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-500">${new Date(campaign.created_at).toLocaleDateString()}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onclick="campaignManager.editCampaign(${campaign.id})" 
                            class="text-mode-pink hover:text-mode-pink-dark mr-3">Edit</button>
                    <button onclick="campaignManager.manageProperties(${campaign.id})" 
                            class="text-mode-blue hover:text-mode-blue-dark mr-3">Properties</button>
                    <button onclick="campaignManager.toggleActive(${campaign.id})" 
                            class="text-gray-600 hover:text-gray-900">
                        ${campaign.active ? 'Deactivate' : 'Activate'}
                    </button>
                </td>
            </tr>
        `).join('');
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
                                <label class="block text-sm font-medium text-gray-700 mb-2">Tune URL (Read-only)</label>
                                <input type="text" value="${campaign.tune_url}" readonly
                                       class="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600">
                            </div>
                            
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Offer ID</label>
                                    <input type="text" value="${campaign.offer_id || ''}" readonly
                                           class="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Aff ID</label>
                                    <input type="text" value="${campaign.aff_id || ''}" readonly
                                           class="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-600">
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
        
        // Validate required fields
        if (!name.trim()) {
            this.showAlert('Campaign name is required!', 'error');
            return;
        }
        
        if (!cta_text.trim()) {
            this.showAlert('CTA button text is required!', 'error');
            return;
        }
        
        const updateData = {
            name: name.trim(),
            description: description.trim(),
            cta_text: cta_text.trim(),
            logo_url: logo_url.trim(),
            main_image_url: main_image_url.trim()
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

    showPropertyModal(campaign) {
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
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">
                                        Visibility Percentage: <span id="visibility_${prop}_${campaign.id}_display">100%</span>
                                    </label>
                                    <input type="range" min="0" max="100" value="100" 
                                           class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                                           id="visibility_${prop}_${campaign.id}"
                                           oninput="document.getElementById('visibility_${prop}_${campaign.id}_display').textContent = this.value + '%'">
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
    }

    async savePropertySettings(campaignId) {
        const settings = {};
        
        for (const prop of this.properties) {
            const activeCheckbox = document.getElementById(`active_${prop}_${campaignId}`);
            const visibilitySlider = document.getElementById(`visibility_${prop}_${campaignId}`);
            
            if (activeCheckbox && visibilitySlider) {
                settings[prop] = {
                    active: activeCheckbox.checked,
                    visibility_percentage: parseInt(visibilitySlider.value)
                };
            }
        }

        try {
            // Save settings via API (endpoint to be implemented)
            console.log('💾 Saving property settings:', { campaignId, settings });
            
            this.showAlert('Property settings saved successfully!', 'success');
            this.closeModals();
            
        } catch (error) {
            console.error('❌ Failed to save property settings:', error);
            this.showAlert('Failed to save settings. Please try again.', 'error');
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

    updateStats() {
        const totalCampaigns = this.campaigns.length;
        const activeCampaigns = this.campaigns.filter(c => c.active).length;
        
        // Update stat cards
        const totalElement = document.getElementById('totalCampaigns');
        const activeElement = document.getElementById('activeCampaigns');
        
        if (totalElement) totalElement.textContent = totalCampaigns;
        if (activeElement) activeElement.textContent = activeCampaigns;
        
        console.log(`📊 Stats updated: ${activeCampaigns} active campaigns out of ${totalCampaigns} total`);
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