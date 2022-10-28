import axios from "axios";
import React, { useEffect, useState } from "react";

function PredictionBoard() {
  const [prediction, setPrediction] = useState({
    bolsonaro: "loading...",
    lula: "loading...",
    time_: "loading...",
  });

  useEffect(() => {
    axios
      .get("http://localhost:8000/predictions/last")
      .then((response) => {
        console.log(response);
        setPrediction(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div style={{ margin: "auto" }}>
      <p>Prediction</p>
      <p>Jair Bolsonaro: {prediction.bolsonaro}</p>
      <p>Lula: {prediction.lula}</p>
      <p>Updated: {prediction.time_}</p>
    </div>
  );
}

export default PredictionBoard;
