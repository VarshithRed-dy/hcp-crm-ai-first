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