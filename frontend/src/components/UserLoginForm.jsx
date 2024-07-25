import { useState } from 'react';
import {
    Button,
    TextField,
    Typography,
    Box,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

import { formatErrorMsg } from '../helper/responseHelper';
import { authApi } from '../api/authApi';
import FadeAlert from './FadeAlert';

function UserLoginForm() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState('success');
    const [isAlertShow, setIsAlertShow] = useState(false);
    const navigate = useNavigate();

    function showAlert() {
        setIsAlertShow(true);
        setTimeout(() => {
            setIsAlertShow(false)
        }, 6000)
    }

    async function handelSubmit(e) {

        e.preventDefault();

        authApi.login({ username: email, password: password }).then((res) => {

            const access_token_data = res.data.access_token;
            const { token, expires_at } = access_token_data;

            localStorage.setItem("access_token", token);
            localStorage.setItem("access_token_expire", expires_at);

            const refresh_token_data = res.data.refresh_token;

            localStorage.setItem("refresh_token", refresh_token_data.token);
            localStorage.setItem("refresh_token_expire", refresh_token_data.expires_at);

            window.dispatchEvent(new Event('storage'));


            setSnackbarMessage('登入成功');
            setSnackbarSeverity('success');
            showAlert()

            setTimeout(() => {
                navigate("/");
            }, 2000)

        }).catch((error) => {
            if (error.response.data.detail === 'Your account is not verified.' || error.response.data.detail === 'Your account is not active.') {

                setSnackbarMessage('請先驗證您的帳戶');
                setSnackbarSeverity('warning');
                showAlert()

                setTimeout(() => {

                    navigate("/auth/verifiy/reminder");
                }, 1500)

                return
            }

            const msg = formatErrorMsg(error.response.data.detail);

            setSnackbarMessage('登入失敗：' + (msg));
            setSnackbarSeverity('error');
            showAlert()

        })
    }



    return (
        <>
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Typography component="h1" variant='h5'>
                    登入
                </Typography>
                <Box component="form" noValidate sx={{ mt: 1 }} onSubmit={handelSubmit}>
                    <TextField
                        margin='normal'
                        required
                        fullWidth
                        id="email"
                        label="電子郵件"
                        name="email"
                        autoComplete='email'
                        autoFocus
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    />
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
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}
                    >
                        登入
                    </Button>
                </Box>
            </Box>
            {isAlertShow && <FadeAlert text={snackbarMessage} severity={snackbarSeverity} fadeTime={6000} />}
        </>
    )
}

export default UserLoginForm;