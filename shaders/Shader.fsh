//
//  Shader.fsh
//  OpenGLTemplate
//
//  Created by John Kim on 12/6/11.
//  Copyright (c) 2011 __MyCompanyName__. All rights reserved.
//
#version 120
varying vec4 colorVarying;

void main()
{
    gl_FragColor = colorVarying;
}
