import { useState, useEffect } from 'react';

import PropTypes from 'prop-types';

import { Alert, Fade } from '@mui/material';
import { styled } from '@mui/system';

const StyledAlert = styled(Alert)(({ theme }) => ({
    position: 'fixed',
    top: theme.spacing(10),
    left: '50%',
    transform: 'translateX(-50%)',
    minWidth: '200px',
}));

function FadeAlert(props) {

    const [show, setShow] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setShow(false);
        }, props.fadeTime);

        return () => clearTimeout(timer);
    }, [props.fadeTime]);

    return (
        <Fade in={show}>
            <StyledAlert severity={props.severity}>
                {props.text}
            </StyledAlert>
        </Fade>
    )

}

FadeAlert.propTypes = {
    text: PropTypes.string.isRequired,
    severity: PropTypes.string.isRequired,
    fadeTime: PropTypes.number.isRequired
}

export default FadeAlert;