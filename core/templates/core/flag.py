import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch

fig, ax = plt.subplots()

# Rectangles for saffron, white, green
ax.add_patch(patch.Rectangle((0, 5), 9, 2, facecolor='#FF9933', edgecolor='grey'))
ax.add_patch(patch.Rectangle((0, 3), 9, 2, facecolor='#FFFFFF', edgecolor='grey'))
ax.add_patch(patch.Rectangle((0, 1), 9, 2, facecolor='#138808', edgecolor='grey'))

# Ashoka Chakra
center_x, center_y = 4.5, 4
radius = 0.8
chakra = plt.Circle((center_x, center_y), radius, color='#000080', fill=False, linewidth=2)
ax.add_artist(chakra)
hub = plt.Circle((center_x, center_y), radius*0.08, color='#000080')
ax.add_artist(hub)

# 24 spokes
for i in range(24):
    angle = 2 * np.pi * i / 24
    x_outer = center_x + radius * np.cos(angle)
    y_outer = center_y + radius * np.sin(angle)
    ax.plot([center_x, x_outer], [center_y, y_outer], color='#000080', linewidth=1)

ax.set_aspect('equal')
ax.axis('off')

# Save to file
plt.savefig("indian_flag.png", dpi=300, bbox_inches='tight')
plt.show()
