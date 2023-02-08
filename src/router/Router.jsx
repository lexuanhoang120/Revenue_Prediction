import React from "react";
import { Routes, Route } from "react-router-dom";

import Home from "../pages/Home/Home";
import Detail from "../pages/Detail/Detail";

const Router = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} exact />
      <Route path="/detail" element={<Detail />} />
    </Routes>
  );
};

export default Router;
