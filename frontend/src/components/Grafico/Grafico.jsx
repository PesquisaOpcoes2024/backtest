import React from 'react';
import Chart from 'react-apexcharts';

const Grafico = ({ chartData, outliersData }) => {
  const options = {
    chart: {
      type: 'boxPlot',
      height: 350,
    },
    plotOptions: {
      boxPlot: {
        colors: {
          upper: '#5C4742',
          lower: '#A5978B',
        },
      },
    },
    xaxis: {
      type: 'category',
      title: {
        text: 'Data',
      },
      labels: {
        rotate: -45,
        rotateAlways: true,
      },
    },
    yaxis: {
      title: {
        text: 'Preço',
      },
    },
  };

  const series = [
    {
      name: 'Variação de Preços',
      type: 'boxPlot',
      data: chartData,
    },
    {
      name: 'Volume',
      type: 'scatter',
      data: outliersData,
      marker: {
        size: 5,
        fillColor: '#00E396',
      },
    },
  ];

  return (
    <div id="chart">
      <Chart options={options} series={series} type="boxPlot" height={350} />
    </div>
  );
};

export default Grafico;

