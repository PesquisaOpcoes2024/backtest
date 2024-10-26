//Rodar o comando npm install chart.js
//Rodar o comando npm install npm install react-chartjs-2
//Rodar o comando npm install npm install axios

import React, { useEffect, useState } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import getOpcoesData from '../service/getOpcoes';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const Grafico = ({ ticker }) => {
  const [chartData, setChartData] = useState(null); // Inicialmente null
  const [loading, setLoading] = useState(true); // Estado de carregamento
  const [error, setError] = useState(null); // Estado de erro

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true); // Ativa o carregamento
        const optionsData = await getOpcoesData(ticker);
        
        // Verifica se optionsData é um array válido antes de usar map
        if (Array.isArray(optionsData) && optionsData.length > 0) {
          setChartData({
            labels: optionsData.map(option => option.expiration),
            datasets: [
              {
                label: 'Preço das Opções',
                data: optionsData.map(option => option.price),
                borderColor: 'rgba(75,192,192,1)',
                fill: false,
              },
              {
                label: 'Volatilidade Implícita',
                data: optionsData.map(option => option.impliedVolatility),
                borderColor: 'rgba(255,99,132,1)',
                fill: false,
              }
            ],
          });
        } else {
          setError('Dados não disponíveis ou retornaram vazio.');
        }
      } catch (err) {
        setError('Erro ao carregar os dados: ' + err.message);
      } finally {
        setLoading(false); // Desativa o carregamento
      }
    };

    fetchData();
  }, [ticker]);

  if (loading) {
    return <div>Carregando gráfico...</div>; // Indicador de carregamento
  }

  if (error) {
    return <div>{error}</div>; // Exibe erro, se houver
  }

  return (
    <div className="grafico-container">
      {chartData ? <Line data={chartData} /> : <div>Nenhum dado para exibir.</div>}
    </div>
  );
};

export default Grafico;
