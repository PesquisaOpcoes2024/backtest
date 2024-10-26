import React, { useState } from 'react';
import Grafico from '../Grafico/Grafico';

const Opcoes = () => {
  const [ticker, setTicker] = useState('');  // Ticker selecionado

  const handleTickerChange = (e) => {
    setTicker(e.target.value);
  };

  return (
    <div>
      <input 
        type="text" 
        value={ticker} 
        onChange={handleTickerChange} 
        placeholder="Digite o ticker da ação" 
      />
      <Grafico ticker={ticker} />
    </div>
  );
};

export default Opcoes;
