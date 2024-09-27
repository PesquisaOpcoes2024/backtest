#O IFR de um ativo nada mais é do que a razão entre suas variações positivas (U) e sua variação total (U+D), ao longo de um período específico, em uma escala de 0 a 100.
#parametros recomendados são um período de 14 dias, , ao passo que valores acima de 70 sugerem um ativo sobrecomprado e abaixo de 30 indicam um ativo sobrevendido.

#para entender as estruturas desse código, acesse os links:https://quantbrasil.com.br/aprenda-a-calcular-o-ifr-indice-de-forca-relativa/ e https://quantbrasil.com.br/criando-o-backtest-da-estrategia-de-ifr2-em-python/

#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import math
from datetime import datetime, timedelta

# Função para calcular o RSI (Índice de Força Relativa)
def calculate_rsi(data, column, window=14):
    data = data.copy()
    
    # Calcula ganhos e perdas diários
    data['Variation'] = data[column].diff()
    data['Gain'] = np.where(data['Variation'] > 0, data['Variation'], 0)
    data['Loss'] = np.where(data['Variation'] < 0, data['Variation'], 0)

    # Calcula médias simples de ganho e perda para inicializar as médias móveis
    simple_avg_gain = data['Gain'].rolling(window).mean()
    simple_avg_loss = data['Loss'].abs().rolling(window).mean()
    classic_avg_gain = simple_avg_gain.copy()
    classic_avg_loss = simple_avg_loss.copy()

    # Calcula médias móveis de ganho e perda
    for i in range(window, len(classic_avg_gain)):
        classic_avg_gain[i] = (classic_avg_gain[i - 1] * (window - 1) + data['Gain'].iloc[i]) / window
        classic_avg_loss[i] = (classic_avg_loss[i - 1] * (window - 1) + data['Loss'].abs().iloc[i]) / window
    
    # Calcula o RSI
    RS = classic_avg_gain / classic_avg_loss
    RSI = 100 - (100 / (1 + RS))
    return RSI

# Função para plotar o RSI junto com o preço do ativo
def plot_rsi(data, column, window=14, limit_up=70.0, limit_down=30.0):
    RSI = calculate_rsi(data, column, window)
    
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
    
    # Plotar dados de preço
    ax1.plot(data.index, data[column], linewidth=3, label=column)
    ax1.legend()

    # Plotar RSI
    ax2.plot(data.index, RSI, label='IFR', color="#033660")
    ax2.axhline(y=limit_down, color='white', linestyle='--')
    ax2.axhline(y=limit_up, color='white', linestyle='--')
    ax2.axhspan(limit_down, limit_up, color='indigo', alpha=0.2)
    ax2.set_ylim(0, 100)
    ax2.legend()

    plt.show()

# Função para executar o backtest da estratégia de compra e venda
def run_backtest(df, rsi_parameter=30, initial_capital=10000):
    df['IFR2'] = calculate_rsi(df, column="Adj Close", window=2)
    
    # Corrige o erro aqui
    df["Target1"] = df["High"].shift(1)
    df["Target2"] = df["High"].shift(2)
    df["Target"] = df[["Target1", "Target2"]].max(axis=1)
    df.drop(columns=["Target1", "Target2"], inplace=True)

    # Definir preços de compra e venda
    df["Buy Price"] = np.where(df["IFR2"] <= rsi_parameter, df["Close"], np.nan)
    df["Sell Price"] = np.where(df["High"] > df['Target'], 
                                np.where(df['Open'] > df['Target'], df['Open'], df['Target']), np.nan)

    total_capital, all_profits = calculate_profits(df, initial_capital)
    return total_capital, all_profits

# Função para calcular lucros de cada operação
def calculate_profits(df, initial_capital):
    total_capital = [initial_capital]
    all_profits = []
    ongoing = False
    
    for i in range(len(df)):
        if ongoing:
            if ~np.isnan(df['Sell Price'][i]):
                exit_price = df['Sell Price'][i]
                profit = shares * (exit_price - entry_price)
                all_profits.append(profit)
                total_capital.append(total_capital[-1] + profit)
                ongoing = False
        else:
            if ~np.isnan(df['Buy Price'][i]):
                entry_price = df['Buy Price'][i]
                shares = round_down(initial_capital / entry_price)
                ongoing = True

    return total_capital, all_profits

# Função para arredondar qualquer número para o menor múltiplo de 100
def round_down(x):
    return int(math.floor(x / 100.0)) * 100

# Função para testar a estratégia e mostrar resultados
def strategy_test(all_profits):
    num_operations = len(all_profits)
    gains = sum(x >= 0 for x in all_profits)
    pct_gains = 100 * (gains / num_operations)
    losses = num_operations - gains
    pct_losses = 100 - pct_gains

    print("Number of operations =", num_operations)
    print("Number of gains =", gains, "or", round(pct_gains), "%")
    print("Number of loss =", losses, "or", round(pct_losses), "%")
    print("The total profit was =", sum(all_profits))

# Função para plotar a evolução do capital
def capital_plot(total_capital, all_profits):
    all_profits = [0] + all_profits
    cap_evolution = pd.DataFrame({'Capital': total_capital, 'Profit': all_profits})
    plt.title("Curva de Capital")
    plt.xlabel("Total Operações")
    cap_evolution['Capital'].plot()
    plt.show()

# Função principal para baixar dados e rodar o backtest
def main():
    
    # Calcula as datas de início e fim
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3000)
    
    # Converte as datas para string no formato exigido pelo yfinance
    end_date_str = end_date.strftime("%Y-%m-%d")
    start_date_str = start_date.strftime("%Y-%m-%d")

    # Baixa os dados de uma semana atrás até hoje
    data = yf.download("EMBR3.SA", start=start_date_str, end=end_date_str)
    plot_rsi(data, column="Adj Close", window=9, limit_up=80, limit_down=20)
    
    df = yf.download("LREN3.SA", start=start_date_str, end=end_date_str).copy()[["Open", "High", "Close", "Adj Close"]]
    total_capital, all_profits = run_backtest(df)
    
    strategy_test(all_profits)
    capital_plot(total_capital, all_profits)

# Executa o script principal
if __name__ == "__main__":
    main()
# %%
