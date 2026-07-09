import { useSelector } from "react-redux";

export default function InteractionTimeline() {
    const { interactions } = useSelector((state) => state.crm);

    return (
        <section className="timeline-card">
            <h2>Interaction Timeline</h2>
            <p className="subtle">Saved interaction records from the database</p>

            {interactions.length === 0 ? (
                <div className="empty-state">No saved interactions yet.</div>
            ) : (
                <div className="timeline-list">
                    {interactions.map((interaction) => (
                        <div className="timeline-item" key={interaction.id}>
                            <div className="timeline-title">
                                {interaction.hcp_name || "Unknown HCP"}
                            </div>

                            <div className="timeline-meta">
                                {interaction.interaction_type || "Interaction"} •{" "}
                                {interaction.interaction_date || "No date"} •{" "}
                                {interaction.sentiment || "No sentiment"}
                            </div>

                            <p>
                                {interaction.ai_summary ||
                                    interaction.topics_discussed ||
                                    interaction.raw_notes ||
                                    "No summary available."}
                            </p>

                            {interaction.next_step && (
                                <div className="next-step">
                                    <strong>Next step:</strong> {interaction.next_step}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </section>
    );
}