import openpyxl
import pandas as pd


def save_to_excel_sheet(data,path_excel,sheet_name,index=False):
    """将DataFrame数据存入指定excel的指定表格名称"""
    wb = openpyxl.load_workbook(path_excel)  # 将空白表格指定为wb
    writer = pd.ExcelWriter(path_excel, engine='openpyxl')  # 准备往空白表格写入数据
    writer.book = wb  # 执行写入目标为空白表格
    data.to_excel(writer, sheet_name=sheet_name,index=index)
    writer.save()
    writer.close()


if __name__=='__main__':
    pd.DataFrame().to_excel('原始数据/表格.xlsx', index=False)  # 创建空白表格，准备填入数据,index=False可以使保存的第一列非数字

    path_excel='原始数据/表格.xlsx'
    sheet_name='表格1'
    data=pd.DataFrame([1, 2, 3, 4, 5])
    save_to_excel_sheet(data,path_excel,sheet_name)

