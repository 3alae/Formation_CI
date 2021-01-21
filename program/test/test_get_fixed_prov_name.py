import unittest 
from program.get_fixed_prov_name import get_fixed_prov_name

class TestGet_fixed_prov_name(unittest.Testcase):

	def test_get_fixed_prov_name(self):

		cell_name = 'CAN'
		result = get_fixed_prov_name(cell_name)
		
		a=True

		if len(result)==0:
			a = False
		m = 'test failed'
		self.assertTrue(a,m)

