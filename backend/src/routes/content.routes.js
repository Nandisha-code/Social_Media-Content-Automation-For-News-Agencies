import express from "express";
import { upload } from "../middlewares/upload.middleware.js";
import {
  generateContent,
  getAllContent,
} from "../controllers/content.controller.js";

const router = express.Router();

router.post("/generate", upload.single("image"), generateContent);
router.get("/", getAllContent);

export default router;
