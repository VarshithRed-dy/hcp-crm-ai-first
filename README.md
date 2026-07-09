# AI-First CRM HCP Module – Log Interaction Screen

## Overview

This project is an AI-first CRM module for Healthcare Professional interaction logging.  
The application allows field representatives to log HCP interactions using an AI assistant instead of manually filling out the form.

The left side of the screen contains the HCP interaction form, and the right side contains an AI assistant chat panel. The AI assistant uses LangGraph and an LLM to extract interaction details, populate the form, edit fields, and support sales-related CRM workflows.

## Tech Stack

### Frontend
- React
- Redux Toolkit
- Axios
- Google Inter Font

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

### AI
- LangGraph
- Groq LLM
- Model: gemma2-9b-it

## Core Features

- AI-controlled HCP interaction form
- Conversational assistant for logging interactions
- LangGraph-based agent workflow
- Minimum 5 tools:
  - Log Interaction
  - Edit Interaction
  - Get HCP Profile
  - Suggest Next Best Action
  - Create Follow-up Task
- PostgreSQL database persistence

## Project Structure

```text
hcp-crm-ai-first/
  frontend/
  backend/
  docker-compose.yml
  README.md

  ## Phase 2 Backend Core

Completed backend core setup:

- FastAPI router structure
- SQLAlchemy database models
- Seed HCP data
- HCP read/create APIs
- Interaction create/read/update/delete APIs
- Groq client setup
- Groq test endpoint

### Backend API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
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

## Phase 3 LangGraph Agent and Tools

The backend now includes a LangGraph-based AI agent for controlling the HCP interaction form.

### Agent Flow

```text
User message
  -> Load selected HCP context
  -> Use Groq gemma2-9b-it for intent extraction
  -> Route to the correct LangGraph tool
  -> Execute tool
  -> Log tool execution
  -> Return assistant response and updated form

  ## Phase 4 Frontend

The frontend now includes a complete AI-first CRM interaction logging screen.

### Frontend Features

- Split-screen layout
- Left-side read-only HCP interaction form
- Right-side AI assistant chat panel
- Redux Toolkit state management
- API integration with FastAPI
- Interaction timeline from database
- LangGraph tool execution display

### Key UI Rule

The interaction form is intentionally read-only. Users populate and edit the form through the AI assistant chat. The assistant sends the message to FastAPI, which invokes the LangGraph agent and returns the updated form state.

### Frontend Flow

```text
User enters message in AI assistant
  -> React dispatches Redux action
  -> POST /api/agent/chat
  -> LangGraph routes request to tool
  -> Backend returns updated_form
  -> Redux updates formDraft
  -> Left form refreshes automatically