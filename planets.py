from ursina import Entity, Vec3, Mesh, color, Tooltip
import numpy as np

# The gravitational constant G
AU = (149.6e6 * 1000)     # 149.6 million km, in meters.
SCALE = 0.000001/ AU
G = 6.67428e-11
dt = 24 * 3600 # one day in seconds

class Object(Entity):

    def __init__(self, mass, radius, lineColor, model, texture):
        super().__init__(model = model, texture = texture)

        self.mass = mass
        self.radius = radius
        
        #Applies for the Sun for example
        self.static = False

        self._position = [[0.0, 0.0, 0.0]]
        self._velocity = [[0.0, 0.0, 0.0]]
        self._acceleration = [[0.0, 0.0, 0.0]]
        self._vnew = [0.0, 0.0, 0.0]
        self._partialPos = [0.0, 0.0, 0.0]

        self._maxPoint = 100

        self._trajectoryMesh = Mesh(mode='line',  vertices = [], thickness = 1)
        
        self._line = Entity(model=self._trajectoryMesh, color=lineColor, z=0)

    def SetState(self, state):
        self.enabled = state
        self._line.enabled = state

    def Reset(self, index, stateContainer):
        self._position = stateContainer[index].copy()
        self._velocity = stateContainer[index + 1].copy()
        self._acceleration = [[0.0, 0.0, 0.0]].copy()
        self._vnew = [0.0, 0.0, 0.0].copy()
        self._partialPos = [0.0, 0.0, 0.0].copy()


        self._trajectoryMesh.vertices = []
        
        #self._line = Entity(model=self._trajectoryMesh, color=color.red, z=-1)


    def GravitationalForce(self, otherObj, index):

        x = otherObj._position[0][0] - self._partialPos[0]
        y = otherObj._position[0][1] - self._partialPos[1]
        z = otherObj._position[0][2] - self._partialPos[2]
        

        r_vec = np.array([x, y, z])
        r_mag = np.linalg.norm(r_vec)
        r_hat = r_vec / r_mag

        r = np.sqrt(np.power(x, 2) +
                    np.power(y, 2) +
                    np.power(z, 2))

        f = (G * self.mass * otherObj.mass ) /  np.power(r_mag, 2) 
        f_vec = f * r_hat


        return f_vec

    def UpdatePartialPos(self, index, dt):

        self._partialPos[0] = self._position[index][0] + self._velocity[index][0] * dt / 2.0
        self._partialPos[1] = self._position[index][1] + self._velocity[index][1] * dt / 2.0
        self._partialPos[2] = self._position[index][2] + self._velocity[index][2] * dt / 2.0

        self._vnew = self._velocity[index].copy()

   

