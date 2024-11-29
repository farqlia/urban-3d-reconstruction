#version 430 core

in vec3 position;
in vec3 ellipsoidCenter;
in vec3 ellipsoidScale;
in float ellipsoidAlpha;
in mat3 ellipsoidRot;
in vec3 color;

uniform vec3 eye;

uniform mat4 model, view, projection;

out vec4 outColor;

vec3 sphereIntersect(vec3 c, vec3 ro, vec3 p, out vec3 normal) {
    mat3 sphereRotationT = transpose(ellipsoidRot);

    vec3 rd = vec3(sphereRotationT * normalize(p - ro)) / vec3(ellipsoidScale);
    vec3 u = (sphereRotationT * vec3(ro - c)) / vec3(ellipsoidScale); // ro relative to c

    float a = dot(rd, rd);
    float b = 2.0 * dot(u, rd);
    float cc = dot(u, u) - 1.0;

    float discriminant = b * b - 4 * a * cc;

    // no intersection
    if (discriminant < 0.0) {
        return vec3(0.0);
    }

    float t1 = (-b + sqrt(discriminant)) / (2.0 * a);
    float t2 = (-b - sqrt(discriminant)) / (2.0 * a);
    float t = min(t1, t2);
    vec3 intersection = ro + ellipsoidRot * (vec3(t * rd) * ellipsoidScale);
    vec3 localIntersection = ((mat3(sphereRotationT) * (intersection - c)) / ellipsoidScale);

    normal = ellipsoidRot * localIntersection;
    return intersection;
}

void main() {
    vec3 normal = vec3(0.0);

    vec3 intersection = sphereIntersect(ellipsoidCenter, eye, position, normal);

    if (intersection == vec3(0.0)) {
        discard;
    }

    vec3 rd = normalize(eye - intersection);
    float align = max(dot(rd, normal), 0.1);

    vec4 newPos = projection * view * model * vec4(intersection, 1.0);
    newPos /= newPos.w;
    gl_FragDepth = newPos.z;

    // Lightly shade it by making it darker around the scraping angles.
    outColor = vec4(align * color, 1.0);
}
