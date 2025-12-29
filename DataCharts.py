#! ./env/Scripts/python.exe
# coding:utf-8
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict, Any
import json
from struct import unpack, pack
import csv

import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class InteractiveResourceVisualizer:
    """
    交互式资源数据可视化工具
    使用Plotly生成可交互的图表
    """
    
    def __init__(self, records: List[Dict[str, Any]]):
        """
        初始化可视化工具
        
        Args:
            records: 资源记录列表
        """
        self.records = records
        self.df = self._create_dataframe()
    
    def _create_dataframe(self) -> pd.DataFrame:
        """
        将记录转换为Pandas DataFrame
        
        Returns:
            包含所有资源数据的DataFrame
        """
        if not self.records:
            return pd.DataFrame()
        
        # 转换为DataFrame
        df = pd.DataFrame(self.records)
        
        # 将时间戳转换为datetime对象
        if 'Time' in df.columns:
            df['datetime'] = pd.to_datetime(df['Time'] + 8*60*60, unit='s',utc=True)
            df = df.sort_values('Time')  # 按时间排序
        
        return df
    
    def create_interactive_timeseries(self):
        """
        创建交互式时间序列图表
        """
        if self.df.empty or 'datetime' not in self.df.columns:
            print("没有有效数据可绘制")
            return
        
        # 资源字段列表
        resource_fields = ['gold', 'credits', 'freeXP', 'eliteXP', 
                          'steel', 'coal', 'paragonXP', 'recruitment_points']
        
        Translate_fields = {
            'gold': '达布隆',
            'credits':'银币',
            'freeXP':'全局',
            'eliteXP':'舰长经验', 
            'steel':'钢',
            'coal':'煤', 
            'paragonXP':'研发点',
            'recruitment_points':'社区点数'
        }
        
        # 确保所有资源字段都存在
        available_fields = {}
        available_fields[0] = [Translate_fields[str(field)] for field in resource_fields if field in self.df.columns]
        available_fields[1] = [field for field in resource_fields if field in self.df.columns]
        plots_title = ['钢,煤,研发点,达布隆,社区点数','全局&舰长经验','银币']
        
        if not available_fields:
            print("没有找到资源字段")
            return
        
        # 创建子图
        fig = make_subplots(
            # rows=len(available_fields[1]), cols=1,
            rows=3, cols=1,
            subplot_titles=plots_title,
            vertical_spacing=0.05
        )
        
        # 为每个资源字段创建图表
        #银币 1
        row = 3
        #银币
        i = 1
        # 添加轨迹
        fig.add_trace(
            go.Scatter(
                x=self.df['datetime'],
                y=self.df[available_fields[1][i]],
                mode='lines+markers',
                name=available_fields[0][i],
                line=dict(width=2,color = "#000000"),
                marker=dict(size=4)
            ),
            row=row, col=1
        )
            
        # 更新Y轴标题
        fig.update_yaxes(title_text=available_fields[0][i], 
                        row=row, 
                        col=1,
                        tickformat=',d',
                        separatethousands=True,
                        rangemode = 'tozero',
                        showexponent='none')
        
        #全局&舰长经验 2 3
        row = 2
        # 全局
        i = 2
        # 添加轨迹
        fig.add_trace(
            go.Scatter(
                x=self.df['datetime'],
                y=self.df[available_fields[1][i]],
                mode='lines+markers',
                name=available_fields[0][i],
                line=dict(width=2,color = "#57ff8f"),
                marker=dict(size=4)
            ),
            row=row, col=1
        )
            
        # 更新Y轴标题
        fig.update_yaxes(title_text=available_fields[0][i], 
                        row=row, 
                        col=1,
                        tickformat=',d',
                        separatethousands=True,
                        rangemode = 'tozero',
                        showexponent='none')
        
        # 舰长经验
        i = 3
        # 添加轨迹
        fig.add_trace(
            go.Scatter(
                x=self.df['datetime'],
                y=self.df[available_fields[1][i]],
                mode='lines+markers',
                name=available_fields[0][i],
                line=dict(width=2,color = "#55c1ff"),
                marker=dict(size=4)
            ),
            row=row, col=1
        )
            
        # 更新Y轴标题
        fig.update_yaxes(title_text=available_fields[0][i], 
                        row=row, 
                        col=1,
                        tickformat=',d',
                        separatethousands=True,
                        rangemode = 'tozero',
                        showexponent='none')
        
        #钢,煤,研发点,达布隆,社区点数 4,5,6,7,0
        row = 1
        # 钢
        i = 4
        # 添加轨迹
        fig.add_trace(
            go.Scatter(
                x=self.df['datetime'],
                y=self.df[available_fields[1][i]],
                mode='lines+markers',
                name=available_fields[0][i],
                line=dict(width=2,color = "#8d8d8d"),
                marker=dict(size=4)
            ),
            row=row, col=1
        )
            
        # 更新Y轴标题
        fig.update_yaxes(title_text=available_fields[0][i], 
                        row=row, 
                        col=1,
                        tickformat=',d',
                        separatethousands=True,
                        rangemode = 'tozero',
                        showexponent='none')
        # 煤
        i = 5
        # 添加轨迹
        fig.add_trace(
            go.Scatter(
                x=self.df['datetime'],
                y=self.df[available_fields[1][i]],
                mode='lines+markers',
                name=available_fields[0][i],
                line=dict(width=2,color = "#222222"),
                marker=dict(size=4)
            ),
            row=row, col=1
        )
            
        # 更新Y轴标题
        fig.update_yaxes(title_text=available_fields[0][i], 
                        row=row, 
                        col=1,
                        tickformat=',d',
                        separatethousands=True,
                        rangemode = 'tozero',
                        showexponent='none')
        # 研发点
        i = 6
        # 添加轨迹
        fig.add_trace(
            go.Scatter(
                x=self.df['datetime'],
                y=self.df[available_fields[1][i]],
                mode='lines+markers',
                name=available_fields[0][i],
                line=dict(width=2,color = "#d1ce00"),
                marker=dict(size=4)
            ),
            row=row, col=1
        )
            
        # 更新Y轴标题
        fig.update_yaxes(title_text=available_fields[0][i], 
                        row=row, 
                        col=1,
                        tickformat=',d',
                        separatethousands=True,
                        rangemode = 'tozero',
                        showexponent='none')
        # 社区代币
        i = 7
        # 添加轨迹
        fig.add_trace(
            go.Scatter(
                x=self.df['datetime'],
                y=self.df[available_fields[1][i]],
                mode='lines+markers',
                name=available_fields[0][i],
                line=dict(width=2,color = "#d3d3d3"),
                marker=dict(size=4)
            ),
            row=row, col=1
        )
            
        # 更新Y轴标题
        fig.update_yaxes(title_text=available_fields[0][i], 
                        row=row, 
                        col=1,
                        tickformat=',d',
                        separatethousands=True,
                        rangemode = 'tozero',
                        showexponent='none')
        # 达布隆
        i = 0
        # 添加轨迹
        fig.add_trace(
            go.Scatter(
                x=self.df['datetime'],
                y=self.df[available_fields[1][i]],
                mode='lines+markers',
                name=available_fields[0][i],
                line=dict(width=2,color = "#ffbb00"),
                marker=dict(size=4)
            ),
            row=row, col=1
        )
            
        # 更新Y轴标题
        fig.update_yaxes(title_text=available_fields[0][i], 
                        row=row, 
                        col=1,
                        tickformat=',d',
                        separatethousands=True,
                        rangemode = 'tozero',
                        showexponent='none')
        
        # 更新布局
        fig.update_layout(
            height=300 * len(available_fields[1]),
            title="资源",
            title_font_size = 50,
            showlegend=True,
            hovermode='x unified',
            legend=dict(x = 0.5,
                        y = 1.1,
                        xanchor = 'center',
                        orientation= 'h',
                        yanchor='bottom'))
        
        
        # 更新X轴标题
        # fig.update_xaxes(title_text="时间", row=len(available_fields[1]), col=1)
        fig.update_xaxes(title_text="时间", col=1)
        
        fig.show()
        return fig

