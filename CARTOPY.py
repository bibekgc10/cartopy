import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

from shapely.geometry import Point
from scipy.spatial import cKDTree
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path


# FOR GEOGRAPHICAL MAP OF FLORDA
# # ----------------------------------
# # 1. Set the output folder
# # ----------------------------------
# output_folder = Path(
#     "D:/Python/datas and research/FLORIDA/RESEARCH FIGURE/FLORIDASPATIAL CARTOPY PLOT")
# output_folder.mkdir(parents=True, exist_ok=True)

# # ----------------------------------
# # 2. Create the map
# # ----------------------------------
# fig = plt.figure(figsize=(9, 10))

# ax = plt.axes(
#     projection=ccrs.PlateCarree()
# )

# # Geographic extent of Florida
# ax.set_extent(
#     [-88.0, -79.5, 24.0, 31.2],
#     crs=ccrs.PlateCarree()
# )

# # ----------------------------------
# # 3. Add map features
# # ----------------------------------
# ax.add_feature(
#     cfeature.LAND,
#     facecolor="white"
# )

# ax.add_feature(
#     cfeature.OCEAN,
#     facecolor="aliceblue"
# )

# # Florida coastline
# ax.add_feature(
#     cfeature.COASTLINE.with_scale("10m"),
#     edgecolor="black",
#     linewidth=0.9
# )

# # Florida state boundary and neighboring states
# ax.add_feature(
#     cfeature.STATES.with_scale("10m"),
#     edgecolor="black",
#     linewidth=0.8,
#     facecolor="none"
# )

# # ----------------------------------
# # 4. Add latitude and longitude
# # ----------------------------------
# gridlines = ax.gridlines(
#     crs=ccrs.PlateCarree(),
#     draw_labels=True,
#     linewidth=0.5,
#     color="gray",
#     alpha=0.6,
#     linestyle="--"
# )

# gridlines.top_labels = False
# gridlines.right_labels = False
# gridlines.xlabel_style = {"size": 9}
# gridlines.ylabel_style = {"size": 9}

# # ----------------------------------
# # 5. Add title
# # ----------------------------------
# ax.set_title(
#     "Geographic Boundary of Florida, USA",
#     fontsize=14,
#     pad=15
# )

# # ----------------------------------
# # 6. Save the map
# # ----------------------------------
# plt.tight_layout()

# output_file = output_folder / "florida_boundary.png"

# plt.savefig(
#     output_file,
#     dpi=300,
#     bbox_inches="tight",
#     facecolor="white"
# )

# print(f"Map saved successfully at: {output_file.resolve()}")

# plt.show()









# TO PLOT THE DATA ON TOP OF THE MAP



# ==========================================
# 1. FILE PATHS
# ==========================================

# csv_path = r"D:/Python/datas and research/FLORIDA/combined data updated/updated combined data/clean_weather_data_updated Worksheet_revised.csv"

# output_folder = Path("D:/Python/datas and research/FLORIDA/RESEARCH FIGURE/FLORIDASPATIAL CARTOPY PLOT")
# output_folder.mkdir(parents=True, exist_ok=True)

# # ==========================================
# # 2. READ CSV FILE
# # ==========================================

# df = pd.read_csv(csv_path)

# # Required columns
# required_columns = [
#     "LATITUDE",
#     "LONGITUDE",
#     "Station ID",
#     "Station Name",
#     "Rainfall Amount (in)"
# ]

# # Check whether required columns exist
# missing_columns = [
#     col for col in required_columns
#     if col not in df.columns
# ]

# if missing_columns:
#     raise ValueError(
#         f"Missing columns in CSV: {missing_columns}\n"
#         f"Available columns: {df.columns.tolist()}"
#     )

# # Convert coordinate and rainfall columns to numeric
# for col in ["LATITUDE", "LONGITUDE", "Rainfall Amount (in)"]:
#     df[col] = pd.to_numeric(df[col], errors="coerce")

# # Keep rows with valid coordinates and rainfall
# plot_df = df.dropna(
#     subset=[
#         "LATITUDE",
#         "LONGITUDE",
#         "Rainfall Amount (in)"
#     ]
# ).copy()

