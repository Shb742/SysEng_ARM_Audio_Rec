const {Builder, By, until} = require('selenium-webdriver');
const assert = require('assert');

(async function example() {
    const driver = await new Builder().forBrowser('chrome').build();

    try {
        await driver.get('https://edvs.uk.to/login');

        await driver.findElement(By.name('username')).sendKeys('kimia');
        await driver.findElement(By.name('password')).sendKeys('123kimia321');
        await driver.findElement(By.name('login')).click();
        var loginTime = new Date().toLocaleTimeString();
        await driver.get('https://edvs.uk.to/users');
        var i =0;
        do{
          i++;
          var d = await driver.findElement(By.xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/table/tbody/tr["+i+"]/td[1]")).getAttribute("innerHTML");
        }while(d!=="kimia")

        var loginTimeRecorded = await driver.findElement(By.xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/div/table/tbody/tr["+i+"]/td[2]")).getAttribute("innerHTML");
        assert.equal("GMT", "GMT");



    }
    catch(UnhandledPromiseRejectionWarning){
      console.log("ERROR!!");

    }
    finally {
        await driver.quit();
    }
})();
