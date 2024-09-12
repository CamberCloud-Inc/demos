import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
import subprocess

def plotslice(i):
    """
    Wrapper for the plot_slice.py script supplied with AthenaK
    """
    basename ='KH.hydro_w'
    suffix = 'bin'

    #n, xmin, xmax, ymin, ymax = get_plot(i,140,35,240,35)
    name = f"bin/{basename}.{i:05}.{suffix}"
    print(f"plotting {name}...")
    imgfile = f"output_images/img{i:05}.png"
    xmin = -1
    xmax = 1
    ymin = -1
    ymax = 1
    
    subprocess.run(["python",
                    "plot_slice.py",
                    name,
                    "dens",
                    imgfile,
                    "-c", "magma",
                    "--vmin", "0.9",
                    "--vmax", "2",
                    "--dpi", "300",
                    "--x1_min", "{:f}".format(xmin),
                    "--x1_max", "{:f}".format(xmax),                
                    "--x2_min", "{:f}".format(ymin),
                    "--x2_max", "{:f}".format(ymax)])

    
def plot_output():
    
    # plot frames
    for i in range(0, 201):
        plotslice(i)
    # create movie
    subprocess.run(["ffmpeg",
                    "-r", "20",
                    "-s", "1920x1080",
                    "-start_number", "0",
                    "-i", "output_images/img%05d.png",
                    "-vframes", "201",
                    "-vcodec", "libx264",
                    "-crf", "25",
                    "-pix_fmt", "yuva420p",
                    "-y",
                    "density.mov"])
        