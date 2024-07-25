import { useEffect, useState } from 'react';

import {
    Typography,
    Box,
} from '@mui/material';


import { authApi } from '../api/authApi';
import { useNavigate } from 'react-router-dom';

function VerifiedAccountPage() {

    const navigate = useNavigate();

    // 取得 url 中的 token 和 email
    const currentUrl = window.location.href;

    const url = new URL(currentUrl);

    const token = url.searchParams.get('token');
    const email = url.searchParams.get('email');

    const [msg, setMsg] = useState("驗證帳戶...")

    // 發送 API 至後端，並驗證帳戶
    // 驗證成功後跳轉至登入畫面
    useEffect(() => {

        authApi.accountVerify({ token, email }).then(() => {

            setTimeout(() => {
                setMsg("驗證成功，將跳轉至登入畫面")

                setTimeout(() => {

                    navigate("/auth")
                }, 2000)

            }, 1000)

        }).catch((error) => {
            if (error.response.status === 400) {
                setTimeout(() => {

                    setMsg("驗證失敗，請重新驗證您的帳戶")

                }, 2000)
            } else {
                setTimeout(() => {

                    setMsg("發生未知的錯誤")

                }, 2000)
            }
            console.error(error)
        })

    }, [email, token, navigate])

    return (
        <Box
            sx={{
                marginTop: 8,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            }}
        >
            <Typography component="h1" variant="h5">
                {msg}
            </Typography>
        </Box>
    );

}

export default VerifiedAccountPage;