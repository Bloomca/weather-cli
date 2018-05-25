## Weather CLI

This is an application to get weather for a city.
Application lets you to choose all available options (there are several Saint-Petersburgs, for example).

I've built this application to check weather in cities where I want to go – just to check what should I pack and expect from the trip, so I've glued two APIs together, bing maps geocoding for intelligent guess of location and darksky API to get an actual forecast.
They both are free until certain limit, and for your personal it should be more than enough.

![Example](./example.gif)

## Run

In order to run this program, you need to provide your [bing maps key](https://www.bingmapsportal.com/) and [darksky api key](https://darksky.net/dev).

This program is written using Python@3.6.5.

```sh
pip install -r requirements.txt
export BING_KEY=xxxxxxx
export DARKSKY_KEY=xxxxx
python run.py
```

## License

MIT