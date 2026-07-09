# AI-First CRM HCP Module – Log Interaction Screen

## Overview

This project is an AI-first Customer Relationship Management CRM module for Healthcare Professional HCP interaction logging.

The application allows life sciences field representatives to log HCP interactions using a conversational AI assistant instead of manually filling out the form.

The screen uses a split layout:

- Left side: AI-controlled, read-only HCP interaction form
- Right side: AI assistant chat panel

The assistant uses LangGraph and Groq LLM to understand natural language, extract interaction details, populate the form, edit fields, summarize notes, recommend next actions, create follow-up tasks, and save interaction records.

---

## Key Assignment Requirement

The interaction form is intentionally read-only.

Users do not manually fill the form. Instead, they describe the interaction in the AI assistant chat. The backend invokes a LangGraph agent, routes the request to the correct tool, and returns an updated form state to the frontend.

---

## Screenshots

### Main AI-Controlled Log Interaction Screen

![Main UI](docs/screenshots/main-ui.png)

### Interaction Timeline and LangGraph Tool Logs

![Timeline and Tool Logs](docs/screenshots/timeline-tool-logs.png)

---

## Tech Stack

### Frontend

- React
- Redux Toolkit
- React Redux
- Axios
- Google Inter Font
- Vite

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

### AI

- LangGraph
- Groq LLM
- Model: `gemma2-9b-it`

### Database

- PostgreSQL using Docker Compose

---

## Core Features

- Split-screen CRM interaction logging UI
- AI-controlled read-only form
- Conversational AI assistant
- Redux-based frontend state management
- FastAPI backend APIs
- LangGraph-based agent workflow
- Groq LLM integration
- PostgreSQL database persistence
- Interaction timeline
- LangGraph tool execution audit logs
- Six working AI tools

---

## LangGraph Agent Flow

```text
User message
  -> FastAPI /api/agent/chat
  -> Load selected HCP context
  -> Use Groq gemma2-9b-it for intent extraction
  -> Route request through LangGraph conditional edges
  -> Execute selected tool
  -> Save tool execution log
  -> Return assistant response and updated form
  -> Redux updates the read-only form
```

---

## LangGraph Nodes

| Node | Purpose |
|---|---|
| `load_context` | Loads selected HCP information |
| `intent_extraction` | Uses Groq LLM to classify intent and extract structured fields |
| `tool_router` | Routes the request to the correct tool |
| `log_interaction` | Captures and optionally saves HCP interaction |
| `edit_interaction` | Updates draft or saved interaction data |
| `get_hcp_profile` | Retrieves selected HCP profile |
| `suggest_next_action` | Recommends next best sales action |
| `create_follow_up_task` | Creates a follow-up task |
| `summarize_interaction` | Summarizes interaction notes |
| `response_generation` | Generates final assistant response |

---

## LangGraph Tools Implemented

### 1. Log Interaction

Captures HCP interaction details from natural language.

Example input:

```text
Log and save this interaction: Met Dr. Emily Smith today at 7:30 PM. Discussed Prodo-X efficacy, shared a product brochure, sentiment was positive, and she asked for a follow-up next week.
```

The tool extracts:

- HCP name
- Interaction type
- Date
- Time
- Attendees
- Topics discussed
- Materials shared
- Sentiment
- Next step
- Follow-up details

It updates the form and saves the interaction record when save is requested.

---

### 2. Edit Interaction

Allows the user to modify form fields using natural language.

Example input:

```text
Change the sentiment to neutral and update the next step to send payer access details before the follow-up.
```

The tool updates the form and saved interaction record.

---

### 3. Get HCP Profile

Retrieves profile information for the selected HCP.

Example input:

```text
Show me Dr. Emily Smith's profile.
```

The tool returns:

- Name
- Specialty
- Territory
- Segment
- Preferred channel
- Organization
- Last interaction date

---

### 4. Suggest Next Best Action

Recommends the next best sales action based on the current form and interaction context.

Example input:

```text
What should I do next for this HCP?
```

The tool generates a CRM-friendly recommendation and updates the next step field.

---

### 5. Create Follow-up Task

Creates a follow-up task linked to the HCP and current interaction.

Example input:

```text
Create a follow-up task to send the Prodo-X clinical deck next Friday.
```

The tool creates a follow-up task and logs the tool execution.

---

### 6. Summarize Interaction

Summarizes raw interaction notes into concise CRM-safe language.

Example input:

```text
Summarize this interaction: Dr. Smith was interested in Prodo-X but asked for more efficacy data and payer coverage information before deciding next steps.
```

The tool updates the AI Summary field in the form.

---

## Project Structure

```text
hcp-crm-ai-first/
  backend/
    app/
      agent/
        graph.py
        prompts.py
        state.py
        tools.py
      routers/
        agent.py
        ai.py
        hcp.py
        interactions.py
      services/
        groq_client.py
      database.py
      main.py
      models.py
      schemas.py
      seed_data.py
    requirements.txt
    .env.example

  frontend/
    src/
      api/
        client.js
      components/
        AiAssistant.jsx
        InteractionForm.jsx
        InteractionTimeline.jsx
        ToolExecutionDisplay.jsx
      features/
        chatSlice.js
        crmSlice.js
      store/
        store.js
      App.jsx
      App.css
      main.jsx
      index.css
    package.json

  docs/
    screenshots/
      main-ui.png
      timeline-tool-logs.png

  docker-compose.yml
  README.md
  .gitignore
```

---

## Environment Variables

