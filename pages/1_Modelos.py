from libraries import *


########## CONFIGURAÇÃO ##############
st.set_page_config(page_icon=":chart:", layout='centered', page_title="Modelos")

with open("src/css/style.css") as i:
        st.markdown(f'<style>{i.read()}</style>', unsafe_allow_html=True)

####### Leitura e Ajuste na Base de Dados ##########

df = pd.read_csv("db_petroleo.csv",sep=";")

# Converter a coluna 'ds' para datetime64
df['ds'] = pd.to_datetime(df['ds'])

# Substituir vírgulas por pontos e converter para float
df['y'] = df['y'].str.replace(',', '.').astype(float)

# Filtrar as linhas para incluir apenas aquelas após 01-01-2010
df = df[df['ds'] >= '2010-01-01'].reset_index(drop=True)

# DataFrame com todos os dias
datas_completas = pd.date_range(start='2010-01-01', end='2024-01-16', freq='D')
df_datas_completas = pd.DataFrame({'ds': datas_completas})

# Realizar um merge para incluir todas as datas
df = df_datas_completas.merge(df, on='ds', how='left')

df['y'] = df['y'].fillna(method='ffill')
df['unique_id'] = df['unique_id'].fillna(method='ffill')

# Definir a coluna 'ds' como o índice
df.set_index('ds', inplace=True)

valor_treino = int(0.8 * len(df))

df_2 = df.copy()
df_2.reset_index(inplace=True) 
df_treino, df_teste = df_2[:valor_treino], df_2[valor_treino:]

def avaliar_resultado(joiner_db,modelo_teste):

    mae = mean_absolute_error(joiner_db['y'],joiner_db[modelo_teste])
    mape = mean_absolute_percentage_error(joiner_db['y'],joiner_db[modelo_teste])
    rmse = np.sqrt(mean_squared_error(joiner_db['y'],joiner_db[modelo_teste]))
    r2 = r2_score(joiner_db['y'],joiner_db[modelo_teste])

    return mae, mape, rmse, r2

    print(f'mae - naive: {mae}')
    print(f'mape - naive: {mape}')
    print(f'rmse - naive: {rmse}')
    print(f'r2 - naive: {r2}')


##########ABAS DO STREAMLIT ###################
aba1, aba2, aba3 = st.tabs(['Avaliação dos Dados', 'NAIVE', 'ARIMA'])



