import numpy as np
import obspy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from obspy.geodetics.base import gps2dist_azimuth
from matplotlib.transforms import blended_transform_factory
from matplotlib import cm
plt.style.use(['seaborn-poster'])

def ray_plot(ev_lat=None,ev_lon=None,min_lat=None,max_lat=None,min_lon=None,max_lon=None,inventory=None,streams=None):
    fig = plt.figure()
    # Define the Cartopy Projection
    maxlat = max_lat
    minlat = min_lat
    maxlon = max_lon
    minlon = min_lon
    lat = ev_lat
    lon = ev_lon
    st_event = streams
    inv = inventory
    lat0 = (maxlat + minlat)/2.0
    lon0 = (maxlon + minlon)/2.0
    proj_kwargs={}
    proj_kwargs['central_latitude'] = lat0
    proj_kwargs['central_longitude'] = lon0
    proj_kwargs['standard_parallels'] = [lat0,lat0]
    proj = ccrs.AlbersEqualArea(**proj_kwargs) # cartopy.crs as ccrs
    map_ax = fig.add_axes([0.1,0.1,0.8,0.8],projection=proj)
    x0, y0 = proj.transform_point(lon0, lat0, proj.as_geodetic())
    deg2m_lat = 2 * np.pi * 6371 * 1000 / 360
    deg2m_lon = deg2m_lat * np.cos(lat0 / 180 * np.pi)
    height = (maxlat - minlat) * deg2m_lat
    width = (maxlon - minlon) * deg2m_lon
    map_ax.set_xlim(x0 - width / 2, x0 + width / 2)
    map_ax.set_ylim(y0 - height / 2, y0 + height / 2)

    # Plot the Coastlines
    map_ax.coastlines()

    # Plot the Parallels and Meridians
    map_ax.gridlines()
    st_event.merge()

    # Plot the source with a dot
    map_ax.scatter(lon, lat, marker="o", s=120, zorder=10,
                    color="k", edgecolor="w", transform = proj.as_geodetic())

    # Plot the station with data with a triangle, and the path source-reciever
    for station in inv[0]:
        if len(st_event.select(station=station.code))!=0:
            map_ax.scatter(station.longitude, station.latitude, marker="v", s=120, zorder=10,
                     color="k", edgecolor="w", transform = proj.as_geodetic())
            an_x, an_y = proj.transform_point(station.longitude, station.latitude, proj.as_geodetic())
            map_ax.annotate(str(station.code),(an_x,an_y),textcoords="offset points",xytext=(0,10),ha='center')
            plt.plot([station.longitude, lon], [station.latitude, lat], color='0.8',  transform=ccrs.Geodetic())
            st_len = len(st_event.select(station=station.code))
            st_event.select(station=station.code)[0].stats.distance=gps2dist_azimuth(station.latitude, station.longitude, lat, lon, a=6378137.0, f=0.0033528106647474805)[0]
            if st_len > 1:
                st_event.select(station=station.code)[1].stats.distance=gps2dist_azimuth(station.latitude, station.longitude, lat, lon, a=6378137.0, f=0.0033528106647474805)[0]
            if st_len > 2:
                st_event.select(station=station.code)[2].stats.distance=gps2dist_azimuth(station.latitude, station.longitude, lat, lon, a=6378137.0, f=0.0033528106647474805)[0]

def adj_plot(min_lat=None,max_lat=None,min_lon=None,max_lon=None,inventory=None,streams=None,adj_mat=None):
    fig = plt.figure()
    # Define the Cartopy Projection
    maxlat = max_lat
    minlat = min_lat
    maxlon = max_lon
    minlon = min_lon
    st_event = streams
    inv = inventory
    lat0 = (maxlat + minlat)/2.0
    lon0 = (maxlon + minlon)/2.0
    proj_kwargs={}
    proj_kwargs['central_latitude'] = lat0
    proj_kwargs['central_longitude'] = lon0
    proj_kwargs['standard_parallels'] = [lat0,lat0]
    proj = ccrs.AlbersEqualArea(**proj_kwargs) # cartopy.crs as ccrs
    map_ax = fig.add_axes([0.1,0.1,0.8,0.8],projection=proj)
    x0, y0 = proj.transform_point(lon0, lat0, proj.as_geodetic())
    deg2m_lat = 2 * np.pi * 6371 * 1000 / 360
    deg2m_lon = deg2m_lat * np.cos(lat0 / 180 * np.pi)
    height = (maxlat - minlat) * deg2m_lat
    width = (maxlon - minlon) * deg2m_lon
    map_ax.set_xlim(x0 - width / 2, x0 + width / 2)
    map_ax.set_ylim(y0 - height / 2, y0 + height / 2)

    # Plot the Coastlines
    map_ax.coastlines()

    # Plot the Parallels and Meridians
    map_ax.gridlines()
    st_event.merge()

    # Get Station Lat/Lon and Save it
    sta_cord = list()
    for station in inv[0]:
        if len(st_event.select(station=station.code))!=0:
            sta_cord.append([station.latitude,station.longitude])

    # Plot the station with data with a triangle, and the path
    # source-reciever
    for station in inv[0]:
        if len(st_event.select(station=station.code))!=0:
            map_ax.scatter(station.longitude, station.latitude, marker="v", s=120, zorder=10,
                     color="k", edgecolor="w", transform = proj.as_geodetic())
            an_x, an_y = proj.transform_point(station.longitude, station.latitude, proj.as_geodetic())
            map_ax.annotate(str(station.code),(an_x,an_y),textcoords="offset points",xytext=(0,10),ha='center')

    for i in range(len(sta_cord)):
        # Akin to looping through adj_mat
        for j in range(len(sta_cord)):
            if i == j:
                continue
            else:
                #print(adj_mat[i,j])
                color = cm.hsv(adj_mat[i,j]/1)
                if adj_mat[i,j] > 0:
                    source = sta_cord[j]
                    dest = sta_cord[i]
                    a = plt.arrow(source[1],source[0],dest[1]-source[1],dest[0]-source[0],
                              linewidth=2, head_width=0.1,
                              head_length=0.1, color=color,
                              overhang = -10,
                              transform = ccrs.Geodetic())
                    a.set_closed(False)
    plt.show()
