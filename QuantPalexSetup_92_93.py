# =============================================================================
# Autor: @opvistar (Aprendiz de Feiticeiro - Twitter)
# SETUP 9.2 e 9.3 PALEX
# =============================================================================

import datetime
import QuantUtilities as util
import QuantMT5ConstantesGlobais as CTE

#######################################################################
# CONFIGURACAOES SETUP 9.2 e 9.3
#######################################################################

# enxergo esse numero de candles para analise do setup
LAG_PRECO_9X = 7
S_92_93_MEDIA_EMA = 9  # media EMA
S_92_93_MEDIA_SMA = 21  # media SMA
DISTANCIA_MME = 5.0

# média movel tem que estar ascendente LAG_MEDIA_MOVEL_92_93 periodos
LAG_MEDIA_MOVEL_92_93 = 10

# diferenca para tendencia não pode sair dessa faixa
TOLERANCIA_EMA9 = -0.0001
#######################################################################

str_path_hist = "...\\PYTHON_SOURCE\\FINANCAS_QUANTITATIVAS\\Database_Python\\"
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

# =============================================================================
# CABECALHO DO RELATORIO     
# =============================================================================
print("|---------------------------------------------------------------------|")
print("|                        SETUPS  9.2/9.3 PALEX                        |")
print("|---------------------------------------------------------------------|")
print("|                                                                     |")
print("| DATA:...............: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z%z")+"                          |")
print("| TIMEFRAME...........:" + util.get_str_timeframe()+"                                            |")
print("| JANELA (períodos)...: {0:2d}                                            |".format(LAG_MEDIA_MOVEL_92_93))
print("| PER. MME CURTA......:{0:3d} períodos   ".format(S_92_93_MEDIA_EMA)+"                                |")
print("| PER. MMA LONGA......:{0:3d} períodos   ".format(S_92_93_MEDIA_SMA)+"                                |")
print("| DIST. MÁX (%) MME...:{0:5.2f}                                          |".format(DISTANCIA_MME))
print("|                                                                     |")
print("|---------------------------------------------------------------------|")
print("|     ATIVO     | DIST. MME  (%)|  IFR(3)  |     SETUP    |    C/V    |")
print("|---------------------------------------------------------------------|")

# file_debug = open("log_console_" +datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S') + ".txt", "a")  # DEBUG

