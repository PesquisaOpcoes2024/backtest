// MenuPrincipal.js
import React from 'react';
import './MenuPrincipal.css';

const MenuPrincipal = ({ symbol, fromDate, toDate, setSymbol, setFromDate, setToDate, fetchData }) => {
  return (
    <div>
      <h2 className="Titulo">Digite abaixo as informações da opção que deseja pesquisar:</h2>
      <div className="Digitacao">
        <div className="Local_digitacao_nome">
          <label>Símbolo:</label>
          <input
            type="text"
            className="Input"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          />
        </div>
        <div className="Local_digitacao_data">
          <label>Data de Início:</label>
          <input
            type="date"
            className="Input_data"
            value={fromDate}
            onChange={(e) => setFromDate(e.target.value)}
          />
          <label>Data de Fim:</label>
          <input
            type="date"
            className="Input_data"
            value={toDate}
            onChange={(e) => setToDate(e.target.value)}
          />
        </div>
        <div className='Botao'>
          <button onClick={fetchData} className='Botao_buscar'>Buscar Dados</button>
        </div>
      </div>
    </div>
  );
};

export default MenuPrincipal;