class DatFileViewer:
    text_str = {
        'title': '资源统计',
        'choose': '选择需要查看的玩家',
        'refresh': '刷新列表',
        'generate': '生成图像',
        'generateCSV': '转换CSV文件',
        'UpdateDat': '更新旧式dat文件',
        'warning': '提示',
        'warning_str': '没有找到\'[Player Name].dat\'文件,请先启动游戏进行一次战斗或开启一次补给箱',
        'error': '错误',
        'error_str': '读取文件时出错: '
    }
    def __init__(self, root):
        self.root = root
        self.root.title(self.text_str['title'])
        self.root.geometry("500x200")
        
        # 获取当前文件夹路径
        self.folder_path = os.path.abspath(".")
        
        # 创建界面元素
        self.create_widgets()
        
        # 加载.dat文件列表
        self.load_dat_files()
    
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 文件选择标签和下拉菜单
        ttk.Label(main_frame, text=self.text_str['choose']).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.selected_file = tk.StringVar()
        self.file_combo = ttk.Combobox(main_frame, textvariable=self.selected_file, state="readonly")
        self.file_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.file_combo.bind('<<ComboboxSelected>>')
        
        # 刷新按钮
        ttk.Button(main_frame, text=self.text_str['refresh'], command=self.load_dat_files).grid(row=0, column=3, padx=(5, 0), pady=5)

        # 加载图标按钮
        ttk.Button(main_frame, text=self.text_str['generate'], command=self.GenerateCharts).grid(row=5, column=3, padx=(5, 0), pady=5)
        
        # 转换CSV文件按钮
        ttk.Button(main_frame, text=self.text_str['generateCSV'], command=self.GenerateCSV).grid(row=5, column=2, padx=(5, 0), pady=5)
        
        # 更新旧式dat文件按钮
        ttk.Button(main_frame, text=self.text_str['UpdateDat'], command=self.UpdateDat).grid(row=5, column=0, padx=(5, 0), pady=5)

        # 配置网格权重
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def load_dat_files(self):
        """加载当前文件夹中的所有.dat文件"""
        try:
            # 获取所有.dat文件
            dat_files = [f for f in os.listdir(self.folder_path) if f.endswith('.dat')]
            
            if not dat_files:
                messagebox.showinfo(self.text_str['warning'],self.text_str['warning_str'])
                self.file_combo['values'] = []
                self.selected_file.set('')
            else:
                # 按文件名排序
                dat_files.sort()
                self.file_combo['values'] = dat_files
                # 默认选择第一个文件
                if dat_files:
                    self.selected_file.set(dat_files[0])
        
        except Exception as e:
            messagebox.showerror(self.text_str['error'], self.text_str['error_str']+str(e))
    
    def GenerateCharts(self):
        selected = self.selected_file.get()
        interactive_visualization_example(selected)

    def GenerateCSV(self):
        selected = self.selected_file.get()
        Data2CSV(selected)

    def UpdateDat(self):
        selected = self.selected_file.get()
        Data_Update(selected)


