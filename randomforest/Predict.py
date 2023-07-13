import numpy as np
import gdal
import pickle 
from sklearn.impute import SimpleImputer

#读取tif数据集
def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName+"文件无法打开")
    return dataset

#保存tif文件函数
def writeTiff(im_data,im_geotrans,im_proj,path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape
    #创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
    if(dataset!= None):
        dataset.SetGeoTransform(im_geotrans) #写入仿射变换参数
        dataset.SetProjection(im_proj) #写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i+1).WriteArray(im_data[i])
    del dataset

# origin
#RFpath = r"F:\code\rf\data\pinjie\auxi\rd\model.pickle"
#Landset_Path = r"F:\code\rf\data\pinjie\auxi\26\0607\rddata\26-band.tif"
#SavePath = r"F:\code\rf\data\pinjie\auxi\26\0607\rddata\2656-predict.tif"


RFpath = r"F:\code\rf\data\pinjie\auxi\rd\modelPaper9.pickle"
Landset_Path = r"F:\code\rf\data\pinjie\auxi\26\0607\rddata\26-band.tif"
SavePath = r"F:\code\rf\data\pinjie\auxi\26\0607\rddata\26-predict-9.tif"

dataset = readTif(Landset_Path)
Tif_width = dataset.RasterXSize #栅格矩阵的列数
Tif_height = dataset.RasterYSize #栅格矩阵的行数
Tif_geotrans = dataset.GetGeoTransform()#获取仿射矩阵信息
Tif_proj = dataset.GetProjection()#获取投影信息
Landset_data = dataset.ReadAsArray(0,0,Tif_width,Tif_height)

print('Landset_data shape : '+ str(Landset_data.shape))

################################################调用保存好的模型
#以读二进制的方式打开文件
file = open(RFpath, "rb")
#把模型从文件中读取出来
rf_model = pickle.load(file)
#关闭文件
file.close()
################################################用读入的模型进行预测
#  在与测试前要调整一下数据的格式
data = np.zeros((9,Landset_data.shape[1]*Landset_data.shape[2]))
for i in range(9):
    data[i] = Landset_data[i].flatten() 
data = data.swapaxes(0,1)
#  对调整好格式的数据进行预测
#pred = np.zeros((data.shape[0],data.shape[1]))
print("data shape :"+str(data.shape))
# data1 = data[0:50000000,:]
# data2 = data[50000000:100000000,:]
# data3 = data[100000000:150000000,:]
# data4 = data[150000000:200000000,:]
# data5 = data[200000000:250000000,:]
# data6 = data[250000000:300000000,:]
# data7 = data[300000000:350000000,:]
# data8 = data[350000000:,:]

imp_0 = SimpleImputer(missing_values=np.nan , strategy="constant" , fill_value=0)
data = imp_0.fit_transform(data)


# pred1 = rf_model.predict(data1)
pred = rf_model.predict(data)
# pred3 = rf_model.predict(data3)
# pred4 = rf_model.predict(data4)
# pred5 = rf_model.predict(data5)
# pred6 = rf_model.predict(data6)
# pred7 = rf_model.predict(data7)
# pred8 = rf_model.predict(data8)
print('suceesss-predict-----')



# pred[0:50000000,:]=pred1
# pred[50000000:100000000,:]=pred2
# pred[100000000:150000000,:]=pred3
# pred[150000000:200000000,:]=pred4
# pred[200000000:250000000,:]=pred5
# pred[250000000:300000000,:]=pred6
# pred[300000000:350000000,:]=pred7
# pred[350000000:,:]=pred8
print('success---')
#  同样地，我们对预测好的数据调整为我们图像的格式
pred = pred.reshape(Landset_data.shape[1],Landset_data.shape[2])
pred = pred.astype(np.uint8)

#  将结果写到tif图像里
writeTiff(pred,Tif_geotrans,Tif_proj,SavePath)