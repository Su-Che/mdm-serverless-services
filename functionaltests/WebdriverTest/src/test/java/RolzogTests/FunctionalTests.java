package RolzogTests;

import org.testng.annotations.Test;
import org.testng.asserts.SoftAssert;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.testng.Assert;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeSuite;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

public class FunctionalTests {

    public WebDriver driver;

    @BeforeSuite
    public void beforeSuite() {

    	ChromeOptions chromeOptions = new ChromeOptions();
        chromeOptions.addArguments("--headless");
        chromeOptions.addArguments("--window-size=1280x800");
	     chromeOptions.addArguments("--verbose");
       chromeOptions.addArguments("--no-sandbox");

        driver = new ChromeDriver(chromeOptions);

        String currentUsersWorkingDir = System.getProperty("user.dir");
	    System.out.println(currentUsersWorkingDir);

    	System.setProperty("webdriver.chrome.driver",currentUsersWorkingDir+"/chromedriver");

    }

	@AfterTest
	public void afterTest() {
		driver.quit();
	}

    @Test(priority=1)
    public void ValidateSMDMRegistration() {

    	String baseUrl = "https://api.mdmdev.thoughtworks.net/rolzog/?serial=C02L70VFF5YW";
        String expectedTitle = "Rolzog: Register your ThoughtWorks laptop";
        driver.get(baseUrl);
        String actualTitle = driver.getTitle();

        SoftAssert softAssertion= new SoftAssert();

        //Validate title
        softAssertion.assertEquals(actualTitle, expectedTitle);
        //Validate redirection to Okta page
        driver.findElement(By.linkText("Register")).click();

        String expectedOktaTitle = "login.okta.com";

        //ThoughtWorks UD - Sign In
        String actualOktaTitle = driver.getTitle();

        softAssertion.assertEquals(actualOktaTitle, actualOktaTitle);

        WebElement userName =  ((ChromeDriver) driver).findElement(By.id("okta-signin-username"));
        WebElement password =  ((ChromeDriver) driver).findElement(By.id("okta-signin-password"));

        String usernameOkta = System.getenv("okta_username");
        String passwordOkta = System.getenv("okta_password");

        userName.sendKeys(usernameOkta);
        password.sendKeys(passwordOkta);
        password.submit();

        //Validate the landing page : should be the ack page
        //Assert.assertEquals(driver.getCurrentUrl(), "https://api.mdmdev.thoughtworks.net/rolzog/register?live=1&serial=C02L70VFF5YW" );
        //Validate message on the landing page
        String successMessage = "Please reboot to complete the enrolment process.";
        String bodyText = driver.findElement(By.tagName("body")).getText();
        driver.manage().timeouts().implicitlyWait(10000, TimeUnit.SECONDS);
        Assert.assertTrue(bodyText.contains(successMessage));

            }

    @Test(enabled = false)
    public void ValidateAssetStatusinServiceNow() {
    	 // Validate the status of the resource in ServiceNow:-
        String serviceNowUrl = "https://thoughtworksdev.service-now.com/navpage.do";

        driver.get(serviceNowUrl);
        WebElement userNameSN =  ((ChromeDriver) driver).findElement(By.id("user_name"));
        WebElement passwordSN =  ((ChromeDriver) driver).findElement(By.id("user_password"));

        //  WebElement password = ((ChromeDriver) driver).findElementsById("okta-signin-password");
        userNameSN.sendKeys("ATFAdmin");
        passwordSN.sendKeys("");
        passwordSN.submit();

        //Click on Impersonate user link:
        driver.findElement(By.className("user-name hidden-xs hidden-sm")).click();

        //*[@class='dropdown-menu’]//*[name()=‘impersonate’]

        String xpathImpersonate = "*[@class='dropdown-menu’]//*[text()=‘Impersonate User’]";
        ((ChromeDriver) driver).findElementByXPath(xpathImpersonate).click();
        driver.manage().timeouts().implicitlyWait(10000, TimeUnit.SECONDS);

    }
}
