import pandas as pd
import datetime
import numpy as np
import QuantMT5ConstantesGlobais as CTE

############################################################################################
############################################################################################
#  AUTOR: @opvistar (Aprendiz de Feiticeiro - Twitter)
#  DATA: 07.04.2020
#  ESSE SCRIPT LE OS ARQUIVOS DO PYTHON E ATUALIZA SEUS VALORES
#  DE PRECO DE FECHAMENTO DIÁRIOS
#  DEVE SER EXECUTADO *** TODOS DIA *** OU NOVA MIGRACAO DO
#  BANCO DE DADOS DO TRYD DEVE SER REALIZADA
#
#  -- 13.04.2020 -- ATUALIZADO PARA CONTER PREÇO DA MAXIMA E MINIMA DOS ATIVOS
#  -- 15.04.2020 -- CHECA AGORA SE EXISTE DADOS DUPLICADOS E TAMBÉM
#                   SE DATA DO ARQUIVO DE PRECO DIÁRIO ESTÁ OK LINHA A LINHA
#  -- 03.09.2020 -- DROPO TODAS AS LINHAS COM ALL COLUNAS nan

############################################################################################
############################################################################################



str_path_log = "...\\FINANCAS_QUANTITATIVAS\\Database_Python\\Logs_Migracao\\log_migracao_diaria_"

file_relat = open(str_path_log + datetime.datetime.now().strftime('%Y_%d_%m_%H_%M_%S') + ".txt", "a")  # DEBUG

ultima_data = datetime.datetime.now().strftime('%d/%m/%Y') 


str_path_py = "...\\PYTHON_SOURCE\\FINANCAS_QUANTITATIVAS\\Database_Python\\"


entrada = input("Continuar y/n? Verifique se é a data DE HOJE!! -->" + ultima_data + " : ")

##########################################################################################################  
# SE A ATUALIZACAO NÃO É FEITA NO MESMO DIA, DESCOMENTAR LINHA ABAIXO COM A DATA CORRETA
# POR EXEMPLO SÓ ATUALIZO O DDE DO EXCEL MAS FACO A MIGRACAO NO OUTRO DIA DE MANHA, MUDAR A DATA PARA
# A DATA DE ONTEM E DESCOMENTAR O CÓDIGO ABAIXO
##########################################################################################################
#ultima_data = "18/09/2020"


lSucesso = True
lCheckEscrita = True
lDataNaoDuplicada = True
lDataTrydMatch    = True
lNaoTerminouUser= True

pd.set_option('display.max_rows', None)     #debug
pd.set_option('display.max_columns', None)  #debug
pd.set_option('display.width', None)        #debug
pd.set_option('display.max_colwidth', None)   #debug





###################################### 
# leio os precos de fechamento do dia
#####################################
try:

    fechamento_dia_hoje = pd.read_csv(str_path_py + "LISTA_ATIVOS_B3_FECHAMENTO.csv", sep=';', engine='python' , encoding = "ISO-8859-1")
    
    fechamento_dia_hoje.dropna(how='all') # dropo todas as linhas com todas colunas nan

    print("Listando arquivo LISTA_ATIVOS_B3_FECHAMENTO.csv...",file=file_relat)
    print(fechamento_dia_hoje,file=file_relat)

except ( IOError, NameError,PermissionError,FileNotFoundError) as e:
    print("#################################################################################################",file=file_relat)
    print("         ### ATENÇÃO ### ocorreu um problema na leitura do arquivo com fechameno diário", file=file_relat )
    print("         ### ATENÇÃO ### ocorreu um problema na leitura do arquivo com fechameno diário" )    
    print(e,file=file_relat)
    lSucesso = False
    print("#################################################################################################",file=file_relat)
 
