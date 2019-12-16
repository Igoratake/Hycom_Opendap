import xarray as xr

#Este script baixa os dados do hycom para os períodos selecionados para o experimento GLBv0.08/expt_53.X

#Importante: Por conta da estruturas dos servidores OpenDAP, é preciso baixar o dado por cada passo de tempo par postriormente concaternar
#Para concatenar, selecionar os arquivos desejados e utilizar o CDO, portando, este processamento é melhor realizado numa máquina Linux.

#Comando: cdo cat <*.nc> <saidamodeloteste.nc>

#Parametros de entrada - Lembrando que as coordenadas deve ser passadas em WGS84 graus decimais
ano_ini = 2011
ano_fin = 2015

xmin = -42
xmax = -40

ymin = -24.5
ymax = -22.5

prof_ini = 0
prof_max = 500

for ano in list(range(ano_ini,ano_fin+1)):

  path =  'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_53.X/data/{}'.format(ano)
  
  hycom = xr.open_dataset(path,decode_times=False,decode_cf=False)
  
  hycom = hycom.sel(lon=slice(xmin,xmax), lat=slice(ymin,ymax),depth = slice(prof_ini,prof_max))
  hycom = hycom.drop(['tau','surf_el','water_temp','salinity','water_temp_bottom','salinity_bottom','water_u_bottom','water_v_bottom'])
  
  for i in list(range(0,len(hycom.time))):
  
    try:
      hyc = hycom.isel(time = i)
      hyc = hyc.load()
      hyc.to_netcdf('MF_Maromba_Expt53_{}_{}.nc'.format(i,ano))
      
    except:
      pass
  
    