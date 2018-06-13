# prisma-project
- 目标：运用深度学习方法对普通照片进行处理，模仿出著名艺术家画作的风格 
- 开发平台：：Linux操作系统、QT Creator和PyCharm
- 需要模块：PyQt4，TensorFlow
- 要求：处理效果好、实时、可选风格多样 

### 实现方法

- 风格迁移

![](https://github.com/songh1024/prisma-project/blob/master/images/results/%E5%9B%BE%E7%89%871.png?raw=true)

<center>Style + Content = styled content </center>

<center>a.针对每个可选风格，训练出相应的CNN模型 </center>

<center>b.训练好的模型可将输入内容图像的风格变成选定的风格 </center>

- 系统结构

![](https://github.com/songh1024/prisma-project/blob/master/images/results/%E5%9B%BE%E7%89%872.png?raw=true)

<center>生成网络：ResNet</center>

<center>损失网络：VGGNet</center>

### 程序演示

![](https://github.com/songh1024/prisma-project/blob/master/images/results/%E5%9B%BE%E7%89%873.png?raw=true)