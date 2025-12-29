API_VERSION = 'API_v1.0'
MOD_NAME = 'RescourcesStatistics'
MOD_PATH = utils.getModDir()
# CONFIG_PATH = '../../../../../profile'
DELAY_SEC = 2.5


try:
    import time
    import constants
    import utils
    import dataHub
    import events
    import devmenu
except:
	pass

ev_Name_entity = ['filters.finishedUpgradeableInit']    #启动游戏后玩家各项数据初始化完毕的SFM事件,用于更新玩家ID信息
entity = dataHub.getSingleEntity('accountResource')

FileName = 'data.dat'
res_Upgrade_Time = 0
res_Upgrade_Flag = False
    
# Resource_struct = {
#     'Count': 0,     # 读取的资源记录数量
#     'Resource':{},  # 资源数据
# }

Resource_struct = {
    'Time': 0,                  # 时间
    'gold': 0,                  # 达布隆
    'credits': 0,               # 银币
    'freeXP': 0,                # 全局
    'eliteXP': 0,               # 舰长经验
    'steel': 0,                 # 钢
    'coal': 0,                  # 煤
    'paragonXP': 0,             # 研发点
    'recruitment_points': 0,    # 社区点
}


def Load_PlayerData(eventName = None,eventData = None):  # 等待游戏基本数据加载完毕后再读取,避免读取不到玩家信息
    Name_entity = dataHub.getSingleEntity('accountName')
    PlayerName = str(Name_entity[constants.UiComponents.accountName].name)
    global FileName
    FileName = PlayerName +'.dat'
    # FileName = PlayerName +'.csv'

def read_resourceData(eventName = 'eventName',eventData = None):
    if eventName in ev_Name_entity:
        Load_PlayerData()
        Load_resevent()

    global res_Upgrade_Time,res_Upgrade_Flag
    isrelpay = Resource_struct['gold'] + Resource_struct['credits'] + Resource_struct['freeXP'] + Resource_struct['steel'] + Resource_struct['coal'] + Resource_struct['paragonXP'] + Resource_struct['recruitment_points']
    if (isrelpay != 0):
        if (res_Upgrade_Flag):
            if(time.time() - res_Upgrade_Time>DELAY_SEC):
                resStatistics_update()
                res_Upgrade_Flag = False

def Load_resevent(*args, **kwargs):
    entity_Id = constants.UiComponents.accountResource
    entity[entity_Id].evChangedGold.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedCredit.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedFreeXP.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedEliteXP.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedSteel.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedCoal.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedRecruitmentPoints.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedParagonXP.add(read_resourceData_ResChanged)

def read_resourceData_ResChanged(*args, **kwargs):
    Load_PlayerData()
    entity_Id = constants.UiComponents.accountResource
    global res_Upgrade_Time,res_Upgrade_Flag
    res_Upgrade_Time = time.time()
    res_Upgrade_Flag = True
    Resource_struct['Time'] = int(res_Upgrade_Time)
    Resource_struct['gold'] = entity[entity_Id].gold if entity[entity_Id] else 0
    Resource_struct['credits'] = entity[entity_Id].credits if entity[entity_Id] else 0
    Resource_struct['freeXP'] = entity[entity_Id].freeXP if entity[entity_Id] else 0
    Resource_struct['eliteXP'] = entity[entity_Id].eliteXP if entity[entity_Id] else 0
    Resource_struct['steel'] = entity[entity_Id].steel if entity[entity_Id] else 0
    Resource_struct['coal'] = entity[entity_Id].coal if entity[entity_Id] else 0
    Resource_struct['paragonXP'] = entity[entity_Id].paragonXP if entity[entity_Id] else 0
    Resource_struct['recruitment_points'] = entity[entity_Id].recruitment_points if entity[entity_Id] else 0

def resStatistics_update():
    x = Resource_struct
    if utils.isFile(MOD_PATH  + '/' + FileName):
        with open(FileName,'ab') as file:
            # file.write('#' + utils.jsonEncode(Resource_struct['Resource'][0]))
            Byte_struct = int2Bytes(x['Time'])+int2Bytes(x['gold']) +\
                            int2Bytes(x['credits'])+int2Bytes(x['freeXP']) + int2Bytes(x['eliteXP'])+int2Bytes(x['steel'])+\
                            int2Bytes(x['coal'])+int2Bytes(x['paragonXP']) + int2Bytes(x['recruitment_points'])
            for byte_val in Byte_struct:
                # 使用chr()将整数转换为字节(Python 2)
                file.write(chr(byte_val))
            file.close()
    else:
        with open(FileName,'wb') as file:
            # file.write('#' + utils.jsonEncode(Resource_struct['Resource'][0]))
            # file.write('Time,Gold,Credits,FreeXP,EliteXP,Stell,Coal,R&D Point,CommiuntyPoint\n')
            # file.write('{},{},{},{},{},{},{},{},{}\n'.format(x['Time'], x['gold'], x['credits'], x['freeXP'], x['eliteXP'], x['steel'], x['coal'], x['paragonXP'], x['recruitment_points']))
            Byte_struct = int2Bytes(x['Time'])+int2Bytes(x['gold']) +\
                            int2Bytes(x['credits'])+int2Bytes(x['freeXP']) + int2Bytes(x['eliteXP'])+int2Bytes(x['steel'])+\
                            int2Bytes(x['coal'])+int2Bytes(x['paragonXP']) + int2Bytes(x['recruitment_points'])
            for byte_val in Byte_struct:
                # 使用chr()将整数转换为字节(Python 2)
                file.write(chr(byte_val))
            file.close()

def int2Bytes(value):
    # 确保数字在64位范围内
    num = value & 0xFFFFFFFFFFFFFFFF
    
    # 提取每个字节
    return [
            (num >> 56) & 0xFF,
            (num >> 48) & 0xFF,
            (num >> 40) & 0xFF,
            (num >> 32) & 0xFF,
            (num >> 24) & 0xFF,
            (num >> 16) & 0xFF,
            (num >> 8) & 0xFF,
            (num >> 0) & 0xFF,
        ]

events.onSFMEvent(read_resourceData)