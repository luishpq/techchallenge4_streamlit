#Importando libraries

from libraries import *

########## CONFIGURAÇÃO ##############
st.set_page_config(page_icon=":chart:", layout='centered', page_title="Início")

image = Image.open('src\img\industry-oil-gas_2.jpg')
st.image(image)

with open("src/css/style.css") as i:
        st.markdown(f'<style>{i.read()}</style>', unsafe_allow_html=True)

########## TÍTULO ##############

        
st.markdown('''
# Análise e Forecasting do Preço do Barril de Petróleo (BRENT)

---
                        
Por: Luis Henrique Queiroz
            
Projeto: Pós Tech Alura/Fiap - Tech Challenge Fase 4
            
Data: 01/2024

          
---

O preço do petróleo se tornou um termômetro econômico global, a oscilação no valor por barril impacta orçamentos familiares e até mesmo a política internacional. Para compreender a dinâmica por trás dessas flutuações, é necessário entender quais são os fatores determinantes que impactam esse mercado volátil. 
            
Mudanças geopolítica, crises econômicas e demanda global por energia, são esses elementos que compõem o complexo cenário que define o valor dessa commoditie. 
            
Neste Dashboard exploraremos como esses fatores se entrelaçam e se manifestam ao longo dos anos, delineando os rumos do mercado petrolífero, bem como analisaremos 2 modelos de Data Analytics para realizar a previsão do preço do petróleo: Naiva e ARIMA.

---


## Metodologia

Para criação dos modelos foram utilizadas as ferramentas: Python e StatsForecast, bem como outras bibliotecas de Data Analytics. A metodologia incluiu:
            
1) Captura dos dados em: https://www.eia.gov/ (Preço do BRENT) e https://ourworldindata.org/energy-production-consumption (Oferta e Demanda de Petróleo).
2) Analise introdutória: verificação de tendências (Seasonal Decompose), testes de estacionaridade (adfuller).
3) Base Treino x Teste: Separação de 80% da base para treino. Segregação do preço de fechamento do petróleo para forecasting.
4) Treinar os Dados: Modelos avaliados: Naive e Arima.
5) Avaliar desempenho dos modelos: Avaliação do MAE, MAPE, RMSE e R2.        
            
## Captura dos Dados
            
Os dados foram capturados entre 01/1990 e 01/2024.

Ajuste a régua abaixo para ver a variação dos preços de Petróleo em diferentes intervalos de tempo:      
''')
            
######### SELECT BOX & FILTROS ############



#todos_anos = st.sidebar.checkbox('Dados de todo o periodo', value = True)


#if todos_anos:
#    ano_min, ano_max = ('1990','2023')
#else:
#    ano_min, ano_max = st.sidebar.slider('Ano', 1990, 2024, (1990, 2024))

########## LEITURA DO BANCO DE DADOS ##############
df = pd.read_csv("db_petroleo.csv",sep=";").set_index('ds')

# Converter o índice para o tipo de data
df.index = pd.to_datetime(df.index)



df_oil = pd.read_excel('Consolidated-Dataset-Narrow-format.xlsx')
#Correção base de dados

cod_paises = pd.read_csv('countries_codes_and_coordinates.csv')
cod_paises['Lat'] = cod_paises['Latitude (average)'].str.replace('"', '').str.replace(',', '.')
cod_paises['Lat'] = pd.to_numeric(cod_paises['Lat'], errors='coerce')
cod_paises['Lon'] = cod_paises['Longitude (average)'].str.replace('"', '').str.replace(',', '.')
cod_paises['Lon'] = pd.to_numeric(cod_paises['Lon'], errors='coerce')

# Substituir vírgulas por pontos e converter para float
df['y'] = df['y'].str.replace(',', '.').astype(float)


# Merge baseado na coluna 'Country'
df_2 = pd.merge(df_oil, cod_paises[['Country', 'Lat', 'Lon']], on='Country', how='left')

# Colunas desejadas
colunas_desejadas = ['Country', 'Year', 'Region', 'SubRegion', 'Var', 'Value', 'Lat', 'Lon']

# Filtrar apenas as colunas desejadas
df_2 = df_2[colunas_desejadas]

