import  numpy as np
import  astropy.units as u
import  astroquery.gaia
from astropy.coordinates import SkyCoord
from    PyAstronomy import pyasl
from    astroquery.gaia import Gaia
from    astroquery.simbad import Simbad

nexa = pyasl.NasaExoplanetArchive()

cols = nexa.availableColumns()

raw_data: np.recarray = nexa.getAllData()  # Replace with your actual data retrieval method
unique_hostnames, unique_indices = np.unique(raw_data['hostname'], return_index=True)
raw_data_1 = raw_data[unique_indices]
is_not_nan = ~np.isnan(raw_data_1['pl_orbincl'])
filtered_data = raw_data_1[is_not_nan]
names = ["hostname", "pl_name", "sy_dist", "ra", "dec", "pl_orbincl"]
fields_to_keep = [name for name in filtered_data.dtype.names if name in names]
new_dtype = np.dtype([(name, filtered_data.dtype[name].type) for name in fields_to_keep] + [('pseudocolour', 'O')])
final_data = np.empty(filtered_data.shape, dtype=new_dtype)
for name in fields_to_keep:
    final_data[name] = filtered_data[name]
    
final_csv = np.empty(2000*50, dtype=final_data.dtype)

for i in range(50):
    print(f"Retrieving information about Exoplanet {final_data[i]['pl_name']}")
    Gaia.ROW_LIMIT = 1999
    final_csv[i*1999 + i] = final_data[i]
    coord = SkyCoord(ra=final_data[i]['ra'], dec=final_data[i]['dec'], unit=(u.degree, u.degree), frame='icrs')
    j = Gaia.cone_search_async(coord, radius=u.Quantity(1.0, u.deg), columns=('designation', 'ra', 'dec', 'pseudocolour'))
    r = j.get_results()
    for j, row in enumerate(r):
        final_csv[i*2000 + j + 1]['hostname'] = row['DESIGNATION']
        final_csv[i*2000 + j + 1]['ra'] = row['ra']
        final_csv[i*2000 + j + 1]['dec'] = row['dec']
        final_csv[i*2000 + j + 1]['sy_dist'] = row['dist']
        final_csv[i*2000 + j + 1]['pseudocolour'] = row['pseudocolour']

np.savetxt('output.csv', final_csv, delimiter=',', fmt='%s', header=','.join(final_csv.dtype.names), comments='')