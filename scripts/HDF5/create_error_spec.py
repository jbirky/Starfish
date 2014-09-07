from StellarSpectra import grid_tools

interface = grid_tools.HDF5Interface("libraries/PHOENIX_TRES_F.hdf5")

machine = grid_tools.ErrorSpectrumCreator(interface)
machine.process_grid()