import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

export default function BasicTable(props) {
  return (
    <TableContainer component={Paper}>
      <Table
        sx={{
          backgroundColor: "#bdaed1",
        }}
      >
        <TableHead>
          <TableRow>
            <TableCell
              sx={{
                fontWeight: "bold",
                fontSize: 20,
              }}
            >
              Candidate
            </TableCell>
            <TableCell
              align="right"
              sx={{
                fontWeight: "bold",
                fontSize: 20,
              }}
            >
              Projected % Votes
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.rows.map((row) => (
            <TableRow>
              <TableCell>{row.candidate}</TableCell>
              <TableCell align="right">{row.percentageVotes}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
