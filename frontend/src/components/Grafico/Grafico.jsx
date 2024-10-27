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
    },
  };

  const series = [
    {
      name: 'box',
      type: 'boxPlot',
      data: chartData,
    },
    {
      name: 'outliers',
      type: 'scatter',
      data: outliersData,
    },
  ];

  return (
    <div id="chart">
      <Chart options={options} series={series} type="boxPlot" height={350} />
    </div>
  );
};

export default Grafico;
