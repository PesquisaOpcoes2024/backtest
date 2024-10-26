import React, { useState } from 'react';
import "./MenuPrincipal.css"

const MenuPrincipal = () => {
    const [data, setData] = useState(null); // Definindo o estado fora da função

    // Função para buscar os dados
    const fetchData = async () => {
        try {
            const response = await fetch('/data');  // Requisição para o endpoint em Node.js
            const result = await response.json();
            setData(result);
        } catch (error) {
            console.error('Erro ao buscar dados:', error);
        }
    };

    return (
        <div>
            <h2 className='Titulo'>Digite abaixo as informacoes da opcao que deseja pesquisar:</h2>
            <div className='Digitacao'>
                <div className='Local_digitacao_nome'>
                    <h3>Nome da opcao:</h3>
                    <input type="text" className='Input' /> {/* Corrigido para text */}
                </div>
                <div className='Local_digitacao_data'>
                    <div className='Data'>
                        <label>Inicio:</label>
                        <input type="date" className='Input_data' />
                    </div>
                    <div className='Data'>
                        <label>Fim:</label>
                        <input type="date" className='Input_data' />
                        <div className='Botao'>
                            <button onClick={fetchData} className='Botao_buscar'>Buscar Dados</button>
                        </div>
                    </div>
                </div>
                {/* Exibe os dados buscados se existirem */}
                {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
            </div>
        </div>
    );
};

export default MenuPrincipal;
