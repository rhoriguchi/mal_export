import enum


class ExportType(enum.Enum):
    ANIME = 1
    MANGA = 2

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)
