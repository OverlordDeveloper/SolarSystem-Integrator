from ursina import *
from ursina.shaders import lit_with_shadows_shader # you have to apply this shader to enties for them to recieve shadows.
import numpy as np
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
import planets
from datetime import date
from prettytable import PrettyTable
import os
# create a window
app = Ursina()
window.title = 'Solar System'    
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = False


speed = 1
dt = planets.dt * speed
AU = planets.AU

index = 0
pause = False

initState = planets.InitialState()
objects = planets.LoadSystem() 

Sky(texture = 'cry.png') #sky cry 

EditorCamera()

# UI Stuff
Dropdown = DropdownMenu('File', buttons=(
    DropdownMenuButton('Export'),
    DropdownMenu('Options', buttons=(
        DropdownMenuButton('Animation'),
        DropdownMenuButton('Enable/Disable Planets'),
    )),
    DropdownMenuButton('Exit')
    ))

ExportPanel = WindowPanel(color=color.gray,
    title='Export Window',
    content=(
        Text('Start Date(yyyy-mm-dd)'),
        InputField(),
        Text('End Date(yyyy-mm-dd)'),
        InputField(),
        Button(text='Export', color=color.azure)
        ),
    )

DateFormatError = WindowPanel(color = color.gray,
    title='Error!',
    content=(
        Text('Wrong date format'),
        Button(text='Ok :(', color=color.azure)
        ),
    )

def ToggleError():
    DateFormatError.enabled = not DateFormatError.enabled 

def ToggleExport():
    ExportPanel.enabled = not ExportPanel.enabled

DateFormatError.content[1].on_click = ToggleError
Dropdown.buttons[0].on_click = ToggleExport
Dropdown.buttons[2].on_click = application.quit

def AddTableRow(table, index):

    row = [str(index)]
    global objects
    
    for i in range(len(objects) - 1):
        if objects[i].enabled == False:
            row.append("")
        else:
            string = ""
            string += "x: " + str(objects[i]._position[index][0]) + " " + "y: " + str(objects[i]._position[index][1]) + " " + "z: " + str(objects[i]._position[index][2]) + "\n" + "vx: " + str(objects[i]._velocity[index][0]) + " " + "vy: " + str(objects[i]._velocity[index][1]) + " " + "vz: " + str(objects[i]._velocity[index][2]) 
            row.append(string)

    table.add_row(row)


