========
Cookbook
========

Download the spectral library to a good location on your disk.


Create a local working directory for the star you wish to process.

Copy `config.yaml` to this directory and modify the settings as you wish. It is generally a good idea to keep the HDF5 paths set to this local directory.

From within this local directory, we will want to create the grid.

    # Downsample the grid
    grid.py create

    # Plot all of the spectra in the hdf5 grid into the plotdir
    grid.py plot


Here we should also have some routines to plot the various spectra within the grid to make sure everything looks as we want.

Then, we will want to make the PCA grid, and do many other things regarding optimization and final plotting. These are all done through the `pca.py` script.

    # create the grid using settings in config.yaml
    pca.py --create

    # Plot all of the eigenspectra and the histogram of weights
    pca.py --plot=eigenspectra

    # reconstruct the grid at the synthetic grid points, plotting the difference
    pca.py --plot=reconstruct

    # Specify and examine priors stored in config.yaml
    pca.py --plot=priors

    # Optimize the emulator using fmin
    pca.py --optimize=fmin

    # Optimize the emulator starting from previous parameter estimates
    pca.py --optimize=fmin --resume

    # OR optimize using emcee
    # default samples = 100
    pca.py --optimize=emcee --samples=100
    pca.py --optimize=emcee --resume

    # Make a triangle plot of the emcee output
    pca.py --plot=emcee

    # Make some plots showing weight interpolations using the emulator
    pca.py --plot=emulator --params=fmin
    # OR
    pca.py --plot=emulator --params=emcee

    # Once you've OK'd the parameters, then store them to the HDF5 file
    pca.py --store --params=fmin
    # OR
    pca.py --store --params=emcee


After doing some more analysis, we'll want to make a bunch of plots showing the scatter of interpolated spectra against what the gridpoint spectrum looks like.

Now that you've optimized the emulator for the specific spectrum you'd like to fit, we can use a series of tools to fit the spectrum. Further customization will require writing your own python scripts.

These codes are much simpler and just output everything to the local directory.

Optimize the grid and observational parameters (:math:`\Theta`)

    star.py --optimize=Theta

    star.py --optimize=Cheb

This script will leave you with a single JSON file which specifies the Theta parameters. The fit might be OK, but is probably not the best you can do, especially since we haven't allowed any flexibility in the Chebyshev paramteters that take care of calibration uncertainties. Hopefully, however, your estimates of radial velocity, Omega, and vsini are in the ballpark of what you might expect. To check that this is the case, it would be a great idea to generate model spectra and plot them to examine the residuals of the fit.

    # Write out model, data, residuals for each order in the CWD
    star.py --generate


Now we can plot these files using our plotting programs.

    splot.py s0_o23_spec.json --matplotlib

    splot.py --D3

    star.py --sample=Theta

Optimize the noise parameters (:math:`\Phi`)

    star.py --optimize=Phi

Starting values for the nuisance parameters (:math:`\Phi`) are read from `*phi.json` files located in the current working directory. If you don't feel like optimizing the Chebyshev polynomials first, then to generate a set of these files for default values read from your config file, run

    star.py --initPhi

Note that this will overwrite any of your current `*phi.json` files in the current working directory. If you previously optimized the Cheb parameters, you may want to borrow these values and use them here.

On all subsquent runs, the starting values are taken from these. So, if you are doing many iterative runs where you by now have a good estimate of the final parameter values, it might be worthwhile to use a text editor to go and edit `s0_o22phi.json` and associated files by hand to these values, in order to speed convergence.

Sample in the Theta and Chebyhev parameters at the same time.

    star.py --sample=ThetaCheb --samples=100

Sample in the Theta, Chebyshev, and global covariance parameters at the same time.

    star.py --sample=ThetaPhi --samples=5

In actuallity you will probably want something like `--samples=5000` or more to get a statistical exploration of the space, but before waiting for a long run to finish it would be good to check that the machinery worked for a small run first.

Then, you can use the `chain.py` tool to examine and plot the parameter estimates. First, navigate to the directory that has the samples. Generally this will be something like `output/WASP14/run01` or whatever you have specified in your `config.yaml`. Then, use the tool to examine the Markov Chain

    chain.py --files mc.hdf5 --chain

Once you have a reasonable guess at the parameters, update your `config.yaml` file and `*phi.json` files to these best-fit parameters. Then, you'll want to create a new residual spectrum

    star.py --generate

Then, we can use this residual spectrum to search for and instantiate the regions for a given order. The JSON file includes the model, data, and residual.

    regions.py s0_o23spec.json --sigma=3 --find

This will create a file called something like `s0_o23region_list.json`, which contains a list of the centroids of each of these lines.

Then, go through and optimize the regions in this list. This will attempt to optimize the line kernels in the list.

    region_optimize.py s0_o23spec.json s0_o23regions.json --sigma0=2.