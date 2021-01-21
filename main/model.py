#######################################
## WEEKLY KPIs PRED FUNCTION        ##
#######################################

# Libraries
import pandas as pd
import numpy as np
import sys
from fbprophet import Prophet
import fbprophet.hdays as hdays_part2
import holidays as hdays_part1
import datetime
import random
from smartcapex.capacity.KPI_predictions_aux import get_fixed_prov_name, get_holidays_df
from smartcapex.capacity.prediction.forecasting.pred_prophet import make_pred


def get_avg_weekly_kpi_preds(df_celdas, celda, n_mcmc=0, period=52):
    '''Obtain weekly throughput, prb and traffic predictions for a specific cell using Prophet model.

    Parameters
    -----------
    df_celdas : DataFrame
        A DataFrame containing train data of a cell

    celda : str
        The name of a specific cell

    n_mcmc : int
        Number of Markov Chain Monte Carlo (MCMC) samples to train and predict (default is 0, then it will do MAP - Maximum a           posteriori estimation)

    period : int
        Number of weeks to predict in the future.

    Returns
    -----------
    DataFrame with columns:
        - Prediction from ocupacion_4g_throughput_dl
            pred_th_peak
            pred_th_low
            pred_th
            pred_th_trend
        - Prediction from ocupacion_4g_carga_prb
            pred_prb_peak
            pred_prb_low
            pred_prb
            pred_prb_trend
        - Prediction from trafico_4g_datos_dl
            pred_traffic_peak
            pred_traffic_low
            pred_traffic
            pred_traffic_trend

    The complete dataframe output would be:
        celda - Cell name
        despliegue - prophet regressor
        estacional  - Flag if it has seasonal traffic
        fecha_ampliacion - Ampliation date
        hist_meses - Number of months of real historic data
        hist_sint_ocupacion_4g_carga_prb  - Flag 1,0 to indicate if the data is synthetic o real
        hist_sint_ocupacion_4g_throughput_dl - Flag 1,0 to indicate if the data is synthetic o real
        hist_sint_trafico_4g_datos_dl - Flag 1,0 to indicate if the data is synthetic o real
        ocupacion_4g_carga_prb - Average cell PRB, variable to predict
        ocupacion_4g_throughput_dl - Average cell throughput, variable to predict
        trafico_4g_datos_dl - Average cell traffic , variable to predict
        pred_prb  - Prophet output
        pred_prb_low - Prophet output
        pred_prb_peak - Prophet output
        pred_prb_trend - Prophet output
        pred_th - Prophet output
        pred_th_low - Prophet output
        pred_th_peak - Prophet output
        pred_th_trend - Prophet output
        pred_traffic - Prophet output
        pred_traffic_low - Prophet output
        pred_traffic_peak - Prophet output
        pred_traffic_trend - Prophet output
    '''

    # Remove duplicates
    df_w = (df_celdas
            .loc[df_celdas.celda == celda]
            .drop_duplicates(['celda', 'dt'], keep='last')
            # .dropna()
            .drop(columns=['celda']))


    # Obtain holidays DataFrame
    holiday_years = [x for x in range(df_w.dt.min().year,
                                      pd.to_datetime(df_w.dt.max() + datetime.timedelta(weeks=period),
                                                     format='%Y-M-%D').year + 1)]
    holidays_df = get_holidays_df(year_list=holiday_years, country='ES', prov=get_fixed_prov_name(celda_name=celda),
                                  freq='W-MON')

    forecast_th = make_pred(df_w, kpi_col='ocupacion_4g_throughput_dl', kpi_out_pred_name='pred_th{}', holidays_df=holidays_df,
                            n_mcmc=n_mcmc, period=period, cap=None, floor=None)
    forecast_prb = make_pred(df_w, kpi_col='ocupacion_4g_carga_prb', kpi_out_pred_name='pred_prb{}', holidays_df=holidays_df,
                             n_mcmc=n_mcmc, period=period, cap=100, floor=0)
    forecast_tf = make_pred(df_w, kpi_col='trafico_4g_datos_dl', kpi_out_pred_name='pred_traffic{}', holidays_df=holidays_df,
                            n_mcmc=n_mcmc, period=period,cap=None, floor=None)
    # Join predictions
    preds = (forecast_th
             .join((df_w.set_index('dt')))
             .join(forecast_prb) 
             .join(forecast_tf)
             .assign(celda=celda))

    return preds

