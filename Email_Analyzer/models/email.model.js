import mongoose from "mongoose";

const emailSchema = new mongoose.Schema({
  sender: String,
  subject: String,
  date: String,
  keyword: {
    type: String,
    index: true,
  },
});

const Email = mongoose.model("Email", emailSchema);

export default Email;
