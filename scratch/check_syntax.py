import os, subprocess

content = open('backend/app/static/index.html').read()
start_idx = 0
script_count = 0
syntax_error = False

temp_file = 'scratch/temp_script.js'

while True:
    start_idx = content.find('<script>', start_idx)
    if start_idx == -1:
        break
    end_idx = content.find('</script>', start_idx)
    if end_idx == -1:
        break
    script_code = content[start_idx+8:end_idx]
    script_count += 1
    
    open(temp_file, 'w').write(script_code)
    
    # Node.js --check syntax kontrolü
    p = subprocess.Popen(['node', '--check', temp_file], stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        print(f'Syntax Error in script {script_count}:')
        print(stderr.decode())
        syntax_error = True
    start_idx = end_idx + 9

if os.path.exists(temp_file):
    os.remove(temp_file)

if not syntax_error:
    print('No syntax errors found in script blocks.')
