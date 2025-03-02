import java.io.IOException;
import java.lang.reflect.Array;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;

import static java.lang.String.valueOf;

/**
 * Solve a Maze with Java
 * @author Hanno Postl
 */
public class Labyrinth {
    // Predefined maps for the labyrinth
    public static String[][] maps = {{
            "############",
            "#  #     # #",
            "## # ### # #",
            "#  # # # # #",
            "## ### # # #",
            "#        # #",
            "## ####### #",
            "#          #",
            "# ######## #",
            "# #   #    #",
            "#   #   # ##",
            "######A#####"
    }, {
            "################################",
            "#                              #",
            "# ############################ #",
            "# # ###       ##  #          # #",
            "# #     ##### ### # ########## #",
            "# #   ##### #     # #      ### #",
            "# # ##### #   ###   # # ## # # #",
            "# # ### # ## ######## # ##   # #",
            "# ##### #  # #   #    #    ### #",
            "# # ### ## # # # # ####### # # #",
            "# #        # #   #     #     # #",
            "# ######## # ######### # ### # #",
            "# ####     #  # #   #  # ##### #",
            "# # #### #### # # # # ## # ### #",
            "#                      # #     #",
            "###########################A####"
    }, {
            "###########################A####",
            "#   #      ## # # ###  #     # #",
            "# ###### #### # # #### ##### # #",
            "# # ###  ## # # # #          # #",
            "# # ### ### # # # # # #### # # #",
            "# #     ### # # # # # ## # # # #",
            "# # # # ### # # # # ######## # #",
            "# # # #     #          #     # #",
            "# ### ################ # # # # #",
            "# #   #             ## # #   # #",
            "# # #### ############# # #   # #",
            "# #                    #     # #",
            "# # #################### # # # #",
            "# # #### #           ###     # #",
            "# # ## # ### ### ### ### # ### #",
            "# #    #     ##  ##  # ###   # #",
            "# ####   ###### #### # ###  ## #",
            "###########################A####"
    }, {
            "#############",
            "#           #",
            "#           #",
            "#           #",
            "###########A#"
    }};

    /**
     * Converts immutable strings to char arrays
     * @param map the plan, a string per line
     * @return char[][] representation of the plan
     */
    public static char[][] fromStrings(String[] map) {
        return Arrays.stream(map).map(String::toCharArray).toArray(char[][]::new);
    }

    /**
     * Prints the labyrinth
     * @param lab the labyrinth to print
     */
    public static void printLabyrinth(char[][] lab) {
        Arrays.stream(lab).forEach(line -> System.out.println(valueOf(line)));
    }

    /**
     * Searches for a way out of the labyrinth
     * @param zeile current row position
     * @param spalte current column position
     * @param lab the labyrinth
     * @return true if a way out is found, false otherwise
     * @throws InterruptedException for delayed output with sleep()
     */
    public static boolean suchen(int zeile, int spalte, char[][] lab) throws InterruptedException {
        if (lab[zeile][spalte] == 'A'){
            return true;
        }

        if (lab[zeile][spalte] == '#' || lab[zeile][spalte] == '.'){
            return false;
        }

        lab[zeile][spalte] = '.';

        //printLabyrinth(lab);
        //Thread.sleep(200);

        boolean hit = suchen(zeile, spalte+1, lab) ||
                suchen(zeile+1, spalte, lab) ||
                suchen(zeile, spalte-1, lab) ||
                suchen(zeile-1, spalte, lab);

        lab[zeile][spalte] = ' ';

        return hit;
    }

    /**
     * Determines the number of ways out of the labyrinth
     * @param zeile current row position
     * @param spalte current column position
     * @param lab the labyrinth
     * @return number of different ways out of the labyrinth (a previously visited field cannot be entered again)
     * @throws InterruptedException for delayed output with sleep()
     */
    public static int alleSuchen(int zeile, int spalte, char[][] lab) throws InterruptedException {
        if (lab[zeile][spalte] == 'A'){
            return 1;
        }

        if (lab[zeile][spalte] == '#' || lab[zeile][spalte] == '.'){
            return 0;
        }

        lab[zeile][spalte] = '.';

        //printLabyrinth(lab);
        //Thread.sleep(200);

        int hits = alleSuchen(zeile, spalte+1, lab) +
                alleSuchen(zeile+1, spalte, lab) +
                alleSuchen(zeile, spalte-1, lab) +
                alleSuchen(zeile-1, spalte, lab);

        lab[zeile][spalte] = ' ';

        return hits;
    }

    /**
     * Get a labyrinth from a file
     * @param path Path to a file
     * @return Labyrinth in char[][] format
     * @throws IOException IO error
     */
    public static char[][] labFromFile(Path path) throws IOException {
        return fromStrings(Files.readAllLines(path).toArray(String[]::new));
    }

    public static void main(String[] args) throws InterruptedException, IOException {
        //char[][] labyrinth = fromStrings(maps[2]);
        char[][] labyrinth = labFromFile(Path.of("/home/hanno/IdeaProjects/0152_SEW5_25/ue04_LabyrinthJava/src/l3.txt"));
        printLabyrinth(labyrinth);
        System.out.println("Ausgang gefunden: " + (suchen(5, 5, labyrinth) ? "ja" : "nein"));
        System.out.println("Anzahl Wege: " + alleSuchen(5, 5, labyrinth));
    }
}