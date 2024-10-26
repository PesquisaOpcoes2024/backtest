import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Chart from 'react-apexcharts';

const App = () => {
  const [symbol, setSymbol] = useState("PETR4");
  const [fromDate, setFromDate] = useState("2023-01-01");
  const [toDate, setToDate] = useState("2023-12-31");
  const [chartData, setChartData] = useState({ dates: [], prices: [] });

  useEffect(() => {
    fetchData();
  }, [symbol, fromDate, toDate]);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/data', {
        params: { symbol, from: fromDate, to: toDate }
      });
      const data = response.data;

      // Formatação dos dados para o ApexCharts
      const dates = data.map(item => new Date(item.date).toLocaleDateString());
      const prices = data.map(item => item.close);

      setChartData({ dates, prices });
    } catch (error) {
      console.error("Erro ao buscar dados", error);
    }
  };

  const chartOptions = {
    chart: {
      type: 'line',
      zoom: { enabled: true },
    },
    xaxis: {
      categories: chartData.dates,
    },
    yaxis: {
      title: { text: "Preço de Fechamento (R$)" }
    },
    title: {
      text: `Preço do Ativo ${symbol} ao Longo do Tempo`,
      align: 'center'
    }
  };

  const chartSeries = [{ name: "Preço de Fechamento", data: chartData.prices }];

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

      <Chart options={chartOptions} series={chartSeries} type="line" height={400} />
    </div>
  );
};

export default App;
