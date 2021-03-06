import xarray as xr

#Este script baixa os dados do hycom para os per�odos selecionados para o experimento GLBv0.08/expt_53.X

#Importante: Por conta da estruturas dos servidores OpenDAP, � preciso baixar o dado por cada passo de tempo par postriormente concaternar
#Para concatenar, selecionar os arquivos desejados e utilizar o CDO, portando, este processamento � melhor realizado numa m�quina Linux.

#Comando: cdo cat <*.nc> <saidamodeloteste.nc>
expt = ['http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_92.8',        
        'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_92.9',
        'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_93.0',
        ]
        
        #'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3',
        #'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.2',
        #'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.7',

#Parametros de entrada - Lembrando que as coordenadas deve ser passadas em WGS84 graus decimais
xmin = -42
xmax = -40

ymin = -24.5
ymax = -22.5

prof_ini = 0
prof_max = 500

for ex in expt:

  hycom = xr.open_dataset(ex,decode_times=False,decode_cf=False)
  
  if '_9' in ex:
    hycom['lon'] = hycom.lon-360
  
  hycom = hycom.sel(lon=slice(xmin,xmax), lat=slice(ymin,ymax),depth = slice(prof_ini,prof_max))
  hycom = hycom.drop(['tau','surf_el','water_temp','salinity','water_temp_bottom','salinity_bottom','water_u_bottom','water_v_bottom'])
  
  for i in list(range(0,len(hycom.time))):
  
    try:
      hyc = hycom.isel(time = i)
      hyc = hyc.load()
      hyc.to_netcdf('Expt_{}_{}/MF_Maromba_Expt{}_{}.nc'.format(ex[-4:-2],ex[-1],ex[-4:],i))
      
    except:
      pass
    
    