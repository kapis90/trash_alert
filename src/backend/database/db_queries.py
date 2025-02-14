import os
from typing import List, Optional

from supabase import create_client, Client

from src.backend.database.model import Area, PickUpDate, Street, User


class DatabaseQueries:
    def __init__(self):
        self.client: Client = create_client(
            os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
        )

    def get_user_by_id(self, id: int) -> Optional[User]:
        if (
            response_data := self.client.table("users")
            .select("*")
            .eq("id", id)
            .execute()
            .data
        ):
            return User(**response_data[0])
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        if (
            response_data := self.client.table("users")
            .select("*")
            .eq("email", email)
            .execute()
            .data
        ):
            return User(**response_data[0])
        return None
    
    def insert_user(self, username: str, email: str) -> User:
        user = {"name": username, "email": email}
        response_data = self.client.table("users").insert(user).execute()
        return User(**response_data.data[0])

    def get_areas(self) -> List[Area]:
        if response_data := self.client.table("areas").select("*").execute().data:
            return [Area(**area) for area in response_data]
        return []

    def get_street_by_id(self, street_id: int) -> Optional[Street]:
        if (
            response_data := self.client.table("streets")
            .select("*")
            .eq("id", street_id)
            .execute()
            .data
        ):
            return Street(**response_data[0])
        return None

    def get_streets_by_area_id(self, area_id: int) -> List[Street]:
        if (
            response_data := self.client.table("streets")
            .select("*")
            .eq("area_id", area_id)
            .execute()
            .data
        ):
            return [Street(**street) for street in response_data]
        return []

    def get_pick_up_dates(self, area_id: int, type: str) -> List[PickUpDate]:
        if (
            response_data := self.client.table("pick_up_dates")
            .select("*")
            .eq("area_id", area_id)
            .eq("type", type)
            .execute()
            .data
        ):
            return [PickUpDate(**date) for date in response_data]
        return []
