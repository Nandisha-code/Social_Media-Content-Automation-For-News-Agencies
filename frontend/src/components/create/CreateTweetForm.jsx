import { useState } from "react";
import { useGenerateContent } from "../../hooks/useGenerateContent";

export default function CreateTweetForm({ onGenerated }) {
  const [headline, setHeadline] = useState("");
  const [image, setImage] = useState(null);

  const { mutate, isLoading } = useGenerateContent();

  const handleSubmit = () => {
    const formData = new FormData();
    formData.append("headline", headline);
    if (image) formData.append("image", image);

    mutate(formData, {
      onSuccess: (data) => onGenerated(data),
    });
  };

  return (
    <div className="bg-[#0f172a] p-6 rounded-xl space-y-4">
      <h2 className="text-xl font-semibold text-white">
        Create Content
      </h2>

      {/* Headline */}
      <input
        type="text"
        placeholder="Enter your news headline..."
        value={headline}
        onChange={(e) => setHeadline(e.target.value)}
        className="w-full p-3 rounded bg-[#020617] border border-slate-700 text-white"
      />

      {/* Image */}
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImage(e.target.files[0])}
        className="text-slate-300"
      />

      {/* Generate */}
      <button
        onClick={handleSubmit}
        disabled={isLoading}
        className="w-full bg-gradient-to-r from-cyan-400 to-blue-500 text-black font-semibold py-3 rounded"
      >
        {isLoading ? "Generating..." : "Generate"}
      </button>
    </div>
  );
}
