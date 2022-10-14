# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 11:56:43 2022

@author: zaloginv
"""

import openpyxl as xl
import re
from docxtpl import DocxTemplate as dt

def excel( xlname ):
    wb = xl.load_workbook(filename = xlname)
    ws = wb.active
    tuplexls = tuple(ws.rows) # набор кортежей с кортежами
    listxl = [] # список с кортежами (новыми) типа [(участок, приказ, ФИО), (участок, приказ, ФИО)...] или ДРУГИМ

    
    for tuplexl in tuplexls: # для каждого кортежа среди всех кортежей
        FIOs = tuplexl[1].value # часть кортежа с несколькими ФИО
        Order = tuplexl[2].value # часть кортежа с номером приказа
        FIOs_list = [] # пустой список для каждого кортежа
        Uch = (str(tuplexl[3].value)).split(' ')[0] # номер судебного участка
        
        if FIOs != None:
            FIOs_list = re.split(',|;| ,|, | , |; | ;| ; ', FIOs)
            for FIO_list in FIOs_list:
                kort = ( Order, FIO_list.strip(), Uch ) # формируем кортеж с ЛС и ФИО
                listxl.append(kort) # добавляем кортеж в список
                print(kort)
    return listxl
        

def word ( wordname, excel_work):
    count = 0
    for element in excel_work:
        doc = dt(wordname)
        count += 1
        context = {} # словаря для связывания
        context.update( order=element[0], dolg=element[1], dolg2=element[1], uch=element[2], uch2=element[2] ) # связываем значения из шаблона со значениями элемента списка
        doc.render(context) # подставляем в шаблон
        doc.save(f'res_mes/mes_{count}.docx')
        

def main():
    xlname = 'mes.xlsx'
    excel_work = excel(xlname)
    
    
    wordname = 'mes_template.docx'
    word(wordname, excel_work)
    
if __name__ == '__main__':
    main()