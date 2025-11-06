package pages;

import java.io.File;
import java.time.Duration;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class InvoiceGeneratorPage {

    private WebDriver driver;
    private WebDriverWait wait;

    //HEADER
    private By invoiceTitleField        = By.id("invoice-title");
    private By logoInput                = By.xpath("//div[contains(@class,'photo-drop-zone')]/input[@type='file']");

    //FROM FIELDS
    private By fromNameField            = By.id("company-name");
    private By fromEmailField           = By.id("company-email");
    private By fromAddressField         = By.id("company-address-address1");
    private By fromCityStateField       = By.id("company-address-address2");
    private By fromZipCodeField         = By.id("company-address-address3");
    private By fromPhoneField           = By.id("company-phone");
    private By fromBusinessPhoneField   = By.id("company-business-number");

    //TO FIELDS
    private By toNameField              = By.id("client-name");
    private By toEmailField             = By.id("client-email");
    private By toAddressField           = By.id("client-address-address1");
    private By toPhoneField             = By.id("client-phone");


    private By invoiceNumberField       = By.id("invoice-number");

    //ITEMS
    private String itemRow_Format       = "(//tr[contains(@class, 'item-row') and not(contains(@class, 'item-row-new'))])[%d]";
    private By itemDescription_Child    = By.id("item-code");
    private By itemPrice_Child          = By.xpath("td[contains(@class, 'item-row-rate')]/descendant::input");
    private By itemQuantity_Child       = By.xpath("td[contains(@class, 'item-row-quantity')]/descendant::input");
    private By itemDetails_Child        = By.tagName("textarea");
    private By addItemButton            = By.id("add-item-button");

    private By getLinkButton            = By.xpath("//button[contains(@class, 'btn-get-public-link')]");   

    private By colorSelectList          = By.className("color-select-option");


    public InvoiceGeneratorPage(WebDriver driver){
        this.driver = driver;
        wait = new WebDriverWait(driver, Duration.ofSeconds(5));
    }

    public void setInvoiceTitle(String title){
        WebElement field = driver.findElement(invoiceTitleField);
        wait.until(ExpectedConditions.elementToBeClickable(field));
        field.clear();
        field.sendKeys(title);
    }

  public void setLogo(File imgFile){
    WebElement input = wait.until(ExpectedConditions.presenceOfElementLocated(logoInput));
    input.sendKeys(imgFile.getAbsolutePath());
}

    public void setFromName(String name){
        driver.findElement(fromNameField).sendKeys(name);
    }

    public void setFromEmail(String email){
        driver.findElement(fromEmailField).sendKeys(email);
    }

    public void setFromAddress(String address){
        driver.findElement(fromAddressField).sendKeys(address);
    }

    public void setFromCityState(String cityAndState){
        driver.findElement(fromCityStateField).sendKeys(cityAndState);
    }

    public void setFromZipCode(String zipCode){
        driver.findElement(fromZipCodeField).sendKeys(zipCode);
    }

    public void setFromPhone(String phoneNumber){
        driver.findElement(fromPhoneField).sendKeys(phoneNumber);
    }

    public void setFromBusinessPhone(String phoneNumber){
        driver.findElement(fromBusinessPhoneField).sendKeys(phoneNumber);
    }

    public void setToName(String name){
        driver.findElement(toNameField).sendKeys(name);
    }

    public void setToEmail(String email){
        driver.findElement(toEmailField).sendKeys(email);
    }

    public void setToAddress(String address){
        driver.findElement(toAddressField).sendKeys(address);
    }

    public void setToPhone(String phoneNumber){
        driver.findElement(toPhoneField).sendKeys(phoneNumber);
    }

    public void setInvoiceNumber(String invoiceNumber){
        WebElement field = driver.findElement(invoiceNumberField);
        field.clear();
        field.sendKeys(invoiceNumber);
    }

    public void setItemDescription(int itemIndex, String description){
        getItemRow(itemIndex).findElement(itemDescription_Child).sendKeys(description);
    }

    public void setItemPrice(int itemIndex, String price){
        getItemRow(itemIndex).findElement(itemPrice_Child).sendKeys(price);
    }

    public void setItemQuantity(int itemIndex, String quantity){
        getItemRow(itemIndex).findElement(itemQuantity_Child).sendKeys(quantity);
    }

    public void setItemAdditionalDetails(int itemIndex, String details){
        getItemRow(itemIndex).findElement(itemDetails_Child).sendKeys(details);
    }

    public void clickToAddNewItem(){
        WebElement button = driver.findElement(addItemButton);
        wait.until(ExpectedConditions.elementToBeClickable(button));
        button.click();
    }

    public void selectColor(int index){
        driver.findElements(colorSelectList).get(index).click();
    }

    public InvoicePreviewPage clickGetLink(){
        WebElement button = driver.findElement(getLinkButton);
        wait.until(ExpectedConditions.elementToBeClickable(button));
        button.click();
        return new InvoicePreviewPage(driver);
    }

    private WebElement getItemRow(int index){
        String xpath = String.format(itemRow_Format, index);
        return driver.findElement(By.xpath(xpath));
    }
}
