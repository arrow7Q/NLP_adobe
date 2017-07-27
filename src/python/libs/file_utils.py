import os
def absolute_path(relPath):
  absPath = os.path.join(os.path.dirname(__file__), relPath)
  return absPath
