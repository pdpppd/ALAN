
import matplotlib.pyplot as plt

# Create a figure and axis
fig, ax = plt.subplots()

# Draw a circle for the face
face = plt.Circle((0, 0), radius=1, edgecolor='black', facecolor='yellow')
ax.add_patch(face)

# Draw the eyes
left_eye = plt.Circle((-0.35, 0.35), radius=0.2, color='black')
ax.add_patch(left_eye)
right_eye = plt.Circle((0.35, 0.35), radius=0.2, color='black')
ax.add_patch(right_eye)

# Draw a semi-circle for the mouth
mouth = plt.arc((0, -0.3), 1.2, 1.2, theta1=30, theta2=150, color='black')
ax.add_patch(mouth)

# Set the x and y-axis limits and remove the ticks
ax.set_xlim([-1.5, 1.5])
ax.set_ylim([-1.5, 1.5])
ax.set_xticks([])
ax.set_yticks([])

# Show the plot
plt.show()
