"""
Date   : 2024-07-08
Author : Zetra Team
Function used to detect Pennant patterns
"""

import numpy as np
import pandas as pd 
import plotly.graph_objects as go

from chart_patterns.chart_patterns.charts_utils import find_points
from chart_patterns.chart_patterns.pivot_points import find_all_pivot_points
from scipy.stats import linregress
from tqdm import tqdm



def find_pennant(ohlc: pd.DataFrame, lookback: int = 20, min_points: int = 3,
                r_max: float = 0.9, r_min: float = 0.9, slope_max: float = -0.0001, slope_min: float = 0.0001, 
                 lower_ratio_slope: float = 0.95, upper_ratio_slope: float = 1,
                 progress: bool = False) -> pd.DataFrame:
    """
    Find the pennant pattern point
    
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
    ohlc["pennant_point"]        = np.nan 
    ohlc["pennant_highs_idx"]    = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["pennant_lows_idx"]     = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["pennant_highs"]        = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["pennant_lows"]         = [np.array([]) for _ in range(len(ohlc)) ]
    ohlc["pennant_slmax"]        = np.nan 
    ohlc["pennant_slmin"]        = np.nan 
    ohlc["pennant_intercmin"]    = np.nan
    ohlc["pennant_intercmax"]    = np.nan
    
    # Find the pivot points
    ohlc = find_all_pivot_points(ohlc, progress=progress)
    

    if not progress:
        candle_iter = range(lookback, len(ohlc))
    else:
        candle_iter = tqdm(range(lookback, len(ohlc)), desc="Finding pennant patterns...")
        
    for candle_idx in candle_iter:
    
        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])

        for i in range(candle_idx-lookback, candle_idx+1):
            if ohlc.loc[i,"pivot"] == 1:
                minim = np.append(minim, ohlc.loc[i, "low"])
                xxmin = np.append(xxmin, i) 
            if ohlc.loc[i,"pivot"] == 2:
                maxim = np.append(maxim, ohlc.loc[i,"high"])
                xxmax = np.append(xxmax, i)

        
        # Check the correct number of pivot points have been found
        if (xxmax.size < min_points and xxmin.size < min_points) or xxmax.size==0 or xxmin.size==0:
            continue

         # Run the regress to get the slope, intercepts and r-squared
        slmin, intercmin, rmin, pmin, semin = linregress(xxmin, minim)
        slmax, intercmax, rmax, pmax, semax = linregress(xxmax, maxim)
        
        
        
        if abs(rmax)>=r_max and abs(rmin)>=r_min and slmin>=slope_min  and slmax<= slope_max  and abs(slmax/slmin) > lower_ratio_slope and abs(slmax/slmin) < upper_ratio_slope:
                ohlc.loc[candle_idx,"chart_type"]          = "pennant"
                ohlc.loc[candle_idx, "pennant_point"]         = candle_idx
                ohlc.at[candle_idx, "pennant_highs"]          = maxim
                ohlc.at[candle_idx, "pennant_lows"]           = minim
                ohlc.at[candle_idx, "pennant_highs_idx"]      = xxmax
                ohlc.at[candle_idx, "pennant_lows_idx"]       = xxmin
                ohlc.loc[candle_idx, "pennant_slmax"]         = slmax
                ohlc.loc[candle_idx, "pennant_slmin"]         = slmin 
                ohlc.loc[candle_idx, "pennant_intercmin"]     = intercmin
                ohlc.loc[candle_idx, "pennant_intercmax"]     = intercmax
                
    return ohlc 