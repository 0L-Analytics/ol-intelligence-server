import React, { Component } from "react";
import axios from "axios";
import { Route, Routes } from "react-router-dom";
import Modal from "react-modal";

import About from "./components/About";
import AddUser from "./components/AddUser";
import LoginForm from "./components/LoginForm";
import Message from "./components/Message";
import NavBar from "./components/NavBar";
import RegisterForm from "./components/RegisterForm";
import UsersList from "./components/UsersList";
import UserStatus from "./components/UserStatus";
import AccountBalanceList from "./components/AccountBalanceList";
import Tokenomics from "./components/Tokenomics";

// import PiePetit from "./components/Pie";
// import { Pie } from 'react-chartjs-2';


const modalStyles = {
  content: {
    top: "0",
    left: "0",
    right: "0",
    bottom: "0",
    border: 0,
    background: "transparent",
  },
};

Modal.setAppElement(document.getElementById("root"));

const state = {
  labels: ['January', 'February', 'March',
           'April', 'May'],
  datasets: [
    {
      label: 'Rainfall',
      backgroundColor: [
        '#B21F00',
        '#C9DE00',
        '#2FDE00',
        '#00A6B4',
        '#6800B4'
      ],
      hoverBackgroundColor: [
      '#501800',
      '#4B5000',
      '#175000',
      '#003350',
      '#35014F'
      ],
      data: [65, 59, 80, 81, 56]
    }
  ]
}

class App extends Component {
  constructor() {
    super();

    this.state = {
      users: [],
      accountBalances: [],
      accessToken: null,
      messageType: null,
      messageText: null,
      showModal: false,
    };
  }

  componentDidMount() {
    this.getUsers();
    this.getAccountBalances();
  }

  addUser = (data) => {
    axios
      .post(`${process.env.REACT_APP_API_SERVICE_URL}/users`, data)
      .then((res) => {
        this.getUsers();
        this.setState({ username: "", email: "" });
        this.handleCloseModal();
        this.createMessage("success", "User added.");
      })
      .catch((err) => {
        console.log(err);
        this.handleCloseModal();
        this.createMessage("danger", "That user already exists.");
      });
  };

  createMessage = (type, text) => {
    this.setState({
      messageType: type,
      messageText: text,
    });
    setTimeout(() => {
      this.removeMessage();
    }, 3000);
  };

  getUsers = () => {
    axios
      .get(`${process.env.REACT_APP_API_SERVICE_URL}/users`)
      .then((res) => {
        this.setState({ users: res.data });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  getAccountBalances = () => {
    axios
      .get(`${process.env.REACT_APP_API_SERVICE_URL}/oldata/accountbalances`)
      .then((res) => {
        this.setState({ accountBalances: res.data });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  handleCloseModal = () => {
    this.setState({ showModal: false });
  };

  handleLoginFormSubmit = (data) => {
    const url = `${process.env.REACT_APP_API_SERVICE_URL}/auth/login`;
    axios
      .post(url, data)
      .then((res) => {
        this.setState({ accessToken: res.data.access_token });
        this.getUsers();
        window.localStorage.setItem("refreshToken", res.data.refresh_token);
        this.createMessage("success", "You have logged in successfully.");
      })
      .catch((err) => {
        console.log(err);
        this.createMessage("danger", "Incorrect email and/or password.");
      });
  };

  handleOpenModal = () => {
    this.setState({ showModal: true });
  };

  handleRegisterFormSubmit = (data) => {
    const url = `${process.env.REACT_APP_API_SERVICE_URL}/auth/register`;
    axios
      .post(url, data)
      .then((res) => {
        console.log(res.data);
        this.createMessage("success", "You have registered successfully.");
      })
      .catch((err) => {
        console.log(err);
        this.createMessage("danger", "That user already exists.");
      });
  };

  isAuthenticated = () => {
    if (this.state.accessToken || this.validRefresh()) {
      return true;
    }
    return false;
  };

  logoutUser = () => {
    window.localStorage.removeItem("refreshToken");
    this.setState({ accessToken: null });
    this.createMessage("success", "You have logged out.");
  };

  removeMessage = () => {
    this.setState({
      messageType: null,
      messageText: null,
    });
  };

  removeUser = (user_id) => {
    axios
      .delete(`${process.env.REACT_APP_API_SERVICE_URL}/users/${user_id}`)
      .then((res) => {
        this.getUsers();
        this.createMessage("success", "User removed.");
      })
      .catch((err) => {
        console.log(err);
        this.createMessage("danger", "Something went wrong.");
      });
  };

  validRefresh = () => {
    const token = window.localStorage.getItem("refreshToken");
    if (token) {
      axios
        .post(`${process.env.REACT_APP_API_SERVICE_URL}/auth/refresh`, {
          refresh_token: token,
        })
        .then((res) => {
          this.setState({ accessToken: res.data.access_token });
          this.getUsers();
          this.getAccountBalances();
          window.localStorage.setItem("refreshToken", res.data.refresh_token);
          return true;
        })
        .catch((err) => {
          return false;
        });
    }
    return false;
  };

  render() {
    return (
      <div>

        <NavBar
          logoutUser={this.logoutUser}
          isAuthenticated={this.isAuthenticated}
        />

        <section className="section">
          <div className="container">

            {this.state.messageType && this.state.messageText && (
              <Message
                messageType={this.state.messageType}
                messageText={this.state.messageText}
                removeMessage={this.removeMessage}
              />
            )}

            <div className="container is-max-desktop">
              
                <Routes>

                  <Route
                    exact
                    path="/"
                    element={
                      <div>
                        <h1 className="title is-1">Community wallet account balances</h1>
                        <hr />
                        <br />

                        <AccountBalanceList
                          accountBalances={this.state.accountBalances}
                        />

                      </div>
                    }
                  />

                  <Route exact path="/about" element={<About />} />

                  <Route exact path="/tokenomics" element={<Tokenomics />} />

                  <Route
                    exact
                    path="/register"
                    element={
                      <RegisterForm
                        // eslint-disable-next-line react/jsx-handler-names
                        handleRegisterFormSubmit={this.handleRegisterFormSubmit}
                        isAuthenticated={this.isAuthenticated}
                      />
                    }
                  />

                  <Route
                    exact
                    path="/login"
                    element={
                      <LoginForm
                        // eslint-disable-next-line react/jsx-handler-names
                        handleLoginFormSubmit={this.handleLoginFormSubmit}
                        isAuthenticated={this.isAuthenticated}
                      />
                    }
                  />
                  <Route
                    exact
                    path="/status"
                    element={
                      <UserStatus
                        accessToken={this.state.accessToken}
                        isAuthenticated={this.isAuthenticated}
                      />
                    }
                  />
                </Routes>
              
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default App;
