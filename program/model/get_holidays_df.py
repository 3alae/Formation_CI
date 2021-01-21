### Functions to help make predictions of network occupancy KPIs (e.g. degraded traffic)
### Then format those predictions for submission

import pandas as pd
import glob
import pickle
import re
import numpy as np
import fbprophet.hdays as hdays_part2
import holidays as hdays_part1





def get_holidays_df(year_list, country, prov=None, freq='D'):
    """Make dataframe of holidays for given years, country and province.
   
    Parameters
    ----------
    year_list: list 
        a list of years
    
    country: str 
        country name
    
    prov: str
        province name
    
    freq: str
        frequency of data. By default is daily (D), but you can choose to make it weekly (W: starting on sunday or W-MON: starting on monday)
    
    Returns
    -------
    Dataframe 
        Contains 'ds' and 'holiday', which can directly feed to 'holidays' params in Prophet
    
    """
    try:
        holidays = getattr(hdays_part2, country)(years=year_list)
    except AttributeError:
        try:
            holidays = getattr(hdays_part1, country)(years=year_list, prov=prov)
        except AttributeError:
            raise AttributeError(
                "Holidays in {} are not currently supported!".format(country))
    holidays_df = pd.DataFrame(list(holidays.items()), columns=['ds', 'holiday'])
    holidays_df.reset_index(inplace=True, drop=True)
    holidays_df['ds'] = pd.to_datetime(holidays_df['ds'])
    
    if freq == 'W':
        holidays_df["day_of_week"] = holidays_df["ds"].dt.dayofweek
        holidays_df["days_since_monday"] = ((holidays_df["day_of_week"] + 1) % 7).apply(lambda x: pd.Timedelta(x,unit='D'))
        holidays_df["ds"] = holidays_df["ds"] - holidays_df["days_since_monday"]
    
    if freq == 'W-MON':
        holidays_df["day_of_week"] = holidays_df["ds"].dt.dayofweek
        holidays_df["days_since_monday"] = ((holidays_df["day_of_week"] + 7) % 7).apply(lambda x: pd.Timedelta(x,unit='D'))
        holidays_df["ds"] = holidays_df["ds"] - holidays_df["days_since_monday"]
    
    # Order by datetime
    holidays_df = (holidays_df
                   .sort_values('ds')
                   .reset_index())
    
    
    
    return (holidays_df[['ds', 'holiday']])

