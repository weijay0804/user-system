import axios from "axios";

const baseURL = "http://127.0.0.1:8000";
const axiosInstance = axios.create({ baseURL })

const refreshToken = async () => {
    const rToken = localStorage.getItem("refresh_token");
    const rTokenExpire = localStorage.getItem("refresh_token_expire");

    if (rToken && rTokenExpire) {

        const expireDate = new Date(rTokenExpire);

        if (expireDate > new Date()) {

            try {
                const response = await axiosInstance.post("/auth/token/refresh", null, {
                    headers: {
                        'refresh-token': rToken
                    }
                })

                const access_token_data = response.data.access_token;
                const refresh_token_data = response.data.refresh_token;

                localStorage.setItem("access_token", access_token_data.token);
                localStorage.setItem("access_token_expire", access_token_data.expires_at);
                localStorage.setItem("refresh_token", refresh_token_data.token);
                localStorage.setItem("refresh_token_expire", refresh_token_data.expires_at);

                return access_token_data.token;
            } catch (error) {
                return null;
            }
        } else {

            localStorage.removeItem("access_token");
            localStorage.removeItem("access_token_expire");
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("refresh_token_expire");
            window.dispatchEvent(new Event('storage'));

            // TODO 這邊之後看可不可以改成好看一點到的樣式
            window.alert("登入逾時，請重新登入")

            return null
        }
    }

    return null;
}

axiosInstance.interceptors.request.use(
    async config => {

        if (config.authRequired) {

            let token = localStorage.getItem("access_token");

            const expire = localStorage.getItem("access_token_expire");

            if (token && expire) {

                const expireDate = new Date(expire)

                if (expireDate <= new Date()) {

                    token = await refreshToken()
                }
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`
                }
            }
        }

        return config
    }, (error) => {

        return Promise.reject(error)
    }
)

export const apiHelper = axiosInstance;