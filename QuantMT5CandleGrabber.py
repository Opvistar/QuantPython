# =============================================================================
# Autor: @opvistar (Twitter)- Jan. 2020 
# Inicializa Terminal MT5, sincroniza e coleta os dados de preço
# no timeframe int_time_frame
# 
# =============================================================================
import MetaTrader5 as mt5
import sys
import datetime
import pytz

# import pytz module for working with time zone

UTC_FROM = datetime.datetime(2018, 8,  1,0,0, tzinfo=pytz.timezone("Etc/UTC"))
UTC_TO   = datetime.datetime(2020, 3, 27,0,0, tzinfo=pytz.timezone("Etc/UTC"))
# =============================================================================
# Coleta os dados de preços do ativo em questão
# =============================================================================
def coleta_precos_B3(str_ticker_B3: str, int_time_frame: int, tipo_saida) -> tuple:
    tuple_tickers_B3 = {}  # empty tuple
    
    file_relat = define_saida_print(tipo_saida)
    try:

        #                                         ticker do ativo, time_frame, data inicio, data fim 
        tuple_tickers_B3 = mt5.copy_rates_range(str_ticker_B3, int_time_frame,UTC_FROM,UTC_TO )

        print('###  OK  ### Coleta do histórico de precos do ativo', str_ticker_B3, ' com sucesso...\n', file=file_relat)

    except RuntimeError:

        print("### ERRO ### Não encontrou histórico de preços do ativo " + str_ticker_B3 + ' ...\n', file=file_relat)

    return tuple_tickers_B3


def inicializa_servidor_MT5(tipo_saida) -> bool:
    file_relat = define_saida_print(tipo_saida)
    
    isInitialized = False
    
    try:
        isInitialized = mt5.initialize()  # initialize MetaTrader 5
    except RuntimeError:
                print("### ERRO ### Não consegiu logar no MT5, verifique credenciais...\n")
                return False

    if not isInitialized:
        print('### ERRO ### Não conseguiu inicializar o MT5...\n', file=file_relat)
    else:
        print('###  OK  ### MT5 inicializado com sucesso...\n', file=file_relat)

        # request connection status and parameters

        print( mt5.terminal_info(),"\n", file=file_relat)

        # get data on MetaTrader 5 version

        listaMT5 = mt5.version ()

        print('Versão MT5 :', listaMT5[1], ' Data:', listaMT5[2], '\n', file=file_relat)

        return isInitialized


def encerra_servidor_MT5(tipo_saida):
    isShutDown = mt5.shutdown()
    file_relat = define_saida_print(tipo_saida)
    if isShutDown:
        print('###  OK  ### Conexão ao MT5 encerrada com sucesso...\n', file=file_relat)
    else:
        print('### ERRO ### Não conseguiu desconectar do MT5...\n', file=file_relat)
        
        

def define_saida_print(file_relat):
    if(file_relat is None):
        return sys.stdout
    else:
        return file_relat