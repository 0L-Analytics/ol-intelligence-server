import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

import "./NavBar.css";


const titleStyle = {
  fontWeight: "bold",
};

const NavBar = (props) => {
  let menu = (
    <div className="navbar-menu">
      <div className="navbar-start">
        <Link to="/about" className="navbar-item" data-testid="nav-about">
          About
        </Link>
        <Link to="/tokenomics" className="navbar-item" data-testid="nav-tokenomics">
          Tokenomics
        </Link>
      </div>
      <div className="navbar-end">
        <Link to="/register" className="navbar-item" data-testid="nav-register">
          Register
        </Link>
        <Link to="/login" className="navbar-item" data-testid="nav-login">
          Log In
        </Link>
      </div>
    </div>
  );
  if (props.isAuthenticated()) {
    menu = (
      <div className="navbar-menu">
        <div className="navbar-start">
          <Link to="/about" className="navbar-item" data-testid="nav-about">
            About
          </Link>
          <Link to="/tokenomics" className="navbar-item" data-testid="nav-tokenomics">
            Tokenomics
          </Link>
          <Link to="/status" className="navbar-item" data-testid="nav-status">
            User Status
          </Link>
        </div>
        <div className="navbar-end">
          <span
            // eslint-disable-next-line react/jsx-handler-names
            onClick={props.logoutUser}
            className="navbar-item"
            data-testid="nav-logout"
          >
            Log Out
          </span>
        </div>
      </div>
    );
  }
  return (
    <nav
      className="navbar is-dark"
      role="navigation"
      aria-label="main navigation"
    >
      <section className="container">
        <div className="navbar-brand">

          <Link to="/" className="navbar-item nav-title" style={titleStyle}>
            <img src="/0l-logo.png" alt="Logo" />
          </Link>
          
          <span
            className="nav-toggle navbar-burger"
            onClick={() => {
              let toggle = document.querySelector(".nav-toggle");
              let menu = document.querySelector(".navbar-menu");
              toggle.classList.toggle("is-active");
              menu.classList.toggle("is-active");
            }}
          >
            <span />
            <span />
            <span />
          </span>
        </div>
        {menu}
      </section>
    </nav>
  );
};

NavBar.propTypes = {
  logoutUser: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired,
};

export default NavBar;
