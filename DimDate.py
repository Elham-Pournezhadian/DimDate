!python -m pip install persiantools

### Please install persiantools first
### https://pypi.org/project/persiantools/


import numpy as np
import pandas as pd
from persiantools.jdatetime import JalaliDateTime as jdate
from persiantools import characters, digits
import datetime , pytz



startdate = '2000-01-01'
enddate = '2050-12-31'

def create_dimDate(start=startdate, end=enddate):
    ## Defining Standard date dim columns
    dimDate = pd.DataFrame({"Date": pd.date_range(start, end)})
    dimDate["year"] = dimDate.Date.dt.year.astype('int')
    dimDate["month"] = dimDate.Date.dt.month.astype('int')
    dimDate["month_name"] = dimDate.Date.dt.month_name()
    dimDate["day"] = dimDate.Date.dt.day.astype('int')
    dimDate["day_name"] = dimDate.Date.dt.day_name()
    dimDate["week"] = dimDate.Date.dt.week.astype('int')  
    dimDate["week_day"] = dimDate["day_name"]+dimDate["week"].map(str)
    #dimDate["week_day"] = dimDate["day_name"]+dimDate.Date.dt.week.map(str)
    dimDate["quarter"] = dimDate.Date.dt.quarter
    dimDate["year_half"] = (dimDate.quarter + 1) // 2
    
    ## day working status list:
    day_kind = []
    ## persian date lists:
    jalali_year  = []
    jalali_month = []
    jalali_day   = []
    jalali_date  = []
    jalali_week  = []
    jalali_year_month = []
    jalali_year_week  = []

   
    for row in dimDate.itertuples():
        
        ### Defining column for day working status
        if (row[1].day_name() == 'Thursday') or (row[1].day_name() == 'Friday'):    # Persian holidays
        #if (row[1].day_name() == 'Saturday') or (row[1].day_name() == 'Sunday'):    # Gregorian holidays
           
            day_kind.append('Weekend')
        else:
            day_kind.append('WorkDay')
        
            
        ## Defining Persian date dim columns
        year  = jdate.to_jalali(datetime.datetime(row[1].year, row[1].month, row[1].day)).year
        month = jdate.to_jalali(datetime.datetime(row[1].year, row[1].month, row[1].day)).month
        day   = jdate.to_jalali(datetime.datetime(row[1].year, row[1].month, row[1].day)).day
        date  = jdate(year,month,day).strftime('%Y/%m/%d')
        week  = jdate(year,month,day).week_of_year()
        year_month = year * 100 + month
        year_week  = str(year)+'-W' + str(week)
        jalali_year.append(year)
        jalali_month.append(month)
        jalali_day.append(day)
        jalali_date.append(date)
        jalali_week.append(week)
        jalali_year_month.append(year_month)
        jalali_year_week.append(year_week)

    
    month_list = [[1,'Far','فروردین'],[2,'Ord','اردیبهشت'],[3,'Khor','خرداد'],[4,'Tir','تیر'],[5,'Mor','مرداد'],[6,'Shah','شهریور']
                  ,[7,'Mehr','مهر'],[8,'Aban','آبان'],[9,'Azar','آذر'],[10,'Dey','دی'],[11,'Bah','بهمن'],[12,'Esf','اسفند']]
    month_list = pd.DataFrame(month_list, columns=['no','Jmonth_name_eng','Jmonth_name'])         
        
    dimDate["day_kind"] = day_kind
    dimDate["Jyear"] = jalali_year
    dimDate["Jmonth"] = jalali_month
    dimDate["Jday"] = jalali_day
    dimDate["Jdate"] = jalali_date
    dimDate["Jweek"] = jalali_week
    dimDate["Jyear_month"] = jalali_year_month    
    dimDate["Jyear_week"]  = jalali_year_week
    dimDate = dimDate.set_index('Jmonth').join(month_list.set_index('no'))
    dimDate['Jyear_month_name'] = dimDate['Jmonth_name'] +'-'+ dimDate['Jyear'].astype(str)

    
    return dimDate
    

dim = create_dimDate()
dim