# 使用交互式图表示例
def interactive_visualization_example(FileName,LimtimeMin = 0,LimtimeMax = 999999999999):
    # 读取数据数据
    Resource_Data = dataRead_bytes(FileName,LimtimeMin,LimtimeMax)
    # print(Resource_Data)
    
    # 创建交互式可视化工具
    visualizer = InteractiveResourceVisualizer(Resource_Data)
    
    # 生成交互式时间序列图表
    # print("生成交互式时间序列图表...")
    visualizer.create_interactive_timeseries()
    

# 读取数据
def Data_Read(FileName,limtimeMin = 0,limtimeMax = 9999999999):
    batch_size = 400        # 缓冲区大小
    records = []
    with open(FileName, 'r', encoding='utf-8') as f:
        f.seek(0, 2)
        file_size = f.tell()
                
        buffer = ""
        position = file_size
                
        while position > 0:
            # 计算要读取的块大小
            chunk_size = min(batch_size, position)
            position -= chunk_size
                    
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

def Data2CSV(resource_Name):
    output_file = resource_Name.replace('.dat', '.csv')
    if not resource_Name:
        # print("No data to write.")
        return
    resource_data = dataRead_bytes(resource_Name)
    # 获取字段名
    fieldnames = resource_data[0].keys()
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in resource_data:
            writer.writerow(data)

def Data_Update(resource_Name):
    ######################################################################
    # 旧式文本文件结构(json格式)(每行以#分隔):
    # Time: unix时间戳
    # gold: 达布隆
    # credits: 银币
    # freeXP: 全局
    # eliteXP: 舰长经验
    # steel: 钢
    # coal: 煤
    # paragonXP: 研发点
    # recruitment_points: 社区点
    ######################################################################
    records = []
    try:
        with open(resource_Name, 'r', encoding='utf-8') as f:
            if (f.read(1) == '#'): # 文件以#开头，说明格式为旧格式，需要更新
                f.seek(0)
                # 对旧文件做备份
                f_bak = open(resource_Name + '.bak', 'w', encoding='utf-8')
                f_bak.write(f.read())
                f_bak.close()
                f.seek(0)
                for chuck in f:
                    lines = chuck.split('#')
                    for line in reversed(lines[1:]):
                        line = line.strip()
                        if line:
                            try:
                                record = json.loads(line)
                                records.append(record)
                            except json.JSONDecodeError:
                                pass
            else:
                return None  # 文件格式已是新格式，无需更新
    except UnicodeDecodeError:
        return None  # 文件格式已是新格式，无需更新

    # 写入二进制文件
    output_file = resource_Name
    with open(output_file, 'wb') as f:
        for record in records:
            packed_data = pack('>QQQQQQQQQ',
                                 record['Time'],
                                 record['gold'],
                                 record['credits'],
                                 record['freeXP'],
                                 record['eliteXP'],
                                 record['steel'],
                                 record['coal'],
                                 record['paragonXP'],
                                 record['recruitment_points'])
            f.write(packed_data)
    return None

if __name__ == "__main__":
    #Data_Update('Johnston_DD_557.dat')

    root = tk.Tk()
    app = DatFileViewer(root)
    root.mainloop()

    # print('输入你的玩家名:\n')
    # FileName = input() + '.dat'

    # print("=== Plotly 交互式图表 ===")
    # interactive_visualization_example(FileName)