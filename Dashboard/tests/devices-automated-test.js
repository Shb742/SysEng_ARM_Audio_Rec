const {Builder, By, until} = require('selenium-webdriver');
const assert = require('assert');

(async function example() {
    const driver = await new Builder().forBrowser('chrome').build();

    try {
        await driver.get('https://edvs.uk.to/login');

        await driver.findElement(By.name('username')).sendKeys('kimia');
        await driver.findElement(By.name('password')).sendKeys('123kimia321');
        await driver.findElement(By.name('login')).click();
        await driver.get('https://edvs.uk.to/devices');

        var row = await driver.findElement(By.xpath("//*[@id='deviceTable']//tbody//tr")).getAttribute("innerHTML");
        var table = await driver.findElement(By.xpath("//*[@id='deviceTable']//tbody")).getAttribute("innerHTML");
        var len  = Math.floor((table.length)/(row.length));
        
        //this has to manually change to ensure the physical nodes and the devices are the same number.
        assert.equal(len, 2);

      }
         catch(UnhandledPromiseRejectionWarning){
           console.log("ERROR!!");

         }
         finally {
             await driver.quit();
         }
     })();
