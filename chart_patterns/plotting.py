"""
Date  : 2023-12-25
Author: Zetra Team

For slider: https://community.plotly.com/t/multiple-traces-with-a-single-slider-in-plotly/16356/2
"""

import os
import pandas as pd
import plotly.graph_objects as go
import sys


from chart_patterns.chart_patterns.utils import check_ohlc_names
from plotly.subplots import make_subplots
from tqdm import tqdm
from typing import Dict, List, Union


def set_theme(fig: go.Candlestick, theme: Dict[str,str] = {"bg_color": "black", "up_color":"#3D9970", 
                                                      "down_color": "#FF4136", "legend_font_color": "white", "xaxes_color": "white", "yaxes_color": "white"}) -> go.Candlestick:
    """
    Set the aesthetics of the plot
    
    :params fig is the candlestick object
    :type :go.Candlestick
    
    :params theme is dictionary with the settings 
    :type :Dict[str, str]
    
    :return (go.Candlestick)
    """
    
    fig.update_layout(xaxis_rangeslider_visible=False, plot_bgcolor=theme["bg_color"], paper_bgcolor=theme["bg_color"],
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=False, side="right"), legend_font_color=theme["legend_font_color"],
                    legend=dict(yanchor="bottom", y=0.99, xanchor="left", x=0.01) )

    fig.update_traces(increasing_fillcolor=theme["up_color"], selector=dict(type='candlestick'))
    fig.update_traces(decreasing_fillcolor=theme["down_color"], selector=dict(type='candlestick'))

    fig.update_xaxes(color=theme["xaxes_color"]) 
    fig.update_yaxes(color=theme["yaxes_color"])       
    
    return fig



def _plot_candlestick(ohlc: pd.DataFrame, plot_obs:int = 500, fig =None ) -> go.Candlestick:
    """
    :params ohlc is a dataframe with Open, High, Low, Close 
    :type :pd.DataFrame
    
    :params plot_obs is the total number of observations to plot
    :type :int 
    
    :return (go.Candlestick)       
    """
    
    # Check if OHLC columns are present
    check_ohlc_names(ohlc)
    
    # Has the user run find_all_pivot_points?
    if ohlc.columns.str.contains("pivot_pos").sum() == 0:
        print(f"-> Column `pivot_pos` was not found. Did you run `find_all_pivot_points`?")
        sys.exit() 
        
      
    # Find the number of obs. Only plot 500 observations
    if len(ohlc)  > plot_obs + 1:
        print(f"Note only the {plot_obs} points will be plotted")
        
        ohlc = ohlc.iloc[:plot_obs,]
    
    
    # Plot the candlesticks
    if fig is not None :
        fig.add_trace(go.Candlestick(
                    x     = ohlc.index,
                    open  = ohlc.open,
                    high  = ohlc.high,
                    low   = ohlc.low,
                    close = ohlc.close, name="OHLC"    
            ))
    else:
        fig = go.Figure(data=[go.Candlestick(
                    x     = ohlc.index,
                    open  = ohlc.open,
                    high  = ohlc.high,
                    low   = ohlc.low,
                    close = ohlc.close, name="OHLC"    
            )])
    
    
    return fig 


def _plot_pivot_points(ohlc: pd.DataFrame, fig: go.Candlestick, pivot_name: int = "pivot") -> go.Candlestick:
    """
    Plot the pivot points. It are assumes there is a "pivot" column
    
    :params ohlc is a dataframe with Open, High, Low, Close 
    :type :pd.DataFrame
    
    :params fig is the figure object that has the candlestick
    :type :go.Candlestick
    
    :params pivot_name is the name of the column that has the pivot points. Note the column should have int values
            where `1` is pivot lows and `2` is pivot highs
    :type :str 
    
    
    :return (go.Candlestick)
    """
    try:
        pivot_lows  = ohlc.loc[ohlc[pivot_name] == 1,]
        pivot_highs = ohlc.loc[ohlc[pivot_name] == 2,]
    except Exception as e:
        print(f"No column named `{pivot_name}`. Did you run `find_all_pivot_points`?")
        sys.exit() 
        
    fig.add_scatter(
            x = pivot_lows.index ,
            y = pivot_lows[f"{pivot_name}_pos"],
            mode="markers", marker=dict(size=20, color="red"), name="Pivot Low"
        )   
    
    fig.add_scatter(
            x=pivot_highs.index,
            y=pivot_highs[f"{pivot_name}_pos"] ,
            mode="markers", marker=dict(size=20, color="green"), name="Pivot High"
        )    

    return fig 

