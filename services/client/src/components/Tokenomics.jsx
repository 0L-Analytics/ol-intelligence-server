import React, { Component } from "react";
import { Route, Routes } from "react-router-dom";
import PropTypes from "prop-types";
import axios from "axios";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import DataPie from "./DataPie";
import DateTime from "./DateTime"

import "./Tokenomics.css";


ChartJS.register(ArcElement, Tooltip, Legend);

function numberWithCommas(x) {
  var parts = x.toString().split(".");
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return parts.join(".");
}

class Tokenomics extends Component {
    constructor(props) {
        super(props);
        this.state = {
            balancesByType: [],
            totalBalance: 0,
            totalCount: 0,
            valBalPercentage: 0.0,
            valCntPercentage: 0.0,
            minBalPercentage: 0.0,
            minCntPercentage: 0.0,
            basBalPercentage: 0.0,
            basCntPercentage: 0.0,
            comBalPercentage: 0.0,
            comCntPercentage: 0.0,           
        };
    }

    componentDidMount() {
        this.getBalanceByType();
    }

    calculatePercentage(data, accountType, measure, divider) {
      let outp = 0.0;
      if('data' in this.state.balancesByType) {
        return 0.0
      }
      data.forEach(element => {
        if(accountType===element['account_type']) {
          outp = (Math.round((parseInt(element[measure]) / parseInt(divider)) * 10000) / 100)
        }
      })
      return outp
    }

    getBalanceByType(event) {
      const options = {
        url: `${process.env.REACT_APP_API_SERVICE_URL}/oldata/balancebytype`,
        method: "get",
        headers: {
          "Content-Type": "application/json",
        },
      }
      return axios(options)
        .then((res) => {
          this.setState({
            balancesByType: res.data['data'],
            totalBalance: res.data['sum_balance'],
            totalCount: res.data['sum_count'],
            valBalPercentage: this.calculatePercentage(res.data['data'], 'validator', 'balance', res.data['sum_balance']),
            valCntPercentage: this.calculatePercentage(res.data['data'], 'validator', 'count', res.data['sum_count']),
            minBalPercentage: this.calculatePercentage(res.data['data'], 'miner', 'balance', res.data['sum_balance']),
            minCntPercentage: this.calculatePercentage(res.data['data'], 'miner', 'count', res.data['sum_count']),
            basBalPercentage: this.calculatePercentage(res.data['data'], 'basic', 'balance', res.data['sum_balance']),
            basCntPercentage: this.calculatePercentage(res.data['data'], 'basic', 'count', res.data['sum_count']),
            comBalPercentage: this.calculatePercentage(res.data['data'], 'community', 'balance', res.data['sum_balance']),
            comCntPercentage: this.calculatePercentage(res.data['data'], 'community', 'count', res.data['sum_count']),
          });
          })
          .catch((error) => {
            console.log(error);
          });
    }
    render() {
      console.log(this.state.basBalPercentage);
      return (
          <div>
            <div className="level">
              <div className="level-left">
                <div className="level-item">
                  <div className="title">Tokenomics</div>
                </div>
              </div>
              <div className="level-right">
                <div className="level-item">
                  <button type="button" className="button is-small">
                    <DateTime />
                  </button>
                </div>
              </div>
            </div>
            
            <div className="columns is-multiline">
              <div className="column">
                <div className="box">
                  <div className="heading has-text-centered">Total supply</div>
                  <div className="title has-text-centered">
                    {numberWithCommas(Math.round(this.state.totalBalance / 10000) / 100) + ' M'}
                  </div>
                  <div className="level">
                    <div className="level-item">
                      <div>
                        <div className="heading ">Community</div>
                        <div className="title is-5">
                          {this.state.basBalPercentage}%
                        </div>
                      </div>
                    </div>
                    <div className="level-item">
                      <div>
                        <div className="heading">Validator</div>
                        <div className="title is-5">
                          {this.state.valBalPercentage}%
                        </div>
                      </div>
                    </div>
                    <div className="level-item">
                      <div>
                        <div className="heading">Miner</div>
                        <div className="title is-5">
                          {this.state.minBalPercentage}%
                        </div>
                      </div>
                    </div>
                    <div className="level-item">
                      <div>
                        <div className="heading">Basic</div>
                        <div className="title is-5">
                          {this.state.basBalPercentage}%
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="column">
                <div className="box">
                  <div className="heading has-text-centered">Addresses</div>
                  <div className="title has-text-centered">
                    {numberWithCommas(this.state.totalCount)}
                  </div>
                  <div className="level">
                    <div className="level-item">
                      <div className="">
                        <div className="heading">Community</div>
                        <div className="title is-5">
                          {this.state.comCntPercentage}%
                        </div>
                      </div>
                    </div>
                    <div className="level-item">
                      <div className="">
                        <div className="heading">Validator</div>
                        <div className="title is-5">
                          {this.state.valCntPercentage}%
                        </div>
                      </div>
                    </div>
                    <div className="level-item">
                      <div className="">
                        <div className="heading">Miner</div>
                        <div className="title is-5">
                          {this.state.minCntPercentage}%
                        </div>
                      </div>
                    </div>
                    <div className="level-item">
                      <div className="">
                        <div className="heading">Basic</div>
                        <div className="title is-5">
                          {this.state.basCntPercentage}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
            
            <div className="columns is-multiline">

              <div className="column is-6">
                <div className="panel">
                  <p className="panel-heading">
                    Token distribution
                  </p>
                  <div className="panel-block">
                    <DataPie 
                      dataSet={this.state.balancesByType}
                      labelElem='account_type'
                      valueElem='balance'
                      centerValue={this.state.totalBalance.toString()}
                    />
                  </div>
                </div>
              </div>

              <div className="column is-6">
                <div className="panel">
                  <p className="panel-heading">
                    Address distribution
                  </p>
                  <div className="panel-block">
                    <DataPie 
                      dataSet={this.state.balancesByType}
                      labelElem='account_type'
                      valueElem='count'
                      centerValue={this.state.totalCount.toString()}
                    />
                  </div>
                </div>
              </div>

              <div className="column is-6">
                <div className="panel">
                  <p className="panel-heading">
                    Something
                  </p>
                  <div className="panel-block">
                    <figure className="image is-16x9">
                      image
                    </figure>
                  </div>
                </div>
              </div>
              
              <div className="column is-6">
                <div className="panel">
                  <p className="panel-heading">
                    Something Else
                  </p>
                  <div className="panel-block">
                    <figure className="image is-16x9">
                      image
                    </figure>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
    }
}
  
export default Tokenomics;
