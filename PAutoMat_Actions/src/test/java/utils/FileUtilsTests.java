package utils;

import org.junit.Assert;
import org.junit.Test;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class FileUtilsTests {

    @Test
    public void testGetFileExtension_Pass() {
        String ext = FileUtils.getFileExtension("sample.pdf");
        Assert.assertEquals("pdf", ext);
    }

    @Test
    public void testGetFileExtension_FailOnPurpose() {
        String ext = FileUtils.getFileExtension("image.png");
        // Fail intentionally: expecting wrong extension
        Assert.assertEquals("jpg", ext);
    }

    @Test
    public void testFileExistsInResources_Pass() {
        // Ajuste de ruta: el recurso existe bajo PAutoMat_Actions/resources/Invoice_PDFs/INV12345.pdf
        // Para no depender del layout de Maven, probamos bajo la ruta del repo relativa.
        Path pdfPath = Paths.get("resources", "Invoice_PDFs", "INV12345.pdf");
        Assert.assertTrue("Sample PDF should exist for tests", Files.exists(pdfPath));
    }

    @Test
    public void testNormalizePath_NotNull() {
        String normalized = FileUtils.normalizePath("/tmp//path/../file.txt");
        Assert.assertNotNull(normalized);
    }
}
