import { apiHelper } from "./apiHelper";

export const authApi = {

    login: async (data) => {

        return await apiHelper.postForm("/auth/login", data)
    },

    signUp: async (data) => {
        return await apiHelper.post("/users", data)
    },

    accountVerify: async (data) => {

        return await apiHelper.post("/auth/verifiy", data)
    },

    forgotPassword: async (data) => {
        return await apiHelper.post("/auth/forgot-password", data)
    },

    resetPassword: async (data) => {
        return await apiHelper.put("auth/forgot-password/reset", data)
    },

    resendVerifyEmail: async (data) => {
        return await apiHelper.post("auth/verifiy/resend", data)
    }

}