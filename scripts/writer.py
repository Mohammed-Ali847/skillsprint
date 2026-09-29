import sys, base64, os
if len(sys.argv) < 3:
    print('Usage: writer.py <filepath> <base64_content>')
    sys.exit(1)
path = sys.argv[1]
os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
content = base64.b64decode(sys.argv[2].encode('utf-8')).decode('utf-8')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'Successfully wrote {path} ({len(content)} chars)')
