import React, { useState } from 'react';
import MenuPrincipal from './components/MenuPrincipal/MenuPrincipal';
import Grafico from './components/Grafico/Grafico';
import axios from 'axios';

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
  
      // Formatar os dados para o gráfico de boxplot
      const formattedData = data.map(item => ({
        x: new Date(item.date).toLocaleDateString(),
        y: [item.low, item.open, item.close, item.high, item.high] // Estrutura do boxplot: [low, q1, median, q3, high]
      }));
  
      // Formatar os outliers usando o volume
      const formattedOutliers = data.map(item => ({
        x: new Date(item.date).toLocaleDateString(),
        y: item.volume
      }));
  
      setChartData(formattedData);
      setOutliersData(formattedOutliers);
      
      console.log(data);
      console.log(formattedData);
      console.log(formattedOutliers);
  
    } catch (error) {
      console.error("Erro ao buscar dados", error);
    }
  };
  
  

  return (
    <div>
      <MenuPrincipal
        symbol={symbol}
        fromDate={fromDate}
        toDate={toDate}
        setSymbol={setSymbol}
        setFromDate={setFromDate}
        setToDate={setToDate}
        fetchData={fetchData}
      />
      <Grafico
        chartData={chartData}
        outliersData={outliersData}
      />
    </div>
  );
};

export default App;
