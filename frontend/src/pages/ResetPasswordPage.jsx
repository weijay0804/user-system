import { useState, useEffect } from 'react';

import {
    Button,
    TextField,
    Typography,
    Container,
    Box,
} from '@mui/material';

import FadeAlert from '../components/FadeAlert';
import { authApi } from '../api/authApi';

function ResetPasswordPage() {

    const [password, setPassword] = useState("")
    const [password2, setPassword2] = useState("")
    const [isAlertShow, setIsAlertShow] = useState(false)
    const [msg, setMsg] = useState("");
    const [alertSeverity, setAlertSeverity] = useState("success");
    const [passwordError, setPasswordError] = useState("");
    const [disableSubmit, setDisableSubmit] = useState(true);

    const currentUrl = window.location.href;

    const url = new URL(currentUrl);

    const token = url.searchParams.get('token');
    const email = url.searchParams.get('email');

    useEffect(() => {
        if (password.length === 0 || password2.length === 0) {
            setDisableSubmit(true)

        } else if (password2 && password !== password2) {
            setPasswordError("密碼必須相同")
            setDisableSubmit(true)

        } else {
            setPasswordError("")
            setDisableSubmit(false)
        }
    }, [password, password2])

    function handelSubmit(e) {

        e.preventDefault();

        const payload = {
            "token": token,
            "email": email,
            "new_password": password
        }

        authApi.resetPassword(payload).then(() => {

            setAlertSeverity("success");
            setMsg("重設密碼成功，將跳轉至登入畫面");
            showAlert();
            setTimeout(() => {
                window.location.href = "/auth";
            }, 5000)
        }).catch((error) => {

            console.error(error)

            setAlertSeverity("error");
            setMsg("發生錯誤");
            showAlert();
        })


    }

    function showAlert() {
        setIsAlertShow(true);
        setTimeout(() => {
            setIsAlertShow(false)
        }, 6000)
    }


    return (
        <Container component="main" maxWidth="xs">
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Typography component="h1" variant="h5" textAlign="center" gutterBottom>
                    重新設定密碼
                </Typography>
            </Box>
            <Box component="form" noValidate sx={{ mt: 1 }} onSubmit={handelSubmit}>
                <TextField
                    margin='normal'
                    required
                    fullWidth
                    name="password"
                    label="密碼"
                    type="password"
                    id="password"
                    autoComplete="current-password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                />
                <TextField
                    margin='normal'
                    required
                    fullWidth
                    name="password2"
                    label="再輸入一次密碼"
                    type="password"
                    id="password2"
                    autoComplete="current-password"
                    value={password2}
                    onChange={e => setPassword2(e.target.value)}
                    error={!!passwordError}
                    helperText={passwordError}
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3, mb: 2 }}
                    disabled={disableSubmit}
                >
                    登入
                </Button>
            </Box>
            {isAlertShow && <FadeAlert text={msg} severity={alertSeverity} fadeTime={6000} />}
        </Container>
    )

}

export default ResetPasswordPage;