import { useState } from 'react';
import {
    Container,
    Button,
    TextField,
    Typography,
    Box,
} from '@mui/material';
import { authApi } from '../api/authApi';
import FadeAlert from '../components/FadeAlert';
import { useNavigate } from 'react-router-dom';

function ForgetPasswordPage() {

    const [email, setEmail] = useState("")
    const [isShowAlert, setIsShowAlert] = useState(false)
    const [msg, setMsg] = useState()
    const [alertSeverity, setAlertSeverity] = useState("success")
    const navigate = useNavigate();

    function showAlert() {

        setIsShowAlert(true);

        setTimeout(() => {
            setIsShowAlert(false)
        }, 6000)
    }

    async function handelSubmit(e) {
        e.preventDefault();

        authApi.forgotPassword({ email }).then(() => {

            setAlertSeverity("success")
            setMsg("重新設定密碼的電子郵件已發送至您的信箱")

            showAlert()

            setTimeout(() => {
                navigate("/auth")
            }, 6000)

        }).catch((error) => {
            if (error.response.data.detail === 'Your account is not verified.' || error.response.data.detail === 'Your account is not active.') {
                setMsg("請先驗證帳戶")
                setAlertSeverity("info")
                showAlert()

                return;
            }

            if (error.response.data.detail === "Email is not exists.") {
                setMsg("電子郵件不存在")
                setAlertSeverity("error")
                showAlert()
                return
            }

            setMsg("發生錯誤")
            setAlertSeverity("error")
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
                <Typography component="h1" variant="h5" textAlign="center" gutterBottom>
                    發送重設密碼電子郵件
                </Typography>
            </Box>
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
                >
                    登入
                </Button>
            </Box>
            {isShowAlert && <FadeAlert text={msg} severity={alertSeverity} fadeTime={6000} />}
        </Container>
    )
}

export default ForgetPasswordPage;