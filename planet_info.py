from PyAstronomy import pyasl
import  numpy as np

nexa = pyasl.NasaExoplanetArchive()

cols = nexa.availableColumns()
print()

raw_data:np.recarray = nexa.getAllData()
is_not_nan = ~np.isnan(raw_data['pl_orbincl'])
data = raw_data[is_not_nan]
print(data)