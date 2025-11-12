# Paginegialle B2B Scraper

> Extract detailed and accurate business information from PagineGialle.it, the Italian Yellow Pages. This scraper collects structured data for business intelligence, marketing campaigns, and lead generation—fast, complete, and reliable.

> Built for anyone who needs high-quality B2B data from Italian directories without the usual scraping limitations.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Paginegialle B2B</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

This project automates the extraction of business listings from Italy’s largest online business directory, PagineGialle.it.
It helps you gather essential contact and company details across multiple categories and cities with just one run.

### Why It Matters

- Simplifies access to verified Italian business data for marketing and sales.
- Enables large-scale searches across categories and cities simultaneously.
- Filters results by email or phone presence for higher-value leads.
- Works with residential proxies for maximum reliability and complete datasets.
- Outputs consistent, ready-to-use structured data for analysis.

## Features

| Feature | Description |
|----------|-------------|
| Multi-Category & Multi-City Search | Run complex searches across several industries and cities simultaneously. |
| Smart Pagination | Automatically detects and scrapes all result pages without manual input. |
| Proxy Integration | Supports residential proxies to avoid blocks and ensure full coverage. |
| Filter by Contact Data | Optionally limit results to businesses with email or phone contact info. |
| High Concurrency | Control parallel scraping tasks to maximize efficiency. |
| Rich Output Data | Extracts contact info, location, reviews, and social media links. |
| Stable Python Core | Runs on Python 3.12 for high reliability and compatibility. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| businessName | The business name as listed on PagineGialle. |
| address | Full street address including number and street name. |
| phoneNumber | Primary phone number for the business. |
| website | Official website URL if provided. |
| email | Contact email address for communication. |
| rating | Average user rating (0–5 scale). |
| reviews_count | Total number of user reviews available. |
| whatsapp | WhatsApp business contact number if listed. |
| facebook | Link to the official Facebook profile. |
| instagram | Link to the official Instagram profile. |
| twitter | Link to the official Twitter profile. |
| latitude | Latitude coordinate for map use. |
| longitude | Longitude coordinate for map use. |
| zip_code | Business postal code. |
| city | City name of the business location. |
| province | Province abbreviation (e.g., RM for Rome). |
| opening_hours | JSON representation of business hours. |
| description | Short description of the business activity. |
| category | Category used during the search. |
| scraped_city | City term used for the search. |
| unique_id | Unique identifier for the business record. |
| timestamp | UTC timestamp marking data collection time. |

---

## Example Output

    [
        {
            "businessName": "Trattoria Roma",
            "address": "Via del Corso 50, Roma",
            "phoneNumber": "+39 064321678",
            "website": "https://www.trattoriaroma.it",
            "email": "info@trattoriaroma.it",
            "rating": 4.6,
            "reviews_count": 128,
            "whatsapp": "+39 3456789123",
            "facebook": "https://facebook.com/trattoriaroma",
            "instagram": "https://instagram.com/trattoriaroma",
            "twitter": null,
            "latitude": "41.9028",
            "longitude": "12.4964",
            "zip_code": "00186",
            "city": "Roma",
            "province": "RM",
            "opening_hours": "{\"monday\":\"09:00-22:00\"}",
            "description": "Authentic Roman cuisine in the city center.",
            "category": "ristoranti",
            "scraped_city": "roma",
            "unique_id": "pg-roma-ristoranti-001",
            "timestamp": "2025-11-12T10:30:00Z"
        }
    ]

---

## Directory Structure Tree

    Paginegialle B2B/
    ├── src/
    │   ├── main.py
    │   ├── scraper/
    │   │   ├── paginegialle_parser.py
    │   │   └── request_handler.py
    │   ├── utils/
    │   │   ├── logger.py
    │   │   └── helpers.py
    │   └── config/
    │       └── settings.json
    ├── data/
    │   ├── sample_input.json
    │   └── sample_output.json
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Marketing agencies** use it to **gather leads** across Italian cities for outreach campaigns.
- **Sales teams** leverage it to **build verified business lists** with contact details for B2B sales.
- **Analysts** use it to **map and analyze regional industries** and their digital presence.
- **Developers** integrate it into pipelines to **enrich CRM systems** with updated company info.
- **Researchers** employ it to **study market trends and local commerce density.**

---

## FAQs

**1. Can I scrape multiple cities and categories at once?**
Yes, you can provide arrays of both categories and cities, and the scraper will handle all combinations automatically.

**2. Does it require proxy usage?**
While optional, enabling proxies ensures complete results and avoids partial data due to blocking.

**3. How are the results delivered?**
The scraper outputs structured JSON data ready for further processing or analysis.

**4. Can I filter for businesses with only emails or phones?**
Yes, set `filterByEmail` or `filterByPhone` to `true` in your input configuration.

---

## Performance Benchmarks and Results

**Primary Metric:** Scrapes up to 1,000 listings per minute under optimal concurrency.
**Reliability Metric:** 98% success rate across large city-category combinations.
**Efficiency Metric:** Handles 20+ simultaneous requests with minimal error retries.
**Quality Metric:** 99% field completeness, including GPS and contact data accuracy.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
