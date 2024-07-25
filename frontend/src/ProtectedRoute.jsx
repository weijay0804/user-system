import { Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';

import PropTypes from 'prop-types'

const ProtectedRoute = ({ children, requireAuth }) => {
    const { isLogin } = useAuth();

    if (requireAuth && !isLogin) {
        return <Navigate to="/auth" replace />;
    } else if (!requireAuth && isLogin) {
        return <Navigate to="/" replace />;
    }

    return children;
};

ProtectedRoute.propTypes = {
    children: PropTypes.node,
    requireAuth: PropTypes.bool
}

export default ProtectedRoute;