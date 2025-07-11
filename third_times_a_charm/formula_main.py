# ╭──────────────────────────────────────────────────────────────────────────╮
# │                    Engineering Test Report Generator                     │
# │                              Main Entry Point                            │
# │                         WITH FORMULA EDITOR SUPPORT                      │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ FUNCTIONS:                                                               │
# │   main() -> None                                                         │
# │     Purpose: Initialize and start the MVC application                    │
# │     Inputs:  None                                                        │
# │     Outputs: None (starts GUI application)                               │
# │     Creates: Model, View, Controller instances and connects them         │
# │                                                                          │
# │ DEPENDENCIES:                                                            │
# │   - formula_controller.Controller: Application business logic            │
# │   - formula_model.Model: Data management and file operations             │
# │   - formula_view.View: GUI interface with tkinter                        │
# │                                                                          │
# │ USAGE:                                                                   │
# │   Run this file to start the Test Report Generator application           │
# │   python formula_main.py                                                 │
# ╰──────────────────────────────────────────────────────────────────────────╯

from formula_controller import FormulaController
from formula_model import FormulaModel
from formula_view import FormulaView

def main() -> None:
    model = FormulaModel()
    view = FormulaView()
    controller = FormulaController(model, view)
    controller.run()

if __name__ == "__main__":
    main()
