import axios from "axios";

const API_BASE = "http://localhost:5000/api/content";

export const generateContentApi = async (formData) => {
  const res = await axios.post(`${API_BASE}/generate`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return res.data;
};
