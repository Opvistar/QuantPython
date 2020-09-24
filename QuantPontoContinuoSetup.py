 
# =============================================================================
#  AQUI PROCESSO O SETUP PONTO CONTINUO  (SOTRMER)   
# =============================================================================

import datetime
import QuantUtilities as util
 
str_path_hist = "...\\FINANCAS_QUANTITATIVAS\\Database_Python\\"
str_path_out_logs = "...\\FINANCAS_QUANTITATIVAS\\LOGS\\"
file_relat = open(str_path_out_logs + "SetupPalex_92_93" + datetime.datetime.now().strftime('%Y_%d_%m_%H_%M_%S') + ".txt", "a")


dict_ativos_precos = util.le_historico_ativos(str_path_hist,str_path_out_logs,file_relat)

#########################################################################################
# não preciso mais do log em arquivo, apresento tudo na tela, caso 
# deseje logar em arquvo ao inve s do console,
#  adicione o parametro "file=file_relat" em cada comando
# print abaixo, não esqueca de mudar a localizacao do comando 
# file_relat.close() para o final do script
######################################################################################
file_relat.close()

#######################################################################
# CONFIGURACAOES SETUP PONTO CONTINUO
#######################################################################

# enxergo esse numero de candles para analise do setup,
# no caso desse setup poderia ser 2, pois só enxergo o 
# ultimo candle.
LAG_PRECO_PC = 7

# média movel tem que estar ascendente LAG_MEDIA_MOVEL_PC periodos
LAG_MEDIA_MOVEL_PC = 10

S_PC_MEDIA_SMA_CURTA = 21   # sma curta
S_PC_MEDIA_SMA_LONGA = 50   # sma longa
# diferenca para tendencia não pode sair dessa faixa
TOLERANCIA_SMA21 = -0.0001
DISTANCIA_MME = 1.5

#######################################################################


# =============================================================================
# CABECALHO DO RELATORIO     
# =============================================================================
print("|------------------------------------------------------------|")
print("|                  SETUP PONTO CONTÍNUO STORMER              |")
print("|------------------------------------------------------------|")
print("|                                                            |")
print("| DATA:...............: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z%z")+"                 |")
print("| TIMEFRAME...........: " + util.get_str_timeframe()+"                                  |")
print("| JANELA..............:  {0:2d} períodos                         |".format(LAG_MEDIA_MOVEL_PC))
print("| PER. MMA............: {0:3d} períodos   ".format(S_PC_MEDIA_SMA_CURTA)+"                      |")
print("| PER. MMA LONGA......: {0:3d} períodos   ".format(S_PC_MEDIA_SMA_LONGA)+"                      |")
print("| DIST. MÁX (%). SMA..: {0:5.2f} ".format(DISTANCIA_MME)+"                               |")
print("| Nota: Dist. max. fechamento ou MMA21 entre MAX e MIN       |")
print("|------------------------------------------------------------|")
print("|      ATIVO    | DIST. MMA  (%)  |  IFR(3)   |      C/V     |")
print("|------------------------------------------------------------|")

