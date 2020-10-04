import os  # importa o sistema
import json
import csv  # importa o CSV para gerar arquivos
import src.verify  # Baixa os arquivos para o selenium
import re
import traceback
import json
from src.interface import Iniciar

# Faz a criação da pasta resultados
if not os.path.exists('./resultados'):
    os.makedirs('./resultados')

nomearquivo, palavrachave, opcao, datainicial, datafinal, quantidade = Iniciar()

# Continua criando a pasta
dir_path = os.path.join('./resultados', f'{opcao} -  {palavrachave} - {nomearquivo}')
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

# Atribui as datas para as variáveis
DIAi = datainicial.split("/")[0]
MESi = datainicial.split("/")[1]
ANOi = datainicial.split("/")[2]

DIAf = datafinal.split("/")[0]
MESf = datafinal.split("/")[1]
ANOf = datafinal.split("/")[2]
qntdresult = 0

# Começa as pesquisas
results = []

if opcao == 'folha':
    import src.folhasp2 as site_atual
elif opcao == 'estadao':
    import src.estadao3 as site_atual
elif opcao == 'uol':
    import src.uol as site_atual
else:
    raise ValueError('Site Invalido')

# Realiza a pesquisa
try:
    pesquisa, valor = site_atual.search(query=palavrachave, DIAi=DIAi, MESi=MESi, ANOi=ANOi, DIAf=DIAf, MESf=MESf, ANOf=ANOf)
    print(f'Finalização da pesquisa -- Nome do arquivo: {opcao} -  {palavrachave} - {nomearquivo}')
finally:
    site_atual.END()
# Pra cada resultado da pesquisa, adiciona o resultado na lista 'results'
for search_result in pesquisa:
    results.append(search_result)
    
# Faz o preenchimento de arquivos (todos)
## Preenche um CSV com os resultados obtidos (Título, Data, descrição e link)
with open('{}.csv'.format(os.path.join(dir_path, "Resultados_da_coleta")), 'w',  encoding='utf-8') as csv_file:
    for res in results:
        res['date'] = res['date'].replace('|', '-')
        csv_file.write((res['date'] + '\t' + res['title'] + '\t' + res['secao'] + '\t' + res['imagem'] + '\t' + res['descr']+ '\t' + res['link']).replace('\n', ' '))
        csv_file.write('\n')
        arquivotxt = re.sub('\W', '_', res['title'])            
        sec_path = os.path.join(dir_path, res['secao'])
        if not os.path.exists(sec_path):
            os.makedirs(sec_path)
        with open('{}.txt'.format(os.path.join(sec_path, res['date'] + ' - ' + arquivotxt[:20])), 'w', encoding='utf-8') as text:
            res['content'] = re.sub('\n+', '\n', res['content'])
            try:
                content = res['title'] + '\n\n' + res['content']
            except KeyError:
                content = 'Algo deu errado - main l.67 KeyError - Informar ao desenvolvedor'
            text.write(content)
            qntdresult+=1
            # Gera o arquivo de coleta
with open('{}.txt'.format(os.path.join(dir_path, "Parâmetros_da_coleta")), 'w', encoding='utf-8') as text:
    text.write(f'Nome da pasta: {opcao} -  {palavrachave} - {nomearquivo}\nPalavra chave: {palavrachave}\nSite: {opcao}\nData inicial: {datainicial}\nData final: {datafinal}\nNotícias encontradas (no site): {valor}\nResultados obtidos: {qntdresult}')