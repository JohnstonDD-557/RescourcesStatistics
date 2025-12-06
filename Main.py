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
# import BigWorld, BWPersonality, Avatar
ev_Name_entity = ['filters.finishedUpgradeableInit']    #启动游戏后玩家各项数据初始化完毕的SFM事件,用于更新玩家ID信息
# ev_entity = ['action.LootboxProxy.openLootboxesByType','action.LootboxProxy.openLootboxes']     # 进行需要进行资源数值记录的事件 依次开箱(不限数量) 开启全部箱子

entity = dataHub.getSingleEntity('accountResource')
# Name_entity = dataHub.getSingleEntity('accountName')

FileName = 'data.dat'
res_Upgrade_Time = 0
res_Upgrade_Flag = False
    
Resource_struct = {
    'Count': 0,     # 读取的资源记录数量
    'Resource':{},  # 资源数据
}

Resource_struct['Resource'][0] = {
    'Time': 0,                  # 时间
    'gold': 0,                  # 达布隆
    'credits': 0,               # 银币
    'freeXP': 0,                # 全局
    'eliteXP': 0,               # 舰长经验
    'steel': 0,                 # 钢
    'coal': 0,                  # 煤
    'paragonXP': 0,             # 研发点
    'recruitment_points': 0,    # 社区代币
}


def Load_PlayerData(eventName = None,eventData = None):  # 等待游戏基本数据加载完毕后再读取,避免读取不到玩家信息
    Name_entity = dataHub.getSingleEntity('accountName')
    PlayerName = str(Name_entity[constants.UiComponents.accountName].name)
    global FileName
    FileName = PlayerName +'.dat'

def read_resourceData(eventName = 'eventName',eventData = None):
    if eventName in ev_Name_entity:
        Load_PlayerData()
        Load_resevent()

    global res_Upgrade_Time,res_Upgrade_Flag
    isrelpay = Resource_struct['Resource'][0]['gold'] + Resource_struct['Resource'][0]['credits'] + Resource_struct['Resource'][0]['freeXP'] + Resource_struct['Resource'][0]['steel'] + Resource_struct['Resource'][0]['coal'] + Resource_struct['Resource'][0]['paragonXP'] + Resource_struct['Resource'][0]['recruitment_points']        
    if (isrelpay != 0):
        if (res_Upgrade_Flag):
            if(time.time() - res_Upgrade_Time>DELAY_SEC):
                resStatistics_update()
                res_Upgrade_Flag = False

    if False:# eventName in ev_entity: # 之前利用SFM事件记录各项资源信息的代码,由于可以使用ev***Changed处理,此部分以弃用
        entity_Id = constants.UiComponents.accountResource
        Resource_struct['Resource'][0]['Time'] = int(time.time())
        Resource_struct['Resource'][0]['gold'] = entity[entity_Id].gold if entity[entity_Id] else 0
        Resource_struct['Resource'][0]['credits'] = entity[entity_Id].credits if entity[entity_Id] else 0
        Resource_struct['Resource'][0]['freeXP'] = entity[entity_Id].freeXP if entity[entity_Id] else 0
        Resource_struct['Resource'][0]['eliteXP'] = entity[entity_Id].eliteXP if entity[entity_Id] else 0
        Resource_struct['Resource'][0]['steel'] = entity[entity_Id].steel if entity[entity_Id] else 0
        Resource_struct['Resource'][0]['coal'] = entity[entity_Id].coal if entity[entity_Id] else 0
        Resource_struct['Resource'][0]['paragonXP'] = entity[entity_Id].paragonXP if entity[entity_Id] else 0
        Resource_struct['Resource'][0]['recruitment_points'] = entity[entity_Id].recruitment_points if entity[entity_Id] else 0
        
        isrelpay = Resource_struct['Resource'][0]['gold'] + Resource_struct['Resource'][0]['credits'] + Resource_struct['Resource'][0]['freeXP'] + Resource_struct['Resource'][0]['steel'] + Resource_struct['Resource'][0]['coal'] + Resource_struct['Resource'][0]['paragonXP'] + Resource_struct['Resource'][0]['recruitment_points'] 
            
        if (isrelpay != 0):     # 播放replay文件时也会获取一次各项资源,但返回空值所以若各项资源总和为0则认为是在播放replay文件,不进行记录 
            resStatistics_update()