with aba1:
    ########## TÍTULO ##############
            
    st.markdown('''
    # Modelagem de Previsão de Preços (BRENT)

    ---

    Ao realizar a modelagem de séries temporais para prever os preços do petróleo, é essencial realizar várias análises exploratórias e ferramentas antes de escolher e ajustar um modelo. 
    Para avaliarmos a melhor forma de montar o modelo utilizaremos Seasonal Decompose, ADF Test, ACF e PACF.
                            
    ## Seasonal Decompose
    
    Os preços do petróleo podem exibir padrões sazonais devido a fatores como flutuações na demanda durante diferentes períodos do ano ou sazonalidade na produção. O seasonal decompose permite identificar e separar essas componentes sazonais dos dados, o que é fundamental para modelar com precisão e remover qualquer efeito sazonal dos preços antes da modelagem.
                
    ~~~python
                   
        def seasonal_decompose_plot(df):
        fig, axes = plt.subplots(4, 1, figsize=(10, 8))

        # Decomposição sazonal
        decomposition = seasonal_decompose(df['y'], model='additive', period=365)

        # Dados reais
        decomposition.observed.plot(ax=axes[0])
        axes[0].set_ylabel('Observed')

        # Tendência
        decomposition.trend.plot(ax=axes[1])
        axes[1].set_ylabel('Trend')

        # Sazonalidade
        decomposition.seasonal.plot(ax=axes[2])
        axes[2].set_ylabel('Seasonal')

        # Resíduos
        decomposition.resid.plot(ax=axes[3])
        axes[3].set_ylabel('Residual')
    ~~~            
                
    ---
    
    Abaixo foram avaliadas:

    1) Série Temporal 
    2) Tendência geral da série
    2) Sazonalidade (período avaliado de 365 dias)
    3) Resíduos (não explicados pelos itens anteriores).

    ''')

    def seasonal_decompose_plot(df):
        fig, axes = plt.subplots(4, 1, figsize=(10, 8))

        # Decomposição sazonal
        decomposition = seasonal_decompose(df['y'], model='additive', period=365)

        # Dados reais
        decomposition.observed.plot(ax=axes[0])
        axes[0].set_ylabel('Observed')

        # Tendência
        decomposition.trend.plot(ax=axes[1])
        axes[1].set_ylabel('Trend')

        # Sazonalidade
        decomposition.seasonal.plot(ax=axes[2])
        axes[2].set_ylabel('Seasonal')

        # Resíduos
        decomposition.resid.plot(ax=axes[3])
        axes[3].set_ylabel('Residual')

        plt.tight_layout()
        return fig

    st.pyplot(seasonal_decompose_plot(df))

    st.markdown('''
    ---            
        
    ## Teste de Estacionaridade (Adfuller)
                
    A estacionariedade é uma premissa para o modelo ARIMA. O teste ADF ajuda a determinar se a série temporal de preços do petróleo é estacionária ou não. Se a série não for estacionária, pode ser necessário aplicar transformações nos dados, como diferenciação, para torná-la estacionária antes da modelagem
                
    Foi realizado o teste sem estacionaridade e identificado que a base de Preços não era estacionária. 
    
    Aplicando adfuller foi verificado que a 1ª diferenciação foi suficiente para tornar a base estacionária.            
    
    ### Adfuller (1º teste)
                
    ---
    
    ''')

    df_diferenciada = df['y'].diff(1)
    df_diferenciada_2 = pd.DataFrame(df_diferenciada).dropna()
    teste_estacionario = adfuller(df_diferenciada_2['y'])

    fig2, ax5 = plt.subplots()
    plt.title('Base de Preços Estacionária')
    ax5.plot(df_diferenciada)


    coluna3, coluna4 = st.columns(2)

    with coluna3:
        #Para criar cartões (métricas) deve-se executar o código abaixo:
        st.pyplot(fig2)

    with coluna4:
        st.metric('ADF Statistic:',round(teste_estacionario[0],2))
        st.metric('p-value:',teste_estacionario[1])
        st.markdown('Critical Values: ')
        st.markdown(f"#### {teste_estacionario[4]}")
    
    st.markdown('''
    
    Foi possível notar que a ADF Statistic resultou em um valor bem negativo de -22.75 e este é um indicador da presença de raízes unitárias na série temporal. Quanto mais negativo é o valor da estatística do teste, mais forte é a evidência contra a presença de raízes unitárias, o que sugere que a série é estacionária.
                
    O p-value é 0.0, o que significa que a probabilidade de obter um valor de estatística de teste tão extremo quanto -22.75 é muito baixa. Isso significa que podemos rejeitar a hipótese nula de que a série temporal possui uma raiz unitária e concluir que a série agora é estacionária, após a 1ª diferenciação.
                
    ## Teste ACF e PACF
                
    Por fim, avaliamos os gráficos ACF e PACF para identificar os parâmetros do modelo ARIMA.

    Do teste ACF, podemos ver que o primeiro valor significativo é o lag 2, enquanto do teste PACF podemos ver que o lag significativo será o lag 3.
      
    ''')

    coluna3, coluna4 = st.columns(2)

    with coluna3:
        image_acf = Image.open('src/img/ACF.png')
        st.image(image_acf)

    with coluna4:
        image_pacf = Image.open('src/img/PACF.png')
        st.image(image_pacf)

    st.markdown('''
    
                
    ## Conclusão da Análise
                
    Após análise da sazonalidade foi possível identificar que a série temporal possui uma sazonalidade anual, com picos de alta no inicio do ano e baixa no final do ano. 
                
    O parâmetro ideal para o Modelo Arima será composto por (3,1,2) e sazonalidade de 365 dias.
                
    **Agora verifique nas abas no inicio da página como foi a avaliação dos modelos *NAIVE* e *ARIMA***.
                
      
    ''')

    