def LoadSystem():

    Sun = Object(mass = 1.989e30, radius = 695508e3 , lineColor = color.white, model="Assets/Sphere.obj", texture="Assets/Sun-map")
    Sun._position = [[0.0, 0.0, 0.0]]
    Sun.scale = 1
    Sun.static = True

    Mercury = Object(mass = 330e21, radius = 2439.4e3, lineColor = color.light_gray , model="Assets/Sphere.obj", texture="Assets/Mercury-map")
    Mercury.position = Vec3(20, 0, 0)
    Mercury.scale =  Mercury.radius / Sun.radius * 100
    Mercury._maxPoint = 80

    Venus = Object(mass = 4.867e24, radius = 6052e3, lineColor = color.lime , model="Assets/Sphere.obj", texture="Assets/Venus-map")
    Venus.position = Vec3(30, 0, 0)
    Venus.scale = Venus.radius / Sun.radius  * 100
    Venus._maxPoint = 215

    Earth = Object(mass = 5.972e24, radius = 6371e3, lineColor = color.blue , model="Assets/Sphere.obj", texture="Assets/Earth-map")
    Earth.position = Vec3(40, 0, 0)
    Earth.scale = Earth.radius / Sun.radius  * 100
    Earth._maxPoint = 366

    Mars = Object(mass = 641.71e21, radius = 3389e3, lineColor = color.orange, model="Assets/Sphere.obj", texture="Assets/Mars-map")
    Mars.position = Vec3(50, 0, 0)
    Mars.scale = Mars.radius /  Sun.radius  * 100
    Mars._maxPoint = 666 # the devil ? 

    Jupiter = Object(mass = 1.898e27, radius = 69911e3, lineColor = color.yellow, model="Assets/Sphere.obj", texture="Assets/Jupiter-map")
    Jupiter.position = Vec3(60, 0, 0)
    Jupiter.scale = Jupiter.radius / Sun.radius  * 100
    Jupiter._maxPoint = 6000

    Saturn = Object(mass = 5.683e26, radius = 58232e3, lineColor = color.yellow, model="Assets/Sphere.obj", texture="Assets/Saturn-map")
    Saturn.position = Vec3(70, 0, 0)
    Saturn.scale = Saturn.radius / Sun.radius  * 100
    Saturn._maxPoint = 6666 


    Uranus = Object(mass = 8.681e25, radius = 25362e3, lineColor = color.azure , model="Assets/Sphere.obj", texture="Assets/Uranus-map")
    Uranus.position = Vec3(80, 0, 0)
    Uranus.scale =  Uranus.radius / Sun.radius  * 100
    Uranus._maxPoint = 66666

    Neptune = Object(mass = 1.024e26, radius = 24622e3, lineColor = color.magenta, model="Assets/Sphere.obj", texture="Assets/Neptune-map")
    Neptune.position = Vec3(90, 0, 0)
    Neptune.scale = Neptune.radius / Sun.radius * 100
    Neptune._maxPoint = 666666
    

    # Km/s to m/s
    Mercury._position = [[-1.004302793346122E+07 * 1000 ,  -6.782848247285485E+07 * 1000, -4.760889633162629E+06 * 1000]] 
    Mercury._velocity = [[3.847265155592926E+01 * 1000, -4.158689546981208E+00 * 1000, -3.869763647804497E+00 * 1000]] 

    Venus._position = [[1.076209595805564E+08 * 1000 ,  8.974122818036491E+06 * 1000, -6.131976661929069E+06 * 1000]] 
    Venus._velocity = [[-2.693485084259549E+00 * 1000, 3.476650462014290E+01 * 1000, 6.320912271467272E-01 * 1000]] 

    Earth._position = [[-2.545323708273825E+07 * 1000 ,  1.460913442868109E+08 * 1000, -2.726527903765440E+03 * 1000]] 
    Earth._velocity = [[-2.986338200235307E+01 * 1000, -5.165822246700293E+00 * 1000, 1.135526860257752E-03 * 1000]] 

    Mars._position = [[-1.980535522170065E+08 * 1000 , -1.313944334060654E+08 * 1000, 2.072245594990239E+06 * 1000]] 
    Mars._velocity = [[1.439273929359666E+01 * 1000, -1.805004074289640E+01 * 1000, -7.312485979614864E-01 * 1000]] 

    Jupiter._position = [[7.814210740177372E+07 * 1000 , -7.769489405106664E+08 * 1000, 1.474081608655989E+06 * 1000]] 
    Jupiter._velocity = [[1.283931035365873E+01 * 1000, 1.930357075733133E+00 * 1000, -2.952599466798547E-01 * 1000]] 

    Saturn._position = [[5.674914809473343E+08 * 1000 , -1.388366463018738E+09 * 1000, 1.549265783457875E+06 * 1000]] 
    Saturn._velocity = [[8.406493531200095E+00 * 1000, 3.627774839464044E+00 * 1000, -3.983651341797232E-01 * 1000]] 

    Uranus._position = [[2.426731532276310E+09 * 1000 ,  1.703392504032894E+09 * 1000, -2.511215084173620E+07 * 1000]] 
    Uranus._velocity = [[-3.962351584219718E+00 * 1000, 5.256523421272158E+00 * 1000, 7.095167477538000E-02 * 1000]] 

    Neptune._position = [[4.374094274093674E+09 * 1000 ,  -9.514049067425712E+08 * 1000, -8.121317847458720E+07 * 1000]] 
    Neptune._velocity = [[1.118822506695780E+00 * 1000, 5.342644352002246E+00 * 1000, -1.362606261073369E-01 * 1000]] 

    return [ Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Sun]


def InitialState():
    state = [[[-1.004302793346122E+07 * 1000 ,  -6.782848247285485E+07 * 1000, -4.760889633162629E+06 * 1000]], [[3.847265155592926E+01 * 1000, -4.158689546981208E+00 * 1000, -3.869763647804497E+00 * 1000]],
             [[1.076209595805564E+08 * 1000 ,  8.974122818036491E+06 * 1000, -6.131976661929069E+06 * 1000]]  , [[-2.693485084259549E+00 * 1000, 3.476650462014290E+01 * 1000, 6.320912271467272E-01 * 1000]],
             [[-2.545323708273825E+07 * 1000 ,  1.460913442868109E+08 * 1000, -2.726527903765440E+03 * 1000]] , [[-2.986338200235307E+01 * 1000, -5.165822246700293E+00 * 1000, 1.135526860257752E-03 * 1000]],
             [[-1.980535522170065E+08 * 1000 , -1.313944334060654E+08 * 1000, 2.072245594990239E+06 * 1000]]  , [[1.439273929359666E+01 * 1000, -1.805004074289640E+01 * 1000, -7.312485979614864E-01 * 1000]],
             [[7.814210740177372E+07 * 1000 , -7.769489405106664E+08 * 1000, 1.474081608655989E+06 * 1000]]   , [[1.283931035365873E+01 * 1000, 1.930357075733133E+00 * 1000, -2.952599466798547E-01 * 1000]], 
             [[5.674914809473343E+08 * 1000 , -1.388366463018738E+09 * 1000, 1.549265783457875E+06 * 1000]]   , [[8.406493531200095E+00 * 1000, 3.627774839464044E+00 * 1000, -3.983651341797232E-01 * 1000]],
             [[2.426731532276310E+09 * 1000 ,  1.703392504032894E+09 * 1000, -2.511215084173620E+07 * 1000]]  , [[-3.962351584219718E+00 * 1000, 5.256523421272158E+00 * 1000, 7.095167477538000E-02 * 1000]],
             [[4.374094274093674E+09 * 1000 ,  -9.514049067425712E+08 * 1000, -8.121317847458720E+07 * 1000]] , [[1.118822506695780E+00 * 1000, 5.342644352002246E+00 * 1000, -1.362606261073369E-01 * 1000]]]
    
    return state

if __name__ == '__main__':
    LoadSystem()