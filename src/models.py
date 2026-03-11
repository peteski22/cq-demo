"""Data models for API responses."""

from pydantic import BaseModel


class Item(BaseModel):
    """An item returned by the API."""

    id: int
    name: str
    tags: list[str] = []
    created_at: str
    updated_at: str | None = None

    def age_days(self) -> int:
        """Return the age of the item in days."""
        from datetime import datetime, timezone

        created = datetime.fromisoformat(self.created_at)
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return (now - created).days
