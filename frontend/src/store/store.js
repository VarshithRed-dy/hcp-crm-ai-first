import { configureStore } from "@reduxjs/toolkit";
import crmReducer from "../features/crmSlice";
import chatReducer from "../features/chatSlice";

export const store = configureStore({
    reducer: {
        crm: crmReducer,
        chat: chatReducer,
    },
});