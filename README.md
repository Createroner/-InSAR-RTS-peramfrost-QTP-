## InSAR-RTS-Peramfrost-QTP
This is the repository for the paper "Satellite radar reveals permafrost thawing and slumping in the Ti-betan Plateau"
### InSAR process
#### SBAS-InSAR process
InSAR processing algorithms including ISCE (source: https://github.com/isce-framework/isce2, accessed on 19 April 2023) and MintPy (source: https://github.com/insarlab/MintPy, accessed on 19 April 2023) are open-source and freely available through Github.
#### HPC-SBAS-InSAR

### Random forest model
The random forst model is used to assessing slump-prone thawing permafrost.<br>

1、randomforest\dataset.txt: The created dataset for assessing slump-prone thawing permafrost. <br>

2、randomforest\Train.py: Train code for random forest. <br>

3、randomforest\Predict.py: Predict code for random forest. <br>

4、randomforest\modelParameter.pickle: Model parameters for trained radom forest. <br>

### Then inventory of RTSs
1、RTSs\RTS-QTP.shp: the known RTSs in QTP provided from Luo (source:https://doi.org/10.5281/ zenodo.7309867, accessed on 19 April 2023). <br>

2、RTSs\NewDiscovery.shp: the newly discovered RTSs in QTP observed by our method.<br>
