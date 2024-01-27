#Importando libraries

from libraries import *

########## CONFIGURAÇÃO ##############
st.set_page_config(layout='wide')

########## TÍTULO ##############
st.title('DASHBOARD PETRÓLEO: TECH CHALLENGE 4 (FIAP/ALURA)')

########## LEITURA DO BANCO DE DADOS ##############
df = pd.read_csv("db_petroleo.csv",sep=";").set_index('ds')
# Converter o índice para o tipo de data
df.index = pd.to_datetime(df.index)

# Substituir vírgulas por pontos e converter para float
df['y'] = df['y'].str.replace(',', '.').astype(float)



# Treino x Teste
valor_treino = int(0.8 * len(df))
df_treino, df_teste = df[:valor_treino], df[valor_treino:]

#####FUNÇÃO PARA AVALIAR ERRO DO MODELO

def avaliar_resultado(joiner_db,modelo_teste):

    mae = mean_absolute_error(joiner_db['y'],joiner_db[modelo_teste])
    mape = mean_absolute_percentage_error(joiner_db['y'],joiner_db[modelo_teste])
    rmse = np.sqrt(mean_squared_error(joiner_db['y'],joiner_db[modelo_teste]))
    r2 = r2_score(joiner_db['y'],joiner_db[modelo_teste])

    print(f'mae - naive: {mae}')
    print(f'mape - naive: {mape}')
    print(f'rmse - naive: {rmse}')
    print(f'r2 - naive: {r2}')


######### GRÁFICOS #############


##### GRÁFICO SEASONAL DECOMPOSE ###########
fig2, (ax1,ax2,ax3,ax4) = plt.subplots(4,1,figsize = (15,8))

resultados = seasonal_decompose(df['y'], model='additive', period=365)


#Dados reais
resultados.observed.plot(ax=ax1)
#Tendência
resultados.trend.plot(ax=ax2)
#Sazonalidade (recorrência)
resultados.seasonal.plot(ax=ax3)
#Resíduos (valores que não se explicam facilmente)
resultados.resid.plot(ax=ax4)



# Redefinindo o índice para transformar 'ds' de volta em uma coluna
df.reset_index(inplace=True)

valor_treino = int(0.8 * len(df))
df_treino, df_teste = df[:valor_treino], df[valor_treino:]

historico = df_treino
historico_das_previsoes = pd.DataFrame(columns=['unique_id', 'ds', 'Naive'])
historico_das_previsoes.set_index('unique_id', inplace=True)
historico_das_previsoes['ds'] = pd.to_datetime(historico_das_previsoes['ds'], format='%Y-%m-%d')

for index, row in df_teste.iterrows():
    #Definir modelo
    model_naive = StatsForecast(models=[Naive()], freq='D', n_jobs=-1)
    #Fit
    model_naive.fit(historico)
    #Predict
    forecast_df = model_naive.predict(h=1)
    #Andando 1 dia no 'historico' ou 'df_treino'
    novo_preco = pd.DataFrame([row], columns=df_teste.columns)
    historico = pd.concat([historico, novo_preco], ignore_index=True)
    historico_das_previsoes = pd.concat([historico_das_previsoes, forecast_df], ignore_index=True)

#Joiner
joiner_naive = df_teste.merge(historico_das_previsoes, on='ds', how='left')

# Substituir NaN pelo numero anterior
joiner_naive['Naive'] = joiner_naive['Naive'].fillna(method='ffill')


######MODELO ARIMA

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
    model_naive = StatsForecast(models=[ARIMA(order=(1,1,1),season_length=365)], freq='D', n_jobs=-1)
    #Fit
    model_naive.fit(historico)
    #Predict
    forecast_df = model_naive.predict(h=prazo)
    #Andando {prazo} dia(s) no 'historico' ou 'df_treino'
    novo_preco = df_teste.iloc[index: index + prazo]
    historico = pd.concat([historico, novo_preco], ignore_index=True)
    historico_das_previsoes = pd.concat([historico_das_previsoes, forecast_df], ignore_index=True)

#Joiner
joiner = df_teste.merge(historico_das_previsoes, on='ds', how='left')

avaliar_resultado(joiner,modelo)


##### GRÁFICO NAIVE

fig3, ax5 = plt.subplots(figsize=(12, 8))

ax5.plot(joiner_naive['ds'],joiner_naive['y'])
ax5.plot(joiner_naive['ds'],joiner_naive['Naive'])


##########ABAS DO STREAMLIT ###################
aba1, aba2, aba3 = st.tabs(['Análise Primária', 'Naive', 'ARIMA'])

with aba1:
    st.pyplot(fig2)

with aba2:
    st.pyplot(fig3)
    mae = mean_absolute_error(joiner_naive['y'],joiner_naive['Naive'])
    mape = mean_absolute_percentage_error(joiner_naive['y'],joiner_naive['Naive'])
    rmse = np.sqrt(mean_squared_error(joiner_naive['y'],joiner_naive['Naive']))
    r2 = r2_score(joiner_naive['y'],joiner_naive['Naive'])

    #st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas')

    st.markdown(f'MAE - naive: {mae}')
    st.markdown(f'MAPE - naive: {mape}')
    st.markdown(f'RMSE - naive: {rmse}')
    st.markdown(f'R2 - naive: {r2}')