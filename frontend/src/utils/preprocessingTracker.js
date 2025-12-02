/**
 * Preprocessing Steps Tracker
 * 
 * This utility helps track and store preprocessing steps in localStorage
 * so they can be displayed in the algorithm selection page.
 */

/**
 * Add a preprocessing step to localStorage
 * @param {string} stepName - Name of the preprocessing step (e.g., "Train/Test Split", "Categorical Encoding")
 * @param {object} details - Optional details about the step
 */
export function addPreprocessingStep(stepName, details = {}) {
  try {
    // Get existing processed data from localStorage
    const processedDataStr = localStorage.getItem('processedData');
    if (!processedDataStr) {
      console.warn('⚠️ No processedData found in localStorage');
      return;
    }

    const processedData = JSON.parse(processedDataStr);
    
    // Initialize processingSteps array if it doesn't exist
    if (!processedData.processingSteps) {
      processedData.processingSteps = [];
    }

    // Create step object
    const step = {
      name: stepName,
      timestamp: new Date().toISOString(),
      ...details
    };

    // Add step if not already present (avoid duplicates)
    const exists = processedData.processingSteps.some(s => s.name === stepName);
    if (!exists) {
      processedData.processingSteps.push(step);
      console.log(`✅ Added preprocessing step: ${stepName}`);
    } else {
      console.log(`ℹ️ Preprocessing step already exists: ${stepName}`);
    }

    // Save back to localStorage
    localStorage.setItem('processedData', JSON.stringify(processedData));
    
    return processedData.processingSteps;
  } catch (error) {
    console.error('❌ Error adding preprocessing step:', error);
    return null;
  }
}

/**
 * Get all preprocessing steps from localStorage
 * @returns {Array} Array of preprocessing steps
 */
export function getPreprocessingSteps() {
  try {
    const processedDataStr = localStorage.getItem('processedData');
    if (!processedDataStr) return [];

    const processedData = JSON.parse(processedDataStr);
    return processedData.processingSteps || [];
  } catch (error) {
    console.error('❌ Error getting preprocessing steps:', error);
    return [];
  }
}

/**
 * Clear all preprocessing steps from localStorage
 */
export function clearPreprocessingSteps() {
  try {
    const processedDataStr = localStorage.getItem('processedData');
    if (!processedDataStr) return;

    const processedData = JSON.parse(processedDataStr);
    processedData.processingSteps = [];
    
    localStorage.setItem('processedData', JSON.stringify(processedData));
    console.log('✅ Cleared all preprocessing steps');
  } catch (error) {
    console.error('❌ Error clearing preprocessing steps:', error);
  }
}

/**
 * Remove a specific preprocessing step
 * @param {string} stepName - Name of the step to remove
 */
export function removePreprocessingStep(stepName) {
  try {
    const processedDataStr = localStorage.getItem('processedData');
    if (!processedDataStr) return;

    const processedData = JSON.parse(processedDataStr);
    if (!processedData.processingSteps) return;

    processedData.processingSteps = processedData.processingSteps.filter(
      s => s.name !== stepName
    );
    
    localStorage.setItem('processedData', JSON.stringify(processedData));
    console.log(`✅ Removed preprocessing step: ${stepName}`);
  } catch (error) {
    console.error('❌ Error removing preprocessing step:', error);
  }
}
