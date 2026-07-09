import { useSelector } from "react-redux";

export default function ToolExecutionDisplay() {
    const { toolLogs } = useSelector((state) => state.crm);

    return (
        <section className="tools-card">
            <h2>LangGraph Tool Executions</h2>
            <p className="subtle">Latest tool audit records from backend</p>

            {toolLogs.length === 0 ? (
                <div className="empty-state">No tool executions yet.</div>
            ) : (
                <div className="tool-log-list">
                    {toolLogs.slice(0, 8).map((log) => (
                        <div className="tool-log-item" key={log.id}>
                            <div>
                                <strong>{log.tool_name}</strong>
                                <span className="status-pill">{log.status}</span>
                            </div>

                            <p>
                                {log.output_payload?.message ||
                                    "Tool executed and logged successfully."}
                            </p>
                        </div>
                    ))}
                </div>
            )}
        </section>
    );
}