"""
Date  : 2023-12-26
Author: Zetra Team
Function used to detect the Flag pattern
"""



import numpy as np
import pandas as pd 
import plotly.graph_objects as go


from chart_patterns.chart_patterns.pivot_points import find_all_pivot_points
from scipy.stats import linregress
from tqdm import tqdm

def find_flag_pattern(ohlc: pd.DataFrame, lookback: int = 25, min_points: int = 3,
                      r_max: float = 0.9, r_min: float = 0.9, slope_max: float = 0, slope_min: float = 0, 
                      lower_ratio_slope: float = 0.9, upper_ratio_slope: float = 1.05,
                      progress: bool = False) -> pd.DataFrame:
    """
    Find the flag pattern 
    
    :params ohlc is the OHLC dataframe
    :type :pd.DataFrame 
    
    :params lookback is the number of periods to use for back candles
    :type :int 
    
    :params min_points is the minimum of pivot points to use to detect a flag pattern
    :type :int
    
    :params r_max is the R-sqaured fit for the high pivot points
    :type :float
    
    :params r_min is the R-sqaured fit for the low pivot points
    :type :float    
    
    :params slope_max is the slope for the high pivot points
    :type :float    
    
    :params slope_min is the slope for the low pivot points
    :type :float    
    
    :params lower_ratio_slope is the lower limit for the ratio of the slope min to slope max
    :type :float    
    
    :params upper_ratio_slope is the upper limit for the ratio of the slope min to slope max
    :type :float   
    
    :params progress bar to be displayed or not 
    :type :bool
    
    :return (pd.DataFrame)
    """
    ohlc["chart_type"]        = ""
    ohlc["flag_point"]        = np.nan 
    ohlc["flag_highs_idx"]    = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["flag_lows_idx"]     = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["flag_highs"]        = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["flag_lows"]         = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["flag_slmax"]        = np.nan 
    ohlc["flag_slmin"]        = np.nan 
    ohlc["flag_intercmin"]    = np.nan
    ohlc["flag_intercmax"]    = np.nan
    
    # Find the pivot points
    ohlc = find_all_pivot_points(ohlc)
    
    
    if not progress:
        candle_iter = range(lookback, len(ohlc))
    else:
        candle_iter = tqdm(range(lookback, len(ohlc)), desc="Finding flag patterns...")
    
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

        
        # Check if the correct number of pivot points have been found
        if (xxmax.size < min_points and xxmin.size < min_points) or xxmax.size==0 or xxmin.size==0:
            continue
        
        # Check the order condition of the pivot points is met
        if (np.any(np.diff(minim) < 0)) or (np.any(np.diff(maxim) < 0)):
               continue
            
        # Run the regress to get the slope, intercepts and r-squared   
        slmin, intercmin, rmin, _, _ = linregress(xxmin, minim)
        slmax, intercmax, rmax, _, _ = linregress(xxmax, maxim)
  
        # Check if the lines are parallel 
        if abs(rmax)>=r_max and abs(rmin)>=r_min and (slmin > slope_min and slmax > slope_max ) or (slmin < slope_min and slmax < slope_max):
                        if (slmin/slmax > lower_ratio_slope and slmin/slmax < upper_ratio_slope):
                            ohlc.loc[candle_idx,"chart_type"]                         = "flag"
                            ohlc.loc[candle_idx, "flag_point"]         = candle_idx
                            ohlc.at[candle_idx, "flag_highs"]          = maxim
                            ohlc.at[candle_idx, "flag_lows"]           = minim
                            ohlc.at[candle_idx, "flag_highs_idx"]      = xxmax
                            ohlc.at[candle_idx, "flag_lows_idx"]       = xxmin
                            ohlc.loc[candle_idx, "flag_slmax"]         = slmax
                            ohlc.loc[candle_idx, "flag_slmin"]         = slmin 
                            ohlc.loc[candle_idx, "flag_intercmin"]     = intercmin
                            ohlc.loc[candle_idx, "flag_intercmax"]     = intercmax
                                    
                            
    return ohlc 

