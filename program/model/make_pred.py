#######################################
## PRB HORA CARGADA PRED FUNCTION    ##
#######################################

# Libraries
import os

import pandas as pd
import numpy as np
from fbprophet import Prophet
import datetime
import random
from program.model.get_fixed_prov_name import get_fixed_prov_name
from program.model.get_holidays_df import get_holidays_df


class suppress_stdout_stderr(object):
    """
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    """
    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        for fd in self.null_fds + self.save_fds:
            os.close(fd)


def make_pred(df_w, kpi_col, kpi_out_pred_name, holidays_df, n_mcmc=0, period=52, cap=None, floor=None):
    # Indicate number changepoints

    if len(df_w) < 100:
        algorithm = 'Newton'
        changepoints = int(len(df_w) / 2)
    else:
        algorithm = 'LBFGS'
        changepoints = int(len(df_w) / 4)

    has_ampliation = False
    has_historic = False

    hist_sint_cols = [col for col in df_w.columns if 'hist_sint' in col]
    kpi_col_hist_sint_cols = [col for col in hist_sint_cols if kpi_col in col]
    kpi_col_hist=None
    if len(kpi_col_hist_sint_cols)>0:
        kpi_col_hist=kpi_col_hist_sint_cols[0]
        if any(df_w[kpi_col_hist]==1):
            has_historic = True

    yearly_seasonality= df_w.hist_meses.max() >= 12
    if yearly_seasonality:
        model_prophet = Prophet(uncertainty_samples=100
                              , yearly_seasonality=True
                              , weekly_seasonality=False
                              , daily_seasonality=False
                              , mcmc_samples=n_mcmc
                              , holidays=holidays_df
                              , n_changepoints=changepoints
                              )
    else:
        model_prophet = Prophet(uncertainty_samples=100
                                , yearly_seasonality=False # Si se pasa como variable coge fourier order 1 ¿?¿?
                                , weekly_seasonality=False
                                , daily_seasonality=False
                                , mcmc_samples=n_mcmc
                                , holidays=holidays_df
                                , n_changepoints=changepoints
                                )

    prophet_cols=[kpi_col,'dt']
    if (df_w['fecha_ampliacion'].isnull().any() == 0) & (df_w['estacional'].any() == False):
        # We ignore the cells which have a seasonability equal to true because we want to be sure that the regressor
        # is the origin of the traffic change
        has_ampliation = True

        fecha_ampliacion = df_w.fecha_ampliacion.values[0]
        # Obtain regressor
        df_w['despliegue'] = np.where(df_w.dt >= fecha_ampliacion, 1, 0)

        # Setup model
        model_prophet.yearly_seasonality=True
        # Add regressor
        model_prophet.add_regressor('despliegue', prior_scale=10000)
        model_prophet.seasonality_prior_scale=0.01
        prophet_cols.append('despliegue')

    if has_historic:
        fecha_historico = max(df_w[df_w[kpi_col_hist]==1].dt)
        model_prophet.add_regressor(kpi_col_hist)
        prophet_cols.append(kpi_col_hist)

    df_w = df_w.reset_index()[prophet_cols]

    df_w=df_w.rename(columns={kpi_col: 'y', 'dt': 'ds'})
    if cap is not None:
        df_w=df_w.assign(cap=cap)
    if floor is not None:
        df_w=df_w.assign(floor=floor)

    # Set seed
    random.seed(123)

    # Fit model
    with suppress_stdout_stderr():
        model_prophet.fit(df_w, algorithm=algorithm)
    # Obtain future data
    future = model_prophet.make_future_dataframe(periods=period, freq='W-MON')
    if cap is not None:
        future = future.assign(cap=cap)
    if floor is not None:
        future  = future.assign(floor=floor)


    # Prophet allows saturating Forecasts but tests done at the begining of 2019 but with bad results
    # https://facebook.github.io/prophet/docs/saturating_forecasts.html

    if has_ampliation:
        # Add regressor
        future['despliegue'] = np.where(future.ds >= fecha_ampliacion, 1, 0)
    if has_historic:
        future[kpi_col_hist] = np.where(future.ds > fecha_historico, 0, 1)


    # Predict KPI
    pred_kpi = model_prophet.predict(future)


    forecast_kpi = (pred_kpi
                      [['ds', 'yhat_upper', 'yhat_lower', 'yhat', 'trend']]
                      .set_index('ds')
                      .rename(columns={'yhat_upper': kpi_out_pred_name.format('_peak')
                                     , 'yhat_lower': kpi_out_pred_name.format('_low')
                                     , 'yhat': kpi_out_pred_name.format("")
                                     , 'trend': kpi_out_pred_name.format('_trend')}))

    return forecast_kpi

