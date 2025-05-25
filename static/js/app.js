// DOM Elements
const welcomeScreen = document.getElementById('welcome-screen');
const chatInterface = document.getElementById('chat-interface');
const studentNameInput = document.getElementById('student-name');
const startButton = document.getElementById('start-button');
const userNameDisplay = document.getElementById('user-name');
const studentNameDisplays = document.querySelectorAll('.student-name-display');
const questionForm = document.getElementById('question-form');
const questionInput = document.getElementById('question-input');
const chatMessages = document.getElementById('chat-messages');
const settingsButton = document.getElementById('settings-button');
const settingsModal = document.getElementById('settings-modal');
const closeSettingsButton = document.getElementById('close-settings');
const changeNameInput = document.getElementById('change-name');
const saveNameButton = document.getElementById('save-name');
const clearHistoryButton = document.getElementById('clear-history');
// Removed subject tabs
const detectedSubject = document.getElementById('detected-subject');
const indicatorDot = document.querySelector('.indicator-dot');

// State
let currentStudent = {
    name: localStorage.getItem('studentName') || '',
    chatHistory: JSON.parse(localStorage.getItem('chatHistory')) || []
};

// No longer using subject tabs

// Initialize the app
function init() {
    // Check if user has already entered their name
    if (currentStudent.name) {
        showChatInterface();
        updateNameDisplays();
        loadChatHistory();
    }

    // Set up event listeners
    startButton.addEventListener('click', handleStartLearning);
    questionForm.addEventListener('submit', handleQuestionSubmit);
    settingsButton.addEventListener('click', openSettings);
    closeSettingsButton.addEventListener('click', closeSettings);
    saveNameButton.addEventListener('click', updateName);
    clearHistoryButton.addEventListener('click', clearHistory);
}

// Event Handlers
function handleStartLearning() {
    const name = studentNameInput.value.trim();
    if (name) {
        currentStudent.name = name;
        localStorage.setItem('studentName', name);
        showChatInterface();
        updateNameDisplays();
    } else {
        studentNameInput.classList.add('error');
        setTimeout(() => studentNameInput.classList.remove('error'), 1000);
    }
}

async function handleQuestionSubmit(e) {
    e.preventDefault();
    const question = questionInput.value.trim();
    
    if (!question) return;
    
    // Add user message to chat
    addMessageToChat('user', question);
    
    // Clear input
    questionInput.value = '';
    
    // Show typing indicator
    const typingIndicator = addTypingIndicator();
    
    try {
        // Send question to API
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: question })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        typingIndicator.remove();
        
        // Determine subject based on keywords in question and answer
        const subject = detectSubject(question, data.answer);
        
        // Add bot message to chat
        addMessageToChat('bot', data.answer, subject);
        
        // Update subject indicator
        updateSubjectIndicator(subject);
        
        // Save to chat history
        saveMessageToHistory(question, data.answer, subject);
    } catch (error) {
        console.error('Error:', error);
        typingIndicator.remove();
        addMessageToChat('system', 'Sorry, I had trouble processing your question. Please try again.');
    }
}

function openSettings() {
    settingsModal.classList.remove('hidden');
    changeNameInput.value = currentStudent.name;
}

function closeSettings() {
    settingsModal.classList.add('hidden');
}

function updateName() {
    const newName = changeNameInput.value.trim();
    if (newName) {
        currentStudent.name = newName;
        localStorage.setItem('studentName', newName);
        updateNameDisplays();
        closeSettings();
    }
}

function clearHistory() {
    if (confirm('Are you sure you want to clear your chat history?')) {
        currentStudent.chatHistory = [];
        localStorage.removeItem('chatHistory');
        chatMessages.innerHTML = '';
        
        // Add welcome message back
        const welcomeMessage = document.createElement('div');
        welcomeMessage.className = 'message system-message';
        welcomeMessage.innerHTML = `
            <div class="message-content">
                <p>Hi ${currentStudent.name}! I'm your AI tutor. Ask me any math or physics question, and I'll help you learn!</p>
            </div>
        `;
        chatMessages.appendChild(welcomeMessage);
        
        closeSettings();
    }
}

