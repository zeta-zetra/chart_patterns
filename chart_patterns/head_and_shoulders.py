"""
Date   : 2023-01-07
Author : Zetra Team 
Function used to detect the Head and Shoulders pattern
"""

import numpy as np
import pandas as pd 
import plotly.graph_objects as go

from chart_patterns.chart_patterns.charts_utils import find_points
from chart_patterns.chart_patterns.pivot_points import find_all_pivot_points
from scipy.stats import linregress
from tqdm import tqdm
from typing import Tuple



def find_head_and_shoulders(ohlc: pd.DataFrame, lookback: int = 60, pivot_interval: int = 10, short_pivot_interval: int = 5,
                                    head_ratio_before: float = 1.0002, head_ratio_after: float = 1.0002,
                                    upper_slmin: float = 1e-4, progress: bool = False) -> pd.DataFrame:
    """
    Find all head and shoulder chart patterns

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
    
    :params upper_slmin is the upper limit of the neckline slope of the pattern
    :type :float 
    
    :params progress bar to be displayed or not 
    :type :bool
    
    :return (pd.DataFrame)
    """


    if short_pivot_interval <= 0 or pivot_interval <= 0:
        raise ValueError("Value cannot be less or equal to 0")  

    if short_pivot_interval >= pivot_interval:
        raise ValueError(f"short_pivot_interval must be less than pivot_interval")
    
    ohlc.loc[:,"hs_lookback"]   = lookback
    ohlc.loc[:,"chart_type"]    = ""
    ohlc.loc[:,"hs_idx"]        = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc.loc[:,"hs_point"]      = [np.array([]) for _ in range(len(ohlc)) ]    
    
    # Find the pivot points   
    ohlc = find_all_pivot_points(ohlc, left_count=pivot_interval, right_count=pivot_interval)
    ohlc = find_all_pivot_points(ohlc, left_count=short_pivot_interval, right_count=short_pivot_interval, name_pivot="short_pivot")
    
    if not progress:
        candle_iter = range(lookback, len(ohlc))
    else:
        candle_iter = tqdm(range(lookback, len(ohlc)), desc="Finding head and shoulders patterns...")
    
    for candle_idx in candle_iter:

        if ohlc.loc[candle_idx, "pivot"] != 2 or ohlc.loc[candle_idx, "short_pivot"] != 2:
            continue
        
        
        maxim, minim, xxmax, xxmin, maxacount, minacount, maxbcount, minbcount = find_points(ohlc, candle_idx, lookback)
      
        if minbcount<1 or minacount<1 or maxbcount<1 or maxacount<1:
            continue

        slmin, _, _, _, _ = linregress(xxmin, minim)
        headidx = np.argmax(maxim, axis=0)

        # If the head index is the last value, then continue
        if len(maxim) - 1 == headidx:
            continue
        
        
        if maxim[headidx]-maxim[headidx-1] > 0 and maxim[headidx]/maxim[headidx-1] > head_ratio_before and \
           maxim[headidx]-maxim[headidx+1]>0 and maxim[headidx]/maxim[headidx+1] > head_ratio_after and \
           abs(slmin)<=upper_slmin  and xxmin[0]>xxmax[headidx-1] and xxmin[1]<xxmax[headidx+1]: 
                 
                ohlc.loc[candle_idx, "chart_type"] = "hs"
            
                # Get the index and values of the HS chart pattern
                indexes = [int(xxmax[headidx-1]), int(xxmin[0]), int(xxmax[headidx]), int(xxmin[1]), int(xxmax[headidx+1]) ]
                values  = [maxim[headidx-1], minim[0], maxim[headidx], minim[1], maxim[headidx+1]]
            
                # Create a tuple of the index and values and sort them by the index
                list_idx_values       =  [ (i, v) for i, v in zip(indexes, values)]
                 
                
                # Assign the index and values
                ohlc.at[candle_idx, "hs_idx"]   = [ t[0] for t in list_idx_values]
                ohlc.at[candle_idx, "hs_point"] = [ t[1] for t in list_idx_values]    
       

    return ohlc

