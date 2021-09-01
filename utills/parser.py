import pandas as pd
import geopandas as gpd

def parse_preplot(filename):
    preplot_df = pd.read_csv(filename, delim_whitespace=True, header=None, names=["X", "Y"])
    preplot_gdf = gpd.GeoDataFrame(preplot_df, geometry=gpd.points_from_xy(preplot_df.X, preplot_df.Y))
    preplot_gdf.crs = "EPSG:32642"
    preplot_gdf = preplot_gdf.to_crs("EPSG:3857")
    preplot_gdf.to_file(f"data/preplot.geojson", driver='GeoJSON')

def parse_summary(filename):
    summary_df = pd.read_csv(filename, delimiter=",", header=None, names=["Параметр", "Значение"])
    summary_df.to_pickle(f"data/summary.pkl")

def parse_aquisition_stats(filename):
    stats_df = pd.read_csv(filename, delim_whitespace=True,
                           header=None, names=["Date", "Planned", "Planned_sum", "Actual", "Actual_sum", "Forecast"])
    stats_df.Date = pd.to_datetime(stats_df.Date)
    stats_df.to_pickle(f"data/stats.pkl")
    
def parse_acquisition_log(filename):
    log_df = pd.read_csv(filename, delimiter=",",
                           header=None, names=["Date", "Time", "FFID", "Line", "Point", "X", "Y"])
    log_df.Date = pd.to_datetime(log_df.Date)
    log_gdf = gpd.GeoDataFrame(
        log_df, geometry=gpd.points_from_xy(log_df.X, log_df.Y))
    log_gdf.crs = "EPSG:32642"
    log_gdf = log_gdf.to_crs("EPSG:3857")
    log_df.X = log_gdf.geometry.x
    log_df.Y = log_gdf.geometry.y
    #log_gdf.to_file(f"data/acquisition_log.geojson")
    log_df.to_pickle(f"data/acq_log.pkl")

if __name__ == "__main__":
    parse_preplot(f"data/preplot.txt")
    parse_summary(f"data/summary.txt")
    parse_aquisition_stats(f"data/stats.txt")
    parse_acquisition_log(f"data/acquisition_log.txt")
