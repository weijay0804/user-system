import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Box, CssBaseline } from '@mui/material';
import NavBar from './components/NavBar';

import ProtectedRoute from './ProtectedRoute';
import {
  HomePage,
  AuthPage,
  UserMePage,
  ResetPasswordPage,
  ForgetPasswordPage,
  VerifiedAccountPage,
  UserResetPasswordPage,
  VerifiedAccountReminderPage
} from './pages';

import authRouters from './routes/auth';
import userRouters from './routes/user';

const routes = [
  { path: "/", element: <HomePage />, requireAuth: null },
  { path: authRouters.loginUrl, element: <AuthPage />, requireAuth: false },
  { path: authRouters.verifyAccountUrl, element: <VerifiedAccountPage />, requireAuth: false },
  { path: authRouters.forgotPasswordUrl, element: <ForgetPasswordPage />, requireAuth: false },
  { path: authRouters.resetPasswordUrl, element: <ResetPasswordPage />, requireAuth: false },
  { path: authRouters.accountVerifyReminderUrl, element: <VerifiedAccountReminderPage />, requireAuth: false },
  { path: userRouters.userMeUrl, element: <UserMePage />, requireAuth: true },
  { path: userRouters.userResetPasswordUrl, element: <UserResetPasswordPage />, requireAuth: true },
]

function App() {

  return (
    <Router>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', width: '100vw', overflow: 'hidden' }}>
        <NavBar />
        <Box component="main" sx={{ flexGrow: 1, width: '100%', p: 3 }}>
          <Routes>

            {routes.map(({ path, element, requireAuth }) => (
              <Route
                key={path}
                path={path}
                element={
                  requireAuth !== null ? (
                    <ProtectedRoute requireAuth={requireAuth}>
                      {element}
                    </ProtectedRoute>
                  ) : (
                    element
                  )
                }
              />
            ))}

          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;