def display_pivot_points(ohlc : pd.DataFrame, 
                         theme: Dict[str, str] = {"bg_color": "black", "up_color":"#3D9970", 
                                                      "down_color": "#FF4136", "legend_font_color": "white", "xaxes_color": "white", "yaxes_color": "white"}, 
                         plot_obs:int = 500 ) -> None:
    """
    Display the pivot points and the OHLC data in a graph
    
    :params ohlc is a dataframe with Open, High, Low, Close and the pivot_pos
    :type :pd.DataFrame
    
    :params theme is the set of parameters to set the aesthetics of the graph
    :type :Dict[str, str]
    
    :params plot_obs is the total number of observations to plot
    :type :int 
    
    :return (None)
    """
    
    # Get the Candlestick figure object
    fig = _plot_candlestick(ohlc, plot_obs)
    
    # Add the pivot points 
    fig = _plot_pivot_points(ohlc, fig)    
                
    # Set the theme   
    fig = set_theme(fig, theme)
    
    
    fig.show()
    

def _add_head_shoulder_pattern_plot(row: Union[tuple, pd.DataFrame], fig: go.Candlestick, 
                                    x_val: str = "hs_idx", y_val: str = "hs_point") -> go.Candlestick:
    """
    Add the Head and Shoulders pattern to the given figure object
    
    :params row is either a pandas dataframe or a row that has the flag chart pattern info.
    :type :Union[tuple, pd.DataFrame]
    
    :params fig is the figure object
    :type :go.Candlestick
    
    :return (go.Candlestick)   
    """
    
    if isinstance(row, tuple):
        x_values = row[1][x_val]
        y_values = row[1][y_val]
    else:
        x_values = row[x_val]
        y_values = row[y_val]       
    
    fig.add_scatter(
            x = x_values , y = y_values,
                    mode='lines',
                    name=None, line=dict(color='royalblue', width=4), showlegend=False )   
        
    return fig   

def _add_doubles_pattern_plot(row: Union[tuple, pd.DataFrame], fig: go.Candlestick) -> go.Candlestick:
    """
    Add the the Double chart patterns to the given figure object
    
    :params row is either a pandas dataframe or a row that has the flag chart pattern info.
    :type :Union[tuple, pd.DataFrame]
    
    :params fig is the figure object
    :type :go.Candlestick
    
    :return (go.Candlestick)    
    """
    
    if isinstance(row, tuple):
        double_idx = row[1]["double_idx"]
        double_pts = row[1]["double_point"]
    else:
        double_idx = row["double_idx"]
        double_pts = row["double_point"] 
    
    fig.add_scatter(x = double_idx , y = double_pts,
                    mode='lines',
                    name=None, line=dict(color='royalblue', width=4), showlegend=False )     
            
    return fig 

def _add_triangle_pattern_plot(row: Union[tuple, pd.DataFrame], fig: go.Candlestick) -> go.Candlestick:
    """
    Add the triangle pattern to the figure object 
    
    :params row is either a pandas dataframe or a row that has the flag chart pattern info.
    :type :Union[tuple, pd.DataFrame]
    
    :params fig is the figure object
    :type :go.Candlestick
    
    :return (go.Candlestick)    
    """
    
    if isinstance(row, pd.DataFrame):
        high_idx  = row["triangle_high_idx"]
        low_idx   = row["triangle_low_idx"]
        intercmin = row["triangle_intercmin"]
        intercmax = row["triangle_intercmax"]
        slmax     = row["triangle_slmax"]
        slmin     = row["triangle_slmin"]
        
    else:
        high_idx  = row[1]["triangle_high_idx"].tolist()
        low_idx   = row[1]["triangle_low_idx"].tolist()
        intercmin = row[1]["triangle_intercmin"]
        intercmax = row[1]["triangle_intercmax"]
        slmax     = row[1]["triangle_slmax"]
        slmin     = row[1]["triangle_slmin"]

    fig.add_scatter(x = [int(idx) for idx in high_idx] , y = [int(idx)*slmax + intercmax for idx in high_idx],
                    mode='lines',
                    name=None, line=dict(color='royalblue', width=4), showlegend=False )
    
    fig.add_scatter(x = [int(idx) for idx in low_idx] , y = [int(idx)*slmin + intercmin for idx in low_idx],
                    mode='lines',
                    name=None, line=dict(color='royalblue', width=4), showlegend=False )   
    
    return fig 


