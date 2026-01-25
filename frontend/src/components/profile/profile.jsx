import { useAuth } from '../../contexts/UserLoginContext.jsx';
import './profile.css';

function profile(){
    const { currentUser, logOut } = useAuth();
    return (
        <div className="profile-container">
            <h1>Hello {currentUser?.displayName}</h1>
        </div>
    )
}

export default profile;