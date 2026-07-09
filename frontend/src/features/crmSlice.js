import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { apiClient } from "../api/client";

const emptyForm = {
    id: null,
    hcp_id: null,
    hcp_name: "",
    interaction_type: "",
    interaction_date: "",
    interaction_time: "",
    attendees: "",
    topics_discussed: "",
    materials_shared: "",
    samples_distributed: "",
    sentiment: "",
    outcome: "",
    next_step: "",
    follow_up_date: "",
    raw_notes: "",
    ai_summary: "",
};

function normalizeFormPayload(payload = {}) {
    return {
        ...payload,

        hcp_id: payload.hcp_id ?? payload.hcpId ?? null,
        hcp_name: payload.hcp_name ?? payload.hcpName ?? payload.hcp ?? "",

        interaction_type:
            payload.interaction_type ?? payload.interactionType ?? payload.type ?? "",

        interaction_date:
            payload.interaction_date ?? payload.date ?? payload.interactionDate ?? "",

        interaction_time:
            payload.interaction_time ?? payload.time ?? payload.interactionTime ?? "",

        attendees:
            payload.attendees ?? payload.attendee ?? "",

        topics_discussed:
            payload.topics_discussed ??
            payload.topics ??
            payload.discussion_points ??
            "",

        materials_shared:
            payload.materials_shared ??
            payload.materials ??
            payload.material_shared ??
            "",

        samples_distributed:
            payload.samples_distributed ??
            payload.samples ??
            "",

        sentiment:
            payload.sentiment ?? "",

        outcome:
            payload.outcome ?? "",

        next_step:
            payload.next_step ?? payload.nextStep ?? payload.follow_up_action ?? "",

        follow_up_date:
            payload.follow_up_date ?? payload.followUpDate ?? payload.follow_up ?? "",

        raw_notes:
            payload.raw_notes ?? payload.rawNotes ?? "",

        ai_summary:
            payload.ai_summary ?? payload.summary ?? payload.aiSummary ?? "",
    };
}

export const fetchHcps = createAsyncThunk("crm/fetchHcps", async () => {
    const response = await apiClient.get("/api/hcps/");
    return response.data;
});

export const fetchInteractions = createAsyncThunk(
    "crm/fetchInteractions",
    async (hcpId) => {
        const url = hcpId ? `/api/interactions/?hcp_id=${hcpId}` : "/api/interactions/";
        const response = await apiClient.get(url);
        return response.data;
    }
);

export const fetchToolLogs = createAsyncThunk("crm/fetchToolLogs", async () => {
    const response = await apiClient.get("/api/ai/tool-logs");
    return response.data;
});

const crmSlice = createSlice({
    name: "crm",
    initialState: {
        hcps: [],
        selectedHcpId: null,
        formDraft: emptyForm,
        interactions: [],
        toolLogs: [],
        loading: false,
        error: null,
    },
    reducers: {
        setSelectedHcp(state, action) {
            const selectedId = action.payload;
            state.selectedHcpId = selectedId;

            const selectedHcp = state.hcps.find((hcp) => hcp.id === Number(selectedId));

            if (selectedHcp) {
                state.formDraft.hcp_id = selectedHcp.id;
                state.formDraft.hcp_name = selectedHcp.name;
            }
        },

        applyUpdatedForm(state, action) {
            const updatedForm = normalizeFormPayload(action.payload || {});

            state.formDraft = {
                ...state.formDraft,
                ...updatedForm,
            };

            if (updatedForm.hcp_id) {
                state.selectedHcpId = Number(updatedForm.hcp_id);
            }
        },

        resetFormDraft(state) {
            state.formDraft = {
                ...emptyForm,
            };

            if (state.selectedHcpId) {
                const selectedHcp = state.hcps.find(
                    (hcp) => hcp.id === Number(state.selectedHcpId)
                );

                if (selectedHcp) {
                    state.formDraft.hcp_id = selectedHcp.id;
                    state.formDraft.hcp_name = selectedHcp.name;
                }
            }
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchHcps.pending, (state) => {
                state.loading = true;
            })
            .addCase(fetchHcps.fulfilled, (state, action) => {
                state.loading = false;
                state.hcps = action.payload;
            })
            .addCase(fetchHcps.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message;
            })

            .addCase(fetchInteractions.fulfilled, (state, action) => {
                state.interactions = action.payload;
            })

            .addCase(fetchToolLogs.fulfilled, (state, action) => {
                state.toolLogs = action.payload;
            });
    },
});

export const { setSelectedHcp, applyUpdatedForm, resetFormDraft } =
    crmSlice.actions;

export default crmSlice.reducer;