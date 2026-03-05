import java.util.Arrays;
import java.util.Random;

public class BusquedaBinariasSocialnk {

    // ── 1. Búsqueda binaria iterativa ──
    public static int busquedaBinaria(int[] array, int objetivo) {
        int izquierda = 0;
        int derecha = array.length - 1;

        while (izquierda <= derecha) {
            int medio = izquierda + (derecha - izquierda) / 2;

            if (array[medio] == objetivo) {
                return medio; // índice encontrado
            } else if (array[medio] < objetivo) {
                izquierda = medio + 1;
            } else {
                derecha = medio - 1;
            }
        }
        return -1; // no encontrado
    }

    // ── 2. Búsqueda lineal para comparación ──
    public static int busquedaLineal(int[] array, int objetivo) {
        for (int i = 0; i < array.length; i++) {
            if (array[i] == objetivo) return i;
        }
        return -1;
    }

    // ── 3. Demostración ──
    public static void main(String[] args) {
        final int TAM = 1_000_000;
        int[] usuarios = new int[TAM];

        // Generar IDs de usuario del 1 al 1.000.000
        for (int i = 0; i < TAM; i++) {
            usuarios[i] = i + 1;
        }

        // Ordenar con Arrays.sort (Mergesort/Timsort internamente)
        Arrays.sort(usuarios);

        System.out.println("=== Búsqueda eficiente en Socialnk ===");
        System.out.printf("Array de %,d usuarios ordenado.%n%n", TAM);

        // Casos de prueba
        int[] objetivos = {1, 500_000, 1_000_000, 1_000_001};
        String[] descripciones = {
            "Primer elemento (inicio)",
            "Elemento central",
            "Último elemento (fin)",
            "Elemento inexistente"
        };

        for (int t = 0; t < objetivos.length; t++) {
            int objetivo = objetivos[t];

            // Búsqueda binaria
            long inicioBin = System.nanoTime();
            int resBin = busquedaBinaria(usuarios, objetivo);
            long tiempoBin = System.nanoTime() - inicioBin;

            // Búsqueda lineal
            long inicioLin = System.nanoTime();
            int resLin = busquedaLineal(usuarios, objetivo);
            long tiempoLin = System.nanoTime() - inicioLin;

            System.out.printf("Búsqueda: %s (objetivo=%,d)%n", descripciones[t], objetivo);
            System.out.printf("  Binaria  → índice: %6d | tiempo: %,d ns%n", resBin, tiempoBin);
            System.out.printf("  Lineal   → índice: %6d | tiempo: %,d ns%n", resLin, tiempoLin);
            if (tiempoBin > 0) {
                System.out.printf("  Mejora: x%.0f más rápida%n", (double) tiempoLin / tiempoBin);
            }
            System.out.println();
        }
    }
}