if (entrada == "y" or entrada == "Y") and lSucesso:
    
    for ativo in sorted (CTE.LISTA_B3):
        
        ###################################################################
        # leio o arquivo DB Python, preco ja vem convertido em numpy64
        ###################################################################

        file_name_py  = str_path_py+ ativo + "_python.csv"

        try:
            df_ativo_B3 = pd.read_csv(file_name_py, encoding = "ISO-8859-1")
        except ( IOError, NameError,PermissionError,FileNotFoundError) as e:
            print("#################################################################################################",file=file_relat)
            print("         ### ATENÇÃO ### ocorreu um problema na leitura do arquivo DB Python ativo: " + ativo,file=file_relat )
            print(e,file=file_relat)
            lSucesso = False
            print("#################################################################################################",file=file_relat)
        
        if lSucesso:
            ###################################################################
            # adiciono o novo preço no arquivo csv, e salvo novamente
            ###################################################################
            
            # identifico a linha do ativo em questão dentro do arquivo LISTA_ATIVOS_B3_FECHAMENTO.csv 

            idx = fechamento_dia_hoje.loc[fechamento_dia_hoje['Ativo'] == ativo].index[0]
            lSucesso = False          

            # só atualizo se a 1a linha do arquivo DB ativo_Python.csv não é a data de hoje,
            # pode ter tido problema e atualização foi parcial
            
            if not df_ativo_B3['Data'][0] == ultima_data:
                    
                # fechamento_dia_hoje['Data'][idx]  data do arquivo LISTA_ATIVOS_B3_FECHAMENTO.csv na linha dada por idx
                # todas as linhas tem que serem iguais a data ultima_data (que é a data a ser atualizada)
                # se não for, vai pular o arquivo csv a a ser atualizado.                
                 
                if ( fechamento_dia_hoje['Data'][idx] == ultima_data): 
                    
                    str_fechamento = fechamento_dia_hoje['Fechamento'][idx] 
                    str_fechamento_fech = str_fechamento.replace(',','.') 
                    
                    str_fechamento_min = fechamento_dia_hoje['Minima'][idx] 
                    str_fechamento_min = str_fechamento_min.replace(',','.') 
                    
                    str_fechamento_max = fechamento_dia_hoje['Maxima'][idx] 
                    str_fechamento_max = str_fechamento_max.replace(',','.') 
                    
                    # somo todos as linhas de preço inclusive a que não foi ainda atualizada
                    sum_X = np.sum(np.array(df_ativo_B3['Fechamento'])) + float(str_fechamento_fech)                   
                    
                    # atualizo a linha dos arquivos csv, passa a ser a 1a linha
                    new_row = [ ultima_data,float(str_fechamento_fech),float(str_fechamento_max) ,float(str_fechamento_min) ]
                    df_ativo_B3.loc[-1] = new_row
                    df_ativo_B3.index = df_ativo_B3.index + 1  # shifting index
                    df_ativo_B3.sort_index(inplace=True) 
    
                    ###################################################
                    # salvo novamente o arquivo CSV
                    # com o preco de fechamento atualizado
                    #####################################################    
                    lSucesso = True
                    
                    try:
                    # salvo arquivo csv
                        df_ativo_B3.to_csv(file_name_py, index=False)
                        # debug print("Debug - Atualizou arquvivo csv")
                    except ( IOError, NameError,PermissionError,FileNotFoundError) as e:
                        print("#################################################################################################",file=file_relat)
                        print("         ### ATENÇÃO ### ocorreu um problema na escrita do arquivo DB Python ativo: " + ativo ,file=file_relat)
                        print(e,file=file_relat)
                        lSucesso = False
                        print("#################################################################################################",file=file_relat)           

                # se bem sucedido e não encontrou data já atualizada...    
                if lSucesso:
                    # leio novemente o mesmo arquivo e somo todos as linhas de preço
                    try:        
                        df_ativo_B3 = pd.read_csv(file_name_py, encoding = "ISO-8859-1")
                    except ( IOError, NameError,PermissionError,FileNotFoundError) as e:
                        print("#################################################################################################",file=file_relat)
                        print("         ### ATENÇÃO ### ocorreu um problema na leitura do arquivo DB Python ativo: " + ativo ,file=file_relat)
                        print(e,file=file_relat)
                        lSucesso = False            
                        print("#################################################################################################",file=file_relat)           
                    
                    if lSucesso:
                        # testo se o conteudo é o mesmo
                        sum_XX = np.sum(np.array(df_ativo_B3['Fechamento']))                    
                        if round( sum_XX,4) == round(sum_X,4):
                            print("### CHECK ESCRITA   OK ### Arquivo csv ativo " + ativo + " esta integro.",file=file_relat)
                        else:
                            lCheckEscrita = False
                            print("### ATENÇÃO CHECK ESCRITA ERRO ### Arquivo csv ativo "+ ativo + " com problemas!",file=file_relat)

                else:
                    
                    print("A data do fechamento do ativo " + ativo + " no arquivo LISTA_ATIVOS_B3_FECHAMENTO.csv NÃO é a data de hoje,...",file=file_relat)                                                    
                    lDataTrydMatch = False
            else:
                print("Data de fechamento " + ultima_data + " já existe no ativo " + ativo + " ...",file=file_relat)
                lDataNaoDuplicada = False
                lSucesso = True
elif not (entrada == "y" or entrada == "Y") and lSucesso:
    lNaoTerminouUser = False
             

    
print("\n")


if  lSucesso and lCheckEscrita and lDataNaoDuplicada and lDataTrydMatch and lNaoTerminouUser:
    print("Atualização concluída com sucesso...")
else:
    if not lCheckEscrita:
        print("### ATENÇÃO ### Houve problemas no check da escrita, verifique os logs...")  
    if not lDataNaoDuplicada:
        print("### ATENÇÃO ### Houve problemas de data duplicada (ja existe no DB Python), verifique os logs...")        
    if not lDataTrydMatch:
        print("### ATENÇÃO ### Houve problemas de datas no arquivo LISTA_ATIVOS_B3_FECHAMENTO.csv, verifique os logs...")  
    if not lNaoTerminouUser:
        print("Script encerrado pelo usuário...")        

file_relat.close()