with aba2:
    st.markdown('''
    # Modelagem de Previsão de Preços (BRENT) - Modelo Baseline NAIVE 

    ---

    Nessa sessão vamos trabalhar o modelo Naive baseline que utiliza uma heurística básica, como a persistência do último valor observado, para gerar previsões diretas. 
    
    Embora sua simplicidade possa parecer limitante o modelo Naive baseline serve como um ponto de referência crucial para avaliar o desempenho de modelos mais complexos, como o ARIMA. 

    ~~~python
                
    valor_treino = int(0.8 * len(df))
    df_treino, df_teste = df[:valor_treino], df[valor_treino:]
                
    #---------DEFINIR VARIAVEIS--------
    prazo = 1
    modelo = 'Naive'  #nome da coluna que é output do modelo

    #--------------------------------

    historico = df_treino
    historico_das_previsoes = pd.DataFrame(columns=['unique_id', 'ds', modelo])
    historico_das_previsoes.set_index('unique_id', inplace=True)
    historico_das_previsoes['ds'] = pd.to_datetime(historico_das_previsoes['ds'], format='%Y-%m-%d')

    for index in range(0, len(df_teste), prazo):
        row = df_teste.iloc[index]
        #Definir modelo
        model_naive2 = StatsForecast(models=[Naive()], freq='D', n_jobs=-1)
        #Fit
        model_naive2.fit(historico)
        #Predict
        forecast_df = model_naive2.predict(h=prazo)
        #Andando {prazo} dia(s) no 'historico' ou 'df_treino'
        novo_preco = df_teste.iloc[index: index + prazo]
        historico = pd.concat([historico, novo_preco], ignore_index=True)
        historico_das_previsoes = pd.concat([historico_das_previsoes, forecast_df], ignore_index=True)

    #Joiner
    joiner = df_teste.merge(historico_das_previsoes, on='ds', how='left')

    avaliar_resultado(joiner,modelo)

    ~~~


    ---
                
    Para a análise do modelo Naive baseline foi utilizado o modelo Naive com o parâmetro móveis de 1, 5, 10 e 30 dias.
                
    Com a mudança do número de dias móveis foi possível identificar que o modelo Naive baseline com 1 dia móvel apresentou os melhores resultados de MAE, MAPE, RMSE e R2.

    Verifique abaixo como foi a avaliação do modelo Naive baseline para os diferentes parâmetros móveis:                            
    ''')

    filtro_prazo = st.selectbox('Prazo', [1, 5, 10, 30], index=0)

    #---------DEFINIR VARIAVEIS--------
    prazo = filtro_prazo
    modelo = 'Naive'  #nome da coluna que é output do modelo

    #--------------------------------


    df_treino = df_treino.reset_index()

    historico = df_treino
    historico_das_previsoes = pd.DataFrame(columns=['unique_id', 'ds', modelo])
    historico_das_previsoes.set_index('unique_id', inplace=True)
    historico_das_previsoes['ds'] = pd.to_datetime(historico_das_previsoes['ds'], format='%Y-%m-%d')

    for index in range(0, len(df_teste), prazo):
        row = df_teste.iloc[index]
        #Definir modelo
        model_naive = StatsForecast(models=[Naive()], freq='D', n_jobs=-1)
        #Fit
        model_naive.fit(historico)
        #Predict
        forecast_df = model_naive.predict(h=prazo)
        #Andando {prazo} dia(s) no 'historico' ou 'df_treino'
        novo_preco = df_teste.iloc[index: index + prazo]
        historico = pd.concat([historico, novo_preco], ignore_index=True)
        historico = historico[['ds', 'y', 'unique_id']]
        historico_das_previsoes = pd.concat([historico_das_previsoes, forecast_df], ignore_index=True)
    
    #Joiner
    joiner = df_teste.merge(historico_das_previsoes, on='ds', how='left')
 
    mae, mape, rmse, r2 = avaliar_resultado(joiner,modelo)

    coluna1,coluna2,coluna3,coluna4 = st.columns(4)
   

    with coluna1:
        st.metric('MAE:',round(mae,2))
    with coluna2:
        st.metric('MAPE:',round(mape,2))
    with coluna3:
        st.metric('RMSE:',round(rmse,2))
    with coluna4:
        st.metric('R2:',round(r2,2))

    st.markdown('''

    ### Modelo Naive com forecasting de 1 dia:
                
    ''')

    image_naive = Image.open(r'src/img/Naive1dia.png')
    st.image(image_naive)
    
    st.markdown('''

    ### Modelo Naive com forecasting de 30 dias:
                
    ''')

    image_naive = Image.open(r'src/img/Naive30dias.png')
    st.image(image_naive)

    st.markdown('''

    O modelo com previsão de 1 dia se saiu muito bem como baseline, com Mean Absolute Error (MAE) baixo de 1.12, Mean Absolute Percentage Error (MAPE) de 0.01%, Root Mean Squared Error de 1.92 e R2 de 0.98, o que sugere que o modelo Baseline Naive explica aproximadamente 98% da variabilidade dos dados, o que é um ajuste muito bom.

    Essas medidas estatísticas de erro são fundamentais para avaliar o desempenho do modelo Baseline Naive e compará-lo com outros modelos de previsão. 
    
    ''')

