import sys

with open("backend/app/static/index.html", "r", encoding="utf-8") as f:
    content = f.read()

target = """} else {
// Eski tek kolonlu düz metin düzeni
var cardStyle = slide.transparentCard === true ? 'background: transparent; border: none; box-shadow: none; padding: 0;' : '';
html += '<div class="slide-info-card" style="' + cardStyle + '">';
if (slide.items && slide.items.length) {
html += '  <div class="slide-card-content">';
for (var si = 0; si < slide.items.length; si++) {
if (si > 0) html += '<div style="border-top: 1px solid #e2e8f0; margin: 16px 0;"></div>';
html += '<div style="margin-bottom: 4px; font-size: 15px; font-weight: 700; color: #1a1a1a;">' + slide.items[si].label + '</div>';
html += '<div>' + slide.items[si].text + '</div>';
}
html += '  </div>';
} else if (slide.value) {
html += '  <div class="slide-card-content">' + slide.value + '</div>';
}
html += '</div>';
}"""

replacement = """} else {
// Eski tek kolonlu veya yeni çoklu kolon düz metin düzeni
var cardStyle = slide.transparentCard === true ? 'background: transparent; border: none; box-shadow: none; padding: 0;' : '';

if (slide.items && slide.items.length >= 2 && !slide.transparentCard) {
    html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px;">';
    for (var si = 0; si < slide.items.length; si++) {
        html += '<div class="slide-info-card" style="padding: 16px; box-sizing: border-box; display: flex; flex-direction: column;">';
        html += '<div class="slide-card-title" style="font-size: 16px; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1.5px solid #64748b;">' + slide.items[si].label + '</div>';
        html += '<div class="slide-card-content" style="font-size: 14.5px; line-height: 1.6; color: #475569;">' + slide.items[si].text + '</div>';
        html += '</div>';
    }
    html += '</div>';
    if (slide.value) {
        html += '<div class="slide-info-card" style="margin-top: 16px; padding: 12px 16px;">' + slide.value + '</div>';
    }
} else {
    html += '<div class="slide-info-card" style="' + cardStyle + '">';
    if (slide.items && slide.items.length) {
        html += '  <div class="slide-card-content">';
        for (var si = 0; si < slide.items.length; si++) {
            if (si > 0) html += '<div style="border-top: 1px solid #e2e8f0; margin: 16px 0;"></div>';
            html += '<div style="margin-bottom: 4px; font-size: 15px; font-weight: 700; color: #1a1a1a;">' + slide.items[si].label + '</div>';
            html += '<div>' + slide.items[si].text + '</div>';
        }
        html += '  </div>';
    } else if (slide.value) {
        html += '  <div class="slide-card-content">' + slide.value + '</div>';
    }
    html += '</div>';
}
}"""

if target in content:
    content = content.replace(target, replacement)
    with open("backend/app/static/index.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Target not found")
