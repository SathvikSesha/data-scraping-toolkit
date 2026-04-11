import express from "express";
import cors from "cors";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";
import Email from "./models/email.model.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();

app.use(express.json());
app.use(cors());

app.post("/analyze-emails", async (req, res) => {
  const { keyword } = req.body;

  if (!keyword || typeof keyword !== "string") {
    return res.status(400).json({ message: "Keyword required" });
  }

  const scriptPath = path.join(__dirname, "analyzer", "email_analyzer.py");
  const py = spawn("python", [scriptPath, keyword], { cwd: __dirname });

  let stdout = "";
  let stderr = "";
  let responded = false;

  const fail = (status, message) => {
    if (responded) return;
    responded = true;
    res.status(status).json({ message });
  };

  py.stdout.on("data", (chunk) => {
    stdout += chunk.toString();
  });

  py.stderr.on("data", (chunk) => {
    stderr += chunk.toString();
  });

  py.on("error", (err) => {
    console.error(err);
    fail(500, "Analysis failed");
  });

  py.on("close", async (code) => {
    if (responded) return;

    if (code !== 0) {
      console.error(stderr || `Python exited with code ${code}`);
      return fail(500, "Analysis failed");
    }

    let rows;
    try {
      rows = JSON.parse(stdout.trim());
    } catch (e) {
      console.error("Invalid JSON:", stdout, e);
      return fail(500, "Invalid analyzer output");
    }

    if (!Array.isArray(rows)) {
      return fail(500, "Invalid data format");
    }

    try {
      // 🔥 IMPORTANT FIX: Clear ALL old data
      await Email.deleteMany({});

      if (rows.length > 0) {
        await Email.insertMany(rows.map((r) => ({ ...r, keyword })));
      }

      responded = true;
      res.status(200).json({
        message: "Analysis completed",
        count: rows.length,
      });
    } catch (err) {
      console.error(err);
      fail(500, "Database error");
    }
  });
});

// 🔹 Fetch emails
app.get("/emails", async (req, res) => {
  try {
    const emails = await Email.find();
    res.json(emails);
  } catch (error) {
    res.status(500).json({ message: "Error fetching emails" });
  }
});

export default app;
