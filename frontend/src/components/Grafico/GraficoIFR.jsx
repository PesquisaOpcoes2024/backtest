import React, { useEffect, useState } from 'react';
import Chart from 'react-apexcharts';

const RsiChart = () => {
    const [rsiData, setRsiData] = useState([]);
    const symbol = 'PETR4';  // Exemplo de ativo
    const from_date = '2023-01-01';
    const to_date = '2024-01-01';

    useEffect(() => {
        const fetchRsiData = async () => {
            try {
                const response = await fetch(`/api/ifr?symbol=${symbol}&from=${from_date}&to=${to_date}`);
                const data = await response.json();
                if (Array.isArray(data)) {
                    setRsiData(data);
                } else {
                    console.error('Erro ao buscar dados do IFR:', data.error);
                }
            } catch (error) {
                console.error('Error fetching RSI data:', error);
            }
        };

        fetchRsiData();
    }, []);

    // Preparando os dados para o gráfico
    const chartOptions = {
        chart: {
            type: 'line',
            height: 350,
        },
        title: {
            text: 'Gráfico do IFR (Índice de Força Relativa)',
            align: 'left'
        },
        xaxis: {
            categories: rsiData.map(item => new Date(item.date).toLocaleDateString()),
        },
        yaxis: {
            min: 0,
            max: 100,
            title: {
                text: 'RSI',
            },
        },
    };

    const series = [
        {
            name: 'RSI',
            data: rsiData.map(item => item.RSI), // Supondo que a propriedade do valor RSI no seu JSON seja `RSI`
        },
    ];

    return (
        <div>
            <Chart
                options={chartOptions}
                series={series}
                type="line"
                height={350}
            />
        </div>
    );
};

export default RsiChart;
