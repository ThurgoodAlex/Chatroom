import { useEffect, useState } from "react";
import { useAuth, useUser } from "../utils/hooks.js";
import Button from "../assets/Button";
import FormInput from "../assets/FormInput";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function Profile() {
    const { logout } = useAuth()
    const user = useUser()
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [readOnly, setReadOnly] = useState(true);

    const reset = () => {
        if (user) {
            setUsername(user.username);
            setEmail(user.email);
          }
    }

    const logoutAndNav = () => {
        logout()
        navigate("/login")
    };

    useEffect(reset, [user]);

    return (
        <div className="max-w-96 mx-auto px-4 py-8">
          <h2 className="text-2xl font-bold py-2">
            details
          </h2>
            <p><strong>Username</strong></p> 
            <p>{username}</p>

            <p><strong>Email</strong></p> 
            <p>{email}</p>
          
            <Button onClick={logoutAndNav}>
              logout
            </Button>

            <div className="mt-4">
              <Link to="/register">Click Here to Create an Account</Link>
            </div>
        </div>
      );
    }
    
    export default Profile;