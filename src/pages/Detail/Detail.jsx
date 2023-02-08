import "./detail.scss";

import React, { useState, useEffect } from "react";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
} from "chart.js";
import { Line } from "react-chartjs-2";

import axios from "axios";
import fileDownload from "js-file-download";

import * as dayjs from "dayjs";

import InputLabel from "@mui/material/InputLabel";
import FormControl from "@mui/material/FormControl";
import NativeSelect from "@mui/material/NativeSelect";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Stack from "@mui/material/Stack";

import { store } from "../../api/ObjectApi";

const Detail = () => {
  const [storeName, setStoreName] = useState(0);
  const [objStore, setObjStore] = useState([]);

  const [fromDate, setFromDate] = useState("2022-04-05");
  const [toDate, setToDate] = useState("2022-05-27");

  const [labelInput, setLabelInput] = useState();
  const [CH, setCH] = useState(storeName);

  /**Start handleChange Store */
  const handleChange = (e) => {
    setStoreName(e.target.value);
    setCH(e.target.value ? e.target.value : undefined);
  };
  /**End handleChange Store */

  /**Start loading */
  const loading = document.getElementsByClassName("loading");
  const loadingOverlay = document.getElementsByClassName("loading-overlay");
  /**End loading */

  /**Start ChartJS */
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Tooltip,
    Filler
  );
  const options = {
    responsive: true,
  };
  const labels = labelInput;
  const data = {
    labels,
    datasets: [
      {
        data: objStore.map((item, index) => objStore[index].value),
        label: "Doanh thu ",
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132, 0.5)",
        fill: true,
        pointStyle: "circle",
        pointRadius: 4,
        option: {
          scales: {
            xAxis: {
              offset: true,
              grid: {
                offset: true,
              },
              ticks: {
                autoSkip: true,
              },
            },
            yAxis: {
              beginAtZero: false,
              ticks: {
                autoSkip: true,
              },
            },
          },
          tooltip: {
            usePointStyle: true,
          },
        },
      },
    ],
  };
  /**End ChartJS */

  //#region Event
  const onDownload = () => {
    var myDict = {
      date1: fromDate,
      date2: toDate,
      CH: CH,
    };
    let formatDate1 = dayjs(fromDate).format("DD/MM");
    let formatDate2 = dayjs(toDate).format("DD/MM");
    axios
      .post("http://localhost:5001/download", {
        responseType: "blob",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(myDict),
      })
      .then((res) => {
        fileDownload(res.data, `${CH}_${formatDate1}_${formatDate2}.csv`);
      })
      .catch((err) => {
        console.log(err);
      });
  };
  //#endregion

  /** Start post API*/
  const getInfo = async () => {
    var myDict = {
      date1: fromDate,
      date2: toDate,
      CH: CH,
    };
    await axios
      .post("http://localhost:5001/predict", {
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(myDict),
      })
      .then((res) => {
        let obj = [];
        let date = [];
        for (var item in res.data) {
          obj.push({ value: res.data[item] });
          date.push(dayjs(item).format("DD/MM"));
        }
        setObjStore(obj);
        setLabelInput(date);
      });
  };
  /**End post API */

  /**Start func Submit */
  const handleSubmit = () => {
    console.log(storeName);
    setCH(storeName);
    getInfo();
  };
  /**Start func Submit */

  useEffect(() => {
    getInfo();

    /** Start Loading */
    window.onload = () => {
      loading[0].classList.add("block");
      loadingOverlay[0].classList.add("block");
    };
    setTimeout(() => {
      window.scrollTo(0, 0);
      loading[0].classList.remove("block");
      loadingOverlay[0].classList.remove("block");
    }, 2000);
    /**End Loading */
  }, []);

  return (
    <div className="detail">
      <div className="container-fluid detail__wrap ">
        <div className="detail__body">
          <div className="col-12 col-md-12 col-lg-3 detail__left">
            <FormControl fullWidth>
              <InputLabel
                id="demo-simple-select-label"
                className="detail-input__title"
              >
                Cửa hàng
              </InputLabel>
              {store.length > 0 && (
                <NativeSelect
                  inputProps={{
                    name: "date",
                    id: "demo-simple-select",
                  }}
                  onChange={handleChange}
                  className="native"
                  defaultValue={0}
                >
                  {store.map((item, index) => (
                    <option value={item.count} key={index}>
                      {item.name}
                    </option>
                  ))}
                </NativeSelect>
              )}
            </FormControl>
            <div className="detail-time">
              <div className="detail-title">Thời gian dự đoán</div>
              <Stack component="form" spacing={3} className="wrap-input">
                <TextField
                  id="date"
                  label="Từ ngày"
                  type="date"
                  className="fromDate"
                  defaultValue="2022-04-05"
                  onChange={(e) => setFromDate(e.target.value)}
                  sx={{ width: 220 }}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
                <TextField
                  id="date"
                  label="Đến ngày"
                  type="date"
                  className="toDate"
                  defaultValue="2022-05-27"
                  onChange={(e) => setToDate(e.target.value)}
                  sx={{ width: 220 }}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Stack>
            </div>
            <Button
              variant="contained"
              className=" predict-btn"
              onClick={handleSubmit}
            >
              DỰ ĐOÁN
            </Button>
            <Button
              variant="contained"
              className="detail-btn"
              onClick={onDownload}
            >
              TẢI VỀ
            </Button>
          </div>
          <div className="loading-overlay">
            <div className="spinner-border loading" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
          <div className="col-12 col-md-12 col-lg-1"></div>
          <div className="col-12 col-sx-12 col-md-12 col-lg-8 detail__right">
            <div className="detail__chart">
              <div className="detail__chart--title">Biểu đồ dự đoán</div>
              <div className="detail__chart--desc">Doanh thu (triệu)</div>
              <Line options={options} data={data} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Detail;
