import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.gridspec as gridspec
import subprocess
from matplotlib import rc
from matplotlib.colors import LinearSegmentedColormap as LSC
from matplotlib.cm import register_cmap
from athena_read import vtk,athdf

def modulo_cmap(cmap, name=None):
    colors = np.roll(cmap(np.arange(cmap.N)), cmap.N // 2, axis=0)
    if name is None:
        name = map.name + "_mod"
    return LSC.from_list(name, colors, cmap.N)

def plotframe(ax, i, par):
    ax.clear()
    basename ='Blast.out2'
    suffix = 'athdf'
    name = f"run{par}/{basename}.{i:05}.{suffix}"
    #print(f"plotting {name}...")
    
    #reading the data dumps
    data  = athdf(name,quantities=['rho'])
    x = data['x1v']
    y = data['x2v']

    iz = len(data['x3v'])//2
    vals = data['rho'][iz,:,:]

    x_grid, y_grid = np.meshgrid(x, y)
    im = ax.pcolormesh(x_grid, y_grid, vals, cmap='sn_iceFire',norm=colors.LogNorm(vmin=1.0e-2, vmax=4.)) 
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    ax.set_aspect("equal")
    ax.text(0.75, 0.9, par, transform=ax.transAxes, size=10, weight='bold')
    #return im
    #ax.set_xlabel(r"$x$")
    #ax.set_ylabel(r"$y$")

    #plt.savefig(f"output_images/img{i:05}.png")
    
def plot_output(params, key):
    init_plot()
    #Plotting
    fig = plt.figure(figsize=(4, 6))
    fig.subplots_adjust(wspace=0, hspace=0)
    spec = gridspec.GridSpec(ncols=2,nrows=2)
    for i in range(0, 101):
        print(f"plotting frame {i}/100")

        for j, par in enumerate(params[key]):
            ax = fig.add_subplot(spec[j // 2, j % 2])
            plotframe(ax, i, par)
        plt.savefig(f"output_images/img{i:05}.png")
        fig.clf()
            
    subprocess.run(["ffmpeg",
                      "-r", "20",
                      "-s", "1920x1080",
                      "-start_number", "0",
                      "-i", "output_images/img%05d.png",
                      "-vframes", "101",
                      "-vcodec", "libx264",
                      "-crf", "25",
                      "-pix_fmt", "yuva420p",
                      "-y",
                      "density.mov"])
    
    
    
def init_plot():
    rc('text', usetex=False)
    rc('font', family='serif', size=15)

    # Load pretty color table
    # erdc_iceFire colormap from Paraview
    _colors = [[0.000000, 0.000000, 0.000006],
               [0.000000, 0.120401, 0.302675],
               [0.000000, 0.216583, 0.524574],
               [0.055247, 0.345025, 0.659500],
               [0.128047, 0.492588, 0.720288],
               [0.188955, 0.641309, 0.792092],
               [0.327673, 0.784935, 0.873434],
               [0.608240, 0.892164, 0.935547],
               [0.881371, 0.912178, 0.818099],
               [0.951407, 0.835621, 0.449279],
               [0.904481, 0.690489, 0.000000],
               [0.854070, 0.510864, 0.000000],
               [0.777093, 0.330180, 0.000882],
               [0.672862, 0.139087, 0.002694],
               [0.508815, 0.000000, 0.000000],
               [0.299417, 0.000366, 0.000548],
               [0.015752, 0.003320, 0.000000]]

    erdc_iceFire = LSC.from_list("erdc_iceFire", _colors, 256)
    erdc_iceFire_rev = LSC.from_list("erdc_iceFire_rev", _colors[::-1], 256)

    # my (msbc) modification to the colormap
    _my_c = _colors[:]
    _my_c[8] = [1, 1, 1]

    msbc_iceFire = LSC.from_list("msbc_iceFire", _my_c[::-1], 256)
    msbc_iceFire_rev = LSC.from_list("msbc_iceFire_rev", _my_c, 256)
    sn_iceFire = modulo_cmap(msbc_iceFire, "sn_iceFire")
    sn_iceFire_rev = modulo_cmap(msbc_iceFire_rev, "sn_iceFire_rev")

    for i in [sn_iceFire]:
        try:
            register_cmap(cmap=i)
        except:
            pass
