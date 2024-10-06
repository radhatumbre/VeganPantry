// App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import RecipeGenerator from "./components/RecipeGenerator";
import RecipeDetails from "./components/RecipeDetails";
import "./App.css";
import Layout from "./components/Layout";
import AboutUs from "./components/About";
import HomePage from "./components/HomePage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          {/* add path="/recipe-gen"  */}
          <Route path="/recipe-gen" element={<RecipeGenerator />} />
          <Route path="/recipe/:id" element={<RecipeDetails />} />
          <Route path="/about" element={<AboutUs />} />
        </Route>
        {/* You can add other routes here */}
      </Routes>
    </Router>
  );
}

export default App;
