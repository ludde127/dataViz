from entsoe import EntsoePandasClient
from secret.secret import ENTSOE_API_KEY
import pandas as pd
from datetime import timedelta
from pytz import timezone


# Collect electricity price data for the rest of the day
# https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show?name=&defaultValue=true&viewType=GRAPH&areaType=BZN&atch=false&dateTime.dateTime=13.08.2022+00:00|CET|DAY&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)&biddingZone.values=CTY|10YSE-1--------K!BZN|10Y1001A1001A47J&resolution.values=PT60M
# Using this lib https://github.com/EnergieID/entsoe-py


class Prices:
    def __init__(self, tz="Europe/Stockholm"):
        self.client = EntsoePandasClient(api_key=ENTSOE_API_KEY)
        self.__tz = timezone(zone=tz)

    def next24hours(self, price_zone="SE_4"):
        start = pd.Timestamp.today(tz=self.__tz)
        end = start + timedelta(days=1)
        return pd.DataFrame(self.client.query_day_ahead_prices(price_zone, start=start, end=end), columns=["prices"])

    def sorted_rolling(self, window_size, zone="SE_4"):
        return self.next24hours(zone).rolling(window_size).mean().sort_values(by="prices")
