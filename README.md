💡 The Problem
Apartment hunting online is time-consuming and inefficient. Most sites don’t offer custom alerts or APIs, and availability changes daily. I wanted a hands-off way to be notified when 2-bedroom units became available on specific floors (1st, 2nd, or 3rd).

🛠️ The Stack
Python 3.12
Requests + BeautifulSoup for scraping
SendGrid for email notifications
Azure Functions (Timer Trigger) to automate it
GitHub for version control
🔎 How It Works
Every 30 minutes, an Azure Function runs my Python script.
The script requests the HTML from the Cortland Las Colinas apartment page.
It uses BeautifulSoup to parse the DOM and extract apartment data (unit number, floor, bedrooms, price).
If a matching 2-bedroom unit on floor 1, 2, or 3 is found, it sends an email via SendGrid.
🧠 Why I Chose Azure Functions
Azure Functions gave me:

💸 Zero cost (fits in the free tier)
⚡ A built-in timer trigger (like cron jobs in the cloud)
🧼 Clean deployment with func azure functionapp publish
📧 Email Alerts with SendGrid
SendGrid makes it easy to send email securely using an API key. I set up a verified sender and passed in a recipient list — done.

📁 The Code
You can find the full source code on GitHub:

👉 https://github.com/rajendar38/scrapeweb

Includes:

__init__.py with scraping + email logic
function.json for scheduling
requirements.txt for dependencies
🚀 Want to Build Your Own?
If you’re curious about serverless Python automation or want to set up alerts for any site, this is a great weekend project. Modify the scraper, change the trigger interval, or even send SMS alerts with Twilio!

🙌 Final Thoughts
This project helped me:

Save time apartment hunting
Learn how to deploy production Python code to Azure
Automate real-life decisions with serverless tech
Give it a try and let me know what you build!

If this helped you or inspired your next automation project, consider giving the repo a ⭐ on GitHub or dropping a comment below.

Happy scraping!