def Load_resevent(*args, **kwargs): # 用于监听各项资源变化
    entity_Id = constants.UiComponents.accountResource
    entity[entity_Id].evChangedGold.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedCredit.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedFreeXP.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedEliteXP.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedSteel.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedCoal.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedRecruitmentPoints.add(read_resourceData_ResChanged)
    entity[entity_Id].evChangedParagonXP.add(read_resourceData_ResChanged)

def remove_resevent(*args, **kwargs): # 用于移除监听各项资源变化
    entity_Id = constants.UiComponents.accountResource
    entity[entity_Id].evChangedGold.remove(read_resourceData_ResChanged)
    entity[entity_Id].evChangedCredit.remove(read_resourceData_ResChanged)
    entity[entity_Id].evChangedFreeXP.remove(read_resourceData_ResChanged)
    entity[entity_Id].evChangedEliteXP.remove(read_resourceData_ResChanged)
    entity[entity_Id].evChangedSteel.remove(read_resourceData_ResChanged)
    entity[entity_Id].evChangedCoal.remove(read_resourceData_ResChanged)
    entity[entity_Id].evChangedRecruitmentPoints.remove(read_resourceData_ResChanged)
    entity[entity_Id].evChangedParagonXP.remove(read_resourceData_ResChanged)

def read_resourceData_ResChanged(*args, **kwargs):
    Load_PlayerData()
    entity_Id = constants.UiComponents.accountResource
    global res_Upgrade_Time,res_Upgrade_Flag
    res_Upgrade_Time = time.time()
    res_Upgrade_Flag = True
    Resource_struct['Resource'][0]['Time'] = int(res_Upgrade_Time)
    Resource_struct['Resource'][0]['gold'] = entity[entity_Id].gold if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['credits'] = entity[entity_Id].credits if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['freeXP'] = entity[entity_Id].freeXP if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['eliteXP'] = entity[entity_Id].eliteXP if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['steel'] = entity[entity_Id].steel if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['coal'] = entity[entity_Id].coal if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['paragonXP'] = entity[entity_Id].paragonXP if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['recruitment_points'] = entity[entity_Id].recruitment_points if entity[entity_Id] else 0
    


def read_resourceData_BattleQuit(eventFeedback):
    Load_PlayerData()
    entity_Id = constants.UiComponents.accountResource
    Resource_struct['Resource'][0]['Time'] = int(time.time())
    Resource_struct['Resource'][0]['gold'] = entity[entity_Id].gold if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['credits'] = entity[entity_Id].credits if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['freeXP'] = entity[entity_Id].freeXP if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['eliteXP'] = entity[entity_Id].eliteXP if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['steel'] = entity[entity_Id].steel if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['coal'] = entity[entity_Id].coal if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['paragonXP'] = entity[entity_Id].paragonXP if entity[entity_Id] else 0
    Resource_struct['Resource'][0]['recruitment_points'] = entity[entity_Id].recruitment_points if entity[entity_Id] else 0
    
    isrelpay = Resource_struct['Resource'][0]['gold'] + Resource_struct['Resource'][0]['credits'] + Resource_struct['Resource'][0]['freeXP'] + Resource_struct['Resource'][0]['steel'] + Resource_struct['Resource'][0]['coal'] + Resource_struct['Resource'][0]['paragonXP'] + Resource_struct['Resource'][0]['recruitment_points'] 
            
    if (isrelpay != 0):
        resStatistics_update()

def resStatistics_update():
    if utils.isFile(MOD_PATH  + '/' + FileName):
        with open(FileName,'a') as file:
            file.write('#' + utils.jsonEncode(Resource_struct['Resource'][0]))
            file.close()
    else:
        with open(FileName,'w') as file:
            file.write('#' + utils.jsonEncode(Resource_struct['Resource'][0]))
            file.close()


# devmenu.enable() #测试菜单,便于在不重启游戏的情况下重载mod

# events.onSFMEvent(Load_PlayerData)
# events.onBattleQuit(read_resourceData_BattleQuit)
events.onSFMEvent(read_resourceData)