for k_ativo, v_preco in sorted(dict_ativos_precos.items()):

    # =============================================================================
    #  AQUI PROCESSO O SETUP 9.2 e 9.3          
    # =============================================================================
    
    v_preco = v_preco.iloc[::-1]    # datas mais recentes serão as ultimas linhas.    


    lista_IFR = (util.calculaIFR(v_preco['Fechamento'], 3)).tolist()
    
        
    # trato somente os LAG_PRECO_PC valores
    
    sma21_lag = v_preco.rolling(window=S_PC_MEDIA_SMA_CURTA).mean()
    sma21_lag = sma21_lag.tail(LAG_MEDIA_MOVEL_PC)
    
    sma50_lag = v_preco.rolling(window=S_PC_MEDIA_SMA_LONGA).mean()
    sma50_lag = sma50_lag.tail(LAG_MEDIA_MOVEL_PC)
    
    # trato somente os LAG_PRECO_PC valores
    df_preco_lag = v_preco.tail(LAG_PRECO_PC)
    
    # converto a porra toda pra type LIST
    
    df_preco_lag_close = df_preco_lag['Fechamento'].tolist()
    df_preco_lag_high = df_preco_lag['Maxima'].tolist()
    df_preco_lag_low = df_preco_lag['Minima'].tolist()
    
    sma21_lag = sma21_lag['Fechamento'].tolist()
    sma50_lag = sma50_lag['Fechamento'].tolist()
    
    bool_tendencia_baixa = False
    bool_tendencia_alta = False
    
    # diferencas dos elementos da lista ema9
    diff_sma21_lag = [j - i for i, j in zip(sma21_lag[:-1], sma21_lag[1:])]
    
    min_diff_sma21_lag = min(diff_sma21_lag)
    max_diff_sma21_lag = max(diff_sma21_lag)
    
    # =============================================================================
    #     VERIFICA SE ESTA EM TENDENCIA
    # =============================================================================
    
    # a. VERIFICO SE SMA21 ESTA ASCENDENTE
    # b. VERIFICO SE SMA21 > SMA50     
    
    if sma21_lag[-1] > sma50_lag[-1] and min_diff_sma21_lag > TOLERANCIA_SMA21:
        bool_tendencia_alta = True
    
    # a. VERIFICO SE SMA21 ESTA DESCENDENTE
    # b. VERIFICO SE SMA21 < SMA50  
    
    if sma21_lag[-1] < sma50_lag[-1] and max_diff_sma21_lag < TOLERANCIA_SMA21 * (-1):
        bool_tendencia_baixa = True
    
    # #############  DEBUG ################################
    # print('bool_tendencia_baixa',file=file_debug)
    # print(bool_tendencia_baixa,file=file_debug)
    # print('bool_tendencia_alta',file=file_debug)
    # print(bool_tendencia_alta,file=file_debug)            
    # print('k_ativo',file=file_debug)
    # print(k_ativo,file=file_debug)       
    # print('df_preco_lag_close',file=file_debug)
    # print(df_preco_lag_close,file=file_debug)
    # print('sma50_lag',file=file_debug)
    # print(sma50_lag,file=file_debug)
    # print('sma21_lag',file=file_debug)
    # print(sma21_lag,file=file_debug)
    # #############  DEBUG ################################
    
    if bool_tendencia_alta or bool_tendencia_baixa:
    
        # VERIFICO SE O FECHAMENTO DO ULTIMO CANDLE ESTA NA VIZINHAÇA DA MM21 ASCENDENTE/DESCENDENTE
        distancia_last_SMA21_close = (abs(sma21_lag[-1] - df_preco_lag_close[-1]) / sma21_lag[-1])*100
    
        # fechamento ou candle cruzando a SMA21
        if ( (distancia_last_SMA21_close <= DISTANCIA_MME) or ( df_preco_lag_high[-1] >= sma21_lag[-1] and df_preco_lag_low[-1] <= sma21_lag[-1]) ) and bool_tendencia_alta:
            # DEVE SER UM CANDLE DE BAIXA PROX A MM21
            #if df_preco_lag_close[-1] < df_preco_lag_open[-1]:
            print("|     {0:<7s}   |      {1:6.2f}     |  {2:6.2f}   |       C      |".format(k_ativo,distancia_last_SMA21_close ,lista_IFR[-1]))
                # print("|      {0:6s}   |     {1:5.2f}       |   {2:5.2f}   |       C      |".format(k_ativo, distancia_last_SMA21_close*100,lista_IFR[-1]),file=file_debug)
    
        if ( (distancia_last_SMA21_close <= DISTANCIA_MME ) or ( df_preco_lag_high[-1] >= sma21_lag[-1] and df_preco_lag_low[-1] <= sma21_lag[-1]) ) and  bool_tendencia_baixa:
            # DEVE SER UM CANDLE DE ALTA PROX A MM21
            #if df_preco_lag_close[-1] > df_preco_lag_open[-1]:
            print("|     {0:<7s}   |      {1:6.2f}     |  {2:6.2f}   |       V      |".format(k_ativo,distancia_last_SMA21_close,lista_IFR[-1]))
    
                # print("|      {0:6s}   |     {1:5.2f}       |   {2:5.2f}   |       V      |".format(k_ativo, distancia_last_SMA21_close*100,lista_IFR[-1]),file=file_debug)


print("|---------------------fim------------------------------------|")

# file_debug.close()
 