/**
 * Learning Portal - API Client
 * 
 * This module handles all communication with the backend API,
 * including streaming responses and error handling.
 * 
 * @author Abhijit Raijada
 * @designation Principle Engineer
 * @organization GRS
 */

/**
 * API functions for the Learning Portal
 * This module handles all communication with the backend API,
 * including streaming responses and error handling.
 */

// Remove hardcoded API_BASE_URL since it's defined in config.js
// const API_BASE_URL = 'https://te-demo-2d13023bc706.herokuapp.com';

/**
 * Process a streaming response from the server
 * Handles Server-Sent Events (SSE) format and provides callbacks for different events
 * 
 * @param {Response} response - The fetch response object containing the stream
 * @param {Function} onChunk - Callback for each chunk (chunk, fullContent, isFirstChunk, score)
 * @param {Function} onComplete - Callback when streaming is complete (finalContent)
 * @param {Function} onError - Callback for error handling (error)
 */
async function processStreamingResponse(response, onChunk, onComplete, onError) {
    try {
        // Set up stream reader and text decoder
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let isFirstChunk = true;
        let fullContent = '';

        // Process the stream chunk by chunk
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            // Process each line in the chunk
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        // Parse the JSON data from the SSE format
                        const data = JSON.parse(line.slice(6));
                        
                        // Handle content updates
                        if (data.content) {
                            fullContent += data.content;
                            onChunk(data.content, fullContent, isFirstChunk);
                            isFirstChunk = false;
                        }
                        
                        // Handle score updates (for assessments)
                        if (data.score !== undefined) {
                            onChunk(null, fullContent, false, data.score);
                        }
                        
                        // Handle error messages
                        if (data.error) {
                            throw new Error(data.error);
                        }
                    } catch (e) {
                        console.error('Error parsing chunk:', e);
                        if (onError) onError(e);
                    }
                }
            }
        }

        // Stream complete - call the completion callback
        if (onComplete) onComplete(fullContent);
    } catch (error) {
        console.error('Error processing stream:', error);
        if (onError) onError(error);
    }
}

/**
 * Send a request to analyze an answer
 * Used for assessing free-text responses against evaluation criteria
 * 
 * @param {string} questionText - The question text
 * @param {string} userAnswer - The user's answer
 * @param {string} module - The module identifier
 * @param {string} unit - The unit identifier
 * @param {string} guide - The answer guidelines/rubric
 * @returns {Promise<Response>} The fetch response for streaming
 */
async function analyzeAnswer(questionText, userAnswer, module = 'module1', unit = 'unit1', guide = '') {
    try {
        // Send POST request to analysis endpoint
        const response = await fetch(`${API_BASE_URL}/analyze_answer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: 'regular',
                question: questionText,
                user_answer: userAnswer,
                module: module,
                unit: unit,
                guide: guide
            })
        });

        // Check response status
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response;
    } catch (error) {
        console.error('Error in analyzeAnswer:', error);
        showError('Failed to analyze answer. Please try again.');
        throw error;
    }
}

/**
 * Send a follow-up question to the bot
 * Supports multi-turn conversations with context from previous exchanges
 * 
 * @param {string} question - The follow-up question
 * @param {Array} history - The conversation history array
 * @param {string} module - The module identifier (for context retrieval)
 * @param {string} unit - The unit identifier (optional)
 * @returns {Promise<Response>} The fetch response for streaming
 */
async function askBot(question, history, module = 'module1', unit = 'unit1') {
    try {
        // Send POST request to bot endpoint
        const response = await fetch(`${API_BASE_URL}/ask_bot`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: question,
                history: history,
                module: module,
                unit: unit
            })
        });

        // Check response status
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return response;
    } catch (error) {
        console.error('Error in askBot:', error);
        showError('Failed to get response from bot. Please try again.');
        throw error;
    }
}

// Make functions available globally for use in other modules
window.processStreamingResponse = processStreamingResponse;
window.analyzeAnswer = analyzeAnswer;
window.askBot = askBot; 