# # Keep coordinates within the displayed map area
# plot_df = plot_df[
#     plot_df["LONGITUDE"].between(-88.0, -79.5)
#     & plot_df["LATITUDE"].between(24.0, 31.2)
# ]

# if plot_df.empty:
#     raise ValueError(
#         "No rows with valid coordinates and rainfall "
#         "were found within the map extent."
#     )

# # ==========================================
# # 3. CREATE FLORIDA MAP
# # ==========================================

# fig = plt.figure(figsize=(10, 11))

# ax = plt.axes(
#     projection=ccrs.PlateCarree()
# )

# ax.set_extent(
#     [-88.0, -79.5, 24.0, 31.2],
#     crs=ccrs.PlateCarree()
# )

# # Geographic background
# ax.add_feature(
#     cfeature.LAND,
#     facecolor="white"
# )

# ax.add_feature(
#     cfeature.OCEAN,
#     facecolor="aliceblue"
# )

# ax.add_feature(
#     cfeature.COASTLINE.with_scale("10m"),
#     edgecolor="black",
#     linewidth=0.8
# )

# ax.add_feature(
#     cfeature.STATES.with_scale("10m"),
#     edgecolor="black",
#     linewidth=0.8,
#     facecolor="none"
# )

# # ==========================================
# # 4. PLOT RAINFALL STATIONS
# # ==========================================

# points = ax.scatter(
#     plot_df["LONGITUDE"],
#     plot_df["LATITUDE"],
#     c=plot_df["Rainfall Amount (in)"],
#     cmap="Blues",
#     s=65,
#     edgecolors="black",
#     linewidths=0.5,
#     transform=ccrs.PlateCarree(),
#     zorder=5
# )

# # ==========================================
# # 5. LABEL STATIONS
# # ==========================================

# for _, row in plot_df.drop_duplicates(
#     subset=["Station ID"]
# ).iterrows():

#     ax.annotate(
#         str(row["Station Name"]),
#         xy=(row["LONGITUDE"], row["LATITUDE"]),
#         xytext=(4, 4),
#         textcoords="offset points",
#         fontsize=7,
#         transform=ccrs.PlateCarree(),
#         zorder=6
#     )

# # ==========================================
# # 6. ADD COLOR BAR
# # ==========================================

# cbar = plt.colorbar(
#     points,
#     ax=ax,
#     orientation="vertical",
#     shrink=0.70,
#     pad=0.04
# )

# cbar.set_label(
#     "Rainfall Amount (inches)",
#     fontsize=11
# )

# # ==========================================
# # 7. GRIDLINES AND TITLE
# # ==========================================

# gl = ax.gridlines(
#     crs=ccrs.PlateCarree(),
#     draw_labels=True,
#     linewidth=0.5,
#     color="gray",
#     alpha=0.6,
#     linestyle="--"
# )

# gl.top_labels = False
# gl.right_labels = False

# ax.set_title(
#     "Spatial Distribution of Rainfall Stations in Florida",
#     fontsize=13,
#     pad=15
# )

# # ==========================================
# # 8. SAVE MAP
# # ==========================================

# plt.tight_layout()

# output_file = output_folder / "florida_rainfall_stations.png"

# plt.savefig(
#     output_file,
#     dpi=300,
#     bbox_inches="tight",
#     facecolor="white"
# )

# print("Map saved successfully:")
# print(output_file.resolve())
# print("Number of plotted records:", len(plot_df))
# print(
#     "Number of unique stations:",
#     plot_df["Station ID"].nunique()
# )

# plt.show()






# RAINFALL STATION MA ,MATRAI COLOR PLOT BHAKO CODE

# # 1. File paths
# csv_path = r"D:/Python/datas and research/FLORIDA/combined data updated/updated combined data/clean_weather_data_updated Worksheet_revised.csv"
# out = Path("D:/Python/datas and research/FLORIDA/RESEARCH FIGURE/FLORIDASPATIAL CARTOPY PLOT")
# out.mkdir(parents=True, exist_ok=True)

# # 2. Read CSV and prepare dates
# df = pd.read_csv(csv_path)
# df["Date"] = pd.to_datetime(df["Date"])
# df["Year"] = df["Date"].dt.year

