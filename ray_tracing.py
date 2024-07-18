
import numpy as np
from PIL import Image

# Dimensões da Imagem
width = 400
height = 300

# Configurações Básicas
aspect_ratio = width / height
viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1.0

origin = np.array([0.0, 0.0, 0.0])
horizontal = np.array([viewport_width, 0.0, 0.0])
vertical = np.array([0.0, viewport_height, 0.0])
lower_left_corner = origin - horizontal / 2 - vertical / 2 - np.array([0.0, 0.0, focal_length])

# Raio e Centro da Esfera
sphere_center = np.array([0.0, 0.0, -1.0])
sphere_radius = 0.5

# Função de Normalização Vetorial
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

# Determina o ponto de intersecção (se existir) do Raio com origem em ray_origin e com direção ray_direction intersecta a esfera 
def hit_sphere(center, radius, ray_origin, ray_direction):
    oc = ray_origin - center
    a = np.dot(ray_direction, ray_direction)
    b = 2.0 * np.dot(oc, ray_direction)
    c = np.dot(oc, oc) - radius * radius
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return -1.0
    else:
        return (-b - np.sqrt(discriminant)) / (2.0 * a)

# Função que implementa o modelo de iluminação
def phong_lighting(ray_origin, ray_direction, t, normal):
    ambient_color = np.array([0.1, 0.1, 0.1])  # Ambient color
    diffuse_color = np.array([1.0, 0.5, 0.0])  # Diffuse color (orange)
    specular_color = np.array([1.0, 1.0, 1.0])  # Specular color (white)
    light_position = np.array([2.0, 2.0, 1.0])  # Position of the light source
    light_color = np.array([1.0, 1.0, 1.0])  # Light color
    
    ambient = ambient_color * diffuse_color
    
    light_direction = normalize(light_position - (ray_origin + t * ray_direction))
    diffuse_intensity = np.dot(normal, light_direction)
    diffuse = np.clip(diffuse_intensity, 0, 1) * diffuse_color * light_color
    
    view_direction = normalize(-ray_direction)
    reflection_direction = normalize(2 * np.dot(light_direction, normal) * normal - light_direction)
    specular_intensity = np.dot(view_direction, reflection_direction) ** 32
    specular = np.clip(specular_intensity, 0, 1) * specular_color * light_color
    
    lighting = ambient + diffuse + specular
    
    return np.clip(lighting, 0, 1)

def ray_color(ray_origin, ray_direction):
    t = hit_sphere(sphere_center, sphere_radius, ray_origin, ray_direction)
    if t > 0:
        hit_point = ray_origin + t * ray_direction
        normal = normalize(hit_point - sphere_center)
        color = phong_lighting(ray_origin, ray_direction, t, normal)
        return (color * 255).astype(np.uint8)
    unit_direction = normalize(ray_direction)
    t = 0.5 * (unit_direction[1] + 1.0)
    background_color = (1.0 - t) * np.array([0.2, 0.2, 0.3])
    return (background_color * 255).astype(np.uint8)

# Função que Gera a Imagem
def generate_image():
    img = np.zeros((height, width, 3), dtype=np.uint8)
    for j in range(height):
        for i in range(width):
            u = i / (width - 1)
            v = j / (height - 1)
            ray_direction = lower_left_corner + u * horizontal + v * vertical - origin
            color = ray_color(origin, ray_direction)
            img[j, i] = color
    return img

# Função que salva a Imagem
def save_image(img, filename):
    Image.fromarray(img).save(filename)

if __name__ == '__main__':
    img = generate_image()
    save_image(img, 'esfera.png')
