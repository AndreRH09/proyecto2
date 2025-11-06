package pages;

import java.time.Duration;
import java.util.UUID;
import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.*;

public class SignupPage {

    private WebDriver driver;
    private WebDriverWait wait;

    // Localizadores
    private By firstNameField = By.id("firstName");
    private By lastNameField = By.id("lastName");
    private By emailField = By.id("email"); // corregido
    private By passwordField = By.id("password");
    private By consentCheckbox = By.id("consent");
    private By signupButton = By.cssSelector("button[data-testid='signup-btn']");

    public SignupPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void createAccount(String firstName, String lastName, String password) {
        // Generar email aleatorio
        String randomEmail = "user_" + UUID.randomUUID().toString().substring(0, 8) + "@gmail.com";

        wait.until(ExpectedConditions.visibilityOfElementLocated(firstNameField)).sendKeys(firstName);
        driver.findElement(lastNameField).sendKeys(lastName);
        driver.findElement(emailField).sendKeys(randomEmail);
        driver.findElement(passwordField).sendKeys(password);

        // Marca el checkbox si existe y no está seleccionado
        WebElement checkbox = driver.findElement(consentCheckbox);
        if (!checkbox.isSelected()) {
            checkbox.click();
        }

        // Clic en "Regístrate"
        driver.findElement(signupButton).click();

        System.out.println("Cuenta creada con email: " + randomEmail);
    }
}
