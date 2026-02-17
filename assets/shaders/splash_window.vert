#version 150

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat3 p3d_NormalMatrix;
in vec4 p3d_Vertex;
in vec3 p3d_Normal;

out vec2 v_clipTexCoord;
out float v_obliquity; // 0 = camera-coplanar
const float pi = 3.14159265359;



void main()  {
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  v_clipTexCoord = 0.5 * gl_Position.xy + vec2(0.5 * gl_Position.w);
  v_obliquity = acos(
    dot(
      normalize(p3d_NormalMatrix * p3d_Normal),
      vec3(0, 1, 0)
    )
  ) / (pi / 2.0);
}
