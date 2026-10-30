import com.healthmarketscience.jackcess.*;
import java.io.File;
/** Abre el .accdb y lista tablas, registros, llave primaria y relaciones (comprobación). */
public class VerificarAccess {
  public static void main(String[] a) throws Exception {
    try (Database db = DatabaseBuilder.open(new File(a[0]))) {
      System.out.println("Archivo: " + a[0] + " formato " + db.getFileFormat());
      for (String t : db.getTableNames()) {
        Table tb = db.getTable(t);
        System.out.println("  " + t + ": " + tb.getRowCount() + " registros, PK=" + tb.getPrimaryKeyIndex().getColumns().get(0).getName());
      }
      int n = 0; for (String t : db.getTableNames()) for (Relationship r : db.getRelationships(db.getTable(t))) if (r.getToTable().getName().equals(t)) n++;
      System.out.println("  Relaciones con integridad referencial: " + n);
    }
  }
}
