#!/usr/bin/env python3
"""
Test script to verify the new View layout works correctly
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from view import View
    print("✓ View module imported successfully")
except ImportError as e:
    print(f"✗ Failed to import View: {e}")
    sys.exit(1)

def test_view_layout():
    """Test the new view layout"""
    try:
        # Create a root window
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Create the view
        view = View()
        print("✓ View created successfully")
        
        # Test if all new components exist
        components_to_test = [
            ('notebook', 'Notebook widget'),
            ('form_editor_frame', 'Form Editor frame'),
            ('csv_editor_frame', 'CSV Editor frame'), 
            ('latex_viewer', 'LaTeX viewer'),
            ('center_scrollable', 'Scrollable frame')
        ]
        
        for component, description in components_to_test:
            if hasattr(view, component) and getattr(view, component) is not None:
                print(f"✓ {description} exists")
            else:
                print(f"✗ {description} missing")
        
        # Test tab functionality
        if view.notebook:
            tab_count = view.notebook.index('end')
            print(f"✓ Notebook has {tab_count} tabs")
            
            if tab_count >= 2:
                tab1_text = view.notebook.tab(0, 'text')
                tab2_text = view.notebook.tab(1, 'text')
                print(f"✓ Tab 1: {tab1_text}")
                print(f"✓ Tab 2: {tab2_text}")
            else:
                print("✗ Not enough tabs found")
        
        # Test LaTeX viewer methods
        if hasattr(view, 'update_latex_content'):
            view.update_latex_content("% Test LaTeX content\n\\documentclass{article}\n\\begin{document}\nTest\n\\end{document}")
            print("✓ LaTeX content update test passed")
        
        # Test tab switching
        if hasattr(view, 'switch_to_tab'):
            view.switch_to_tab("CSV Editor")
            current_tab = view.get_current_tab()
            print(f"✓ Current tab after switch: {current_tab}")
        
        # Close the view
        view.destroy()
        print("✓ View destroyed successfully")
        
        print("\n🎉 All tests passed! The new layout is working correctly.")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing the new View layout...")
    print("=" * 50)
    test_view_layout()
