import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { apiClient } from "../api/client";
import {
    applyUpdatedForm,
    fetchInteractions,
    fetchToolLogs,
} from "./crmSlice";

export const sendAgentMessage = createAsyncThunk(
    "chat/sendAgentMessage",
    async (message, thunkApi) => {
        const state = thunkApi.getState();

        const payload = {
            message,
            selected_hcp_id: state.crm.selectedHcpId,
            current_form: state.crm.formDraft,
        };

        const response = await apiClient.post("/api/agent/chat", payload);

        const data = response.data;

        if (data.updated_form) {
            thunkApi.dispatch(applyUpdatedForm(data.updated_form));
        }

        thunkApi.dispatch(fetchInteractions(state.crm.selectedHcpId));
        thunkApi.dispatch(fetchToolLogs());

        return data;
    }
);

const chatSlice = createSlice({
    name: "chat",
    initialState: {
        messages: [
            {
                role: "assistant",
                content:
                    'Log HCP interaction details here. Example: "Met Dr. Emily Smith, discussed Prodo-X efficacy, shared brochure, positive sentiment, follow-up next week."',
                toolName: null,
            },
        ],
        loading: false,
        error: null,
        lastToolName: null,
        lastConfidence: null,
    },
    reducers: {
        addUserMessage(state, action) {
            state.messages.push({
                role: "user",
                content: action.payload,
                toolName: null,
            });
        },

        clearChat(state) {
            state.messages = [
                {
                    role: "assistant",
                    content:
                        "Chat cleared. Tell me about the HCP interaction and I will populate the form.",
                    toolName: null,
                },
            ];
            state.lastToolName = null;
            state.lastConfidence = null;
            state.error = null;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(sendAgentMessage.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(sendAgentMessage.fulfilled, (state, action) => {
                state.loading = false;

                state.messages.push({
                    role: "assistant",
                    content: action.payload.assistant_response || "Done.",
                    toolName: action.payload.tool_name,
                    confidence: action.payload.confidence,
                });

                state.lastToolName = action.payload.tool_name;
                state.lastConfidence = action.payload.confidence;
            })
            .addCase(sendAgentMessage.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message;

                state.messages.push({
                    role: "assistant",
                    content:
                        "I could not process that request. Please confirm the backend is running and try again.",
                    toolName: "error",
                });
            });
    },
});

export const { addUserMessage, clearChat } = chatSlice.actions;

export default chatSlice.reducer;