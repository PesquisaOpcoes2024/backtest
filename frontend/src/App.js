import React, { useState } from 'react';
import MenuPrincipal from './components/MenuPrincipal/MenuPrincipal';
import Grafico from './components/Grafico/Grafico';
import GraficoRSI from './components/Grafico/GraficoIFR';
import axios from 'axios';
import './App.css';

const App = () => {
  const [symbol, setSymbol] = useState("");
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [chartData, setChartData] = useState([]);
  const [outliersData, setOutliersData] = useState([]);
  const [rsiData, setRsiData] = useState([]);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/data', {
        params: { symbol, from: fromDate, to: toDate, limitUp: 70, limitDown: 30, window: 15 }
      });
      const data = response.data;

      const formattedData = data.map(item => ({
        x: new Date(item.date).toLocaleDateString(),
        y: [item.low, item.open, item.close, item.high, item.high]
      }));

      const formattedOutliers = data.map(item => ({
        x: new Date(item.date).toLocaleDateString(),
        y: item.volume
      }));

      const formattedRsiData = data.map(item => ({
        x: new Date(item.date).toLocaleDateString(),
        y: item.RSI
      }));

      setChartData(formattedData);
      setOutliersData(formattedOutliers);
      setRsiData(formattedRsiData);
    } catch (error) {
      console.error("Erro ao buscar dados", error);
    }
  };

  return (
    <>
    <div className="container_principal">
      <div className="menu_container">
        <MenuPrincipal
          symbol={symbol}
          fromDate={fromDate}
          toDate={toDate}
          setSymbol={setSymbol}
          setFromDate={setFromDate}
          setToDate={setToDate}
          fetchData={fetchData}
        />
      </div>
      <div className="grafico_container">
        <Grafico
          chartData={chartData}
          outliersData={outliersData}
        />
      </div>
    </div>
    <div className="graficoIFR_container">
      <GraficoRSI rsiData={rsiData} />
    </div>
    </>
  );
};

export default App;
