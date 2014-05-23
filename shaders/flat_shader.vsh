#version 120
attribute vec3 position;
attribute vec3 normal;
attribute vec4 color;

varying vec4 colorVarying;

uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    // take out translational element from modelview.
    vec3 eyeNormal = mat3(modelViewMatrix) * normal;
    //light should be coming from viewer probably.
    vec3 lightVector = vec3(0.0, 0.0, 1.0);

    float nDotVP = max(0.0, dot(eyeNormal, lightVector));
    colorVarying = color * nDotVP;
    gl_Position =  projectionMatrix*modelViewMatrix *vec4(position,1.0);
}