# df["Rainfall Amount (in)"] = pd.to_numeric(
#     df["Rainfall Amount (in)"]
# )

# # 3. Convert 15-minute rainfall into annual station totals
# annual = (
#     df[df["Year"].between(2005, 2020)]
#     .groupby(["Year", "Station ID"], as_index=False)
#     .agg({
#         "Station Name": "first",
#         "LATITUDE": "first",
#         "LONGITUDE": "first",
#         "Rainfall Amount (in)": "sum"
#     })
# )

# annual.to_csv(out / "annual_rainfall_totals.csv", index=False)

# # 4. Create Florida map
# fig = plt.figure(figsize=(9, 10))
# ax = plt.axes(projection=ccrs.PlateCarree())

# ax.set_extent([-88, -79.5, 24, 31.2], crs=ccrs.PlateCarree())
# ax.add_feature(cfeature.LAND, facecolor="white")
# ax.add_feature(cfeature.OCEAN, facecolor="lightcyan")
# ax.add_feature(cfeature.COASTLINE.with_scale("10m"), linewidth=0.8)
# ax.add_feature(cfeature.STATES.with_scale("10m"), linewidth=0.7)

# ax.gridlines(draw_labels=True, linestyle="--", alpha=0.4)

# # Fixed color scale for fair comparison between years
# vmin = annual["Rainfall Amount (in)"].min()
# vmax = annual["Rainfall Amount (in)"].max()

# if vmin == vmax:
#     vmax = vmin + 1

# # 5. Plot and animate
# years = list(range(2005, 2021))
# stations = annual.drop_duplicates("Station ID").set_index("Station ID")

# rainfall = annual.pivot(
#     index="Station ID",
#     columns="Year",
#     values="Rainfall Amount (in)"
# ).reindex(index=stations.index, columns=years)

# points = ax.scatter(
#     stations["LONGITUDE"], stations["LATITUDE"],
#     c=rainfall[2005], cmap="turbo",
#     vmin=vmin, vmax=vmax, s=75,
#     edgecolors="black", linewidths=0.4,
#     transform=ccrs.PlateCarree()
# )

# cbar = plt.colorbar(points, ax=ax, shrink=0.75, pad=0.04)
# cbar.set_label("Annual Rainfall (inches)")

# title = ax.set_title("Annual Rainfall in Florida — 2005")

# def update(i):
#     points.set_array(rainfall[years[i]].to_numpy(dtype=float))
#     title.set_text(f"Annual Rainfall in Florida — {years[i]}")
#     return points, title

# ani = FuncAnimation(
#     fig, update, frames=len(years),
#     interval=800, repeat=True, blit=False
# )

# # 6. Save animated GIF
# ani.save(
#     str(out / "Florida_Annual_Rainfall_2005_2020.gif"),
#     writer=PillowWriter(fps=1.25),
#     dpi=120
# )

# plt.close(fig)

# print("Animation saved:", (out / "Florida_Annual_Rainfall_2005_2020.gif").resolve())
# print("Annual totals saved:", (out / "annual_rainfall_totals.csv").resolve())














# 1. File paths
csv_path = r"D:/Python/datas and research/FLORIDA/combined data updated/updated combined data/clean_weather_data_updated Worksheet_revised.csv"
out = Path("D:/Python/datas and research/FLORIDA/RESEARCH FIGURE/FLORIDASPATIAL CARTOPY PLOT")
out.mkdir(parents=True, exist_ok=True)

# 2. Aggregate 15-minute rainfall into annual totals
df = pd.read_csv(csv_path)
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Rainfall Amount (in)"] = pd.to_numeric(
    df["Rainfall Amount (in)"]
)

df = df[df["Year"].between(2005, 2020)]

annual = (
    df.groupby(["Year", "Station ID"], as_index=False)
    .agg({
        "Station Name": "first",
        "LATITUDE": "first",
        "LONGITUDE": "first",
        "Rainfall Amount (in)": "sum"
    })
)

annual.to_csv(out / "annual_rainfall_totals.csv", index=False)

# 3. Obtain Florida's geographic boundary
shp = shpreader.natural_earth(
    resolution="10m",
    category="cultural",
    name="admin_1_states_provinces"
)

