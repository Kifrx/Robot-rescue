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

# FONT
font_path = "assets/fonts/font.ttf"
if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 16)
    inst_font = pygame.font.Font(font_path, 18)
else:
    font = pygame.font.SysFont("Arial", 16, bold=True)
    inst_font = pygame.font.SysFont("Arial", 18, bold=True)

# BUTTON
btn_bfs = Button(150, 20, 120, 40, "Jalankan BFS", GRAY, (150, 150, 150))
btn_dijkstra = Button(300, 20, 150, 40, "Jalankan Dijkstra", GRAY, (150, 150, 150))
btn_reset = Button(480, 20, 100, 40, "Reset", (255, 100, 100), RED)

# STATE
robot_node = None
robot_entity = None
victim_nodes = []
victim_entities = {}
final_path = []

is_animating = False
anim_index = 0

total_langkah = 0
total_bobot = 0

blocked_nodes = set()

# PATH CALCULATION
def calculate_full_path(algo_func, is_bfs=False):
    global final_path, is_animating, anim_index
    global robot_entity, victim_entities
    global total_langkah, total_bobot

    if robot_node is None or len(victim_nodes) != 3:
        return

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
            segment = algo_func(current, v, blocked_nodes)

            if not segment:
                continue

            if is_bfs:
                cost = len(segment)
            else:
                cost = sum(edges[segment[i]][segment[i+1]] for i in range(len(segment)-1))

            if cost < best_cost:
                best_cost = cost
                best_segment = segment
                target_victim = v

        if target_victim is None:
            print("Gagal: Ada jalur terputus!")
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

# MAIN LOOP
running = True
while running:
    screen.fill(WHITE)

    # DRAW
    draw_graph(screen, font, blocked_nodes)
    btn_bfs.draw(screen, font)
    btn_dijkstra.draw(screen, font)
    btn_reset.draw(screen, font)

    # DRAW VICTIMS
    for v in victim_entities.values():
        v.draw(screen)

    # TEXT INFO
    if robot_node is None:
        instruksi = "Klik node untuk meletakkan Robot"
    elif len(victim_nodes) < 3:
        instruksi = f"Pilih Korban ({len(victim_nodes)}/3)"
    elif not final_path:
        instruksi = "Pilih algoritma"
    elif is_animating:
        instruksi = "Robot sedang bergerak..."
    else:
        instruksi = "Selesai! Klik Reset"

    text = inst_font.render(instruksi, True, BLACK)
    screen.blit(text, (WIDTH // 2 - 150, 80))

    # STATS
    if final_path:
        stats = f"Langkah: {total_langkah} | Bobot: {total_bobot}"
        stats_text = inst_font.render(stats, True, BLUE)
        screen.blit(stats_text, (WIDTH // 2 - 120, HEIGHT - 30))

    # ANIMATION
    if is_animating and final_path and robot_entity:
        target = final_path[anim_index + 1]
        target_pos = nodes[target]

        if robot_entity.move_towards(target_pos):
            anim_index += 1

            if target in victim_entities:
                del victim_entities[target]

            if anim_index >= len(final_path) - 1:
                is_animating = False

        draw_animated_path(screen, final_path, anim_index, robot_entity.pos)

    elif final_path:
        draw_animated_path(screen, final_path, len(final_path)-1, robot_entity.pos)

    # DRAW ROBOT
    if robot_entity:
        robot_entity.draw(screen)

    # EVENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not is_animating:

            if btn_bfs.is_clicked(event):
                calculate_full_path(run_bfs, True)

            elif btn_dijkstra.is_clicked(event):
                calculate_full_path(run_dijkstra, False)

            elif btn_reset.is_clicked(event):
                robot_node = None
                robot_entity = None
                victim_nodes.clear()
                victim_entities.clear()
                final_path = []
                blocked_nodes.clear()
                total_langkah = 0
                total_bobot = 0

            elif event.type == pygame.MOUSEBUTTONDOWN and not final_path:
                mx, my = pygame.mouse.get_pos()

                for node, pos in nodes.items():
                    if math.hypot(mx - pos[0], my - pos[1]) <= 22:

                        # RIGHT CLICK → BLOCK
                        if event.button == 3:
                            if node in blocked_nodes:
                                blocked_nodes.remove(node)
                            elif node != robot_node and node not in victim_nodes:
                                blocked_nodes.add(node)

                        # LEFT CLICK → SELECT
                        elif event.button == 1:

                            if node in blocked_nodes:
                                continue

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