# 1. Filtrar o DataFrame por consumo/produção
grouped_df_mundo_oilcons = df_2[(df_2['Var'] == 'oilcons_mt')].groupby(['Year']).agg({'Value': 'sum'}).reset_index().sort_values(by='Year')
grouped_df_mundo_oilprod = df_2[(df_2['Var'] == 'oilprod_mt')].groupby(['Year']).agg({'Value': 'sum'}).reset_index().sort_values(by='Year')
grouped_df_mundo_oilcons['Year'] = pd.to_datetime(grouped_df_mundo_oilcons['Year'], format='%Y')
grouped_df_mundo_oilprod['Year'] = pd.to_datetime(grouped_df_mundo_oilprod['Year'], format='%Y')

# 1. Filtrar o DataFrame para uma única região
grouped_df = df_2[(df_2['Var'] == 'oilprod_mt')].groupby(['Region', 'Year']).agg({'Value': 'sum'}).reset_index()

# Dicionário de mapeamento
mapeamento = {
    'oilcons_mt': 'Demanda de Petróleo',
    'oilprod_mt' : 'Produção de Petróleo'
    # Adicione mais mapeamentos conforme necessário
}

# Substituir os valores na coluna 'Var' usando o mapeamento
df_2['Var'] = df_2['Var'].map(mapeamento)

######### FILTROS ##########



########## TABELAS ##############

#TIME SERIES PREÇO DO PETRÓLEO

ano_min, ano_max = st.slider('Ano', 1990, 2024, (1990, 2024))

# Filtrar com base em datas maiores que 'aaaa-01-01'
filtered_df = df.loc[(df.index >= f"{ano_min}-01-01") & (df.index <= f"{ano_max}-12-31")]

fig1, ax1 = plt.subplots(figsize=(12, 8))


ax1.plot(filtered_df.index, filtered_df['y'])
ax1.set_xlabel('Ano')
ax1.set_ylabel('USD')
ax1.set_title('Gráfico 1: Preço Petróleo Bruto')


st.pyplot(fig1)

st.markdown('''

## Análise de Oferta e Demanda
            
PUYANA (2021) cita elementos políticos, militares, tecnológicos e climáticos como fatores que influenciam a oferta e demanda de petróleo no mundo.

Além destes, porém, um dos principais fatores que mais impactam a variação de preços é segundo PUYANA (2021) o relacionamento desse mercado com o mercado financiero, principalmente o mercado futuro. Isso ocorre pois nesse mercado é muito mais simples a transação de barris de petróleo, o que facilita a especulação e arbitragem de preços, impactando assim o preço de forma mais imediata a qualquer possível impacto no processo produtivo, seja a possível iminência de uma guerra, seja uma informação ainda não confirmada de um encontro da OPEP (Organização dos Países Exploradores de Petróleo).

No mesmo artigo os autores ressaltam que essa variável de "mercado financeiro" passa a atenuar a influência de oferta e demanda para esse mercado. 

É possível confirmar essa informação anterior pelo gráfico abaixo, com a informação de Ofera/Demanda e Preço do Barril de Petróleo. Enquanto a Oferta/Demanda estão correlacionados, o preço por si só varia bastante, apesar de ainda estar diretamente relacionado com a oferta/demana em situação de maior estresse, como 2008 (crise financeira nos EUA), 2016 (crise geopolítica) e 2020 (crise da covid-19)                  
''')

oferta_select = st.checkbox('Oferta de Petróleo', value = True)
demanda_select = st.checkbox('Demanda de Petróleo', value = True)

fig2, ax2 = plt.subplots()

if oferta_select:
    ax2.plot(grouped_df_mundo_oilcons['Year'], grouped_df_mundo_oilcons['Value'], label='Demanda')
if demanda_select:
    ax2.plot(grouped_df_mundo_oilprod['Year'], grouped_df_mundo_oilprod['Value'], label='Oferta')

# Criar eixos secundários para os dados de preço do petróleo
ax3 = ax2.twinx()
ax3.plot(df.index, df['y'], color='green', label='Preço do Petróleo')

