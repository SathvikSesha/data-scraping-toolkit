import express from "express";
import Quote from "../backend/models/quotes.model.js";
import cors from "cors";
import mongoose from "mongoose";
import { exec } from "child_process";

const app = express();

app.use(express.json());
app.use(cors());

app.get("/quotes", async (req, res) => {
  try {
    const quotes = await Quote.find();
    res.status(200).json(quotes);
  } catch (error) {
    console.log(error);
    res.status(500).json({ message: "Server error" });
  }
});

app.post("/scrape", (req, res) => {
  exec("python ../quotes_scraper.py", (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error}`);
      return res.status(500).json({ message: "Scraping failed" });
    }

    console.log(stdout);
    res.status(200).json({ message: "Scraping completed successfully" });
  });
});

app.post("/scrape-emails", (req, res) => {
  const { url } = req.body;

  if (!url) {
    return res.status(400).json({ message: "URL required" });
  }

  exec(
    `python ../email_scraper/email_extractor.py "${url}"`,
    (error, stdout, stderr) => {
      if (error) {
        console.error(error);
        return res.status(500).json({ message: "Email scraping failed" });
      }

      console.log(stdout);
      res.status(200).json({ message: "Emails scraped successfully" });
    },
  );
});

app.get("/emails", async (req, res) => {
  try {
    const db = mongoose.connection.db;

    if (!db) {
      return res.status(500).json({ message: "Database not initialized" });
    }

    const emails = await db.collection("emails").find().toArray();
    res.status(200).json(emails);
  } catch (error) {
    console.log(error);
    res.status(500).json({ message: "Error fetching emails" });
  }
});

export default app;
