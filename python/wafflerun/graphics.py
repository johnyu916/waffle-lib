import sys
#import pdb
from wafflecore.camera import camera_aspect
from wafflecore.compute import matrix_identity, ortho_make, look_at_make, perspective_make, orientation_up, matrix_translate, sum_arrays, matrix_rotate_ortho
from app.mouse import mouse_on_click_move, mouse_on_move, mouse_on_click
from app.keyboard import keyboard_on_event
from app.idle import idle
from shared import get_state

import numpy as np
from OpenGL.GL import (
    GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_FLOAT, GL_TRIANGLES, GL_BACK_LEFT, GL_VIEWPORT, GL_RGB, GL_UNSIGNED_BYTE, GL_INVALID_OPERATION, GL_INVALID_VALUE, GL_VERSION, GL_SHADING_LANGUAGE_VERSION, GL_DEPTH_TEST, GL_VERTEX_ARRAY, GL_COLOR_ARRAY, GL_LESS, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
    glEnable, glDisableClientState, glEnableClientState, glColorPointer, glGetAttribLocation, glGetUniformLocation, glUniformMatrix4fv, glEnableVertexAttribArray, glVertexAttribPointer, glDrawArrays, glDisableVertexAttribArray, glGetDoublev, glReadPixels, glReadBuffer, glGetString, glUseProgram, glViewport, glClear, glClearColor, glDepthFunc, glClearDepth,
    shaders, glFlush, glFinish)
from OpenGL.arrays import vbo
from OpenGL.GLUT import (
    glutInit, glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition, glutCreateWindow, glutDisplayFunc, glutPostRedisplay, glutIdleFunc, glutReshapeFunc, glutKeyboardFunc, glutMouseFunc, glutMainLoop, glutSwapBuffers, glutMotionFunc, glutPassiveMotionFunc, glutKeyboardUpFunc,
    GLUT_RGBA, GLUT_DOUBLE, GLUT_DEPTH
)
from time import time

# Number of the glut window.
window = 0
contexts = {}
vbos = {}

def run():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:   
    #  Double buffer 
    #  RGBA color
    # Alpha components supported 
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    
    # get a 640 x 480 window
    resolution = get_state()["camera"]["resolution"]
    glutInitWindowSize(int(resolution[0]), int(resolution[1]))
    
    # the window starts at the upper left corner of the screen 
    glutInitWindowPosition(0, 0)
    
    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("Waffle")

       # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.    
    glutDisplayFunc(DrawGLScene)
    
    # Uncomment this line to get full screen.
    # glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(idleFunc)
    
    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)
    
    # Register the function called when the keyboard is pressed.  
    glutKeyboardFunc(keyDown)
    glutKeyboardUpFunc(keyUp)
    glutMouseFunc(onMouseClick)
    glutMotionFunc(onMouseClickMove)
    glutPassiveMotionFunc(onMouseMove)

    # Initialize our window. 
    InitGL()
    init_world()
    init_interface()

    # Start Event Processing Engine    
    glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
def ReSizeGLScene(Width, Height):
    if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation

def idleFunc():
    # do state stuff.
    one = time()
    state = get_state()
    idle(state)
    two = time()
    #print "idleFunc idle time: ", (two - one)
    glutPostRedisplay()
    #DrawGLScene()

def DrawGLScene():
    modelview_matrix, projection_matrix = update_world_matrices()
    contexts["world"]["modelview"]["matrix"] = modelview_matrix
    contexts["world"]["projection"]["matrix"] = projection_matrix

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    # Clear The Screen And The Depth Buffer
    one = time()
    render_with_context(contexts["world"])
    render_with_context(contexts["interface"])
    two = time()
    glutSwapBuffers()
    three = time()
    #print "idleFunc render time: ", one, two, three

def InitGL():                # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                # Enables Depth Testing



# 0 is down, 1 is up.
def onMouseClick(button, mouse_state, x, y):
    #print "onMouseClick: {} {} {} {}".format(button, mouse_state, x, y)
    state = get_state()
    if mouse_state == 0:
        event = "MOUSE_DOWN"
    else:
        event = "MOUSE_UP"
    height = state["camera"]["resolution"][1]
    mouse_on_click(state, x, height - y, event)

def onMouseClickMove(x, y):
    """
    mouse clicked and moved.
    """
    #print "onMouseClickMove: {} {}".format(x, y)
    state = get_state()
    height = state["camera"]["resolution"][1]
    mouse_on_click_move(state, x, height - y)
    #print "onMouseClickMove context: {} ".format(state["mouse"]["context"])

def onMouseMove(x, y):
    """
    mouse moved but not clicked.
    """
    #print "onMouseMove: {} {}".format(x, y)
    state = get_state()
    height = state["camera"]["resolution"][1]
    mouse_on_move(state, x, height - y)

def keyDown(key, x, y):
    #print "keyDown: {} {} {}".format(key, x, y)
    state = get_state()
        #record("key released: {}".format(event.name))
    keyboard_on_event(state, key, "KEY_DOWN")
        #board.setKey(event.name, keyboard.KEY_RELEASED)

def keyUp(key, x, y):
    #print "keyUp: {} {} {}".format(key, x, y)
    state = get_state()
    keyboard_on_event(state, key, "KEY_UP")

