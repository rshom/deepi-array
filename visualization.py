''' Visualization from camera array

'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def build_cam_graphic(P, color='r', scaled_focal_len=5,
                      aspect_ratio=0.3):

    a = aspect_ratio
    f = scaled_focal_len
    
    V= np.array([[  0,    0,0,1],
                 [f*a, -f*a,f,1],
                 [f*a,  f*a,f,1],
                 [-f*a, f*a,f,1],
                 [-f*a,-f*a,f,1]])

    V = V @ P.T
    meshes = [[V[0,:-1], V[1][:-1], V[2,:-1]],
              [V[0,:-1], V[2,:-1], V[3,:-1]],
              [V[0,:-1], V[3,:-1], V[4,:-1]],
              [V[0,:-1], V[4,:-1], V[1,:-1]],
              [V[1,:-1], V[2,:-1], V[3,:-1], V[4,:-1]]]
    
    return Poly3DCollection(meshes, facecolors=color, linewidths=0.3,
                            edgecolors=color, alpha=0.35)



class Scene:
    def __init__(self):

        self.cams = []
        self.points = []
        self.lines = []

    def add_cam(self,P, color='r', scaled_focal_len=5,
                aspect_ratio=0.3):
        cam = build_cam_graphic(P, color='r', scaled_focal_len=5,
                                aspect_ratio=0.3)
        self.cams.append(cam)



def plot_scene(scene,ax=None):

    if ax is None:
        fig,ax = plt.subplots(1,1, subplot_kw={'projection':'3d'})
    
    ax.set_aspect("auto")
    ax.set_xlim([-50, 50])
    ax.set_ylim([-50, 50])
    ax.set_zlim([0,50])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    for cam in self.cams:
        ax.add_collection3d(cam)

    # TODO: plot the calibration checks
    # TODO: plot a sample of shared points

    return ax



if __name__=='__main__':

    N=4
    P = [np.eye(4) for n in range(N)]
    R = [np.eye(3) for n in range(N)]
    T = []
    x_dist = 10
    y_dist = 10
    T.append(np.array([0,0,0]))
    T.append(np.array([0,y_dist,0]))
    T.append(np.array([x_dist,0,0]))
    T.append(np.array([x_dist,y_dist,0]))


    scene = Scene()

    for n in range(N):
        P[n][:3,:3] = R[n]
        P[n][:3,-1] = T[n]

        scene.add_cam(P[n])

    # Plot scene
    fig,ax = plt.subplots(1,1, subplot_kw={'projection':'3d'})
    

    plot_scene(scene,ax)


    plt.show()
