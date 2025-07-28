/**
 * Mode Popup Admin Interface JavaScript
 * Handles campaign management, real-time preview, and API interactions
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000/api'; // Will be updated for production
let currentCampaigns = [];
let previewData = {
    name: 'Campaign Name',
    description: 'Campaign description will appear here...',
    cta_text: 'View Offer',
    logo_url: 'https://assets.isu.pub/document-structure/230821210201-6b2c1d176d5b4af7574d98b41de5de0d/v1/d08ce648ec2d8a39bf81ea8b6f317a12.jpeg',
    main_image_url: 'https://via.placeholder.com/300x160/F7007C/FFFFFF?text=Upload+Main+Image'
};

// Initialize admin interface
document.addEventListener('DOMContentLoaded', function() {
    loadCampaigns();
    setupRealTimePreview();
    setupImageUploadHandlers();
});

/**
 * Modal Management
 */
function openAddCampaignModal() {
    // Load modal HTML
    fetch('../admin/add-campaign.html')
        .then(response => response.text())
        .then(html => {
            document.getElementById('add-campaign-modal').innerHTML = html;
            document.getElementById('add-campaign-modal').classList.remove('hidden');
            
            // Setup form handlers after modal is loaded
            setTimeout(() => {
                setupFormHandlers();
                setupRealTimePreview();
                setupImageUploadHandlers();
            }, 100);
        })
        .catch(error => {
            console.error('Error loading modal:', error);
            showNotification('Error loading campaign form', 'error');
        });
}

function closeAddCampaignModal() {
    document.getElementById('add-campaign-modal').classList.add('hidden');
    document.getElementById('add-campaign-modal').innerHTML = '';
    
    // Reset preview data
    previewData = {
        name: 'Campaign Name',
        description: 'Campaign description will appear here...',
        cta_text: 'View Offer',
        logo_url: 'https://assets.isu.pub/document-structure/230821210201-6b2c1d176d5b4af7574d98b41de5de0d/v1/d08ce648ec2d8a39bf81ea8b6f317a12.jpeg',
        main_image_url: 'https://via.placeholder.com/300x160/F7007C/FFFFFF?text=Upload+Main+Image'
    };
}

/**
 * Real-time Preview System
 */
function setupRealTimePreview() {
    // Campaign name input
    const nameInput = document.getElementById('campaign-name');
    if (nameInput) {
        nameInput.addEventListener('input', function() {
            previewData.name = this.value || 'Campaign Name';
            updatePreview();
        });
    }

    // Description textarea
    const descInput = document.getElementById('description');
    if (descInput) {
        descInput.addEventListener('input', function() {
            previewData.description = this.value || 'Campaign description will appear here...';
            updatePreview();
        });
    }

    // CTA text input
    const ctaInput = document.getElementById('cta-text');
    if (ctaInput) {
        ctaInput.addEventListener('input', function() {
            previewData.cta_text = this.value || 'View Offer';
            updatePreview();
        });
    }
}

function updatePreview() {
    // Update preview elements
    const titleEl = document.getElementById('preview-title');
    const descEl = document.getElementById('preview-description');
    const ctaEl = document.getElementById('preview-cta');
    const logoEl = document.getElementById('preview-logo');
    const mainImageEl = document.getElementById('preview-main-image');

    if (titleEl) titleEl.textContent = previewData.name;
    if (descEl) descEl.textContent = previewData.description;
    if (ctaEl) ctaEl.textContent = previewData.cta_text;
    if (logoEl) logoEl.src = previewData.logo_url;
    if (mainImageEl) mainImageEl.src = previewData.main_image_url;
}

/**
 * Image Upload Handling
 */
