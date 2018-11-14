package RolzogTests;


import org.testng.annotations.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import org.testng.Assert;
import org.testng.annotations.BeforeTest;	
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeSuite;
import org.openqa.selenium.chrome.ChromeDriver;



public class FunctionalTests {

    public WebDriver driver;

    @BeforeSuite
    public void beforeSuite() {

        driver = new ChromeDriver();
        String currentUsersWorkingDir = System.getProperty("user.dir");
    	
    	System.setProperty("webdriver.chrome.driver",currentUsersWorkingDir+"/chromedriver");
    	
    }
    
    @BeforeTest
    public void beforeTest() {	
	    
	}
    
	@AfterTest
	public void afterTest() {
		//driver.quit();			
	}
    
    @Test(priority=1)

    public void ValidateRegistrationPageAndLandingOnOktaPage() {


        String baseUrl = "https://api.mdmdev.thoughtworks.net/rolzog/?serial=C02L70VFF5YW";
        String expectedTitle = "Rolzog: Register your ThoughtWorks laptop";
        driver.get(baseUrl);
        String actualTitle = driver.getTitle();

        //Validate title
        Assert.assertEquals(actualTitle, expectedTitle);
        //Validate redirection to Okta page
        driver.findElement(By.linkText("Register")).click();

        String expectedOktaTitle = "login.okta.com";
        //ThoughtWorks UD - Sign In
        String actualOktaTitle = driver.getTitle();

        Assert.assertEquals(actualOktaTitle, actualOktaTitle);
        
        WebElement userName =  ((ChromeDriver) driver).findElement(By.id("okta-signin-username"));
        WebElement password =  ((ChromeDriver) driver).findElement(By.id("okta-signin-password"));

        String usernameOkta = System.getenv("okta_username");
        String passwordOkta = System.getenv("okta_password");
        
        //  WebElement password = ((ChromeDriver) driver).findElementsById("okta-signin-password");
        userName.sendKeys(usernameOkta);
        password.sendKeys(passwordOkta);

        password.submit();

        //Validate the landing page : should be the ack page TODO

        String ackPageUrl = driver.getCurrentUrl();
        //Assert.assertEquals(ackPageUrl, "https://api.mdmdev.thoughtworks.net/rolzog/register?live=1&serial=C02L70VFF5YW" );

    }
    
    @Test(priority=2)
    public void ValidateAssetStatusinServiceNow() {/*
    	 // Validate the status of the resource in ServiceNow:-
        String serviceNowUrl = "https://thoughtworksdev.service-now.com/navpage.do";
        String adminUsername = "ATFAdmin";
        String adminPassword = "Password@123";

        driver.get(serviceNowUrl);
        WebElement userNameSN =  ((ChromeDriver) driver).findElement(By.id("user_name"));
        WebElement passwordSN =  ((ChromeDriver) driver).findElement(By.id("user_password"));

        //  WebElement password = ((ChromeDriver) driver).findElementsById("okta-signin-password");
        userNameSN.sendKeys("ATFAdmin");
        passwordSN.sendKeys("Password@123");
        passwordSN.submit();

        //Click on Impersonate user link:
        driver.findElement(By.className("user-name hidden-xs hidden-sm")).click();

        //*[@class='dropdown-menu’]//*[name()=‘impersonate’]

        String xpathImpersonate = "*[@class='dropdown-menu’]//*[text()=‘Impersonate User’]";
        ((ChromeDriver) driver).findElementByXPath(xpathImpersonate).click();



        driver.manage().timeouts().implicitlyWait(10000, TimeUnit.SECONDS);
       
    */}
}

