# ╭──────────────────────────────────────────────────────────────────────────╮
# │                    Engineering Test Report Generator                     │
# │                              Main Entry Point                            │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ FUNCTIONS:                                                               │
# │   main() -> None                                                         │
# │     Purpose: Initialize and start the MVC application                    │
# │     Inputs:  None                                                        │
# │     Outputs: None (starts GUI application)                               │
# │     Creates: Model, View, Controller instances and connects them         │
# │                                                                          │
# │ DEPENDENCIES:                                                            │
# │   - controller.Controller: Application business logic                    │
# │   - model.Model: Data management and file operations                     │
# │   - view.View: GUI interface with tkinter                                │
# │                                                                          │
# │ USAGE:                                                                   │
# │   Run this file to start the Test Report Generator application           │
# │   python main.py                                                         │
# ╰──────────────────────────────────────────────────────────────────────────╯

from controller import Controller
from model import Model
from view import View

def main() -> None:
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.run()

if __name__ == "__main__":
    main()
