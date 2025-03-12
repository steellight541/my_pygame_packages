from .scene import WindowScene


class WindowSceneHandler:
    scenes: dict[str, WindowScene]
    def __init__(self):
        self.scenes = {}

    def add_scene(self, scene: WindowScene):
        if scene.name in self.scenes: raise ValueError(f"Scene with name '{scene.name}' already exists")
        self.scenes[scene.name] = scene

    def get_scene(self, name: str) -> WindowScene:
        return self.scenes[name]
    
    def remove_scene(self, name: str):
        if name not in self.scenes: raise ValueError(f"Scene with name '{name}' does not exist")
        del self.scenes[name]
