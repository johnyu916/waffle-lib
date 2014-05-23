#version 120
attribute vec3 position;
attribute vec4 color;

varying vec4 colorVarying;

uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    colorVarying = color;
    gl_Position =  projectionMatrix*modelViewMatrix *vec4(position,1.0);
}
