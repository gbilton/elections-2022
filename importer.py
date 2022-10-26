import pandas as pd


from db import get_database


class StatesImporter:
    def import_states(self) -> None:
        """Imports a list of brazilian state from the internet to the database."""
        states = self._get_states()
        self._save_states(states)

    def _get_states(self) -> list[str]:
        """Gets a list of all brazilian states.

        Returns:
            list[str]: A list of all brazilian states.
        """
        URL = (
            "https://www.oobj.com.br/bc/article/quais-os-c%C3%B3digos-de-cada-uf-no-brasil-465.html"
        )
        dfs = pd.read_html(URL)
        states = sorted(dfs[0]["UF"].to_list())
        return states

    def _save_states(self, states: list[str]) -> None:
        """Saves all states to database.

        Args:
            states (list[str]): list of all brazilian states
        """
        db = get_database()
        db["states"].insert_one({"states": states})


if __name__ == "__main__":
    importer = StatesImporter()
    importer.import_states()
