#version 120
attribute vec3 position;
//attribute vec3 normal;
attribute vec4 color;

varying vec4 colorVarying;

uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;

void main()
{
    //vec3 eyeNormal = vec3(modelViewMatrix * vec4(normal,0.0));
    //vec3 lightPosition = vec3(0.0, 0.0, 1.0);
    //vec4 diffuseColor = vec4(1, 1, 1, 1.0);

    //float nDotVP = max(0.0, dot(eyeNormal, normalize(lightPosition)));
    //colorVarying = (diffuseColor  color) * nDotVP;
    //colorVarying = color * nDotVP;
    //colorVarying = diffuseColor color;
    //colorVarying = vec4(color,1.0);
    colorVarying = color;
    //gl_Position =  modelViewMatrix *projectionMatrix*  vec4(position,1.0);
    gl_Position =  projectionMatrix*modelViewMatrix *vec4(position,1.0);
    //gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
}