Create a local `.env` file inside the `backend` folder using `.env.example`.

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/hcp_crm
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=gemma2-9b-it
```

Important: Do not commit the real `.env` file.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/hcp-crm-ai-first.git
cd hcp-crm-ai-first
```

---

### 2. Start PostgreSQL

```bash
docker compose up -d
```

This starts PostgreSQL on:

```text
localhost:5432
```

---

### 3. Start Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

For Windows:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://localhost:8000
```

FastAPI Swagger docs:

```text
http://localhost:8000/docs
```

---

### 4. Start Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at:

```text
http://localhost:5173
```

---

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend root check |
| GET | `/health` | Health check |
| GET | `/api/hcps/` | Get all HCPs |
| GET | `/api/hcps/{hcp_id}` | Get HCP by ID |
| POST | `/api/hcps/` | Create HCP |
| POST | `/api/interactions/` | Create interaction |
| GET | `/api/interactions/` | Get all interactions |
| GET | `/api/interactions/?hcp_id=1` | Get interactions by HCP |
| GET | `/api/interactions/{interaction_id}` | Get interaction by ID |
| PUT | `/api/interactions/{interaction_id}` | Update interaction |
| DELETE | `/api/interactions/{interaction_id}` | Delete interaction |
| POST | `/api/ai/groq-test` | Test Groq LLM connection |
| GET | `/api/ai/tool-logs` | Get LangGraph tool execution logs |
| POST | `/api/agent/chat` | Main LangGraph agent chat endpoint |

---

## Main Agent API

### Endpoint

```http
POST /api/agent/chat
```

### Sample Request

```json
{
  "message": "Log and save this interaction: Met Dr. Emily Smith today at 7:30 PM. Discussed Prodo-X efficacy, shared a product brochure, sentiment was positive, and she asked for a follow-up next week.",
  "selected_hcp_id": 1,
  "current_form": {}
}
```

### Sample Response

```json
{
  "assistant_response": "The interaction was saved successfully.",
  "tool_name": "log_interaction",
  "intent": "log_interaction",
  "confidence": 0.95,
  "updated_form": {
    "hcp_id": 1,
    "hcp_name": "Dr. Emily Smith",
    "interaction_type": "Meeting",
    "interaction_date": "2026-07-09",
    "interaction_time": "19:30",
    "attendees": "Dr. Emily Smith",
    "topics_discussed": "Prodo-X efficacy",
    "materials_shared": "product brochure",
    "sentiment": "positive",
    "next_step": "follow-up next week"
  }
}
```

---

## Demo Prompts

Use these prompts to test and demonstrate all tools.

### Log Interaction

```text
Log and save this interaction: Met Dr. Emily Smith today at 7:30 PM. Discussed Prodo-X efficacy, shared a product brochure, sentiment was positive, and she asked for a follow-up next week.
```

### Edit Interaction

```text
Change the sentiment to neutral and update the next step to send payer access details before the follow-up.
```

### Get HCP Profile

```text
Show me Dr. Emily Smith's profile.
```

### Suggest Next Action

```text
What should I do next for this HCP?
```

### Create Follow-up Task

```text
Create a follow-up task to send the Prodo-X clinical deck next Friday.
```

### Summarize Interaction

```text
Summarize this interaction: Dr. Smith was interested in Prodo-X but asked for more efficacy data and payer coverage information before deciding next steps.
```

---

## Frontend Behavior

The frontend uses Redux Toolkit to manage:

- HCP list
- Selected HCP
- AI-controlled form draft
- Chat messages
- Interaction timeline
- LangGraph tool execution logs

Frontend flow:

```text
User enters message in AI assistant
  -> React dispatches Redux action
  -> POST /api/agent/chat
  -> FastAPI invokes LangGraph agent
  -> LangGraph routes request to selected tool
  -> Backend returns updated_form
  -> Redux updates formDraft
  -> Left-side read-only form refreshes automatically
```

---

## Database Tables

| Table | Purpose |
|---|---|
| `hcps` | Stores sample HCP profile data |
| `interactions` | Stores logged HCP interactions |
| `follow_up_tasks` | Stores follow-up tasks created by AI |
| `agent_tool_logs` | Stores audit logs for each LangGraph tool execution |

---

## Demo Video Walkthrough Plan

Recommended video flow:

1. Show the assignment goal and tech stack.
2. Show the split-screen UI.
3. Explain that the form is read-only and AI-controlled.
4. Click or enter the Log Interaction prompt.
5. Show the left form getting populated.
6. Demo Edit Interaction.
7. Demo Get HCP Profile.
8. Demo Suggest Next Action.
9. Demo Create Follow-up Task.
10. Demo Summarize Interaction.
11. Show Interaction Timeline.
12. Show LangGraph Tool Executions.
13. Briefly show backend LangGraph files:
    - `backend/app/agent/graph.py`
    - `backend/app/agent/tools.py`
    - `backend/app/agent/prompts.py`
14. Briefly show frontend Redux files:
    - `frontend/src/features/chatSlice.js`
    - `frontend/src/features/crmSlice.js`
15. End with explanation of how LangGraph, Groq, FastAPI, PostgreSQL, and Redux work together.

---

## Notes

This is a prototype assignment implementation. It demonstrates the required AI-first HCP interaction logging workflow using LangGraph, Groq LLM, FastAPI, React, Redux, and PostgreSQL.

The implementation is focused on demonstrating:

- AI-controlled form population
- LangGraph tool routing
- LLM-based extraction and summarization
- CRM interaction persistence
- Tool execution audit logging