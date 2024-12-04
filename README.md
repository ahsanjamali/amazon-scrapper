# Amazon Scraper Project

This project consists of two parts:

- Frontend: A Next.js web application to display scraped products
- Backend: A Python scraper to collect product data from Amazon

## Frontend

Navigate to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

## Backend

Navigate to the backend directory:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python scraper.py
```

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
