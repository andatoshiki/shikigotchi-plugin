from shikigotchi.ui.components import LabeledValue
from shikigotchi.ui.view import BLACK
import shikigotchi.ui.fonts as fonts
import shikigotchi.plugins as plugins
import shikigotchi
import logging
import datetime
import os
import toml
import yaml


class ShikiClock(plugins.Plugin):
    __author__ = 'https://github.com/LoganMD'
    __version__ = '1.0.2'
    __license__ = 'GPL3'
    __description__ = 'Clock/Calendar for shikigotchi'

    def on_loaded(self):
        if 'date_format' in self.options:
            self.date_format = self.options['date_format']
        else:
            self.date_format = "%m/%d/%y"

        logging.info("shikigotchi Clock Plugin loaded.")

    def on_ui_setup(self, ui):
        memenable = False
        config_is_toml = True if os.path.exists(
            '/etc/shikigotchi/config.toml') else False
        config_path = '/etc/shikigotchi/config.toml' if config_is_toml else '/etc/shikigotchi/config.yml'
        with open(config_path) as f:
            data = toml.load(f) if config_is_toml else yaml.load(
                f, Loader=yaml.FullLoader)

            if 'memtemp' in data["main"]["plugins"]:
                if 'enabled' in data["main"]["plugins"]["memtemp"]:
                    if data["main"]["plugins"]["memtemp"]["enabled"]:
                        memenable = True
                        logging.info(
                            "shikigotchi Clock Plugin: memtemp is enabled")
        if ui.is_waveshare_v2():
            pos = (130, 80) if memenable else (200, 80)
            ui.add_element('clock', LabeledValue(color=BLACK, label='', value='-/-/-\n-:--',
                                                 position=pos,
                                                 label_font=fonts.Small, text_font=fonts.Small))

    def on_ui_update(self, ui):
        now = datetime.datetime.now()
        time_rn = now.strftime(self.date_format + "\n%I:%M %p")
        ui.set('clock', time_rn)
