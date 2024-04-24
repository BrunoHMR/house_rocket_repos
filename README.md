## **Projeto de Insights Para a Compra e Venda de Imóveis**

------------------------------------------------------------------------------------------------------------------------------------------

**1. Descrição do problema de negócio:**

A House Rocket é uma empresa fictícia que trabalha com a compra e venda de imóveis. A equipe de negócio da empresa precisa decidir quais são as melhores opções de imóveis para compra. Devido a grande quantidade de imóveis no portfólio e da quantidade de atributos que cada imóvel possui, é demandada uma análise mais criteriosa e técnica. Porém, realizar o trabalho manualmente é muito demorado e pode levar a decisões precipitadas. Deste modo, é necessária a realização de um projeto para avaliar quais são as melhores estratégias para que a empresa consiga escolher bons imóveis para a compra, aumentando o seu faturamento.

------------------------------------------------------------------------------------------------------------------------------------------

**2. Questões de negócio:**

2.1. Quais são os imóveis que a House Rocket deveria comprar?

2.2. Uma vez comprados os imóveis, qual o melhor momento para vendê-los e por qual preço?

------------------------------------------------------------------------------------------------------------------------------------------

**3. Base de dados e descrição dos atributos:**

3.1. Dados disponíveis em: https://www.kaggle.com/harlfoxem/housesalesprediction/discussion/207885.

3.2. Descrição dos atributos (colunas):

- 'id': código do imóvel.
- 'date': data em que o imóvel foi vendido.
- 'price': preço de venda do imóvel.
- 'bedrooms': quantidade de quartos.
- 'bathrooms': quantidade de banheiros.
- 'sqft_living': tamanho interno do imóvel em ft.
- 'sqft_lot': tamanho do lote em ft.
- 'floors': quantidade de andares.
- 'waterfront': se possui vista para o mar (1) ou não (0).
- 'view': qualidade da vista (0 até 4).
- 'condition': condição do imóvel (1 até 5).
- 'grade': qualidade do design e da construção (1 até 13).
- 'sqft_above': tamanho do andar superior (ou do único andar).
- 'sqft_basement': tamanho do andar inferior (porão).
- 'yr_built': ano de construção do imóvel.
- 'yr_renovated': ano de reforma do imóvel (se reformado).
- 'zipcode': localidade.
- 'lat': latitude.
- 'long': longitude.
- 'sqft_living15': tamanho interno do imóvel em ft dos 15 vizinhos mais próximos.
- 'sqft_lot15': tamanho do lote em ft dos 15 vizinhos mais próximos.

Total: 19 atributos.

------------------------------------------------------------------------------------------------------------------------------------------

**4. Premissas de negócio:**

4.1. Foram removidos os imóveis com 'ids' duplicados, sendo mantidos apenas os 'ids' com a coluna 'date' mais recente.

4.2. Foram criados novos atributos para a análise:
- 'condition_good': indica se o imóvel está em boas condições ('condition' > 3) ou em más condições ('condition' <= 3).
- 'water_view': indica se o imóvel possui vista para o mar ('waterfront' == 1) ou não ('waterfront' == 0).
- 'renovated': indica se o imóvel é renovado ('yr_renovated' != 0) ou não renovado ('yr_renovated' == 0).
- 'year': retorna o ano do imóvel de acordo com a coluna 'date'.
- 'month': retorna o mês do imóvel de acordo com a coluna 'date'.
- 'year_month': retorna o ano e o mês do imóvel de acordo com a coluna 'date'.
- 'season': determina a sazonalidade do imóvel de acordo com os meses, sendo elas: dez-fev, mar-mai, jun-ago e set-nov.

------------------------------------------------------------------------------------------------------------------------------------------

**5. Planejamento da solução:**

5.1 Ferramentas utilizadas:
- Python 3.10.8;
- PyCharm Community;
- Jupyter Notebook;
- Streamlit.

5.2 Produto final:
- Relatório 'purchase_recommendations.csv' com sugestões de compra de imóveis;
- Relatório 'selling_recommendations.csv' com sugestões de preço de venda de imóveis e momento de venda de imóveis;
- Aplicação 'house_rocket_app.py' utilizando o framework Streamlit para visualização e validação de hipóteses e para que o time de negócio possa realizar a sua própria análise. Disponível em: https://brunohmr-house-rocket-repos-house-rocket-app-3rq183.streamlit.app/.

5.3 Planejamento para a criação do relatório de sugestão de compra dos imóveis:

- Foram coletados os dados e aplicadas as premissas de negócio.
- Os imóveis foram agrupados de acordo com a sua localidade por meio da coluna 'zipcode'.
- Foram determinadas as medianas dos preços para cada localidade.
- Foram eliminados das opções de compra os imóveis em más condições e sem vista para o mar.
- Foram escolhidos como opções de compra os imóveis que possuem um preço menor que a mediana referente à sua localidade.

