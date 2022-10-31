import React, { useEffect, useState } from "react";
import axios from "axios";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS } from "chart.js/auto";

function PredictionsChart() {
  const [predictions, setPredictions] = useState({
    datasets: [],
    labels: [],
  });

  useEffect(() => {
    axios
      .get("http://localhost:8000/predictions")
      .then((response) => {
        console.log(response);
        setPredictions(parseData(response.data));
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  useEffect(() => {
    const interval = setInterval(
      () =>
        axios
          .get("http://localhost:8000/predictions")
          .then((response) => {
            console.log(response);
            setPredictions(parseData(response.data));
          })
          .catch((error) => {
            console.log(error);
          }),
      5 * 60 * 1000
    );
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ width: 850, margin: "auto" }}>
      {console.log(predictions)}
      <Line
        data={predictions}
        options={{
          plugins: {
            title: {
              display: true,
              text: "Predictions X Time",
            },
          },
          maintainAspectRatio: true,
          scales: {
            y: {
              min: 40,
              max: 60,
              ticks: {
                callback: function (value) {
                  return value + "%";
                },
              },
            },
            x: {
              ticks: {
                autoSkip: true,
                maxTicksLimit: 6,
              },
            },
          },
        }}
      />
    </div>
  );
}

export default PredictionsChart;

function parseData(predictions) {
  const bolsonaro = predictions.map((prediction) => prediction.bolsonaro * 100);
  const lula = predictions.map((prediction) => prediction.lula * 100);
  const time_ = predictions.map((prediction) => parseTime(prediction.time_));

  function parseTime(time_) {
    const date = new Date(time_);
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }
  const data = {
    backgroundColor: ["rgb(189, 174, 209)"],
    labels: time_,
    datasets: [
      {
        label: "Jair Bolsonaro",
        data: bolsonaro,
        borderColor: "#3c9e35",
        backgroundColor: "#3c9e35",
      },
      {
        label: "Lula",
        data: lula,
        borderColor: "#ff3200",
        backgroundColor: "#ff3200",
      },
    ],
  };

  return data;
}
