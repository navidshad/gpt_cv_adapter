const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const generatePDF = async () => {

	const html_file_path = path.join(process.env.HTML_FILE_PATH) //process.env.HTML_FILE_PATH;

	const browser = await puppeteer.launch({
		headless: true,
		executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
		args: ['--no-sandbox', '--disable-setuid-sandbox']
	});

	const page = await browser.newPage();
	await page.goto(`file://${html_file_path}`, {
		waitUntil: 'networkidle0'
	});

	await page.setViewport({
		width: 1280,
		height: 1024
	});

	const container = await page.$('#cv-container');

	// get hight of body
	const bodyHeight = await container.evaluate((_container) => {
		return _container.clientHeight;
	});

	const pdf = await page.pdf({
		width: 1280 / 96 + 'in',
		height: ((bodyHeight / 96) - 3) + 'in',
	});

	await browser.close();

	const pdf_file_path = html_file_path.replace('.html', '.pdf');

	// Save pdf file
	fs.writeFile(pdf_file_path, pdf, (err) => {
		if (err) {
			console.log(err);
		}
	});
}

generatePDF();