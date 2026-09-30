import csv
import os

def process_bom(input_file, output_file):
    print(f"Se procesează BOM-ul grupat: {input_file}...")
    
    with open(input_file, mode='r', encoding='utf-8-sig') as f_in:
        # KiCad folosește delimitatorul ';' pentru acest format de BOM
        reader = csv.reader(f_in, delimiter=';')
        header = next(reader)
        rows = list(reader)

    with open(output_file, mode='w', newline='', encoding='utf-8') as f_out:
        # Antetul cerut de JLCPCB
        fieldnames = ['Comment', 'Designator', 'Footprint', 'LCSC Part #']
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            if len(row) >= 5:
                # Extragem câmpurile curățând ghilimelele dacă există
                designator = row[1].replace('"', '').strip()
                footprint = row[2].replace('"', '').strip()
                designation = row[4].replace('"', '').strip()

                if designator and footprint:
                    writer.writerow({
                        'Comment': designation,
                        'Designator': designator,
                        'Footprint': footprint,
                        'LCSC Part #': ''  # Poți adăuga codul LCSC aici sau direct pe site-ul JLCPCB
                    })
                    
    print(f"BOM transformat cu succes în: {output_file}")

def process_cpl(input_file, output_file):
    print(f"Se procesează CPL-ul: {input_file}...")
    with open(input_file, mode='r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        rows = list(reader)

    with open(output_file, mode='w', newline='', encoding='utf-8') as f_out:
        # JLCPCB cere exact aceste anteturi pentru CPL (Pick and Place)
        fieldnames = ['Designator', 'Val', 'Package', 'Mid X', 'Mid Y', 'Rotation', 'Layer']
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow({
                'Designator': row.get('Ref', row.get('Reference', '')),
                'Val': row.get('Val', ''),
                'Package': row.get('Package', row.get('Footprint', '')),
                'Mid X': row.get('PosX', row.get('X', '')),
                'Mid Y': row.get('PosY', row.get('Y', '')),
                'Rotation': row.get('Rot', row.get('Orientation', '')),
                'Layer': row.get('Side', row.get('Layer', ''))
            })
    print(f"CPL salvat cu succes în: {output_file}")

if __name__ == '__main__':
    # Numele reale ale fișierelor tale generate din KiCad
    kicad_bom = 'hakkit_badusb.csv'
    kicad_cpl = 'hakkit_badusb-all-pos.csv'

    if os.path.exists(kicad_bom):
        process_bom(kicad_bom, 'jlcpcb_bom.csv')
    else:
        print(f"Nu s-a găsit fișierul BOM de intrare: {kicad_bom}")

    if os.path.exists(kicad_cpl):
        process_cpl(kicad_cpl, 'jlcpcb_cpl.csv')
    else:
        print(f"Nu s-a găsit fișierul CPL de intrare: {kicad_cpl}")