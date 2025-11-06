package utils;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;

public class FileUtils {

    /**
     * Moves file from one location to another.
     * Deletes file from destination if it already exists, before moving
     * @param file file to move
     * @param destination pathname to move file to
     * @return was move successful
     */
    public static boolean moveFile(File file, String destination){

        File existingFile = new File(destination);
        if(existingFile.exists()){
            existingFile.delete();
        }

        return file.renameTo(new File(destination));
    }

    /**
     * Returns the lowercase extension of a file name without the dot. If none, returns empty string.
     */
    public static String getFileExtension(String filename) {
        if (filename == null) return "";
        int lastSep = Math.max(filename.lastIndexOf('/'), filename.lastIndexOf('\\'));
        String name = lastSep >= 0 ? filename.substring(lastSep + 1) : filename;
        int idx = name.lastIndexOf('.');
        if (idx <= 0 || idx == name.length() - 1) return "";
        return name.substring(idx + 1).toLowerCase();
    }

    /**
     * Normalizes a path using the platform defaults and removes redundant parts.
     */
    public static String normalizePath(String path) {
        if (path == null) return null;
        Path p = Paths.get(path).normalize();
        return p.toString();
    }
}
