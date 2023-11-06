import geopandas as gpd
import pandas as pd
from fiona.drvsupport import supported_drivers
import fiona

supported_drivers['kml'] = 'rw'  # enable KML support which is disabled by default
supported_drivers['KML'] = 'rw'  # enable KML support which is disabled by default
supported_drivers['LIBKML'] = 'rw'  # enable KML support which is disabled by default

fp = "S2A_MP_ACQ__KML_20230921T120000_20231009T150000.kml"
#print(fiona.listlayers(fp))
for layer in fiona.listlayers(fp):    
    if layer == "NOMINAL (#2)":      
        #print(layer)
        polys = gpd.read_file(fp, driver='LIBKML', layer=layer, engine = "fiona")#.set_crs(epsg=4326)
        #print(polys.head)

fp = "S2A_MP_ACQ__KML_20230907T120000_20230925T150000.kml"
for layer in fiona.listlayers(fp):    
    if layer == "NOMINAL":   
        polys2 = gpd.read_file(fp, driver='LIBKML', layer=layer, engine = "fiona")#.set_crs(epsg=4326)

fp = "S2B_MP_ACQ__KML_20230914T120000_20231002T150000.kml"
for layer in fiona.listlayers(fp):    
    if layer == "NOMINAL (#2)":   
        polys3 = gpd.read_file(fp, driver='LIBKML', layer=layer, engine = "fiona")

fp = "S2B_MP_ACQ__KML_20230928T120000_20231016T150000.kml"
for layer in fiona.listlayers(fp):    
    if layer == "NOMINAL (#2)":   
        polys4 = gpd.read_file(fp, driver='LIBKML', layer=layer, engine = "fiona")


polystot = gpd.GeoDataFrame(pd.concat([polys,polys2,polys3,polys4])) #polys.union(polys2)
print(len(polys),len(polys2),len(polys3),len(polys4),len(polystot)) 
polystot.to_file('polystot.geojson', driver='GeoJSON') 
polys3.to_file('polys3.geojson', driver='GeoJSON') 

ocean = "ocean.geojson"
mapocean = gpd.read_file(ocean)

count = 0
count2 = 0
for j in range(len(mapocean)):

    temp = mapocean.iloc[j].geometry
    result = polystot.intersects(temp)
    result2 = temp.intersects(polystot.geometry)

    if sum(result) > 0 :
        count += 1
    if sum(result2) > 0 :
        count2 += 1


print("\n Intersection are : "+str(count)+"\n")
print("\n Intersection2 are : "+str(count2)+"\n")

import matplotlib.pyplot as plt

"""
ax = (mapocean).plot(color="blue")
(polystot).plot(color="red",ax = ax)
(polystot.sjoin(mapocean)).plot(color="green",ax = ax)
plt.show()
"""

test = polystot.intersection(mapocean.geometry)
print(test)
count = 0
for j in range(len(mapocean)):
    temp = mapocean.iloc[j].geometry
    result = test.intersects(temp)
    if sum(result) > 0 :
        count += 1
print("\n Intersection are : "+str(count)+"\n")

################## With TILPAR map, a global worlds grid #######################

"""
tilpar = "S2A_OPER_GIP_TILPAR_MPC__20151209T095117_V20150622T000000_21000101T000000_B00.kml"
map = gpd.read_file(tilpar, driver='LIBKML', engine = "fiona").set_crs(epsg=4326)

count = 0
for j in range(len(map.Name)):
    temp = map.iloc[j].geometry #gpd.GeoSeries(map.iloc[j].geometry)
    result = polys.intersects(temp)
    count +=sum(result)
    
print(count)
"""

######################################################
