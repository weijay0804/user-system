export function formatErrorMsg(message) {

    switch (message) {
        case 'Email is already exists.':
            return '電子郵件或用戶名已經存在';

        case 'Incorrect email or password.':
            return "錯誤的密碼或電子郵件";

        case 'Your account is not active.':
            return "您的帳號尚未啟用";

        case 'Your account is not verified.':
            return "您的帳號尚未驗證，請至您的信箱進行驗證";

        default:
            return '發生未知的錯誤';
    }
}