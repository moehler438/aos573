import numpy as np
import matplotlib.pyplot as plt
import metpy
from datetime import datetime
from siphon.simplewebservice.wyoming import WyomingUpperAir
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, SkewT

def test_my_skew_t(date, station):

    # Read in data
    ds = WyomingUpperAir.request_data(date, station)

    # Add units to variable
    pressure = ds.pressure.values*units.hPa
    height = ds.height.values*units.meter
    temperature = ds.temperature.values*units.degC
    dewpoint = ds.dewpoint.values*units.degC
    direction = ds.direction.values*units.deg
    speed = ds.speed.values*units.knots
    u_wind = ds.u_wind.values*units.knots
    v_wind = ds.v_wind.values*units.knots
    elevation = ds.elevation.values*units.meters
    pw = ds.pw.values*units.millimeter

    # Calculate lifting condensation level (LCL)
    lcl_pressure, lcl_temperature = metpy.calc.lcl(pressure[0], temperature[0], dewpoint[0])

    # Calculate parcel profile and convert to degrees C
    parcel = metpy.calc.parcel_profile(pressure, temperature[0], dewpoint[0]).to('degC')

    # Find u and v components of wind
    u, v = metpy.calc.wind_components(speed, direction)

    # Create figure
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig, rotation=45)

    # Plot temperature and dewpoint
    skew.plot(pressure, temperature, 'r') 
    skew.plot(pressure, dewpoint, 'g') 

    # Plot wind barbs
    skew.plot_barbs(pressure, u, v)

    # Set axis limits and labels
    skew.ax.set_ylim(1000, 100)
    skew.ax.set_xlim(-40, 60)
    skew.ax.set_xlabel(f'Temperature ({temperature.units:~P})')
    skew.ax.set_ylabel(f'Pressure ({pressure.units:~P})')

    # Plot lcl
    skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

    # Plot parcel profile
    skew.plot(pressure, parcel, 'k', linewidth=2)

    # Shade areas of CAPE and CIN
    skew.shade_cin(pressure, temperature, parcel, dewpoint)
    skew.shade_cape(pressure, temperature, parcel)

    # Add the relevant special lines
    skew.plot_dry_adiabats()
    skew.plot_moist_adiabats()
    skew.plot_mixing_lines()

    # Add plot titles
    plt.title(station, loc='left')
    plt.title(date, loc='right')
    
    return fig