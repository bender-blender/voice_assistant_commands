# Voice commands review (15 may 20225)

## Issues

1. Never use images to share text. Use code snippets for code or quotes for text.

## repo review

### branch name

why not master/main/develop?

https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow


### general organisation:

by modules:

mkdir /{app}/shared_models/{file per model} (including custom types, both input and output, for common use across different commands)
mkdir /{app}/helpers/{file per each domain} (auxiliary functions for common use across different commands)

mkdir /{app}/modules/{module} (for module-specific code)
+ commands.py
+ providers.py
+ models.py
+ helpers 
\* each file can be replaced with folder (python module) that contains multiple files if needed, for example, in case of many long code structures. Use a single file only for a few short items.

### gitignore

1. \__pycache__ - no "/" will fix. remove first, then ignore
2. use python gitignore template
3. pytest.ini looks important
4. проблемы.txt - место в личных заметках, а не в репе
5. downloads - ок

### main.py

SILERO_MODEL_URL, VOSK_MODEL_URL - use .env file (ignore) and add example.env

### clock/current_date

1. Data != Date
2. Don't mix layers. Response, patterns, speech-and-text models are only for commands. Commands use providers and  Providers work with programming models
3. refactor show_date method to accept optional datetime (default now) and have a computed property pretty_date
4. Use built-in utils or existing libraries for such things as much as possible. Don't re-invent the wheel, these cases were created decades ago. Formatting date is built-in os feature. Supports all locales installed in the system out of the box. Then you don't need to map all weekdays and months manually for each language.
```python
import locale
from datetime import datetime

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
print(datetime(2024, 1, 5).strftime('Сегодня %-d %B %Y года'))
```
5. Remove "today" word, because this date object can be reused in other context, for example, "reminder set for {January the 5th, 2024}"
6. Also, does TTS module handle numbers correctly? e.g. "the 5th" instead of "the fifth"
7. the line 9 docstring isn't required; don't comment obvious things that just duplicate the code
8. keep in mind later localisation

### clock/current_time
1. mostly same comments, could be the same model btw, just with different properties like .formattedDate and .formattedTime, that also can be used together for complete datetime in some command later

### clock/time_in_city

1. this is no longer a model, but an adult provider; formatting is duplicated here, while can use the current_date; instead, create a CurrentTimeProvider that receives location as a string and returns a native datetime object. In the command, it will look like.

```python
datetime_at_location: datetime = CurrentTimeProvider().get_time_at(location_str)
stark_date = Date(datetime_at_location)
response: str
if datetime_at_location.day == datetime.now().day:
	response_text = f'Current time in {location_str} is {stark_date.formatted_time}'
else:
	response_text = f'Current time in {location_str} is {stark_date.formatted_day} {stark_date.formatted_time}'
return Response(text=response_text)
```

2. code grouping by steps could be a lil better
3. Also, it worth noting that getting location by place's name can be used in multiple different commands, for example, in weather. So, it would be smart to extract it to a general (common) provider LocationProvider that can be reused in other parts of the code without duplicating the logic. Other providers will just import and use it inside their functions. OR (perhaps even better) you can completely remove location finding logic from the domain providers and make them accept ready location coordinates (geocode).

```python
geocode = LocationProvider().find(location_str) # str, I suppose
weather_at_location: WeatherInfo = WeatherProvider().get_current_weather(geocode) # or time at location
stark_weather = Weather(weather_at_location) # Maybe, to avoid confusion, we should add some prefix to our NLP-related classes, for example "ST" (after STARK, or Speach and Text) so the result will be STWeather, STDate, STNumber.
return Response(text=stark_weather.formatted)
```

4. use guard clause instead of nesting `if`s 
   https://www.youtube.com/watch?v=CFRhGnuXG-4

5.  L42: don't call same long services multiple times, use saved in ram value instead

### auxilary functions


1. `from translate import Translator # <--------- это установить!`

Use requirements.txt or even better - poetry for dependency management.

2. what is Translator?

3. `convert` is not a very descriptive name. a function must describe its purpose without comments

### Stopwatch

1. remove obvious comments
2. no need for separate reset, just do it in stop
3. separate text-speech from pure programming stopwatch implementation
	1. timer object manages only 

### Notes

1. Rename to reminders, which are temporary or recuiring TODO tasks or short reminders. "Notes" are a little different feature, that is more like a notebook of pages for consistent storage.
2. Add type annotations for all properties.
3. Replace is_\<something> with optional types. None means not set, and any other value means set
4. Separate ST layer from programming logic
5. Change approach to command context menus, aggregate all info there. Talk to the provider class only once per session, so each call is a complete CRUD transaction without intermediate states. google.com/search?q=транзакционность
   Why: abort in the middle, update info. Namespace (context) visibility.
6. 

### Timer

1. Move to clock
2. Refactor online
3. Timer is a long command (unlike reminder)
4. past check: can just check start < end
5. move date parsing to a custom type

### Media

1. again, separate layers
2. (command) volume: add int and percentage (separate) custom types with parsing 
3. (provider) volume: expect exact player-native value format, add NewType or a custom class for it e.g. PlayerVolume with int from 0 to 100
4. make self.player not optional, raise error on init if can't get it, because the class is useless without it
5. add "seek to beginning" method
6. return None instead of "неизвестно", don't include them in response. Track_name and author is enough for voice, details can be in text.

### UserRequest

1. rename to WebBrowser
2. connection check is too long, and the timeout is too big. try to google immediately and catch an exception in case of connection failure (*it's easier to ask for forgiveness than permission* principle)
3. I see you don't know when you need static or class methods. It's easy, don't use them, unless you can't use simple methods. An example of a class method is an alternative init method.
4. `import webbrowser; webbrowser.open('<url>')`
5. use "open \<sth> in broswer" command
6. also, you can add "open \$url" syntax with a custom type of "\$host:String dot $domain:Word", (host.replace(' ', '') + '.' + domain).strip().lower()
7. don't handle all `except Exception as e:`, handle only specific ones you need. some of them may have system use, some must drop the app completely, some provide useful debug info that you can't catch at runtime.

## New

###  WebSearch

1. Instead of opening a new tab, give a quick summary of the request. Also, you can use it as a fallback command. See the implementation of google, dictionary, and wiki search at old stark commands sent earlier.

