/**
 * Learning Portal - Assessment Module
 * 
 * This module handles the assessment functionality including question presentation,
 * answer submission, scoring, and feedback for the learning portal.
 * 
 * @author Abhijit Raijada
 * @designation Principle Engineer
 * @organization GRS
 */

/**
 * Assessment functionality for Learning Portal
 * This file handles navigation, chat interactions, and assessment logic
 */

// State variables
let currentStep = 1;
let totalSteps = 5;
const submittedQuestions = new Set(); // Track submitted questions
const userAnswers = {};
const userScores = {};

/**
 * Initialize the assessment with the current module and unit
 * @param {string} moduleParam - Optional module parameter from query string
 * @param {string} unitParam - Optional unit parameter from query string
 */
function initializeAssessment(moduleParam, unitParam) {
    // If module/unit params provided via URL, set them in sessionStorage
    if (moduleParam && unitParam) {
        sessionStorage.setItem('moduleParam', moduleParam);
        sessionStorage.setItem('unitParam', unitParam);
    }
    
    // Get current module and unit configuration
    const config = getConfig();
    const { module, unit, moduleId, unitId } = config;
    
    // Update page title and description
    document.title = `${module.name} - ${unit.title || 'Assessment'}`;
    document.getElementById('assessment-title').textContent = unit.title || 'Assessment';
    document.getElementById('assessment-description').textContent = unit.description || 'Complete the assessment questions.';
    
    // Set total steps based on questions length
    totalSteps = unit.questions?.length || 0;
    
    if (totalSteps === 0) {
        // Handle case where no questions are available
        const questionContainer = document.getElementById('question-container');
        questionContainer.innerHTML = '<div class="p-4 text-center text-gray-500">No questions available for this module and unit.</div>';
        
        // Hide navigation buttons
        document.getElementById('prev-btn').classList.add('hidden');
        document.getElementById('next-btn').classList.add('hidden');
        document.getElementById('step-indicator').textContent = 'No questions available';
        return;
    }
    
    // Update step indicator with dynamic number of questions
    document.getElementById('step-indicator').textContent = `Question 1 of ${totalSteps}`;
    
    // Create question containers dynamically
    const questionContainer = document.getElementById('question-container');
    questionContainer.innerHTML = ''; // Clear container
    
    // Generate HTML for each question
    for (let i = 0; i < totalSteps; i++) {
        const questionNumber = i + 1;
        const isHidden = questionNumber > 1 ? 'hidden' : '';
        
        // Create question container
        const questionElement = document.createElement('div');
        questionElement.id = `question-${questionNumber}`;
        questionElement.className = `question-step ${isHidden} space-y-6`;
        
        // Create question content
        const question = unit.questions[i];
        questionElement.innerHTML = `
            <div class="space-y-4">
                <h2 class="text-lg font-semibold text-gray-700">${questionNumber}. ${question.text.split('?')[0]}?</h2>
                <div class="chat-container bg-gray-50 p-4 rounded-lg max-h-[600px] overflow-y-auto mb-4">
                    <div class="messages" id="chat-messages-${questionNumber}">
                        <!-- Initial bot message will be added here -->
                    </div>
                </div>
                
                <!-- Chat input -->
                <div id="chat-input-${questionNumber}" class="mt-4">
                    <div class="flex space-x-2">
                        <input type="text" class="chat-input flex-1 p-2 border rounded-lg" placeholder="Type your answer...">
                        <button class="send-chat px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[100px]">
                            <span class="button-spinner hidden"></span>
                            <span class="button-text">Send</span>
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Analysis Result Section -->
            <div id="analysis-${questionNumber}" class="analysis-section hidden mt-6 p-4 bg-gray-50 rounded-lg"></div>
        `;
        
        // Add to container
        questionContainer.appendChild(questionElement);
    }
    
    // Initialize each question
    for (let i = 1; i <= totalSteps; i++) {
        initializeChat(i);
    }
    
    // Set up navigation
    document.getElementById('next-btn').addEventListener('click', nextStep);
    document.getElementById('prev-btn').addEventListener('click', prevStep);
    
    // Initialize first step
    updateStepVisibility();
}

/**
 * Go to the next step
 */
function nextStep() {
    if (currentStep < totalSteps) {
        currentStep++;
        updateStepVisibility();
    }
}

/**
 * Go to the previous step
 */
function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        updateStepVisibility();
    }
}