function setupImageUploadHandlers() {
    // Setup drag and drop for image upload zones
    const logoZone = document.querySelector('[ondrop*="logo"]');
    const mainZone = document.querySelector('[ondrop*="main"]');
    
    if (logoZone) {
        logoZone.addEventListener('dragover', handleDragOver);
        logoZone.addEventListener('dragleave', handleDragLeave);
        logoZone.addEventListener('drop', (e) => handleDrop(e, 'logo'));
    }
    
    if (mainZone) {
        mainZone.addEventListener('dragover', handleDragOver);
        mainZone.addEventListener('dragleave', handleDragLeave);
        mainZone.addEventListener('drop', (e) => handleDrop(e, 'main'));
    }
}

function handleDragOver(event) {
    event.preventDefault();
    event.target.closest('.image-upload-zone').classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    event.target.closest('.image-upload-zone').classList.remove('dragover');
}

function handleDrop(event, type) {
    event.preventDefault();
    const zone = event.target.closest('.image-upload-zone');
    zone.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        handleImageFile(files[0], type);
    }
}

function handleImageUpload(event, type) {
    const file = event.target.files[0];
    if (file) {
        handleImageFile(file, type);
    }
}

function handleImageFile(file, type) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showNotification('Please select a valid image file', 'error');
        return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        showNotification('Image size must be less than 5MB', 'error');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        const imageUrl = e.target.result;
        
        // Update preview
        if (type === 'logo') {
            previewData.logo_url = imageUrl;
            showImagePreview('logo', imageUrl);
        } else if (type === 'main') {
            previewData.main_image_url = imageUrl;
            showImagePreview('main', imageUrl);
        }
        
        updatePreview();
    };
    
    reader.readAsDataURL(file);
}

function showImagePreview(type, imageUrl) {
    const previewEl = document.getElementById(`${type}-preview`);
    const placeholderEl = document.getElementById(`${type}-placeholder`);
    const imageEl = document.getElementById(`${type}-image`);
    
    if (previewEl && placeholderEl && imageEl) {
        imageEl.src = imageUrl;
        placeholderEl.classList.add('hidden');
        previewEl.classList.remove('hidden');
    }
}

/**
 * Property Toggle Management
 */
function toggleProperty(property) {
    const toggle = document.querySelector(`[data-property="${property}"]`);
    const checkbox = toggle.querySelector('input[type="checkbox"]');
    
    if (checkbox.checked) {
        toggle.classList.add('active');
    } else {
        toggle.classList.remove('active');
    }
}

function updateVisibility(property, value) {
    document.getElementById(`${property}-visibility`).textContent = `${value}%`;
}

/**
 * Form Submission
 */
function setupFormHandlers() {
    const form = document.getElementById('add-campaign-form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const submitBtn = event.target.querySelector('button[type="submit"]');
    
    // Show loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    
    try {
        // Prepare campaign data
        const campaignData = {
            name: formData.get('name'),
            tune_url: formData.get('tune_url'),
            description: formData.get('description'),
            cta_text: formData.get('cta_text') || 'View Offer',
            logo_url: previewData.logo_url,
            main_image_url: previewData.main_image_url,
            active: true
        };

        // Get selected properties
        const selectedProperties = Array.from(formData.getAll('properties'));
        if (selectedProperties.length === 0) {
            throw new Error('Please select at least one property');
        }

        // Create campaign
        const response = await fetch(`${API_BASE_URL}/campaigns`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(campaignData)
        });

        if (!response.ok) {
            throw new Error('Failed to create campaign');
        }

        const campaign = await response.json();

        // Set property assignments
        for (const property of selectedProperties) {
            const visibility = document.querySelector(`[data-property="${property}"] .visibility-slider`).value;
            
            await fetch(`${API_BASE_URL}/campaigns/${campaign.id}/properties`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    property_code: property,
                    visibility_percentage: parseInt(visibility),
                    active: true
                })
            });
        }

        // Success!
        showNotification('Campaign created successfully!', 'success');
        closeAddCampaignModal();
        loadCampaigns(); // Refresh the campaign list

    } catch (error) {
        console.error('Error creating campaign:', error);
        showNotification(error.message || 'Failed to create campaign', 'error');
    } finally {
        // Remove loading state
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}

/**
 * Campaign Management
 */
