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
            state.formDraft = {
                ...state.formDraft,
                ...action.payload,
            };
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