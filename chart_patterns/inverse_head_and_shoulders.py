"""
Date   : 2023-01-09
Author : Zetra Team
Function used to detect inverse head and shoulders
"""

import numpy as np
import pandas as pd 
import plotly.graph_objects as go

from chart_patterns.chart_patterns.charts_utils import find_points
from chart_patterns.chart_patterns.pivot_points import find_all_pivot_points
from scipy.stats import linregress
from typing import Tuple


def find_inverse_head_and_shoulders(ohlc: pd.DataFrame, lookback: int = 60, pivot_interval: int = 10, short_pivot_interval: int = 5,
                                    head_ratio_before: float = 0.98, head_ratio_after: float = 0.98,
                                    upper_slmax: float = 1e-4) -> pd.DataFrame:
    """
    Find all the inverse head and shoulders chart patterns

    :params ohlc is the OHLC dataframe
    :type :pd.DataFrame 
    
    :params lookback is the number of periods to use for back candles
    :type :int 
    
    :params pivot_interval is the number of candles to consider when detecting a pivot point
    :type :int 
    
    :params short_pivot_interval is same as pivot_interval but must be less than it. 
    :type :int
    
    :params head_ratio_before is the ratio between the head value and the shoulder value to the left 
    :type :float 
    
    :params head_ratio_after is the ratio between the head value and the shoulder value to the right 
    :type :float 
    
    :params upper_slmax is the upper limit of the neckline slope of the pattern
    :type :float 
    
    :return (pd.DataFrame)
    """
    if short_pivot_interval <= 0 or pivot_interval <= 0:
            raise ValueError("Value cannot be less or equal to 0")  

    if short_pivot_interval >= pivot_interval:
        raise ValueError(f"short_pivot_interval must be less than pivot_interval")
    
    ohlc["ihs_lookback"]   = lookback
    ohlc["chart_type"]     = ""
    ohlc["ihs_idx"]        = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["ihs_point"]      = [np.array([]) for _ in range(len(ohlc)) ]    
    
     # Find the pivot points   
    ohlc = find_all_pivot_points(ohlc, left_count=pivot_interval, right_count=pivot_interval)
    ohlc = find_all_pivot_points(ohlc, left_count=short_pivot_interval, right_count=short_pivot_interval, name_pivot="short_pivot")
       
    for candle_idx in range(lookback, len(ohlc)):
        
        if ohlc.loc[candle_idx, "pivot"] != 1 or ohlc.loc[candle_idx,"short_pivot"] != 1:
            continue
        

        maxim, minim, xxmax, xxmin, maxacount, minacount, maxbcount, minbcount = find_points(ohlc, candle_idx, lookback)
        if minbcount<1 or minacount<1 or maxbcount<1 or maxacount<1:
            continue

        slmax, _, _, _, _ = linregress(xxmax, maxim)
        
        headidx = np.argmin(minim, axis=0)
        
         # If the head index is the last value, then continue
        if len(minim) - 1 == headidx:
            continue       

  
        if minim[headidx-1]-minim[headidx]>0 and (minim[headidx]/minim[headidx-1] < 1 and minim[headidx]/minim[headidx-1] >= head_ratio_before)  and \
            (minim[headidx]/minim[headidx+1] < 1 and minim[headidx]/minim[headidx+1] >= head_ratio_after) and \
            minim[headidx+1]-minim[headidx]> 0 and abs(slmax)<=upper_slmax and \
            xxmax[0]>xxmin[headidx-1] and xxmax[1]<xxmin[headidx+1]: 

                print(f"head_ratio_before: {minim[headidx]/minim[headidx-1]}")
                print(f"head_ratio_after : {minim[headidx]/minim[headidx+1]}")
                ohlc.loc[candle_idx, "chart_type"] = "ihs"
            
                # Get the index and values of the IHS chart pattern
                indexes = [int(xxmin[headidx-1]), int(xxmax[0]), int(xxmin[headidx]), int(xxmax[1]), int(xxmin[headidx+1]) ]
                values  = [minim[headidx-1], maxim[0], minim[headidx], maxim[1], minim[headidx+1]]
            
                # Create a tuple of the index and values and sort them by the index
                list_idx_values       =  [ (i, v) for i, v in zip(indexes, values)]
                 
                
                # Assign the index and values
                ohlc.at[candle_idx, "ihs_idx"]   = [ t[0] for t in list_idx_values]
                ohlc.at[candle_idx, "ihs_point"] = [ t[1] for t in list_idx_values]    
 
            

    return ohlc


