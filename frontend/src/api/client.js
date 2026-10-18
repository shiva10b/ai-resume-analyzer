import axios from "axios";

const API_BASE = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8001"
).replace(/\/+$/, "");

export async function analyzeResume(file, jobDescription) {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("job_description", jobDescription);

  const response = await axios.post(`${API_BASE}/api/analyze`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
}
