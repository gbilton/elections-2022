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

  return (
    <div style={{ width: 1000, margin: "auto" }}>
      <p>PredictionsChart</p>
      {console.log(predictions)}
      <Line
        data={predictions}
        options={{
          maintainAspectRatio: true,
        }}
      />
    </div>
  );
}

export default PredictionsChart;

function parseData(predictions) {
  const bolsonaro = predictions.map((prediction) => prediction.bolsonaro);
  const lula = predictions.map((prediction) => prediction.lula);
  const time_ = predictions.map((prediction) => prediction.time_);

  const data = {
    labels: time_,
    datasets: [
      {
        label: "Jair Bolsonaro",
        data: bolsonaro,
      },
      {
        label: "Lula",
        data: lula,
      },
    ],
  };

  return data;
}
