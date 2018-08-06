from functions.mat_to_netcdf4 import main as mat_to_netcdf4
from glob import glob
import pandas as pd
import os

# Define inputs
# mat_dir = '/Users/mikesmith/Documents/projects/bpu/totals/hudson_south/mat'
mat_dir = '/Users/mikesmith/Documents/projects/bpu/totals/domain/mat'
files = glob(os.path.join(mat_dir, '*.mat'))

files = ['/Volumes/home/michaesm/z/totals/data/2016_01/tuv_oi_MARA_2016_01_03_1100.mat']
grid_file = '/Users/mikesmith/Documents/git/rucool/codar_processing/totals/grid_files/maracoos_grid_6km_extended.txt'
save_dir = '/Users/mikesmith/Documents/projects/bpu/totals/domain/nc/'

threshold = dict(u_err=1.0, v_err=1.0, uv_covariance=1.0)

# load csv file containing the grid
grid = pd.read_csv(grid_file, sep=',', header=None, names=['lon', 'lat'], delim_whitespace=True)

user_attributes = dict(title='MARACOOS 6km Sea Surface Currents',
                       naming_authority='edu.rutgers.marine.rucool',
                       comment='Network maintained by MARACOOS. For oi_* global attribute explanations, see references attribute',
                       acknowledgment='This data is provided by the Mid-Atlantic Regional Association Coastal Ocean Observing System (MARACOOS). Funding is provided by the U.S. Integration Ocean Observing System (IOOS).',
                       standard_name_vocabulary='CF Standard Name Table v41',
                       creator_name='Michael Smith',
                       creator_email='michaesm@marine.rutgers.edu',
                       creator_url='rucool.marine.rutgers.edu',
                       institution='Center for Ocean Observing and Leadership, Department of Marine & Coastal Sciences, Rutgers University',
                       project='Mid-Atlantic Regional Association Coastal Ocean Observing System - High Frequency Radar Sea Surface Current Mapping',
                       sea_name='Mid-Atlantic Bight',
                       creator_type='person',
                       creator_institution='Rutgers University',
                       contributor_name='Scott Glenn, Josh Kohut, Hugh Roarty, Ethan Handel, Michael Smith, Laura Nazzaro, Teresa Updyke, Larry Atkinson, Rich Arena, Wendell Brown, Mike Muglia, Harvey Seim',
                       contributor_role='Principal Investigator, Principal Investigator, Principal Investigator, Hardware Maintenance, Data Manager, Data Manager, Hardware Maintenance, Principal Investigator, Hardware Maintenance, Principal Investigator, Hardware Maintenance, Principal Investigator',
                       platform='MARACOOS HF Radar 5MHz Network',
                       instrument='Network includes CODAR sites AMAG, ASSA, BLCK, BRIG, CEDR, CORE, DUCK, FARO, HATY, HEMP, HOOK, LISL, LOVE, MABO, MRCH, MVCO, NANT, NAUS, PYFC, and WILD',
                       references='http://maracoos.org/node/146 https://rucool.marine.rutgers.edu/facilities https://rucool.marine.rutgers.edu/data',
                       summary='Optimally Interpolated Total Vectors calculated by HFRProgs toolbox using MATLAB. Mercator lat/lon projection',
                       ncei_template_version='NCEI_NetCDF_Grid_Template_v2.0',
                       history='Hourly codar radial data combined into one hourly file containing vectors.',
                       cdm_data_type='Grid',
                       source='CODAR SeaSonde Surface Current Mapping Device',
                       processing_level='Level 3',
                       keywords='Environmental Advisories > Marine Advisories > Marine Weather/Forecast, Oceans > Coastal Processes, Oceans > Ocean Circulation, Oceans > Ocean Waves, Oceans > Ocean Winds, Oceans > Ocean Tides, Spectral/Engineering > Radar',
                       publisher_name='NOAA National Centers for Environmental Information',
                       publisher_email='ncei.info@noaa.gov',
                       publisher_url='www.ncei.noaa.gov')

for file in files:
    # save_dir = os.path.dirname(file)
    mat_to_netcdf4(grid, file, save_dir, user_attributes, threshold)
