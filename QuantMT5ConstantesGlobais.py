# =============================================================================
# Autor: @opvistar (Aprendiz de Feiticeiro no Twitter)
# Arquivo com as constantes globais de configuração dos setups e
# conexao MT5
# =============================================================================

#######################################################################
# CONFIGURACAOES GERAIS
#######################################################################
import datetime
import pytz

# constantes para utilizar conexão MT5 (caso desejar um dia)

MT5_TIMEFAME_M60  =1
MT5_TIMEFAME_M2  =2
MT5_TIMEFAME_M3  =3
MT5_TIMEFAME_M4  =4
MT5_TIMEFAME_M5  =5
MT5_TIMEFAME_M6  =6
MT5_TIMEFAME_M10 =10
MT5_TIMEFAME_M12 =12
MT5_TIMEFAME_M15 =15
MT5_TIMEFAME_M20 =20
MT5_TIMEFAME_M30 =30
MT5_TIMEFAME_H1  =1  | 0x4000
MT5_TIMEFAME_H2  =2  | 0x4000
MT5_TIMEFAME_H3  =3  | 0x4000
MT5_TIMEFAME_H4  =4  | 0x4000
MT5_TIMEFAME_H6  =6  | 0x4000
MT5_TIMEFAME_H8  =8  | 0x4000
MT5_TIMEFAME_H12 =12 | 0x4000
MT5_TIMEFAME_D1  =24 | 0x4000
MT5_TIMEFAME_W1  =1 | 0x8000
MT5_TIMEFAME_MON1=1 | 0xC000

#                              year , month, day, hour, minute,  tz
UTC_FROM = datetime.datetime(2018, 8,  1,0,0, tzinfo=pytz.timezone("Etc/UTC"))
UTC_TO   = datetime.datetime(2020, 3, 27,0,0, tzinfo=pytz.timezone("Etc/UTC"))

TIME_FRAME_DEFAULT= MT5_TIMEFAME_D1

# de ativos, removidos

# DEFINE ACHAR VALOR MINIMO OU MAXIMO DE UMA SERIE
MAXIMO=1
MINIMO=0

STR_W1       = " W1"
STR_H1        = " H1"    
STR_D1    =     " D1"
STR_M30       = "M30"

TIME_FRAME_DEFAULT= MT5_TIMEFAME_D1

# porcentual fechamento em relação a media movel
DISTANCIA_MEDIA_MOVEL_M30 = 0.25  # em percentual
DISTANCIA_MEDIA_MOVEL_H1= 0.35      # em percentual
DISTANCIA_MEDIA_MOVEL_W1= 2.5      # em percentual

# ignoro ultimo candle (aberto) ou não
DROP_LAST_CANDLE = False

#######################################################################
# CONFIGURACAOES SETUP MM200
#######################################################################
S_200_MEDIA_MOVEL = 200  # media movel a detectar a proximidade
#######################################################################

#######################################################################
# CONFIGURACAOES SETUP IFR3
#######################################################################
MEDIA_SMA_IFR3 = 50   # ativo deve estar em tendencia
LAG_MEDIA_MOVEL_IFR3 = 17   # vejo os ultimos 15 periodos pra verificar tendencia
IFR3_TOLERANCIA_SMA = -0.0001    # threshold quando mm esta flat
IFR3_THRESHOLD_UP = 90       # IFR2 sobrecomprado threshold
IFR3_THRESHOLD_DOWN = 10     # IFR2 sobrevendio threshold
AVALIAR_TENDENCIA="Nao"
#######################################################################


######################################################################
# LISTA DE TICKERS DA B3
#######################################################################




LISTA_B3 = {'ABEV3','ALPA4','ALUP11','ARZZ3','AZUL4','B3SA3','BBAS3',
            'BBDC4','BBSE3','BEEF3','BIDI4','BOVA11','BRAP4','BRDT3','BRFS3','BRKM5',
            'BRML3','BRSR6','BTOW3','CCRO3','CESP6','CMIG4',
            'CPFE3','CPLE6','CRFB3','CSAN3','CSMG3','CSNA3','CVCB3','CYRE3','DTEX3',
            'ECOR3','EGIE3','ELET3','ELET6','EMBR3','ENBR3','ENGI11','EQTL3',
            'EZTC3','FLRY3','GFSA3','GGBR4','GOAU4','GOLL4','GRND3','GUAR3',
            'HGTX3','HYPE3','IGTA3','IRBR3','ITSA4','ITUB4','JBSS3',
            'KLBN11','COGN3','LAME4','LIGT3','LINX3','LREN3','MDIA3','MGLU3',
            'MRFG3','MRVE3','MULT3','MYPK3','ODPV3','PETR4','PSSA3','QUAL3','RADL3','RAIL3',
            'RAPT4','RENT3','RLOG3','SANB11','SAPR11','SBSP3','SLCE3','SMTO3','SMLS3',
            'SUZB3','TAEE11','TIET11','TIMP3','TRPL4','TUPY3','UGPA3',
            'USIM5','VALE3','VIVT4','VVAR3','WEGE3','JHSF3','LOGN3','CEAB3','OIBR3','BPAN4'}
  
AMOSTRA_LONGA = 260          # tamanho MINIMO da amostra executar os scripts