// Subject tabs functionality removed

// Helper Functions
function showChatInterface() {
    welcomeScreen.classList.add('hidden');
    chatInterface.classList.remove('hidden');
}

function updateNameDisplays() {
    userNameDisplay.textContent = currentStudent.name;
    studentNameDisplays.forEach(display => {
        display.textContent = currentStudent.name;
    });
}

function addMessageToChat(sender, content, subject = null) {
    const messageDiv = document.createElement('div');
    
    if (sender === 'user') {
        messageDiv.className = 'message user-message';
    } else if (sender === 'bot') {
        messageDiv.className = 'message bot-message';
        if (subject) {
            messageDiv.dataset.subject = subject;
        }
    } else {
        messageDiv.className = 'message system-message';
    }
    
    let messageHTML = `<div class="message-content"><p>${formatMessageContent(content)}</p></div>`;
    
    if (sender !== 'system') {
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageHTML += `
            <div class="message-metadata">
                <span>${time}</span>
                ${subject ? `<span class="subject-tag ${subject}">${subject}</span>` : ''}
            </div>
        `;
    }
    
    messageDiv.innerHTML = messageHTML;
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageDiv;
}

function addTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'message bot-message typing-indicator';
    indicator.innerHTML = `
        <div class="message-content">
            <p>Thinking<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></p>
        </div>
    `;
    chatMessages.appendChild(indicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Animate dots
    let count = 0;
    const dots = indicator.querySelectorAll('.dot');
    const interval = setInterval(() => {
        dots.forEach((dot, i) => {
            dot.style.opacity = (count + i) % 3 === 0 ? '1' : '0.3';
        });
        count = (count + 1) % 3;
    }, 300);
    
    // Store the interval ID so we can clear it when removing the indicator
    indicator.dataset.intervalId = interval;
    
    return indicator;
}

function formatMessageContent(content) {
    // Use the Marked.js library to parse Markdown
    if (typeof marked !== 'undefined') {
        // Configure Marked options
        marked.setOptions({
            breaks: true,           // Add <br> on single line breaks
            gfm: true,              // GitHub Flavored Markdown
            headerIds: false,       // Don't add IDs to headers
            mangle: false,          // Don't mangle email links
            sanitize: false,        // Don't sanitize HTML (we trust the API)
        });
        
        // Parse Markdown to HTML
        content = marked.parse(content);
        
        // Format math expressions (e.g., $x^2$) - do this after Markdown parsing
        content = content.replace(/\$([^$]+)\$/g, '<span class="math-expression">$1</span>');
        
        return content;
    } else {
        // Fallback if Marked.js isn't loaded
        // Convert line breaks to <br>
        content = content.replace(/\n/g, '<br>');
        
        // Basic formatting for bold and italic
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Format math expressions
        content = content.replace(/\$([^$]+)\$/g, '<span class="math-expression">$1</span>');
        
        return content;
    }
}

