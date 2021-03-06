"""
This code tests the discretization procedure and computes the system step response.

"""
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv

# define the system parameters

m1=20  ; m2=20   ; k1=1000  ; k2=2000 ; d1=1  ; d2=5; 


# define the continuous-time system matrices
Ac=np.matrix([[0, 1, 0, 0],[-(k1+k2)/m1 ,  -(d1+d2)/m1 , k2/m1 , d2/m1 ], [0 , 0 ,  0 , 1], [k2/m2,  d2/m2, -k2/m2, -d2/m2]])
Bc=np.matrix([[0],[0],[0],[1/m2]])
Cc=np.matrix([[1, 0, 0, 0]])

#define an initial state for simulation
#x0=np.random.rand(2,1)
x0=np.zeros(shape=(4,1))

#define the number of time-samples used for the simulation and the sampling time for the discretization
time=300
sampling=0.05

#define an input sequence for the simulation
#input_seq=np.random.rand(time,1)
input_seq=5*np.ones(time)
#plt.plot(input_sequence)

I=np.identity(Ac.shape[0]) # this is an identity matrix
A=inv(I-sampling*Ac)
B=A*sampling*Bc
C=Cc


# check the eigenvalues
eigen_A=np.linalg.eig(Ac)[0]
eigen_Aid=np.linalg.eig(A)[0]


# the following function simulates the state-space model using the backward Euler method
# the input parameters are:
#    -- Ad,Bd,Cd           - discrete-time system matrices 
#    -- initial_state      - the initial state of the system 
#    -- time_steps         - the total number of simulation time steps 
# this function returns the state sequence and the output sequence
# they are stored in the matrices Xd and Yd respectively
def simulate(Ad,Bd,Cd,initial_state,input_sequence, time_steps):
    Xd=np.zeros(shape=(A.shape[0],time_steps+1))
    Yd=np.zeros(shape=(C.shape[0],time_steps+1))
    
    for i in range(0,time_steps):
       if i==0:
           Xd[:,[i]]=initial_state
           Yd[:,[i]]=C*initial_state
           x=Ad*initial_state+Bd*input_sequence[i]
       else:
           Xd[:,[i]]=x
           Yd[:,[i]]=C*x
           x=Ad*x+Bd*input_sequence[i]
    Xd[:,[-1]]=x
    Yd[:,[-1]]=C*x
    return Xd, Yd
    
state,output=simulate(A,B,C,x0,input_seq, time)    

plt.plot(output[0,:])
plt.xlabel('Discrete time instant-k')
plt.ylabel('Position- d')
plt.title('System response')
plt.savefig('step_response1.png')
plt.show()   