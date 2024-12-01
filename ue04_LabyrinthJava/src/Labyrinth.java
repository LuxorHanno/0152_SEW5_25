import java.util.Arrays;

import static java.lang.String.valueOf;

/**
 *Solve a Maze with Java
 *@author Hanno Postl
 */

public class Labyrinth {
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
     * Wandelt (unveränderliche) Strings in Char-Arrays
     * @param map  der Plan, ein String je Zeile
     * @return char[][] des Plans
     */
    public static char[][] fromStrings(String[] map) {
        return Arrays.stream(map).map(String::toCharArray).toArray(char[][]::new);
    }


    /**
     * Ausgabe des Layrinths
     * @param lab
     */
    public static void printLabyrinth(char[][] lab) {
        Arrays.stream(lab).forEach(line -> System.out.println(valueOf(line)));
    }

    /**
     * Sucht, ob ein Weg aus dem Labyrinth führt
     * @param zeile     aktuelle Position
     * @param spalte     aktuelle Position
     * @param lab     Labyrinth
     * @throws InterruptedException    für die verlangsamte Ausgabe mit sleep()
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

        lab [zeile][spalte] = ' ';

        return hit;
    }

    /**
     * Ermittelt die Anzahl der Wege, die aus dem Labyrinth führen
     * @param zeile     aktuelle Position
     * @param spalte     aktuelle Position
     * @param lab     Labyrinth
     * @return anzahl Anzahl der unterschiedlichen Wege, die aus dem Labyrinth führen (ein bereits besuchtes Feld darf nicht nochmals betreten werden)
     * @throws InterruptedException    für die verlangsamte Ausgabe mit sleep()
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

        lab [zeile][spalte] = ' ';

        return hits;
    }


    public static void main(String[] args) throws InterruptedException {
        char[][] labyrinth = fromStrings(maps[2]);
        printLabyrinth(labyrinth);
        System.out.println("Ausgang gefunden: " + (suchen(5, 5, labyrinth) ? "ja" : "nein"));
        System.out.println("Anzahl Wege: " + alleSuchen(5, 5, labyrinth));
    }
}