/**
 * Update the visibility of steps
 */
function updateStepVisibility() {
    document.querySelectorAll('.question-step').forEach(step => step.classList.add('hidden'));
    document.getElementById(`question-${currentStep}`).classList.remove('hidden');
    document.getElementById('step-indicator').textContent = `Question ${currentStep} of ${totalSteps}`;
    
    // Update navigation buttons
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    prevBtn.classList.toggle('hidden', currentStep === 1);
    nextBtn.classList.toggle('hidden', currentStep === totalSteps);
}

/**
 * Initialize chat for a question
 * @param {number} questionNumber - The question number
 */
function initializeChat(questionNumber) {
    const config = getConfig();
    const question = config.unit.questions[questionNumber - 1];
    
    if (!question) return;
    
    const messagesContainer = document.getElementById(`chat-messages-${questionNumber}`);
    if (!messagesContainer) return;
    
    // Clear existing messages
    messagesContainer.innerHTML = '';
    
    // Add question title and text as bot messages
    messagesContainer.appendChild(createChatMessage(question.text, true));
    messagesContainer.appendChild(createChatMessage("Please provide your answer to this question.", true));
    
    // Set up chat input
    const chatInput = document.querySelector(`#chat-input-${questionNumber} .chat-input`);
    const sendButton = document.querySelector(`#chat-input-${questionNumber} .send-chat`);
    
    if (chatInput && sendButton) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && chatInput.value.trim()) {
                handleChatMessage(questionNumber, chatInput.value.trim());
                chatInput.value = '';
            }
        });
        
        sendButton.addEventListener('click', () => {
            if (chatInput.value.trim()) {
                handleChatMessage(questionNumber, chatInput.value.trim());
                chatInput.value = '';
            }
        });
    }
}

/**
 * Create a chat message element
 * @param {string} content - The message content
 * @param {boolean} isBot - Whether the message is from the bot
 * @returns {HTMLElement} The message element
 */
