# RescourcesStatistics

## 简介

这是各项文件的说明,mod的具体安装/使用方式请参阅[Readme_Mod.md](./Readme_Mod.md)\
Main.py:用来定期从WowsPythonAPI中获取玩家各项资源信息,并存储为```[玩家名].dat```文件\
Read.py:读取```[玩家名].dat```文件的基本示例\
DataCharts.py:读取```[玩家名].dat```并将其中的数据转换成统计图。\
DataCharts_EN.py:```DataCharts.py```的英文版

## 环境安装方式

1. 解压缩后在对应路径调出命令行(在地址栏输cmd)\
2. 输入 ```py -3.10 -m venv env && env\Scripts\activate.bat```
3. 输入 ```pip install -r requirements.txt``` 安装环境
4. 安装完成,可以在配置完脚本开头的路径之后直接双击 ```DataCharts.py``` 来进行测试了。

## 存储信息结构

dat文件中是以 ```#```为分割符的json格式数据,其中包含了
```Time```获取资源数据时的UNIX时间戳,
```gold```达布隆,
```credits```银币,
```freeXP```全局,
```eliteXP```舰长经验,
```steel```钢,
```coal```煤,
```paragonXP```研发点,
```recruitment_points```社区代币;8项数据,可以参考[```read.py```](./read.py)中的方式来进行读取。
