import React, { Component } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

import DataPie from "./DataPie";
import "./Tokenomics.css";

class TokenomicsMetricsBar extends Component {
  constructor(props) {
    super(props);
    this.state = {
        balancesByType: [],
    };
  };

  componentDidMount() {
    this.getBalanceByType();
  };

  getBalanceByType(event) {
    const options = {
      url: `${process.env.REACT_APP_API_SERVICE_URL}/oldata/balancebytype`,
      method: "get",
      headers: {
        "Content-Type": "application/json",
    },
  };
  return axios(options)
    .then((res) => {
      this.setState({
          balancesByType: res.data,
      });
      })
      .catch((error) => {
      console.log(error);
      });
  };
  render() {
    return (
      <div className="container topBar box">
        <div className="columns">
          <div className="column pieBox">
            <DataPie 
              dataSet={this.state.balancesByType}
              labelElem='account_type'
              valueElem='balance'
              divider='1000000'
              suffix=' M'
            />
          </div>
          <div className="column pieBox">
            <DataPie 
              dataSet={this.state.balancesByType}
              labelElem='account_type'
              valueElem='count'
            />
          </div>
          <div className="column pieBox">
            <DataPie 
              dataSet={this.state.balancesByType}
              labelElem='account_type'
              valueElem='balance'
              divider='1000000'
              suffix=' M'
            />
          </div>
          <div className="column pieBox">
            <DataPie 
              dataSet={this.state.balancesByType}
              labelElem='account_type'
              valueElem='count'
            />
          </div>
        </div>
      </div>
    );
  };
};
  
export default TokenomicsMetricsBar;
