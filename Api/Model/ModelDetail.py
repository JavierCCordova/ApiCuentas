import Api.Model.Component.componentDetail as detail
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np 
import traceback

class ModelDetail():
    
    def __init__(self):
        pass

    def getDetailData(self,idUser, conn):        
        try:
            response    =   dict(status=200)
            ArrayReponse=   []
            respons     =   detail.getDetailData(idUser,conn)
            dfIncome    =   self.getIncomeActive(idUser,conn)
            df          =   pd.DataFrame(respons['data'])
            df['Fecha'] =   pd.to_datetime(df['Fecha'])
            dfT         =   pd.DataFrame(respons['dataT'])
            dfS         =   pd.merge(df, dfT, on='Tarjeta', how='left')
            dfS         =   dfS.fillna(0)
            hoy         =   datetime.now()
            dfCredito   =   dfS[dfS['TipoTar'] == 1]
            dfDebito    =   dfS[dfS['TipoTar'] == 0] 
            tarjetasUnico = dfCredito[['Tarjeta','Inicio','Fin','Pago']].drop_duplicates().to_dict(orient='records')
            dfGraph     =   self.setIncomeGraphList(df ,dfIncome)
            if tarjetasUnico:
                for x in tarjetasUnico: 
                    responDa            = {}
                    anterior            = hoy - relativedelta(months=1)
                    mesAnterior         = datetime(day=int(x['Inicio']),month=anterior.month,year=anterior.year)
                    mesConcurre         = datetime(day=int(x['Fin']),   month=hoy.month,     year=hoy.year) 
                    DfDfm               = dfCredito[(dfCredito['Fecha']> mesAnterior) & (dfCredito['Fecha']< mesConcurre)]
                    DfDfs               = dfCredito[(dfCredito['Fecha']> mesConcurre)]
                    responDa['Tarjeta']  =  x['Tarjeta']
                    responDa['Pago']     =  float(DfDfm['Monto'].sum() or 0.0)
                    responDa['Cantidad'] =  float(DfDfm['Monto'].count() or 0.0)
                    responDa['Promedio'] =  float(np.nan_to_num(DfDfm['Monto'].mean()) or 0.0)

                    responDa['PagoSigu']     =  float(DfDfs['Monto'].sum() or 0.0)
                    responDa['CantidadSigu'] =  float(DfDfs['Monto'].count() or 0.0)
                    responDa['PromedioSigu'] =  float(np.nan_to_num(DfDfs['Monto'].mean()) or 0.0)

                    siguienteMes             = hoy +  relativedelta(months=1)
                    if x['Pago'] >= hoy.day:
                        responDa['FechaPago']     = datetime(day=int(x['Pago']),month=hoy.month,year=hoy.year).strftime('%Y-%m-%d') 
                    else:
                        responDa['FechaPago']     = siguienteMes.replace(day=int(x['Pago'])).strftime('%Y-%m-%d') 
 
                    ArrayReponse.append(responDa) 

            response['data']        = ArrayReponse
            response['Efectivo']    =       {
                                                'montoEfec':float(dfDebito['Monto'].sum()),
                                                'conteoEfec': float(dfDebito['Monto'].count()),
                                                'promEfec':float(dfDebito['Monto'].mean()) 
                                            }
            response['Graph']       =   dfGraph 
            return response
        except Exception as e:
            return {'status':500, 'Error':traceback.format_exc()}
        
    def getIncomeActive(self,idUser,conn):
        """
            Obtiene y ordena las predicciones de consumo por día.
            Parámetros:
                -   idUser(class) : Clase.
                -   conn (BBDD)   : Conexion de base de datos

            Retorna:
                -   Dataframe: Información 
        """
        listIncome  =   detail.getIncomeActive(idUser,conn)
        df          =   pd.DataFrame(listIncome)
        dfOrdenr    =   df.groupby('Date',as_index=False)['Monto'].sum().rename(
                                columns =  {  'Monto':'Total','Date':'dia' }
                            ).sort_values('dia')
        return  dfOrdenr

    def setIncomeGraphList(self, dfS ,dfIncome):
        """
            Genera el dataframe de salia para grafico.
            Parámetros:
                -   dfS(pandas)         :  dataframe, deudas.
                -   dfIncome (pandas)   :  dataframe, predic.
            Retorna:
                -   Dict: Información Graph
        """    
        response            =   dict(fecha = [],consumo = [],predic = [])
        #dfS['Fecha']       =   pd.to_datetime( dfIncome['Fecha']).dt.date
        #
        now                 =   datetime.now()
        inicio              =   now.replace(day=1)
        fin                 =   calendar.monthrange(now.year,now.month)[1]
        fin                 =   now.replace(day=fin,hour=23,minute=59)
        #
        dfIncome['dia']     =   pd.to_datetime( dfIncome['dia'])
        dfS                 =   dfS[(dfS['Fecha']>= inicio) & (dfS['Fecha']<= fin)]
        #
        dfS                 =   dfS.groupby('Fecha', as_index=False)['Monto'].sum()
        df_merge            =   pd.merge(dfS, dfIncome, left_on='Fecha', right_on='dia', how='right')        
        df_merge['Monto']   =   df_merge['Monto'].fillna(0)     
        df_merge['dia']     =   df_merge['dia'].dt.strftime('%Y-%m-%d')    
        response['fecha']   =   df_merge['dia'].to_list()
        response['consumo'] =   df_merge['Monto'].to_list()
        response['predic']  =   df_merge['Total'].to_list() 
        return  response
        
