
import unittest 
from model import get_avg_weekly_kpi_preds
from program.model.make_pred import make_pred
from program.model.get_holidays_df import get_holidays_df
from program.model.get_fixed_prov_name import get_fixed_prov_name

class TestGet_avg_weely_kpi_preds(unittest.Testcase):

	def test_get_avg_weekly_kpi_preds(self):

	# When 
	# Build a fake dataframe
	dt_begin = dt.datetime(year=1985, month=10, day=25) 
	date_list = [dt_begin + dt.timedelta(days = day) for day in range(1000)] 
	df_data = pd.DataFrame({ 'celda': ['CELL_A'] * 1000, 'dt': date_list, 'ocupacion_4g_carga_prb': np.arange(0, 100, 0.1), 'ocupacion_4g_throughput_dl': np.arange(50, 75, 0.025) + 2 * np.sin(2.0 * np.pi / 10.0 * np.arange(0, 100, 0.1)) + 20 * np.sin(2.0 * np.pi / 200.0 * np.arange(0, 100, 0.1)) + np.random.normal(scale = 1, size = 1000), 'trafico_4g_datos_dl': np.arange(0, 100, 0.1), 'estacional': [False] * 1000, 'fecha_ampliacion': [pd.NaT] * 1000, 'hist_meses': [20.0] * 1000 }) 
	# Do 
	# Extract data for training 
	df_train = df_data[:800] 
	# Build the model 
	result = get_avg_weekly_kpi_preds( df_train, celda='CELL_A', n_mcmc=0, period=50)

	a = True

	if len(result)==0:
		a = False
	
	m = 'test failed'
	
	self.assertTrue(a,m)