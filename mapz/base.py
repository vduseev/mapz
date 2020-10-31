class BaseMapz(dict):
    def __repr__(self) -> str:
        return f"MapZ{dict.__repr__(self)}"
