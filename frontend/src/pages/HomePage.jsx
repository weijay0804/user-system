import { Container, Typography, Box } from '@mui/material';

function HomePage() {
    return (
        <Container maxWidth={false}>
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Typography component="h1" variant="h3" gutterBottom>
                    User System
                </Typography>
                <Typography variant="h5" gutterBottom>
                    歡迎來到用戶系統
                </Typography>
            </Box>
        </Container>
    );
}

export default HomePage;