for k_ativo, v_preco in sorted(dict_ativos_precos.items()):

    # =============================================================================
    #  AQUI PROCESSO O SETUP 9.2 e 9.3          
    # =============================================================================
    
    v_preco = v_preco.iloc[::-1]    # datas mais recentes serão as ultimas linhas.    


    lista_IFR = (util.calculaIFR(v_preco['Fechamento'], 3)).tolist()

    # trato somente os LAG_PRECO_9X valores
    # NOCA CASO DE MEDIA MOVEL, PEGO PERIODO MAIOR

    ema9_lag = v_preco.ewm(span=S_92_93_MEDIA_EMA, adjust=False).mean()
    ema9_lag = ema9_lag.tail(LAG_MEDIA_MOVEL_92_93)

    sma21_lag = v_preco.rolling(window=S_92_93_MEDIA_SMA).mean()
    sma21_lag = sma21_lag.tail(LAG_MEDIA_MOVEL_92_93)

    # print("sma21_lag") #debug
    # print(sma21_lag)   # debug

    # trato somente os LAG_PRECO_9X valores
    df_preco_lag = v_preco.tail(LAG_PRECO_9X)

    # converto a porra toda pra type LIST

    df_preco_lag_close = df_preco_lag['Fechamento'].tolist()
    df_preco_lag_high = df_preco_lag['Maxima'].tolist()
    df_preco_lag_low = df_preco_lag['Minima'].tolist()

    sma21_lag = sma21_lag['Fechamento'].tolist()
    ema9_lag = ema9_lag['Fechamento'].tolist()

    bool_tendencia_baixa = False
    bool_tendencia_alta = False

    # diferencas dos elementos da lista ema9
    diff_ema9_lag = [j - i for i, j in zip(ema9_lag[:-1], ema9_lag[1:])]

    min_diff_ema9_lag = min(diff_ema9_lag)
    max_diff_ema9_lag = max(diff_ema9_lag)

    # =============================================================================
    #     VERIFICA SE ESTA EM TENDENCIA
    # =============================================================================

    # a. VERIFICO SE EMA9 ESTA ASCENDENTE
    # b. VERIFICO SE EMA9 > SMA21          
    if ema9_lag[-1] > sma21_lag[-1] and min_diff_ema9_lag > TOLERANCIA_EMA9:
        bool_tendencia_alta = True

    # a. VERIFICO SE EMA9 ESTA DESCENDENTE
    # b. VERIFICO SE EMA9 < SMA21         
    if ema9_lag[-1] < sma21_lag[-1] and max_diff_ema9_lag < TOLERANCIA_EMA9 * (-1):
        bool_tendencia_baixa = True

    str_setup = ""

    distancia_last_MME9_close = (abs(ema9_lag[-1] - df_preco_lag_close[-1]) / ema9_lag[-1])*100

    # #############  DEBUG ################################
    # print(k_ativo,file=file_debug)  
    # print("ema9_lag",file=file_debug)  
    # print(ema9_lag,file=file_debug) 
    # print('sma21_lag',file=file_debug)
    # print(sma21_lag,file=file_debug)
    # print('bool_tendencia_alta',file=file_debug)
    # print(bool_tendencia_alta,file=file_debug)
    # print('bool_tendencia_baixa',file=file_debug)
    # print(bool_tendencia_baixa,file=file_debug)
    # #############  DEBUG ################################

    if bool_tendencia_alta:

        # VERIFICO ONDE ACONTECEU ***TOPO*** MAX (HIGH) DO PERIODO LAG_PRECO_9X   === SETUP 9.2 ==   
        # idx_preco_maior_maxima = util.acha_idx_max_min(CTE.MAXIMO,df_preco_lag_high)

        # VERIFICO ONDE ACONTECEU MAIOR FECHAMENTO === SETUP 9.3 ===   
        idx_preco_maior_fechamento = util.acha_idx_max_min(CTE.MAXIMO, df_preco_lag_close)

        # SE O TOPO FOI NO CANDLE IMEDIATAMENTE ANTERIOR VERIFICO 9.2
        if idx_preco_maior_fechamento == (LAG_PRECO_9X - 2):

            # SE O FECHAMENTO DO CANDLE ATUAL FECHOU ABAIXO DA MINIMA DO TOPO
            # setup 9.2 - fecha abaixo da minima do topo
            if df_preco_lag_close[-1] < df_preco_lag_low[-2]:
                str_setup = "9.2"

                # SE O TOPO FOI DE NO MINIMO 2 CANDLES PARA TRÁS VERIFICO 9.3
        elif idx_preco_maior_fechamento == (LAG_PRECO_9X - 3):

            # posso estar analisando um ativo que armou 9.2 anterioremente, logo só vou reportar
            # ativos que fecharam abaixo fechamento do candle de referencia (que fez o topo), assim o candle que 
            # vem logo apos o candle de maior fechaento não pode ter rompido a minima do candle de maior fechamento             

            if df_preco_lag_close[idx_preco_maior_fechamento + 1] > df_preco_lag_low[idx_preco_maior_fechamento]:

                # ANALISO OS CANDLES DEPOIS DO MAIOR FECHAMENTO
                candles_close_pos_topo = df_preco_lag_close[
                                         (LAG_PRECO_9X - 1 - idx_preco_maior_fechamento) * (-1):]

                # #############  DEBUG ################################
                # print('df_preco_lag_low',file=file_debug)
                # print(df_preco_lag_low,file=file_debug)
                # print("df_preco_lag_close",file=file_debug)   
                # print(df_preco_lag_close,file=file_debug)  
                # print("candles_close_pos_topo",file=file_debug)  
                # print(candles_close_pos_topo,file=file_debug)  
                # print('min(candles_close_pos_topo)',file=file_debug) # 
                # print(min(candles_close_pos_topo),file=file_debug)  
                # #############  DEBUG #################################  

                # SE O FECHAMENTO DE NO MINIMO 2 ULTIMOS CANDLES FECHARAM ABAIXO DO FECHAMENTO DO TOPO
                if max(candles_close_pos_topo) < df_preco_lag_close[idx_preco_maior_fechamento]:
                    str_setup = "9.3"

        if str_setup:
            # VERIFICO SE O FECHAMENTO DO ULTIMO CANDLE ESTA NAS VINHANCAS DA MME9
            if distancia_last_MME9_close <= DISTANCIA_MME:
                print(
                    "|      {0:6s}   |   {1:5.2f}       |   {2:5.2f}  |     {3:6s}   |     C     |".format(k_ativo,
                                                                                                           distancia_last_MME9_close,
                                                                                                           lista_IFR[
                                                                                                               -1],
                                                                                                           str_setup))
                # print("|      {0:6s}   |   {1:5.2f}       |   {2:5.2f}  |     {3:6s}   |     C     |".format(k_ativo, distancia_last_MME9_close*100,lista_IFR[-1],str_setup),file=file_debug) # DEBUG
    if bool_tendencia_baixa:

        # VERIFICO ONDE ACONTECEU ***FUNDO*** MIN (MIN) DO PERIODO LAG_PRECO_9X   === SETUP 9.1 ===   
        # idx_preco_menor_minima = util.acha_idx_max_min(CTE.MINIMO,df_preco_lag_low)

        # VERIFICO ONDE ACONTECEU MENOR FECHAMENTO === SETUP 9.3 ===   
        idx_preco_menor_fechamento = util.acha_idx_max_min(CTE.MINIMO, df_preco_lag_close)

        # SE O FUNDO FOI NO CANDLE IMEDIATAMENTE ANTERIOR VERIFICO 9.2
        if idx_preco_menor_fechamento == (LAG_PRECO_9X - 2):

            # SE O FECHAMENTO DO CANDLE ATUAL FECHOU ACIMA DA MAXIMA DO CANDLE QUE FEZ O FUNDO...
            # setup 9.2 - fecha abaixo da minima do topo
            if df_preco_lag_close[-1] > df_preco_lag_high[-2]:
                str_setup = "9.2"

                # SE O MENOR FECHAMENTO FOI 2 CANDLES PARA TRÁS VERIFICO 9.3
        elif idx_preco_menor_fechamento == (LAG_PRECO_9X - 3):

            # posso estar analisando um ativo que armou 9.2 anterioremente, logo só vou reportar
            # ativos que fecharam acima do fechamento do candle de referencia (que fez o fundo), assim o candle que 
            # vem logo apos o candle de menor fechaento não pode ter rompido a maxima do candle de maior fechamento  

            if df_preco_lag_close[idx_preco_menor_fechamento + 1] < df_preco_lag_high[idx_preco_menor_fechamento]:

                # ANALISO OS CANDLES DEPOIS DO MENOR FECHAMENTO
                candles_close_pos_fundo = df_preco_lag_close[
                                          (LAG_PRECO_9X - 1 - idx_preco_menor_fechamento) * (-1):]

                # #############  DEBUG ################################
                # print('df_preco_lag_high',file=file_debug)
                # print(df_preco_lag_high,file=file_debug)
                # print("df_preco_lag_close",file=file_debug)   
                # print(df_preco_lag_close,file=file_debug)  
                # print("candles_close_pos_fundo",file=file_debug)  
                # print(candles_close_pos_fundo,file=file_debug)  
                # print('min(candles_close_pos_fundo)',file=file_debug) # 
                # print(min(candles_close_pos_fundo),file=file_debug)  
                # #############  DEBUG #################################

                # SE O FECHAMENTO DO NO MINIMO 2 ULTIMOS CANDLES FECHARAM ACIMA DO FECHAMENTO DO FUNDO
                if min(candles_close_pos_fundo) > df_preco_lag_close[idx_preco_menor_fechamento]:
                    str_setup = "9.3"

        if str_setup:
            # VERIFICO SE O FECHAMENTO DO ULTIMO CANDLE ESTA NAS VINHANCAS DA MME9
            if distancia_last_MME9_close <= DISTANCIA_MME:
                print(
                    "|      {0:6s}   |   {1:5.2f}       |   {2:5.2f}  |     {3:6s}   |     V     |".format(k_ativo,
                                                                                                           distancia_last_MME9_close,
                                                                                                           lista_IFR[
                                                                                                               -1],
                                                                                                           str_setup))
                # print("|      {0:6s}   |   {1:5.2f}       |   {2:5.2f}  |     {3:6s}   |     V     |".format(k_ativo, distancia_last_MME9_close*100,lista_IFR[-1],str_setup),file=file_debug) # DEBUG
print("|--------------------------fim----------------------------------------|\n")


# file_debug.close() # DEBUG


