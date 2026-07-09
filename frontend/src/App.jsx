import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import AiAssistant from "./components/AiAssistant";
import InteractionForm from "./components/InteractionForm";
import InteractionTimeline from "./components/InteractionTimeline";
import ToolExecutionDisplay from "./components/ToolExecutionDisplay";
import {
  fetchHcps,
  fetchInteractions,
  fetchToolLogs,
} from "./features/crmSlice";

export default function App() {
  const dispatch = useDispatch();
  const { selectedHcpId } = useSelector((state) => state.crm);

  useEffect(() => {
    dispatch(fetchHcps());
    dispatch(fetchInteractions());
    dispatch(fetchToolLogs());
  }, [dispatch]);

  useEffect(() => {
    dispatch(fetchInteractions(selectedHcpId));
  }, [dispatch, selectedHcpId]);

  return (
    <main className="app-shell">
      <header className="app-header">
        <div>
          <h1>AI-First CRM HCP Module</h1>
          <p>
            Conversational, LangGraph-powered interaction logging for field representatives
          </p>
        </div>

        <div className="stack-badges">
          <span>React</span>
          <span>Redux</span>
          <span>FastAPI</span>
          <span>LangGraph</span>
          <span>Groq</span>
        </div>
      </header>

      <section className="main-layout">
        <InteractionForm />
        <AiAssistant />
      </section>

      <section className="bottom-layout">
        <InteractionTimeline />
        <ToolExecutionDisplay />
      </section>
    </main>
  );
}