import React from 'react';
import Chart from 'react-apexcharts';

const Grafico = ({ chartData, outliersData }) => {
  const chartOptions = {
    chart: {
      type: 'boxPlot',
    },
    title: {
      text: `Preço do Ativo ao Longo do Tempo`,
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
    <div id="chart">
      <Chart options={chartOptions} series={chartSeries} type="boxPlot" height={400} />
    </div>
  );
};

export default Grafico;

