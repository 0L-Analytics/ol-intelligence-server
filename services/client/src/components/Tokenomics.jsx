import React, { Component } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

import "./Tokenomics.css";


ChartJS.register(ArcElement, Tooltip, Legend);


class Tokenomics extends Component {
    constructor(props) {
        super(props);
        this.state = {
            balancesByType: [],
        };
    }

    componentDidMount() {
        this.getBalanceByType();
    }

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
            balancesByType: res.data['data'],
        });
        })
        .catch((error) => {
        console.log(error);
        });
    }
    render() {
        const labels = [];
        const balances = [];
        this.state.balancesByType
            .forEach(element => {
                labels.push(element['account_type']);
                balances.push(element['balance'])
        })

        const data = {
            labels: labels,
            datasets: [
              {
                label: "bladiebla",
                data: balances,
                backgroundColor: [
                  "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(255, 206, 86, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(255, 159, 64, 0.2)"
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(255, 206, 86, 1)",
                  "rgba(75, 192, 192, 1)",
                  "rgba(153, 102, 255, 1)",
                  "rgba(255, 159, 64, 1)"
                ],
                borderWidth: 1,
                polyline: {
                  color: "gray",
                  labelColor: "gray",
                  formatter: (value) => `formatted ${value}`
                }
              }
            ]
        };

        return (
          <div className="columns tokenomics">
            <div className="main column mx-2 mb-4">
              <div className="main-section mb-4 bb">
                <h1 className="is-size-4 has-text-centered mb-3">
                  Distribution
                </h1>
                <div className="columns mb-3">
                  <div className="column level-item has-text-centered">
                    <p className="heading">
                      nr of wallets
                    </p>
                    <p className="title">
                      426
                    </p>
                  </div>
                  <div className="column level-item has-text-centered">
                    <p className="heading">
                      total supply
                    </p>
                    <p className="title">
                      426
                    </p>
                  </div>
                  <div className="column level-item has-text-centered">
                    <p className="heading">
                      tokens locked
                    </p>
                    <p className="title">
                      426
                    </p>
                  </div>
                </div>
                <div className="columns">
                  <div className="column">
                    <h1 className="heading has-text-centered mb-1">
                      Allocation by wallet type
                    </h1>
                    <Pie data={data} />
                  </div>
                  <div className="column">
                    <h1 className="heading has-text-centered mb-1">
                      Wallet count by wallet type
                    </h1>
                    <Pie data={data} />
                  </div>
                </div>
                {/* main-section */}
              </div>
              <div className="main-section">
                <h1 className="is-size-4 has-text-centered mb-3">
                  Validators
                </h1>
                <div className="columns mb-3">
                  <div className="column level-item has-text-centered">
                    <p className="heading">
                      Active validators
                    </p>
                    <p className="title">
                      426
                    </p>
                  </div>
                  <div className="column level-item has-text-centered">
                    <p className="heading">
                      Validators
                    </p>
                    <p className="title">
                      426
                    </p>
                  </div>
                  <div className="column level-item has-text-centered">
                    <p className="heading">
                      Validators
                    </p>
                    <p className="title">
                      426
                    </p>
                  </div>
                  <div className="column level-item has-text-centered">
                    <p className="heading">
                      Validators
                    </p>
                    <p className="title">
                      426
                    </p>
                  </div>
                </div>
                {/* main-section */}
              </div>
              {/* main */}
            </div>
            {/* tokenomics */}
          </div>
        );   }
}
  
export default Tokenomics;
