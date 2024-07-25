import { useState } from 'react';
import {
    Container,
    Grid,
    Link,
} from '@mui/material';

import UserLoginForm from '../components/UserLoginForm';
import UserRegisetrForm from '../components/UserRegisterForm';
import ReminderText from '../components/ReminderText';
import { useNavigate } from 'react-router-dom';

function AuthPage() {

    const [isLoginOn, setIsLoginOn] = useState(true);
    const [isRegistered, setIsRegistered] = useState(false);
    const navigate = useNavigate();

    return (
        <Container component="main" maxWidth="xs">
            {isRegistered ? <ReminderText text="註冊成功，請至您的電子郵件中進行認證，5 秒後自動跳轉..." /> : <>
                {isLoginOn ? <UserLoginForm /> : <UserRegisetrForm setIsRegistered={setIsRegistered} setIsLoginOn={setIsLoginOn} />}
                <Grid container justifyContent="space-between" alignItems="center">
                    <Grid item justifyItems="flex-start">
                        <Link href="#" variant="body2" onClick={() => navigate('/auth/forget')}>
                            忘記密碼？
                        </Link>
                    </Grid>
                    <Grid item>
                        <Link href="#" variant="body2" onClick={() => setIsLoginOn(!isLoginOn)}>
                            {isLoginOn ? '還沒有帳號？註冊' : '已有帳號？登入'}
                        </Link>
                    </Grid>
                </Grid>
            </>
            }
        </Container>
    )

}

export default AuthPage;