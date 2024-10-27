import React, { useState } from 'react';
import MenuPrincipal from './components/MenuPrincipal/MenuPrincipal';
import Grafico from './components/Grafico/Grafico';
import RsiChart from './components/Grafico/GraficoIFR'; // Importar o componente RsiChart
import axios from 'axios';
import './App.css'; // Importar o arquivo CSS

const App = () => {
  const [symbol, setSymbol] = useState("");
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [chartData, setChartData] = useState([]);
  const [outliersData, setOutliersData] = useState([]);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/data', {
        params: { symbol, from: fromDate, to: toDate }
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
  
      setChartData(formattedData);
      setOutliersData(formattedOutliers);
      
    } catch (error) {
      console.error("Erro ao buscar dados", error);
    }
  };

  const fetchRsiData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/ifr', {
        params: { symbol, from: fromDate, to: toDate }
      });
      // Aqui você pode processar e armazenar os dados do IFR se necessário
      console.log("Dados do IFR:", response.data);
    } catch (error) {
      console.error("Erro ao buscar dados do IFR", error);
    }
  };

  return (
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
          fetchRsiData={fetchRsiData} // Passando a função fetchRsiData como prop
        />
      </div>
      <div className="grafico_container">
        <Grafico
          chartData={chartData}
          outliersData={outliersData}
        />
      </div>
      <div className="rsi_chart_container">
        <RsiChart /> {/* Adicionando o componente RsiChart aqui */}
      </div>
    </div>
  );
};

export default App;
