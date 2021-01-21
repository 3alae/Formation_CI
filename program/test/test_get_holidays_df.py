import unittest

from program.get_holidays_df import get_holidays_df

class TestGet_holidays_df(unittest.Testcase):

	def test_get_holidays_df(self):

		year = 2020
		country = 'ES'

		result = get_holidays_df(year,country)

		a=True
		
		if len(result)==0:
			a = False
		m = 'test failed'
		self.assertTrue(a,m)
