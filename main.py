import pygame
import math
import os
from settings import *
from ui.renderer import draw_graph, draw_animated_path
from ui.sidebar import Button
from core.graph_data import nodes, edges 
from core.algorithms import run_bfs, run_dijkstra
from core.entities import Robot, Victim

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Rescue Pathfinding")
clock = pygame.time.Clock()

# Setup Font
font_path = "assets/fonts/font.ttf"
if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 16)
    inst_font = pygame.font.Font(font_path, 18)
else:
    font = pygame.font.SysFont("Arial", 16, bold=True)
    inst_font = pygame.font.SysFont("Arial", 18, bold=True)

# Setup UI Tombol
btn_bfs = Button(150, 20, 120, 40, "Jalankan BFS", GRAY, (150, 150, 150))
btn_dijkstra = Button(300, 20, 150, 40, "Jalankan Dijkstra", GRAY, (150, 150, 150))
btn_reset = Button(480, 20, 100, 40, "Reset", (255, 100, 100), RED)

# State Management
robot_node = None
robot_entity = None
victim_nodes = []
victim_entities = {}
final_path = []

is_animating = False
anim_index = 0

# Variabel penyimpan hasil untuk ditampilkan
total_langkah = 0
total_bobot = 0

def calculate_full_path(algo_func, is_bfs=False):
    global final_path, is_animating, anim_index, robot_entity, victim_entities
    global total_langkah, total_bobot
    
    if robot_node is None or len(victim_nodes) != 3:
        return

    # Reset posisi robot dan korban untuk kalkulasi ulang
    robot_entity = Robot(nodes[robot_node])
    victim_entities.clear()
    for v_node in victim_nodes:
        victim_entities[v_node] = Victim(nodes[v_node])

    path = []
    current = robot_node
    unvisited = victim_nodes.copy()

    while unvisited:
        best_segment = []
        best_cost = float('inf')
        target_victim = None

        for v in unvisited:
            segment = algo_func(current, v)
            if not segment:
                continue
            
            if is_bfs:
                cost = len(segment) # BFS 
            else:
                cost = sum(edges[segment[i]][segment[i+1]] for i in range(len(segment)-1)) # Dijkstra

            if cost < best_cost:
                best_cost = cost
                best_segment = segment
                target_victim = v

        if not target_victim:
            print("Gagal: Ada jalur yang terputus!")
            return
        
        if path:
            path.extend(best_segment[1:])
        else:
            path.extend(best_segment)
            
        current = target_victim
        unvisited.remove(target_victim)
        
    final_path = path
    if final_path:
        is_animating = True
        anim_index = 0
        
        total_langkah = len(final_path) - 1
        total_bobot = sum(edges[final_path[i]][final_path[i+1]] for i in range(len(final_path)-1))

running = True
while running:
    screen.fill(WHITE)
    
    # 1. Gambar Komponen Dasar
    draw_graph(screen, font)
    btn_bfs.draw(screen, font)
    btn_dijkstra.draw(screen, font)
    btn_reset.draw(screen, font)
    
    # 2. Gambar Entity Korban
    for v_id, v_ent in victim_entities.items():
        v_ent.draw(screen)

    # 3. Logika Teks Petunjuk
    if robot_node is None:
        instruksi = "Petunjuk: Klik sembarang titik untuk meletakkan Robot."
    elif len(victim_nodes) < 3:
        instruksi = f"Petunjuk: Klik untuk meletakkan Korban ({len(victim_nodes)}/3)."
    elif not final_path:
        instruksi = "Petunjuk: Data lengkap! Silakan pilih algoritma di atas."
    elif is_animating:
        instruksi = "Status: Robot sedang bergerak melakukan misi penyelamatan..."
    else:
        instruksi = "Status: Misi Selesai! Semua korban berhasil dievakuasi. Klik Reset."
        
    inst_surf = inst_font.render(instruksi, True, BLACK)
    inst_rect = inst_surf.get_rect(center=(WIDTH // 2, 85))
    bg_rect = inst_rect.inflate(20, 10)
    pygame.draw.rect(screen, (255, 255, 150), bg_rect, border_radius=5)
    pygame.draw.rect(screen, BLACK, bg_rect, 1, border_radius=5)
    screen.blit(inst_surf, inst_rect)

    # 4. TAMPILKAN STATISTIK LANGKAH & BOBOT
    if final_path:
        stats_text = f"Total Langkah: {total_langkah} nodes   |   Total Bobot Jarak: {total_bobot}"
        stats_surf = inst_font.render(stats_text, True, BLUE)
        stats_rect = stats_surf.get_rect(center=(WIDTH // 2, HEIGHT - 25))
        screen.blit(stats_surf, stats_rect)

    # 5.logic Pergerakan Robot
    if is_animating and final_path and robot_entity:
        target_node = final_path[anim_index + 1]
        target_pos = nodes[target_node]
        
        reached = robot_entity.move_towards(target_pos)
        if reached:
            anim_index += 1
            if target_node in victim_entities:
                del victim_entities[target_node]
            if anim_index >= len(final_path) - 1:
                is_animating = False
                
        draw_animated_path(screen, final_path, anim_index, robot_entity.pos)

    elif final_path and not is_animating:
        draw_animated_path(screen, final_path, len(final_path)-1, robot_entity.pos)

    # 6. Gambar Entity Robot
    if robot_entity:
        robot_entity.draw(screen)

    # 7. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if not is_animating: 
            if btn_bfs.is_clicked(event):
                calculate_full_path(run_bfs, is_bfs=True)
            elif btn_dijkstra.is_clicked(event):
                calculate_full_path(run_dijkstra, is_bfs=False)
            elif btn_reset.is_clicked(event):
                robot_node = None
                robot_entity = None
                victim_nodes = []
                victim_entities = {}
                final_path = []
                total_langkah = 0
                total_bobot = 0
                
            elif event.type == pygame.MOUSEBUTTONDOWN and not final_path:
                mx, my = pygame.mouse.get_pos()
                for node, pos in nodes.items():
                    if math.hypot(mx - pos[0], my - pos[1]) <= 22:
                        if robot_node is None:
                            robot_node = node
                            robot_entity = Robot(pos)
                        elif node != robot_node and node not in victim_nodes:
                            if len(victim_nodes) < 3:
                                victim_nodes.append(node)
                                victim_entities[node] = Victim(pos)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()