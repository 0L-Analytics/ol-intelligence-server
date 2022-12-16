import React, { Component } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import { 
  Chart as ChartJS, 
  ArcElement, 
  Tooltip, 
  Legend, 
  LineController,
  BarController,
  CategoryScale, 
  LinearScale, 
  PointElement,
  LineElement,
  BarElement
} from 'chart.js';

import { Line, Doughnut, Bar } from 'react-chartjs-2';

import "./Tokenomics.css";

ChartJS.register(
  ArcElement, 
  Tooltip, 
  Legend, 
  LineController,
  BarController,
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement,
  BarElement
);


function addDecSeperator(x) {
  var parts = x.toString().split(".");
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return parts.join(".");
}


class Tokenomics extends Component {
  constructor(props) {
    super(props);
    this.state = {
      balancesByType: [],
      supplyLiquidity: [],
      distributionChart1: [],
      distributionChart2: [],
      distributionChart3: [],
      total_balance: 0,
      total_addr_cnt: 0,
      top10_balance: 0,
      top100_balance: 0,
      top10_balance_nv: 0,
      top10_perc: 0.0,
      top100_perc: 0.0,
      top10_nv_perc: 0.0,
      sum_bal_ex_com: 0,
      sum_bal_ex_com_v: 0,
      addr_cnt_bal_gt1: 0,
      bal_community: 0,
      bal_slow: 0,
      bal_liquid: 0,
      cnt_community: 0,
      cnt_slow: 0,
      cnt_liquid: 0,
      active_set_cnt: 0, 
      validator_cnt: 0,
    };
  }

