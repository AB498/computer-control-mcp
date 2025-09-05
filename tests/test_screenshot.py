import sys
sys.path.append('src')
from computer_control_mcp.core import take_screenshot

# Test with save_to_downloads=False
result = take_screenshot(mode='whole_screen', save_to_downloads=False)
print('Base64 image included:', 'base64_image' in result)
print('MCP Image included:', 'image' in result)

# Test with save_to_downloads=True
result = take_screenshot(mode='whole_screen', save_to_downloads=True)
print('Base64 image included:', 'base64_image' in result)
print('MCP Image included:', 'image' in result)
print('File path included:', 'file_path' in result)
