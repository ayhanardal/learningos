import re

# index_origin_section.txt dosyasını oku
lines = open('/home/ubuntu/Desktop/agentos/projects/learningos/scratch/index_origin_section.txt').readlines()

cleaned_lines = []
for line in lines:
    m = re.match(r'^(\d+):\s*(.*)', line)
    if m:
        file_line_num = int(m.group(1))
        # _buildSlideHtml fonksiyonunun tamamını (1387'den 1595'e kadar) alalım
        if 1387 <= file_line_num <= 1595:
            cleaned_lines.append(m.group(2) + '\n')

cleaned_code = ''.join(cleaned_lines)

# index.html dosyasını oku
index_content = open('/home/ubuntu/Desktop/agentos/projects/learningos/backend/app/static/index.html').read()

# window._buildSlideHtml başlangıcı
start_marker = "window._buildSlideHtml = function(slide, sectionIdx, slideIdx) {"
end_marker = "window._renderSection = function(section, idx) {"

index_content_norm = index_content.replace('\r\n', '\n')
start_idx = index_content_norm.find(start_marker)
end_idx = index_content_norm.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # start_idx öncesi + cleaned_code (zaten fonksiyon tanımını içeriyor) + end_idx sonrası
    new_content = index_content_norm[:start_idx] + cleaned_code + "\n" + index_content_norm[end_idx:]
    open('/home/ubuntu/Desktop/agentos/projects/learningos/backend/app/static/index.html', 'w').write(new_content)
    print("SUCCESS")
else:
    print("Markers not found!")
