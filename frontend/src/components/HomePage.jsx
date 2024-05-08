import { Link, useNavigate } from "react-router-dom";

function HomePage(){
    return(
    <div className="flex flex-col items-center justify-center flex-grow">
        <p>
            Welcome to Pony Express! This is an application that allows you to post messages and create chats
        </p>
        <div className="pt-2.5 font-bold">
            <Link to="/login">
                Get Started
            </Link>
        </div>
    </div>
    );
}

export default HomePage