"""Genera un script SQL en dialecto Access (DDL) a partir de los .def: crear tablas, PK y relaciones.
En Access: Crear > Diseño de consulta > Vista SQL; pegar UNA sentencia a la vez y Ejecutar."""
def tipo(t, n, pk_auto):
    t = t.lower()
    if pk_auto: return 'COUNTER'
    if 'char' in t or t in ('text', 'enum'): return f'TEXT({n})' if 0 < n <= 255 else 'MEMO'
    if t in ('boolean', 'tinyint'): return 'YESNO'
    if t == 'smallint': return 'SHORT'
    if 'int' in t: return 'LONG'
    if 'date' in t or 'time' in t: return 'DATETIME'
    if 'numeric' in t or 'decimal' in t: return 'DOUBLE'
    return 'MEMO'
for base in ('prestamos', 'prestamos_aux'):
    out, fks, t = [f'-- Script DDL para Microsoft Access - base {base}\n-- Ejecutar una sentencia por consulta (Vista SQL). Luego: Herramientas de base de datos > Relaciones.\n'], [], None
    cols = []
    def cerrar():
        if t:
            pk = [c[0] for c in cols if c[4]]
            defs = ',\n  '.join(f'[{c[0]}] {tipo(c[1], c[2], c[4] and c[5])}{"" if c[3] or c[4] else " NOT NULL"}' for c in cols)
            out.append(f'CREATE TABLE [{t}] (\n  {defs},\n  CONSTRAINT [pk_{t}] PRIMARY KEY ({", ".join(pk)})\n);\n')
    for l in open(f'{base}.def', encoding='utf-8'):
        l = l.rstrip('\n'); p = l.split('|')
        if p[0] == 'T': cerrar(); t, cols = p[1], []
        elif p[0] == 'C': cols.append((p[1], p[2], int(p[3]), p[4] == '1', p[5] == '1', any(k in p[6] for k in ('nextval', 'auto_increment', 'identity'))))
        elif p[0] == 'F': fks.append(p[1:])
    cerrar()
    out.append('-- ===== Relaciones (integridad referencial) =====\n')
    for padre, cp, hija, ch in fks:
        out.append(f'ALTER TABLE [{hija}] ADD CONSTRAINT [fk_{hija}_{ch}] FOREIGN KEY ([{ch}]) REFERENCES [{padre}] ([{cp}]);\n')
    open(f'../{base}_access.sql', 'w', encoding='utf-8').write('\n'.join(out))
print('ok')
