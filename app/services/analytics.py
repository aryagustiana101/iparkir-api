import numpy as np
import pandas as pd

from app.libs.utils import read_file_data
from app.libs.constants import RESERVATIONS_FILE_DATA, SPOTS_FILE_DATA


def get_analytics():
    spots = read_file_data(SPOTS_FILE_DATA).get("records") or []
    reservations = read_file_data(RESERVATIONS_FILE_DATA).get("records") or []

    spots_df = pd.DataFrame(spots)
    reservations_df = pd.DataFrame(reservations)

    total_spots = len(spots_df)
    total_reservations = len(reservations_df)

    average_reservation_duration = 0

    if reservations_df.size > 0:
        average_reservation_duration = np.mean(
            (pd.to_datetime(reservations_df['end']) - pd.to_datetime(
                reservations_df['start'])).dt.total_seconds() / 3600
        )

    highest_price_rate_spot = None
    lowest_price_rate_spot = None

    if spots_df.size > 0:
        highest_price_rate_spot = spots_df.loc[spots_df['price_rate'].idxmax()]
        lowest_price_rate_spot = spots_df.loc[spots_df['price_rate'].idxmin()]

    return {
        "success": True,
        "data": {
            "total_spots": total_spots,
            "total_reservations": total_reservations,
            "average_reservation_duration": average_reservation_duration,
            **(
                {
                    "highest_price_rate_spot": None
                    if highest_price_rate_spot is None
                    else {
                        "id": int(highest_price_rate_spot['id']),
                        "name": highest_price_rate_spot['name'],
                        "price_rate": int(highest_price_rate_spot['price_rate']),
                    }
                }
            ),
            **(
                {
                    "lowest_price_rate_spot": None
                    if lowest_price_rate_spot is None
                    else {
                        "id": int(lowest_price_rate_spot['id']),
                        "name": lowest_price_rate_spot['name'],
                        "price_rate": int(lowest_price_rate_spot['price_rate']),
                    }
                }
            ),
        }
    }
