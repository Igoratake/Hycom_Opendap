#!/bin/bash

for D in *; do
    if [ -d "${D}" ]; then
        echo "${D}" 
        cdo cat "${D}"/*.nc "${D}"/teste.nc
        cdo sorttimestamp "${D}"/teste.nc "${D}"/sort_teste.nc
    fi
done