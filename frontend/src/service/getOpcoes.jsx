import axios from 'axios';

const getOpcoesData = async (ticker) => {
  const apiKey = 'qUoxkqtK2dhIa4q3Ir9yqwnuYMvfYnHLtedgxM/EjBZHqE7SQv8/0ZE7y+nukIYZ--XhgBD6EPwF8T0Ffj4y3u1A==--ZTNjNDZiMDNkZGQ0MzBlMjFhMGQ4OGVhN2MyMWVkMzE=';  // Coloque sua chave de API aqui.

  try {
    const response = await axios.get(`https://api.oplab.com.br/v3/options/${ticker}`, {
      headers: {
        'Authorization': `Bearer ${apiKey}`,
      },
    });

    const optionsData = response.data;

    // Processar os dados como necessário para o gráfico.
    const formattedData = optionsData.map(option => ({
      strike: option.strike, 
      price: option.lastPrice, 
      expiration: option.expirationDate,
      impliedVolatility: option.impliedVolatility,
    }));

    return formattedData;

  } catch (error) {
    console.error('Erro ao buscar dados da opção:', error);
    return [];
  }
};

export default getOpcoesData;