# Adicionar rótulos e título
plt.xlabel('Ano')
ax2.set_ylabel('Bilhões de Toneladas')
ax3.set_ylabel('Preço do Petróleo (BRENT)')
plt.title('Consumo de Petróleo (Mundo)')
plt.legend()  # Adicionar legenda

st.pyplot(fig2)

st.markdown('''
            
No entanto, além da análise macro também é importante analisar individualmente cada país e território. Uma vez que a consultoria pode ter um mercado específico como alvo.

Para isso, é possível analisar a oferta e demanda de cada país, bem como a participação de cada um no mercado mundial. 
            
**Basta selecionar os países desejados no filtro abaixo:**
''')

#selecionar_tipo_ofertademanda = st.selectbox('Região', regioes)

coluna1, coluna2 = st.columns(2)

with coluna1:
#Para criar cartões (métricas) deve-se executar o código abaixo:
    filtro_paises = st.multiselect('Países', df_2['Country'].unique(),max_selections=4, default=["Brazil", "Venezuela", "Total S. & Cent. America"])
with coluna2:
    filtro_var = [st.selectbox('Oferta/Demanda', df_2['Var'].unique(), index=0)]



# Aplicar filtros
if filtro_paises:
    df_3 = df_2[df_2['Country'].isin(filtro_paises)]
else:
    df_3 = df_2

if filtro_var:
    df_3 = df_3[df_3['Var'].isin(filtro_var)]

ano_min_int = int(ano_min)
ano_max_int = int(ano_max)
df_3 = df_3[(df_3['Year'] >= ano_min) & (df_3['Year'] <= ano_max)]

grouped_df = df_3.groupby(['Year']).agg({'Value': 'sum'}).reset_index()
grouped_df_paises = df_3.groupby(['Year','Country']).agg({'Value': 'sum'}).reset_index()

fig3, ax4 = plt.subplots()
ax4.bar(grouped_df['Year'], grouped_df['Value'])

fig4, ax5 = plt.subplots()

for country, country_data in grouped_df_paises.groupby('Country'):
     sorted_data = country_data.sort_values(by='Year')
     ax5.plot(sorted_data['Year'], sorted_data['Value'], label=country)

ax5.set_xticklabels(ax5.get_xticklabels(), rotation=45)
plt.xlabel('Ano')
plt.ylabel('Milhões de Toneladas')
plt.title(f'{str(filtro_var[0])} Por País em Milhões de Toneladas Por Ano')
plt.legend()


grouped__paises_value = df_3.groupby(['Country']).agg({'Value': 'sum'}).sort_values('Value', ascending=False).head().reset_index()


fig5, ax6 = plt.subplots()
ax6.bar(grouped__paises_value['Country'], grouped__paises_value['Value'])


coluna3, coluna4 = st.columns(2)

with coluna3:
#Para criar cartões (métricas) deve-se executar o código abaixo:
    st.pyplot(fig4)

with coluna4:
    st.pyplot(fig5)
    st.dataframe(grouped__paises_value)

coluna3, coluna4 = st.columns(2)

with coluna3:
    st.markdown('''
                
    ### Top 10 Países *Consumidores* de Petróleo (Milhões de Toneladas)            
                
    | País                | Valor (apróx.)      |
    |---------------------|--------------|
    | US                  | 45538 |
    | China               | 13669 |
    | Japan               | 12737 |
    | Germany             | 7256  |
    | USSR                | 6377  |
    | Russian Federation  | 6246  |
    | India               | 5323  |
    | France              | 5163  |
    | Canada              | 5151  |
    | Italy               | 4822  |
    
    ''')


with coluna4:
    st.markdown('''
                
    ### Top 10 Países *Produtores* de Petróleo (Milhões de Toneladas)            
                
    | País                | Valor (apróx.)       |
    |---------------------|--------------|
    | US                  | 26560 |
    | Saudi Arabia        | 23421 |
    | Russian Federation  | 17820 |
    | Iran                | 10553 |
    | USSR                | 9218  |
    | Venezuela           | 7934  |
    | China               | 7863  |
    | Canada              | 7345  |
    | Mexico              | 6798  |
    | Kuwait              | 6474  |
    
    ''')


#st.dataframe(df_3)
#st.dataframe(grouped_df)
#st.pyplot(fig3)




