import { useEffect, useState } from 'react';

import { userApi } from '../api/userApi';
import ReminderText from '../components/ReminderText';

function UserMePage() {

    const [msg, setMsg] = useState("")

    useEffect(() => {

        userApi.fetchUser().then((res) => {

            const username = res.data.name

            setMsg(`你好: ${username}`)

        }).catch((error) => {
            if (error.response.status === 401) {
                setMsg("請先登入")
            }
        })

    }, [])

    return (
        <div>
            <ReminderText text={msg} />
        </div>
    )


}

export default UserMePage;