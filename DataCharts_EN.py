#! ./env/Scripts/python.exe
# coding:utf-8
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict, Any
import json

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
            df['datetime'] = pd.to_datetime(df['Time'], unit='s',utc=True)
            df = df.sort_values('Time')  # 按时间排序
        
        return df
    
    def create_interactive_timeseries(self):
        """
        创建交互式时间序列图表
        """
        if self.df.empty or 'datetime' not in self.df.columns:
            print("May some data lost.")
            return
        
        # 资源字段列表
        resource_fields = ['gold', 'credits', 'freeXP', 'eliteXP', 
                          'steel', 'coal', 'paragonXP', 'recruitment_points']
        
        Translate_fields = {
            'gold': 'Doubloons',
            'credits':'Credits',
            'freeXP':'Free XP',
            'eliteXP':'Elite Commander XP', 
            'steel':'Steel',
            'coal':'Coal', 
            'paragonXP':'R&D Points',
            'recruitment_points':'Community Tokens'
        }
        
        # 确保所有资源字段都存在
        available_fields = {}
        available_fields[0] = [Translate_fields[str(field)] for field in resource_fields if field in self.df.columns]
        available_fields[1] = [field for field in resource_fields if field in self.df.columns]
        plots_title = ['Steel,Coal,R&D Points,Doubloons,Community Tokens','Free XP & Elite Commander XP','Credits']
        
        if not available_fields:
            print("May some data lost.")
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
            title="Resources",
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
        fig.update_xaxes(title_text="Time", col=1)
        
        fig.show()
        return fig

class DatFileViewer:
    text_str = {
        'title': 'RescourcesStatistics',
        'choose': 'Choose the player you want to see',
        'refresh': 'Refresh list',
        'generate': 'Generate',
        'warning': 'Warning',
        'warning_str': 'No \'[Player Name].dat\' file found, please open the game for a battle or open at least one container',
        'error': 'Error',
        'error_str': 'Error reading file:: '
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
        ttk.Button(main_frame, text=self.text_str['refresh'], command=self.load_dat_files).grid(row=0, column=2, padx=(5, 0), pady=5)

        # 加载图标按钮
        ttk.Button(main_frame, text=self.text_str['generate'], command=self.GenerateCharts).grid(row=5, column=2, padx=(5, 0), pady=5)
        
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

# 使用交互式图表示例
def interactive_visualization_example(FileName,LimtimeMin = 0,LimtimeMax = 999999999999):
    # 读取数据数据
    Resource_Data = Data_Read(FileName,LimtimeMin,LimtimeMax)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = DatFileViewer(root)
    root.mainloop()
    #print('Enter your Player Name:\n')
    #FileName = input() + '.dat'

    # print("=== Plotly 交互式图表 ===")
    #interactive_visualization_example(FileName)