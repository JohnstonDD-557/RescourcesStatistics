try:
    import json
    from struct import unpack
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

def dataRead_bytes(FileName,limtimeMin = 0,limtimeMax = 9999999999):
    ######################################################################
    # 二进制文件结构(数值均以大端序存储):
    # Time: 8字节 (64位整数) unix时间戳
    # gold: 8字节 (64位整数)
    # credits: 8字节 (64位整数)
    # freeXP: 8字节 (64位整数)
    # eliteXP: 8字节 (64位整数)
    # steel: 8字节 (64位整数)
    # coal: 8字节 (64位整数)
    # paragonXP: 8字节 (64位整数)
    # recruitment_points: 8字节 (64位整数)
    ######################################################################
    record_size = 8 * 9  # 每条记录的字节数
    records = []
    with open(FileName, 'rb') as f:
        while True:
            bytes_data = f.read(record_size)
            if not bytes_data or len(bytes_data) < record_size:
                break
            
            # 解包数据
            unpacked_data = unpack('>QQQQQQQQQ', bytes_data)
            record = {
                'Time': unpacked_data[0],
                'gold': unpacked_data[1],
                'credits': unpacked_data[2],
                'freeXP': unpacked_data[3],
                'eliteXP': unpacked_data[4],
                'steel': unpacked_data[5],
                'coal': unpacked_data[6],
                'paragonXP': unpacked_data[7],
                'recruitment_points': unpacked_data[8],
            }
            
            if (record['Time'] <= limtimeMax):
                records.append(record)
            if (record['Time'] <= limtimeMin):
                return records
    return records

Resource_Data = dataRead_bytes('LSOP.dat',LimtimeMin,LimtimeMax)

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