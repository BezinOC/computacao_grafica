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

# Função de Normalização Vetorial
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

# Calcula a intersecção (Se houver) entre o raio e a esfera
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

# Determina a cor de um raio lançado de ray_origin na direção ray_direction
def ray_color(ray_origin, ray_direction):
    sphere_center = np.array([0.0, 0.0, -1.0])
    sphere_radius = 0.5
    t = hit_sphere(sphere_center, sphere_radius, ray_origin, ray_direction)
    if t > 0:
        # Calcular vetor normal no ponto de interseção
        normal = normalize(ray_origin + t * ray_direction - sphere_center)
        # Converter normal para cor
        color = 0.5 * (normal + 1.0)
        return 255 * color
    # Gradiente de fundo
    unit_direction = normalize(ray_direction)
    t = 0.5 * (unit_direction[1] + 1.0)
    # Mistura linear: de azul escuro para branco
    return (1.0 - t) * np.array([0.2, 0.2, 0.3]) * 255

# Função que gera imagem
def generate_image():
    img = np.zeros((height, width, 3))
    for j in range(height):
        for i in range(width):
            u = i / (width - 1)
            v = j / (height - 1)
            ray_direction = lower_left_corner + u * horizontal + v * vertical - origin
            color = ray_color(origin, ray_direction)
            img[j, i] = color.astype(np.uint8)
    return img.astype(np.uint8)

# Função que salva imagem
def save_image(img, filename):
    Image.fromarray(img).save(filename)

if __name__ == '__main__':
    img = generate_image()
    save_image(img, 'esfera.png')
