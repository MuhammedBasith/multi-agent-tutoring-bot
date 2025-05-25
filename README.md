# Gemini Tutor - Multi-Agent Learning Assistant

## What is this project?

Gemini Tutor is an AI-powered learning assistant that helps students with questions in math, physics, chemistry, and computer science. It uses a multi-agent system where each subject has its own specialized agent that knows how to handle questions in that field.

Unlike simple chatbots, this system can actually understand what subject your question is about and send it to the right expert. It can also use special tools - like a calculator for math problems or code analysis for programming questions.

## Project Structure

The project is built with these main parts:

- **Frontend**: A clean, modern web interface where students can ask questions and see answers with proper formatting
- **Backend API**: Built with FastAPI to handle requests and communicate with the agents
- **Agent System**: A main "tutor" agent that figures out what subject your question is about, then passes it to the right specialist
- **Specialist Agents**: Four different agents that handle specific subjects:
  - Math Agent (with calculator tool)
  - Physics Agent (with physics calculation tools)
  - Chemistry Agent (with equation balancing and analysis)
  - Computer Science Agent (with code analysis and algorithm explanations)

## Setting Up Locally

### Requirements

- Python 3.8 or higher
- A Google Gemini API key
- Basic knowledge of running commands in a terminal

### Step 1: Clone the Repository

```bash
git clone https://github.com/MuhammedBasith/multi-agent-tutoring-bot.git
cd gemini-tutor
```

### Step 2: Set Up a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it (on Windows)
venv\Scripts\activate

# Activate it (on Mac/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Your API Key

1. Create a file named `.env` in the project root
2. Add your Gemini API key to the file like this:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Application

1. Make sure your virtual environment is activated
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
3. Open your browser and go to: http://localhost:8000
4. Enter your name and start asking questions!

## How It Works

### The Multi-Agent System

When you ask a question, here's what happens:

1. The **Tutor Agent** receives your question and analyzes what subject it's about
2. It sends your question to the right **Specialist Agent** (math, physics, chemistry, or computer science)
3. The specialist uses its knowledge and tools to craft a helpful answer
4. The answer is formatted nicely and sent back to you

### Special Tools

Each agent has special tools to help answer questions better:

- **Math Agent**: Can solve equations and do calculations
- **Physics Agent**: Can solve physics problems with formulas for motion, energy, and forces
- **Chemistry Agent**: Can balance chemical equations and identify functional groups
- **Computer Science Agent**: Can analyze code, explain algorithms, and provide programming help

### User Interface

The web interface has these features:

- **Name Storage**: Remembers your name between sessions
- **Chat History**: Saves your conversation in your browser
- **Markdown Support**: Shows formatted text with headings, bold, code blocks, etc.
- **Subject Indicators**: Shows what subject each question belongs to

## Challenges and Solutions

### Challenge 1: Subject Classification

It was tricky to make the system correctly identify what subject a question was about. Sometimes a question about RAM would be classified as math instead of computer science.

**Solution**: We improved the keyword detection system and added more context-aware classification using Gemini's understanding of different subjects.

### Challenge 2: Tool Integration

Making the AI agents use tools at the right time was difficult. Sometimes they would try to answer directly when using a tool would be better.

**Solution**: We created a two-step approach where the agent first decides if a tool is needed, then uses it appropriately.

### Challenge 3: Markdown Rendering

Gemini's responses include formatting like bold text and headings, but displaying this correctly was challenging.

**Solution**: We integrated a Markdown parser (Marked.js) to properly render all the formatting in the responses.

## Live Demo

You can try out the live application here: [Gemini Tutor Demo](https://gemini-tutor-demo.netlify.app)

## Feedback and Contributions

If you have ideas for improvements or want to contribute, please:

1. Open an issue to discuss what you'd like to change
2. Submit a pull request with your changes


