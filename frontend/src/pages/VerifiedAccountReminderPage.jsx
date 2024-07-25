import { useState, useEffect } from 'react';

import {
    Container,
    Typography,
    TextField,
    Button,
    Box,
} from '@mui/material';

import FadeAlert from '../components/FadeAlert';
import { authApi } from '../api/authApi';
import { useNavigate } from 'react-router-dom';

function VerifiedAccountReminderPage() {

    const [email, setEmail] = useState("")
    const [isBtnDisabled, setIsBtnDisabled] = useState(true)
    const [msg, setMsg] = useState("")
    const [alertSeverity, setAlertSeverity] = useState("success")
    const [isShowAlert, setIsShowAlert] = useState(false)
    const navigate = useNavigate();

    useEffect(() => {

        if (!email || email.trim().length == 0) {

            setIsBtnDisabled(true)
        } else {
            setIsBtnDisabled(false)
        }
    }, [email])

    function showAlert() {
        setIsShowAlert(true);
        setTimeout(() => {
            setIsShowAlert(false)
        }, 6000)
    }

    function handelSubmit(e) {

        e.preventDefault();

        authApi.resendVerifyEmail({ email }).then(() => {

            setAlertSeverity("success")
            setMsg("驗證信已重新發送至您的信箱")
            showAlert()

            setTimeout(() => {
                navigate("/auth")
            }, 2000)
        }).catch((error) => {

            if (error.response.data.detail === "Email is not exists.") {

                setAlertSeverity("error")
                setMsg("電子郵件不存在")
                showAlert()
                return;
            }

            if (error.response.data.detail === "Your account is already active.") {

                setAlertSeverity("warning")
                setMsg("您的帳戶已驗證")
                showAlert()
                return
            }

            console.error(error)
            setAlertSeverity("error")
            setMsg("發生錯誤")
            showAlert()
        })

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
                <Typography component="h1" variant="h5" textAlign='center'>
                    請先至您的信箱中驗證帳戶
                </Typography>
                <Typography textAlign='center'>
                    如沒有收到驗證信，請輸入您的 email 並重新發送
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
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2 }}
                        disabled={isBtnDisabled}
                    >
                        送出
                    </Button>
                </Box>
            </Box>
            {isShowAlert && <FadeAlert text={msg} severity={alertSeverity} fadeTime={6000} />}
        </Container>
    )

}

export default VerifiedAccountReminderPage;