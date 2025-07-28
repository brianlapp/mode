/**
 * Simple Campaign Manager - No overengineering, just works
 */

// Simple global functions - no classes, no complexity
let campaigns = [];

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded, starting simple campaign manager');
    loadCampaigns();
    setupButtons();
});

// Load campaigns with basic fetch
async function loadCampaigns() {
    try {
        console.log('Loading campaigns...');
        const response = await fetch('/api/campaigns');
        
        if (response.ok) {
            campaigns = await response.json();
            console.log('Loaded campaigns:', campaigns);
            displayCampaigns();
            updateStats();
        } else {
            console.error('Failed to load campaigns:', response.status);
            showError('Failed to load campaigns');
        }
    } catch (error) {
        console.error('Error loading campaigns:', error);
        showError('Error loading campaigns: ' + error.message);
    }
}

// Display campaigns in table
function displayCampaigns() {
    const tableBody = document.getElementById('campaigns-table');
    if (!tableBody) {
        console.error('Table body not found');
        return;
    }

    if (campaigns.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                    <div class="flex flex-col items-center space-y-4">
                        <svg class="w-12 h-12 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 4a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1V8zm8 0a1 1 0 011-1h4a1 1 0 011 1v2a1 1 0 01-1 1h-4a1 1 0 01-1-1V8z"></path>
                        </svg>
                        <div>
                            <p class="text-lg font-medium">No campaigns yet</p>
                            <p class="text-sm">Click "Add New Campaign" to get started</p>
                        </div>
                    </div>
                </td>
            </tr>`;
        return;
    }

    // Show campaigns
    tableBody.innerHTML = campaigns.map(campaign => `
        <tr class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10">
                        <img class="h-10 w-10 rounded-full object-cover" src="${campaign.logo_url || '/static/img/default-logo.png'}" alt="Logo">
                    </div>
                    <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">${campaign.name}</div>
                        <div class="text-sm text-gray-500">${campaign.description || ''}</div>
                    </div>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">${campaign.tune_url}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="text-sm text-gray-500">100%</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${campaign.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                    ${campaign.active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button onclick="editCampaign(${campaign.id})" class="text-indigo-600 hover:text-indigo-900 mr-3">Edit</button>
                <button onclick="deleteCampaign(${campaign.id})" class="text-red-600 hover:text-red-900">Delete</button>
            </td>
        </tr>
    `).join('');
}

// Update stats
function updateStats() {
    const totalElement = document.getElementById('totalCampaigns');
    const activeElement = document.getElementById('activeCampaigns');
    
    if (totalElement) totalElement.textContent = campaigns.length;
    if (activeElement) activeElement.textContent = campaigns.filter(c => c.active).length;
}

// Setup button event listeners
function setupButtons() {
    const addButton = document.getElementById('addCampaignBtn');
    if (addButton) {
        addButton.addEventListener('click', function() {
            console.log('Add campaign button clicked');
            showAddCampaignModal();
        });
    }
    
    // Form submission
    const form = document.getElementById('addCampaignForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

// Show add campaign modal
function showAddCampaignModal() {
    const modal = document.getElementById('addCampaignModal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

// Hide add campaign modal
function hideAddCampaignModal() {
    const modal = document.getElementById('addCampaignModal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

// Show error message
function showError(message) {
    console.error('Error:', message);
    // You could add a toast notification here
}

// Placeholder functions
function editCampaign(id) {
    console.log('Edit campaign:', id);
    alert('Edit functionality coming soon');
}

function deleteCampaign(id) {
    console.log('Delete campaign:', id);
    if (confirm('Are you sure you want to delete this campaign?')) {
        alert('Delete functionality coming soon');
    }
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const campaignData = {
        name: formData.get('name'),
        tune_url: formData.get('tune_url'),
        logo_url: formData.get('logo_url'),
        main_image_url: formData.get('main_image_url'),
        description: formData.get('description')
    };
    
    try {
        const response = await fetch('/api/campaigns', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(campaignData)
        });
        
        if (response.ok) {
            console.log('Campaign created successfully!');
            hideAddCampaignModal();
            e.target.reset();
            await loadCampaigns(); // Reload campaigns
        } else {
            console.error('Failed to create campaign');
            alert('Failed to create campaign. Please try again.');
        }
    } catch (error) {
        console.error('Error creating campaign:', error);
        alert('Error creating campaign: ' + error.message);
    }
}

// Make functions global so buttons can access them
window.showAddCampaignModal = showAddCampaignModal;
window.hideAddCampaignModal = hideAddCampaignModal;
window.editCampaign = editCampaign;
window.deleteCampaign = deleteCampaign; 