
from pypdf import PdfReader
import re

mCNPJ = r'[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}\/[A-Z0-9]{4}-\d{2}'
mRaizPJ = r"[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}"





reArquivos = {
    # Guias
    'Guia FGTS': {
        'pArquivo':['GFD - Guia do FGTS Digital','Não há informações de recolhimentos do Consignado'],
        'cnpj': mRaizPJ,
        'pasta': 'Guias'
    },
    'Guia FGTS Empréstimo consignado': {
    'pArquivo':['GFD - Guia do FGTS Digital','Não há informações de recolhimentos do FGTS'],
    'cnpj': mRaizPJ,
    'pasta': 'Guias'

    },
    'Guia RF': {
        'pArquivo':['Documento de Arrecadação\\nde Receitas Federais'],
        'cnpj': mCNPJ,
        'pasta': 'Guias'

    },
    'Contribuição Assistencial': {

        'pArquivo':['CONTRIBUIÇÃO ASSISTENCIAL'],
        'cnpj': fr'(?<=CPF\/CNPJ:) {mCNPJ}',
        'pasta': 'Guias'
    },

    # DCTF Web

    'Declaração completa DCTFWeb': {
        'pArquivo':['RELATÓRIO DA DECLARAÇÃO COMPLETA - DCTFWeb'],
        'cnpj': mCNPJ,
        'pasta': 'DCTFWEB'

    },


    'Recibo DCTFWeb': {
        'pArquivo':['Recibo de Entrega da Declaração de Débitos e Créditos Tributários Federais - DCTFWeb'],
        'cnpj': mCNPJ,
        'pasta': 'DCTFWEB'
    },

    'Resumo DCTFWeb': {
    'pArquivo':['RELATÓRIO RESUMO DE (DÉBITOS|CRÉDITOS) - DCTFWeb'],
    'cnpj': mCNPJ,
    'pasta': 'DCTFWEB'
    },


    # Fechamento


    'Encargos de IRRF': {
    'pArquivo':['RELAÇÃO DAS BASES DO IRRF'],
    'cnpj': mCNPJ,
    'pasta': 'Fechamento'
    },


    'Relatório de Líquidos': {
    'pArquivo':['RELAÇÃO GERAL DOS LÍQUIDOS'],
    'cnpj': mCNPJ,
    'pasta': 'Fechamento'
    },

    'Recibo de pagamento': {
    'pArquivo':['Declaro ter recebido a importância líquida discriminada neste recibo'],
    'cnpj': mCNPJ,
    'pasta': 'Fechamento'
    },

    # Domínio

    'Analítico GPS': {
    'pArquivo':['ANALÍTICO DE GPS'],
    'cnpj': mCNPJ,
    'pasta': 'Fechamento'
    },

    'RELAÇÃO DE EMPRÉSTIMOS CONSIGNADOS': {
    'pArquivo':['RELAÇÃO DE EMPRÉSTIMOS CONSIGNADOS'],
    'cnpj': mCNPJ,
    'pasta': 'Fechamento'
    },

    'Folha Mensal e Complementar': {
    'pArquivo':['Folha Mensal e Complementar'],
    'cnpj': mCNPJ,
    'pasta': 'Fechamento'
    },

    'Movimentos': {
    'pArquivo':['\\nCódigo\\nMOVIMENTOS'],
    'cnpj': mCNPJ,
    'pasta': 'Fechamento'
    },

    'RESUMO DA FOLHA': {
    'pArquivo':['RESUMO DA FOLHA'],
    'cnpj': mCNPJ,
    'pasta': 'Fechamento'
    },


    'Relatório FGTS': {
    'pArquivo':['Origem: Gestão de Guias'],
    'cnpj': mRaizPJ,
    'pasta': 'Fechamento'
    },



}




def defineArquivo(texto):


    ok = False
    for tipoA in reArquivos:

        for requisito in reArquivos[tipoA]['pArquivo']:

            resultado = re.findall(requisito, texto)
            if len(resultado) == 0:
                ok = False
                break

            else: ok = True

        if ok: return reArquivos[tipoA] |{'tipoA':tipoA}

    return None

def extrairPJ(texto,tipo:dict):


    resultado = re.search(tipo['cnpj'], texto)

    if resultado is None: return None


    return resultado.group(0)

def extrairPDF(caminho):
    pdfTXT = ""

    try:
        reader = PdfReader(caminho)

        for pagina in reader.pages:
            conteudo = pagina.extract_text()
            if conteudo:
                pdfTXT += "\n" + conteudo

    except Exception as e:
        print("Erro ao ler PDF:", e)

    return pdfTXT


#print(extrairPDF(r"C:\Users\Marcelo\Documents\Projetos GitHub\PDFSRT\data\Entrada\ResumoCreditos_36214840000102_012026_40_.pdf"))