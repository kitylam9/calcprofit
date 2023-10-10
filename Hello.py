import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(layout="wide")
#df = pd.DataFrame(np.random.randn(10, 5), columns=("col %d" % i for i in range(5)))
#edst.table(df)

DaySale=[]
AcceleratePrizePool=[]
RebatePrizePool=[]
projectOwner=[]
Mall=[]
HistorSale=[]
RebateBalance=[]
DayRebate=[]
RebatedHistory=[]
RemainingSale=[]
D1income=[]
NumOfDay=0
day1Sale=2300
DaySaleIncreaseRatio=1
currentAccumulated=0
genre ="指定日數"  
labelText=["當天銷售","加速獎池(當天銷售 * 加速獎池率)","返佣獎池 (當天銷售 *返佣獎池率)", "項目方收 (當天銷售 * 項目方率)", "商城收入", "歷史銷售", "返佣餘額", "當天返佣", "已返歷史","未返銷售", "D1收入"]    
def recalculate():
    i=0
    while currentAccumulated:
        if i > 0 :
            DaySale.append( DaySale[i-1]*DaySaleIncreaseRatio)
            HistorSale.append(DaySale[i-1]+HistorSale[i-1])
            DayRebate.append( RebatePrizePool[i-1] * RebateCoefficient)
            RebateBalance.append(RebatePrizePool[i-1]-DayRebate[i])
            RebatedHistory.append(DayRebate[i]+RebatedHistory[i-1])
            RemainingSale.append(HistorSale[i]- RebatedHistory[i])
            D1income.append(DayRebate[i]/HistorSale[i]*day1Sale)
        AcceleratePrizePool.append( DaySale[i]*AcceleratePrizePoolPercent)
        RebatePrizePool.append(DaySale[i]*RebatePrizePoolPercent)
        projectOwner.append( DaySale[i]*projectOwnerPercent)
        Mall.append( DaySale[i]*MallCost)
        i=i+1
        
with st.form("my_form"):
    col1, col2, col3, col4, col5  = st.columns(5)
    with col1:
        RebateCoefficient = st.number_input('返佣系數',min_value= 0.0, max_value= 1.0,value=0.01826)
    with col2:
        MallCost=st.number_input('商城成本',min_value=0.0,max_value=1.0,value=0.7) 
    with col3:
        AcceleratePrizePoolPercent=st.number_input('加速獎池率',min_value=0.0,max_value=1.0,value=0.08)
    with col4:    
        RebatePrizePoolPercent=st.number_input('返佣獎池率',0.0,1.0,0.15)
    with col5:
        projectOwnerPercent=st.number_input('項目方率',0.0,1.0,0.07)
        
    l2col1, l2col2, l2col3, l2col4, l2col5 = st.columns(5)
    with l2col1:
        DaySaleIncreaseRatio=st.number_input(label='日銷售增減比率',value=1.2)
    with l2col2:
        day1Sale=st.number_input('Day1銷售',value=2300)
        
    with l2col3: 
        genre = st.radio( "計算模式", [ "指定日數", "直致達標日子"])
        if genre == "指定日數": 
            NumOfDay=st.number_input('指定日數',min_value=1,value=100)
    with l2col4: 
        submitted = st.form_submit_button("Submit")
        if submitted:
            df = pd.DataFrame()
            if genre=="指定日數":
                DaySale.append(day1Sale)
                HistorSale.append(0)
                RebateBalance.append(0)
                DayRebate.append(0)
                RebatedHistory.append(0)
                RemainingSale.append(0)
                D1income.append(0)
                for i in range(NumOfDay):
                    if i > 0 :
                        DaySale.append( DaySale[i-1]*DaySaleIncreaseRatio)
                        HistorSale.append(DaySale[i-1]+HistorSale[i-1])
                        DayRebate.append( RebatePrizePool[i-1] * RebateCoefficient)
                        RebateBalance.append(RebatePrizePool[i-1]-DayRebate[i])
                        RebatedHistory.append(DayRebate[i]+RebatedHistory[i-1])
                        RemainingSale.append(HistorSale[i]- RebatedHistory[i])
                        D1income.append(DayRebate[i]/HistorSale[i]*day1Sale)
                    AcceleratePrizePool.append( DaySale[i]*AcceleratePrizePoolPercent)
                    RebatePrizePool.append(DaySale[i]*RebatePrizePoolPercent)
                    projectOwner.append( DaySale[i]*projectOwnerPercent)
                    Mall.append( DaySale[i]*MallCost)
                    new_row = pd.DataFrame({labelText[0]: DaySale[i] , labelText[1]: AcceleratePrizePool[i],  labelText[2]: RebatePrizePool[i],  labelText[3]: projectOwner[i], 
                                            labelText[4]:Mall[i],  labelText[5]:HistorSale[i], labelText[6]:RebateBalance[i], labelText[7]:DayRebate[i], labelText[8]:RebatedHistory[i],
                                            labelText[9]: RemainingSale[i],  labelText[10]:D1income[i]}, index=[1])
                    df = pd.concat([df, new_row], ignore_index=True) 
            else:
                recalculate()
    if submitted:
        edited_df = st.data_editor(df,  hide_index=False, num_rows="dynamic") 
