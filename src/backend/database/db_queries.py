import os
from typing import List

# from dotenv import load_dotenv
from supabase import create_client, Client

from src.backend.database.model import Area, PickUpDate, Street, User


class DatabaseQueries:
    def __init__(self):
        self.client: Client = create_client(
            os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
        )

    def get_user_by_name(self, name: str) -> User:
        return User(
            **self.client.table("users").select("*").eq("name", name).execute().data[0]
        )
    
    def get_areas(self) -> List[Area]:
        return [
            Area(**area)
            for area in self.client.table("areas").select("*").execute().data
        ]

    def get_street_by_id(self, street_id: int) -> Street:
        return Street(
            **self.client.table("streets")
            .select("*")
            .eq("id", street_id)
            .execute()
            .data[0]
        )
    
    def get_streets_by_area_id(self, area_id: int) -> List[Street]:
        return [
            Street(**street)
            for street in self.client.table("streets")
            .select("*")
            .eq("area_id", area_id)
            .execute()
            .data
        ]

    def get_pick_up_dates(self, area_id: int, type: str) -> List[PickUpDate]:
        pick_up_dates_raw = (
            self.client.table("pick_up_dates")
            .select("*")
            .eq("area_id", area_id)
            .eq("type", type)
            .execute()
            .data
        )
        return [PickUpDate(**date) for date in pick_up_dates_raw]


# load_dotenv()
# db_queries = DatabaseQueries()
# user = db_queries.get_user_by_name("kajetan")
# street_id = db_queries.get_user_by_name("kajetan").street_id
# street = db_queries.get_street_by_id(street_id)
# area_id = db_queries.get_street_by_id(street_id).area_id
# dates = db_queries.get_pick_up_dates(area_id, "Zmieszane")

# pass
