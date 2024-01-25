#!/binibash
export PATH=/opt/conda/bin:$PATH
export ISCE_HOME=/home/ops/.conda/envs/isce2_env/lib/python3.8/site-packages/isce
export PATH=$PATH:$ISCE_HOME/applications:$ISCE_HOME/bin
export ISCE_STACK=/home/ops/isce2_code/isce2
export prepStackToStaMPS=/home/ops/isce2_code/isce2/contrib/timeseries/prepStackToStaMPS
export PATH=$prepStackToStaMPS/bin:/home/ops/isce2_code/isce2/contrib/stack/topsStack:$PATH
export PATH_ALOSSTACK=/home/ops/isce2_code/isce2/contrib/stack/alosStack
export PATH_ALOSSTACK=/home/ops/isce2_code/isce2/contrib/stack/topsStack
source /opt/conda/bin/activate
conda activate /home/ops/.conda/envs/isce2_env



# go to directory
frame=$1
cd $frame
#cd /data/sentinel/114-9/

# mkdir run directory
mkdir run

# revise DEM file absoult path
cd DEM
sed -i "84s#value.*demLat#value>`echo ${PWD}`\/demLat#g" `ls *.xml`

dem_wgs84=`ls *.wgs84`

# get DEM box
lat_min=$(awk -F " " '{print $1}' ll.txt)
lat_max=$(awk -F " " '{print $2}' ll.txt)
long_min=$(awk -F " " '{print $3}' ll.txt)
long_max=$(awk -F " " '{print $4}' ll.txt)


# go to run directory
cd ../
cd run

# create run_files
#echo `stackSentinel.py -s ../SLC/ -d ../DEM/$dem_wgs84 -a ../orbits/ -o ../orbits -b "$lat_min $lat_max $long_min $long_max" --coregistration geometry` | grep -o -P '(?<=South North East West).*(?= isce.log)' >> zlc.txt

box=`cat zlc.txt|grep -o -P '(?<= ).*(?= isce.log)'`

#stackSentinel.py -s ../SLC/ -d ../DEM/$dem_wgs84 -a ../orbits/ -o ../orbits -b "$box" -n 1 -c 2 --coregistration geometry -z 2 -r 4

#stackSentinel.py -s ../SLC/ -d ../DEM/$dem_wgs84 -a ../orbits/ -o ../orbits -b "34.5 34.71 92.8 93.2" -n 3 -c 2 --coregistration geometry -z 2 -r 4

# automatic run this run_files
cd run_files
# create run_all file
#ls `pwd`/run_* >>run_all
# cp run_all.py file

cp /data/run_ISCE.py ./

python run_ISCE.py run_all



#time series deformaiton extracting


cd ../
mkdir mintpy
cd mintpy
cp /data/FernandinaSenDT128.txt ./
smallbaselineApp.py FernandinaSenDT128.txt


# 
cd geo
timeseries2velocity.py geo_timeseries_tropHgt_ramp_demErr.h5 --poly 1 --period 1 -o velocity.h5
mask.py  velocity.h5 -m geo_maskTempCoh.h5 -o velocity_msk.h5
save_gdal.py velocity_msk.h5 -o geo_velocity.tif
save_gdal.py velocity_msk.h5 -d annualAmplitude -o annualAmplitude.tif 
save_gdal.py velocity_msk.h5 -d annualcoef_cos annualcoef_cos.tif
save_gdal.py velocity_msk.h5 -d annualcoef_sin -o annualcoef_sin.tif
save_gdal.py geo_temporalCoherence.h5
#save_gdal.py velocity_msk.h5 -d velocity -o geo_velocity_msk.tif

#mask.py  geo_velocity.h5   -m geo_temporalCoherence.h5  -t 0.7
#save_gmt.py geo_velocity_msk.h5  -o geo_vel_mask.grd
#save_gdal.py geo_velocity.h5 -o geo_velocity.tif --of GTiff

# save geo_makTempCoh.h5
#save_gdal.py geo_maskTempCoh.h5 -o geo_maskTempCoh.tif --of GTiff

# set null
#python /data/code/set_null.py geo_velocity.tif geo_maskTempCoh.tif trans_geo_velocity.tif
#export PATH="$PATH:/home/ops/isce2_code/isce2/contrib/stack/alosStack/"
#cp alosStack.xml ./
# export PATH_ALOSSTACK=/home/ops/isce2_code/isce2/contrib/stack/alosStack/
# cd /data
# #mkdir saf_d169_proc
# cd saf_d169_proc
# cp ../beiluhe_sig.sh ./
# #cp ${PATH_ALOSSTACK}/alosStack.xml ./
# python ${PATH_ALOSSTACK}/create_cmds.py -stack_par alosStack.xml
# ./cmd_1.sh
