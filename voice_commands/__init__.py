from .apps.clock.commands import manager
from .apps.mediaplayer.commands import player_manager
from .apps.reminders.commands import reminder, reminders_manager
from .apps.weather.commands import weather_manager
from .apps.webbrowser.commands import webbrowser_manager
from .helpers.helpers import day_to_date, parse_day_phrase
from .providers import LocationProvider
