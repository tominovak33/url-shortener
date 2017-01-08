
import os
import sys

# explicitly add lib to sys.path, so that libraries in lib can reference other
# libraries in lib without needing the lib. prefix
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir)
