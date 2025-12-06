try:
    import json
except:
	pass

# LimtimeMin = 1764068157     # 最早时间
# LimtimeMax = 1764070089     # 最晚时间
LimtimeMin = 0     # 最早时间
LimtimeMax = 999999999999     # 最晚时间

def Data_Read(limtimeMin = 0,limtimeMax = 9999999999):
    batch_size = 400        # 缓冲区大小
    records = []
    with open('data.dat', 'r', encoding='utf-8') as f:
        f.seek(0, 2)
        file_size = f.tell()
                
        buffer = ""
        position = file_size
                
        while position > 0:
            # 计算要读取的块大小
            chunk_size = min(batch_size, position)
            position = position - chunk_size
                    
            # 读取块
            f.seek(position)
            chunk = f.read(chunk_size) + buffer
                    
            # 分割行
            lines = chunk.split('#')
                    
            # 最后一个元素可能是部分行，保存到缓冲区
            buffer = lines[0]
            for line in reversed(lines[1:]):
                line = line.strip()
                if line:
                    try:
                        record = json.loads(line)
                        if (int(record['Time']) <= limtimeMax):
                            records.append(record)
                        if (int(record['Time']) <= limtimeMin):
                            return records
                    except:
                        pass
        if buffer.strip():
                    try:
                        record = json.loads(buffer)
                        records.append(record)
                    except json.JSONDecodeError:
                        pass
    return records

Resource_Data = Data_Read(LimtimeMin,LimtimeMax)

print(Resource_Data)
count = len(Resource_Data)
print(count)

MinTime = Resource_Data[0]['Time']
MaxTime = Resource_Data[count-1]['Time']
# 归一化
i = 0
while(i<count):
     Resource_Data[i]['Time'] = abs(float(Resource_Data[i]['Time'] - MinTime)/(MaxTime-MinTime))
     i = i + 1

print(Resource_Data)

'''
一些Main.py中用来调试的代码,用于收集wows中的SFM事件名称和数据
with open('SFMevent.txt','a') as file:
        file.write("Name: %s \n Data: %s \n"%(eventName,eventData))
        file.close()

        'up.exitGame' #退出游戏时触发
'''