5.4 Planejamento para a criação do relatório de sugestão de venda dos imóveis:

- Os imóveis foram agrupados de acordo com a sua localidade e sazonalidade.
- Foram determinadas as medianas dos preços para cada localidade e sazonalidade.
- Foram criados dois novos atributos: 'selling_price' e 'selling_moment'.
- 'selling_price': representa o preço pelo qual os imóveis devem ser vendidos. Imóveis com preço abaixo do preço da mediana são vendidos pelo preço de compra acrescido de 30%, imóveis com preço igual da mediana são vendidos pelo preço de compra acrescido de 20% e imóveis com preço acima da mediana são vendidos pelo preço de compra acrescido de 10%.
- 'selling_moment': representa o momento da venda. Imóveis com preço abaixo do preço da mediana na sazonalidade referente aquele preço indicam que é um bom momento para a venda, imóveis com preço igual da mediana na sazonalidade referente aquele preço indicam que é um momento regular para a venda (nem bom e nem ruim) e imóveis com preço acima da mediana na sazonalidade referente aquele preço indicam que é um momento ruim para a venda.

------------------------------------------------------------------------------------------------------------------------------------------

**6. Hipóteses e validações:**

6.1. Hipóteses:

- 6.1.1. Imóveis que possuem vista para o mar são 30% mais caros, na média.
- 6.1.2. Imóveis construídos depois de 1955 são 50% mais caros, na média.
- 6.1.3. Imóveis com porão são 50% maiores do que imóveis sem porão, na média.
- 6.1.4. O crescimento do preço dos imóveis YoY (Year over Year) por ano de construção é de 10%.
- 6.1.5. Imóveis com 3 banheiros tem um crescimento MoM (Month over Month) de 15%.
- 6.1.6. No mês de dezembro os imóveis são 25% mais caros que nos outros meses, na média.
- 6.1.7. Imóveis reformados são 50% mais caros que imóveis não reformados, na média.
- 6.1.8. Imóveis com porão são 40% mais caros que imóveis sem porão, na média.
- 6.1.9. Imóveis com boas condições são 10 anos mais novos que imóveis com más condições, na média.
- 6.1.10. Imóveis reformados tem um crescimento de preço médio mensal MoM 5% maior que imóveis não reformados.

6.2. Validações:

- 6.2.1. Falso. Imóveis com vista para o mar são 211,76% mais caros, na média.
- 6.2.2. Falso. Imóveis construídos depois de 1955 são 1,4% mais caros, na média.
- 6.2.3. Falso. Imóveis com porão são 19,83% maiores, na média.
- 6.2.4. Falso. O crescimento de preço anual dos por ano de construção dos imóveis é de 1,07%, na média.
- 6.2.5. Falso. O crescimento de preço mensal dos imóveis com 3 banheiros é de 0,16%, na média.
- 6.2.6. Falso. Em dezembro os imóveis são 3,13% mais baratos que nos outros meses, na média.
- 6.2.7. Falso. Imóveis reformados são 43,29% mais caros, na média.
- 6.2.8. Falso. Imóveis com porão são 27,76% mais caros, na média.
- 6.2.9. Falso. Imóveis em boas condições são 23,57 anos mais velhos, na média.
- 6.2.10. Falso. Imóveis reformados tem um crescimento de preço médio mensal MoM de 3,58%, enquanto imóveis não reformados tem um crescimento de preço médio mensal MoM de 0,11%.

------------------------------------------------------------------------------------------------------------------------------------------

**7. Resultados financeiros:**

Os imóveis sugeridos para compra estão detalhados no arquivo 'purchase_recommendations.csv' e na aplicação em Streamlit. Enquanto isso, os valores de venda individuais são mostrados no arquivo 'selling_recommendations.csv' e também na aplicação em Streamlit. O custo total da compra dos imóveis é de US$ 1.814.492,00. O ganho total com as vendas dos imóveis pode chegar até US$ 2.358.839,60, caso sejam todos vendidos nos momentos considerados mais adequados. Desta forma, o lucro obtido com as vendas pode chegar até US$ 544.347,60. 

------------------------------------------------------------------------------------------------------------------------------------------

**8. Conclusão:**

Após a realização das análises foi possível responder as questões de negócio com sucesso. Foi identificado que os imóveis endereçados pelo código 98070 são os mais interessantes para a compra, visto que os 5 imóveis sugeridos para compra encontram-se nesta mesma localidade. Estes imóveis além de bem localizados e com vista para o mar, encontram-se em boas condições do ponto de vista construtivo e contam com preços atrativos. Na questão das vendas, com as medianas dos preços para cada sazonalidade e para cada localidade, é possível identificar qual momento do ano é mais propício para a venda de imóveis em uma determinada região. De um modo geral, os imóveis selecionados podem ser vendidos em qualquer momento do ano, exceto o imóvel de código 8550001515, que nos meses entre setembro e novembro possui um preço maior que o da sua mediana.
