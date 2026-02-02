import mongoose from "mongoose";

const contentSchema = new mongoose.Schema(
  {
    headline: {
      type: String,
      required: true,
    },
    imageUrl: {
      type: String,
    },
    imageCaption: {
      type: String,
    },
    tweet: {
      type: String,
      required: true,
    },
    status: {
      type: String,
      enum: ["draft", "approved"],
      default: "draft",
    },
  },
  { timestamps: true }
);

export default mongoose.model("Content", contentSchema);
    