  componentDidMount() {
    this.getBalanceByType();
    this.getTokenomicsSingleMeasures();
    this.getSupplyLiquidity();
    this.getDistributionChart1();
    this.getDistributionChart2();
    this.getDistributionChart3();
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
          balancesByType: res.data,
      });
      })
      .catch((error) => {
      console.log(error);
      });
  };
  
  getDistributionChart3(event) {
    const options = {
      url: `${process.env.REACT_APP_API_SERVICE_URL}/oldata/top100distribution`,
      method: "get",
      headers: {
        "Content-Type": "application/json",
      },
    };
    return axios(options)
      .then((res) => {
        this.setState({
          distributionChart3: res.data,
        });
        })
        .catch((error) => {
          console.log(error);
        });
  };

  getDistributionChart2(event) {
    const options = {
      url: `${process.env.REACT_APP_API_SERVICE_URL}/oldata/topaddrbaldistribution`,
      method: "get",
      headers: {
        "Content-Type": "application/json",
      },
    };
    return axios(options)
      .then((res) => {
        this.setState({
          distributionChart2: res.data,
        });
        })
        .catch((error) => {
          console.log(error);
        });
  };

  getDistributionChart1(event) {
    const options = {
      url: `${process.env.REACT_APP_API_SERVICE_URL}/oldata/addrbaldistribution`,
      method: "get",
      headers: {
        "Content-Type": "application/json",
      },
    };
    return axios(options)
      .then((res) => {
        this.setState({
          distributionChart1: res.data,
        });
        })
        .catch((error) => {
          console.log(error);
        });
  };

  getSupplyLiquidity(event) {
    const options = {
      url: `${process.env.REACT_APP_API_SERVICE_URL}/oldata/supplyliquidity`,
      method: "get",
      headers: {
        "Content-Type": "application/json",
      },
    };
    return axios(options)
      .then((res) => {
        this.setState({
          supplyLiquidity: res.data,
        });
        })
        .catch((error) => {
          console.log(error);
        });
  };

  getTokenomicsSingleMeasures(event) {
    const options = {
      url: `${process.env.REACT_APP_API_SERVICE_URL}/oldata/tokenomics`,
      method: "get",
      headers: {
        "Content-Type": "application/json",
    },
  };
  return axios(options)
    .then((res) => {
      this.setState({
        total_balance: res.data["total_balance"],
        total_addr_cnt: res.data["total_addr_cnt"],
        top10_balance: res.data["top10_balance"],
        top100_balance: res.data["top100_balance"],
        top10_balance_nv: res.data["top10_balance_nv"],
        top10_perc: res.data["top10_perc"],
        top100_perc: res.data["top100_perc"],
        top10_nv_perc: res.data["top10_nv_perc"],
        sum_bal_ex_com: res.data["sum_bal_ex_com"],
        sum_bal_ex_com_val: res.data["sum_bal_ex_com_val"],
        addr_cnt_bal_gt1: res.data["addr_cnt_bal_gt1"],
        bal_community: res.data["bal_community"],
        bal_slow: res.data["bal_slow"],
        bal_liquid: res.data["bal_liquid"],
        cnt_community: res.data["cnt_community"],
        cnt_slow: res.data["cnt_slow"],
        cnt_liquid: res.data["cnt_liquid"],
        active_set_cnt: res.data["active_set_cnt"],
        validator_cnt: res.data["validator_cnt"],
      });
      })
      .catch((error) => {
      console.log(error);
      });
  };

  render() {
    const labels = [];
    const balances = [];
    const counts = [];
    this.state.balancesByType
      .forEach(element => {
        labels.push(element['account_type']);
        balances.push(element['balance']);
        counts.push(element['count']);
    });

    const labels_liq = [];
    const balances_liq = [];
    this.state.supplyLiquidity
      .forEach(element => {
        labels_liq.push(element['wallet_type_name']);
        balances_liq.push(element['balance']);
    });

    const labels_distr_chart1 = [];
    const balances_distr_chart1 = [];
    this.state.distributionChart1
      .forEach(element => {
        labels_distr_chart1.push(element['bucket_name']);
        balances_distr_chart1.push(element['balance']);
    });

    const labels_distr_chart2 = [];
    const balances_distr_chart2 = [];
    const percentages_distr_chart2 = [];
    this.state.distributionChart2
      .forEach(element => {
        labels_distr_chart2.push(element['bucket_name']);
        balances_distr_chart2.push(element['bucket_cumul']);
        percentages_distr_chart2.push(element['balance_perc']);
    });

    const labels_distr_chart3 = [];
    const balances_distr_chart3 = [];
    this.state.distributionChart3
      .forEach(element => {
        labels_distr_chart3.push(element['addr_order']);
        balances_distr_chart3.push(element['balance']);
    });

    const label_list = [labels, labels, labels_liq];
    const data_list = [balances, counts, balances_liq];
    const pie_obj_list = [];

    for (var i = 0; i < label_list.length; i++) {
      const obj = {
        labels: label_list[i],
        datasets: [
          {
            label: "data",
            data: data_list[i],
            backgroundColor: [
              "rgba(255, 99, 132, 0.8)",
              "rgba(54, 162, 235, 0.8)",
              "rgba(255, 206, 86, 0.8)",
              "rgba(75, 192, 192, 0.8)",
              "rgba(153, 102, 255, 0.8)",
              "rgba(255, 159, 64, 0.8)"
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
      pie_obj_list.push(obj);
    };

    const distribChart1Data = {
      labels: labels_distr_chart1,
      datasets: [
        {
          label: "Balance",
          data: balances_distr_chart1,
          fill: true,
          backgroundColor: "rgba(75,192,192,0.2)",
          borderColor: "rgba(75,192,192,1)"
        }
      ]
    };

    const distribChart2Data = {
      labels: labels_distr_chart2,
      datasets: [
        {
          label: "Total balance",
          data: balances_distr_chart2,
          fill: true,
          backgroundColor: "rgba(75,192,192,0.6)",
          borderColor: "rgba(75,192,192,1)"
        }
      ]
    };

    const distribChart3Data = {
      labels: labels_distr_chart3,
      datasets: [
        {
          label: "Balances",
          data: balances_distr_chart3,
          fill: true,
          backgroundColor: "rgba(75,192,192,0.2)",
          borderColor: "rgba(75,192,192,1)"
        }
      ]
    };

    return (
      <div className="columns tokenomics">
        <div className="main column mx-2 mb-4">
          <div className="main-section mb-4 bb">
            
            <h1 className="is-size-4 has-text-left mb-4 p-3 has-background-light">0L Tokenomics in numbers</h1>
            <div className="columns mb-3">
              <div className="column level-item has-text-centered">
                <p className="heading">
                  Active validators
                </p>
                <p className="title">
                  {this.state.active_set_cnt} / {this.state.validator_cnt}
                </p>
              </div>
              <div className="column level-item has-text-centered">
                <p className="heading">
                  community wallets
                </p>
                <p className="title">
                  {addDecSeperator(this.state.cnt_community)}
                </p>
              </div>
              <div className="column level-item has-text-centered">
                <p className="heading">
                  Addresses
                </p>
                <p className="title">
                  {addDecSeperator(this.state.total_addr_cnt)}
                </p>
              </div>
            </div>

            <div className="columns mb-3">
              <div className="column level-item has-text-centered">
                <p className="heading">
                  total supply
                </p>
                <p className="title">
                  {addDecSeperator(this.state.total_balance)}
                </p>
              </div>
              <div className="column level-item has-text-centered">
                <p className="heading">
                  liquid supply
                </p>
                <p className="title">
                  {addDecSeperator(this.state.bal_liquid)}
                </p>
              </div>
              <div className="column level-item has-text-centered">
                <p className="heading">
                  slow supply (non-community wallets)
                </p>
                <p className="title">
                  {addDecSeperator(this.state.bal_slow)}
                </p>
              </div>
            </div>

            <h1 className="is-size-4 has-text-left mb-4 p-3 has-background-light">Distribution</h1>
            <div className="columns">
              <div className="column">
                <h1 className="heading has-text-centered mb-1">
                  Balances by account type
                </h1>
                <Doughnut data={pie_obj_list[0]} />
              </div>
              <div className="column">
                <h1 className="heading has-text-centered mb-1">
                  Addresses count by account type
                </h1>
                <Doughnut data={pie_obj_list[1]} />
              </div>
              <div className="column">
                <h1 className="heading has-text-centered mb-1">
                  token liquidity
                </h1>
                <Doughnut data={pie_obj_list[2]} />
              </div>
            </div>
            <div className="mb-6 mt-6">
              <h1 className="heading has-text-centered mb-1">
                Address balance distribution (*)
              </h1>
              <Line data={distribChart1Data} />
              <p className="is-size-7">
                (*) Community wallets are not taken into account
              </p>
            </div>
            <div className="columns mb-6 mt-6">
              <div className="column">
                <h1 className="heading has-text-centered mb-1">
                  Distribution by top wallets (*)
                </h1>
                <Bar data={distribChart2Data} />
                <p className="is-size-7">
                  (*) Community wallets are not taken into account
                </p>
              </div>
              <div className="column">
                <h1 className="heading has-text-centered mb-1">
                  Top 100 address balance distribution (*)
                </h1>
                <Line data={distribChart3Data} />
                <p className="is-size-7">
                  (*) Community wallets are not taken into account
                </p>
              </div>
            </div>
            {/* main-section */}
          </div>
          {/* main */}
        </div>
        {/* tokenomics */}
      </div>
    );
  }
}
  
export default Tokenomics;
