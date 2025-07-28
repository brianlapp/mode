/**
 * Mode Popup Campaign Manager - Admin Interface
 * JavaScript functionality for Mike's campaign management dashboard
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

        // Image preview for URL inputs
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

    showAddCampaignModal() {
        const modal = document.getElementById('addCampaignModal');
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
    }

    closeModals() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        });
        
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
            description: formData.get('description')
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
        const campaign = this.campaigns.find(c => c.id === campaignId);
        if (!campaign) return;

        // For now, show an alert. Full edit modal would be next enhancement
        this.showAlert(`Edit functionality for "${campaign.name}" coming soon!`, 'info');
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