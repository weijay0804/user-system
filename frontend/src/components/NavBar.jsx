import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

function NavBar() {

    const { isLogin, logout } = useAuth();

    return (
        <AppBar position="static" sx={{ width: '100vw', left: 0, borderBottom: '1px solid rgba(255, 255, 255, 0.3)' }}>
            <Toolbar sx={{ justifyContent: 'space-between', width: '100%', px: 2 }}>
                <Typography variant="h6" component="div">
                    User System
                </Typography>
                <Box>
                    <Button color="inherit" component={RouterLink} to="/">
                        首頁
                    </Button>
                    {isLogin &&
                        <>

                            <Button color='inherit' component={RouterLink} to="/me">
                                個人資料
                            </Button>
                            <Button color='inherit' component={RouterLink} to="/user/reset-password">
                                重設密碼
                            </Button>
                        </>

                    }
                    <Button color="inherit" component={RouterLink} to="/auth" onClick={isLogin ? logout : null}>
                        {isLogin ? '登出' : '登入/註冊'}
                    </Button>
                </Box>
            </Toolbar>
        </AppBar>
    );
}

export default NavBar;