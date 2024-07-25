const authRouters = {

    // 登入、註冊
    "loginUrl": "/auth",

    // 用戶忘記密碼
    "forgotPasswordUrl": "/auth/forgot",

    // 認證帳戶，通過 email 跳轉到這
    "verifyAccountUrl": "/auth/verify",

    // 用戶重設密碼，通過 email 跳轉到這
    "resetPasswordUrl": "/auth/password/reset",

    // 提醒用戶要先驗證帳號
    "accountVerifyReminderUrl": "/auth/verify/reminder",
}

export default authRouters;