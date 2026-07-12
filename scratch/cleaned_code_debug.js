window._buildSlideHtml = function(slide, sectionIdx, slideIdx) {
console.log("[_buildSlideHtml] slide:", slide, "sectionIdx:", sectionIdx, "slideIdx:", slideIdx);
var html = '';
var hasImageProp = slide.hasOwnProperty('image') || slide.hasOwnProperty('images');

if (hasImageProp) {
var hasTextContent = (slide.value && slide.value.trim() !== '') || (slide.items && slide.items.length > 0);

if (!hasTextContent) {
// SADECE GÖRSEL (İçerik yok)
if (slide.image) {
html += '<div class="slide-image-container" style="min-height: 400px;">';
html += '  <div onmouseenter="var b=this.querySelector(\'.img-change-btn\'); if(b) b.style.opacity=1;" onmouseleave="var b=this.querySelector(\'.img-change-btn\'); if(b) b.style.opacity=0;" style="position: relative; display: inline-block; width: 100%; text-align: center;">';
html += '    <img src="' + slide.image + '" style="max-width: 100%; max-height: 400px; object-fit: contain; border-radius: 6px;" />';
html += '    <label class="img-change-btn" style="position: absolute; top: 8px; right: 8px; opacity: 0; transition: opacity 0.2s; cursor: pointer; background: rgba(17, 24, 39, 0.85); color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; z-index: 10; box-shadow: 0 2px 8px rgba(0,0,0,0.3);" title="Görseli Değiştir">';
html += '      📷';
html += '      <input type="file" accept="image/*" onchange="window.uploadSlideImage(this, \'' + sectionIdx + '\', ' + slideIdx + ')" style="display: none;" />';
html += '    </label>';
html += '  </div>';
html += '</div>';
} else {
html += '<div class="slide-image-container" style="min-height: 400px;">';
html += '  <div class="slide-image-placeholder" style="min-height: 360px;">';
html += '    <span style="display: block; color: #64748b; font-size: 14px; margin-bottom: 16px; font-weight: 600;">Henüz görsel yüklenmemiş.</span>';
html += '    <label style="cursor: pointer; background: #2563eb; color: white; padding: 8px 18px; border-radius: 6px; font-size: 13px; font-weight: 700; display: inline-block; transition: background 0.2s; box-shadow: 0 2px 4px rgba(37,99,235,0.2);">';
html += '      Görsel Yükle';
html += '      <input type="file" accept="image/*" onchange="window.uploadSlideImage(this, \'' + sectionIdx + '\', ' + slideIdx + ')" style="display: none;" />';
html += '    </label>';
html += '  </div>';
html += '</div>';
}
} else {
var useThreeColumns = slide.items && (slide.items.length === 2 || slide.items.length === 3);

if (useThreeColumns) {
var imgOrder = slide.imageRight === true ? 'order: 3;' : 'order: 1;';
var item0Order = slide.imageRight === true ? 'order: 1;' : 'order: 2;';
var item1Order = slide.imageRight === true ? 'order: 2;' : 'order: 3;';
var cardClass = 'slide-info-card' + (slide.compact ? ' compact' : '');

html += '<div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; width: 100%;">';

// 1. Kolon: Görsel
html += '  <div style="flex: 1.2; min-width: 250px; display: flex; flex-direction: column; justify-content: flex-start; ' + imgOrder + '">';
if (slide.image) {
html += '    <div class="slide-image-container" style="min-height: 400px; display: flex; align-items: center;">';
html += '      <div onmouseenter="var b=this.querySelector(\'.img-change-btn\'); if(b) b.style.opacity=1;" onmouseleave="var b=this.querySelector(\'.img-change-btn\'); if(b) b.style.opacity=0;" style="position: relative; display: inline-block; width: 100%; text-align: center;">';
html += '        <img src="' + slide.image + '" style="max-width: 100%; max-height: 400px; object-fit: contain; border-radius: 6px;" />';
html += '        <label class="img-change-btn" style="position: absolute; top: 8px; right: 8px; opacity: 0; transition: opacity 0.2s; cursor: pointer; background: rgba(17, 24, 39, 0.85); color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; z-index: 10; box-shadow: 0 2px 8px rgba(0,0,0,0.3);" title="Görseli Değiştir">';
html += '          📷';
html += '          <input type="file" accept="image/*" onchange="window.uploadSlideImage(this, \'' + sectionIdx + '\', ' + slideIdx + ')" style="display: none;" />';
html += '        </label>';
html += '      </div>';
html += '    </div>';
} else {
html += '    <div class="slide-image-container" style="min-height: 400px; display: flex; align-items: center;">';
html += '      <div class="slide-image-placeholder" style="min-height: 360px; width: 100%;">';
html += '        <span style="display: block; color: #64748b; font-size: 14px; margin-bottom: 16px; font-weight: 600;">Henüz görsel yüklenmemiş.</span>';
html += '        <label style="cursor: pointer; background: #2563eb; color: white; padding: 8px 18px; border-radius: 6px; font-size: 13px; font-weight: 700; display: inline-block; transition: background 0.2s; box-shadow: 0 2px 4px rgba(37,99,235,0.2);">';
html += '          Görsel Yükle';
html += '          <input type="file" accept="image/*" onchange="window.uploadSlideImage(this, \'' + sectionIdx + '\', ' + slideIdx + ')" style="display: none;" />';
html += '        </label>';
html += '      </div>';
html += '    </div>';
}
html += '  </div>';

// 2. Kolon: Orta (Enlem)
html += '  <div style="flex: 1; min-width: 200px; ' + item0Order + '">';
html += '    <div class="' + cardClass + '">';
html += '      <div class="slide-card-title">' + slide.items[0].label + '</div>';
html += '      <div class="slide-card-content">' + slide.items[0].text + '</div>';
html += '    </div>';
html += '  </div>';

// 3. Kolon: Sağ (Boylam)
html += '  <div style="flex: 1; min-width: 200px; ' + item1Order + '">';
html += '    <div class="' + cardClass + '">';
html += '      <div class="slide-card-title">' + slide.items[1].label + '</div>';
html += '      <div class="slide-card-content">' + slide.items[1].text + '</div>';
html += '    </div>';
html += '  </div>';

html += '</div>';
} else {
// İki kolonlu düzen (Sol: Görsel, Sağ: Metin veya row-reverse ile tersi)
var rowDirection = slide.imageRight === true ? 'flex-direction: row-reverse;' : '';
html += '<div style="display: flex; gap: 24px; align-items: stretch; flex-wrap: wrap; width: 100%; ' + rowDirection + '">';

// Sol Kolon (Görsel)
var separatorStyle = slide.imageRight === true ? 'border-left: 2px solid #94a3b8; padding-left: 24px;' : 'border-right: 2px solid #94a3b8; padding-right: 24px;';
html += '  <div style="flex: 1; min-width: 250px; display: flex; flex-direction: column; justify-content: center; ' + separatorStyle + '">';

var isMultiImage = Array.isArray(slide.images);
var activeImgIdx = 0;
var currentImage = '';
var hasAnyImages = false;
if (isMultiImage) {
window._activeImageIndices = window._activeImageIndices || {};
var key = sectionIdx + '_' + slideIdx;
activeImgIdx = window._activeImageIndices[key] || 0;
if (activeImgIdx >= slide.images.length) activeImgIdx = 0;
if (activeImgIdx < 0) activeImgIdx = 0;
currentImage = slide.images[activeImgIdx] || '';
hasAnyImages = slide.images.length > 0;
} else {
currentImage = slide.image || '';
hasAnyImages = !!currentImage;
}

if (hasAnyImages) {
html += '    <div class="slide-image-container" style="min-height: 400px; display: flex; align-items: center; position: relative;">';
html += '      <div onmouseenter="var b=this.querySelectorAll(\'.img-ctrl-btn\'); b.forEach(function(x){x.style.opacity=1;});" onmouseleave="var b=this.querySelectorAll(\'.img-ctrl-btn\'); b.forEach(function(x){x.style.opacity=0;});" style="position: relative; display: inline-block; width: 100%; text-align: center;">';
html += '        <img src="' + currentImage + '" style="max-width: 100%; max-height: 400px; object-fit: contain; border-radius: 6px;" />';

html += '        <div class="img-ctrl-btn" style="position: absolute; top: 8px; right: 8px; opacity: 0; transition: opacity 0.2s; display: flex; gap: 8px; z-index: 10;">';
if (isMultiImage) {
html += '          <button onclick="window.deleteSlideImage(\'' + sectionIdx + '\', ' + slideIdx + ')" style="cursor: pointer; background: rgba(239, 68, 68, 0.85); border: none; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.3);" title="Görseli Sil">🗑️</button>';
}
html += '          <label style="cursor: pointer; background: rgba(17, 24, 39, 0.85); color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.3);" title="' + (isMultiImage ? 'Yeni Görsel Ekle' : 'Görseli Değiştir') + '">';
html += '            📷';
html += '            <input type="file" accept="image/*" onchange="window.uploadSlideImage(this, \'' + sectionIdx + '\', ' + slideIdx + ')" style="display: none;" />';
html += '          </label>';
html += '        </div>';

if (isMultiImage && slide.images.length > 1) {
html += '        <button class="img-ctrl-btn" onclick="window.changeSlideSubImage(\'' + sectionIdx + '\', ' + slideIdx + ', -1)" style="position: absolute; left: 8px; top: 50%; transform: translateY(-50%); opacity: 0; transition: opacity 0.2s; cursor: pointer; background: rgba(0, 0, 0, 0.6); border: none; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; z-index: 10; font-weight: bold;">◀</button>';
html += '        <button class="img-ctrl-btn" onclick="window.changeSlideSubImage(\'' + sectionIdx + '\', ' + slideIdx + ', 1)" style="position: absolute; right: 8px; top: 50%; transform: translateY(-50%); opacity: 0; transition: opacity 0.2s; cursor: pointer; background: rgba(0, 0, 0, 0.6); border: none; color: white; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; z-index: 10; font-weight: bold;">▶</button>';
html += '        <div class="img-ctrl-btn" style="position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.6); color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; z-index: 10; opacity: 0; transition: opacity 0.2s;">' + (activeImgIdx + 1) + ' / ' + slide.images.length + '</div>';
}

html += '      </div>';
html += '    </div>';
} else {
html += '    <div class="slide-image-container" style="min-height: 400px; display: flex; align-items: center;">';
html += '      <div class="slide-image-placeholder" style="min-height: 360px; width: 100%;">';
html += '        <span style="display: block; color: #64748b; font-size: 14px; margin-bottom: 16px; font-weight: 600;">Henüz görsel yüklenmemiş.</span>';
html += '        <label style="cursor: pointer; background: #2563eb; color: white; padding: 8px 18px; border-radius: 6px; font-size: 13px; font-weight: 700; display: inline-block; transition: background 0.2s; box-shadow: 0 2px 4px rgba(37,99,235,0.2);">';
html += '          Görsel Yükle';
html += '          <input type="file" accept="image/*" onchange="window.uploadSlideImage(this, \'' + sectionIdx + '\', ' + slideIdx + ')" style="display: none;" />';
html += '        </label>';
html += '      </div>';
html += '    </div>';
}
html += '  </div>';

// Sağ Kolon (Metin)
html += '  <div style="flex: 1.5; min-width: 250px; display: flex; flex-direction: column;">';
if (slide.items && (slide.items.length === 4 || slide.items.length === 5)) {
// Grid Düzeni (Minik Kartlar)
html += '    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-content: stretch; overflow: visible;">';
for (var si = 0; si < slide.items.length; si++) {
var isLast = si === slide.items.length - 1;
var isOdd = slide.items.length % 2 !== 0;
var gridSpan = (isLast && isOdd) ? 'grid-column: span 2; max-width: calc(50% - 8px); margin: 0 auto; width: 100%;' : '';
html += '      <div class="slide-info-card" style="padding: 16px; box-sizing: border-box; display: flex; flex-direction: column; justify-content: flex-start; min-height: 170px; ' + gridSpan + '">';
html += '        <div class="slide-card-title" style="font-size: 13.5px; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1.5px solid #64748b;">' + slide.items[si].label + '</div>';
html += '        <div class="slide-card-content" style="font-size: 12.5px; line-height: 1.6; color: #475569;">' + slide.items[si].text + '</div>';
html += '      </div>';
}
html += '    </div>';
if (slide.value) {
html += '    <div class="slide-info-card" style="margin-top: 12px; padding: 12px 16px; font-size: 13px; line-height: 1.5; color: #334155; border-left: 4px solid #d97706; background: #fafafa;">' + slide.value + '</div>';
}
} else {
html += '    <div class="slide-info-card">';
if (slide.items && slide.items.length) {
if (slide.items.length === 1) {
html += '      <div class="slide-card-title">' + slide.items[0].label + '</div>';
html += '      <div class="slide-card-content">' + slide.items[0].text + '</div>';
} else {
html += '      <div class="slide-card-content">';
for (var si = 0; si < slide.items.length; si++) {
if (si > 0) html += '<div style="border-top: 1px solid #e2e8f0; margin: 16px 0;"></div>';
html += '<div style="margin-bottom: 4px; font-size: 15px; font-weight: 700; color: #1a1a1a;">' + slide.items[si].label + '</div>';
html += '<div>' + slide.items[si].text + '</div>';
}
html += '      </div>';
}
} else if (slide.value) {
html += '      <div class="slide-card-content">' + slide.value + '</div>';
}
html += '    </div>';
}
html += '  </div>';

html += '</div>';
}
}
} else {
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
}

return html;
};
