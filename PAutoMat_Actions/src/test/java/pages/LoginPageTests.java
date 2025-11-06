package pages;

import org.junit.Assert;
import org.junit.Test;

public class LoginPageTests {

    @Test
    public void dummyFailingUiTest_OnPurpose() {
        // This test is intentionally incorrect to demonstrate a failing test in reports
        String pageTitle = "Login"; // pretend fetched from driver
        Assert.assertEquals("Home", pageTitle);
    }

    @Test
    public void simpleAssertion_Pass() {
        Assert.assertTrue(true);
    }
}
