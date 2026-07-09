import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
    addUserMessage,
    clearChat,
    sendAgentMessage,
} from "../features/chatSlice";

const demoPrompts = [
    {
        label: "Log Interaction",
        text: "Log and save this interaction: Met Dr. Emily Smith today at 7:30 PM. Discussed Prodo-X efficacy, shared a product brochure, sentiment was positive, and she asked for a follow-up next week.",
    },
    {
        label: "Edit Interaction",
        text: "Change the sentiment to neutral and update the next step to send payer access details before the follow-up.",
    },
    {
        label: "Get HCP Profile",
        text: "Show me Dr. Emily Smith's profile.",
    },
    {
        label: "Suggest Next Action",
        text: "What should I do next for this HCP?",
    },
    {
        label: "Create Follow-up Task",
        text: "Create a follow-up task to send the Prodo-X clinical deck next Friday.",
    },
    {
        label: "Summarize",
        text: "Summarize this interaction: Dr. Smith was interested in Prodo-X but asked for more efficacy data and payer coverage information before deciding next steps.",
    },
];

export default function AiAssistant() {
    const dispatch = useDispatch();
    const { messages, loading, error, lastToolName, lastConfidence } = useSelector(
        (state) => state.chat
    );

    const [message, setMessage] = useState("");

    const submitMessage = async (textToSend = message) => {
        const trimmed = textToSend.trim();

        if (!trimmed || loading) {
            return;
        }

        dispatch(addUserMessage(trimmed));
        setMessage("");
        dispatch(sendAgentMessage(trimmed));
    };

    const handleKeyDown = (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            submitMessage();
        }
    };

    return (
        <section className="chat-card">
            <div className="chat-header">
                <div>
                    <h2>🤖 AI Assistant</h2>
                    <p className="subtle">Log interaction details here via chat</p>
                </div>

                <button
                    type="button"
                    className="secondary-button"
                    onClick={() => dispatch(clearChat())}
                >
                    Clear
                </button>
            </div>

            <div className="tool-status-bar">
                <span>
                    Last Tool: <strong>{lastToolName || "None yet"}</strong>
                </span>
                <span>
                    Confidence:{" "}
                    <strong>
                        {lastConfidence ? `${Math.round(lastConfidence * 100)}%` : "N/A"}
                    </strong>
                </span>
            </div>

            <div className="demo-prompts">
                {demoPrompts.map((prompt) => (
                    <button
                        key={prompt.label}
                        type="button"
                        onClick={() => submitMessage(prompt.text)}
                        disabled={loading}
                    >
                        {prompt.label}
                    </button>
                ))}
            </div>

            <div className="chat-messages">
                {messages.map((item, index) => (
                    <div
                        key={`${item.role}-${index}`}
                        className={`message-bubble ${item.role}`}
                    >
                        <div className="message-content">{item.content}</div>

                        {item.toolName && (
                            <div className="tool-badge">Tool used: {item.toolName}</div>
                        )}

                        {item.confidence && (
                            <div className="confidence-badge">
                                Confidence: {Math.round(item.confidence * 100)}%
                            </div>
                        )}
                    </div>
                ))}

                {loading && (
                    <div className="message-bubble assistant">
                        <div className="message-content">Thinking and routing through LangGraph...</div>
                    </div>
                )}

                {error && <div className="error-box">{error}</div>}
            </div>

            <div className="chat-input-row">
                <textarea
                    value={message}
                    onChange={(event) => setMessage(event.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Describe interaction..."
                    rows={2}
                />

                <button
                    type="button"
                    className="primary-button"
                    onClick={() => submitMessage()}
                    disabled={loading}
                >
                    AI Log
                </button>
            </div>
        </section>
    );
}