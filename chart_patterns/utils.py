"""
Date  : 2023-12-25
Author: Zetra Team

"""


import numpy as np 
import pandas as pd
import sys

from typing import Union

def columns_message(msg: str) -> None:
        print(f"No `{msg.title()}` or `{msg}` price column ")
        sys.exit() 

def check_ohlc_names(ohlc: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """
    Check if the OHLC dataframe has the open, high, low and close columns
  
    :params ohlc is a dataframe with Open, High, Low, Close data
    :type :pd.DataFrame        
    
    :return (Union[pd.DataFrame, None])
    """
    
    for name in ["open", "high", "low", "close"]:
        if ohlc.columns.str.lower().str.contains(name).sum() == 0:
                columns_message(name)
        else:
            
            result = ohlc.columns.str.lower().str.contains(name).tolist()
            index  = np.where(result)[0][0] 
            column = ohlc.columns[index]
            ohlc.rename(columns = {column: name }, inplace=True)

            
    return ohlc