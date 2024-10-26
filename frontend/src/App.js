import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Chart from 'react-apexcharts';

const App = () => {
  const [symbol, setSymbol] = useState("PETR4");
  const [fromDate, setFromDate] = useState("2023-01-01");
  const [toDate, setToDate] = useState("2023-12-31");
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    fetchData();
  }, [symbol, fromDate, toDate]);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/data', {
        params: { symbol, from: fromDate, to: toDate }
      });
      const data = response.data;

      // Formatação dos dados para o BoxPlot
      const formattedData = data.map(item => ({
        x: new Date(item.date).toLocaleDateString(),
        y: [item.high, item.close, item.close, item.close, item.high] // Exemplo de dados para o BoxPlot
      }));

      setChartData(formattedData);
    } catch (error) {
      console.error("Erro ao buscar dados", error);
    }
  };

  const chartOptions = {
    chart: {
      type: 'boxPlot',
    },
    title: {
      text: `Preço do Ativo ${symbol} ao Longo do Tempo`,
      align: 'center'
    },
    xaxis: {
      type: 'category',
    },
    yaxis: {
      title: { text: "Preço (R$)" },
    },
  };

  const chartSeries = [{
    name: 'BoxPlot',
    data: chartData
  }];

  return (
    <div>
      <h1>Visualizador de Preço de Ativo</h1>
      <input
        type="text"
        placeholder="Símbolo do Ativo"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
      />
      <input
        type="date"
        value={fromDate}
        onChange={(e) => setFromDate(e.target.value)}
      />
      <input
        type="date"
        value={toDate}
        onChange={(e) => setToDate(e.target.value)}
      />
      <button onClick={fetchData}>Atualizar Gráfico</button>

      <Chart options={chartOptions} series={chartSeries} type="boxPlot" height={400} />
    </div>
  );
};

export default App;
