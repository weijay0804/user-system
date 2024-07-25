import {
    Typography,
    Box,
} from '@mui/material';
import PropTypes from 'prop-types';

function ReminderText(props) {

    return (
        <Box
            sx={{
                marginTop: 8,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            }}
        >
            <Typography component="h1" variant="h5">
                {props.text}
            </Typography>
        </Box>
    );

}

ReminderText.propTypes = {
    text: PropTypes.string.isRequired
}

export default ReminderText;