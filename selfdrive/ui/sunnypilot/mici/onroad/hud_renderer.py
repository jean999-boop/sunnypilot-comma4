"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""
import pyray as rl

from openpilot.selfdrive.ui.mici.onroad.hud_renderer import HudRenderer
from openpilot.selfdrive.ui.sunnypilot.onroad.blind_spot_indicators import BlindSpotIndicators
from openpilot.selfdrive.ui.ui_state import ui_state


class HudRendererSP(HudRenderer):
  def __init__(self):
    super().__init__()
    self.blind_spot_indicators = BlindSpotIndicators()
    self._scroll_offset_x = 0.0

  def _update_state(self) -> None:
    super()._update_state()
    self.blind_spot_indicators.update()

  def _render(self, rect: rl.Rectangle) -> None:
    super()._render(rect)
    self.blind_spot_indicators.render(rect)
    self._render_custom_park_marquee(rect)

  def _render_custom_park_marquee(self, rect: rl.Rectangle) -> None:
    if ui_state.sm.valid.get('carState', False):
      car_state = ui_state.sm['carState']
      gear = getattr(car_state, 'gearShifter', '')
      
      # CUSTOM BRAND DISPLAY (PARK ONLY)
      if str(gear).lower() == 'park':
        text_string = "sunnypilotboop"
        font_size = 24  # Adjusted cleanly for the compact comma 4 display

        font_bold = getattr(ui_state, 'font_bold', rl.get_font_default())
        text_size = rl.measure_text_ex(font_bold, text_string, font_size, 0)

        self._scroll_offset_x += 1.8
        if self._scroll_offset_x > (rect.width + text_size.x):
          self._scroll_offset_x = 0.0

        draw_x = rect.x + rect.width - self._scroll_offset_x
        draw_y = rect.y + 40

        rl.draw_text_ex(
          font_bold,
          text_string,
          rl.Vector2(draw_x, draw_y),
          font_size,
          0,
          rl.Color(255, 255, 255, 180),
        )
      else:
        self._scroll_offset_x = 0.0

  def _has_blind_spot_detected(self) -> bool:
    return self.blind_spot_indicators.detected
