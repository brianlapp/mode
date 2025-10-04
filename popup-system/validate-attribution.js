/**
 * UTM Attribution Validation Script
 * Tests the buildAttributedTuneUrl method with various scenarios
 */

// Import URL for Node.js compatibility
const { URL } = require('url');

// Mock the ModePopup class for testing
class MockModePopup {
    constructor() {
        this.debug = (message, data) => console.log(`[DEBUG] ${message}`, data || '');
    }

    /**
     * Build attributed Tune URL with UTM source as aff_sub3
     * @param {string} baseUrl - Original campaign tune_url
     * @param {Object} trackingData - Captured UTM parameters
     * @returns {string} - Enhanced URL with attribution
     */
    buildAttributedTuneUrl(baseUrl, trackingData) {
        try {
            const url = new URL(baseUrl);
            
            // Add UTM source as aff_sub3 if:
            // 1. We have a valid source from UTM parameters
            // 2. aff_sub3 slot is not already used
            if (trackingData.source && !url.searchParams.has('aff_sub3')) {
                url.searchParams.set('aff_sub3', trackingData.source);
                this.debug('Added aff_sub3 attribution', {
                    source: trackingData.source,
                    originalUrl: baseUrl,
                    enhancedUrl: url.toString()
                });
            }
            
            return url.toString();
        } catch (error) {
            this.debug('Error building attributed URL', error);
            // Fallback to original URL if construction fails
            return baseUrl;
        }
    }
}

// Test Scenarios
const testScenarios = [
    {
        name: 'Facebook Traffic Attribution',
        baseUrl: 'https://track.modemobile.com/aff_c?offer_id=6998&aff_id=43045&aff_sub5=popup_tradingTips',
        trackingData: { source: 'facebook', subsource: 'cpc', utm_campaign: 'finance_lookalike' },
        expectedContains: 'aff_sub3=facebook'
    },
    {
        name: 'Google Traffic Attribution', 
        baseUrl: 'https://track.modemobile.com/aff_c?offer_id=7521&aff_id=43045&aff_sub5=popup_behindMarkets',
        trackingData: { source: 'google', subsource: 'organic', utm_campaign: 'trading_tips' },
        expectedContains: 'aff_sub3=google'
    },
    {
        name: 'Email Traffic Attribution',
        baseUrl: 'https://track.modemobile.com/aff_c?offer_id=7389&aff_id=43045&aff_sub5=popup_brownstone', 
        trackingData: { source: 'email', subsource: 'newsletter', utm_campaign: 'weekly_market' },
        expectedContains: 'aff_sub3=email'
    },
    {
        name: 'Direct Traffic (No UTM)',
        baseUrl: 'https://track.modemobile.com/aff_c?offer_id=7385&aff_id=43045&aff_sub5=popup_hotsheets',
        trackingData: { source: null, subsource: 'popup' },
        expectedContains: null // Should not add aff_sub3
    },
    {
        name: 'Existing aff_sub3 Preservation',
        baseUrl: 'https://track.modemobile.com/aff_c?offer_id=7390&aff_id=43045&aff_sub3=existing',
        trackingData: { source: 'facebook', subsource: 'cpc' },
        expectedContains: 'aff_sub3=existing', // Should preserve existing
        shouldNotContain: 'aff_sub3=facebook'
    }
];

// Run Tests
function runValidationTests() {
    console.log('🎯 Starting UTM Attribution Validation Tests\n');
    
    const popup = new MockModePopup();
    let passedTests = 0;
    let totalTests = testScenarios.length;

    testScenarios.forEach((scenario, index) => {
        console.log(`\n📋 Test ${index + 1}: ${scenario.name}`);
        console.log(`   Original URL: ${scenario.baseUrl}`);
        console.log(`   UTM Source: ${scenario.trackingData.source || 'None'}`);
        
        try {
            const result = popup.buildAttributedTuneUrl(scenario.baseUrl, scenario.trackingData);
            console.log(`   Result URL: ${result}`);
            
            // Validate expectations
            let testPassed = true;
            
            if (scenario.expectedContains) {
                if (result.includes(scenario.expectedContains)) {
                    console.log(`   ✅ Contains expected: ${scenario.expectedContains}`);
                } else {
                    console.log(`   ❌ Missing expected: ${scenario.expectedContains}`);
                    testPassed = false;
                }
            } else if (scenario.expectedContains === null) {
                if (!result.includes('aff_sub3=')) {
                    console.log(`   ✅ Correctly no aff_sub3 added`);
                } else {
                    console.log(`   ❌ Unexpected aff_sub3 parameter added`);
                    testPassed = false;
                }
            }
            
            if (scenario.shouldNotContain && result.includes(scenario.shouldNotContain)) {
                console.log(`   ❌ Contains unwanted: ${scenario.shouldNotContain}`);
                testPassed = false;
            }
            
            if (testPassed) {
                console.log(`   🎉 Test PASSED`);
                passedTests++;
            } else {
                console.log(`   💥 Test FAILED`);
            }
            
        } catch (error) {
            console.log(`   💥 Test FAILED with error: ${error.message}`);
        }
    });

    console.log(`\n📊 Test Results: ${passedTests}/${totalTests} tests passed`);
    
    if (passedTests === totalTests) {
        console.log(`🎉 ALL TESTS PASSED! UTM attribution implementation is working correctly.`);
        return true;
    } else {
        console.log(`❌ ${totalTests - passedTests} tests failed. Please review implementation.`);
        return false;
    }
}

// Run the tests immediately
runValidationTests();