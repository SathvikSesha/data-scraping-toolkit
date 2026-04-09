import express from "express";
import Quote from "../backend/models/quotes.model.js";
import cors from "cors";

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

export default app;
