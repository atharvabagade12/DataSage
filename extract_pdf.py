import sys, subprocess

try:
    from pypdf import PdfReader
except ImportError:
    print("Installing pypdf...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', 'pypdf', '-q'])
    from pypdf import PdfReader

try:
    pdf_path = r'c:\Users\ATHARVA BAGADE\Downloads\DataSage_IRJET.pdf'
    out_path = r'c:\Users\ATHARVA BAGADE\Downloads\DataSage_IRJET_extracted.txt'
    
    reader = PdfReader(pdf_path)
    text = []
    for i, page in enumerate(reader.pages):
        text.append(f'\n--- Page {i+1} ---\n')
        text.append(page.extract_text() or '')
        
    full_text = ''.join(text)
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
        
    print(f'Successfully extracted {len(reader.pages)} pages to {out_path}')
    print('\n--- Snippet (first 1000 chars) ---')
    print(full_text[:1000])
    
except Exception as e:
    print(f"Error: {e}")
