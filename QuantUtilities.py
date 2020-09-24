# =============================================================================
# Autor: @opvistar (Aprendiz de Feiticeiro no Twitter)
# Arquivo com funções utilizadas com frequencia em outros scripts
# a funcao mais importante é a "le_historico_ativos", tem uma de leitura
# de IFR para bater com TradingView mas não utilizo mais.
# =============================================================================

import QuantMT5ConstantesGlobais as CTE
import sys
import pandas as pd
import warnings

def acha_idx_max_min(tipo: int, lista: list):

    if tipo == CTE.MINIMO: # MINIMO EH ZERO
        valor = min(lista)
        valor_idxs = [idx for idx, val in enumerate(lista) if val == valor] 
    if tipo == CTE.MAXIMO: # MAXIMO EH UM
        valor = max(lista)
        valor_idxs = [idx for idx, val in enumerate(lista) if val == valor]        
    return valor_idxs[-1]


def calculaIFR (data, time_window):
    
    #######################################################################################
    # CHECAR SEMPRE DADOS DO METATRADER, AS VEZES VEM GAP DE CANDLES DEPENDENDO DO ATIVO
    #######################################################################################
    
    diff = data.diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]
    
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    #up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    #down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    # RSI UTILIZADO NO TRADINGVIEW (EMA COM ALFA=1/n)
    up_chg_avg   = up_chg.ewm(com=time_window , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

# string para o cabecalho do relatorio
def get_str_timeframe():
    if CTE.TIME_FRAME_DEFAULT == CTE.MT5_TIMEFAME_H1:
        return CTE.STR_H1
    elif CTE.TIME_FRAME_DEFAULT == CTE.MT5_TIMEFAME_D1:
        return CTE.STR_D1
    elif CTE.TIME_FRAME_DEFAULT == CTE.MT5_TIMEFAME_M30:
        return CTE.STR_M30
    elif CTE.TIME_FRAME_DEFAULT == CTE.MT5_TIMEFAME_W1:
        return CTE.STR_W1    

# # define a distancia do ultimo candle da janela em relacao a media movel em percentual  
# def get_str_tolerancia_MM():
#     if CTE.TIME_FRAME_DEFAULT == CTE.MT5_TIMEFAME_H1:
#         return CTE.DISTANCIA_MEDIA_MOVEL_H1
#     elif CTE.TIME_FRAME_DEFAULT == CTE.MT5_TIMEFAME_D1:
#         return CTE.DISTANCIA_MEDIA_MOVEL_D1
#     elif CTE.TIME_FRAME_DEFAULT == CTE.MT5_TIMEFAME_M30:
#         return CTE.DISTANCIA_MEDIA_MOVEL_M30
#     elif CTE.TIME_FRAME_DEFAULT == CTE.MT5_TIMEFAME_W1:
#         return CTE.DISTANCIA_MEDIA_MOVEL_W1  
    
def get_Z_alfa(p_valor):
    if p_valor == CTE.Z_ALFA_0DOT05:
        return 1.96
    elif p_valor == CTE.Z_ALFA_0DOT01:
        return 2.58
        
def define_saida_print(file_relat):
    if(file_relat is None):
        return sys.stdout
    else:
        return file_relat

###############################################################
###  LE OS ATIVOS DO BANCO DE DADOS DO PYTHON               ###
### entradas (path arquivos, path logs, arquivo logs)       ###
### saida dicionario com ativos e historico                 ###
### define tambem as colunas que quer ler do csv            ###
### bem como tipo de Enconding (MT5 ou Tryd)
### default sao as que já uso                               ###
###############################################################    
def le_historico_ativos(str_path_hist,str_path_out_logs,file_relat,colunas=["Data", "Fechamento","Maxima","Minima"],bEncondingMT5=False):

    dict_ativos_precos = {}
     
    #tamanho_historico = []
    lWarning = False
    str_warning_msgs = []
    
    pd.set_option('display.max_rows', None)     #debug
    pd.set_option('display.max_columns', None)  #debug
    pd.set_option('display.width', None)        #debug
    pd.set_option('display.max_colwidth', None)   #debug
    warnings.filterwarnings("ignore", message="invalid value encountered in log")
    
    
    for ativo in CTE.LISTA_B3:
    
        file_name_py  = str_path_hist + ativo + "_python.csv"
        lSucesso = True
        ativo_python = pd.DataFrame(columns = colunas )
        
        try:
            
            if not bEncondingMT5:
                ativo_python = pd.read_csv(file_name_py, encoding = "ISO-8859-1")  # LE DO PYTHON
            else:
                ativo_python = pd.read_csv(file_name_py, encoding = "UTF-16LE")     # LE DO MT5 (encoding diferente)
        
        except ( IOError, NameError,PermissionError,FileNotFoundError) as e:
            print("#################################################################################################",file=file_relat)
            print("         ### ATENÇÃO ### ocorreu um problema na leitura do arquivo DB Python ativo: " + ativo,file=file_relat )
            print(e,file=file_relat)
            lSucesso = False
            print("#################################################################################################",file=file_relat)
        
        if lSucesso and len(ativo_python) > 0:   
            # cria dicionario para cada ticker com o historico de preços
            if len(ativo_python) > CTE.AMOSTRA_LONGA + 1:
                dict_ativos_precos[ativo] = ativo_python 
                #tamanho_historico.append(len(ativo_python))
            else:
              print("### ATENÇÃO ###  ticker " + ativo + " tem tamanho total de " + str(len(ativo_python)) + " dias, inferior ao mínimo de " + str(2*CTE.AMOSTRA_LONGA + 1) + " dias..." ,file=file_relat)
              lWarning = True
              str_warning_msgs.append(ativo)
    print('\n')
    if lWarning :
        print("### ATENÇÃO ###  Verifique os logs, alguns ativos com tamanho de amostra incompatíveis...")
        for str_atv in str_warning_msgs:
            print(str_atv)
    else:
        if not lSucesso:
            print("### ATENÇÃO ###  problema na leitura dos arquivos de preços, verifique os logs...")
        else:
            print("Importação de dados bem sucedida!...Total de ativos importados : " + str(len(dict_ativos_precos)))
            print("\n")
                    
    return dict_ativos_precos    