def _add_pennant_pattern_plot(row: Union[tuple, pd.DataFrame], fig: go.Candlestick) -> go.Candlestick:
    """
     Add the pennant pattern to the figure object
    
    :params row is either a pandas dataframe or a row that has the pennant chart pattern info.
    :type :Union[tuple, pd.DataFrame]
    
    :params fig is the figure object
    :type :go.Candlestick
    
    :return (go.Candlestick)   
    """
    
    if isinstance(row, pd.DataFrame):
    
        x_low_vals      = row["pennant_lows_idx"].tolist()[0].tolist()
        y_low_vals_arr  = row["pennant_slmin"]*row["pennant_lows_idx"] + row["pennant_intercmin"]
        y_low_vals      = y_low_vals_arr.tolist()[0].tolist()
        
        x_high_vals      = row["pennant_highs_idx"].tolist()[0].tolist()
        y_high_vals_arr  = row["pennant_slmax"]*row["pennant_highs_idx"] + row["pennant_intercmax"]
        y_high_vals      = y_high_vals_arr.tolist()[0].tolist()    
        
    else:
        
        x_low_vals      = row[1]["pennant_lows_idx"]
        y_low_vals_arr  = row[1]["pennant_slmin"]*row[1]["pennant_lows_idx"] + row[1]["pennant_intercmin"]
        y_low_vals      = y_low_vals_arr
        
        x_high_vals      = row[1]["pennant_highs_idx"]
        y_high_vals_arr  = row[1]["pennant_slmax"]*row[1]["pennant_highs_idx"] + row[1]["pennant_intercmax"]
        y_high_vals      = y_high_vals_arr   
        
    fig.add_scatter(x = x_low_vals , y = y_low_vals,
                    mode='lines',
                    name=None, line=dict(color='royalblue', width=4), showlegend=False )
    
    fig.add_scatter(x = x_high_vals , y = y_high_vals,
                    mode='lines',
                    name=None, line=dict(color='royalblue', width=4), showlegend=False)      

    return fig 


def _add_flag_pattern_plot(row: Union[tuple, pd.DataFrame], fig: go.Candlestick) -> go.Candlestick:
    """
    Add the flag pattern to the figure object
    
    :params row is either a pandas dataframe or a row that has the flag chart pattern info.
    :type :Union[tuple, pd.DataFrame]
    
    :params fig is the figure object
    :type :go.Candlestick
    
    :return (go.Candlestick)
    """
    
    if isinstance(row, pd.DataFrame):

        x_low_vals      = row["flag_lows_idx"].tolist()[0].tolist()
        y_low_vals_arr  = row["flag_slmin"]*row["flag_lows_idx"] + row["flag_intercmin"]
        y_low_vals      = y_low_vals_arr.tolist()[0].tolist()
        
        x_high_vals      = row["flag_highs_idx"].tolist()[0].tolist()
        y_high_vals_arr  = row["flag_slmax"]*row["flag_highs_idx"] + row["flag_intercmax"]
        y_high_vals      = y_high_vals_arr.tolist()[0].tolist()    
        
    else:
        
        x_low_vals      = row[1]["flag_lows_idx"]
        y_low_vals_arr  = row[1]["flag_slmin"]*row[1]["flag_lows_idx"] + row[1]["flag_intercmin"]
        y_low_vals      = y_low_vals_arr
        
        x_high_vals      = row[1]["flag_highs_idx"]
        y_high_vals_arr  = row[1]["flag_slmax"]*row[1]["flag_highs_idx"] + row[1]["flag_intercmax"]
        y_high_vals      = y_high_vals_arr   
        
    fig.add_scatter(x = x_low_vals , y = y_low_vals,
                    mode='lines',
                    name=None, line=dict(color='royalblue', width=4), showlegend=False )
    
    fig.add_scatter(x = x_high_vals , y = y_high_vals,
                    mode='lines',
                    name=None, line=dict(color='royalblue', width=4), showlegend=False)      

    return fig 

def save_chart_pattern(fig: go.Candlestick, pattern: str, row: Union[None,tuple]) -> None:
    """
    Save the chart pattern plot
    
    :params fig is the Candlestick object
    :type :go.Candlestick
    
    :params pattern is the name of the chart pattern to save
    :type :str
    
    :params row is the pandas Series that has the index value
    :type :Union[None,tuple]
    
    :return (None)
    """
    
    # Create the images/flag folder if it does not exist
    if not os.path.exists(os.path.join(os.path.realpath(''), "images")):
            os.mkdir(os.path.join(os.path.realpath(''), "images"))
           
    if not  os.path.exists(os.path.join(os.path.realpath(''), "images", pattern)):
         os.mkdir(os.path.join(os.path.realpath(''), "images", pattern))
    
    if row:        
        fig.write_image(os.path.join(os.path.realpath(''), "images", pattern, f"fig{row[0]}.png"))
    else:
        fig.write_image(os.path.join(os.path.realpath(''), "images", pattern, f"fig-{pattern}.png"))
                   
