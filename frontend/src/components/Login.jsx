import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useApiWithoutToken, useAuth } from "../utils/hooks.js";
import Button from "../assets/Button";
import FormInput from "../assets/FormInput";

function Error({ message }){
    if (message === ""){
        return <></>
    }
    return(
        <div className="text-red-300 text-sx">
            {message}
        </div>
    );
}


function RegistrationInfo(){
    return(
        <div className="pt-8 flex flex-col">
            <div className="text-xs">
                Do you need to register?
            </div>
            <Link to="/register">
                <Button className="mt-1 w-full">
                    Register!
                </Button>
            </Link>
        </div>
    );
}


function Login(){
    const[username, setUsername] = useState("")
    const[password, setPassword] = useState("")
    const[error, setError] = useState("")
    const navigate = useNavigate()

    const { login } = useAuth()
    const api = useApiWithoutToken()

    const disabled = username === "" || password === ""

    const onSubmit = (e) => {
        e.preventDefault()
        api.postForm("/auth/token", { username, password })
        .then((response) => {
          if (response.ok) {
            response.json().then(login).then(
              () => navigate("/")
            );
          } else if (response.status === 401) {
            response.json().then((data) => {
              setError(data.detail.error_description);
            });
          } else {
            setError("error logging in");
          }
        });
    }

    return (
        <div className="max-w-96 mx-auto py-8 px-4">
          <form onSubmit={onSubmit}>
            <FormInput type="text" name="username" setter={setUsername} />
            <FormInput type="password" name="password" setter={setPassword} />
            <Button className="w-full" type="submit" disabled={disabled}>
              login
            </Button>
            <Error message={error} />
          </form>
          <RegistrationInfo />
        </div>
      );
    }
    
    export default Login;