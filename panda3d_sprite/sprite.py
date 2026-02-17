from panda3d import core as p3d
from direct.showbase import ShowBaseGlobal


class Sprite2D:
    def __init__(self, file_path: str, rows: int = 1, cols: int = 1):
        self.rows = max(1, int(rows))
        self.cols = max(1, int(cols))
        self.animations = {}
        self._animation_name = None
        self._animation_frames = []
        self._animation_loop = False
        self._animation_index = 0
        self._frame_time = 1.0 / 12.0
        self._elapsed = 0.0

        self.node = p3d.NodePath("Sprite2D")
        card = p3d.CardMaker("sprite-card")
        card.set_frame(-0.5, 0.5, 0.0, 1.0)
        self._card_np = self.node.attach_new_node(card.generate())
        self._card_np.set_two_sided(True)
        self._card_np.set_transparency(p3d.TransparencyAttrib.M_alpha)

        texture = p3d.TexturePool.load_texture(file_path)
        if texture is not None:
            self._card_np.set_texture(texture, 1)

        self._texture_stage = p3d.TextureStage.get_default()
        self._card_np.set_tex_scale(self._texture_stage, 1.0 / self.cols, 1.0 / self.rows)
        self._apply_frame(0)

        base = getattr(ShowBaseGlobal, "base", None)
        if base is not None:
            base.taskMgr.add(self._tick, f"sprite2d_tick_{id(self)}")

    def create_animation(self, key: str, frames):
        self.animations[key] = list(frames or [])

    def play_animation(self, key: str, loop: bool = False):
        frames = self.animations.get(key, [])
        if not frames:
            return

        self._animation_name = key
        self._animation_frames = frames
        self._animation_loop = loop
        self._animation_index = 0
        self._elapsed = 0.0
        self._apply_frame(frames[0])

    def flip_x(self, enabled: bool):
        scale = self.node.get_scale()
        sx = -abs(scale.x) if enabled else abs(scale.x)
        self.node.set_scale(sx, scale.y, scale.z)

    def _apply_frame(self, frame: int):
        frame = max(0, int(frame))
        col = frame % self.cols
        row = frame // self.cols
        if row >= self.rows:
            row = self.rows - 1

        u = float(col) / float(self.cols)
        v = 1.0 - float(row + 1) / float(self.rows)
        self._card_np.set_tex_offset(self._texture_stage, u, v)

    def _tick(self, task):
        if not self._animation_frames:
            return task.cont

        dt = getattr(ShowBaseGlobal.globalClock, "dt", 0.0)
        self._elapsed += dt
        if self._elapsed < self._frame_time:
            return task.cont

        self._elapsed = 0.0
        self._animation_index += 1
        if self._animation_index >= len(self._animation_frames):
            if self._animation_loop:
                self._animation_index = 0
            else:
                self._animation_index = len(self._animation_frames) - 1

        self._apply_frame(self._animation_frames[self._animation_index])
        return task.cont
