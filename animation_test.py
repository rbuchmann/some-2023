from manim import *

class Plot3DFunction(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        self.play(Create(axes))
        
        # Test function
        def func(x, y, t):
            return np.sin(np.sqrt(x**2 + y**2 + t))
        
        surface = Surface(
            lambda u, v: np.array([
                u,
                v,
                func(u, v, 0)  # Evaluate the function at time t = 0
            ]),
            resolution=(20, 20),
            u_range=(-5, 5),
            v_range=(-5, 5)
        )
        
        # Update the surface plot over time
        self.play(Create(surface))
        self.wait()
        
        for t in np.linspace(0, 2 * PI, 100):
            self.update_surface(surface, func, t)
            self.wait(0.05)
    
    def update_surface(self, surface, func, t):
        u_values = surface.u_range
        v_values = surface.v_range
        surface.mesh = [
            [
                surface.func(u, v) for v in np.linspace(v_values[0], v_values[1], surface.resolution[1])
            ]
            for u in np.linspace(u_values[0], u_values[1], surface.resolution[0])
        ]
        surface.become(surface)
        
        # Update the z-coordinate of each point on the surface based on the current time
        for u_index in range(surface.resolution[0]):
            for v_index in range(surface.resolution[1]):
                u = interpolate(u_values[0], u_values[1], u_index / surface.resolution[0])
                v = interpolate(v_values[0], v_values[1], v_index / surface.resolution[1])
                z = func(u, v, t)
                surface.mesh[u_index][v_index][2] = z

