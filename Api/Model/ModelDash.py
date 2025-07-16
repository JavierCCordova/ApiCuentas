import Api.Model.Component.componentDash  as dash
import pandas as pd
from datetime import datetime, timedelta
import calendar
class ModelDash():

    def __init__(self):
        pass

        ## 
    def GetDataConsumption(self,userId, conn):
        try:
            listIncome  = dash.GetDataConsumption(userId,conn)
            response    = dict(MontoSemana = 0)
            responseData= dict(status = 200, data = {})
            dfIncome    = pd.DataFrame(listIncome)
            dfIncome['Fecha'] = pd.to_datetime( dfIncome['Fecha'])
            dfIncome['Mes']   = dfIncome['Fecha'].dt.month            
            hoy         = datetime.now()
            dfIncome    = dfIncome[dfIncome['Mes'] == hoy.month]
            lunes       = hoy - timedelta(days=hoy.weekday()) 
            domingo     = hoy + timedelta(days=6) 
            mes         = datetime.now().month 

            dfWeek      = dfIncome[(dfIncome['Fecha'] >= lunes) &  (dfIncome['Fecha']<= domingo)]

            dfResumen               =  dfIncome['Mes'].value_counts().sort_index().reset_index()
            dfResumen.columns       =  ['Mes','Cantidad']
            dfResumen['MesNombre']  =  dfResumen['Mes'].apply(lambda m : calendar.month_name[m])

            response['MontoSemana']  = sum(dfWeek['Monto'])
            response['CanSemana']    = dfWeek['Monto'].shape[0]
            response['CanMontoDia']  = dfIncome[ dfIncome['Fecha'] == hoy.strftime('%Y-%m-%d') ]['Monto'].shape[0]
            response['MontoDia']     = sum(dfIncome[ dfIncome['Fecha'] == hoy.strftime('%Y-%m-%d') ]['Monto'])
            response['CanGastosMes'] = dfIncome[( dfIncome['Fecha'].dt.month == mes)].shape[0]
            response['GastosMes']    = sum(dfIncome[( dfIncome['Fecha'].dt.month == mes)]['Monto'])

            for x in range(1,13):
                if x in dfResumen['Mes'].tolist(): 
                    continue
                else:
                    new =  {'Mes':x , 'Cantidad': 0, 'MesNombre': calendar.month_name[x]} 
                    dfResumen.loc[len(dfResumen)] = new

            dfResumen       =   dfResumen.sort_values(by='Mes').reset_index(drop=True)
            dfProducto      =   dfIncome.groupby('Producto',as_index=False)['Monto'].sum()
            
            response['graphGasto']  = {
                                        'Meses' : dfResumen['Cantidad'].tolist(),
                                        'Nombre': dfResumen['MesNombre'].tolist()
                                    }
            
            response['graphProc']   = {
                                        'Producto': dfProducto['Producto'].tolist(),
                                        'Cantidad': dfProducto['Monto'].tolist()
                                    }

            responseData['data'] = response

            return responseData
        except Exception as e:
            return { 'status': 500, 'data': f' Se tuvo problemas {str(e)}' }