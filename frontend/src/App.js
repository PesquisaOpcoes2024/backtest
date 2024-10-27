import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Chart from 'react-apexcharts';

const App = () => {
  const [symbol, setSymbol] = useState("");
  const [fromDate, setFromDate] = useState("2023-01-01");
  const [toDate, setToDate] = useState("2023-12-31");
  const [chartData, setChartData] = useState([]);
  const [outliersData, setOutliersData] = useState([]);

  useEffect(() => {
    fetchData();
  }, [symbol, fromDate, toDate]);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/data', {
        params: { symbol, from: fromDate, to: toDate }
      });
      const data = response.data;

      // Formatação dos dados para o BoxPlot (grafico gordinho) e Outliers (bola que representa o volume do ativo)
      const formattedData = data.map(item => ({
        x: new Date(item.date).toLocaleDateString(),
        y: [item.low, item.open, item.close, item.close, item.high]
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
    yaxis: [
      {
        title: { text: "Preço (R$)" },
      },
      {
        opposite: true,
        title: { text: "Volume" },
        labels: {
          formatter: (val) => `${val.toFixed(0)}`,
        }
      }
    ]
  };

  const chartSeries = [
    {
      name: 'BoxPlot',
      type: 'boxPlot',
      data: chartData,
    },
    {
      name: 'Volume',
      type: 'scatter',
      data: outliersData,
      yAxisIndex: 1, // Define que os outliers(volume) usarão o eixo Y secundário
    },
  ];

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
