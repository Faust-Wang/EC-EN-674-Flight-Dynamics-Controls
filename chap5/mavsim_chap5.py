"""
mavSimPy
    - Chapter 5 assignment for Beard & McLain, PUP, 2012
    - Update history:
        1/1/2019 - RWB
        1/29/2019 - RWB
        2/2/2019 - RWB
"""
import sys
sys.path.append('..')
import numpy as np
import parameters.simulation_parameters as SIM
import parameters.aerosonde_parameters as P

from chap2.mav_viewer import mav_viewer
#from chap2.video_writer import video_writer
from chap3.data_viewer import data_viewer
from chap4.mav_dynamics import mav_dynamics
from chap4.wind_simulation import wind_simulation
from chap5.trim import compute_trim
from chap5.compute_models import compute_ss_model, compute_tf_model
import time

# initialize the visualization
VIDEO = False  # True==write video, False==don't write video
mav_view = mav_viewer()  # initialize the mav viewer
data_view = data_viewer()  # initialize view of data plots
if VIDEO == True:
    video = video_writer(video_name="chap5_video.avi",
                         bounding_box=(0, 0, 1000, 1000),
                         output_rate=SIM.ts_video)


# initialize elements of the architecture
wind = wind_simulation(SIM.ts_simulation)
mav = mav_dynamics(SIM.ts_simulation,[P.pn0,P.pe0,P.pd0])

# use compute_trim function to compute trim state and trim input
Va = 25.
gamma = 0.*np.pi/180.
trim_state, trim_input = compute_trim(mav, Va, gamma)

# OUTPUT TO FILE
filename = "../chap5/trim_results.py"
file = open(filename,'w')
file.write("import numpy as np\n\n")
# trim state
file.write("trim_state = np.array([")
trim_state.tofile(file,sep=",")
file.write("])\n\n")
# trim inputs
file.write("trim_input = np.array([")
trim_input.tofile(file,sep=",")
file.write("])\n\n")
# Va
file.write("Va = ")
file.write(str(Va))
file.write('\n\n')
# gamma
file.write("gamma = ")
file.write(str(gamma))
file.write('\n\n')
# gamma
file.write("Vg = ")
file.write(str(mav._Vg))
file.write('\n\n')
# alpha
file.write("alpha = ")
file.write(str(mav._alpha))
file.write('\n\n')
# close file
file.close()


#print("trim_state=",trim_state)
#print("trim_input=",trim_input)
mav._state = trim_state  # set the initial state of the mav to the trim state
mav._update_velocity_data()
delta = trim_input  # set input to constant constant trim input


# # compute the state space model linearized about trim
A_lon, B_lon, A_lat, B_lat = compute_ss_model(mav, trim_state, trim_input)
T_phi_delta_a, T_chi_phi, T_theta_delta_e, T_h_theta, \
T_h_Va, T_Va_delta_t, T_Va_theta, T_beta_delta_r \
    = compute_tf_model(mav, trim_state, trim_input)

# initialize the simulation time
sim_time = SIM.start_time

# main simulation loop
print("Press Command-Q to exit...")
while sim_time < SIM.end_time:

    #-------physical system-------------
    #current_wind = wind.update()  # get the new wind vector
    current_wind = np.zeros((6,1))
    mav.update_state(delta, current_wind)  # propagate the MAV dynamics

    #-------update viewer-------------
    mav_view.update(mav.msg_true_state)  # plot body of MAV
    data_view.update(mav.msg_true_state, # true states
                     mav.msg_true_state, # estimated states
                     mav.msg_true_state, # commanded states
                     SIM.ts_simulation)
    if VIDEO == True:
        video.update(sim_time)

    #-------increment time-------------
    sim_time += SIM.ts_simulation

if VIDEO == True:
    video.close()
