import axios from "axios";
import FormData from "form-data";
import fs from "fs";

export const generateFromAI = async ({ headline, image }) => {
  const formData = new FormData();
  formData.append("headline", headline);

  if (image) {
    formData.append("image", fs.createReadStream(image));
  }

  const response = await axios.post(
    "http://localhost:8000/generate",
    formData,
    {
      headers: formData.getHeaders(),
      timeout: 60000,
    }
  );

  return response.data;
};