function detectSubject(question, answer) {
    // Simple keyword-based detection
    const mathKeywords = ['equation', 'calculate', 'solve', 'math', 'algebra', 'geometry', 'calculus', 'theorem', 'formula', 'number', 'arithmetic'];
    const physicsKeywords = ['physics', 'force', 'energy', 'motion', 'gravity', 'velocity', 'acceleration', 'momentum', 'newton', 'mass', 'weight'];
    const chemistryKeywords = ['chemistry', 'chemical', 'reaction', 'molecule', 'atom', 'element', 'compound', 'acid', 'base', 'periodic table', 'bond', 'organic', 'inorganic', 'solution'];
    const csKeywords = [
        // Programming concepts
        'programming', 'code', 'algorithm', 'computer science', 'data structure', 
        'function', 'variable', 'class', 'object', 'loop', 'conditional', 'software', 
        'development', 'debugging', 
        // Hardware and system components
        'ram', 'memory', 'cpu', 'processor', 'hard drive', 'ssd', 'computer hardware',
        'motherboard', 'gpu', 'graphics card', 'operating system', 'linux', 'windows',
        'mac os', 'binary', 'network', 'internet', 'server', 'database', 'cloud computing'
    ];
    
    // General question indicators
    const generalIndicators = [
        'sorry, i can only answer', 
        'i\'m your educational tutor',
        'how can i help you',
        'my name is',
        'i am a',
        'nice to meet you',
        'hello',
        'hi there'
    ];
    
    const combinedText = (question + ' ' + answer).toLowerCase();
    
    // Check for general question indicators first
    for (const indicator of generalIndicators) {
        if (combinedText.includes(indicator.toLowerCase())) {
            return 'general';
        }
    }
    
    let mathScore = 0;
    let physicsScore = 0;
    let chemistryScore = 0;
    let csScore = 0;
    
    mathKeywords.forEach(keyword => {
        if (combinedText.includes(keyword.toLowerCase())) {
            mathScore++;
        }
    });
    
    physicsKeywords.forEach(keyword => {
        if (combinedText.includes(keyword.toLowerCase())) {
            physicsScore++;
        }
    });
    
    chemistryKeywords.forEach(keyword => {
        if (combinedText.includes(keyword.toLowerCase())) {
            chemistryScore++;
        }
    });
    
    csKeywords.forEach(keyword => {
        if (combinedText.includes(keyword.toLowerCase())) {
            csScore++;
        }
    });
    
    // Find the subject with the highest score
    const scores = [
        { subject: 'math', score: mathScore },
        { subject: 'physics', score: physicsScore },
        { subject: 'chemistry', score: chemistryScore },
        { subject: 'cs', score: csScore }
    ];
    
    // Sort by score in descending order
    scores.sort((a, b) => b.score - a.score);
    
    // If the highest score is greater than 0, return that subject
    if (scores[0].score > 0) {
        return scores[0].subject;
    } else {
        // If no keywords found at all, it's likely a general question
        return 'general';
    }
}

function updateSubjectIndicator(subject) {
    if (subject === 'general') {
        // Hide the subject indicator for general questions
        detectedSubject.textContent = 'General Conversation';
        indicatorDot.className = 'indicator-dot general';
    } else {
        // Show the appropriate subject
        let subjectText = '';
        switch(subject) {
            case 'math':
                subjectText = 'Math Question';
                break;
            case 'physics':
                subjectText = 'Physics Question';
                break;
            case 'chemistry':
                subjectText = 'Chemistry Question';
                break;
            case 'cs':
                subjectText = 'Computer Science Question';
                break;
            default:
                subjectText = 'Academic Question';
        }
        
        detectedSubject.textContent = subjectText;
        indicatorDot.className = 'indicator-dot ' + subject;
    }
}

function saveMessageToHistory(question, answer, subject) {
    const messageObj = {
        timestamp: new Date().toISOString(),
        question,
        answer,
        subject
    };
    
    currentStudent.chatHistory.push(messageObj);
    
    // Limit history to last 100 messages to prevent localStorage overflow
    if (currentStudent.chatHistory.length > 100) {
        currentStudent.chatHistory = currentStudent.chatHistory.slice(-100);
    }
    
    localStorage.setItem('chatHistory', JSON.stringify(currentStudent.chatHistory));
}

function loadChatHistory() {
    if (currentStudent.chatHistory.length === 0) {
        // Add welcome message if no history
        const welcomeMessage = document.createElement('div');
        welcomeMessage.className = 'message system-message';
        welcomeMessage.innerHTML = `
            <div class="message-content">
                <p>Hi ${currentStudent.name}! I'm your AI tutor. Ask me any math or physics question, and I'll help you learn!</p>
            </div>
        `;
        chatMessages.appendChild(welcomeMessage);
        return;
    }
    
    // Clear existing messages
    chatMessages.innerHTML = '';
    
    // Add messages from history
    currentStudent.chatHistory.forEach(msg => {
        // Add user question
        addMessageToChat('user', msg.question);
        
        // Add bot answer
        addMessageToChat('bot', msg.answer, msg.subject);
    });
}

// Filter messages functionality removed

// Initialize the app
document.addEventListener('DOMContentLoaded', init);
