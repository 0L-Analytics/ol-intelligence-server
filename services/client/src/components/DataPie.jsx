import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

const DataPie = (props) => {
  const labels = [];
  const values = [];
  
  props.dataSet.forEach(element => {
    labels.push(element[props.labelElem]);
    values.push(element[props.valueElem]);
  });

  const data = {
    labels: labels,
    datasets: [
      {
        data: values,
        backgroundColor: [
          "rgba(255, 99, 132, 0.8)",
          "rgba(54, 162, 235, 0.8)",
          "rgba(255, 206, 86, 0.8)",
          "rgba(75, 192, 192, 0.8)",
          "rgba(153, 102, 255, 0.8)",
          "rgba(255, 159, 64, 0.8)"
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

  const plugins = [
    {
      afterRender: function (chart) {
        var width = chart.width,
        height = chart.height,
        ctx = chart.ctx;
        ctx.restore();
        var fontSize = (height / 200).toFixed(2);
        ctx.font = fontSize + "em sans-serif";
        ctx.textBaseline = "top";
        var text = props.centerValue,
          textX = Math.round((width - ctx.measureText(text).width) / 2) - 60,
          textY = height / 2.18;
        ctx.fillText(text, textX, textY);
        ctx.save();
      }
    }
  ]

  const options = {
    plugins: {
      legend: { 
        // display: true,
        position: 'right'
      },
    },
    aspectRatio: 2,
    centerText: {
      display: true
    }
  };
  
  return (
    <Doughnut 
      data={data}
      options={options} 
      // plugins={plugins}
    />
  );
}
  
DataPie.propTypes = {
    dataSet: PropTypes.array.isRequired,
    centerValue: PropTypes.string.isRequired,
    labelElem: PropTypes.string.isRequired,
    valueElem: PropTypes.string.isRequired,
};
  
export default DataPie;