with aba3:
    st.markdown('''
    # Modelagem de Previsão de Preços (BRENT) - Modelo ARIMA
            
    ---

    O modelo ARIMA (Autoregressive Integrated Moving Average) é uma ferramenta poderosa e amplamente utilizada na análise e previsão de séries temporais devido a sua capacidade de capturar tanto padrões de autocorrelação quanto tendências temporais, o ARIMA oferece uma abordagem robusta para modelar e prever dados temporais complexos. Foram utilizados os parâmetros (3,1,2) para o modelo, de acordo com informações vistas na etapa de Avaliação de Dados.
                
    ~~~python
    #---------DEFINIR VARIAVEIS--------
    prazo = 1
    modelo = 'ARIMA'  #nome da coluna que é output do modelo

    #--------------------------------

    historico = df_treino
    historico_das_previsoes = pd.DataFrame(columns=['unique_id', 'ds', modelo])
    historico_das_previsoes.set_index('unique_id', inplace=True)
    historico_das_previsoes['ds'] = pd.to_datetime(historico_das_previsoes['ds'], format='%Y-%m-%d')



    for index in range(0, len(df_teste), prazo):
        row = df_teste.iloc[index]
        #Definir modelo
        model_arima3 = StatsForecast(models=[ARIMA(order=(3,1,2),season_length=365)], freq='D', n_jobs=-1)
        #Fit
        model_arima3.fit(historico)
        #Predict
        forecast_df = model_arima3.predict(h=prazo, level=[90])
        #Andando {prazo} dia(s) no 'historico' ou 'df_treino'
        novo_preco = df_teste.iloc[index: index + prazo]
        historico = pd.concat([historico, novo_preco], ignore_index=True)
        historico_das_previsoes = pd.concat([historico_das_previsoes, forecast_df], ignore_index=True)

    #Joiner
    joiner = df_teste.merge(historico_das_previsoes, on='ds', how='left')

    avaliar_resultado(joiner,modelo)
    ~~~
                
    ---''')

    st.markdown('''

    ### Modelo ARIMA com forecasting de 1 dia:
                
    ''')

    coluna1,coluna2,coluna3,coluna4 = st.columns(4)

    with coluna1:
        st.metric('MAE:',round(1.29,2))
    with coluna2:
        st.metric('MAPE:',round(0.01,2))
    with coluna3:
        st.metric('RMSE:',round(2.04,2))
    with coluna4:
        st.metric('R2:',round(0.98,2))

    image_arima = Image.open(r'src/img/Arima1dia312.png')
    st.image(image_arima)

    st.markdown('''

    ### Modelo ARIMA com forecasting de 30 dias:
                
    ''')
        
    coluna1,coluna2,coluna3,coluna4 = st.columns(4)

    with coluna1:
        st.metric('MAE:',round(4.95,2))
    with coluna2:
        st.metric('MAPE:',round(0.055,2))
    with coluna3:
        st.metric('RMSE:',round(6.85,2))
    with coluna4:
        st.metric('R2:',round(0.78,2))

    image_arima = Image.open(r'src/img/Arima30dias312.png')
    st.image(image_arima)

    

    

