// expects 1 arg:
// argv[2] => url to archive

const puppeteer = require('puppeteer');
const sleep = require('sleep');

(async () => {
    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
//        headless: false,
//        slowMo: 250,
    });
    const page = await browser.newPage();
    await page.setViewport({width: 1280, height: 2000});

    await page.goto('https://archive.is');
    var text = await page.$('#url');
    await text.type(process.argv[2], {delay: 10});

    var button = await page.$('input[type=submit]');
    await button.click();

    sleep.sleep(3);

    /*await page.waitForNavigation();
    console.log(page.url());*/

    await browser.close();
})().catch((err) => {
    console.log('error: ', err);
});