function createChatMessage(content, isBot = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${isBot ? 'justify-start' : 'justify-end'} mb-2`;
    
    const messageContent = document.createElement('div');
    messageContent.className = `rounded-lg p-2 max-w-[80%] ${
        isBot ? 'bg-blue-100 text-blue-900 prose prose-sm' : 'bg-green-100 text-green-900'
    }`;
    
    // Parse markdown for bot messages only
    if (isBot) {
        messageContent.innerHTML = marked.parse(content);
    } else {
        messageContent.textContent = content;
    }
    
    messageDiv.appendChild(messageContent);
    return messageDiv;
}

/**
 * Handle a chat message
 * @param {number} questionNumber - The question number
 * @param {string} message - The message text
 */
async function handleChatMessage(questionNumber, message) {
    const config = getConfig();
    const { moduleId, unitId } = config;
    const question = config.unit.questions[questionNumber - 1];
    
    const messagesContainer = document.getElementById(`chat-messages-${questionNumber}`);
    const sendButton = document.querySelector(`#chat-input-${questionNumber} .send-chat`);
    const spinner = sendButton.querySelector('.button-spinner');
    const buttonText = sendButton.querySelector('.button-text');
    
    // Disable button and show spinner
    sendButton.disabled = true;
    spinner.classList.remove('hidden');
    buttonText.textContent = 'Sending...';
    
    // Add user message
    messagesContainer.appendChild(createChatMessage(message, false));
    scrollToBottom(document.querySelector(`#question-${questionNumber} .chat-container`));
    
    // Get module and unit IDs without the prefix
    const moduleNumber = moduleId.replace('module', '');
    const unitNumber = unitId.replace('unit', '');
    
    if (!submittedQuestions.has(questionNumber)) {
        // This is the first submission for this question (initial answer)
        try {
            // Store the answer
            userAnswers[questionNumber] = message;
            
            // Add initial analysis message
            messagesContainer.appendChild(createChatMessage(
                "Thank you for your answer. Here's my analysis:", 
                true
            ));
            
            // Create and append analysis container with loader
            const analysisMessage = document.createElement('div');
            analysisMessage.className = 'flex justify-start mb-2';
            const analysisDiv = document.createElement('div');
            analysisDiv.className = 'rounded-lg p-2 max-w-[80%] bg-blue-100 text-blue-900 prose prose-sm';
            analysisDiv.appendChild(createTypingLoader());
            analysisMessage.appendChild(analysisDiv);
            messagesContainer.appendChild(analysisMessage);
            scrollToBottom(document.querySelector(`#question-${questionNumber} .chat-container`));
            
            // Send for streaming analysis with module/unit parameters and guide
            const response = await analyzeAnswer(
                question.text, 
                message,
                moduleNumber,
                unitNumber,
                question.guide // Add guide to API request
            );

            if (!response.ok) throw new Error('Failed to analyze answer');
            
            let analysisContent = '';
            
            // Process the streaming response
            await processStreamingResponse(
                response,
                (chunk, fullContent, isFirstChunk, score) => {
                    // Handle content chunk
                    if (chunk) {
                        if (isFirstChunk) {
                            // Remove loader on first content
                            analysisDiv.innerHTML = '';
                        }
                        analysisContent = fullContent;
                        analysisDiv.innerHTML = marked.parse(analysisContent);
                        scrollToBottom(document.querySelector(`#question-${questionNumber} .chat-container`));
                    }
                    
                    // Handle score
                    if (score !== undefined) {
                        userScores[questionNumber] = score;
                    }
                },
                (finalContent) => {
                    // Mark question as submitted
                    submittedQuestions.add(questionNumber);
                    
                    // Add follow-up prompt
                    messagesContainer.appendChild(createChatMessage(
                        "You can now ask follow-up questions about this topic.", 
                        true
                    ));
                    scrollToBottom(document.querySelector(`#question-${questionNumber} .chat-container`));
                },
                (error) => {
                    console.error('Error:', error);
                    messagesContainer.appendChild(createChatMessage(
                        'Sorry, I encountered an error analyzing your answer. Please try again.', 
                        true
                    ));
                    scrollToBottom(document.querySelector(`#question-${questionNumber} .chat-container`));
                }
            );
            
        } catch (error) {
            console.error('Error:', error);
            messagesContainer.appendChild(createChatMessage(
                'Sorry, I encountered an error analyzing your answer. Please try again.', 
                true
            ));
            scrollToBottom(document.querySelector(`#question-${questionNumber} .chat-container`));
        } finally {
            sendButton.disabled = false;
            spinner.classList.add('hidden');
            buttonText.textContent = 'Send';
        }
    } else {
        // This is a follow-up question
        try {
            // Create response message container with loader for follow-up questions
            const responseContainer = createChatMessage("", true);
            const responseContent = responseContainer.querySelector('div');
            responseContent.appendChild(createTypingLoader());
            messagesContainer.appendChild(responseContainer);
            scrollToBottom(document.querySelector(`#question-${questionNumber} .chat-container`));
            
            // Collect conversation history
            const history = Array.from(messagesContainer.children).map(msg => {
                const messageDiv = msg.querySelector('div');
                return {
                    content: messageDiv.textContent,
                    isBot: messageDiv.classList.contains('bg-blue-100')
                };
            });

            // Pass module/unit number parameters
            const response = await askBot(
                message,
                history,
                moduleNumber,
                unitNumber
            );

            if (!response.ok) throw new Error('Failed to get response');
            
            // Process the streaming response
            await processStreamingResponse(
                response,
                (chunk, fullContent, isFirstChunk) => {
                    if (chunk) {
                        if (isFirstChunk) {
                            // Remove loader on first content
                            responseContent.innerHTML = '';
                        }
                        responseContent.innerHTML = marked.parse(fullContent);
                        scrollToBottom(document.querySelector(`#question-${questionNumber} .chat-container`));
                    }
                },
                null,
                (error) => {
                    console.error('Error:', error);
                    responseContent.innerHTML = 'Sorry, I encountered an error. Please try again.';
                    scrollToBottom(document.querySelector(`#question-${questionNumber} .chat-container`));
                }
            );
        } catch (error) {
            console.error('Error:', error);
            responseContent.innerHTML = 'Sorry, I encountered an error. Please try again.';
            scrollToBottom(document.querySelector(`#question-${questionNumber} .chat-container`));
        } finally {
            sendButton.disabled = false;
            spinner.classList.add('hidden');
            buttonText.textContent = 'Send';
        }
    }
}

// Initialize assessment when document is loaded
document.addEventListener('DOMContentLoaded', () => {
    const moduleParam = new URLSearchParams(window.location.search).get('module');
    const unitParam = new URLSearchParams(window.location.search).get('unit');
    initializeAssessment(moduleParam, unitParam);
}); 