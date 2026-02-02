import express from "express";
import cors from "cors";

import contentRoutes from "./routes/content.routes.js";

const app = express();

app.use(cors());
app.use(express.json());
app.use("/uploads", express.static("uploads"));

app.use("/api/content", contentRoutes);

app.get("/health", (req, res) => {
  res.json({ status: "Backend running" });
});

export default app;
