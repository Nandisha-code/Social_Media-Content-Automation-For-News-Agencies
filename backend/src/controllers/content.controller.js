import Content from "../models/Content.model.js";
import { generateFromAI } from "../services/ai.service.js";

export const generateContent = async (req, res) => {
  try {
    const { headline } = req.body;

    if (!headline) {
      return res.status(400).json({ error: "Headline required" });
    }

    const imagePath = req.file ? req.file.path : null;

    const aiResult = await generateFromAI({
      headline,
      image: imagePath,
    });

    const content = await Content.create({
      headline,
      imageUrl: imagePath,
      imageCaption: aiResult.image_caption,
      tweet: aiResult.tweet,
    });

    res.status(201).json(content);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

export const getAllContent = async (req, res) => {
  const data = await Content.find().sort({ createdAt: -1 });
  res.json(data);
};
    