florida = None

for record in shpreader.Reader(shp).records():
    attrs = record.attributes
    if (attrs.get("name") == "Florida"
            and "United States" in str(attrs.get("admin", ""))):
        florida = record.geometry
        break

if florida is None:
    raise ValueError("Florida boundary could not be found.")

# 4. Create a grid covering Florida
lon = np.linspace(-88.0, -79.5, 250)
lat = np.linspace(24.0, 31.2, 250)
lon_grid, lat_grid = np.meshgrid(lon, lat)

grid_points = np.column_stack([
    lon_grid.ravel(), lat_grid.ravel()
])

# Mask grid cells outside Florida
inside = np.array([
    florida.covers(Point(x, y))
    for x, y in grid_points
])

# 5. Prepare the map
fig = plt.figure(figsize=(9, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.set_extent([-88, -79.5, 24, 31.2],
              crs=ccrs.PlateCarree())

ax.add_feature(cfeature.OCEAN, facecolor="white")
ax.add_feature(cfeature.LAND, facecolor="whitesmoke")
ax.add_feature(cfeature.COASTLINE.with_scale("10m"), linewidth=0.7)
ax.add_feature(cfeature.STATES.with_scale("10m"), linewidth=0.7)

# Fixed color scale across all years
vmin = annual["Rainfall Amount (in)"].min()
vmax = annual["Rainfall Amount (in)"].max()

if vmin == vmax:
    vmax = vmin + 1

# 6. IDW interpolation for each year
def interpolate_year(year):
    data = annual[annual["Year"] == year].dropna(
        subset=["LATITUDE", "LONGITUDE", "Rainfall Amount (in)"]
    )

    xy = data[["LONGITUDE", "LATITUDE"]].to_numpy()
    values = data["Rainfall Amount (in)"].to_numpy()

    if len(values) == 0:
        return np.full(lon_grid.shape, np.nan)

    # Find up to 8 nearest stations for each grid cell
    tree = cKDTree(xy)
    k = min(8, len(values))
    distances, indices = tree.query(grid_points, k=k)

    if k == 1:
        distances = distances[:, None]
        indices = indices[:, None]

    # IDW: closer stations receive greater weight
    distances = np.maximum(distances, 1e-10)
    weights = 1 / distances**2

    estimates = (
        np.sum(weights * values[indices], axis=1)
        / np.sum(weights, axis=1)
    )

    # Use the exact station value at a station location
    exact = distances[:, 0] < 1e-9
    estimates[exact] = values[indices[exact, 0]]

    estimates[~inside] = np.nan

    return estimates.reshape(lon_grid.shape)

# 7. Draw the first year's rainfall surface
years = list(range(2005, 2021))
first_grid = interpolate_year(years[0])

mesh = ax.pcolormesh(
    lon_grid, lat_grid, first_grid,
    cmap="turbo", vmin=vmin, vmax=vmax,
    shading="auto",
    transform=ccrs.PlateCarree(),
    zorder=2
)

# Outline Florida over the rainfall surface
ax.add_geometries(
    [florida],
    crs=ccrs.PlateCarree(),
    facecolor="none",
    edgecolor="black",
    linewidth=1.1,
    zorder=4
)

cbar = plt.colorbar(mesh, ax=ax, shrink=0.75, pad=0.04)
cbar.set_label("Annual Rainfall (inches)")

title = ax.set_title(
    f"Interpolated Annual Rainfall in Florida — {years[0]}"
)

# 8. Animate 2005–2020
def update(i):
    year = years[i]
    grid = interpolate_year(year)
    mesh.set_array(np.ma.masked_invalid(grid).ravel())
    title.set_text(f"Interpolated Annual Rainfall in Florida — {year}")
    return mesh, title

ani = FuncAnimation(
    fig, update, frames=len(years),
    interval=800, repeat=True, blit=False
)

ani.save(
    str(out / "Florida_Full_Area_Rainfall_2005_2020.gif"),
    writer=PillowWriter(fps=1.25),
    dpi=120
)

plt.close(fig)

print("Animation saved:", (out / "Florida_Full_Area_Rainfall_2005_2020.gif").resolve())
