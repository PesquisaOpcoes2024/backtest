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
        <div className="Local_digitacao_nome">
          <label>Data de Início:</label>
          <input
            type="date"
            className="Input"
            value={fromDate}
            onChange={(e) => setFromDate(e.target.value)}
          />
        </div>
        <div className="Local_digitacao_nome">
          <label>Data de Fim:</label>
          <input
            type="date"
            className="Input"
            value={toDate}
            onChange={(e) => setToDate(e.target.value)}
          />
        </div>
      <button onClick={fetchData}>Buscar Dados</button>
      </div>
    </div>
  );
};

export default MenuPrincipal;
