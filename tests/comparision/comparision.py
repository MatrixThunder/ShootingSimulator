from __future__ import print_function
import cv2
import numpy as np
MAX_MATCHES=500
GOOD_MATCH_PERCENT=0.15
def alignImages(im1,im2):
    # 将图像转换为灰度图
    im1Gray = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
    # 寻找ORB特征
    orb=cv2.ORB_create(MAX_MATCHES)
    keypoints1,descriptors1=orb.detectAndCompute(im1Gray,None)
    keypoints2,descriptors2=orb.detectAndCompute(im2Gray,None)
    # 匹配特征
    matcher=cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches=matcher.match(descriptors1, descriptors2,None)
    # 对特征进行排序
    matches.sort(key=lambda x:x.distance,reverse=False)
    # 移除不良特征
    numGoodMatches=int(len(matches)*GOOD_MATCH_PERCENT)
    matches=matches[:numGoodMatches]
    # 选取正确的特征
    imMatches=cv2.drawMatches(im1,keypoints1,im2,keypoints2,matches,None)
    cv2.imwrite("matches.jpg", imMatches)
    # 对特征进行定位
    points1=np.zeros((len(matches), 2),dtype=np.float32)
    points2=np.zeros((len(matches), 2),dtype=np.float32)
    for i,match in enumerate(matches):
      points1[i,:]=keypoints1[match.queryIdx].pt
      points2[i,:]=keypoints2[match.trainIdx].pt
    # 寻找矩阵
    h,mask=cv2.findHomography(points1,points2,cv2.RANSAC)
    # 使用矩阵
    height,width,channels =im2.shape
    im1Reg=cv2.warpPerspective(im1,h,(width, height))
    return im1Reg, h


if __name__ == '__main__':
    # 读取标准图像
    
    refFilename="../../images/testing/13.jpg"
    imReference=cv2.imread(refFilename)
    
    # 读取待对齐的图像
    imFilename="../../images/testing/14.png"
    im=cv2.imread(imFilename)
    print("正在对齐")
    imReg,h=alignImages(im,imReference)
    (x,y,z)=imReg.shape
    cv2.namedWindow('img',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img',int(y/2),int(x/2))
    cv2.imshow('img',imReg)
    cv2.waitKey(0)
    # 对齐后输出到本地 
    outFilename="aligned.jpg"
    print("将图片保存为: ",outFilename)
    cv2.imwrite(outFilename,imReg)
    # 输出映射矩阵
    print("映射矩阵为: \n",h)
cv2.destroyAllWindows()