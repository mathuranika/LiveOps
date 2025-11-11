# 🚚 NextGen LiveOps — Real-Time Incident Intelligence System

## 📘 Overview
**NextGen LiveOps** is a multi-agent, AI-driven logistics intelligence system built with **Python**, **Streamlit**, and **Gemini 2.5 Flash**. It detects, analyses, and explains operational incidents — such as delivery delays, cost spikes, and customer complaints — in real time.

The app unifies seven datasets from NexGen Logistics to generate actionable insights, automate response planning, and enable natural-language Q&A through an embedded RAG assistant.

---

## 🧠 Key Features
- 🧩 **Multi-Agent Architecture:** Modular agents for data ingestion, incident detection, response planning, and Gemini-powered analytics.  
- ⚡ **Anomaly Detection:** Combines rule-based heuristics and Isolation Forest to flag unusual delays, low ratings, and cost anomalies.  
- 🚛 **Response Planner:** Suggests reroutes or re-assigns vehicles based on fleet availability, traffic, and weather impact.  
- 💬 **RAG Chat Assistant (Gemini):** Answers operator questions like “Why is Order 142 delayed?” using context-aware reasoning.  
- 📊 **Interactive Streamlit Dashboard:** Clean, professional UI for incident review and conversational analytics.  
- **📊 Real-Time KPIs**: Dashboard with key performance indicators and metrics

## 🏗️ Project Structure

```
LiveOps/
├── app.py                          # Main Streamlit application
├── agents/                         # AI Agent modules
│   ├── detection_agent.py          # Data ingestion & incident detection
│   ├── response_agent.py           # Response planning logic
│   ├── communication_agent.py      # Communication orchestration
│   └── rag_agent.py                # RAG-based Q&A agent
├── data/                           # Sample logistics datasets
│   ├── orders.csv                  # Order information
│   ├── delivery_performance.csv    # Delivery metrics
│   ├── customer_feedback.csv       # Customer ratings & 
│   ├── cost_breakdown.csv          # Cost analysis
│   ├── routes_distance.csv         # Route information
│   ├── vehicle_fleet.csv           # Fleet data
│   └── warehouse_inventory.csv     # Inventory levels
└── requirements.txt                # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Google Gemini API Key (for AI assistant features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mathuranika/LiveOps.git
   cd LiveOps
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the dashboard**
   
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage

### 1. View Master Data
The dashboard automatically loads all CSV files from the `data/` directory and displays:
- Combined master dataset preview
- Quick KPIs (total orders, low-rating orders, average costs)

### 2. Detect Incidents
Click **"Run Detection & Plan Responses"** to:
- Flag basic incidents (delays, low ratings)
- Perform anomaly detection using machine learning
- Generate automated response plans

### 3. Query with AI Assistant
Use the Gemini Assistant to ask questions like:
- "Why is Order_ID 142 delayed?"
- "Which customer complained about damaged items?"
- "Show me all high-priority incidents"

The assistant uses RAG to retrieve relevant data and provide context-aware answers.

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, SciPy
- **AI/LLM**: Google Generative AI (Gemini)
- **Environment Management**: Python-dotenv

## 📊 Data Sources

The system processes multiple logistics data streams:
- **Orders**: Order details, customer info, delivery status
- **Delivery Performance**: Actual vs. expected delivery times
- **Customer Feedback**: Ratings and textual feedback
- **Cost Breakdown**: Operational cost analysis
- **Routes & Distance**: Route optimization data
- **Vehicle Fleet**: Fleet availability and status
- **Warehouse Inventory**: Stock levels and SKU information

## 🤖 Agent Architecture

The system uses a multi-agent architecture:

1. **DataIngestionAgent**: Loads and merges data from multiple sources
2. **IncidentDetectionAgent**: Identifies operational issues and anomalies
3. **ResponsePlannerAgent**: Creates actionable response plans
4. **CommunicationAgent**: Manages stakeholder communications
5. **RAGAgent**: Provides intelligent Q&A capabilities

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for AI features | Yes (for LLM features) |

## 📝 License

This project is available for use as an AI-powered logistics intelligence prototype.

## 👤 Author

**Mathuranika**
- GitHub: [@mathuranika](https://github.com/mathuranika)

## 🙏 Acknowledgments

- Built with Streamlit for rapid dashboard development
- Powered by Google's Gemini AI for intelligent insights
- Uses scikit-learn for anomaly detection
