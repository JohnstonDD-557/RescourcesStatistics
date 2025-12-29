try:
    import csv
except:
	pass

def Data_Convert(resource_data, output_file='data.csv'):
    if not resource_data:
        print("No data to write.")
        return
    
    # 获取字段名
    fieldnames = resource_data[0].keys()
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in resource_data:
            writer.writerow(data)
    
    print(f"Data successfully written to {output_file}")

from DataCharts import Data_Read
Resource_Data = Data_Read('LSOP.dat')
Data_Convert(Resource_Data, 'data.csv')