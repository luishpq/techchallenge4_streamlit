from libraries import *


########## CONFIGURAÇÃO ##############
st.set_page_config(page_icon=":chart:", layout='centered', page_title="Conclusão")

image = Image.open('src/img/industry-oil-gas_2.jpg')
st.image(image)

with open("src/css/style.css") as i:
        st.markdown(f'<style>{i.read()}</style>', unsafe_allow_html=True)
       
st.markdown('''
# Análise e Forecasting do Preço do Barril de Petróleo (BRENT)

---
            
## Conclusão
            
1)	O preço do barril de petróleo é volátil, porém o seu preço muitas vezes está além do relacionamento entre oferta e demanda. Segundo PUYANA (2021) as mudanças geradas pelo mercado futuro podem ser inclusive mais relevantes que oferta/demanda, uma vez que as crises geopolíticas e econômicas refletem mais rapidamente nesse mercado financeiro. Sendo fundamental acompanhá-lo para melhor forecasting de preços do barril de petróleo.
2)	É possível notar uma grande queda nos preços durante a crise financeira de 2008/2009, efeitos geopolíticos gerados pelo crescimento da China e crise diplomática entre Irã e Arábia Saudita em 2015/2016 e o impacto gerado pela covid-19 em 2020, demonstrando como acompanhar esses eventos, bem como outros relacionados aos maiores produtores/consumidores de petróleo do mundo podem ser fundamentais para melhor forecasting de preço.
3)	O Brasil vem ganhando notoriedade como maior produtor de petróleo da América do Sul, posto que já foi da Venezuela, país este que tem sofrido nos últimos anos com sansões americanas e escândalos de corrupção que degradaram a maior estatal petroleira do país, a PDVSA.
4)	Nos modelos de forecasting foi possível concluir que o modelo baseline Naive se saiu melhor que o modelo ARIMA nos parâmetros de erro escolhidos. Esse fato é positivo dado que o modelo Naive exige pouco processamento computacional, porém o modelo ARIMA pode ser testado com outros parâmetros e afim de atingir um melhor forecasting principalmente para datas mais prolongadas.

## Referências
            
- ESTADÃO. Venezuela: apesar de nova licença, petróleo pode demorar para chegar aos mercados. UOL Economia. 2022. Disponível em: https://economia.uol.com.br/noticias/estadao-conteudo/2022/11/27/venezuela-apesar-de-nova-licenca-petroleo-pode-demorar-para-chegar-aos-mercados.htm#:~:text=A%20produ%C3%A7%C3%A3o%20de%20petr%C3%B3leo%20da, acesso em 18 jan. 2024.
- IPEADATA. Preço do Barril do Petróleo Bruno Brent. 2023. Disponível em: http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view, acesso em 18 jan. 2024.
- OUR WORLD IN DATA. 2022. Energy production & consumption. Disponível em: https://ourworldindata.org/energy-production-consumption, acesso em 18 jan. 2024.
- PUYANA, A., PEÑA, I., & MANRIQUE, G, L.. 2021. Factores relevantes de la inestabilidad del mercado petrolero. Revista de Economía Institucional, 23(45), 227-256.
- VEJA. Da liderança ao colapso: como a indústria petroleira da Venezuela ruiu. 2019. Disponível em: https://veja.abril.com.br/economia/da-lideranca-ao-colapso-como-a-industria-petroleira-da-venezuela-ruiu, acesso em 18 jan. 2024.

            
''')