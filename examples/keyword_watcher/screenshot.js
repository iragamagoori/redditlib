// expects 2 args:
// argv[2] => url to fetch
// argv[3] => filename to save screenshot at

const puppeteer = require('puppeteer');
const sleep = require('sleep');

(async () => {
    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
        //headless: false,
        //slowMo: 250,
    });
    const page = await browser.newPage();
    await page.setViewport({width: 1280, height: 2000});
    await page.goto(process.argv[2]);
    sleep.sleep(1);
    await page.screenshot({path: process.argv[3]});

    await browser.close();
})().catch((err) => {
    console.log('error: ', err);
});