def display_chart_pattern(ohlc: pd.DataFrame, pattern: str = "flag", 
                          save: bool = True, lookback: int = 60, pivot_name: str = "pivot") -> None:
    """
    Display the specified chart pattern. 
    
    :params ohlc is the dataframe that contains the OHLC data and the chart pattern points
    :type :pd.DataFrame
    
    :params pattern is the name of the pattern to plot 
    :type :str 
    
    :params save is whether to save the plot(s) and not display them
    :type :bool
    
    :params lookback is the number of candlesticks to plot
    :type :int
    
    :params pivot_name is the name of the column that has the pivot points. Note the column should have int values
            where `1` is pivot lows and `2` is pivot highs
    :type :str 
    
    
    :return (None)
    """
    
    # Check if the columns have the `pattern` results
    if ohlc.columns.str.lower().str.contains(pattern).sum() == 0:
        print(f"No columns for the pattern `{pattern}`. Did you run the function to get the pattern?")
        sys.exit()
    

    if pattern == "flag":
        pattern_points = ohlc.loc[ohlc["chart_type"]== "flag"]
    elif pattern == "double":
        pattern_points = ohlc.loc[ohlc["chart_type"]== "double"]
    elif pattern == "hs":
        pattern_points = ohlc.loc[ohlc["chart_type"]=="hs"]
    elif pattern == "ihs":
        pattern_points = ohlc.loc[ohlc["chart_type"]=="ihs"]        
    elif pattern == "triangle":
        pattern_points = ohlc.loc[ohlc["chart_type"]=="triangle"]
    elif pattern == "pennant":
        pattern_points = ohlc.loc[ohlc["chart_type"]=="pennant"]
            
    
    if len(pattern_points) == 0: # There is no pattern found
        print(f"There are no `{pattern}` patterns detected.")
    elif len(pattern_points) == 1:
        # Get the Candlestick figure object
        fig = _plot_candlestick(ohlc)
        
        # Add the pivot points 
        fig = _plot_pivot_points(ohlc, fig, pivot_name)    
                    
        # Set the theme   
        fig = set_theme(fig)
            
        if pattern == "flag":
            # Plot the Flag pattern
            fig = _add_flag_pattern_plot(pattern_points, fig)
        elif pattern == "double":
            fig = _add_doubles_pattern_plot(pattern_points, fig)
        elif pattern == "hs":
            fig = _add_head_shoulder_pattern_plot(pattern_points, fig)
        elif pattern == "ihs":
            fig  = _add_head_shoulder_pattern_plot(pattern_points, fig, "ihs_idx", "ihs_point")
        elif pattern == "triangle":
                fig  = _add_triangle_pattern_plot(pattern_points, fig)
        elif pattern == "pennant":
            fig = _add_pennant_pattern_plot(pattern_points, fig)
                
        if save:
            save_chart_pattern(fig, pattern, None)
        else:
            fig.show()
    elif len(pattern_points) > 1:
             
      for row in tqdm(pattern_points.iterrows(), desc=f"Saving the {pattern} charts..."):
            # Get the row index
            pattern_point = row[0]
            
            # Make sure at least 50 candlesticks are available, if possible
            if pattern_point - lookback < 0:
                start  = 0
            else:
                start = pattern_point - lookback
            
            # Get a subset of the ohlc plus chart pattens included
            ohlc_copy = ohlc.loc[start:pattern_point,]
            
            # Add the ohlc data
            fig = _plot_candlestick(ohlc_copy)
                
            # Add the pivot points 
            fig = _plot_pivot_points(ohlc_copy, fig, pivot_name)    
                        
            # Set the theme   
            fig = set_theme(fig)   
            
            if pattern == "flag":    
                # Add the flag pattern 
                fig = _add_flag_pattern_plot(row, fig)
            elif pattern == "double":
                # Add the double pattern         
                fig = _add_doubles_pattern_plot(row, fig)
            elif pattern == "hs":
                fig = _add_head_shoulder_pattern_plot(row, fig)
            elif pattern == "ihs":
                fig  = _add_head_shoulder_pattern_plot(row, fig, "ihs_idx", "ihs_point")
            elif pattern == "triangle":
                fig  = _add_triangle_pattern_plot(row, fig)
            elif pattern == "pennant":
                fig = _add_pennant_pattern_plot(row, fig)
            
            # Save the figures 
            save_chart_pattern(fig, pattern, row)
                
      if save:
        sys.exit()
              
