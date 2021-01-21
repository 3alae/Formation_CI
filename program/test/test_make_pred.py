import unittest
from program.make_pred import make_pred
from program.get_holidays_df import get_holidays_df
from program.get_fixed_prov_name import get_fixed_prov_name

class Testmake_pred(unittest.Testcase):

	def test_make_pred(self):

	# Obtain holidays DataFrame
    holiday_years = [x for x in range(df_w.dt.min().year,
                                      pd.to_datetime(df_w.dt.max() + datetime.timedelta(weeks=period),
                                                     format='%Y-M-%D').year + 1)]
    holidays_df = get_holidays_df(year_list=holiday_years, country='ES', prov=get_fixed_prov_name(celda_name=celda),
                                  freq='W-MON')
    dt_begin = dt.datetime(year=1985, month=10, day=25) 
	date_list = [dt_begin + dt.timedelta(days = day) for day in range(1000)] 
	df_data = pd.DataFrame({ 'celda': ['CELL_A'] * 1000, 'dt': date_list, 'ocupacion_4g_throughput_dl': np.arange(50, 75, 0.025) + 2 * np.sin(2.0 * np.pi / 10.0 * np.arange(0, 100, 0.1)) + 20 * np.sin(2.0 * np.pi / 200.0 * np.arange(0, 100, 0.1)) + np.random.normal(scale = 1, size = 1000)}) 

	result = make_pred(df_data,'ocupacion_4g_throughput_dl','pred_ocu',holidays_df)
	
	a=True
	
	if len(result)==0:
			a = False
	m = 'test failed'

	self.assertTrue(a,m)
