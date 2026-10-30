import com.healthmarketscience.jackcess.*;
import java.io.*;
import java.nio.file.*;
import java.text.SimpleDateFormat;
import java.util.*;

/** Crea una base de datos Microsoft Access (.accdb) con tablas, llaves primarias,
 *  relaciones con integridad referencial y los datos de prueba, usando Jackcess. */
public class GenerarAccess {
  static class Col { String nombre, tipo; int largo; boolean nulo, pk, auto; }

  public static void main(String[] a) throws Exception {
    String def = a[0], salida = a[1];
    Map<String, List<Col>> tablas = new LinkedHashMap<>();
    Map<String, List<String[]>> filas = new HashMap<>();
    List<String[]> fks = new ArrayList<>();
    String actual = null;
    for (String l : Files.readAllLines(Paths.get(def))) {
      if (l.startsWith("T|")) { actual = l.substring(2); tablas.put(actual, new ArrayList<>()); filas.put(actual, new ArrayList<>()); }
      else if (l.startsWith("C|")) {
        String[] p = l.split("\\|", -1); Col c = new Col();
        c.nombre = p[1]; c.tipo = p[2]; c.largo = Integer.parseInt(p[3]); c.nulo = p[4].equals("1"); c.pk = p[5].equals("1");
        c.auto = c.pk && (p[6].contains("nextval") || p[6].contains("auto_increment") || p[6].contains("identity"));
        tablas.get(actual).add(c);
      } else if (l.startsWith("R|")) filas.get(actual).add(l.substring(2).split("\t", -1));
      else if (l.startsWith("F|")) fks.add(l.substring(2).split("\\|"));
    }
    new File(salida).delete();
    SimpleDateFormat fmt = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    try (Database db = new DatabaseBuilder(new File(salida)).setFileFormat(Database.FileFormat.V2016).create()) {
      db.setAllowAutoNumberInsert(true);
      for (var e : tablas.entrySet()) {
        TableBuilder tb = new TableBuilder(e.getKey());
        List<String> pk = new ArrayList<>();
        for (Col c : e.getValue()) {
          ColumnBuilder cb = new ColumnBuilder(c.nombre);
          String t = c.tipo.toLowerCase();
          if (t.contains("char") || t.equals("text") || t.equals("enum")) {
            if (c.largo > 0 && c.largo <= 255) cb.setType(DataType.TEXT).setLengthInUnits(c.largo);
            else cb.setType(DataType.MEMO);
          } else if (t.equals("boolean") || t.equals("tinyint")) cb.setType(DataType.BOOLEAN);
          else if (t.equals("smallint")) cb.setType(DataType.INT);
          else if (t.contains("int")) cb.setType(DataType.LONG);
          else if (t.contains("numeric") || t.contains("decimal") || t.contains("double") || t.contains("real")) cb.setType(DataType.DOUBLE);
          else if (t.contains("date") || t.contains("time")) cb.setType(DataType.SHORT_DATE_TIME);
          else cb.setType(DataType.MEMO);
          if (c.auto) cb.setAutoNumber(true);
          tb.addColumn(cb);
          if (c.pk) pk.add(c.nombre);
        }
        if (!pk.isEmpty()) tb.setPrimaryKey(pk.toArray(new String[0]));
        Table tabla = tb.toTable(db);
        int nfilas = 0;
        for (String[] f : filas.get(e.getKey())) {
          Object[] vals = new Object[f.length];
          for (int i = 0; i < f.length; i++) {
            Col c = e.getValue().get(i); String v = f[i]; String t = c.tipo.toLowerCase();
            if (v.equals("\\N")) vals[i] = null;
            else if (t.equals("boolean") || t.equals("tinyint")) vals[i] = v.equals("1") || v.equals("true");
            else if (t.contains("date") || t.contains("time")) vals[i] = fmt.parse(v);
            else if (t.contains("int")) vals[i] = Integer.valueOf(v);
            else if (t.contains("numeric") || t.contains("decimal") || t.contains("double")) vals[i] = Double.valueOf(v);
            else vals[i] = v.replace("\\\\", "\\");
          }
          tabla.addRow(vals); nfilas++;
        }
        System.out.println("Tabla " + e.getKey() + ": " + nfilas + " registros");
      }
      for (String[] fk : fks) {
        new RelationshipBuilder(db.getTable(fk[0]), db.getTable(fk[2]))
          .addColumns(fk[1], fk[3]).setReferentialIntegrity().setName(fk[0] + "_" + fk[2] + "_" + fk[3]).toRelationship(db);
        System.out.println("Relación " + fk[0] + "." + fk[1] + " 1 -> N " + fk[2] + "." + fk[3]);
      }
    }
  }
}
