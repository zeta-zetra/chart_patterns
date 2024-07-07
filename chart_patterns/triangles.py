"""
Date   : 2024-01-13
Author : Zetra Team
Detect Triangle Patterns - Ascending, Descending and Symmetrical 
"""

import numpy as np
import pandas as pd 
import plotly.graph_objects as go


from chart_patterns.chart_patterns.pivot_points import find_all_pivot_points
from scipy.stats import linregress
from tqdm import tqdm

def find_triangle_pattern(ohlc: pd.DataFrame, lookback: int = 25, min_points: int = 3, rlimit: int = 0.9, 
                          slmax_limit: float = 0.00001, slmin_limit: float = 0.00001,
                          triangle_type: str = "ascending", progress: bool = False ) -> pd.DataFrame:
    """
    Find the specified triangle pattern 
    
    :params ohlc is the OHLC dataframe 
    :type :pd.DataFrame
    
    :params lookback is the number of periods to use for back candles
    :type :int 

    :params min_points is the minimum of pivot points to use to detect a flag pattern
    :type :int
    
    :params rlimit is the R-squared fit lower limit for the pivot points
    :type :float
    
    :params slmax_limit is the limit for the slope of the pivot highs
    :type :float
    
    :params slmin_limit is the limit for the slope of the pivot lows
    :type :float
    
    :params triangle_type is the type of triangle pattern to detect. Options - ["ascending", "descending", "symmetrical"]
    :type :str 
    
    :params progress bar to be displayed or not
    :type :bool
    
    :return (pd.DataFrame)
    """
    
    
    ohlc["chart_type"]            = ""
    ohlc["triangle_type"]         = ""
    ohlc["triangle_slmax"]        = np.nan
    ohlc["triangle_slmin"]        = np.nan
    ohlc["triangle_intercmin"]    = np.nan
    ohlc["triangle_intercmax"]    = np.nan
    ohlc["triangle_high_idx"]     = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["triangle_low_idx"]      = [np.array([]) for _ in range(len(ohlc)) ]
    
    
    # Find the pivot points
    ohlc = find_all_pivot_points(ohlc)   
    
    if not progress:
        candle_iter = range(lookback, len(ohlc))
    else:
        candle_iter = tqdm(range(lookback, len(ohlc)), desc="Finding triangle patterns")
    
    for candle_idx in candle_iter:
        
        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])

        for i in range(candle_idx - lookback, candle_idx+1):
            if ohlc.loc[i,"pivot"] == 1:
                minim = np.append(minim, ohlc.loc[i, "low"])
                xxmin = np.append(xxmin, i) 
            if ohlc.loc[i,"pivot"] == 2:
                maxim = np.append(maxim, ohlc.loc[i,"high"])
                xxmax = np.append(xxmax, i)

       
        if (xxmax.size < min_points and xxmin.size < min_points) or xxmax.size==0 or xxmin.size==0:
               continue

        slmin, intercmin, rmin, _, _ = linregress(xxmin, minim)
        slmax, intercmax, rmax, _, _ = linregress(xxmax, maxim)

        if triangle_type == "symmetrical":
            if abs(rmax)>=rlimit and abs(rmin)>=rlimit and slmin>=slmin_limit and slmax<=-1*slmax_limit:
                    ohlc.loc[candle_idx, "chart_type"]            = "triangle"
                    ohlc.loc[candle_idx, "triangle_type"]         = "symmetrical"
                    ohlc.loc[candle_idx, "triangle_slmax"]        = slmax
                    ohlc.loc[candle_idx, "triangle_slmin"]        = slmin
                    ohlc.loc[candle_idx, "triangle_intercmin"]    = intercmin
                    ohlc.loc[candle_idx, "triangle_intercmax"]    = intercmax
                    ohlc.at[candle_idx,  "triangle_high_idx"]     = xxmax
                    ohlc.at[candle_idx,  "triangle_low_idx"]      = xxmin
                    ohlc.loc[candle_idx, "triangle_point"]        = candle_idx
                    

        elif triangle_type == "ascending":
            if abs(rmax)>=rlimit and abs(rmin)>=rlimit and slmin>=slmin_limit and (slmax>=-1*slmax_limit and slmax <= slmax_limit):
                    ohlc.loc[candle_idx, "chart_type"]            = "triangle"
                    ohlc.loc[candle_idx, "triangle_type"]         = "ascending"
                    ohlc.loc[candle_idx, "triangle_slmax"]        = slmax
                    ohlc.loc[candle_idx, "triangle_slmin"]        = slmin
                    ohlc.loc[candle_idx, "triangle_intercmin"]    = intercmin
                    ohlc.loc[candle_idx, "triangle_intercmax"]    = intercmax
                    ohlc.at[candle_idx,  "triangle_high_idx"]     = xxmax
                    ohlc.at[candle_idx,  "triangle_low_idx"]      = xxmin
                    ohlc.loc[candle_idx, "triangle_point"]        = candle_idx
                    
    
        elif triangle_type == "descending":
            if abs(rmax)>=rlimit and abs(rmin)>=rlimit and slmax<=-1*slmax_limit and (slmin>=-1*slmin_limit and slmin <= slmin_limit):
                    ohlc.loc[candle_idx, "chart_type"]            = "triangle"
                    ohlc.loc[candle_idx, "triangle_type"]         = "descending"
                    ohlc.loc[candle_idx, "triangle_slmax"]        = slmax
                    ohlc.loc[candle_idx, "triangle_slmin"]        = slmin
                    ohlc.loc[candle_idx, "triangle_intercmin"]    = intercmin
                    ohlc.loc[candle_idx, "triangle_intercmax"]    = intercmax
                    ohlc.at[candle_idx,  "triangle_high_idx"]     = xxmax
                    ohlc.at[candle_idx,  "triangle_low_idx"]      = xxmin
                    ohlc.loc[candle_idx, "triangle_point"]        = candle_idx   
                    print(f"Found pattern at index: {candle_idx}")
    return ohlc


