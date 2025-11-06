package pages;

import java.io.File;
import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;


public class InvoicePreviewPage {

    private WebDriver driver;
    private WebDriverWait wait;

    private By pdfButton = By.xpath("//button[.//p[text()='PDF']]");

    public InvoicePreviewPage(WebDriver driver) {
        this.driver = driver;

        wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        wait.until(ExpectedConditions.numberOfWindowsToBe(2));

        for(String window: driver.getWindowHandles()){
            driver.switchTo().window(window);
        }

        wait.until(ExpectedConditions.visibilityOfAllElementsLocatedBy(pdfButton));
    }

    public void clickPDFButton(String invoiceNumber){
        driver.findElement(pdfButton).click();

        // Construir la ruta completa donde Chrome descarga los archivos
        String downloadPath = System.getProperty("user.home") + "/Downloads/" + invoiceNumber + ".pdf";
        File file = new File(downloadPath);
        
        // Esperar hasta 30 segundos para que el archivo se descargue
        int maxWaitTime = 30; // segundos
        int waitedTime = 0;
        
        while (!file.exists() && waitedTime < maxWaitTime) {
            try{
                Thread.sleep(1000);
                waitedTime++;
            }catch(InterruptedException e){
                e.printStackTrace();
            }
        }
        
        if (!file.exists()) {
            throw new RuntimeException("El archivo PDF no se descargó después de " + maxWaitTime + " segundos. Ruta esperada: " + downloadPath);
        }
        
        System.out.println("PDF descargado exitosamente en: " + downloadPath);
    }
}