async function loadCampaigns() {
    try {
        const response = await fetch(`${API_BASE_URL}/campaigns`);
        if (response.ok) {
            currentCampaigns = await response.json();
            updateCampaignTable();
            updateStats();
        }
    } catch (error) {
        console.error('Error loading campaigns:', error);
        // Show empty state for now
        updateCampaignTable();
    }
}

function updateCampaignTable() {
    const tbody = document.getElementById('campaigns-table');
    
    if (currentCampaigns.length === 0) {
        tbody.innerHTML = `
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
            </tr>
        `;
        return;
    }

    // Render campaign rows
    tbody.innerHTML = currentCampaigns.map(campaign => `
        <tr class="campaign-row-new hover:bg-gray-50">
            <td class="px-6 py-4">
                <div class="flex items-center space-x-3">
                    <img src="${campaign.logo_url}" alt="Logo" class="w-10 h-10 rounded-full object-cover">
                    <div>
                        <p class="font-medium text-gray-900">${campaign.name}</p>
                        <p class="text-sm text-gray-500">Created ${new Date(campaign.created_at).toLocaleDateString()}</p>
                    </div>
                </div>
            </td>
            <td class="px-6 py-4">
                <div class="flex space-x-1">
                    ${getPropertyBadges(campaign)}
                </div>
            </td>
            <td class="px-6 py-4">
                <div class="text-sm text-gray-600">
                    ${getVisibilityInfo(campaign)}
                </div>
            </td>
            <td class="px-6 py-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${campaign.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}">
                    ${campaign.active ? 'Active' : 'Inactive'}
                </span>
            </td>
            <td class="px-6 py-4">
                <div class="flex space-x-2">
                    <button onclick="editCampaign(${campaign.id})" 
                            class="text-mode-blue hover:text-mode-pink transition-colors">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
                        </svg>
                    </button>
                    <button onclick="toggleCampaign(${campaign.id})" 
                            class="text-gray-400 hover:text-gray-600 transition-colors">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"></path>
                        </svg>
                    </button>
                    <button onclick="deleteCampaign(${campaign.id})" 
                            class="text-red-400 hover:text-red-600 transition-colors">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"></path>
                            <path fill-rule="evenodd" d="M4 5a1 1 0 011-1h10a1 1 0 011 1v9a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 112 0v4a1 1 0 11-2 0V9zm4 0a1 1 0 112 0v4a1 1 0 11-2 0V9z"></path>
                        </svg>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function getPropertyBadges(campaign) {
    // For now, show all properties as active
    // This would be populated from campaign property assignments
    const properties = ['MFF', 'MMM', 'MCAD', 'MMD'];
    return properties.map(prop => 
        `<span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-mode-pink/10 text-mode-pink">${prop}</span>`
    ).join('');
}

function getVisibilityInfo(campaign) {
    // Show average visibility across properties
    return '85% avg visibility';
}

function updateStats() {
    // Update dashboard stats
    document.getElementById('active-campaigns').textContent = currentCampaigns.filter(c => c.active).length;
}

/**
 * Utility Functions
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg text-white transform transition-all duration-300 translate-x-full`;
    
    switch (type) {
        case 'success':
            notification.classList.add('bg-green-500');
            break;
        case 'error':
            notification.classList.add('bg-red-500');
            break;
        case 'warning':
            notification.classList.add('bg-yellow-500');
            break;
        default:
            notification.classList.add('bg-blue-500');
    }
    
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-2 hover:opacity-75">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"></path>
                </svg>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 10);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }, 5000);
}

function saveDraft() {
    showNotification('Draft saved locally', 'info');
}

function editCampaign(id) {
    showNotification('Edit functionality coming soon!', 'info');
}

function toggleCampaign(id) {
    showNotification('Campaign toggled', 'success');
    loadCampaigns(); // Refresh list
}

function deleteCampaign(id) {
    if (confirm('Are you sure you want to delete this campaign?')) {
        showNotification('Campaign deleted', 'success');
        loadCampaigns(); // Refresh list
    }
} 