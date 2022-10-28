import axios from "axios";
import React, { useEffect, useState } from "react";
import BasicTable from "./DataTable";

function PredictionBoard() {
  const rows = [createData("Jair Bolsonaro", "loading..."), createData("Lula", "loading...")];
  const [prediction, setPrediction] = useState({
    time_: "loading...",
    rows: rows,
  });

  useEffect(() => {
    axios
      .get("http://localhost:8000/predictions/last")
      .then((response) => {
        console.log(response);
        setPrediction(parseData(response.data));
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div
      style={{
        // backgroundColor: "green",
        paddingLeft: "500px",
        paddingRight: "500px",
        paddingTop: "20px",
        borderRadius: "50px",
        marginBottom: "50px",
      }}
    >
      <BasicTable rows={prediction.rows} />
      <p style={{ textAlign: "center", fontWeight: "bold", fontSize: 20 }}>
        Updated: {prediction.time_}
      </p>
    </div>
  );
}

export default PredictionBoard;

function createData(candidate, percentageVotes) {
  return { candidate, percentageVotes };
}

function parseData(prediction) {
  const bolsonaro = parsePercentage(prediction.bolsonaro);
  const lula = parsePercentage(prediction.lula);
  const time_ = parseTime(prediction.time_);

  const rows = [createData("Jair Bolsonaro", bolsonaro), createData("Lula", lula)].sort();

  return {
    time_: time_,
    rows: rows,
  };
}

function parseTime(time_) {
  const date = new Date(time_);
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

function parsePercentage(percentage) {
  return (percentage * 100).toFixed(2) + "%";
}
