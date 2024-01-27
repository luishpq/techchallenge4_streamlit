#Importando libraries

from libraries import *

########## CONFIGURAÇÃO ##############
st.set_page_config(page_icon=":house:", layout='centered', page_title="Início")

image = Image.open('src\img\industry-oil-gas_2.jpg')
st.image(image)

with open("src/css/style.css") as i:
        st.markdown(f'<style>{i.read()}</style>', unsafe_allow_html=True)

########## TÍTULO ##############
        
st.markdown('''
# Dashboard: Forecasting do Preço de Petróleo
            
---

O preço do petróleo se tornou um termômetro econômico global, cada oscilação no valor por barril reverbera em cadeias de suprimentos, orçamentos familiares e até mesmo na política internacional. Para compreender a dinâmica por trás dessas flutuações, é essencial mergulhar nas raízes históricas e nos fatores determinantes que moldam esse mercado volátil. 
            
Mudanças geopolítica, crises econômicas e demanda global por energia, são esses elementos que compõem o complexo cenário que define o valor do combustível que alimenta a máquina da civilização moderna. 
            
Nesta jornada de análise e descoberta, exploraremos como esses fatores se entrelaçam e se manifestam ao longo dos anos, delineando os rumos do mercado petrolífero e delineando os contornos do nosso mundo contemporâneo.

---
''')
            
######### SELECT BOX & FILTROS ############
#Criando o select box no Streamlit
st.sidebar.title('Filtros')


todos_anos = st.sidebar.checkbox('Dados de todo o periodo', value = True)


if todos_anos:
    ano_min, ano_max = ('1990','2023')
else:
    ano_min, ano_max = st.sidebar.slider('Ano', 1990, 2024, (1990, 2024))

########## LEITURA DO BANCO DE DADOS ##############
df = pd.read_csv("db_petroleo.csv",sep=";").set_index('ds')
# Converter o índice para o tipo de data
df.index = pd.to_datetime(df.index)

# Substituir vírgulas por pontos e converter para float
df['y'] = df['y'].str.replace(',', '.').astype(float)

# Filtrar com base em datas maiores que '2006-01-01'
filtered_df = df.loc[(df.index >= f"{ano_min}-01-01") & (df.index <= f"{ano_max}-12-31")]




########## TABELAS ##############

#TIME SERIES PREÇO DO PETRÓLEO

fig1, ax1 = plt.subplots(figsize=(12, 8))


ax1.plot(filtered_df.index, filtered_df['y'])
ax1.set_xlabel('Ano')
ax1.set_ylabel('USD')
ax1.set_title('Gráfico 1: Preço Petróleo Bruto')


st.pyplot(fig1)
st.dataframe(filtered_df)
