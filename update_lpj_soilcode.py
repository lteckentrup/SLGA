import xarray as xr
import pandas as pd
import numpy as np

df_LPJ_global = pd.read_csv('../lpj_guess_4.1/forcing/soil/soilmap_center_interpolated.dat',
                            delim_whitespace=True)
                            
### Median across all layers                            
# ds_SLGA_CLY = xr.open_dataset('CLY/CLY_median_EV.nc')
# ds_SLGA_SLT = xr.open_dataset('SLT/SLT_median_EV.nc')
# ds_SLGA_SND = xr.open_dataset('SND/SND_median_EV.nc')
# ds_SLGA_pHc = xr.open_dataset('pHc/pHc_median_EV.nc')

### Upper layer
ds_SLGA_CLY = xr.open_dataset('CLY/CLY_000_005_EV_halfdegree.nc')
ds_SLGA_SLT = xr.open_dataset('SLT/SLT_000_005_EV_halfdegree.nc')
ds_SLGA_SND = xr.open_dataset('SND/SND_000_005_EV_halfdegree.nc')
ds_SLGA_pHc = xr.open_dataset('pHc/pHc_000_005_EV_halfdegree.nc')

# Convert xarray dataset to pandas dataframe and drop ocean points (nan)
df_SLGA_CLY = ds_SLGA_CLY.to_dataframe().dropna().reset_index()
df_SLGA_SLT = ds_SLGA_SLT.to_dataframe().dropna().reset_index()
df_SLGA_SND = ds_SLGA_SND.to_dataframe().dropna().reset_index()
df_SLGA_pHc = ds_SLGA_pHc.to_dataframe().dropna().reset_index()

### Select Australia
df_LPJ_oz = df_LPJ_global[(df_LPJ_global['lon']>110) & (df_LPJ_global['lon']<160) &
                          (df_LPJ_global['lat']<-10)&(df_LPJ_global['lat']>-45)]

lons = df_LPJ_oz.lon
lats = df_LPJ_oz.lat

for lat, lon in zip(lats,lons):
    CLY_list = df_SLGA_CLY[(df_SLGA_CLY['lon']==lon) &
                           (df_SLGA_CLY['lat']==lat)].Band1.values.tolist()
    if len(CLY_list) == 0:
        pass
    else:
        CLY = df_SLGA_CLY[(df_SLGA_CLY['lon']==lon) &
                          (df_SLGA_CLY['lat']==lat)].Band1.iloc[0]/100
        SLT = df_SLGA_SLT[(df_SLGA_SLT['lon']==lon) &
                          (df_SLGA_SLT['lat']==lat)].Band1.iloc[0]/100
        SND = df_SLGA_SND[(df_SLGA_SND['lon']==lon) &
                          (df_SLGA_SND['lat']==lat)].Band1.iloc[0]/100
        pHc = df_SLGA_pHc[(df_SLGA_CLY['lon']==lon) &
                          (df_SLGA_pHc['lat']==lat)].Band1.iloc[0]

        ### convert pH CaCl to pH in water following Brennan and Bolland, 1998
        pHw = pHc/0.918 + 0.33556/0.918

        CLY = round(CLY,2)
        SLT = round(SLT,2)
        SND = round(SND,2)
        pHw = round(pHw,2)

        df_LPJ_global['clay'] = np.where((df_LPJ_global['lon']==lon) &
                                         (df_LPJ_global['lat']==lat),CLY,
                                         df_LPJ_global['clay'])

        df_LPJ_global['silt'] = np.where((df_LPJ_global['lon']==lon) &
                                         (df_LPJ_global['lat']==lat),SLT,
                                         df_LPJ_global['silt'])

        df_LPJ_global['sand'] = np.where((df_LPJ_global['lon']==lon) &
                                         (df_LPJ_global['lat']==lat),SND,
                                          df_LPJ_global['sand'])

        df_LPJ_global['pH'] = np.where((df_LPJ_global['lon']==lon) &
                                       (df_LPJ_global['lat']==lat),pHw,
                                       df_LPJ_global['pH'])

df_LPJ_global.to_csv('../lpj_guess_4.1/forcing/soil/soilmap_center_interpolated_SLGA_upperlayer.dat',
                     index=False, sep ='\t')
