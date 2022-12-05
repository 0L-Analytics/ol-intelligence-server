import React from "react";
import { NavLink } from "react-router-dom";
import PropTypes from "prop-types";

const SideBar = (props) => {
  let menu = (
    <nav className="menu">
        <p className="menu-label">
            General
        </p>
        <ul className="menu-list">
            <li>
                <NavLink 
                  to="/"
                  className={() => (location.pathname=='/') ? "is-active" : ""}
                >
                    Home
                </NavLink>
            </li>
            <li>
                <NavLink 
                  to="/tokenomics"
                  className={() => (location.pathname=='/tokenomics') ? "is-active" : ""}
                >
                    Tokenomics
                </NavLink>
            </li>
        </ul>
        <p className="menu-label">
            Transactions
        </p>
        <ul className="menu-list">
            <li><a>Payments</a></li>
            <li><a>Balance</a></li>
            <li>
                <NavLink 
                  to="/about"
                  className={() => (location.pathname=='/about') ? "is-active" : ""}
                >
                    About
                </NavLink>
            </li>
        </ul>
    </nav>
  );

  if (props.isAuthenticated()) {
    menu = (
        <nav className="menu">
            <p className="menu-label">
                General
            </p>
            <ul className="menu-list">
                <li>
                    <NavLink 
                      to="/"
                      className={() => (location.pathname=='/') ? "is-active" : ""}
                    >
                        Home
                    </NavLink>
                </li>
                <li>
                    <NavLink 
                      to="/tokenomics"
                      className={() => (location.pathname=='/tokenomics') ? "is-active" : ""}
                    >
                        Tokenomics
                    </NavLink>
                </li>
                <li><a>Chain status</a></li>
            </ul>
            <p className="menu-label">
                Transactions
            </p>
            <ul className="menu-list">
                <li><a>Payments</a></li>
                <li><a>Balance</a></li>
                <li>
                    <NavLink 
                      to="/about"
                      className={() => (location.pathname=='/about') ? "is-active" : ""}
                    >
                        About
                    </NavLink>
                </li>
            </ul>
        </nav>
    );
  }
  return (
    <aside className="column is-2">
        {menu}
    </aside>
  );
};

SideBar.propTypes = {
  isAuthenticated: PropTypes.func.isRequired,
};

export default SideBar;
