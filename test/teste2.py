# pip install textual rich
from textual.app import App, ComposeResult
from textual.widgets import SelectionList
from textual import events

class MenuApp(App):
    CSS_PATH = None  # sem CSS externo

    def compose(self) -> ComposeResult:
        # (label, value)
        yield SelectionList(
            ("Laranja", "laranja"),
            ("Maçã",    "maca"),
            ("Banana",  "banana"),
            ("Sair",    "sair"),
        )

    def on_selection_list_selected(
        self, event: SelectionList.selected
    ) -> None:
        escolha = event.value
        if escolha == "sair":
            self.exit()
        else:
            self.console.print(f"Você escolheu: {escolha!r}")

if __name__ == "__main__":
    MenuApp().run()
