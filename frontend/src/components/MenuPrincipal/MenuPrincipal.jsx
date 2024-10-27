import React from 'react';
import './MenuPrincipal.css';

const MenuPrincipal = ({ symbol, fromDate, toDate, setSymbol, setFromDate, setToDate, fetchData }) => {
  return (
    <div>
      <h2 className="Titulo">Digite abaixo as informações da opção que deseja pesquisar:</h2>
      <div className="Digitacao">
        <div className="Local_digitacao_nome">
          <h3>Nome da opção:</h3>
          <input
            type="text"
            className="Input"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          />
        </div>
        <div className="Local_digitacao_data">
          <div className="Data">
            <label>Referência Inicial:</label>
            <input
              type="date"
              className="Input_data"
              value={fromDate}
              onChange={(e) => setFromDate(e.target.value)}
            />
          </div>
          <div className="Data">
            <label>Referência Final:</label>
            <input
              type="date"
              className="Input_data"
              value={toDate}
              onChange={(e) => setToDate(e.target.value)}
            />
            <div className="Botao">
              <button onClick={fetchData} className="Botao_buscar">Buscar Dados</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MenuPrincipal;
