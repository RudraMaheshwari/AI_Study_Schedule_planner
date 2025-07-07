# AI Study Schedule Planner

A sophisticated AI-powered study planner that demonstrates the **Planning Pattern** using LangGraph StateGraph. The system breaks down complex study scheduling into manageable, sequential steps for optimal learning outcomes.

## 🎯 Features

- **AI-Powered Planning**: Uses AWS Bedrock Claude model for intelligent planning
- **StateGraph Architecture**: Implements LangGraph for structured planning workflow
- **Four-Step Planning Process**: Goal Analysis → Time Allocation → Daily Scheduling → Optimization
- **Interactive UI**: Clean Streamlit interface for easy interaction
- **Persistent Memory**: InMemorySaver for session state management
- **Downloadable Plans**: Export your study schedule as Markdown

## 🏗️ Architecture

The planner uses a four-node StateGraph:

1. **Goal Analysis**: Analyzes topics and assigns difficulty levels
2. **Time Allocation**: Distributes study hours based on complexity
3. **Daily Schedule**: Creates detailed day-by-day plans
4. **Optimization**: Refines the plan for maximum effectiveness

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- AWS credentials configured

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd study-schedule-planner
2. **Install dependencies**
    ```bash
    pip install -r requirements.txt

3. **Configure environment**
    ```bash
    cp .env.example .env

# Edit .env with your AWS credentials

4. **Run the application**
    ```bash
    streamlit run app.py


# Study Schedule Planner

## 📖 Usage

### Enter Study Details:

1. **Study Goal** (e.g., "Math Final Exam")
2. **Time Available** (7-30 days)
3. **Daily Study Time** (0.5-12 hours)
4. **Topics to Cover** (comma-separated)

### Generate Plan:
Click "Generate Study Schedule"

### Review & Download:
View your personalized plan and download as needed.

## 🧪 Test Case

**Input:**

- Study Goal: "Math Final Exam"
- Time Available: 10 days
- Daily Study Time: 3 hours
- Topics: "Algebra, Geometry, Statistics"

**Expected Output:**

- 10-day structured schedule
- 30 total study hours
- Geometry prioritized (harder topic)
- Review sessions in final days
- Detailed time blocks and study methods

## 📁 Project Structure

study-schedule-planner/
├── src/
│   ├── agentic_prompt/     # AI prompts and templates
│   ├── tools/              # Planning utilities and helpers
│   ├── utils/              # General utility functions
│   ├── agent/              # Main LangGraph agent
│   └── models/             # Pydantic models and state definitions
├── app.py                  # Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
└── README.md              # Project documentation
🔧 Key Components


## 🔧 Key Components

- `StudyPlannerAgent`: Main LangGraph implementation
- `StudyPlanState`: TypedDict for state management
- `Planning Tools`: Utility functions for time allocation
- `Streamlit UI`: Interactive web interface

## 🛠️ Technologies

- LangGraph: StateGraph workflow management
- LangChain: LLM integration and tooling
- AWS Bedrock: Claude model access
- Streamlit: Web UI framework
- Pydantic: Data validation and modeling

## 📝 License

This project is created for educational purposes as part of an AI planning pattern assignment.

## 🤝 Contributing

This is an assignment project. For educational use and reference only.
