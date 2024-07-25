import { createContext, useState, useEffect } from 'react';
import PropTypes from 'prop-types';

import FadeAlert from '../components/FadeAlert';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

    const [isLogin, setIsLogin] = useState(checkIsLogin());
    const [isShowAlert, setIsShowAlert] = useState(false);
    const [msg, setMsg] = useState("");
    const [alertSeverity, setAlertSeverity] = useState("success");

    useEffect(() => {

        const handleStorageChange = () => {
            setIsLogin(checkIsLogin());
        };

        window.addEventListener('storage', handleStorageChange);

        return () => window.removeEventListener('storage', handleStorageChange);
    }, []);

    const logout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("access_token_expire");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("refresh_token_expire");
        setIsLogin(false);
        setIsShowAlert(true);
        setMsg("登出成功");
        setAlertSeverity("info");
    }

    return (
        <AuthContext.Provider value={{ isLogin, setIsLogin, logout }}>
            {children}
            {isShowAlert && <FadeAlert severity={alertSeverity} text={msg} fadeTime={3000} />}
        </AuthContext.Provider >
    )
}

const checkIsLogin = () => {

    const token = localStorage.getItem("access_token");
    const expire = localStorage.getItem("access_token_expire");

    if (token && expire) {
        const expireDate = new Date(expire);

        if (expireDate > new Date()) {
            return true;
        }
    }

    return false;
}

AuthProvider.propTypes = {
    children: PropTypes.node
}

export default AuthContext;