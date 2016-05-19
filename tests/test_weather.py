import unittest
import commands.weather as weather

class TestWeather(unittest.TestCase):
    def test_is_zip_code(self):
        self.assertFalse(weather.is_zip_code("Cincinatti"))
        self.assertTrue(weather.is_zip_code("45202"))

    def test_get_weather_name(self):
        self.assertNotEqual("", weather.get_weather_name("Cincinatti"))

    def test_get_weather_zip(self):
        self.assertNotEqual("", weather.get_weather_zip("45202"))
