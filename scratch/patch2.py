import sys

with open("backend/app/static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Undo accidental replacement
wrong_target = """html += '      <div class="slide-card-title" style="font-size: 16px;">' + slide.items[0].label + '</div>';"""
wrong_replacement = """html += '      <div class="slide-card-title">' + slide.items[0].label + '</div>';"""
content = content.replace(wrong_target, wrong_replacement)

# Do correct replacement
target = """html += '<div class="slide-info-card" style="padding: 16px; box-sizing: border-box; display: flex; flex-direction: column;">';
html += '<div class="slide-card-title" style="font-size: 16px; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1.5px solid #64748b;">' + slide.items[si].label + '</div>';"""

replacement = """html += '<div class="slide-info-card" style="padding: 16px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: center;">';
html += '<div class="slide-card-title" style="font-size: 16px;">' + slide.items[si].label + '</div>';"""

if target in content:
    content = content.replace(target, replacement)
    with open("backend/app/static/index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Target not found")
