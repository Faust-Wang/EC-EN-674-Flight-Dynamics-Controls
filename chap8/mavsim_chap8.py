"""
mavsim_python
    - Chapter 8 assignment for Beard & McLain, PUP, 2012
    - Last Update:
        2/21/2019 - RWB
"""
import sys
sys.path.append('..')
import numpy as np
import parameters.simulation_parameters as SIM
import parameters.aerosonde_parameters as P

from chap2.mav_viewer import mav_viewer
from chap3.data_viewer import data_viewer
from chap4.wind_simulation import wind_simulation
from chap6.autopilot import autopilot
from chap7.mav_dynamics import mav_dynamics
from chap8.observer_ekf import observer
from tools.signals import signals
from message_types.msg_state import msg_state


def updateInput(true,estimate):
    input.pn = estimate.pn      # inertial north position in meters
    input.pe = estimate.pn      # inertial east position in meters
    input.h = estimate.h       # inertial altitude in meters
    input.phi = estimate.phi     # roll angle in radians
    input.theta = estimate.theta   # pitch angle in radians
    input.psi = estimate.psi     # yaw angle in radians
    input.Va = estimate.Va      # airspeed in meters/sec
    input.alpha = estimate.alpha   # angle of attack in radians
    input.beta = estimate.beta    # sideslip angle in radians
    input.p = estimate.p       # roll rate in radians/sec
    input.q = estimate.q       # pitch rate in radians/sec
    input.r = estimate.r       # yaw rate in radians/sec
    input.Vg = estimate.Vg      # groundspeed in meters/sec
    input.gamma = true.gamma   # flight path angle in radians
    input.chi = estimate.chi     # course angle in radians
    input.wn = estimate.wn      # inertial windspeed in north direction in meters/sec
    input.we = estimate.we      # inertial windspeed in east direction in meters/sec
    input.bx = estimate.bx      # gyro bias along roll axis in radians/sec
    input.by = estimate.by      # gyro bias along pitch axis in radians/sec
    input.bz = estimate.bz      # gyro bias along yaw axis in radians/sec

# initialize the visualization
VIDEO = False  # True==write video, False==don't write video
mav_view = mav_viewer()  # initialize the mav viewer
data_view = data_viewer()  # initialize view of data plots
if VIDEO == True:
    from chap2.video_writer import video_writer
    video = video_writer(video_name="chap8_video.avi",
                         bounding_box=(0, 0, 1000, 1000),
                         output_rate=SIM.ts_video)

# initialize elements of the architecture
wind = wind_simulation(SIM.ts_simulation)
mav = mav_dynamics(SIM.ts_simulation,[P.pn0,P.pe0,P.pd0])
ctrl = autopilot(SIM.ts_simulation)
obsv = observer(SIM.ts_simulation,[P.pn0,P.pe0,P.pd0])
input = msg_state()

# autopilot commands
from message_types.msg_autopilot import msg_autopilot
commands = msg_autopilot()
Va_command = signals(dc_offset=25.0, amplitude=3.0, start_time=2.0, frequency = 0.01)
h_command = signals(dc_offset=100.0, amplitude=10.0, start_time=0.0, frequency = 0.02)
chi_command = signals(dc_offset=np.radians(30), amplitude=np.radians(45), start_time=5.0, frequency = 0.015)
# initialize the simulation time
sim_time = SIM.start_time

# main simulation loop
print("Press Command-Q to exit...")
jj = 0
while sim_time < SIM.end_time:
    #while jj < 5:
    jj += 1

    #-------autopilot commands-------------
    commands.airspeed_command = Va_command.square(sim_time)
    commands.course_command = chi_command.square(sim_time)
    commands.altitude_command = h_command.square(sim_time)

    #-------controller-------------
    measurements = mav.sensors  # get sensor measurements
    estimated_state = obsv.update(measurements)  # estimate states from measurements
    updateInput(mav.msg_true_state,estimated_state)
    delta, commanded_state = ctrl.update(commands,input)
    #delta, commanded_state = ctrl.update(commands, estimated_state)

    #-------physical system-------------
    current_wind = wind.update()  # get the new wind vector
    #current_wind = np.zeros((6,1))
    mav.update_state(delta, current_wind)  # propagate the MAV dynamics
    mav.update_sensors()

    #-------update viewer-------------
    mav_view.update(mav.msg_true_state)  # plot body of MAV
    data_view.update(mav.msg_true_state, # true states
                     estimated_state, # estimated states
                     commanded_state, # commanded states
                     SIM.ts_simulation)
    if VIDEO == True: video.update(sim_time)

    #-------increment time-------------
    sim_time += SIM.ts_simulation

if VIDEO == True: video.close()