def ExportDataTable():
    start = ExportPanel.content[1].text
    end = ExportPanel.content[3].text
    
    try:
        start_s = start.split('-')
        end_s = end.split('-')

        base_d = date(2020, 1, 1)
        d0 = date(int(start_s[0]), int(start_s[1]), int(start_s[2]))
        d1 = date(int(end_s[0]), int(end_s[1]),int(end_s[2]))

        delta0 = d0 - base_d
        delta1 = d1 - d0


        # Back to start
        ResetSystem()

        # Loop until the end date 

        LoopSystem((d1 - base_d).days)
        
        f = open(os.path.dirname(os.path.realpath(__file__)) + "\Export.txt", "a")
        f.truncate(0)

        infoTable = PrettyTable(["Start Date", "End Date", "Number of days", "Period of integration"])
        infoTable.add_row([start, end, str(delta1.days), "1d"])

        dataTable = PrettyTable(["Day", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"])
        dataTable.hrules = 1

        for i in range(delta0.days, delta1.days - 1):
            AddTableRow(dataTable, i)
 
        f.write(str(infoTable))
        f.write("\n")
        f.write(" Symbol meaning: \n")
        f.write("X:      X-component of position vector (m) \n")
        f.write("Y:      Y-component of position vector (m) \n")
        f.write("Z:      Z-component of position vector (m) \n")
        f.write("VX:     X-component of velocity vector (m/sec) \n")
        f.write("VY:     Y-component of velocity vector (m/sec) \n")
        f.write("VZ:     Z-component of velocity vector (m/sec) \n")

        f.write("\n")

        f.write(str(dataTable))
        f.close()
        ToggleExport()
        
    except:
        if DateFormatError.enabled == False:
            ToggleError()


def ResetSystem():
    global index
    global pause
    pause = True
    index = 0
    ind = 0
    for i in range(len(objects) - 1):
        objects[i].Reset(ind, initState)
        ind += 2


AnimationPanel = WindowPanel(color=color.gray,
    title='Animation Window',
        content=(
            Space(),
        Button(text='Play', color=color.azure, scale=.25),
        Button(text='Pause', color=color.azure, scale=.25),
        Button(text='Restart', color=color.azure, scale=.25),
        Slider(min = 0.001, max = 10, default = 1)
        ),
    )

def UpdateSpeed():
    global speed
    global dt
    speed = float(AnimationPanel.content[4].value)
    dt = planets.dt * speed

def ToggleAnimation():
    AnimationPanel.enabled = not AnimationPanel.enabled 

def Play():
    global pause
    pause = False

def Pause():
    global pause
    pause = True

AnimationPanel.content[1].on_click = Play
AnimationPanel.content[2].on_click = Pause
AnimationPanel.content[3].on_click = ResetSystem
AnimationPanel.content[4].on_value_changed = UpdateSpeed
Dropdown.buttons[1].buttons[0].on_click = ToggleAnimation

ExportPanel.content[4].on_click = ExportDataTable

ToggleError()
ToggleExport()
ToggleAnimation()


column = [None for x in range(9)]
names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

def SetObjectStateButtons(name):
    
    Pause()
    ResetSystem()

    global objects
    global column
    for i in range(len(names)):
        if names[i] == name:

            if objects[i].enabled == True:
                objects[i].SetState(False) 
                column[i].color = color.red
            else:
                objects[i].SetState(True) 
                column[i].color = color.green
            
for i in range(8):
    column[i] = Button(text=names[i], color=color.green,scale=Vec3(0.22, 0.08, 1), position=Vec3(-0.75, 0.5 - (i + 1) * 0.09, 1))
    column[i].on_click = Func(SetObjectStateButtons, column[i].text)


def UpdateObjectState():
    global column
    global pause
    for c in column:
        c.enabled = not c.enabled
    
    Play()

column[8] = Button(text="Close", color=color.gray,scale=Vec3(0.22, 0.08, 1), position=Vec3(-0.75, 0.5 - (9) * 0.09, 1), on_click = UpdateObjectState)
Dropdown.buttons[1].buttons[1].on_click = UpdateObjectState

UpdateObjectState()
def LoopSystem(var):

    global objects
    global dt
    for index in range(0, var):
        for obj in objects:
            if obj.static == False:
                obj.UpdatePartialPos(index, dt)

        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                        
                if not objects[i].enabled:
                    continue

                if not objects[j].enabled:
                    continue

                f_vec = objects[i].GravitationalForce(objects[j], index)

                objects[i]._vnew[0] += dt * f_vec[0] / objects[i].mass
                objects[i]._vnew[1] += dt * f_vec[1] / objects[i].mass
                objects[i]._vnew[2] += dt * f_vec[2] / objects[i].mass

                objects[j]._vnew[0] -= dt * f_vec[0] / objects[j].mass
                objects[j]._vnew[1] -= dt * f_vec[1] / objects[j].mass
                objects[j]._vnew[2] -= dt * f_vec[2] / objects[j].mass


        for obj in objects:
            obj._velocity.append(obj._vnew)

            xp = obj._partialPos[0] + 1 / 2.0 * dt * obj._velocity[index + 1][0]
            yp = obj._partialPos[1] + 1 / 2.0 * dt * obj._velocity[index + 1][1]
            zp = obj._partialPos[2] + 1 / 2.0 * dt * obj._velocity[index + 1][2]

            obj._position.append([xp, yp, zp])    

def update():
    global index
    global pause
    global dt
    global speed
    if pause == False:

        for obj in objects:
            if obj.static == False:
                obj.UpdatePartialPos(index, dt)

        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                    
                if not objects[i].enabled:
                    continue

                if not objects[j].enabled:
                    continue

                f_vec = objects[i].GravitationalForce(objects[j], index)

                objects[i]._vnew[0] += dt * f_vec[0] / objects[i].mass
                objects[i]._vnew[1] += dt * f_vec[1] / objects[i].mass
                objects[i]._vnew[2] += dt * f_vec[2] / objects[i].mass

                objects[j]._vnew[0] -= dt * f_vec[0] / objects[j].mass
                objects[j]._vnew[1] -= dt * f_vec[1] / objects[j].mass
                objects[j]._vnew[2] -= dt * f_vec[2] / objects[j].mass


        for obj in objects:

            obj._velocity.append(obj._vnew)

            xp = obj._partialPos[0] + 1 / 2.0 * dt * obj._velocity[index + 1][0]
            yp = obj._partialPos[1] + 1 / 2.0 * dt * obj._velocity[index + 1][1]
            zp = obj._partialPos[2] + 1 / 2.0 * dt * obj._velocity[index + 1][2]

            obj._position.append([xp, yp, zp])

            obj.x = obj._position[index][0] / AU * 20
            obj.y = obj._position[index][1] / AU * 20
            obj.z = obj._position[index][2] / AU * 20
            
            
            # draw trajectory line
           
            if len(obj._trajectoryMesh.vertices) > int(obj._maxPoint / speed):
                obj._trajectoryMesh.vertices.pop(0)

            obj._trajectoryMesh.vertices.append([obj.x , obj.y, obj.z])
        

            obj._trajectoryMesh.triangles = [range(0, len(obj._trajectoryMesh.vertices) - 1)]
            if( len(obj._trajectoryMesh.vertices) > 2):
                obj._trajectoryMesh.generate()

        index = index + 1

    return None

app.run()
