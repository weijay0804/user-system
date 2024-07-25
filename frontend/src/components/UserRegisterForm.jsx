import { useState } from 'react';
import PropTypes from 'prop-types';
import {
    Button,
    TextField,
    Typography,
    Box,
    Snackbar,
} from '@mui/material';
import Alert from '../utils/Alert';
import { formatErrorMsg } from '../helper/responseHelper';
import { authApi } from '../api/authApi';

function UserRegisetrForm({ setIsRegistered, setIsLoginOn }) {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState('success');

    async function handelSubmit(e) {

        e.preventDefault();

        authApi.signUp({ email, name, password }).then(() => {

            setIsRegistered(true);

            setTimeout(() => {
                setIsRegistered(false);
                setIsLoginOn(true);
            }, 5000)

        }).catch((error) => {
            console.error('Registration failed:', error.response.data.detail);
            const msg = formatErrorMsg(error.response.data.detail);
            setSnackbarMessage('註冊失敗：' + (msg));
            setSnackbarSeverity('error');
            setOpenSnackbar(true);
        })
    }

    const handleCloseSnackbar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setOpenSnackbar(false);
    };

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
                    註冊
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
                        margin="normal"
                        required
                        fullWidth
                        id="name"
                        label="姓名"
                        name="name"
                        autoComplete="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
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
                        註冊
                    </Button>
                </Box>

            </Box>
            <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar}>
                <Alert onClose={handleCloseSnackbar} severity={snackbarSeverity} sx={{ width: '100%' }}>
                    {snackbarMessage}
                </Alert>
            </Snackbar>
        </>
    )
}

UserRegisetrForm.propTypes = {
    setIsRegistered: PropTypes.func.isRequired,
    setIsLoginOn: PropTypes.func.isRequired
}

export default UserRegisetrForm;