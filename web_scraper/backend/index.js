import app from "./app.js";
import connectDB from "./db.js";
import "dotenv/config";
const server = async () => {
  try {
    await connectDB();
    app.listen(process.env.PORT, () => {
      console.log(`Server is running on port ${process.env.PORT}`);
    });
  } catch (error) {
    console.log(`Server error ${error}`);
    process.exit(1);
  }
};
server();
