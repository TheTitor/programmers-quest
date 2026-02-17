#version 150

uniform sampler2D background;
uniform float fade;
in vec2 v_clipTexCoord;
in float v_obliquity;
out vec4 fragColor;


void main () {
  vec4 pixel = texture(background, v_clipTexCoord * gl_FragCoord.w);

  pixel = (1.0 - v_obliquity) * vec4(1) + v_obliquity * pixel;
  fragColor = pixel * (1.0 - fade);
}
