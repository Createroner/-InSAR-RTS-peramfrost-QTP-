from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn import model_selection
import pickle 

#  定义字典，便于来解析样本数据集txt
def Iris_label(s):
    it={b'1':1, b'2':2,b'3':3,b'4':4}
    return it[s]

path=r"F:\code\rf\data-exclude-velocity-environment.txt"
# path=r"F:\code\rf\data\pinjie\auxi\data.txt"
SavePath = r"F:\code\rf\data\pinjie\auxi\rd\modelPaper9-111111.pickle"


#  1.读取数据集
data=np.loadtxt(path, dtype=float, converters={9:Iris_label} )
#data=np.loadtxt(path,delimiter='    ', dtype=int )
print(data.shape)
#  converters={7:Iris_label}中“7”指的是第8列：将第8列的str转化为label(number)

#  2.划分数据与标签
x,y=np.split(data,indices_or_sections=(9,),axis=1) #x为数据，y为标签
x=x[:,0:15] #选取前7个波段作为特征
train_data,test_data,train_label,test_label = model_selection.train_test_split(x,y, random_state=1, train_size=0.7,test_size=0.3)

#  3.用100个树来创建随机森林模型，训练随机森林
classifier = RandomForestClassifier(n_estimators=150, 
                               bootstrap = True,
                               max_features = 'sqrt')
classifier.fit(train_data, train_label.ravel())#ravel函数拉伸到一维


#  4.计算随机森林的准确率
print("训练集：",classifier.score(train_data,train_label))
print("测试集：",classifier.score(test_data,test_label))

#  5.保存模型
#以二进制的方式打开文件：
file = open(SavePath, "wb")
#将模型写入文件：
pickle.dump(classifier, file)
#最后关闭文件：
file.close()

## conda acitvate 


## plot

# 画特征因子
tezhengLable=np.array(['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']) 


import matplotlib
import matplotlib.pyplot as plt
# feature importance
feature_importance = classifier.feature_importances_
feature_importance = 100.0 * (feature_importance / feature_importance.max())

sorted_idx = np.argsort(feature_importance)
pos        = np.arange(sorted_idx.shape[0]) + .5

plt.barh(pos, feature_importance[sorted_idx], align='center')
print(sorted_idx)
print(tezhengLable[sorted_idx])
print(sorted_idx)
plt.yticks(pos, tezhengLable[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()