def init_context(name, modelview_matrix, projection_matrix):
    state = get_state()
    with open(state["shaders"][name]['vertex_shader_path']) as f:
        vertex_shader_text = f.read()
    vertex_shader = shaders.compileShader(vertex_shader_text, GL_VERTEX_SHADER)
    with open(state["shaders"][name]['fragment_shader_path']) as f:
        fragment_shader_text = f.read()
    fragment_shader = shaders.compileShader(fragment_shader_text, GL_FRAGMENT_SHADER)
    shader = shaders.compileProgram(vertex_shader, fragment_shader)

    #print "init interface state: ", state

    position_location = glGetAttribLocation(shader, 'position')
    normal_location = glGetAttribLocation(shader, 'normal')
    color_location = glGetAttribLocation(shader, 'color')
    modelview_location = glGetUniformLocation(shader, 'modelViewMatrix')
    projection_location = glGetUniformLocation(shader, 'projectionMatrix')


    contexts[name] = {
        'shader': shader,
        'modelview': {
            'location': modelview_location,
            'matrix': modelview_matrix
        },
        'projection': {
            'location': projection_location,
            'matrix': projection_matrix
        },
        'position_location': position_location,
        'color_location': color_location,
        'normal_location': normal_location,
        'thing': state[name]
    }

def init_interface():
    state = get_state()
    resolution = state["camera"]["resolution"]
    projection_matrix = np.array(ortho_make(0, resolution[0], 0, resolution[1], -10.0, 10.0), 'f')
    modelview_matrix = np.array(matrix_identity(), 'f')
    init_context("interface", modelview_matrix, projection_matrix)


def init_world():
    modelview_matrix, projection_matrix = update_world_matrices()
    init_context("world", modelview_matrix, projection_matrix)


def update_world_matrices():
    #print '_update_world_matrices 1'
    state = get_state()
    camera = state["camera"]
    placement = camera["placement"]
    position = placement["position"]
    orientation = placement["orientation"]
    front = orientation["front"]
    up = orientation_up(orientation)
    # OpenGL matrices are column major, so transpose it.
    projection_matrix = np.array(perspective_make(camera["fovy"], camera_aspect(camera), camera["near"] , camera["far"]), 'f')
    # OpenGL matrices are column major, so transpose it.
    modelview_matrix = np.array(look_at_make(position, sum_arrays(position, front), up), 'f')
    #print 'repositioning finished: {}\n {}'.format(self.projection_matrix, self.modelview_matrix)
    return modelview_matrix, projection_matrix


# stack is the current modelview stack
def render_thing(thing, position_location, normal_location, color_location, modelview_location, context_matrix):
    try:
        translate = np.array(matrix_translate(thing["position"]), 'f')
    except:
        print "render_thing can't translate thing: ", thing
        exit()
    #print "render_thing type: ", thing["type"], thing["position"]
    context_matrix = np.dot(context_matrix, translate)

    rotates = thing["rotates"]
    if len(rotates) == 2:
        rotate0 = np.array(matrix_rotate_ortho(rotates[0]["angle"], rotates[0]["axis"]), 'f')
        tmp_matrix = np.dot(context_matrix, rotate0)
        rotate1 = np.array(matrix_rotate_ortho(rotates[1]["angle"], rotates[1]["axis"]), 'f')
        context_matrix = np.dot(tmp_matrix, rotate1)
    #print "render_thing:\n {}\n{}\n{}".format(translate, rotate0, rotate1)
    #print "context_matrix:\n", context_matrix
    glUniformMatrix4fv(modelview_location, 1, True, context_matrix)
    geometry = thing["geometry"]

    if geometry != None:
        if geometry["static"]:
            key = int(float(geometry["id"]))
            #print "thing type: {}, key: {}".format(thing["type"], key)
            if not key in vbos:
                vertices = geometry["vertices"]
                #print "adding geometry:\n{}".format(vertices[0])
                #vbos[key] = (vbo.VBO(np.array(vertices, 'f')), len(vertices))
                vbos[key] = (vbo.VBO(vertices), len(vertices))
            buffer_object, buffer_size = vbos[key]
        else:
            vertices = geometry["vertices"]
            buffer_object = vbo.VBO(vertices)
            buffer_size = len(vertices)
        #print "rendering type: {}, size: {}".format(buffer_object, buffer_size)
        #pdb.set_trace()
        buffer_object.bind()
        try:
            glEnableVertexAttribArray( position_location )
            glEnableVertexAttribArray( normal_location )
            glEnableVertexAttribArray( color_location )
            stride = 10*4
            glVertexAttribPointer(
                position_location,
                3, GL_FLOAT,False, stride, buffer_object
            )
            glVertexAttribPointer(
                normal_location,
                3, GL_FLOAT,False, stride, buffer_object+12
            )
            glVertexAttribPointer(
                color_location,
                4, GL_FLOAT,False, stride, buffer_object+24
            )
            glDrawArrays(GL_TRIANGLES, 0, buffer_size)
            #print 'buffer size: ', buffer_size

        finally:
            buffer_object.unbind()
            glDisableVertexAttribArray( position_location )
            glDisableVertexAttribArray( color_location )
    else:
        for child in thing["children"]:
            render_thing(child, position_location, normal_location, color_location, modelview_location, context_matrix)


def render_with_context(context):
    glUseProgram(context["shader"])

    # need true because our matrices are row-major and opengl wants column major by default.
    modelview = context["modelview"]
    projection = context["projection"]

    glUniformMatrix4fv(modelview["location"], 1, True, modelview["matrix"])
    glUniformMatrix4fv(projection["location"], 1, True, projection["matrix"])
    position_location = context["position_location"]
    normal_location = context["normal_location"]
    color_location = context["color_location"]

    stack = [modelview["matrix"]]
    try:
        render_thing(context["thing"], position_location, normal_location, color_location, modelview["location"], stack)
    finally:
        shaders.glUseProgram( 0 )
    #print 'out Render'
