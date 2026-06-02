

import os
import shutil

from datetime import datetime
from PrintTool import printTool

import dotenv
dotenv.load_dotenv('DbLabs.env')

import DbLabs
from leitura import extrairPJ, extrairPDF, defineArquivo

import pandas as pd


class Arquivo:
    def __init__(self,tipo:dict, cliente, arquivo):
        self.tipo = tipo
        self.cliente = cliente
        self.arquivo = arquivo

verde = printTool.configColorizar('verde',autoPrint=True).colorizar
vermelho = printTool.configColorizar('vermelho',autoPrint=True).colorizar

bd = DbLabs.buscaDominio()

mes = '01'
os.system('cls')

while mes not in [f'0{m}'[-2:] for m in range(1, 13)]:
    mes = f'0{str(input('mes: '))}'[-2:]



if 'data' not in os.listdir(os.getcwd()): os.mkdir(f'{os.getcwd()}/data')

# Processa
verde('Processando Arquivos')


files = []
erros = []

entradas = len(os.listdir('data/Entrada'))

if entradas == 0:
    vermelho("Não há arquivos na pasta de entradas")
    input('precione qualquer tecla para sair')
    exit()

for arquivo in os.listdir('data/Entrada'):

    try:

        if not arquivo.endswith('.pdf'):

            erros.append(f'{arquivo} -> Extensão do arquivo não é PDF')

            continue



        textPDF = extrairPDF(f'data/Entrada/{arquivo}')
        tipoArquivoAtual = defineArquivo(textPDF)
        pj = ''


        if tipoArquivoAtual is None:

            erros.append(f'{arquivo} -> Tipo do arquivo não definido')
            continue


        pj = extrairPJ(textPDF,tipoArquivoAtual)
        if pj is None :
            erros.append(f'{arquivo} -> CNPJ não encontrado no arquivo')
            continue

        cliente = bd.buscaCNPJ(str(pj))
        if cliente is None:
            erros.append(f'{arquivo} -> CNPJ não encontrado na base de clientes {pj}')
            continue

        infos = tipoArquivoAtual

    except Exception as e:

        print(f"{arquivo}: {e} ")

        continue


    a:Arquivo = Arquivo(infos,cliente,arquivo)
    files.append(a)

# Salva


df = pd.DataFrame(columns=[['titulo', 'tipo', 'pasta']])

pastaSaida = datetime.today().strftime('%Y%m%d-%H%M')

verde(f'Salvando Arquivos na pasta {pastaSaida}')

saidas = 0

for f in files:
    df.loc[len(df)] = [f.arquivo, f.tipo['tipoA'],f.tipo['pasta']]

    saidaAtual = f"data/Saida/{pastaSaida}/{f.cliente.razao} - {f.cliente.cod}/{f.tipo['pasta']}"


    os.makedirs(saidaAtual,exist_ok=True)
    shutil.copy(f'data/Entrada/{f.arquivo}', saidaAtual)
    saidas = saidas + 1

print(f'Entradas:{entradas}')
print(f'Saidas:{saidas}')

caminhoSaidas = f'{os.getcwd()}/data/Saida/{pastaSaida}'


if saidas == entradas:
    verde('Processo finalizado, todos os arquivos foram processados e salvos')

else:
    vermelho(f'Processo finalizado, {saidas}/{entradas} arquivos foram processados e salvos \n'
             f' ocorreram {entradas - saidas} erros\n')

    for e in erros:
        vermelho(e)
        saidaAtual = f'{caminhoSaidas}/erros'
        os.makedirs(saidaAtual, exist_ok=True)
        arquivo = e.split(' -> ')[0]
        shutil.copy(f'data/Entrada/{arquivo}', fr'{saidaAtual}\{arquivo}')

os.startfile(caminhoSaidas)

input('clique qualquer tecla para sair')