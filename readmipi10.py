## read mipi10 raw to convert formats
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image

curPath = os.getcwd()
mipi10FilePath = os.path.join(curPath, 'mipi10')

mipi10Rows = 3072
mipi10Cols = 4096
## 4096 * 3072 size
for mipiFile in os.listdir(mipi10FilePath):
    if os.path.splitext(mipiFile)[1] == '.raw':
        imageFile = np.fromfile(os.path.join(mipi10FilePath, mipiFile), dtype="uint8")
        #print(imageFile.size) ## dtype shape ndim size是多少字节
        # 创建空的一维数组 存储转换后的数据
        tempMat = np.zeros(mipi10Rows * mipi10Cols,dtype='uint16')
        for index in range(0, imageFile.size//5):
            tempMat[index * 4 + 0] = (imageFile[index * 5 + 0] << 2) +  (imageFile[index * 5 + 4] & 0x3)
            tempMat[index * 4 + 1] = (imageFile[index * 5 + 1] << 2) + ((imageFile[index * 5 + 4] >> 2) & 0x3)
            tempMat[index * 4 + 2] = (imageFile[index * 5 + 2] << 2) + ((imageFile[index * 5 + 4] >> 4) & 0x3)
            tempMat[index * 4 + 3] = (imageFile[index * 5 + 3] << 2) + ((imageFile[index * 5 + 4] >> 6) & 0x3)
            # print("1_iamgeFile[%d] = %d "%(index * 5 + 0, imageFile[index * 5 + 0]))
            # print('2_tempMat[%d] = %d'%(index * 4 + 0,tempMat[index * 4 + 0]))
        ## 将转换后的一维数据 reshape成二维
        targetImage = tempMat.reshape(mipi10Rows, mipi10Cols)
        plt.title(mipiFile)
        plt.imshow(targetImage,cmap='gray', vmin=0, vmax=255)
        plt.show()
        outFilePath = os.path.join(mipi10FilePath,'translate') + '\\' + os.path.splitext(mipiFile)[0] + '.jpeg'
        image.imsave(outFilePath, targetImage, dpi = 300, cmap='gray')
        print('Current Progress: %s' % mipiFile)
    else:
        pass





