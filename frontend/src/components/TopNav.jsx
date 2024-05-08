import { useAuth, useUser } from "../utils/hooks.js";
import { NavLink } from "react-router-dom";

function NavItem({ to, name, right }) {
    const className = [
      "border-purple-400",
      "py-2 px-4",
      "hover:bg-slate-800",
      right ? "border-l-2" : "border-r-2"
    ].join(" ")
  
    const getClassName = ({ isActive }) => (
      isActive ? className + " bg-slate-800" : className
    );
  
    return (
      <NavLink to={to} className={getClassName}>
        {name}
      </NavLink>
    );
  }


function LoggedInNav(){
    const user = useUser();

    return(
        <>
            <NavItem to="/" name ="Pony Express"/>
            <NavItem to="/profile" name = {user?.username} />
        </>
    );
}


function LoggedOutNav(){
    return(
        <>
            <NavItem to="/" name ="Pony Express"/>
            <NavItem to="/login" name = "login" />
        </>
    );
}


function TopNav() {
    const { isLoggedIn } = useAuth();
  
    return (
      <nav className="flex flex-row border-b-4 border-purple-400">
        {isLoggedIn ?
          <LoggedInNav /> :
          <LoggedOutNav />
        }
      </nav>
    );
  }
  
  export default TopNav;
  