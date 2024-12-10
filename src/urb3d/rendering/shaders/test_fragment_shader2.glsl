#version 430 core

uniform vec3 eye;
uniform mat4 model, view, projection;

// Input from vertex shader
in vec3 color;
in vec3 instanceScale;
in mat3 instanceRotation;
in vec3 WorldNormal;
in vec3 WorldPos;

// Output to the screen
out vec4 outColor;

// vec3 closestEllipsoidIntersection(vec3 rayDirection, out vec3 normal) {
//   // Convert ray to ellipsoid space
//   dvec3 localRayOrigin = (eye - WorldPos) * instanceRotation;
//   dvec3 localRayDirection = normalize(rayDirection * instanceRotation);

//   dvec3 oneover = double(1) / dvec3(instanceScale);

//   // Compute coefficients of quadratic equation
//   double a = dot(localRayDirection * oneover, localRayDirection * oneover);
//   double b = 2.0 * dot(localRayDirection * oneover, localRayOrigin * oneover);
//   double c = dot(localRayOrigin * oneover, localRayOrigin * oneover) - 1.0;

//   // Compute discriminant
//   double discriminant = b * b - 4.0 * a * c;

//   // If discriminant is negative, there is no intersection
//   if (discriminant < 0.0) {
//     return vec3(0.0);
//   }

//   // Compute two possible solutions for t
//   float t1 = float((-b - sqrt(discriminant)) / (2.0 * a));
//   float t2 = float((-b + sqrt(discriminant)) / (2.0 * a));

//   // Take the smaller positive solution as the closest intersection
//   float t = min(t1, t2);

//   // Compute intersection point in ellipsoid space
//   vec3 localIntersection = vec3(localRayOrigin + t * localRayDirection);

//   // Compute normal vector in ellipsoid space
//   vec3 localNormal = normalize(localIntersection / instanceScale);

//   // Convert normal vector to world space
//   normal = normalize(instanceRotation * localNormal);

//   // Convert intersection point back to world space
//   vec3 intersection = instanceRotation * localIntersection + WorldPos;

//   return intersection;
// }

void main()
{
  //   if (WorldPos == vec3(0.0)) {
  //       discard;
  //   }

	// vec3 dir = normalize(WorldPos - eye);

	// vec3 normal;
	// vec3 intersection = closestEllipsoidIntersection(dir, normal);
	// float align = max(0.4, dot(-dir, normal));

	// outColor = vec4(1, 0, 0, 1);

	// if(intersection == vec3(0))
	// 	discard;

	// vec4 newPos = MVP * vec4(intersection, 1);
	// newPos /= newPos.w;

	// gl_FragDepth = newPos.z;

	// float a = 1.0;
  // outColor = vec4(align * color, a);
  outColor = vec4(color, a);
}