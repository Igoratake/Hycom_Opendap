import xarray as xr
import numpy as np

#Este script baixa os dados do hycom para os períodos selecionados para o experimento GLBv0.08/expt_53.X

#Importante: Por conta da estruturas dos servidores OpenDAP, e preciso baixar o dado por cada passo de tempo para postriormente concaternar
#Para concatenar, selecionar os arquivos desejados e utilizar o CDO, portando, este processamento é melhor realizado numa máquina Linux.

#Comando: cdo cat <*.nc> <saidamodeloteste.nc>
expt = ['http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3',
        'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.2',
        'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.7',
        'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_92.8',        
        'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_92.9',
        'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_93.0',
        ]

#Parametros de entrada - Lembrando que as coordenadas deve ser passadas em WGS84 graus decimais
x = -73.575979
y = 11.552520

prof_ini = 0
prof_max = 1000

#Opcao para exportar area ao redor do ponto
#celulas ao redor. 0 para extrair apenas a localização mais proxima ao ponto
cell = 2
area = 0 + cell

for ex in expt:

  hycom = xr.open_dataset(ex,decode_times=False,decode_cf=False)
  
  if '_9' in ex:
    hycom['lon'] = hycom.lon-360
  
  #extraindo area ou pontos do HYCOM
  if area ==0:
    hycom = hycom.sel(lon=x, lat=y,method='nearest')
    hycom = hycom.sel(depth = slice(prof_ini,prof_max))
  
  if area >0:
    #matriz de distancias
    dist = ((hycom.lon-x)**2 + (hycom.lat-y)**2)**0.5
    #procurar pelo indice do modelo com as coordenadas mais proximas ao dado    
    ind = np.unravel_index(np.argmin(dist, axis=None), dist.shape)
    hycom = hycom.isel(lon=slice(ind[0]-area,ind[0]+area), lat=slice(ind[1]-area,ind[1]+area))
    hycom = hycom.sel(depth = slice(prof_ini,prof_max))  
  
  #dropando informações nao necessarias
  hycom = hycom.drop(['tau','surf_el','water_temp_bottom','salinity_bottom','water_u_bottom','water_v_bottom'])
  
  for i in list(range(0,len(hycom.time))):
  
    try:
      hyc = hycom.isel(time = i)
      hyc = hyc.load()
      hyc.to_netcdf('Hycom_Expt{}_{}.nc'.format(ex[-4:],i))
      
    except:
      pass
    
    