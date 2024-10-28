import React from 'react';
import Chart from 'react-apexcharts';

const GraficoRSI = ({ rsiData }) => {
  const options = {
    chart: {
      type: 'line',
      height: 350
    },
    stroke: {
      curve: 'smooth'
    },
    yaxis: {
      title: {
        text: 'RSI'
      },
      min: 0,
      max: 100
    },
    annotations: {
      yaxis: [
        {
          y: 70,
          borderColor: '#FF0000',
          label: {
            text: 'Limite Superior',
            style: {
              color: '#FF0000'
            }
          }
        },
        {
          y: 30,
          borderColor: '#0000FF',
          label: {
            text: 'Limite Inferior',
            style: {
              color: '#0000FF'
            }
          }
        }
      ]
    }
  };

  const series = [
    {
      name: "RSI",
      data: rsiData
    }
  ];

  return <Chart options={options} series={series} type="line" height={350} />;
};

export default GraficoRSI;
