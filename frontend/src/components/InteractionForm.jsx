import { useDispatch, useSelector } from "react-redux";
import {
    resetFormDraft,
    setSelectedHcp,
} from "../features/crmSlice";

const fieldRows = [
    [
        {
            key: "hcp_name",
            label: "HCP Name",
            type: "select",
        },
        {
            key: "interaction_type",
            label: "Interaction Type",
            type: "text",
            placeholder: "Meeting / Call / Email / Conference",
        },
    ],
    [
        {
            key: "interaction_date",
            label: "Date",
            type: "text",
            placeholder: "YYYY-MM-DD",
        },
        {
            key: "interaction_time",
            label: "Time",
            type: "text",
            placeholder: "07:30 PM",
        },
    ],
];

const longFields = [
    {
        key: "attendees",
        label: "Attendees",
        placeholder: "AI will populate attendees",
    },
    {
        key: "topics_discussed",
        label: "Topics Discussed",
        placeholder: "AI will populate key discussion points",
        textarea: true,
    },
    {
        key: "materials_shared",
        label: "Materials Shared",
        placeholder: "AI will populate shared materials",
    },
    {
        key: "samples_distributed",
        label: "Samples Distributed",
        placeholder: "AI will populate samples",
    },
    {
        key: "sentiment",
        label: "Sentiment",
        placeholder: "Positive / Neutral / Negative",
    },
    {
        key: "outcome",
        label: "Outcome",
        placeholder: "AI will populate outcome",
        textarea: true,
    },
    {
        key: "next_step",
        label: "Next Step",
        placeholder: "AI will recommend or capture next step",
        textarea: true,
    },
    {
        key: "follow_up_date",
        label: "Follow-up Date",
        placeholder: "YYYY-MM-DD",
    },
    {
        key: "ai_summary",
        label: "AI Summary",
        placeholder: "AI-generated CRM summary",
        textarea: true,
    },
];

function ReadOnlyInput({ value, placeholder }) {
    return (
        <input
            value={value || ""}
            placeholder={placeholder}
            readOnly
            className="readonly-input"
        />
    );
}

function ReadOnlyTextarea({ value, placeholder }) {
    return (
        <textarea
            value={value || ""}
            placeholder={placeholder}
            readOnly
            className="readonly-textarea"
        />
    );
}

export default function InteractionForm() {
    const dispatch = useDispatch();
    const { hcps, selectedHcpId, formDraft } = useSelector((state) => state.crm);

    const handleHcpChange = (event) => {
        const value = event.target.value ? Number(event.target.value) : null;
        dispatch(setSelectedHcp(value));
    };

    return (
        <section className="form-card">
            <div className="section-header">
                <div>
                    <h1>Log HCP Interaction</h1>
                    <p className="subtle">
                        AI-controlled form. Use the assistant on the right to populate or edit fields.
                    </p>
                </div>

                <button
                    type="button"
                    className="secondary-button"
                    onClick={() => dispatch(resetFormDraft())}
                >
                    Reset Form
                </button>
            </div>

            <div className="compliance-note">
                The form is read-only by design for this assignment. All updates are driven by
                LangGraph tools and Groq LLM extraction.
            </div>

            <h3>Interaction Details</h3>

            {fieldRows.map((row) => (
                <div className="form-grid" key={row.map((field) => field.key).join("-")}>
                    {row.map((field) => (
                        <div className="field" key={field.key}>
                            <label>{field.label}</label>

                            {field.key === "hcp_name" ? (
                                <select value={selectedHcpId || ""} onChange={handleHcpChange}>
                                    <option value="">Search or select HCP...</option>
                                    {hcps.map((hcp) => (
                                        <option key={hcp.id} value={hcp.id}>
                                            {hcp.name} — {hcp.specialty}
                                        </option>
                                    ))}
                                </select>
                            ) : (
                                <ReadOnlyInput
                                    value={formDraft[field.key]}
                                    placeholder={field.placeholder}
                                />
                            )}
                        </div>
                    ))}
                </div>
            ))}

            <div className="stacked-fields">
                {longFields.map((field) => (
                    <div className="field" key={field.key}>
                        <label>{field.label}</label>

                        {field.textarea ? (
                            <ReadOnlyTextarea
                                value={formDraft[field.key]}
                                placeholder={field.placeholder}
                            />
                        ) : (
                            <ReadOnlyInput
                                value={formDraft[field.key]}
                                placeholder={field.placeholder}
                            />
                        )}
                    </div>
                ))}
            </div>
        </section>
    );
}