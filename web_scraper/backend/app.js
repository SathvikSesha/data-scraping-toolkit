import express from "express";
import Quote from "../backend/models/quotes.model.js";
import cors from "cors";
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

export default app;
