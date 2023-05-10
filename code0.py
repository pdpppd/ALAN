
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# draw a yellow circle for the face
face_circle = plt.Circle((0, 0), radius=1, color='yellow')
ax.add_artist(face_circle)

# draw black circles for the eyes
left_eye = plt.Circle((-0.3, 0.4), radius=0.1, color='black')
right_eye = plt.Circle((0.3, 0.4), radius=0.1, color='black')
ax.add_artist(left_eye)
ax.add_artist(right_eye)

# draw a red smiley mouth using Arc
smiling_mouth = plt.Arc((0, -0.3), width=0.6, height=0.3, theta1=0, theta2=180, color='red')
ax.add_artist(smiling_mouth)

ax.set_aspect('equal')
plt.show()
