import axios from "axios";
const apiUrl = "https://peaceful-journey-07506.herokuapp.com/api/";

axios.interceptors.response.use(
  function (response) {
    return response;
  },
  function (error) {
    if (error.status === 404 || error.status === 403) {
      console.log("error");
    }
    return Promise.reject(error);
  }
);

export default {
  getHeaders() {
    let token = window.localStorage.getItem("token");
    if (token == null) {
      return {};
    }
    return { Authorization: "Bearer " + token };
  },
  get(url) {
    return axios.get(apiUrl + url, { headers: this.getHeaders() });
  },
  post(url, data) {
    return axios.post(apiUrl + url, data, { headers: this.getHeaders() });
  },
};
