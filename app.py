import dash
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import holoviews as hv
from holoviews.operation.datashader import datashade
from holoviews.plotting.plotly.dash import to_dash


def prepare_preplot_raster():
    preplot_gdf = gpd.read_file(f"data/preplot.geojson")
    preplot_gdf.X = preplot_gdf.geometry.x
    preplot_gdf.Y = preplot_gdf.geometry.y
    preplot_gdf.drop("geometry", axis=1, inplace=True)
    hv_preplot = hv.Dataset(preplot_gdf)
    points = hv.Points(hv_preplot, ["X", "Y"]).opts(color="green")
    tiles = hv.element.tiles.EsriImagery()
    overlay = tiles * datashade(points)
    overlay.opts(margins=(1, 1, 1, 1))
    return overlay


summary_df = pd.read_pickle(f"data/summary.pkl")
stats_df = pd.read_pickle(f"data/stats.pkl")
stats_df = stats_df.set_index(["Date"]).sort_index(inplace=False)
acq_df = pd.read_pickle(f"data/acq_log.pkl")
acq_df = acq_df.set_index(["Date"]).sort_index(inplace=False)


app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.MATERIA])
server = app.server

preplot_raster_graph = to_dash(app, [prepare_preplot_raster()], responsive=True).graphs
